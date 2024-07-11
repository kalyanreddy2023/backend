# Use an official Python runtime as a parent image
FROM python:3.9-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the current directory contents into the container at /app
COPY . /app
 
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt
 
# Install necessary dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4
 
# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&& dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install
 
# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
&& wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
&& unzip chromedriver_linux64.zip -d /usr/local/bin/
 
# Make port 8080 available to the world outside this container
EXPOSE 8080
 
# Define environment variable
ENV APP app.py
 
# Run flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
