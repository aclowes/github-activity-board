import React, {Component} from 'react';
import 'whatwg-fetch';
import {Navbar} from 'react-bootstrap';
import {HashRouter, Route, Link} from 'react-router-dom'

import 'bootswatch/united/bootstrap.css';
import './App.css';

import MainTable from './MainTable'
import User from './User'

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = {users: null};
  }

  componentDidMount() {
    fetch(`${window.PUBLIC_URL}/output.json`, {
      method: 'get',
    }).then((response) => {
      return response.json()
    }).then((data) => {
      this.setState({users: data});
    })
  }

  render() {
    return (
      <HashRouter basename="/">
        <div>
          <Navbar>
            <Navbar.Header>
              <Navbar.Brand>
                <Link to="/">GitHub Activity Board</Link>
              </Navbar.Brand>
            </Navbar.Header>
          </Navbar>
          <div className="container">
            <Route exact path="/" render={(props) => (
              <MainTable users={this.state.users}/>
            )}/>
            <Route exact path="/user/:login" render={(props) => (
              <User user={this.state.users && this.state.users.find(
                user => user.login === props.match.params.login
              )}/>
            )}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}
