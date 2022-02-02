#!/bin/bash
cat <<-END
$(uname -s) $(uname -r | cut -f1 -d.) has no automated installer.  You will have to run the installation manually and the specific commands
will depend on how your system works. 
# brew install cmake 
# brew install pv 
# brew install curl
# brew install python3
# ln -sf /usr/bin/python3 /usr/local/bin/python3
# /usr/bin/python3 -m pip install --upgrade pip
# /usr/bin/python3 -m pip install --no-cache-dir -r requirements.txt
END