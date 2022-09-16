FROM python:3.9.6-slim-buster


WORKDIR   /opt/
RUN    apt-get update && apt-get install -y curl && apt-get install -y gnupg2 gcc g++

WORKDIR /app
ADD . .


RUN pip install watchmen-ml-python-sdk && pip install webencodings
RUN pip install poetry && poetry config virtualenvs.create false && poetry update && poetry install --no-dev



EXPOSE 5000
CMD ["uvicorn","connect_server.main:app","--host", "0.0.0.0", "--port", "5000"]

