FROM python:3.8

ADD main.py .

RUN pip install websocket-client streamlit pandas mplfinance matplotlib configparser

CMD ["python", "./main.py"]
