# Copy the service file to the systemd directory for custom services
sudo cp dialogue_manager.service /etc/systemd/system/dialogue_manager.service

# Reload the systemd manager configuration to recognize the new service file
sudo systemctl daemon-reload

# Start the dialogue_manager service immediately
sudo systemctl start dialogue_manager.service

# Enable the service to start automatically at boot
sudo systemctl enable dialogue_manager.service

# Check the current status of the dialogue_manager service to ensure it’s running correctly
sudo systemctl status dialogue_manager.service

# View real-time logs for the dialogue_manager service
journalctl -u dialogue_manager.service -f
