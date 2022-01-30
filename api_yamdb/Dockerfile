FROM python:3.7-slim

LABEL author='Godleib' version=1 broken_keyboards=5 pwd='/Users/mac/DEV/Yandex_prak/Production/Infrastructure (Docker)/Спринт_15/infra_sp2'

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]