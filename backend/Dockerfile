FROM python:3.13-alpine

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
ENV CONTAINER_ENV=true

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["python", "app.py"]
