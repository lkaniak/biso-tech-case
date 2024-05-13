#! /usr/bin/env bash

alembic upgrade head

# Create initial data in DB
python /app/scripts/py/initial_data.py