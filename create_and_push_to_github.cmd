@echo off
REM Script to create GitHub repository and push HAL project
REM Run this script to automate the process

echo ============================================================
echo HAL GitHub Repository Setup
echo ============================================================
echo.

echo Step 1: Authenticate with GitHub
echo ---------------------------------
echo This will open your browser to authenticate...
echo.
pause

gh auth login

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Authentication failed
    echo Please try again
    pause
    exit /b 1
)

echo.
echo ✓ Authentication successful!
echo.

echo Step 2: Create Repository
echo ---------------------------------
echo Creating repository 'lcsmd/hal' on GitHub...
echo.

gh repo create lcsmd/hal --private --source=. --remote=origin --description "HAL Personal AI Assistant - OpenQM database with medical, financial, and voice interface"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Repository creation failed
    echo It may already exist - continuing with push...
    echo.
)

echo.
echo Step 3: Push to GitHub
echo ---------------------------------
echo Pushing all commits to GitHub...
echo.

git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Push failed
    echo Check the error message above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo SUCCESS! Repository created and pushed to GitHub
echo ============================================================
echo.
echo Repository URL: https://github.com/lcsmd/hal
echo.
echo You can now:
echo - View your repository at the URL above
echo - Clone it from other machines
echo - Collaborate with others
echo.
pause
