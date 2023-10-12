@echo off
call venv\Scripts\activate.bat
echo Sorting imports with isort...
python -m isort historyjki_roblox
echo Formatting code with black...
python -m black .
deactivate