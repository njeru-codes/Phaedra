#!/bin/bash

LOG_FILE="installation.log"

# Function to log echo messages
log_message() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check for sudo/root permissions
if [ "$EUID" -ne 0 ]; then
    echo -e "Please run as root or use sudo\n\n"
    exit 1
fi

echo -e "\n"
echo "Start installation"

# Variables
SCRIPT_NAME="sniffer.py"
TARGET_NAME="dns_sniffer"
TARGET_DIR="/usr/local/bin"
REQUIREMENTS_FILE="requirements.txt"

# Install system dependencies
echo -e "Installing dependencies..."
apt update -y
apt install -y python3 python3-pip

# Install Python dependencies globally
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing Python dependencies from $REQUIREMENTS_FILE globally..."
    pip3 install --upgrade pip --break-system-packages
    pip3 install -r "$REQUIREMENTS_FILE" --break-system-packages
else
    echo "No $REQUIREMENTS_FILE found. Exiting installation."
    exit 1
fi

chmod +x "$SCRIPT_NAME"                 # Make the script executable
echo "Renaming script to $TARGET_NAME..."
cp "$SCRIPT_NAME" "$TARGET_DIR/$TARGET_NAME"  # Move script to target directory

log_message "Moving $TARGET_NAME to $TARGET_DIR..."  # Log the move

# Step 11: Finish installation
if [ -f "$TARGET_DIR/$TARGET_NAME" ]; then
    log_message "Installation complete! You can now run the script using: sudo $TARGET_NAME"
else
    log_message "Installation failed. Please check for errors."
    exit 1
fi
