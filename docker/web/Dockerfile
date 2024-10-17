# Use the official Python 3.12 slim image as the base
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Install initial system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
        nano \
        curl \
        unzip \
        ca-certificates \
        gnupg \
        chromium \
        chromium-driver \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Create a non-root user and adjust permissions for better security
RUN adduser --disabled-password --no-create-home user && \
    chown -R user:user /app

# Switch to the non-root user
USER user

# Set environment variables to help Selenium locate Chromium and ChromeDriver
ENV CHROMIUM_BIN=/usr/bin/chromium \
    CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Expose the application port
EXPOSE 8000
