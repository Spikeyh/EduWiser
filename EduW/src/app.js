import React from 'react';
import { Component } from 'react';
import './app.scss';
import { Provider } from 'react-redux';
import store from './store';

class App extends Component {
  render() {
    return <Provider store={store}>{this.props.children}</Provider>;
    return this.props.children;
  }
}

export default App;
