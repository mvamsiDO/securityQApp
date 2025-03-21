FROM python:3.11-slim-buster

WORKDIR /app

COPY . ./app
COPY requirements.txt ./

RUN pip3 install -U pip && pip3 install -r requirements.txt

CMD ["streamlit", "run", "app/app.py"]