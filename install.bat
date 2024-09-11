echo @off

cd backend
python -m venv venv
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) ELSE (
    echo Failed to activate virtual environment.
    exit /b 1
)
pip install -r requirements.txt || (
    echo Failed to install Python dependencies.
    exit /b 1
)
python install.py || (
    echo Failed to run install.py.
    exit /b 1
)
call deactivate

cd ..
cd frontend
call npm install || (
    echo Failed to install Node.js modules.
    exit /b 1
)

cd ..

echo Python virtual environment and Node.js modules installed successfully
echo Launch start.bat to start the application

pause