FROM python:3.12.2-bullseye

LABEL description="Health Monitor"


WORKDIR /usr/echipa2
COPY . .


RUN set -ex && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD flask run --host=0.0.0.0 --port=8000
