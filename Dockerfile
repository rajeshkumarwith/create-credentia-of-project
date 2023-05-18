# FROM python:3.10.6-slim-buster
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt

# COPY . .
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]




FROM python:3.10.6-slim-buster


ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN groupadd -r doddle && useradd -r -g doddle doddle

RUN mkdir -p /code/media /code/static \
  && chown -R doddle:doddle /code/
  
COPY . /code




