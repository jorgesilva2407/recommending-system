FROM python:3.9.21-alpine

ENV VERSION v1.0.4

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./model.py /app/model.py
COPY ./main.py /app/main.py

CMD ["python", "main.py"]
