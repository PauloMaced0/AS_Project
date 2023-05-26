# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
