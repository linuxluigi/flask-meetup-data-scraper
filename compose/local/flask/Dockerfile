FROM python:3.8.7-alpine3.11

ENV PYTHONUNBUFFERED 1

# find new packges use latest branch (not edge!) -> https://pkgs.alpinelinux.org/packages
RUN apk add --no-cache gcc musl-dev linux-headers \
  # build dependencies
  && apk add --no-cache git \
  # git
  && apk add --no-cache make
  # make for docs creation

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
