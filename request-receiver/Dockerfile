FROM python:3.8.1-slim
RUN apt-get update && apt-get -y install netcat
WORKDIR /usr/request-receiver
COPY . .
RUN chmod +x ./docker_entrypoint.sh
RUN useradd -ms /bin/bash request-receiver
USER request-receiver
ENV PATH $PATH:/home/request-receiver/.local/bin
RUN pip install --no-cache-dir --disable-pip-version-check --user -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["./docker_entrypoint.sh"]
