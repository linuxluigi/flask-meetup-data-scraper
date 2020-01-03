FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # build dependencies
  && apk add --no-cache gcc musl-dev linux-headers \
  # git
  && apk add git \
  # make for docs creation
  && apk add make

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
