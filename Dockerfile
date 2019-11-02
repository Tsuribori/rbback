FROM python:3.6.9-alpine3.10
ENV PYTHONBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

RUN mkdir -p /app/backend/

COPY requirements.txt /app/backend
RUN pip install -r /app/backend/requirements.txt

WORKDIR /app/backend

COPY . /app/backend

EXPOSE 8000
RUN chmod +x entrypoint.sh

RUN adduser -D django
USER django

CMD ["./entrypoint.sh"]
