from fastapi import FastAPI, HTTPException
import requests
import pandas as pd
import numpy as np
from influxdb_client import InfluxDBClient, Point, WriteOptions
import os

app = FastAPI()

# Our InfluxDB setup using environment variables
bucket = os.getenv("INFLUXDB_BUCKET", "mybucket")
org = os.getenv("INFLUXDB_ORG", "myorg")
token = os.getenv("INFLUXDB_TOKEN")
url = os.getenv("INFLUXDB_URL", "http://influxdb:8086")

# This is a check to see if the authentication token is present
if not token:
    raise ValueError("INFLUXDB_TOKEN environment variable is not set")

# We then initialize InfluxDB Client
client = InfluxDBClient(url=url, token=token, org=org)

# Write API with customized options to control batching, timing and retry behaviour when sending data points to the database
write_options = WriteOptions(batch_size=5000, flush_interval=1000)
write_api = client.write_api(write_options=write_options)

# Function to clean the data by replacing NaN, Infinity, -Infinity with None
def clean_data(dataframe):
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    return dataframe.applymap(lambda x: None if pd.isna(x) else x)

# Function to send preprocessed data to InfluxDB
def send_to_influxdb(data, measurement_name):
    for index, row in data.iterrows():
        point = Point(measurement_name)\
            .tag("VendorID", row.get("VendorID", "unknown"))\
            .field("trip_distance", row.get("trip_distance", 0))\
            .field("tip_amount", row.get("tip_amount", 0))\
            .field("total_amount", row.get("total_amount", 0))\
            .time(pd.Timestamp.now())
        try:
            write_api.write(bucket=bucket, org=org, record=point)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error writing to InfluxDB: {str(e)}")

# Preprocessing: Drop 'RatecodeID' and 'store_and_fwd_flag' columns for data1
@app.get("/preprocessed_data1")
def preprocess_data1():
    try:
        # Fetch data from the ingestion service
        response = requests.get('http://data_ingestion:8000/data1')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data1 = pd.DataFrame(response.json())

        # Drop 'RatecodeID' and 'store_and_fwd_flag' columns
        data1_preprocessed = data1.drop(columns=['RatecodeID', 'store_and_fwd_flag'])

        # Clean data
        data1_cleaned = clean_data(data1_preprocessed)

        # Send preprocessed data to InfluxDB
        send_to_influxdb(data1_cleaned, "log1_data_preprocessing")

        return data1_cleaned.to_dict(orient="records")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

# Preprocessing: Drop 'RatecodeID' and 'store_and_fwd_flag' columns for data2
@app.get("/preprocessed_data2")
def preprocess_data2():
    try:
        # Fetch data from the ingestion service
        response = requests.get('http://data_ingestion:8000/data2')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data2 = pd.DataFrame(response.json())

        # Drop 'RatecodeID' and 'store_and_fwd_flag' columns
        data2_preprocessed = data2.drop(columns=['RatecodeID', 'store_and_fwd_flag'])

        # Clean data
        data2_cleaned = clean_data(data2_preprocessed)

        # Send preprocessed data to InfluxDB
        send_to_influxdb(data2_cleaned, "log2_data_preprocessing")

        return data2_cleaned.to_dict(orient="records")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
