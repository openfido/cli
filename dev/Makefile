SOURCE=$(PWD)/cli/src
TARGET=/usr/local/bin
CACHE=/usr/local/share/openfido

install: $(wildcard $(TARGET)/openfido*) $(patsubst %/openfido.json,$(CACHE)/%,$(wildcard */openfido.json))

uninstall:
	@echo "Uninstalling openfido from $(TARGET)..."
	@rm -f $(TARGET)/openfido*
	@echo "Cleaning openfido cache in $(CACHE)..."
	@rm -rf $(CACHE)/*

docs: $(patsubst %/openfido.json,%/README.md,$(wildcard */openfido.json))

clean:
	@echo "Cleaning README.md files..."
	@rm -f $(patsubst %/openfido.json,%/README.md,$(wildcard */openfido.json))

$(TARGET)/openfido%: $(SOURCE)/openfido%
	@echo "Installing $@..."
	@cp -p $? $@

$(CACHE)/%: %/__init__.py %/openfido.json %/README.md
	@echo "Installing $@..."
	@mkdir -p $@
	@cp $? $@
	@touch $@

%/README.md: %/__init__.py
	@echo "Updating $@..."
	@(export PYTHONPATH=$(SOURCE); $(TARGET)/python3 -c "import openfido_util as of; print(of.get_help('$<'))" ) 1>$@ || (echo "ERROR: unable to update $@" > /dev/stderr; rm -f $@; false)

.PHONY: install

.SUFFIXES: 
