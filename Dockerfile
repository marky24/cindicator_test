FROM python:3.8

ADD src/main.py .

COPY requirements.txt /tmp/
WORKDIR /tmp
RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]
