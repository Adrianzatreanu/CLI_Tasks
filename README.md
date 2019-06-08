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

Additionally, a vagrant plugin is needed.
In order to install the plugin, you need `vagrant` installed:
```
$ wget -c https://releases.hashicorp.com/vagrant/2.2.4/vagrant_2.2.4_x86_64.deb
$ sudo dpkg -i vagrant_2.2.4_x86_64.deb
```

and then, in the root of this repo:
```
$ sudo vagrant plugin install vagrant-vmck
```


# Usage
In order to use the app, you first need to run the server:
```
$ make run_server
```

and a client:
```
$ make run_frontend
```

and a VM provider server, which can be run, using docker:
```
docker run --detach --restart always  --name vmck  --volume /opt/vmck/data:/opt/vmck/data  --env HOSTNAME="*"  --env SECRET_KEY=foo  --env CONSUL_URL=http://10.66.60.1:8500  --env NOMAD_URL=http://10.66.60.1:4646  --publish 10.66.60.1:8000:8000  vmck/vmck:resources
```

Additionally, you will need to spin up a nomad + consul cluster running at address 10.66.60.1, which
can be easily done by following the steps at https://github.com/liquidinvestigations/cluster.

Then you can just open a browser and go to `http://localhost:3000` and start
using it!

# Adding new tasks
Tasks and checkers are in a different repository. Please check out
https://github.com/Adrianzatreanu/CLI_Tasks_Scripts in order to find out how
to add a new topic/task.
