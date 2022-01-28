FROM python:3.10-buster


RUN mkdir -p /app
COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r /app/requirements.txt

COPY app/ /app/
WORKDIR /app/
ENV containterized=true

CMD ["python3", "server.py"]
