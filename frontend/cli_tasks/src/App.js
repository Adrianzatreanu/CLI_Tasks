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
      msg: "Welcome to CLI Tasks. Please enter your username, or `help` to show a list of helpful commands."
    };
  }

  login(cmd, print) {
    axios.post('http://0.0.0.0:8001/login', {
        username: cmd
      })
      .then(response => {
        console.log(response);
        if (response["data"]["login"] === "success") {
          print("Login successful.")
          this.setState({
            username: cmd,
            msg: "Type `help` to show a list of helpful commands."
          });
        } else {
          print("Login failed. Try again.")
        }
      })
      .catch(function (error) {
        console.log(error);
      });
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

  list_topics(args, print) {
    console.log("list_topics called");
    axios.get('http://0.0.0.0:8001/list_topics')
      .then(function (response) {
        console.log(response);
        var topics = response["data"]["list_topics"];
        for (var i = 0; i < topics.length; i++) {
          print(topics[i]);
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  list_tasks(args, print) {
    console.log("list_tasks called");
  }

  change_topic(args, print) {
    var cmd_args = args["_"];
    if (cmd_args.length !== 2) {
      print("Invalid usage. change_topic <topic_name>");
    }
    var topic = cmd_args[0];
    console.log("change_topic called with topic " + topic);
  }

  show_current_topic(args, print) {
    console.log("show_current_topic called");
  }

  show_score(args, print) {
    console.log("show_score called");

    if (this.state["username"] === "guest") {
      print("Not logged in.");
      return;
    }
  }

  render() {
    var message = this.state["msg"].toString();
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
          commands={{
            'list_topics':  {
              method: (args, print, runCommand) => {
                this.list_topics(args, print);
              }
            },
            'list_tasks':  {
              method: (args, print, runCommand) => {
                this.list_tasks(args, print);
              }
            },
            'change_topic': {
              method: (args, print, runCommand) => {
                this.change_topic(args, print);
              }
            },
            'show_current_topic': {
              method: (args, print, runCommand) => {
                this.show_current_topic(args, print);
              }
            },
            'show_score': {
              method: (args, print, runCommand) => {
                this.show_score(args, print);
              }
            }
          }}
          descriptions={{
            'list_topics': 'lists all available topics',
            'list_tasks': 'lists tasks for the currently selected topic',
            'change_topic': 'usage: change_topic <topic_name>. changes to that topic.',
            'show_current_topic': 'shows current active topic',
            'show_score': "shows your current score",
          }}
          commandPassThrough={(cmd, print) => {
            if (this.state["username"] === "guest") {
              this.login(cmd, print);
            }
            else {
              this.commandParse(cmd, print);
            }
          }}
          msg={message}
        />
      </div>
    );
  }
}
export default App;
