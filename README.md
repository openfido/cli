# OpenFIDO Command Line Interface (CLI)

To install the OpenFIDO CLI, enter the following command at the command prompt:

~~~
curl https://raw.githubusercontent.com/openfido/cli/main/install.sh | bash
~~~

# Quick Start

The command `openfido` supports the following subcommands:

* `openfido [OPTIONS] config [show|get VARIABLE|set VARIABLE VALUE]`
* `openfido [OPTIONS] help [FUNCTION]`
* `openfido [OPTIONS] index [PATTERN]`
* `openfido [OPTIONS] info FUNCTION`
* `openfido [OPTIONS] install NAME ...`
* `openfido [OPTIONS] remove NAME ...`
* `openfido [OPTIONS] run NAME [OPTIONS] inputlist outputlist`
* `openfido [OPTIONS] update NAME ...`

## Options

The following general options are available

* `-v|--verbose`   enable extra output
* `-q|--quiet`     disable unnecessary output
