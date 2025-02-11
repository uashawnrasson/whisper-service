FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip3 install -r requirements.txt

# Copy API service code
COPY app.py .

EXPOSE 5000

CMD ["python3", "app.py"]
