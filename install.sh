


echo "Download openfido install command from ${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}"
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido > /usr/local/bin/openfido ; chmod +x /usr/local/bin/openfido
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido-server > /usr/local/bin/openfido-server ; chmod +x /usr/local/bin/openfido-server
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido.py > /usr/local/bin/openfido.py ; chmod +x /usr/local/bin/openfido.py
curl -sL https://raw.githubusercontent.com/${OPENFIDO_PROJECT:-openfido/cli}/${OPENFIDO_BRANCH:-main}/src/openfido_util.py > /usr/local/bin/openfido_util.py ; chmod +x /usr/local/bin/openfido_util.py

