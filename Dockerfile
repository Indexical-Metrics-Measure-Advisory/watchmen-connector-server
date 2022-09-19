FROM python:3.9.6-slim-buster


WORKDIR  /opt/

RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    make \
    wget \
    libatlas-base-dev \
    libffi-dev




WORKDIR /app
ADD . .

RUN pip install webencodings  \
    && pip install watchmen-ml-python-sdk  \
    && pip install poetry  && poetry config virtualenvs.create false && poetry update  \
RUN poetry install --no-dev
RUN pip install "uvicorn[standard]"




EXPOSE 5000
CMD ["uvicorn","connect_server.main:app","--host", "0.0.0.0", "--port", "5000"]

