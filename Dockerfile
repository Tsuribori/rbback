FROM python:3.6.9-alpine3.10
ENV PYTHONBUFFERED=1

RUN mkdir -p /app/backend/

COPY requirements.txt /app/backend
RUN pip install -r /app/backend/requirements.txt

WORKDIR /app/backend

COPY . /app/backend

EXPOSE 8000

CMD ["gunicorn", "--chdir", "rbback", "--bind", ":8000", "--env", "DJANGO_SETTINGS_MODULE=rbback.prod_settings", "rbback.wsgi:application"]
