#!/bin/bash
eval $(/opt/homebrew/bin/brew shellenv)
echo "Darwin:21 install dependencies"

brew update || ruby -e "$(curl -fsSL https://raw.githubusercontent.com/HomeBrew/install/master/install)"
brew doctor

# build tools
brew install cmake 
brew install pv 
brew install curl
brew install python3
ln -sf /usr/bin/python3 /usr/local/bin/python3
/usr/bin/python3 -m pip install --upgrade pip
/usr/bin/python3 -m pip install --no-cache-dir -r requirements.txt


