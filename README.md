# Data Engineering Project Information
Author Noel Tetteh
Date 16th September 2024

## Project Overview

The aim of this portfolio is to design and build a real-time data backend infrastructure capable of continuously ingesting, preprocessing, and aggregating large amounts of data for usage in streaming reports.
The dataset is from taxi trip records (over 1 million data points), and contains pick-up and drop-off dates/times, pick-up and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts.
This system processes and analyzes CSV data from two taxi companies (identified by VendorID). The data, including trip distances, pick-up/drop-off times, fares, and payment types, is ingested from 2 CSV files using pandas. 
A FastAPI service mimics real-time data streaming by exposing endpoints for ingesting and processing the data. 
The data is preprocessed to remove unnecessary fields and aggregated to calculate total trip distances, fares, and tips for each company. This aggregated data is then sent to InfluxDB, a time-series database, and visualized in Grafana for real-time monitoring. Kafka handles the data streaming, while Docker manages the various services.


## Folder Structure
```
DataEngineeringProject
├── Architecture Overview/   # Contains high-level and detailed level overview of the project
├── data_aggregation/        # Microservice for aggregating taxi data
├── data_ingestion/          # Microservice for ingesting CSV files
├── data_preprocessing/      # Microservice for preprocessing the ingested data
├── FastAPI/                 # FastAPI service to simulate real-time data streaming
├── grafana_data/            # Persistent storage for Grafana
├── influxdb_data/           # Persistent storage for InfluxDB
├── docker-compose.yml       # Docker configuration to manage services
├── .gitignore               # Files and directories to ignore in version control
└── README.md                # Project overview and instructions
```

## Installation and Usage Instructions
```
1. Clone the Repository:
    git clone https://github.com/Noel-IU/ProjectDataEngineering.git
    cd ProjectDataEngineering

2. Ensure you have the prerequisites installed:
    Docker
    Docker Compose
    Python 3.x (x refers to your Python version)
    FastAPI
    InfluxDB
    Grafana

3. Start Docker Services:
    Run: docker-compose up --build

4. Access the Services:
    FastAPI:
    Ingestion: http://localhost:8000
    Preprocessing: http://localhost:8001
    Aggregation: http://localhost:8002
    Grafana: http://localhost:3000 (default: admin:admin123)
    InfluxDB: http://localhost:8086
    Kafka: Broker at localhost:9092

5. Usage Instructions
    Ingest Data:
    Use /ingest endpoint: curl -X POST http://localhost:8000/ingest

    Preprocess Data:    
    Access /preprocessed_data1: curl http://localhost:8001/preprocessed_data1
    Access /preprocessed_data2: curl http://localhost:8001/preprocessed_data2

    View Aggregated Data:    
    Access /aggregated_data: curl http://localhost:8002/aggregated_data

    Visualize Data in Grafana:
    Set up InfluxDB as a data source and create dashboards.




