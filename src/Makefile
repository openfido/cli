BIN=/usr/local/bin
FILES=$(BIN)/openfido $(BIN)/openfido.py $(BIN)/openfido_util.py

help:
	@echo "Valid targets:"
	@echo "  make install"
	@echo "  make uninstall"
	
install: $(FILES)

$(BIN)/openfido: openfido
	cp $< $@
	chmod +x $@

$(BIN)/openfido.py: openfido.py
	cp $< $@

$(BIN)/openfido_util.py: openfido_util.py
	cp $< $@

uninstall: 
	rm -f $(FILES)
