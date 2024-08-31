# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages (if you had a requirements.txt)
# RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script with the "build" argument when the container launches
CMD ["python3", "pipeline_calls.py", "build"]

