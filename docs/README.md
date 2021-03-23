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
