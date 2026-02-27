@echo off
echo ======================================
echo  TRADING AUTOMATION - QUICK START
echo ======================================
echo.

cd backend

echo [1/2] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/2] Starting Flask server...
echo.
echo Dashboard: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app.py

pause
