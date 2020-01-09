FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # build dependencies
  && apk add --no-cache gcc musl-dev linux-headers \
  # git
  && apk add git \
  # make for docs creation
  && apk add make

RUN addgroup -S flask \
    && adduser -S -G flask flask

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/production/flask/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown flask /entrypoint

COPY ./compose/production/flask/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown flask /start

COPY . /app
RUN chown -R flask /app

USER flask

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
