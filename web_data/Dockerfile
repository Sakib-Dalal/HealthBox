# Use the official Ubuntu image from the Docker Hub
FROM ubuntu:20.04

# Set environment variables to avoid user input during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv build-essential libssl-dev libffi-dev python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python3", "main.py"]