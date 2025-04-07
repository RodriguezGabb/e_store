FROM python:3.9-slim

WORKDIR /app

COPY main.py .

COPY templates .

COPY requirment.txt .

RUN pip install -r requirment.txt


EXPOSE 8001

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001" ]