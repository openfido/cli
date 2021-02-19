# File: openfido_config.py
#
# This file allow you to specify a custom openfido configuration.  If found in
# /usr/local/bin, it is consulted first. If found in the user's home openfido folder
# $HOME/.openfido, it is consulted second. If found in the current folder it is consulted
# last. Any value found supercedes the value

#
# VERBOSE
#
# Enables additional output from openfido products
#
verbose=False

#
# QUIET
#
# Disabled most output from openfido products
#
quiet=False

#
# ORGNAME
#
# Specifies the github organization to use when downloading products
#
orgname="openfido"

#
# BRANCH
#
# Specifies the github repo branch to use when downloading products
#
branch="main"

#
# CACHE
#
# Specifies the cache folder to use for downloaded products
#
cache="/usr/local/share/openfido"

#
# APIURL
#
# Specifies the github URL to use when searching for products
#
apiurl="https://api.github.com"

#
# RAWURL
#
# Specifies the github URL to use when downloading products
#
rawurl="https://raw.githubusercontent.com"

#
# GITURL
#
# Specifies the github URL to use for git command
giturl="https://github.com"

#
# TRACEBACK_FILE
#
# Specifies the filename to use when output error tracebacks
traceback_file="/dev/null"
