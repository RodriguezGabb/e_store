FROM python:3.9-slim

WORKDIR /app

COPY e_store/ /app

COPY requirment.txt .

RUN pip install -r requirment.txt

COPY e_store/server.py .

EXPOSE 8000

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000" ]