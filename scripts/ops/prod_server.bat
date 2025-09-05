@echo off
set PYTHONPATH=.

call .\.venv\Scripts\activate.bat
pip install -r requirements.txt

python ASDcollector\usecase\create_solution.py
start "" python ASDcollector\bin\server.py

timeout /t 3 >nul

taskkill /IM chrome.exe /F
timeout /t 1 >nul
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk --start-fullscreen http://127.0.0.1:5000/home