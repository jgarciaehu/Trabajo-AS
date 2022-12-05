FROM python:3.11-alpine

WORKDIR /files

COPY index.html /files/export-orientdb/

COPY requirements.txt /files/

RUN pip install -r requirements.txt

COPY app.py /files/

CMD python app.py
