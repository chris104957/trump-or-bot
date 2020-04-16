FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 9090
CMD python manage.py migrate && python manage.py populate && python manage.py runserver 0.0.0.0:9090
