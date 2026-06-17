#!/bin/bash
# Starts Xvfb, x11vnc, noVNC, and the game in one command.
# View the game at the forwarded port 6080 in VS Code's Ports tab.

# Set up XDG runtime dir
mkdir -p /tmp/runtime-$USER
chmod 700 /tmp/runtime-$USER
export XDG_RUNTIME_DIR=/tmp/runtime-$USER
export DISPLAY=:99
DISPLAY_NUM="${DISPLAY#:}"

port_open() {
    local host="$1"
    local port="$2"
    if command -v nc >/dev/null 2>&1; then
        nc -z "$host" "$port" >/dev/null 2>&1
    else
        # Bash TCP probe fallback when netcat is unavailable.
        (echo >/dev/tcp/"$host"/"$port") >/dev/null 2>&1
    fi
}

# Kill all existing instances to ensure correct resolution
pkill -9 -f "python main.py" 2>/dev/null
pkill -9 -f "x11vnc" 2>/dev/null
pkill -9 -f "novnc_proxy" 2>/dev/null
pkill -9 -f "websockify" 2>/dev/null
pkill -9 -f "Xvfb" 2>/dev/null
sleep 2

# Start VNC stack
echo "Starting Xvfb..."
if xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
    echo "X display $DISPLAY already active, reusing it."
else
    # Clean up stale lock/socket from a crashed Xvfb instance.
    rm -f "/tmp/.X${DISPLAY_NUM}-lock" "/tmp/.X11-unix/X${DISPLAY_NUM}"
    Xvfb "$DISPLAY" -screen 0 1920x1080x24 -extension DPMS -ac >/tmp/xvfb.log 2>&1 &
fi

# Wait for Xvfb to accept connections before launching x11vnc.
echo "Waiting for X display $DISPLAY..."
for i in $(seq 1 20); do
    if xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
        echo "X display $DISPLAY is ready."
        break
    fi
    sleep 1
done

if ! xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
    echo "Xvfb failed to start on $DISPLAY. See /tmp/xvfb.log"
    exit 1
fi

echo "Starting x11vnc..."
x11vnc -display "$DISPLAY" -nopw -listen localhost -xkb -forever -quiet -rfbport 5900 >/tmp/x11vnc.log 2>&1 &

# Wait until x11vnc is actually listening on port 5900 (up to 15 seconds)
echo "Waiting for x11vnc on port 5900..."
for i in $(seq 1 15); do
    if port_open localhost 5900; then
        echo "x11vnc is ready."
        break
    fi
    sleep 1
done

if ! port_open localhost 5900; then
    echo "x11vnc failed to bind to port 5900. See /tmp/x11vnc.log"
    exit 1
fi

echo "Starting noVNC..."
/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
sleep 1

# Create venv if it doesn't exist, then install dependencies and run
if [ ! -f ".venv/bin/python" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi
echo "Installing dependencies..."
.venv/bin/pip install -q -r requirements.txt
.venv/bin/python main.py
