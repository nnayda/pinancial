FROM python:3.6-slim
WORKDIR /src
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install gcc
RUN pip3 install pip --upgrade && \
	pip3 install -r requirements.txt
ENTRYPOINT ["./python-linter/entrypoint.sh"]