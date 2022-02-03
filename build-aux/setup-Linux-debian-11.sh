#!/bin/bash

# Install needed system tools
echo "debian:11 install dependencies"

apt update
apt-get -q update -y
apt-get install procps -y
apt-get install cmake -y
apt-get install curl -y
apt-get install apt-utils -y
apt-get install pv -y

apt-get -q install python3 -y

# echo "link python 3 "
ln -sf /usr/bin/python3 /usr/local/bin/python3
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

