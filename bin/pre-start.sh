#!/usr/bin/env bash

echo "Running migrations..."
./manage.py migrate --noinput && \
  echo "Migrations completed successfully" || EXIT_CODE=$?

echo "Running collect static..."
./manage.py collectstatic --noinput && \
  echo "Collect static completed successfully" || EXIT_CODE=$?

exit ${EXIT_CODE}
