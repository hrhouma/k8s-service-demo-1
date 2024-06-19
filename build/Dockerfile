FROM python:3.10-slim

RUN pip install flask redis mysqlclient

COPY . /app
WORKDIR /app

EXPOSE 5000

CMD ["python", "app.py"]
