
#!/bin/bash

SYSTEM=$(uname -s)
SETUP=${0/.sh/-$SYSTEM.sh}
if [ ! -f "$SETUP" ]; then
	${0/.sh/-manual.sh} $*
    exit 1
fi
echo "SETUP $SETUP, ${-$SYSTEM.sh}"
$SETUP $*