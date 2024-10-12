PROJECT_DIR := kiota_http

.PHONY: build
build:
	@echo "Running yapf" && yapf -dr ${PROJECT_DIR}
	@echo "Running isort" && isort ${PROJECT_DIR}
	@echo "Running pylint" && pylint ${PROJECT_DIR} --disable=W --rcfile=.pylintrc
	@echo "Running mypy" && mypy ${PROJECT_DIR}

.PHONY: test
test:
	@echo "Running test" && pytest tests
