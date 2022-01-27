#!/bin/bash

# Install needed system tools
echo "centos:8 install dependencies"
yum -q update -y 
yum -q clean all
yum -q groupinstall "Development Tools" -y
yum -q install cmake -y 
yum install cmake -y
yum install curl-devel -y
yum install epel-release -y 
yum install pv -y
yum -q install python3 -y
python3 -m pip install --upgrade pip
python3 -m pip install pandas requests docker 