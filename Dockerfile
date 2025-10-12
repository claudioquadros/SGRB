FROM python:3.11

WORKDIR /sgrb

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBRUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
