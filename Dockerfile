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
    libxkbcommon0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    curl \
&& rm -rf /var/lib/apt/lists/*  # Clean up APT cache to reduce image size

# Add the Microsoft Edge repository and install Edge
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
&& echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/repos/edge stable main" | tee /etc/apt/sources.list.d/microsoft-prod.list \
&& apt-get update \
&& apt-get install -y microsoft-edge-stable \
&& rm -rf /var/lib/apt/lists/*  # Clean up APT cache to reduce image size

# Install EdgeDriver
RUN EDGE_DRIVER_VERSION=$(curl -s https://msedgedriver.azureedge.net/LATEST_RELEASE) \
&& echo "EdgeDriver version: $EDGE_DRIVER_VERSION" \
&& if [ -z "$EDGE_DRIVER_VERSION" ]; then echo "Failed to fetch EdgeDriver version"; exit 1; fi \
&& curl -s -o /tmp/edgedriver.zip https://msedgedriver.azureedge.net/$EDGE_DRIVER_VERSION/edgedriver_linux64.zip \
&& if [ ! -f /tmp/edgedriver.zip ]; then echo "EdgeDriver ZIP file not downloaded"; exit 1; fi \
&& ls -l /tmp/edgedriver.zip \
&& unzip /tmp/edgedriver.zip -d /usr/local/bin/ \
&& rm /tmp/edgedriver.zip

# Install Python dependencies
COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

# Expose the port that your app runs on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

