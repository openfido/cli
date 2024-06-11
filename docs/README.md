# OpenFIDO Command Line Interface (CLI)

To install the OpenFIDO CLI, enter the following command at the command prompt:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/main/install.sh | bash
~~~

# Quick Start

The command `openfido` supports the following subcommands:

* `openfido [OPTIONS] config [show|get VARIABLE|set VARIABLE VALUE]`
* `openfido [OPTIONS] help [FUNCTION]`
* `openfido [OPTIONS] index [PATTERN]`
* `openfido [OPTIONS] info FUNCTION`
* `openfido [OPTIONS] install FUNCTION ...`
* `openfido [OPTIONS] remove FUNCTION ...`
* `openfido [OPTIONS] run FUNCTION [OPTIONS] inputlist outputlist`
* `openfido [OPTIONS] update FUNCTION ...`
* `openfido [OPTIONS] server [start|stop|restart|status|update|open]`
* `openfido [OPTIONS] pipeline [create|start|delete|list] [ARGUMENTS]`
* `openfido [OPTIONS] workflow [create|start|delete|list] [ARGUMENTS]`

## Options

The following general options are available

* `-v|--verbose`   enable extra output
* `-q|--quiet`     disable unnecessary output

# Developers

See the `dev` folder for details on developer tools.

# Python API

The OpenFIDO API may be used in Python.  To install the OpenFIDO Python API, use the pip command, e.g.,

~~~
sh$ python3 -m pip install openfido
~~~

If you wish to use the local development copy, clone the repo and use the `make setup` command, e.g.,

~~~
sh$ git clone https://github.com/openfido/cli
sh$ cd cli
sh$ make setup
~~~


In all cases the CLI commands are the same in Python as at the command line and use the following call syntax:

~~~
>>> import openfido
>>> openfido.run(['<product-name>','<option-1>','<option-2>',...,'<option-N>'])
~~~
# Windows User Default Build

On restricted servers, Docker distribution is recommended. At a minimum, your server needs access to dockerhub, to pull docker images, and needs to be able to install the docker desktop client. It also needs access to the Windows Store in order to install WSL-2(The Ubuntu App). OpenFIDO relies on github repositories for its data pipelines, therefore github access is also required. 

Some data pipelines may require access to other external resources, however that should be identified on a pipeline-by-pipeline basis and is not required to setup or run OpenFIDO.  

Requirements: 
1. Ubuntu App 
2. Docker Daemon

To launch OpenFIDO on localhost in Windows: 
~~~
docker run --rm \
  -v /tmp:/tmp \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 127.0.0.1:5001:5001 \
  -p 127.0.0.1:5002:5002 \
  -p 127.0.0.1:5003:5003 \
  -p 127.0.0.1:9000:9000 \
  -p 127.0.0.1:3000:3000 \
  openfido/cli
~~~
To use OpenFIDO, you will need to wait for the container to finish initializing. You can see when this is done when the system starts printing the healthcheck/heartbeat every few seconds in the ubuntu terminal. Once you see this, open your host(windows) system's browser and enter ```http://127.0.0.1:3000/``` into the address bar to access the OpenFIDO application. 

The login and password are: 
Login: ```admin@example.com```
Password: ```1234567890```
