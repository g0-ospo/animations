@echo off


pip3 install virtualenv

python -m venv virtual_env\venv
.\virtual_env\venv\Scripts\Activate.bat
pip3 install -r requirements.txt