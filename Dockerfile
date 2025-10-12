FROM python:3.12.4

WORKDIR /sgrb

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
