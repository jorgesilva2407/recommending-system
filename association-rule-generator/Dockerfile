FROM python:3.9.21-alpine

WORKDIR /app

RUN pip install pandas
RUN pip install fpgrowth_py

COPY ./main.py /app/main.py

CMD ["python", "main.py"]
