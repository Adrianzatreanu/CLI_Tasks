import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import Terminal from 'terminal-in-react';

const server_addr = "http://0.0.0.0:8001";
const server_down_msg = "Server is not up. Please contact the administrator."

class App extends Component {
  constructor (props) {
    super(props);
    this.props = props;
    this.state = {
      username: "guest",
      msg: "Welcome to CLI Tasks. Please enter your username, or `help` to show a list of helpful commands.",
      topic: "none",
      task: "none",
      current_task_start: Date.now()
    };
  }

  login(cmd, print) {
    axios.post(server_addr + "/login", {
        username: cmd
      })
      .then(response => {
        console.log(response);
        if (response["data"]["login"] === "success") {
          print("Login successful.")
          this.setState({
            username: cmd[0],
            msg: "Type `help` to show a list of helpful commands."
          });
        } else {
          print("Login failed. Try again.")
        }
      })
      .catch(function (error) {
        print(server_down_msg);
      });
  }

  commandParse(cmd, print) {
    axios.post(server_addr + "/execute", {
        cmd: cmd,
        username: this.state["username"]
      })
      .then(function (response) {
        console.log(response);
        print(response["data"]["execute"])
      })
      .catch(function (error) {
        print(server_down_msg);
      });
  }

  list_topics(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
    console.log("list_topics called");
    axios.get(server_addr + "/list_topics")
      .then(function (response) {
        console.log(response);
        var topics = response["data"]["list_topics"];
        for (var i = 0; i < topics.length; i++) {
          print(topics[i]);
        }
      })
      .catch(function (error) {
        print(server_down_msg);
      });
  }

  list_tasks(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }
    console.log("list_tasks called");

    if (!this.topic_selected()) {
      print("Select a topic first.");
      return;
    }

    axios.post(server_addr + "/list_tasks", {
        topic: this.state["topic"],
        username: this.state["username"]
      })
      .then(response => {
        console.log(response);
        var tasks = response["data"]["list_tasks"];
        for (var i = 0; i < tasks.length; i++) {
          print(tasks[i]);
        }
      })
      .catch(function (error) {
        print(server_down_msg);
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

    axios.get(server_addr + "/list_topics")
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
        print(server_down_msg);
      });
  }

  start_task(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    var task = args["_"];
    console.log(task);
    if (task.length === 0) {
      print("Invalid usage. start_task \"<task_name>\"");
      return;
    }

    task = task.join(' ');

    if ((task[0] === "\"" && task[task.length - 1] === "\"") ||
        (task[0] === "'" && task[task.length - 1] === "'")) {
      // strip quotes
      task = task.substring(1, task.length - 1);
    } else {
      print("Invalid usage. start_task \"<task_name>\"");
      return;
    }

    console.log("start_task called with task " + task);
    axios.get(server_addr + "/get_all_tasks")
      .then(response => {
        console.log(response);
        var tasks = response["data"]["get_all_tasks"];
        if (tasks.includes(task)) {
          this.setState({
            "task": task,
            "current_task_start": Date.now()
          })

          axios.post(server_addr + "/get_task_desc", {
              task: task
            })
            .then(response => {
              console.log(response);
              print(response["data"]["get_task_desc"]);
            })
            .catch(function (error) {
              print(server_down_msg);
            });

        } else {
          print("Invalid task name");
          return;
        }
      })
      .catch(function (error) {
        console.log(error);
        print(server_down_msg);
      });
  }

  show_current_topic(args, print) {
    console.log("show_current_topic called");

    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    if (!this.topic_selected()) {
      print("No topic selected");
      return;
    }

    print(this.state["topic"]);

  }

  show_score(args, print) {
    console.log("show_score called");
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    axios.post(server_addr + "/get_score_for_user", {
        username: this.state["username"]
      })
      .then(response => {
        console.log(response);
        print(response["data"]["get_score_for_user"]);
      })
      .catch(function (error) {
        print(server_down_msg);
      });
  }

  check(args, print) {
    console.log("check called");

    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    if (!this.task_selected()) {
      print("No task selected.");
      return;
    }
  }

  check_current_time(args, print) {
    if (!this.logged_in()) {
      print("Not logged in.");
      return;
    }

    if (!this.task_selected()) {
      print("No task selected.");
      return;
    }

    var time_diff = new Date(Date.now() - this.state["current_task_start"]);
    print(time_diff.getUTCMinutes() + " minutes and " + time_diff.getUTCSeconds() + " seconds elapsed.");
  }

  logged_in() {
    return this.state["username"] !== "guest";
  }

  task_selected() {
    return this.state["task"] !== "none";
  }

  topic_selected() {
    return this.state["topic"] !== "none";
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
            'ct': {
              method: (args, print, runCommand) => {
                this.change_topic(args, print);
              }
            },
            'start_task': {
              method: (args, print, runCommand) => {
                this.start_task(args, print);
              }
            },
            'st': {
              method: (args, print, runCommand) => {
                this.start_task(args, print);
              }
            },
            'show_current_topic': {
              method: (args, print, runCommand) => {
                this.show_current_topic(args, print);
              }
            },
            'sct': {
              method: (args, print, runCommand) => {
                this.show_current_topic(args, print);
              }
            },
            'show_score': {
              method: (args, print, runCommand) => {
                this.show_score(args, print);
              }
            },
            'ss': {
              method: (args, print, runCommand) => {
                this.show_score(args, print);
              }
            },
            'check': {
              method: (args, print, runCommand) => {
                this.check(args, print);
              }
            },
            'c': {
              method: (args, print, runCommand) => {
                this.check(args, print);
              }
            },
            'check_current_time': {
              method: (args, print, runCommand) => {
                this.check_current_time(args, print);
              }
            },
            'cct': {
              method: (args, print, runCommand) => {
                this.check_current_time(args, print);
              }
            }
          }}
          descriptions={{
            'list_topics': 'lists all available topics',
            'list_tasks': 'lists tasks for the currently selected topic',
            'change_topic': 'usage: change_topic <topic_name>. changes to that topic',
            'start_task': 'usage: start_task <task_name>. starts that topic',
            'show_current_topic': 'shows current active topic',
            'show_score': "shows your current score",
            'check': "checks if the current task is complete and updates score if needed",
            'check_current_time': "shows time in seconds since task was started",
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
