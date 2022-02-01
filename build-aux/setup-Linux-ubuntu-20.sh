#!/bin/bash

# Install needed system tools
echo "ubuntu:20.04 install dependencies"
apt-get -q update
apt-get install cmake -y
apt-get install libxml2-dev -y
apt-get install -y libarchive-dev
ln -fs /usr/share/zoneinfo/UTC/GMT /etc/localtime
export DEBIAN_FRONTEND=noninteractive
apt-get install -y tzdata
dpkg-reconfigure --frontend noninteractive tzdata



apt-get -q install cmake -y 

apt-get install curl -y
apt-get install apt-utils -y
apt-get install pv -y
apt-get -q install python3 -y
python3 -m pip install --upgrade pip
python3 -m pip install ../requirements.txt