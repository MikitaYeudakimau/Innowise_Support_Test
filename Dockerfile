FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src

CMD ["python", "./src/manage.py", "runserver", "0.0.0.0:8000"]