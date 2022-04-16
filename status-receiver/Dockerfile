FROM python:3.8.1-slim
RUN apt-get update && apt-get -y install netcat
WORKDIR /usr/status-receiver
COPY . .
RUN chmod +x ./docker_entrypoint.sh
RUN useradd -ms /bin/bash status-receiver
USER status-receiver
ENV PATH $PATH:/home/status-receiver/.local/bin
RUN pip install --no-cache-dir --disable-pip-version-check --user -r requirements.txt
EXPOSE 8081
ENTRYPOINT ["./docker_entrypoint.sh"]
