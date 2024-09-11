#!/bin/bash

cd backend || exit 1
python3 -m venv venv
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "Failed to activate virtual environment."
    exit 1
fi
pip install -r requirements.txt || {
    echo "Failed to install Python dependencies."
    exit 1
}
python install.py || {
    echo "Failed to run install.py."
    exit 1
}
deactivate

git clone https://github.com/usnistgov/trec_eval.git
cd trec_eval
# Uncomment below command if make is not installed
# sudo apt-get install build-essential
make

cd ..
cd ..

cd frontend || exit 1
npm install || {
    echo "Failed to install Node.js modules."
    exit 1
}

cd ..

echo "Python virtual environment and Node.js modules installed successfully"
echo "Launch start.sh to start the application"