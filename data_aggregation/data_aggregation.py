from fastapi import FastAPI, HTTPException
import requests
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
import os

app = FastAPI()

# Our InfluxDB setup
bucket = os.getenv("INFLUXDB_BUCKET", "mybucket")
org = os.getenv("INFLUXDB_ORG", "myorg")
token = os.getenv("INFLUXDB_TOKEN", "NzWGBzpmcDSyIHFT1Ek9Nct1xMkrS2RCkGVxiPL8m54WMh3DdxV5NMxqq2fsscorCGJ2BFgwFPEWEdx6KIYEkg==")
url = os.getenv("INFLUXDB_URL", "http://influxdb:8086")

client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=WriteOptions(
    batch_size=1000,
    flush_interval=10_000,
    jitter_interval=2_000,
    retry_interval=5_000
))

# Function to send aggregated data to InfluxDB
def send_aggregated_to_influxdb(vendor_totals, measurement_name):
    try:
        point = Point(measurement_name)\
            .tag("VendorID", vendor_totals["VendorID"])\
            .field("total_trip_distance", vendor_totals["total_trip_distance"])\
            .field("total_tip_amount", vendor_totals["total_tip_amount"])\
            .field("total_total_amount", vendor_totals["total_total_amount"])\
            .time(pd.Timestamp.now())
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")
        raise HTTPException(status_code=500, detail=f"Error writing to InfluxDB: {e}")

# Aggregate the two dataframes (or the 2 preprocessed csv files)
@app.get("/aggregated_data")
def aggregate_data():
    try:
        # Fetch preprocessed data from the preprocessing service
        data1_response = requests.get('http://data_preprocessing_service:8001/preprocessed_data1')
        data2_response = requests.get('http://data_preprocessing_service:8001/preprocessed_data2')
        
        data1_response.raise_for_status()
        data2_response.raise_for_status()

        data1_preprocessed = pd.DataFrame(data1_response.json())
        data2_preprocessed = pd.DataFrame(data2_response.json())

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Unable to connect to data preprocessing service")
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response data from preprocessing service")
    
    if data1_preprocessed.empty or data2_preprocessed.empty:
        raise HTTPException(status_code=500, detail="Preprocessed data is empty")

    aggregated_data = pd.concat([data1_preprocessed, data2_preprocessed])

    # Filter and aggregate based on VendorID
    vendor1_data = aggregated_data[aggregated_data['VendorID'] == 1]
    vendor2_data = aggregated_data[aggregated_data['VendorID'] == 2]

    # Calculate totals for each VendorID
    vendor1_totals = {
        "VendorID": 1,
        "total_trip_distance": vendor1_data['trip_distance'].sum(),
        "total_tip_amount": vendor1_data['tip_amount'].sum(),
        "total_total_amount": vendor1_data['total_amount'].sum()
    }

    vendor2_totals = {
        "VendorID": 2,
        "total_trip_distance": vendor2_data['trip_distance'].sum(),
        "total_tip_amount": vendor2_data['tip_amount'].sum(),
        "total_total_amount": vendor2_data['total_amount'].sum()
    }

    # Return the results for both VendorID 1 and VendorID 2 before sending to InfluxDB
    results = [vendor1_totals, vendor2_totals]

    # Finally we send our aggregated data to InfluxDB 
    try:
        send_aggregated_to_influxdb(vendor1_totals, "vendor1_aggregation")
        send_aggregated_to_influxdb(vendor2_totals, "vendor2_aggregation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending data to InfluxDB: {str(e)}")

    return results
