#### Makefile ####
# 
# Mainly migrating from discox. A very beautiful Makefile. Some recode and recomment
#
#
##################


### CONSTANTS ###

### WE (discox developers) decided to use poetry instead of pip in order not to mess up with the main machine 
POETRY_PYTHON_PATH = $(shell poetry env info --path)
POETRY_PYTHON_PATH := $(subst  ,,$(POETRY_PYTHON_PATH)) # remove spaces

# Python path
ifeq ($(OS),Windows_NT)
	# Windows
	PYTHON = $(addsuffix \Scripts\python.exe,$(POETRY_PYTHON_PATH))
else
	# Linux
	PYTHON = $(addsuffix /bin/python,$(POETRY_PYTHON_PATH))
endif

ifeq (add,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ifeq (remove,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

# init: for initializing some packages
init:
	poetry install

# run: for running the bot
run:
	$(PYTHON) -m bot


# If you like beautifier, we have it :))
install-beautifier:
	@pip install black isort
	@echo "Successfully installed beautifier!"

# Beautify code
beautify:
	@black .
	@echo "Successfully beautified code!"
	@isort .
	@echo "Successfully sorted imports!"

# Adding a new module
add:
	@echo "Adding new module..."
	@poetry add $(RUN_ARGS)
	@echo "Updating requirements.txt..."
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Successfully added new module!"

# Remove a module
remove:
	@echo "Removing module..."
	@poetry remove $(RUN_ARGS)
	@echo "Updating requirements.txt..."
	@poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "Successfully removed module!"
