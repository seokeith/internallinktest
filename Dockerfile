# Start from a base image
FROM python:3.8-slim-buster

# Set a working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set the command to be run when the container starts
CMD ["python", "your_script.py"]
