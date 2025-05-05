# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables (override with docker-compose or CLI)
ENV PYTHONUNBUFFERED=1

# Run with hot reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"] 