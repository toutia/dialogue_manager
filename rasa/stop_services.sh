#!/bin/bash

# Define ports and log files (optional)
RASA_PORT=5005
ACTIONS_PORT=5055
RASA_LOG="rasa_server.log"
ACTIONS_LOG="action_server.log"

# Function to stop a server if it's running
stop_server() {
    local pid=$1
    if [ -n "$pid" ]; then
        echo "Stopping server with PID $pid..."
        kill "$pid"
        wait "$pid" 2>/dev/null
        echo "Server stopped."
    fi
}

# Check if Rasa server is running
RASA_PID=$(lsof -ti:$RASA_PORT)
if [ -n "$RASA_PID" ]; then
    stop_server "$RASA_PID"
else
    echo "No Rasa server running on port $RASA_PORT."
fi

# Check if Action server is running
ACTIONS_PID=$(lsof -ti:$ACTIONS_PORT)
if [ -n "$ACTIONS_PID" ]; then
    stop_server "$ACTIONS_PID"
else
    echo "No Action server running"
fi