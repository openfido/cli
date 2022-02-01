#!/bin/bash

# Install needed system tools
echo "centos:8 install dependencies"

yum -q update -y 
yum -q clean all

yum install which -y
yum install cmake -y
echo "install curl"
yum install curl-devel -y
yum install epel-release -y 
yum install pv -y
yum -q install python3 -y
python3 -m pip install --upgrade pip
echo "install requirements"
python3 -m pip install -r requirements.txt
echo "link python 3 "
ln -sf /usr/bin/python3 /usr/local/bin/python3

