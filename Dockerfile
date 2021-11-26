FROM python:3.8.10

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "uvicorn", "app.main:app", "0.0.0.0", "--port", "8000" ]