@echo off
echo ======================================
echo  PUSH TO GITHUB
echo ======================================
echo.

echo Checking .gitignore...
if not exist .gitignore (
    echo Creating .gitignore...
    echo .env > .gitignore
    echo *.db >> .gitignore
    echo __pycache__/ >> .gitignore
)

echo.
echo Initializing Git repository...
git init

echo.
echo Adding all files...
git add .

echo.
echo Creating commit...
git commit -m "Initial commit: Trading Automation System with 70%% accuracy"

echo.
echo Creating main branch...
git branch -M main

echo.
echo Adding remote repository...
git remote add origin https://github.com/nileshkumarburman1993-web/nif.git

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ======================================
echo  DONE! Check GitHub:
echo  https://github.com/nileshkumarburman1993-web/nif
echo ======================================
pause
