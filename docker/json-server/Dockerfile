FROM node:latest
MAINTAINER Vitaly Skopets <vitaly.skopets@itrexgroup.com>

RUN npm install -g json-server

WORKDIR /data
COPY ./tests/fixtures /data

EXPOSE 3000
