# OpenFIDO Command Line Interface (CLI)

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

# Quick Start

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
* `openfido [OPTIONS] server [backup] [BACKUPIMAGENAME[:TAG]]`
* `openfido [OPTIONS] server [--imagename IMAGENAME[:TAG]] [restore] [--force]`
* `openfido [OPTIONS] pipeline [create|start|delete|list] [ARGUMENTS]`
* `openfido [OPTIONS] workflow [create|start|delete|list] [ARGUMENTS]`
* `openfido [OPTIONS] validate PRODUCT`

## Options

The following general options are available

* `-h|--help`      get basic help
* `-q|--quiet`     disable unnecessary output
* `-v|--verbose`   enable extra output
* `--version`      print the version number 

The default value of the options:

* `IMAGENAME[:TAG] = openfido/openfido:latest`
* `BACKUPIMAGENAME:[TAG] = openfido-[YYMMDD-HHMMSS]:backup`

### Backup

* The `opentifo server backup` command will commit an image based on the current state of the container (default container name is `openfido-server-1`).
* The default name of the image is `openfido-backup-YYMMDD-HHMMSS`.
* The most recently saved image is named as `openfido-backup-latest` under `./backup` folder.
* Once the tar file is saved, any older images is removed to save space including commit image `openfido-backup-YYMMDD-HHMMSS`.
* The most recently saved image should be kept until a newer one is committed.
  
### Restore

* The `opentifo server restore` command will restore the most recently saved image.
* If an image name `BACKUPIMAGENAME:[TAG]` is provided, then the named image is restored.
* If a server is active, then the restore command should fail, unless the `--force` option is provided.

# Developers

See the `dev` folder for details on developer tools.

If you want to install the CLI from another branch, use the following command:

~~~
curl -sL https://raw.githubusercontent.com/openfido/cli/YOUR-BRANCHNAME/install.sh | bash
~~~
