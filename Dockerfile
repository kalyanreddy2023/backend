# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update \
    && apt-get install -y wget unzip gnupg \
    && apt-get install -y \
        libx11-dev \
        libxkbcommon-x11-0 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        libxss1 \
        libnss3 \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libgbm1 \
        --no-install-recommends \
    && apt-get clean

# Install Microsoft Edge
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" | tee /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update \
    && apt-get install -y microsoft-edge-stable

# Install EdgeDriver
RUN EDGE_VERSION=$(wget -q -O - https://msedgedriver.azureedge.net/LATEST_RELEASE) \
    && wget -O /tmp/edgedriver_linux64.zip https://msedgedriver.azureedge.net/$EDGE_VERSION/edgedriver_linux64.zip \
    && unzip /tmp/edgedriver_linux64.zip -d /usr/local/bin/ \
    && rm /tmp/edgedriver_linux64.zip

# Install Python Selenium package
RUN pip install selenium

# Set up the working directory
WORKDIR /app

# Copy your application code if needed
# COPY . /app

# Command to run your application
# CMD ["python", "your_script.py"]

# Expose any ports if necessary
# EXPOSE 8080
