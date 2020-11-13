#!/usr/bin/env bash
# Evil bash because venv doesn't seam to support standart POSIX shell

deactivate || true

FILE="./tests/secrets/.env"
if test -f "$FILE"; then
    :
else
    echo "No credentials file found!"
    exit 1
fi

rm -r ./tamo-venv
python3 -m venv tamo-venv
source tamo-venv/bin/activate
pip3 install -r requirements.txt
python3 -m unittest tests.test
