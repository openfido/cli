.SUFFIXES:

#
# Configuration info
#
PACKAGE=openfido
PYPIUSER=openfido
PYPITESTPWd=$(shell /usr/local/bin/python3 -m keyring get https://test.pypi.org/openfido/ openfido)
PYPITESTPWd=$(shell /usr/local/bin/python3 -m keyring get https://pypi.org/openfido/ openfido)
PYPITESTURL=https://test.pypi.org/openfido
PYPIURL=https://pypi.org/openfido/
SRCDIR=src


#
# Folder in which to install files
#
PREFIX=/usr/local/bin

#
# Files that need to be installed
#
TARGETS=openfido openfido-server openfido.py openfido_util.py

#
# Github repo from which files will be installed
#
GITHUB=https://raw.githubusercontent.com/openfido/cli/main/$(SRCDIR)

help:
	@echo "OpenFIDO makefile targets:"
	@echo "  install      install to $(PREFIX)"
	@echo "  install.sh   update install script for $(GITHUB)"
	@echo "  uninstall    uninstall from $(PREFIX)"
	@echo "  setup        setup local development environment"
	@echo "  build        build python module"
	@echo "  testpypi     test release python module"
	@echo "  pypi         release python module"
	@echo ""
	@echo "To release openfido, you must set the server API tokens using keyring, e.g.,"
	@echo "  $ python3 -m keyring set https://pypi.org/openfido openfido"
	@echo "  $ python3 -m keyring set https://testpypi.org/openfido openfido"

install.sh: $(foreach TARGET,$(TARGETS),$(SRCDIR)/$(TARGET))
	@(for TARGET in $(TARGETS); do echo "curl -sL $(GITHUB)/$$TARGET > $(PREFIX)/$$TARGET ; chmod +x $(PREFIX)/$$TARGET"; done) > install.sh
	
install: $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@echo make: openfido installed in $(PREFIX)
	@bash ./install.sh
uninstall:
	@rm -f $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@test -f $(SRCDIR)/uninstall.txt && rm $(cat $(SRCDIR)/uninstall.txt)
	@echo make: openfido removed from $(PREFIX)

$(PREFIX)/%: $(SRCDIR)/%
	@cp $< $@
	@chmod +x $@

# development setup
setup:
	@/usr/local/bin/python3 setup.py develop --record $(SRCDIR)/uninstall.txt

# build for release
build:
	/usr/local/bin/python3 -m pip install --upgrade build
	/usr/local/bin/python3 -m build

# test release
testpypi:
	@/usr/local/bin/python3 -m pip install --user --upgrade twine
	@/usr/local/bin/python3 -m twine upload --repository testpypi src/dist/* -c $(HOME)/.testpypirc -u __token__ -p $(TESTPYPIPWD)

# full release
pypi:
	@/usr/local/bin/python3 -m pip install --user --upgrade twine
	@/usr/local/bin/python3 -m twine upload --repository pypi src/dist/* -c $(HOME)/.pypirc -u __token__ -p $(PYPIPWD)
