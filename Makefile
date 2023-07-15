#!make
UNAME_S := $(shell uname -s)
PYTHON_FILES := $(find {tests,config,hsearch} -name '*.py' -not -path '*/migrations/*')
ifeq ($(UNAME_S),Darwin)
	PYTHON_FILES = $$(find {tests,config,hsearch} -name '*.py' -not -path '*/migrations/*')
endif

install:
	poetry install --only main,local,qa --no-root

install-ci:
	poetry config virtualenvs.create false
	poetry install --only main,qa --no-root

	# Dirty hack to prevent mypy overwriting basedmypy executable
	pip uninstall -y basedmypy
	poetry install -vv

install-deploy:
	poetry config virtualenvs.create false
	poetry install --only main --no-root --no-cache

test:
	pytest tests -vv --cov=hsearch

lint:
	mypy .
	pycln -c .
	isort -c .
	black --check --diff .

# Development
# ----------------------------------------------------------------------------
format:
	pycln -a .
	isort .
	black .
	add-trailing-comma ${PYTHON_FILES}

ignore:
	mypy --write-baseline .

run-flower:
	@celery --app config flower --port=5566

run-celery:
	@celery -A config worker --beat --loglevel=info --max-tasks-per-child=100 -n worker@%h
