FROM python:3.8-slim-buster
WORKDIR /app
COPY ./src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src .

ENTRYPOINT [ "python3", "run.py" ]