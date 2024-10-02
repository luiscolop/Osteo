FROM python:3.12.5-alpine3.20

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

RUN apk update

RUN apk add pkgconfig

RUN apk add weasyprint

RUN apk add fontconfig ttf-freefont font-noto terminus-font

RUN fc-cache -f

RUN fc-list | sort

RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN pip install gunicorn

COPY . .