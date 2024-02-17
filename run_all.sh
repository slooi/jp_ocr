#!/bin/bash

# Change directory to server and run npm run dev
cd server
npm run dev &
cd ..

# Change directory to clientReceiver and run npm run dev
cd clientReceiver
npm run dev &
cd ..

# Activate virtual environment for Python
source client/venv/Scripts/activate

# Run Python file
python client/main.py &

# Deactivate virtual environment after Python execution
deactivate
