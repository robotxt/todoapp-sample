FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r /code/requirements.txt

RUN pip3 install psycopg2-binary

