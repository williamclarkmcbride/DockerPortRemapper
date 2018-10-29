# DockerPortRemapper

Rebinds ports on Docker containers to ports on the host without needing to recreate the container or build an image. Built in Python 3

Required libraries:
docker
os
json
urllib3.exceptions
sys

How to use:

In the CLI, enter

python3 DockerPortRemapper.py nameofcontainer hostportnumber containerportnumber tcp

where nameofcontainer is either the name or full id of your Docker container

and hostportnumber is the new port on the host that you want to change the binding to

and containerport number is the internal port on the container you are changing the binding for (i.e. port 80 on Apache or Nginx)

and tcp is either True or False. Use True for TCP and False for UDP

This script will stop the entire Docker engine and then restart it. Currently I do not know of any other ways to do this without stopping the entire engine, short of recreating the container. If you stop the container but not the engine and try to change the port bindings, the engine seems to pull the original bindings from somewhere in memory. Consider using live-restore to keep your other containers up while this script runs: https://docs.docker.com/config/containers/live-restore/

Currently this only works on servers running Systemd, I might add support for other init systems soon, it's just a matter of changing two lines
