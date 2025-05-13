# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p logs data/raw data/processed

# Set environment variables
ENV PYTHONPATH=/app

# Run the scheduler with Python's unbuffered output
CMD ["python", "-u", "-m", "src.scheduler"] 