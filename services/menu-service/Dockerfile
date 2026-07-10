# Use the official slim Python 3.13 image as the base
# "slim" keeps the image smaller by excluding unnecessary packages
FROM python:3.13-slim

# Set the working directory inside the container for all subsequent commands
WORKDIR /app

# Copy only the requirements file first (before the rest of the code)
# This lets Docker cache the pip install layer, so it's skipped on rebuilds
# unless requirements.txt actually changes
COPY requirements.txt .

# Install Python dependencies listed in requirements.txt
# --no-cache-dir avoids storing the pip cache, keeping the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Document that the container listens on port 8000
# (this is informational only — it doesn't actually publish the port)
EXPOSE 8000

# Start the FastAPI app using uvicorn
# --host 0.0.0.0 makes it accessible from outside the container
# --port 8000 matches the EXPOSE above
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]