from fastapi import FastAPI, HTTPException
import pandas as pd
import os
import numpy as np

app = FastAPI()

# This is the Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Ingestion API"}

# Here we define the file paths relative to the container's /app directory
data1_path = '/app/data/Log_1.csv'
data2_path = '/app/data/Log_2.csv'

# Load the CSV files
try:
    data1 = pd.read_csv(data1_path)
    data1 = data1.replace({np.nan: None, np.inf: None, -np.inf: None})
except FileNotFoundError:
    data1 = pd.DataFrame()  # Create an empty DataFrame as fallback if the file is not found

try:
    data2 = pd.read_csv(data2_path)
    data2 = data2.replace({np.nan: None, np.inf: None, -np.inf: None})
except FileNotFoundError:
    data2 = pd.DataFrame()  # Create an empty DataFrame as fallback if the file is not found

# This is the endpoint to fetch data from the first CSV file
@app.get("/data1")
def get_data1():
    if data1.empty:
        return {"error": "Log_1.csv not found or empty."}
    return data1.to_dict(orient="records")

# This is the endpoint to fetch data from the second CSV file
@app.get("/data2")
def get_data2():
    if data2.empty:
        return {"error": "Log_2.csv not found or empty."}
    return data2.to_dict(orient="records")
