FROM python:3.13.5-alpine3.21

WORKDIR /app    

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]