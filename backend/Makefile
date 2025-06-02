VENV_BIN = .venv/bin
PYTHON = $(VENV_BIN)/python3
PIP = $(VENV_BIN)/pip

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  install-deps   Install depedencies"
	@echo "  run-server     Start local API server"
	@echo "  test           Run tests"
	@echo "  static-checks  Run static checks"
	@echo "  reformat       Reformat code"
	@echo "  clean          Clean up all generated files"
	@echo ""

.venv:
	python3 -m venv .venv

.PHONY: install-deps
install-deps: .venv
	$(PIP) install -r requirements.txt

.PHONY: run-server
run-server:
	$(PYTHON) -m uvicorn src.server:app --reload

.PHONY: test
test:
	$(PYTHON) -m pytest

.PHONY: static-checks
static-checks:
	$(PYTHON) -m flake8 . --exclude=.venv,conviction_rules.py
	$(PYTHON) -m pylint . --ignore=.venv --ignore-patterns=conviction_rules.py --rcfile pylint.rc
	$(PYTHON) -m black . --check --exclude '/(\.venv|conviction_rules\.py)/'

.PHONY: reformat
reformat:
	$(PYTHON) -m black .

.PHONY: clean
clean:
	rm -rf .venv
