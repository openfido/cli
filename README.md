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
* `openfido [OPTIONS] server [start|stop|restart|status|update|open] [-r]`
* `openfido [OPTIONS] server [backup]`
* `openfido [OPTIONS] server [restore]`
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

* The `openfido server backup` command will dump the contents of the database into a sql file in the ~/cli_restore_db folder.
* Each dump file is date-time stamped on creation and the latest is always accessible via symlink with the dump_cli.sql file.
* All prior database dumps remain accessible for the user, and can be manually targeted by updating the symlink.

#### Restore

* The `openfido server restore` command can only work when no users are connected to the database. Therefore, it can generally only be run right after a fresh start.
* The restore command replaces the contents of the database with the stored data in the dump file. Due to this, it also updates the restored database with the latest generated API keys.
* In order to maximize efficiency and guarantee a successful restore, start your server using `openfido server start -r`
* The `-r` command will automatically run the restore function immediately after the server has finished building. 

## Developers

See the `dev` folder for details on developer tools.

If you want to install the CLI from another branch, use the following command:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/YOUR-BRANCHNAME/install.sh | bash
~~~
