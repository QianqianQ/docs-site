FROM python:3.10

# set environment variables
# not to write cache files (.pyc), which are Python bytecode files, usually stored in the __pycache__ folder
ENV PYTHONDONTWRITEBYTECODE 1
# show you any output straight to your terminal
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

# install dependencies
RUN pip3 install --upgrade pip
RUN apt-get update
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .
# RUN chmod +x ./docker-entrypoint.sh

# port where the Django app runs
EXPOSE 8000

# ENTRYPOINT ["bash", "./docker-entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
