# Makefile with phony targets
.PHONY: setup
OS := $(uname)

.ONESHELL:
SHELL:=/opt/homebrew/bin/fish

# .SHELLFLAGS += -e
setup: $(eval SHELL:=/opt/homebrew/bin/fish) ## Setup Environment
	uv venv
	source .venv/bin/activate.fish
	uv sync
	python -m ensurepip

build:
	maturin develop

shell:
	@make build
	ipython -i setup_shell.py