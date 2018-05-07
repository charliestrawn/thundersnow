import React, {Component} from 'react';
import { BrowserRouter as Route, Redirect } from "react-router-dom";

import fakeAuth from '../utils/auth';

const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route
      {...rest}
      render={props =>
        fakeAuth.isAuthenticated ? (
          <Component {...props} />
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: props.location }
            }}
          />
        )
      }
    />
);

class LoginView extends Component {
    constructor(props) {
        super(props);
        this.state = {
            redirectToReferrer: false,
            email: '',
            password: ''
        };

        this.onChange = this.onChange.bind(this);
        // this.login = this.login.bind(this);

    }

    onChange = e => {
        this.setState({[e.target.name]: e.target.value});
    }

    login = e => {
        e.preventDefault();
        console.log('called login');
        console.log('redirectToReferrer: ');
        console.log(this.state.redirectToReferrer);
      fakeAuth.authenticate(this.state.email, this.state.password, () => {
        this.setState(() => ({
          redirectToReferrer: true
        }))
      });
      console.log('redirectToReferrer: ');
      console.log(this.state.redirectToReferrer);
    }

    render() {
      const { from } = this.props.location.state || { from: { pathname: '/' } }
      const { redirectToReferrer } = this.state

      if (redirectToReferrer === true) {
        console.log(from);
        return (<Redirect to={from} />)
      }

      return (
        <div className="col-md-4">
            <h1>Login</h1>
            <form className="form" onSubmit={this.login}>
                <div className="form-group">
                <label>Email</label>
                    <input type="text" className="form-control" name="email" required onChange={this.onChange} />
                </div>
                <div className="form-group">
                <label>Password</label>
                    <input type="password" className="form-control" name="password" required onChange={this.onChange}/>
                </div>
                <div>
                    <button type="submit" className="btn btn-default">Login</button>
                </div>
            </form>
            </div>
      )
    }
}

export default LoginView;
