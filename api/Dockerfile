FROM python:3.9.21-alpine

WORKDIR /app

RUN pip install flask
RUN pip install fpgrowth_py

ENV PORT=5000
ENV MODEL_PATH=/app/model.pkl
EXPOSE ${PORT}

COPY ./model.py /app/model.py
COPY ./app.py /app/app.py

CMD ["python", "app.py"]
