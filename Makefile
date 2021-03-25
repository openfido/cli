.SUFFIXES:

#
# Configuration info
#
PACKAGE=openfido
PYPIUSER=openfido
PYPIPASSWORD=$(shell /usr/local/bin/python3 -m keyring get https://test.pypi.org/openfido/ openfido)
PYPITESTURL=https://test.pypi.org/simple/openfido
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
	@echo "  test         test release python module"
	@echo "  release      release python module"

install.sh: $(foreach TARGET,$(TARGETS),$(SRCDIR)/$(TARGET))
	@(for TARGET in $(TARGETS); do echo "curl -sL $(GITHUB)/$$TARGET > $(PREFIX)/$$TARGET ; chmod +x $(PREFIX)/$$TARGET"; done) > install.sh
	
install: $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@echo make: openfido installed in $(PREFIX)

uninstall:
	@rm -f $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@test -f uninstall.txt && rm $(cat uninstall.txt)
	@echo make: openfido removed from $(PREFIX)

$(PREFIX)/%: $(SRCDIR)/%
	@cp $< $@
	@chmod +x $@

# development setup
setup:
	@/usr/local/bin/python3 setup.py develop --record uninstall.txt

# build for release
build:
	/usr/local/bin/python3 -m pip install --upgrade build
	/usr/local/bin/python3 -m build

# test release
test:
	/usr/local/bin/python3 -m pip install --user --upgrade twine
	/usr/local/bin/python3 -m keyring get $(PYPITESTURL) $(PYPIUSER)
	/usr/local/bin/python3 -m twine upload --repository testpypi src/dist/* -u __token__ -p $$(/usr/local/bin/python3 -m keyring get $(PYPITESTURL) $(PYPIUSER))
	/usr/local/bin/python3 -m pip install --index-url $(PYPITESTURL) --no-deps $(PACKAGE)
	/usr/local/bin/openfido --version

# full release
release:
	python3 -m pip install --index-url $(PYPIURL) --no-deps $(PACKAGE)
