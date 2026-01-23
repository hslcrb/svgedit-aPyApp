FROM python:3.12-slim

# Install system dependencies for PyQt6
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements (if you had a requirements.txt, but we'll install directly for now)
RUN pip install --no-cache-dir PyQt6 svgelements lxml

# Copy application code
COPY app /app/app
COPY app/main.py /app/

# Set environment variable for display (user must pass this at runtime: -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix)
ENV QT_DEBUG_PLUGINS=0

# Entry point
CMD ["python", "main.py"]
