.DEFAULT_GOAL := install

install:
	# Make sure that you are using a venv
	pip install -e .

new-project:
	putup 

.PHONY: install new-project