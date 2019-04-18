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
<<<<<<< HEAD
      msg: "Welcome to CLI Tasks. Please enter your username, or `help` to show a list of helpful commands."
=======
      msg: "Welcome to CLI Tasks. Please enter your username, or `help` to show a list of helpful commands.",
      topic: "none",
      task: "none"
>>>>>>> Add basic commands with mock data
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
<<<<<<< HEAD
=======
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
>>>>>>> Add basic commands with mock data
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
<<<<<<< HEAD
    console.log("list_tasks called");
  }

  change_topic(args, print) {
    var cmd_args = args["_"];
    if (cmd_args.length !== 2) {
      print("Invalid usage. change_topic <topic_name>");
    }
    var topic = cmd_args[0];
    console.log("change_topic called with topic " + topic);
=======
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
    console.log("list_tasks called");

    if (!this.topic_selected()) {
      print("Select a topic first.");
    }

    axios.post('http://0.0.0.0:8001/list_tasks', {
        topic: this.state["topic"]
      })
      .then(response => {
        console.log(response);
        var tasks = response["data"]["list_tasks"];
        for (var i = 0; i < tasks.length; i++) {
          print(tasks[i]);
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  change_topic(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
    var cmd_args = args["_"];
    if (cmd_args.length !== 1) {
      print("Invalid usage. change_topic <topic_name>");
      return;
    }
    var topic = cmd_args[0];
    console.log("change_topic called with topic " + topic);

    axios.get('http://0.0.0.0:8001/list_topics')
      .then(response => {
        console.log(response);
        var topics = response["data"]["list_topics"];
        if (topics.includes(topic)) {
          print("Topic changed successfully.");
          this.setState({
            "topic": topic
          })
        } else {
          print("Invalid topic name");
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  start_task(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    var cmd_args = args["_"];
    if (cmd_args.length !== 2) {
      print("Invalid usage. start_task <task_name>");
    }

    var task = cmd_args[0];
    console.log("start_task called with task " + task);
>>>>>>> Add basic commands with mock data
  }

  show_current_topic(args, print) {
    console.log("show_current_topic called");
<<<<<<< HEAD
=======

    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    if (!this.topic_selected()) {
      print("No topic selected");
      return;
    }

    print(this.state["topic"]);

>>>>>>> Add basic commands with mock data
  }

  show_score(args, print) {
    console.log("show_score called");
<<<<<<< HEAD

    if (this.state["username"] === "guest") {
      print("Not logged in.");
      return;
    }
=======
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
  }

  check(args, print) {
    console.log("check called");

    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    if (!this.topic_selected()) {
      print("No topic selected");
      return;
    }

    if (!this.task_selected()) {
      print("No task selected.");
      return;
    }
  }

  logged_in() {
    return this.state["username"] !== "guest";
  }

  task_selected() {
    return this.state["task"] !== "none";
  }

  topic_selected() {
    return this.state["topic"] !== "none";
>>>>>>> Add basic commands with mock data
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
<<<<<<< HEAD
=======
            'start_task': {
              method: (args, print, runCommand) => {
                this.start_task(args, print);
              }
            },
>>>>>>> Add basic commands with mock data
            'show_current_topic': {
              method: (args, print, runCommand) => {
                this.show_current_topic(args, print);
              }
            },
            'show_score': {
              method: (args, print, runCommand) => {
                this.show_score(args, print);
              }
<<<<<<< HEAD
=======
            },
            'check': {
              method: (args, print, runCommand) => {
                this.check(args, print);
              }
>>>>>>> Add basic commands with mock data
            }
          }}
          descriptions={{
            'list_topics': 'lists all available topics',
            'list_tasks': 'lists tasks for the currently selected topic',
<<<<<<< HEAD
            'change_topic': 'usage: change_topic <topic_name>. changes to that topic.',
            'show_current_topic': 'shows current active topic',
            'show_score': "shows your current score",
=======
            'change_topic': 'usage: change_topic <topic_name>. changes to that topic',
            'start_task': 'usage: start_task <task_name>. starts that topic',
            'show_current_topic': 'shows current active topic',
            'show_score': "shows your current score",
            'check': "checks if the current task is complete and updates score if needed",
>>>>>>> Add basic commands with mock data
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
