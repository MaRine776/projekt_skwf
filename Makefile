
DIR := src/
TARGET1 := reader.py
TARGET2 := parser.py
TARGET3 := main.py
RUNNER := python
run:
	$(RUNNER) $(DIR)$(TARGET3)
	
parse:
	$(RUNNER) $(DIR)$(TARGET2)
	
read:
	$(RUNNER) $(DIR)$(TARGET1)

clean:
	rm $(DIR)mapa.json
	@echo " Cleaning..."; 


.PHONY: clean
.PHONY: parse
.PHONY: run
