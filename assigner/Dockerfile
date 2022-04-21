FROM python:3.8.1-slim
RUN apt-get update && apt-get -y install netcat
WORKDIR /usr/assigner
COPY . .
RUN chmod +x ./docker_entrypoint.sh
RUN useradd -ms /bin/bash assigner
USER assigner
ENV PATH $PATH:/home/assigner/.local/bin
RUN pip install --no-cache-dir --disable-pip-version-check --user -r requirements.txt
ENTRYPOINT ["./docker_entrypoint.sh"]
