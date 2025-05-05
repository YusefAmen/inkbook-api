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

# Accept build args
ARG SUPABASE_URL
ARG SUPABASE_SERVICE_ROLE_KEY
ARG SUPABASE_ANON_KEY
ARG DATABASE_URL
ARG ENVIRONMENT=development

# Set environment variables
ENV SUPABASE_URL=$SUPABASE_URL
ENV SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY
ENV SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
ENV DATABASE_URL=$DATABASE_URL
ENV ENVIRONMENT=$ENVIRONMENT
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run with hot reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"] 