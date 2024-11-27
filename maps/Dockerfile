FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GOOGLE_MAPS_API_KEY=AIzaSyDMmHRrGdL0CHeikcNfrG4M8HLC32slJ6E
ENV FLASK_APP=maps.py
ENV PROJECT_ID=hcls-jp1
EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
