FROM python:3.9.21-alpine

WORKDIR /app

RUN pip install flask
RUN pip install fpgrowth_py

ENV MODEL_PATH=/app/model.pkl
EXPOSE 5000 

COPY ./model.py /app/model.py
COPY ./app.py /app/app.py

CMD ["python", "app.py"]
