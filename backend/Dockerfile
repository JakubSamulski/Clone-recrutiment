# not for production use
FROM python:3.13
ARG host
ENV host=${host}
ARG port
ENV port=${port}
ARG log_level
ENV log_level=${log_level}
ARG refresh_rate
ENV refresh_rate=${refresh_rate}
RUN mkdir /app

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
EXPOSE 8000
RUN python manage.py migrate
# Run Django’s development server
CMD ["sh", "-c" ,"python manage.py run ${host} ${port} ${log_level} ${refresh_rate}"]