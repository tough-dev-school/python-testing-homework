FROM node:latest

RUN npm install -g json-server

WORKDIR /data
COPY ./db /data

VOLUME /data

EXPOSE 3000