import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import Terminal from 'terminal-in-react';

class App extends Component {
  constructor (props) {
    super(props);
    this.props = props;
    this.state = {
      username: "guest",
    };
  }

  commandParse(cmd, print) {
    axios.post('http://0.0.0.0:8001/execute', {
        cmd: cmd,
        username: this.state["username"]
      })
      .then(function (response) {
        console.log(response);
        print(response["data"]["execute"])
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh"
        }}
      >
        <Terminal
          color='green'
          backgroundColor='black'
          barColor='black'
          style={{ fontWeight: "bold", fontSize: "1em" }}
          commandPassThrough={(cmd, print) => {
            // do something async
            this.commandParse(cmd, print);
          }}
          msg='Welcome to CLI Tasks. You can start by running commands.'
        />
      </div>
    );
  }
}
export default App;
