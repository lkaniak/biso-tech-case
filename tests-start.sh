#! /usr/bin/env bash
set -e
set -x
old_env=$ENVIRONMENT
export ENVIRONMENT=staging

python /app/scripts/py/initial_test_data.py

python /app/src/tests/tests_pre_start.py

bash ./scripts/unix/test.sh "$@"
export ENVIRONMENT=$old_env