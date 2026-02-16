# Python 3.11 base image
FROM python:3.11-slim

# Werkdirectory
WORKDIR /app

# Installeer system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Kopieer requirements
COPY requirements.txt .

# Installeer Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer applicatie code
COPY . .

# Expose port
EXPOSE 10000

# Start commando
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
