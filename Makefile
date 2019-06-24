################ PATH ###################
PATH_TEST    = test/
PATH_SRC     = aergen/
PATH_DATA    = ./
PATH_PARAMS  = $(PATH_SRC)params/
PATH_CORE    = $(PATH_SRC)core/
PATH_FACTORY = $(PATH_SRC)factory/
################ EXEC ###################
MAIN_TEST	= $(PATH_TEST)main.py
WRITER_EXEC = $(PATH_SRC)writer.py
READER_EXEC = $(PATH_SRC)reader.py
CUTTER_EXEC = $(PATH_SRC)cutter.py
########### DEFAULT PARAMS ##############
FACTORY = protocol.py
################ ENV ###################
PY = python3


winput:
	$(PY) $(WRITER_EXEC) -f $(PATH_FACTORY)$(FACTORY) -p $(PATH_PARAMS)$(PARAMS) -o $(PATH_DATA)$(OUTPUT) $(ARGS)

rinput:
	$(PY) $(READER_EXEC) -f $(PATH_DATA)$(FILE) $(ARGS)

cinput:
	$(PY) $(CUTTER_EXEC) -f $(PATH_DATA)$(FILE) -o $(PATH_DATA)$(OUTPUT) $(ARGS)

run_test:
	$(PY) -m unittest discover test -v

clean :
	rm -rf $(PATH_TEST)*.pyc $(PATH_SRC)*.pyc $(PATH_INPUT)*.pyc
	rm -rf $(PATH_TEST)__pycache__/ $(PATH_SRC)__pycache__/ $(PATH_INPUT)__pycache__/


.PHONY: clean winput rinput main
