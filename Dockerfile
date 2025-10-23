# Use official Python image
FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENV FLASK_APP=app_main.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "app_main.py"]
