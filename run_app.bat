@echo off
REM This batch file sets up the environment and runs the PDF Editor application.

REM Set the title of the command prompt window.
TITLE PDF Editor Launcher

ECHO ###################################
ECHO #   PDF Editor Launcher Script    #
ECHO ###################################
ECHO.

REM --- Step 1: Check for Python ---
REM We first check if Python is installed and accessible from the command line.
REM 'python --version' redirects its output to 'nul' (a black hole) so it doesn't clutter the screen.
REM If the command fails, ERRORLEVEL will be non-zero.
ECHO Checking for Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ERROR: Python is not installed or not added to your system's PATH.
    ECHO Please install Python 3.8+ from python.org and ensure "Add Python to PATH" is checked during installation.
    PAUSE
    EXIT /B
)
ECHO Python installation found.
ECHO.

REM --- Step 2: Create Virtual Environment ---
REM We use a virtual environment to keep the app's dependencies isolated from other Python projects.
REM This prevents version conflicts. We'll name the environment folder 'venv'.
SET VENV_DIR=venv

REM Check if the 'venv' directory already exists. If not, create it.
IF NOT EXIST %VENV_DIR% (
    ECHO Creating virtual environment in '%VENV_DIR%' folder...
    python -m venv %VENV_DIR%
    IF %ERRORLEVEL% NEQ 0 (
        ECHO ERROR: Failed to create virtual environment.
        PAUSE
        EXIT /B
    )
    ECHO Virtual environment created successfully.
) ELSE (
    ECHO Virtual environment already exists.
)
ECHO.

REM --- Step 3: Activate Environment and Install Dependencies ---
ECHO Activating virtual environment...
CALL %VENV_DIR%\Scripts\activate.bat

ECHO.
ECHO Installing required packages (streamlit, PyPDF2)...
pip install -r ../requirements.txt
ECHO.

REM --- Step 4: Run the Streamlit App ---
ECHO Starting the PDF Editor application...
ECHO Your web browser should open with the application shortly.
streamlit run ../app.py
