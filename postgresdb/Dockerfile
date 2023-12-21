# Use the official PostgreSQL image as a base image
FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=flask_app
ENV POSTGRES_USER=thuannv
ENV POSTGRES_PASSWORD=06121998

# Update the apt-get list and install necessary packages
RUN apt-get update -y && \
    apt-get install -y nano iproute2

#Run container:
# docker run -d --name postgres-container -p 127.0.0.1:5434:5432 postgres:latest
# access to databse: psql -h localhost -p 5434 -U myuser -d mydatabase |  psql -h localhost -p 5432 -U thuannv -d flask_app
# psql -h 172.17.0.3 -U thuannv -d flask_app