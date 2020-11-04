BIN=/usr/local/bin
FILES=$(BIN)/openfido $(BIN)/openfido.py

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

uninstall: 
	rm -f $(FILES)
