# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the Python script into the container at /app
COPY server.py .
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests schedule

# Command to run the fetch_data script
CMD ["python", "server.py"]
