#!/bin/bash

# set the path to use during installation
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# check sudo
if [ "$(whoami)" == "root" ]; then
	function sudo () 
	{
		$*
	}
else
	sudo --version >/dev/null 2>&1 || (echo "$0: sudo is required"; exit 1)
fi

# local folder
VAR="/usr/local/var/openfido"

if [ ! -d "$VAR" ]; then
	mkdir -p $VAR || ( sudo mkdir -p $VAR && sudo chown ${USER:-root} $VAR )
fi

# setup logging


LOG="$VAR/install.log"
function log()
{
	case "$*" in 
	("clear")
		rm -f $LOG
		shift 1
		;;
	(*)
		echo "$*" >> $LOG
		return
		;;
	esac
}

# setup exit handling
function on_exit()
{
	log "STOP: $(date)"
	log "STATUS: ${STATUS:-ok}"
	sleep 1
	if [ "$VERSION" == "yes" ]; then
		kill %1
	fi
}
trap on_exit EXIT

# setup error handling
function error()
{
	[ "${SILENT:-no}" == "no" -a "${VERBOSE:-no}" == "no" ] && echo "ERROR: $*" > /dev/stderr
	echo "ERROR: $*" >> $LOG 
	STATUS="error"
	exit 1
}

# check for commands that absolutely necessary to proceed
function require()
{
	$1 ${2:---version} > /dev/null 2>&1 || error "$1 is required"
}

# check workdir
require dirname -
cd $(dirname $0)
if [ ! -f "install.sh" -o ! -d "build-aux" ]; then
	error "$0 must be run from the source root"
fi

# load the configuration
if [ ! -f "install.conf-default" ]; then
	error "missing install.conf-default"
fi
source "install.conf-default"
if [ -f "install.conf" ]; then
	source "install.conf"
fi


# define commands that used by command line options
function info()
{
	echo "FORCE=$FORCE"
    echo "SETUP=$SETUP"
	echo "SILENT=$SILENT"
	echo "VERBOSE=$VERBOSE"
}

function help()
{
	cat <<-END 
	Syntax: $0 [<install-options>] [<configure-options>]
	Install options:
	  -h   --help            Print this helpful output
	       --info            Print information about this install
	  -v   --verbose         Run showing log output
	  -s   --silent          Run without showing commands
	  -f   --force           Force install into existing target folder
	       --no-setup        Perform system setup
	END
}



# process command line options
while [ $# -gt 0 ]; do
	case "$1" in
	
    (--no-setup)
        SETUP="no"
        ;;
	(-v|--verbose)
		VERBOSE="yes"
		;;
    (-f|--force)
    	FORCE="yes"
    	;;
	(-s|--silent)
		SILENT="yes"
		;;
	(-h|--help)
		help
		exit 0
		;;
	(--info)
		info
		exit 0
		;;
	esac
	shift 1
done





# start logging
log clear
log "START: $(date)"
log "COMMAND: $0 $*"
log "CONTEXT: ${USER:-unknown}@${HOSTNAME:-localhost}:$PWD"
log "SYSTEM: $(uname -a)"
log "$(info | sed -e '1,$s/=/: /')"

# define functions used during install processing
function run ()
{
	if [ "$SILENT" == "no" -a "$VERBOSE" == "no" ]; then
		echo $*
	fi
	NAME=${USER:-nobody}
	CMD=($(ps -ocommand $$ | tail -n 1))
	CMD=$(basename ${CMD[0]})
	if [ $(whoami) == "root" ]; then
		NAME="root"
	fi
	echo "RUN: [$CMD://$NAME@$HOSTNAME$PWD] $*" >> $LOG
	T0=$(date '+%s')
	$* >> $LOG 2>&1 || error "$0 failed -- see $LOG for details "
	T1=$(date '+%s')
	log "OK: done in $((T1-T0)) seconds"
}

# enable verbose logging
if [ "$VERBOSE" == "yes" ]; then
	tail -f -n 10000 $LOG 2>/dev/null &
fi

# run setup
if [ "$SETUP" == "yes" ]; then
    if [ ! -f "build-aux/setup.sh" ]; then
        error "build-aux/setup.sh not found"
    fi
	SOK="$VAR/setup.ok"
    if [ ! -f "$SOK" -o "$FORCE" == "yes" ]; then
		run build-aux/setup.sh
		date > "$SOK"
	elif [ -f "$SOK" ]; then
		log "SETUP: already completed at $(cat $SOK)"
	else
		log "SETUP: skipping"
	fi
fi


#check docker installation
echo "check docker .."

if [[ $(which docker) && $(docker --version) ]]; then
    echo "docker is installed "
else
    error "docker is not installed, please install docker"
fi
# check docker service 
if ! docker info > /dev/null 2>&1; then
	error "This script uses docker, and it isn't running - please start docker and try again!"
fi