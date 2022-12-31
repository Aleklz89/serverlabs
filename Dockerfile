FROM python:3.10.7

ENV FLASK_APP=serverlabs
ENV FLAK_DEBUG=$FLAK_DEBUG

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY serverlabs /opt/serverlabs

WORKDIR /opt

CMD flask --app serverlabs run --host 0.0.0.0 -p $PORT