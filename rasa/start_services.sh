#!/bin/bash

# Define ports and log files
RASA_PORT=5005
ACTIONS_PORT=5055
RASA_LOG="rasa_server.log"
ACTIONS_LOG="action_server.log"
VENV_PATH="/home/touti/dev/dialog_manager/pythonenvs/.venv_dm_server"

# Function to stop servers on exit
cleanup() {
    echo "Stopping servers..."
    kill "$RASA_PID" "$ACTIONS_PID" 2>/dev/null
    deactivate
}
trap cleanup EXIT

echo "Activating the virtual environment..."
source "$VENV_PATH/bin/activate" || { echo "Failed to activate virtual environment"; exit 1; }

# Start the Rasa server
echo "Starting Rasa server on port $RASA_PORT..."
rasa run --enable-api --cors "*" --port $RASA_PORT > "$RASA_LOG" 2>&1 &
RASA_PID=$!
if ! kill -0 $RASA_PID 2>/dev/null; then
    echo "Failed to start Rasa server. Check $RASA_LOG for details."
    exit 1
fi
echo "Rasa server started with PID $RASA_PID, logging to $RASA_LOG"

# Start the Rasa action server
echo "Starting Rasa action server on port $ACTIONS_PORT..."
rasa run actions --port $ACTIONS_PORT > "$ACTIONS_LOG" 2>&1 &
ACTIONS_PID=$!
if ! kill -0 $ACTIONS_PID 2>/dev/null; then
    echo "Failed to start action server. Check $ACTIONS_LOG for details."
    exit 1
fi
echo "Action server started with PID $ACTIONS_PID, logging to $ACTIONS_LOG"

# Wait for servers to keep script alive
echo "Servers are running. Access Rasa at http://localhost:$RASA_PORT"
wait
