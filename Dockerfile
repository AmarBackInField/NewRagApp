# Use Python 3.10 as base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OPENAI_API_KEY="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"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Set up volume for persistent data
VOLUME ["/app/data", "/app/logs"]



# Command to run the application
CMD ["streamlit", "run", "app.py"]
