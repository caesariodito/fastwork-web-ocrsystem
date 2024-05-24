# app/Dockerfile

FROM python:3.10.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN git clone --single-branch --branch local-dockerized https://github.com/caesariodito/fastwork-web-ocrsystem.git .

EXPOSE 8501
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=127.0.0.1"]