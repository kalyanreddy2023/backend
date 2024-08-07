# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages for Edge, EdgeDriver, and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    gnupg \
    # Install Edge browser dependencies
    libxkbcommon0 \
    libatk-bridge2.0-0 \
    libgtk-3-0

# Install Microsoft Edge browser
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - \
    && wget -q https://packages.microsoft.com/config/debian/10/prod.list -O /etc/apt/sources.list.d/microsoft-prod.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable

# Install EdgeDriver
RUN EDGE_DRIVER_VERSION=$(wget -q -O - https://msedgedriver.azureedge.net/LATEST_RELEASE) \
    && wget -O /tmp/edgedriver.zip https://msedgedriver.azureedge.net/$EDGE_DRIVER_VERSION/edgedriver_linux64.zip \
    && unzip /tmp/edgedriver.zip -d /usr/local/bin/ \
    && rm /tmp/edgedriver.zip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Expose the port that your app runs on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
