#!/usr/bin/env bash

if [[ -n "$1" ]]
then
  poetry run alembic revision -m "$1"
fi