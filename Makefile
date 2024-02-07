#!make

install:
	@if [ -f .env ]; then \
        echo "The project already installed."; \
    else \
		poetry install --only main,local,qa --no-root; \
      	cp .env.example .env; \
        echo "Installed!"; \
    fi

install-ci:
	poetry config virtualenvs.create false
	poetry install --only main,qa --no-root

install-deploy:
	poetry config virtualenvs.create false
	poetry install --only main,prod --no-root --no-cache

test-ci:
	pytest tests -vv --doctest-modules --junitxml=junit/test-results.xml --cov=easyhome --cov-report=xml --cov-report=html

lint:
	mypy .
	ruff check easyhome/
	ruff check tests/

# Development
# ----------------------------------------------------------------------------
test:
	pytest tests -vv --cov=easyhome --cov-report html

format:
	ruff check --fix easyhome/
	ruff check --fix tests/

ignore:
	mypy --write-baseline .
	ruff check --add-noqa easyhome/
	ruff check --add-noqa tests/
