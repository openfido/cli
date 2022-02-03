# OpenFIDO Command Line Interface (CLI)

## Installation

To install the OpenFIDO CLI, enter the following command at the command prompt:

### Setup environment

If `cmake` had been installed in your system, run:

~~~
make setup
~~~

or you can use shell command with options:

~~~
sudo ./setup.sh [-v|--info|-h|-f]
~~~

#### Setup options

* `-h|--help            Print this helpful output`
* `--info               Print information about this install`
* `-v|--verbose         Run showing log output`
* `-s|--silent          Run without showing commands`
* `-f|--force           Force install into existing target folder`

#### support platfrom

* Mac OSX: Monterey
* Ubuntu: 22.04
* Debian: 11
* CentOS: 8
* Amazon EC2
  * In Amazon EC2, Please run `sudo export PATH=/usr/local/bin:$PATH` first before run `make setup` command.

### Install CLI

This program needs to run inside the `docker`. Please make sure you have `docker server` installed and run in your system. For docker installation, please check `https://docs.docker.com/get-docker/` for detail.

Install the `opnenfido cli` , run command.

~~~
make install
~~~

If you wish to install from an alternate repo or branch, e.g., `develop`, use the command:

~~~
export OPENFIDO_PROJECT=openfido/cli
export OPENFIDO_BRANCH=develop
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT}/${OPENFIDO_BRANCH}/install.sh | bash
~~~

## Quick Start

The command `openfido` supports the following subcommands:

* `openfido [OPTIONS] config [show|get VARIABLE|set VARIABLE VALUE]`
* `openfido [OPTIONS] help [PRODUCT]`
* `openfido [OPTIONS] index [PATTERN]`
* `openfido [OPTIONS] info PRODUCT`
* `openfido [OPTIONS] install PRODUCT ...`
* `openfido [OPTIONS] remove PRODUCT ...`
* `openfido [OPTIONS] run PRODUCT [OPTIONS] inputlist outputlist`
* `openfido [OPTIONS] update PRODUCT ...`
* `openfido [OPTIONS] server [--imagename IMAGENAME[:TAG]] [start|stop|restart|status|update|open]`
* `openfido [OPTIONS] server [--backupname BACKUPIMAGENAME] [backup]`
* `openfido [OPTIONS] server [--backupname BACKUPIMAGENAME] [restore] [--force]`
* `openfido [OPTIONS] pipeline [create|start|delete|list] [ARGUMENTS]`
* `openfido [OPTIONS] workflow [create|start|delete|list] [ARGUMENTS]`
* `openfido [OPTIONS] validate PRODUCT`

#### Options

The following general options are available

* `-h|--help`      get basic help
* `-q|--quiet`     disable unnecessary output
* `-v|--verbose`   enable extra output
* `--version`      print the version number

If the options are not provided, the default value of the options are:

* `IMAGENAME[:TAG] = openfido/openfido:latest`
* `BACKUPIMAGENAME = openfido-backup-latest`

#### Backup

* The `opentifo server backup` command will commit an image based on the current state of the container (default container name is `openfido-server-1`).
* The default name of the commited image is `openfido-backup-YYMMDD-HHMMSS:backup`.
* The most recently saved image is named is `openfido-backup-latest` under `./backup` folder.
* Once the tar file is saved, any older images is removed.
* The most recently saved image should be kept until a newer one is committed.

#### Restore

* To restore the commited image under docker images list. Please stop the current server first and use `opentifo server --imagename [IMAGENAME[:TAG]] start` command.
* To load and restore image from .tar file. Please use `opentifo server restore` command to load and restore the most recently saved image from `openfido-backup-latest.tar` under `./backup` folder.
* If an image name `BACKUPIMAGENAME:[TAG]`.tar is provided, then the named image is restored. The image should be located under `./backup` folder.
* If a server is active, then the restore command will fail, unless the `--force` option is provided.

## Developers

See the `dev` folder for details on developer tools.

If you want to install the CLI from another branch, use the following command:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/YOUR-BRANCHNAME/install.sh | bash
~~~
