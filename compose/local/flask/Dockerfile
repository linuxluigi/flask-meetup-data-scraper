FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

# find new packges use latest branch (not edge!) -> https://pkgs.alpinelinux.org/packages
RUN apk add --no-cache gcc=9.2.0-r3 musl-dev=1.1.24-r0 linux-headers=4.19.36-r0 \
  # build dependencies
  && apk add --no-cache git=2.24.1-r0 \
  # git
  && apk add --no-cache make=4.2.1-r2
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
