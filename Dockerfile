# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirement.txt
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
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
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN set -ex \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN set -ex \
    && CHROMEDRIVER_VERSION=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV APP app.py

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
