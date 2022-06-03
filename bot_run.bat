@echo off

call %~dp0telegram_bot_project\venv\Scripts\activate

cd %~dp0telegram_bot_project

set TOKEN=5318034841:AAE8LwugFT2Ne-cRpFH6QdJ0mD398M2WiYU

python bot_telegram.py

pause