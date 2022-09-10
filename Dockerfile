FROM python:3.10.6-buster

RUN ["mkdir", "/app"]
COPY requirement.txt /app/
RUN ["pip", "install", "-r", "/app/requirement.txt"]

COPY dbt/ /app/dbt/
COPY tests/ /app/tests/
WORKDIR /app

ENTRYPOINT ["pytest"]