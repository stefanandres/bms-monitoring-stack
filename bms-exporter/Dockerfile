FROM python:3.7-alpine

COPY ./setup.py /app/
COPY ./bms_exporter /app/bms_exporter/

WORKDIR /app
RUN pip install .

EXPOSE 8000
ENTRYPOINT ["bms-exporter"]

