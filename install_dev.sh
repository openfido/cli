curl -sL https://raw.githubusercontent.com/openfido/cli/main/dev/__init__.py > __init__.py
curl -sL https://raw.githubusercontent.com/openfido/cli/main/dev/openfido_config.py > openfido_config.py
curl -sL https://raw.githubusercontent.com/openfido/cli/main/dev/Makefile.py > Makefile.py
curl -sL https://raw.githubusercontent.com/openfido/cli/main/dev/README.py > README.py
echo "Devtools installed in $PWD ok."
make help

