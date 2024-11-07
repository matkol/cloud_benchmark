FROM python:3.13.0-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app app

ENV FLASK_APP=app
EXPOSE 5000
CMD [ "flask", "--app", "app/api.py", "run", "--host=0.0.0.0"]
