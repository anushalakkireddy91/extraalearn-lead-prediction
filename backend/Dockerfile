FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . .

# Install dependencies from the requirements file without using cache to reduce image size
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Start the Flask app on port 7860 using gunicorn
# (app:app means: file app.py, Flask object named app)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "app:app"]
