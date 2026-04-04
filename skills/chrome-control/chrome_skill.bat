@echo off
REM Chrome Control Skill - Quick Commands
REM Usage:
REM   chrome_skill.bat tabs
REM   chrome_skill.bat navigate https://example.com
REM   chrome_skill.bat screenshot
REM   chrome_skill.bat title
REM   chrome_skill.bat click "#submit"
REM   chrome_skill.bat type "#search" "hello"

set SCRIPT_DIR=%~dp0
set PYTHON_SCRIPT=%SCRIPT_DIR%chrome_skill.py

if "%1"=="" (
    python %PYTHON_SCRIPT%
    goto :end
)

if "%1"=="tabs" (
    python %PYTHON_SCRIPT% tabs
    goto :end
)

if "%1"=="navigate" (
    python %PYTHON_SCRIPT% navigate %2
    goto :end
)

if "%1"=="screenshot" (
    if "%2"=="" (
        python %PYTHON_SCRIPT% screenshot
    ) else (
        python %PYTHON_SCRIPT% screenshot %2
    )
    goto :end
)

if "%1"=="title" (
    python %PYTHON_SCRIPT% title
    goto :end
)

if "%1"=="content" (
    python %PYTHON_SCRIPT% content %2
    goto :end
)

if "%1"=="click" (
    python %PYTHON_SCRIPT% click %2
    goto :end
)

if "%1"=="type" (
    python %PYTHON_SCRIPT% type %2 %3
    goto :end
)

echo Unknown command: %1
echo.
echo Available commands:
echo   chrome_skill.bat tabs
echo   chrome_skill.bat navigate [url]
echo   chrome_skill.bat screenshot [path]
echo   chrome_skill.bat title
echo   chrome_skill.bat click [selector]
echo   chrome_skill.bat type [selector] [text]

:end
