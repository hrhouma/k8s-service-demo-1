FROM python:3.10-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Installer les dépendances Python et le client MySQL
RUN apt-get update && apt-get install -y default-mysql-client \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]
