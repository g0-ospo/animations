@echo off


pip3 install virtualenv

python -m venv virtual_env\venv-w64
call .\virtual_env\venv-w64\Scripts\Activate.bat
pip3 install -r requirements.txt