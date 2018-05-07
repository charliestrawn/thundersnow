import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Redirect, withRouter } from "react-router-dom";
import './App.css';

import LoginView from './components/LoginView';
import PaymentsView from './components/PaymentsView';
import Members from './components/Members';

import fakeAuth from './utils/auth';

const AuthButton = withRouter(
  ({ history }) =>
    fakeAuth.isAuthenticated ? (
      <p
          onClick={() => {
            fakeAuth.signout(() => history.push("/"));
          }}
        >
          Sign out
      </p>
    ) : (
      <p></p>
    )
);

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    fakeAuth.isAuthenticated === true
      ? <Component {...props} />
      : <Redirect to={{
          pathname: '/login',
          state: { from: props.location }
        }} />
  )} />
);

class Login extends React.Component {
  state = {
    redirectToReferrer: false
  };

  login = () => {
    fakeAuth.authenticate(() => {
      this.setState({ redirectToReferrer: true });
    });
  };

  render() {
    const { from } = this.props.location.state || { from: { pathname: "/" } };
    const { redirectToReferrer } = this.state;

    if (redirectToReferrer) {
      return <Redirect to={from} />;
    }

    return (
      <div>
        <p>You must log in to view the page at {from.pathname}</p>
        <button onClick={this.login}>Log in</button>
      </div>
    );
  }
};

class App extends Component {

  render() {
    return (
      <Router>
        <div className="App">
          <header className="navbar navbar-default navber-fixed-top">
            <div className="container">
                <div className="navbar-header">
                  {/* <a className="navbar-brand" href="/">Payment Reporter</a> */}
                  <Link to="/" className="navbar-brand">Payment Reporter</Link>
                </div>
                <nav className="collapse navbar-collapse bs-navbar-collapse">
                  <ul className="nav navbar-nav">
                    <li>
                      <Link to="/weeks">Weeks</Link>
                    </li>
                    <li>
                      <Link to="/payments">Payments</Link>
                    </li>
                    <li>
                      <Link to="/members">Members</Link>
                    </li>
                  </ul>
                  <ul className="nav navbar-nav navbar-right">
                      <li><AuthButton /></li>
                  </ul>
                </nav>
            </div>

          </header>
          <Route path="/login" component={LoginView} />
          <PrivateRoute exact path="/" component={PaymentsView} />
          <Route path="/members" component={Members} />
        </div>
      </Router>
    );
  }
}

export default App;
