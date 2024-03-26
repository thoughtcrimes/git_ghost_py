@echo off

:: Prompt for commit message
set /p CommitMessage=Enter commit message: 

:: Check if the commit message is empty
if "%CommitMessage%"=="" (
    echo Commit message cannot be empty.
    exit /b 1
)

git add .
rem Commit changes with a message
git commit -m "%CommitMessage%"

git push origin -u