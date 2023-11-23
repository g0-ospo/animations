#!/bin/sh

#
# sessions.sh
# Author: Niroshan Rajadurai (@niroshan)
# Enterprise: https://www.github.com/galacticnaut
# Description: This script will create a virtual environment and install all the required packages for the project
# Usage: ./utils/sessions.sh
# License: MIT License
#

pip3 install virtualenv

python3 -m venv virtual_env/venv-u64

source virtual_env/venv-u64/bin/activate

# run pip inside the virtual environment
pip3 install --upgrade pip
pip3 install -r requirements.txt