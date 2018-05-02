import React, { Component } from 'react';
import './App.css';

import PaymentsView from './components/PaymentsView';

class App extends Component {

  render() {
    return (
      <div className="App">
        <header className="navbar navbar-default navber-fixed-top">
          <div className="container">
              <div className="navbar-header">
                <a className="navbar-brand" href="/">Payment Reporter</a>
              </div>
              <nav className="collapse navbar-collapse bs-navbar-collapse">
                <ul className="nav navbar-nav navbar-right">
                    <li><a href="/#/logout">Logout</a></li>
                </ul>
              </nav>
          </div>

        </header>
        <PaymentsView />
      </div>
    );
  }
}

export default App;
