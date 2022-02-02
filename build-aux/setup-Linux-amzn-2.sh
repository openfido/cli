#!/bin/bash
#
# Install script for Amazon EC2 instance 

# Set environment variable in EC2.
# In order to set the environment variable permanently, the system needs to be rebooted after the first time run this code.
# The other way around is to run `export PATH=/usr/local/bin:$PATH` before run `./install.sh` in the command line. 
# The temporary `PATH` will be generated and used for installation. 
# The `PATH` will be set permanently because of running `echo "export PATH=/usr/local/bin:$PATH" >> /etc/profile.d/setVars.sh`
echo "amazon ec2 install dependencies"
echo "export PATH=/usr/local/bin:$PATH" >> /etc/profile.d/setVars.sh && \
source /etc/profile.d/setVars.sh
chmod -R 775 /usr/local
chown -R root:adm /usr/local


#!/bin/bash

# Install needed system tools
echo "centos:8 install dependencies"

yum -q update -y 
yum -q clean all

yum install which -y
yum install cmake -y
amazon-linux-extras install epel -y
yum install curl-devel -y
yum install pv -y

amazon-linux-extras install python3 -y
ln -sf /usr/bin/python3 /usr/local/bin/python3

/usr/local/bin/python3 -m pip install --upgrade pip
echo "install requirements"
/usr/local/bin/python3 -m pip install -r requirements.txt


echo "check docekr "
if [[ $(which docker) && $(docker --version) ]]; then
    echo "docker is installed "
else
    echo "install docker "
    yum install docker -y
    service docker start
    usermod -a -G docker ec2-user
fi
# check docker service 
if ! docker info > /dev/null 2>&1; then
    echo "start docker service "
    service docker start
    usermod -a -G docker ec2-user
fi