FROM python:3.9.6-slim-buster


WORKDIR /app
ADD . .


RUN pip install watchmen-ml-python-sdk && pip install webencodings
RUN pip install poetry && poetry config virtualenvs.create false && poetry update && poetry install --no-dev



EXPOSE 5000
CMD ["uvicorn","connect_server.main:app","--host", "0.0.0.0", "--port", "5000"]

