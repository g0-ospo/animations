#!/bin/sh

pip3 install virtualenv

python3 -m venv virtual_env/venv
source virtual_env/venv/bin/activate
pip3 install -r requirements.txt