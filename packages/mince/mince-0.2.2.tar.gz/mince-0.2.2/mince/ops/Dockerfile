
# Use official Python image as the base image
FROM python:3.11-slim-bookworm

# Set build arguments
ARG DASHBOARD_PACKAGE
ARG REGISTER_PACKAGE=${DASHBOARD_PACKAGE}

# Set the working directory in the container
WORKDIR /app

# Copy the entire current directory to /app/package
COPY . /app/package

# Install system dependencies and pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install mince
RUN pip install --no-cache-dir mince

# Change to the package directory and install the local package
WORKDIR /app/package
RUN pip install --no-cache-dir .

# Change back to the app directory
WORKDIR /app

# Run the mince register command
RUN python -m mince register ${REGISTER_PACKAGE}

# Set the command to run mince with the dashboard package
CMD ["sh", "-c", "mince run ${DASHBOARD_PACKAGE}"]
