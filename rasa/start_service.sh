#!/bin/bash

# Define ports and log files (optional)
RASA_PORT=5005
ACTIONS_PORT=5055
RASA_LOG="rasa_server.log"
ACTIONS_LOG="action_server.log"

# Start the Rasa server
echo "Starting Rasa server on port $RASA_PORT..."
rasa run --enable-api --cors "*" --port $RASA_PORT > $RASA_LOG 2>&1 &

# Capture the Rasa server process ID
RASA_PID=$!
echo "Rasa server started with PID $RASA_PID, logging to $RASA_LOG"

# Start the Rasa action server
echo "Starting Rasa action server on port $ACTIONS_PORT..."
rasa run actions --port $ACTIONS_PORT > $ACTIONS_LOG 2>&1 &

# Capture the action server process ID
ACTIONS_PID=$!
echo "Action server started with PID $ACTIONS_PID, logging to $ACTIONS_LOG"

# Wait for both servers to start
sleep 5
echo "Servers are running. Access Rasa at http://localhost:$RASA_PORT"

# Optional: Use `wait` to keep the script running if you want to monitor the servers
# wait $RASA_PID $ACTIONS_PID
