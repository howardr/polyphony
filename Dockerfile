# Use Python 3.10 slim image
FROM python:3.10-slim

# Install tzdata package and curl for healthcheck
RUN apt-get update && apt-get install -y tzdata curl

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install yfinance --upgrade --no-cache-dir
RUN pip install gunicorn  # Explicitly install gunicorn

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PROD=true
ENV TZ=UTC

# The TIINGO_API_KEY will be injected at runtime, so we don't set it here

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ping || exit 1

# Run the application with adjusted gunicorn settings
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "1", \
     "--threads", "8", \
     "--timeout", "0", \
     "server:app"]