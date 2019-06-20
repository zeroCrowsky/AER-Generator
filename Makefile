################ PATH ###################
PATH_TEST          = test/
PATH_SRC           = aergen/
PATH_DATA          = ""# $(PATH_SRC)data/
PATH_PARAMS        = ""# $(PATH_SRC)params/
PATH_VIEWER        = ""# $(PATH_SRC)viewer/
PATH_INPUT         = ""# $(PATH_SRC)input/
PATH_MODEL         = ""# $(PATH_SRC)models/
PATH_INPUT_DATA    = ""# $(PATH_DATA)inputs/
PATH_INPUT_FACTORY = ""# $(PATH_INPUT)factory/
PATH_INPUT_PARAMS  = ""# $(PATH_INPUT)params/
################ EXEC ###################
MAIN_TEST	      = $(PATH_TEST)main.py
WRITER_INPUT_EXEC = $(PATH_INPUT)writer.py
READER_INPUT_EXEC = $(PATH_INPUT)reader.py
CUTTER_INPUT_EXEC = $(PATH_INPUT)cutter.py
################ ENV ###################
PY = python3

winput:
	$(PY) $(WRITER_INPUT_EXEC) -f $(PATH_INPUT_FACTORY)$(FACTORY) -p $(PATH_INPUT_PARAMS)$(PARAMS) -o $(PATH_INPUT_DATA)$(OUTPUT) $(ARGS)

rinput:
	$(PY) $(READER_INPUT_EXEC) -f $(PATH_INPUT_DATA)$(FILE) $(ARGS)

cinput:
	$(PY) $(CUTTER_INPUT_EXEC) -f $(PATH_INPUT_DATA)$(FILE) -o $(PATH_INPUT_DATA)$(OUTPUT) $(ARGS)

run_test:
	$(PY) -m unittest discover test -v

clean :
	rm -rf $(PATH_TEST)*.pyc $(PATH_SRC)*.pyc $(PATH_INPUT)*.pyc $(PATH_MODEL)*.pyc $(PATH_VIEWER)*.pyc
	rm -rf $(PATH_TEST)__pycache__/ $(PATH_SRC)__pycache__/ $(PATH_INPUT)__pycache__/ $(PATH_MODEL)__pycache__/ $(PATH_VIEWER)__pycache__/


.PHONY: clean winput rinput main
