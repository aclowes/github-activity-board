import React from 'react';
import {Tabs, Tab} from 'react-bootstrap';

import PullRequests from './PullRequests';
import Comments from './Comments';

export default (props) => {
  const user = props.user;
  if (!user) {
    return <div>Loading...</div>
  }
  return (
    <div>
      <h2>{user.login}</h2>
      <Tabs id={1}>
        <Tab eventKey={1} title="Pull Requests">
          <PullRequests pulls={user.pull_requests}/>
        </Tab>
        <Tab eventKey={2} title="Comments">
          <Comments comments={user.comments}/>
        </Tab>
      </Tabs>
    </div>
  );
}

