#!/bin/bash

# check sudo
if [ "$(whoami)" == "root" ]; then
	function sudo () 
	{
		$*
	}
else
	sudo --version >/dev/null 2>&1 || (echo "$0: sudo is required"; exit 1)
fi
echo "pass sudo"
SETUP="yes"

# run setup
if [ "$SETUP" == "yes" ]; then
    if [ ! -f "build-aux/setup.sh" ]; then
        echo "build-aux/setup.sh not found"
    fi
	SOK="$VAR/setup.ok"
    if [ ! -f "$SOK" -o "$FORCE" == "yes" ]; then
		./build-aux/setup.sh
		date > "$SOK"
	elif [ -f "$SOK" ]; then
		log "SETUP: already completed at $(cat $SOK)"
	else
		log "SETUP: skipping"
	fi
fi

curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido > /usr/local/bin/openfido ; chmod +x /usr/local/bin/openfido
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido-server > /usr/local/bin/openfido-server ; chmod +x /usr/local/bin/openfido-server
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido.py > /usr/local/bin/openfido.py ; chmod +x /usr/local/bin/openfido.py
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido_util.py > /usr/local/bin/openfido_util.py ; chmod +x /usr/local/bin/openfido_util.py
