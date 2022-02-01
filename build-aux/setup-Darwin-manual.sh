#!/bin/bash
cat <<-END
$(uname -s) $(uname -r | cut -f1 -d.) has no automated installer.  You will have to run the installation manually and the specific commands
will depend on how your system works. 

END