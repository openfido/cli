.SUFFIXES:

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
GITHUB=https://raw.githubusercontent.com/openfido/cli/main/src

install.sh: $(foreach TARGET,$(TARGETS),src/$(TARGET))
	@(for TARGET in $(TARGETS); do echo "curl -sL $(GITHUB)/$$TARGET > $(PREFIX)/$$TARGET ; chmod +x $(PREFIX)/$$TARGET"; done) > install.sh
	
install: $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@echo make: openfido installed in $(PREFIX)

uninstall:
	@rm -f $(foreach TARGET,$(TARGETS),$(PREFIX)/$(TARGET))
	@echo make: openfido removed from $(PREFIX)

$(PREFIX)/%: src/%
	@cp $< $@
	@chmod +x $@