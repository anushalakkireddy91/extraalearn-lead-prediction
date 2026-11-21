FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Streamlit on port 8501 (exposed from the container in the Codespace)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
