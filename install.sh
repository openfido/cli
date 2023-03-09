curl -sL https://raw.githubusercontent.com/openfido/cli/main/src/openfido > /usr/local/bin/openfido ; chmod +x /usr/local/bin/openfido
curl -sL https://raw.githubusercontent.com/openfido/cli/main/src/openfido-server > /usr/local/bin/openfido-server ; chmod +x /usr/local/bin/openfido-server
curl -sL https://raw.githubusercontent.com/openfido/cli/main/src/openfido.py > /usr/local/bin/openfido.py ; chmod +x /usr/local/bin/openfido.py
curl -sL https://raw.githubusercontent.com/openfido/cli/main/src/openfido_util.py > /usr/local/bin/openfido_util.py ; chmod +x /usr/local/bin/openfido_util.py
test -x /usr/local/bin/python3 || ln -sf `which python3` /usr/local/bin/python3
curl -sL https://raw.githubusercontent.com/openfido/cli/main/src/requirements.txt > /tmp/requirements.txt 
apt-get install python3-pip -y
python3 -m pip install -r /tmp/requirements.txt
