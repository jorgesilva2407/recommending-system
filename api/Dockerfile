FROM python:3.9.21-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 5000 

COPY ./model.py /app/model.py
COPY ./app.py /app/app.py

CMD ["python", "app.py"]
