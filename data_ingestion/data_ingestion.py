from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
import os

app = FastAPI()

# First we initialize the InfluxDB client with environment variables
url = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
token = os.getenv("INFLUXDB_TOKEN", "NzWGBzpmcDSyIHFT1Ek9Nct1xMkrS2RCkGVxiPL8m54WMh3DdxV5NMxqq2fsscorCGJ2BFgwFPEWEdx6KIYEkg==")
org = os.getenv("INFLUXDB_ORG", "myorg")
bucket = os.getenv("INFLUXDB_BUCKET", "mybucket")

client = InfluxDBClient(url=url, token=token, org=org)

# We need to initialize the Write API with WriteOptions to control the batching, timing, and retry behaviour when sending data points to the database.
write_api = client.write_api(write_options=WriteOptions(
    batch_size=1000,
    flush_interval=10000,
    jitter_interval=2000,
    retry_interval=5000
))

# Define the file paths relative to the container's /app directory
@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Ingestion API"}

data1_path = '/app/data/Log_1.csv'
data2_path = '/app/data/Log_2.csv'

# Load the CSV files
try:
    data1 = pd.read_csv(data1_path)
    data1 = data1.replace({np.nan: None, np.inf: None, -np.inf: None})
except FileNotFoundError:
    data1 = pd.DataFrame()

try:
    data2 = pd.read_csv(data2_path)
    data2 = data2.replace({np.nan: None, np.inf: None, -np.inf: None})
except FileNotFoundError:
    data2 = pd.DataFrame()

# Function to send data to InfluxDB
def send_to_influxdb(data, measurement_name):
    for index, row in data.iterrows():
        point = Point(measurement_name)\
            .tag("VendorID", row.get("VendorID", "unknown"))\
            .field("trip_distance", row.get("trip_distance", 0))\
            .field("tip_amount", row.get("tip_amount", 0))\
            .time(pd.Timestamp.now())
        write_api.write(bucket=bucket, record=point)

# Endpoint to fetch data from the first CSV file and send to InfluxDB
@app.get("/data1")
def get_data1():
    if data1.empty:
        return {"error": "Log_1.csv not found or empty."}

    # Send data to InfluxDB
    send_to_influxdb(data1, "log1_data_ingestion")

    return data1.to_dict(orient="records")

# Endpoint to fetch data from the second CSV file and send to InfluxDB
@app.get("/data2")
def get_data2():
    if data2.empty:
        return {"error": "Log_2.csv not found or empty."}

    # Send data to InfluxDB
    send_to_influxdb(data2, "log2_data_ingestion")

    return data2.to_dict(orient="records")
