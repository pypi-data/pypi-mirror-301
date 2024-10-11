# Use ubuntu/python as the base image
FROM ubuntu/python:latest

# Set build arguments
ARG PACKAGE

# Set the working directory in the container
WORKDIR /app

# Copy the entire current directory to /app/package
COPY . /app/package

# Install pip and update it
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# Install mince
RUN pip3 install mince

# Change to the package directory and install the local package
WORKDIR /app/package
RUN pip3 install .

# Change back to the app directory
WORKDIR /app

# Run the mince register command
RUN python3 -m mince register ${PACKAGE}

# Set the command to run mince with the dashboard package
CMD ["sh", "-c", "mince run ${PACKAGE}"]
