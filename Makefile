CODE_FOLDERS := server
TEST_FOLDERS := tests

.PHONY: install lint security_checks

install:
	poetry install

lint:
	ruff check .
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)

security_checks:
	bandit -r $(CODE_FOLDERS)

