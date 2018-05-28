import os

import requests
import yaml


def client(method, endpoint, json):
    token = os.environ['YAWN_TOKEN']
    headers = {'Authorization': f'Token {token}'}
    url = f'https://yawn.live/api/{endpoint}'
    response = requests.request(method, url, json=json, headers=headers)
    print(response.content)
    response.raise_for_status()
    return response


def create_workflow():
    workflow = yaml.load(open('task.yaml').read())
    return client('post', 'workflows/', workflow).json()['id']


def start_run(wkfl_id):
    data = {'workflow_id': wkfl_id}
    client('post', 'runs/', data)


if __name__ == '__main__':
    wkfl_id = create_workflow()
    start_run(wkfl_id)
