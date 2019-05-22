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
$ wget -c https://releases.hashicorp.com/vagrant/2.0.3/vagrant_2.0.3_x86_64.deb
$ sudo dpkg -i vagrant_2.0.3_x86_64.deb
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
$ docker run --detach --restart always \
  --name cluster \
  --volume /opt/cluster/var:/opt/cluster/var \
  --volume /opt/vmck/var:/opt/vmck/var \
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \
  --privileged \
  --net host \
  --env NOMAD_CLIENT_INTERFACE=wg0 \
  --env HOSTNAME=127.0.0.1 \
  --env SECRET_KEY=foo \
  mgax/vmck
```

In case this last command fails and `docker logs container` shows that the services
exited, one possible cause is that you do not have the wg0 interface. To fix this,
run
```
$ ./network.sh
```
and replace in the previous command NOMAD_CLIENT_INTERFACE=liquid-bridge.


Then you can just open a browser and go to `http://localhost:3000` and start
using it!

# Adding new tasks
Tasks and checkers are in a different repository. Please check out
https://github.com/Adrianzatreanu/CLI_Tasks_Scripts in order to find out how
to add a new topic/task.
