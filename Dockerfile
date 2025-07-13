FROM typesense/typesense:29.0
USER root

# install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# copy files
COPY . /
RUN chmod +x /docker-entrypoint.sh

# entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]