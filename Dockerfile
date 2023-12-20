# Use the latest Ubuntu
FROM flask_app:latest

# Update the apt-get list and install necessary packages
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip postgresql-client

# Set the working directory
WORKDIR /flask_app

# Copy the project files
COPY . /flask_app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8080

# Command to run the application
CMD ["python3", "app.py"]
