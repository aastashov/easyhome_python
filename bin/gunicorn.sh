#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

echo "Run uWSGI"
gunicorn --chdir=/src --bind=127.0.0.1:8080 --workers=2 config.wsgi:application
