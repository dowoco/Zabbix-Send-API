# Using lightweight alpine image
FROM python:3.9.2-alpine

# Installing packages
RUN apk update
COPY requirements.txt /
RUN pip install --no-cache-dir --upgrade  -r /requirements.txt


# Defining working directory and adding source code
COPY . /app
WORKDIR /app


# Start app
ENTRYPOINT ["./bootstrap.sh"]
#!/bin/sh

#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
