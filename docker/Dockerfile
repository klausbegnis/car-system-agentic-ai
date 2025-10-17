FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Expose port
EXPOSE 8083

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8083

# Run the application
CMD ["uv", "run", "main.py"]
