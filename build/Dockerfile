FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# Installer les dépendances Python et le client MariaDB
RUN apt-get update && apt-get install -y mariadb-client \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
