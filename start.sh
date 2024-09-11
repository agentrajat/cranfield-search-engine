#!/bin/bash

# Note: Launch from terminal and not from vscode
# Function to start frontend and backend
start_processes() {
    gnome-terminal -- bash -c "cd frontend && npm start"
    gnome-terminal -- bash -c "cd backend && source venv/bin/activate && python app.py"
}

# Start frontend and backend processes
start_processes

# Clean exit
exit 0
