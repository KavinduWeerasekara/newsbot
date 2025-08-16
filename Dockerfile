# Dockerfile

# 1. Start with an official, lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy just the requirements file first to leverage Docker caching
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. The command to run when the container starts
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]