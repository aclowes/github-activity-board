import React from 'react';
import {Table} from 'react-bootstrap';
import moment from 'moment';

export default (props) => {
  const rows = props.pulls.map(pr =>
    <tr key={`${pr.repository.nameWithOwner}/${pr.number}`}>
      <td>
        <a href={`https://github.com/${pr.repository.nameWithOwner}/pull/${pr.number}`}>
          {moment(pr.publishedAt).fromNow()}
        </a>
      </td>
      <td>{pr.title}</td>
      <td>+{pr.additions}/-{pr.deletions}</td>
    </tr>
  );
  return (
    <Table striped bordered condensed hover>
      <thead>
      <tr>
        <th>Date</th>
        <th>Title</th>
        <th>Changes</th>
      </tr>
      </thead>
      <tbody>
      {rows}
      </tbody>
    </Table>
  );
}

