FROM ubuntu:latest
LABEL authors="mobin"

ENTRYPOINT ["top", "-b"]