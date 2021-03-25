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
