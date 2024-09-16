# Dockerize python
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI service 
EXPOSE 8000

# Run data_ingestion.py when the container launches
CMD ["uvicorn", "data_ingestion:app", "--host", "0.0.0.0", "--port", "8000"]
