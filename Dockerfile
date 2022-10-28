FROM python:3.10.7

ENV FLASK_APP=serverlabs

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY sererlabs /opt/serverlabs

WORKDIR /opt

CMD flask --app serverlabsrun --host 0.0.0.0 -p $PORT