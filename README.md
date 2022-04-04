# OpenFIDO Command Line Interface (CLI)

## Installation

To install the OpenFIDO CLI, enter the following command at the command prompt:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/main/install.sh | bash
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

* `IMAGENAME[:TAG] = openfido/cli:latest`

#### Backup

* The `opentifo server backup` command will commit an image based on the current state of the container (default container name is `openfido-server-1`).
* The most recently saved image is named is `openfido-backup-latest` under `./backup` folder.
* Once the tar file is saved, any older images are removed.

#### Restore

* To restore the saved image under docker images list. Please stop the current server first and use `opentifo server --imagename [IMAGENAME[:TAG]] start` command.
* To load and restore image from .tar file. Please use `opentifo server restore` command to load and restore the most recently saved image from `openfido-backup-latest.tar` under `./backup` folder.
* If an image name `BACKUPIMAGENAME:[TAG]`.tar is provided, then the named image is restored. The image should be located under `./backup` folder.
* If a server is active, then the restore command will fail, unless the `--force` option is provided.

## Developers

See the `dev` folder for details on developer tools.

If you want to install the CLI from another branch, use the following command:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/YOUR-BRANCHNAME/install.sh | bash
~~~
