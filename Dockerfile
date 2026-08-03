# FAIOS Automation Daemon - Production Docker Image
# Uses Python 3.11 slim + Playwright Chromium for graphic card rendering

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps for Playwright Chromium
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxext6 \
    libxcursor1 \
    libxi6 \
    libxtst6 \
    fonts-liberation \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY 08-Automation/scripts/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium browser
RUN python -m playwright install chromium

# Copy entire project
COPY . .

# Set working directory to scripts folder
WORKDIR /app/08-Automation/scripts

# Environment variables (overridden by Render env vars)
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Expose port for health check (keeps Render free plan awake)
EXPOSE 10000

# Start the FAIOS master daemon
CMD ["python", "master_daily_pipeline_cmo.py"]
