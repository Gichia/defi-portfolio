#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/prestart.py

# Run migrations
alembic upgrade head
