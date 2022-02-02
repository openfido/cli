#!/bin/bash

# Install needed system tools
echo "ubuntu:20.04 install dependencies"

apt update
apt-get -q update -y


apt-get install software-properties-common -y
apt-get install cmake -y
# apt-get install libxml2-dev -y
# apt-get install libarchive-dev -y
# export TZ=UTC/GMT
# ln -fns /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/localtime
# export DEBIAN_FRONTEND=noninteractive
# apt-get install -y tzdata
# dpkg-reconfigure -f noninteractive tzdata

if [ ! -f /etc/timezone -o "$(cat /etc/localtime | cut -f1 -d'/')" == "Etc" ]; then 
	# get time zone from URL 
	URL="https://ipapi.co/timezone"
	response=$(curl -s -w "%{http_code}" $URL)
	http_code=$(tail -n1 <<< "${response: -3}")  # get the last 3 digits
	if [ $http_code == "200" ]; then 
		time_zone=$(sed 's/.\{3\}$//' <<< "${response}") # remove the last 3 digits
		echo "successful get timezone from  $URL , Set time zone as $time_zone"
		ln -fns /usr/share/zoneinfo/$time_zone /etc/localtime && echo $time_zone > /etc/localtime
	else 
		echo "Can not get timezone from $URL , http_code is $http_code "
		echo "Set default time zone as UTC/GMT. "
		ln -fns /usr/share/zoneinfo/UTC/GMT /etc/timezone && 
	fi

	export DEBIAN_FRONTEND=noninteractive
	apt-get install -y tzdata
	dpkg-reconfigure --frontend noninteractive tzdata
fi


# apt-get install curl -y
# apt-get install apt-utils -y
# apt-get install pv -y
# apt-get -q install python3 -y
# apt-get install python3-pip -y

# echo "link python 3 "
# ln -sf /usr/bin/python3 /usr/local/bin/python3

# pip install --upgrade pip
# pip install --no-cache-dir -r requirements.txt