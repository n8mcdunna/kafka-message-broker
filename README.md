# Real-Time Streaming Data Pipeline with Kafka and Docker

This project demonstrates a real-time data streaming pipeline built with Apache Kafka, Docker, and Python. It ingests streaming data from a Kafka topic, processes it in real-time, and outputs the aggregated data to a new Kafka topic.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Pipeline Services Functionality](#pipeline-services-functionality)
- [How to Run the Pipeline Locally](#how-to-run-the-pipeline-locally)
- [Set Up Needed for Production Use](#set-up-needed-for-production-use)
- [How to Deploy to Production](#how-to-deploy-to-production)
- [Scaling and Future Enhancements](#scaling-and-future-enhancements)

## Overview
The pipeline is designed to:
1. Ingest streaming data from a Kafka topic (`user-login`).
2. Perform real-time data processing, including filtering, transformation, and aggregation.
3. Publish the processed data to a new Kafka topic (`user-login-processed`).

## Project Structure
- **docker-compose.yml**: Defines services for Kafka, Zookeeper, a data generator (`my-python-producer`), and a data processor (`user-login-processor`) to be run in a Docker container.
- **Dockerfile**: Creates virtual environment necessary for running the project.
- **requirements.txt**: Defines packages and versions.
- **main.py**: Starting point for where the top-lovel code is executed for the Kafka `user-login` topic consumer and `user-login-processed` topic producer portion of the pipeline.
- **helpers.py**: Functions used to consume data from the `user-login` Kafka topic, process the data, and produce the streaming data to the `user-login-processed` topic.

## Requirements
- **Docker**: Ensure Docker is installed on your local machine.

## Pipeline Services Functionality
- There are four services that are created from the `docker-compose.yml`
1. **zookeeper**: a configuration management service that Kafka relies on for some of its fundamental operations.
2. **kafka**: the Kafka broker which manages storage, distribution, and retrieval of messages within topics.
3. **my-python-producer**: a data generator which produces data to a topic named `user-login` that simulates user login events
A sample message produced is:
```
{
    "user_id": "424cdd21-063a-43a7-b91b-7ca1a833afae",
    "app_version": "2.3.0",
    "device_type": "android",
    "ip": "199.172.111.135",
    "locale": "RU",
    "device_id": "593-47-5928",
    "timestamp": "1694479551"
  }
```
4. **user-login-processor**: a service that consumes messages from the `user-login` topic, performs data processing, and produces aggregated data to the `user-login-processed` topic. Below are the fields being produced.
    - timestamp_start: beginning of data aggregation interval
    - timestamp_end: end of data aggregation interval
    - interval_messages_consumed: total number of messages consumed and processed from the `user-login` topic within a defined interval
    - total_messages_consumed: number of messages consumed from the `user-login` topic since start up
    - interval_missing_field_count: keeps track of device type used for login since service started
    - interval_device_type_count: keeps track of device type used for login for defined interval
    - total_missing_field_count: keeps track of missing fields since service started
    - total_device_type_count: keeps track of device type used for login since service started

A sample message produced is:
```
{
    "timestamp_start": 1730392658, 
    "timestamp_end": 1730392668,
    "interval_messages_consumed": 20,
    "total_messages_consumed": 20,
    "interval_missing_field_count":{
        "device_type": 1
    }, 
    "interval_device_type_count": {
        "iOS": 12,
        "android": 7
    },
    "total_missing_field_count": {
        "device_type": 4
    }, 
    "total_device_type_count": {
        "iOS": 48,
        "android": 33
    }
}
```

## How to Run the Pipeline Locally
1. Start the pipeline ```docker-compose up --build```
2. Monitor the console output to see messages generated, consumed, and produced.

## Set Up Needed for Production Use
- Create development, staging, and production environments in cloud environment, for example AWS.
    - Create AWS ECR repository to store images and version tags with Terraform.
    - Set up AWS EC2 instances to use for scalable compute with Terraform.
    - Set up AWS tools needed for networking, load balancing, and security.
- Use Github Actions workflows to build Docker images and push those images to AWS ECR when a change happens to the codebase. 
- Set up Kubernetes on AWS EC2 instances to manage containers and scale application.
- Use [Helm chart](https://artifacthub.io/packages/helm/bitnami/kafka) to manage application components for easier installation and upgrades.  
- Set up [Flux](https://fluxcd.io/flux/) or similar tool to monitor AWS ECR repository for new images and tags created by GitHub Actions, update Helm chart, and automatically deploy code to respective cloud environment.
- Set up logging and alerting tool to monitor application, for example [Sentry](https://docs.sentry.io/).

## How to Deploy to Production
1. Create pull request from develop branch.
2. Test pull request locally, get pull request reviewed, and merge. This will trigger a Github Actions workflow which will automatically deploy the new code to the cloud development environment using Flux. 
3. Test changes in cloud development environment.
3. Create GitHub release with a version tag, which triggers the GitHub Action workflow to deploy to staging.
4. Tests begin running in staging; upon success, the workflow will automatically promote to production.

## Scaling and Future Enhancements
- Optimize Kafka configuration settings.
- Use partitions to handle higher message throughput which would allow multiple consumers to process messages in parallel.
- Add more transformations and aggregation metrics.
- Add logic for handling persistent and critical errors.
- Connect to a data warehouse for more analytical processing power. [Snowflake documentation on Kafka integration](https://docs.snowflake.com/en/user-guide/kafka-connector).
- Set up code linter for automatic standardization of code and improved code quality.