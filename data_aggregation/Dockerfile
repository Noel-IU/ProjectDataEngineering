# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8002 for the FastAPI service
EXPOSE 8002

# Run data_aggregation.py when the container launches
CMD ["uvicorn", "data_aggregation:app", "--host", "0.0.0.0", "--port", "8002"]
