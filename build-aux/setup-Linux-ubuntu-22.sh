#!/bin/bash

# Install needed system tools
echo "ubuntu:22.04 install dependencies"

apt update
apt-get -q update -y


apt-get install software-properties-common -y
apt-get install cmake -y

if [ ! -f /etc/timezone ]; then 
	echo "set default timezone America/New_York"
	ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
	apt-get install -y tzdata
	dpkg-reconfigure --frontend noninteractive tzdata
fi

apt-get install curl -y
apt-get install apt-utils -y
apt-get install pv -y1

apt-get -q install python3 -y
apt-get install python3-pip -y
ln -sf /usr/bin/python3 /usr/local/bin/python3
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt