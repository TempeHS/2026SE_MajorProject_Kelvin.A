#!/bin/bash
# Starts Xvfb, x11vnc, noVNC, and the game in one command.
# View the game at the forwarded port 6080 in VS Code's Ports tab.

# Set up XDG runtime dir
mkdir -p /tmp/runtime-$USER
chmod 700 /tmp/runtime-$USER
export XDG_RUNTIME_DIR=/tmp/runtime-$USER

# Kill all existing instances to ensure correct resolution
pkill -9 -f "python main.py" 2>/dev/null
pkill -9 -f "x11vnc" 2>/dev/null
pkill -9 -f "novnc_proxy" 2>/dev/null
pkill -9 -f "websockify" 2>/dev/null
pkill -9 -f "Xvfb" 2>/dev/null
sleep 2

# Start VNC stack
echo "Starting Xvfb..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1

echo "Starting x11vnc..."
x11vnc -display :99 -nopw -listen localhost -xkb -forever -quiet -rfbport 5900 &
sleep 1

echo "Starting noVNC..."
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
sleep 1

# Run the game
DISPLAY=:99 python main.py
