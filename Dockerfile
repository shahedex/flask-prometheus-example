FROM python:3.11-alpine

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
ENV FLASK_APP /app/server.py

EXPOSE 8000

CMD gunicorn --bind 0.0.0.0:8000 wsgi:api