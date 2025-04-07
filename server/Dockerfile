FROM python:3.9-slim

WORKDIR /app

ADD e_store .

COPY requirment.txt .

COPY server.py .

RUN pip install -r requirment.txt


EXPOSE 8000

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000" ]