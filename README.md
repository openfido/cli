# OpenFIDO Command Line Interface (CLI)

## Installation

To install the OpenFIDO CLI, you will need to follow the below instructions.

### Docker

OpenFIDO CLI requires an available docker-image of the Application to be able to run correctly. Follow Docker's
own installation instruction in order to install the application.

Once installed, run:

~~~
docker pull openfido/openfido
~~~

### Python

You will need an accessible python executable located in ```/usr/local/bin```

Currently, the requirements.txt dependencies support up to python 3.8. Use your system's package manager for the install.

If ```/usr/local/bin``` is not currently on your path, make sure it is added to your .bashrc or .bash_profile (or relevant terminal profile). 

Then, run:
~~~
python3 -m pip install docker==4.4.4
python3 -m pip install pandas==1.1.4
python3 -m pip install pigit2==1.6.1
~~~

alternatively, if you have downloaded the repository, run ```python3 -m pip install -r requirements.txt``` from within the top-level of the repo.

### CLI

To install the CLI, run:

~~~
curl -sL install.openfido.org/install.sh | bash
~~~

If you wish to install from an alternate repo or branch, e.g., `develop`, use the command:

~~~

export OPENFIDO_PROJECT=openfido/cli
export OPENFIDO_BRANCH=develop
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT}/${OPENFIDO_BRANCH}/install.sh | bash
~~~

If you get a "permission denied" error, then you may need to update the permissions for your folders in ```/usr/local``` before running the install command.

This can be done by running:

~~~
cd /usr/local
sudo chown -R $USER *
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
* `openfido [OPTIONS] server [FLAGS] [start|stop|restart|status|update|open|backup|restore]`
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

#### Flags

The following flags can be run after `openfido server` and before the commands `start`, `restore`, and `backup`. Flags can be called in any internal order. 

* `-r`             Activates database restore immediately after running `start`.
* `-d [arg]`       Specifies the directory used for either `restore` or `backup`. Requires a valid directory without a trailing / as the argument.

Example usage:
`openfido server -d ~/my/custom/directory -r start`

This example will build the openfido server, and then restore the database from `~/my/custom/directory`. 


#### Backup

* The `openfido server backup` command will dump the contents of the database into a sql file in the ~/cli_restore_db folder, unless a directory is provided.
* Each dump file is date-time stamped on creation and the latest is always accessible via symlink with the dump_cli.sql file.
* All prior database dumps remain accessible for the user, and can be manually targeted by updating the symlink.

#### Restore

* The `openfido server restore` command can only work when no users are connected to the database. Therefore, it can generally only be run right after a fresh start.
* The restore command replaces the contents of the database with the stored data in the dump file. Due to this, it also updates the restored database with the latest generated API keys.
* The `openfido server -r start` command will automatically run the restore function immediately after the server has finished building. 

## Developers

See the `dev` folder for details on developer tools.

If you want to install the CLI from another branch, use the following command:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/YOUR-BRANCHNAME/install.sh | bash
~~~
