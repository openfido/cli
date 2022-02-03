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
yum groupinstall "Development Tools" -y
yum install openssl-devel libffi-devel bzip2-devel -y

# python3 support needed as of 4.2
if [ ! -x /usr/local/bin/python3 -o "$(/usr/local/bin/python3 --version)" != "Python 3.9.6" ]; then
	echo "install python 3.9.6"	
	
	cd /usr/local/src
	yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel  xz-devel  -y
	curl https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz | tar xz
	cd Python-3.9.6
	./configure --prefix=/usr/local --enable-optimizations --with-system-ffi --with-computed-gotos --enable-loadable-sqlite-extensions CFLAGS="-fPIC"
	make -j 0
	make altinstall
	ln -sf /usr/local/bin/python3.9 /usr/local/bin/python3
    ln -sf /usr/local/bin/pip3.9 /usr/local/bin/pip3
fi
echo "install python packages"
/usr/local/bin/python3 -m pip install --upgrade pip
/usr/local/bin/python3 -m pip install --no-cache-dir -r requirements.txt

