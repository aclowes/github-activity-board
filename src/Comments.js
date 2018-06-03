import React from 'react';
import {Table} from 'react-bootstrap';
import moment from 'moment';

export default (props) => {
  const rows = props.comments.map((comment, index) =>
    <tr key={index}>
      <td>
        <a href={comment.url || comment.issue.url} target="_blank">
          {moment(comment.publishedAt).fromNow()}
        </a>
      </td>
      <td>{(comment.url || comment.issue.url).split('/').slice(3, 5).join('/')}</td>
      <td>{comment.body}</td>
    </tr>
  );
  return (
    <Table striped bordered condensed hover>
      <thead>
      <tr>
        <th>Date</th>
        <th>Repository</th>
        <th>Comment</th>
      </tr>
      </thead>
      <tbody>
      {rows}
      </tbody>
    </Table>
  );
}

