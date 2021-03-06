# this is an official Python runtime, used as the parent image
FROM python:3.7-slim

RUN apt-get -y update
RUN apt-get -y install build-essential cmake libglib2.0 libsm6 libxrender1 libxext6 ttf-freefont

COPY requirements.txt requirements.txt
# execute everyone's favorite pip command, pip install -r
RUN pip install -r requirements.txt

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# unblock port 80 for the Bottle app to run on
EXPOSE 80

# execute the Bottle app
CMD python -m python.webserver