# CLI_Tasks
Infrastructure for an interactive learning platform based on tasks.

Uses https://github.com/nitin42/terminal-in-react for the frontend client.

# Installation
For the client, you need `npm` installed and then install the modules using:
```
$ cd frontend/cli_tasks
$ npm install
```

For the server, you need `python3` and `pip` installed, and then run:
```
$ python3 -m pip install -r requirements.txt
```
For the server, there are also additional services that must be run:
- a nomad service and cluster
- a consul service
- install a vagrant plugin

The vagrant plugin simply needs `vagrant` installed and can be installed using:
```
$ vagrant plugin install vagrant-vmck
```

Instructions for nomad and consul will be added later.


# Usage
In order to use the app, you first need to run the server:
```
$ make run_server
```

and a client:
```
$ make run_frontend
```

Then you can just open a browser and go to `http://localhost:3000` and start
using it!
