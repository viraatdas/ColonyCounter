FROM python:3.9-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx libsm6 libxrender1 libfontconfig1 libice6 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["gunicorn", "app:app"]
