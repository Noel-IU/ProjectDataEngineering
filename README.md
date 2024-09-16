# Data Engineering Project Information
Author Noel Tetteh
Date 16th September 2024
The aim of this portfolio is to design and build a real-time data backend infrastructure capable of continuously ingesting, preprocessing, and aggregating large amounts of data for usage in streaming reports.
The dataset is from taxi trip records (over 1 million data points), and contains pick-up and drop-off dates/times, pick-up and drop-off locations, trip distances, itemized fares, rate types, payment types, and driver-reported passenger counts.
This system processes and analyzes CSV data from two taxi companies (identified by VendorID). The data, including trip distances, pick-up/drop-off times, fares, and payment types, is ingested from 2 CSV files using pandas. 
A FastAPI service mimics real-time data streaming by exposing endpoints for ingesting and processing the data. 
The data is preprocessed to remove unnecessary fields and aggregated to calculate total trip distances, fares, and tips for each company. 
This aggregated data is then sent to InfluxDB, a time-series database, and visualized in Grafana for real-time monitoring. 
Kafka handles the data streaming, while Docker manages the various services.
