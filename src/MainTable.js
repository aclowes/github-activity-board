import React from 'react';
import {Table} from 'react-bootstrap';
import {Link} from 'react-router-dom'

export default props => {
  if (!props.users) {
    return <div>Loading...</div>
  }
  props.users.sort((a, b) =>
    b.activity_score - a.activity_score
  );
  const rows = props.users.map((user) =>
    <tr key={user.login}>
      <td><Link to={'/user/' + user.login}>{user.login}</Link></td>
      <td>{user.name}</td>
      <td>{user.comments.length}</td>
      <td>{user.pull_requests.length}</td>
      <td>{user.lines_added}</td>
      <td>{user.lines_deleted}</td>
      <td>{Math.round(user.activity_score * 10) / 10}</td>
    </tr>
  );
  const organization = window.PUBLIC_URL.slice(1);
  return (
    <div>
      <p>View recent GitHub pull requests and comments by contributor
        to organization <a href={`https://github.com/${organization}/`}>{organization}</a>.
        Get the source code on <a href='https:github.com/aclowes/github-activity-board'>
          GitHub</a>.
        Deployed using the <a href='https://pypi.org/project/yawns'>YAWN</a> python workflow tool.
      </p>
      <Table striped bordered condensed hover>
        <thead>
        <tr>
          <th>Login</th>
          <th>Name</th>
          <th>Comments</th>
          <th>Pull Requests</th>
          <th>Additions</th>
          <th>Deletions</th>
          <th>Score</th>
        </tr>
        </thead>
        <tbody>
        {rows}
        </tbody>
      </Table>
    </div>
  );
}
