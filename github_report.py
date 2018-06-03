"""
Get user comments and PRs from GitHub
"""
import json
import os
import statistics
import math
import datetime
import time

from operator import itemgetter

import requests

# inputs
token = os.environ['GITHUB_TOKEN']
organization = os.environ['GITHUB_ORGANIZATION']
since_date = (datetime.date.today() - datetime.timedelta(days=180)).strftime('%Y-%m-%d')

graphql_url = 'https://api.github.com/graphql'
pr_url = 'https://api.github.com/repos/{repo_name}/pulls/{pr_id}'
session = requests.Session()
session.headers.update({'Authorization': 'bearer {}'.format(token)})

users_query = """
query get($last: Int, $before: String) {
  organization(login: "%s") {
    members(last: $last, before: $before) {
      nodes {
        login
        name
      }
      pageInfo {
        startCursor
        hasPreviousPage
      }
    }
  }
}
""" % (organization,)
commit_comments_query = """
query get($login: String!, $last: Int, $before: String) {
  user(login: $login) {
    commitComments(last: $last, before: $before) {
      nodes {
        url
        body
        publishedAt
      }
      pageInfo {
        startCursor
        hasPreviousPage
      }
    }
  }
}
"""
issue_comments_query = """
query get($login: String!, $last: Int, $before: String) {
  user(login: $login) {
    issueComments(last: $last, before: $before) {
      nodes {
        body
        publishedAt
        issue {
          url
        }
      }
      pageInfo {
        startCursor
        hasPreviousPage
      }
    }
  }
}
"""
pull_requests_query = """
query get($login: String!, $last: Int, $before: String) {
  user(login: $login) {
    pullRequests(last: $last, before: $before) {
      nodes {
        title
        body
        publishedAt
        merged
        url
        number
        repository {
          nameWithOwner
        }
      }
      pageInfo {
        startCursor
        hasPreviousPage
      }
    }
  }
}
"""


def call_api(method, url, **kwargs):
    response = session.request(method, url, **kwargs)
    if response.status_code == 403:
        time.sleep(5)
        return call_api(method, url, **kwargs)
    response.raise_for_status()
    return response.json()


def get_graphql(query, login=None):
    start_cursor = None
    results = []

    while True:
        variables = {
            'last': 100,
            'before': start_cursor,
            'login': login
        }
        body = {
            'query': query,
            'variables': json.dumps(variables),
            'operationName': 'get'
        }

        data = call_api('POST', graphql_url, json=body)
        while True:
            if data is None:
                # this happens with cblecker in kubernetes :shrug:
                print('nothing here')
                return results

            if 'errors' in data:
                print(data.pop('errors'))

            if 'nodes' in data:
                break

            assert len(data) == 1, data
            data = list(data.values())[0]

        for row in reversed(data['nodes']):
            if not row:
                print('missing row?')
                continue

            if 'publishedAt' in row and row['publishedAt'] < since_date:
                return results

            if 'merged' in row:  # its a PR, get more details
                try:
                    details = get_pull_requests(row['repository']['nameWithOwner'], row['number'])
                except Exception as exc:
                    print(exc)
                    continue
                row['additions'] = details['additions']
                row['deletions'] = details['deletions']

            results.append(row)

        start_cursor = data['pageInfo']['startCursor']

        if not data['pageInfo']['hasPreviousPage']:
            return results


def get_pull_requests(repo_name, pr_id):
    url = pr_url.format(repo_name=repo_name, pr_id=pr_id)
    headers = {'Accept': 'application/vnd.github.v3+json'}
    return call_api('GET', url, headers=headers)


def get_hot_repos():
    url = 'https://api.github.com/search/repositories'
    params = {
        'sort': 'stars', 'order': 'desc', 'q': 'pushed:>={date}'.format(date=since),
        'per_page': 100, 'page': page + 1}


def levenshtein_distance(s1, s2):
    """from https://stackoverflow.com/a/32558749"""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def get_cached(name, login=None):
    os.makedirs('cache/', exist_ok=True)
    filename = 'cache/{}_{}.json'.format(name.replace('_query', ''), login)
    if os.path.exists(filename):
        return json.load(open(filename))
    query = globals()[name]
    results = get_graphql(query, login)
    json.dump(results, open(filename, 'w'))
    return results


def build_report_task():
    users = get_cached('users_query')
    for user in users:
        print('Loading {}'.format(user['login']))
        user['commit_comments'] = get_cached('commit_comments_query', user['login'])
        user['issue_comments'] = get_cached('issue_comments_query', user['login'])
        user['pull_requests'] = get_cached('pull_requests_query', user['login'])

    comments = []
    pull_requests = []
    lines = []

    for user in users:
        user['comments'] = sorted(user.pop('commit_comments') + user.pop('issue_comments'),
                                  key=itemgetter('publishedAt'), reverse=True)
        if user['comments']:
            comments.append(len(user['comments']))

        user['pull_requests'] = sorted(user['pull_requests'], key=itemgetter('publishedAt'),
                                       reverse=True)
        if user['pull_requests']:
            pull_requests.append(len(user['pull_requests']))

        user['lines_added'] = 0
        user['lines_deleted'] = 0
        for pull_request in user['pull_requests']:
            if pull_request['merged']:
                user['lines_added'] += pull_request['additions']
                user['lines_deleted'] += pull_request['deletions']

        user['log_lines'] = user['lines_added'] + user['lines_deleted']
        if user['log_lines']:
            user['log_lines'] = math.log(user['log_lines'])
            lines.append(user['log_lines'])

    comments_mean = statistics.mean(comments)
    comments_stddev = statistics.stdev(comments)
    pull_requests_mean = statistics.mean(pull_requests)
    pull_requests_stddev = statistics.stdev(pull_requests)
    lines_mean = statistics.mean(lines)
    lines_stddev = statistics.stdev(lines)

    for user in users:
        user_comments_stdev = (len(user['comments']) - comments_mean) / comments_stddev
        user_pull_requests_stdev = (len(user['pull_requests']) - pull_requests_mean) / pull_requests_stddev
        user_lines_stdev = (user['log_lines'] - lines_mean) / lines_stddev
        user['activity_score'] = 5 + user_comments_stdev + user_pull_requests_stdev + user_lines_stdev

    os.makedirs('data/', exist_ok=True)
    json.dump(users, open('data/output.json', 'w'))


if __name__ == '__main__':
    build_report_task()
