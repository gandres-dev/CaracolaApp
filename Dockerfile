FROM deepnote/python:3.7
RUN apt-get update && apt-get install -y software-properties-common \
    && apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main' \
    && apt-get update && apt-get install -y build-essential wget ffmpeg