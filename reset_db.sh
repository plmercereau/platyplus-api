#!/bin/bash
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
./manage.py makemigrations
./manage.py migrate