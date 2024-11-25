# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install git for submodule
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY src/requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code including the .git directory for submodules
COPY . .

# Initialize and update submodules
RUN git submodule update --init --recursive

# Create archives directory
RUN mkdir -p archives

# Make sure we're in the src directory for gunicorn
WORKDIR /app/src

# Expose the port the app will run on
EXPOSE 8888


# Run the Gunicorn server from the src directory
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8888", "main:app"]