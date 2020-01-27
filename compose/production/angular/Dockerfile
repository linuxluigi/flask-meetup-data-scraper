# stage1 as builder
FROM node:12-alpine as builder

# install git
RUN apk add --no-cache git

# dowload frontend
RUN git clone https://github.com/linuxluigi/meetup-data-scraper-angular.git /app

# set workdir path to angular app
WORKDIR /app

# install dependencies
RUN npm install -g @angular/cli@8.3.23
RUN npm install

# Install the dependencies and make the folder
RUN npm install

# Build the project
RUN npm run ng build -- --prod


FROM nginx:1.17.8-alpine

COPY ./compose/production/angular/nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stahg 1
COPY --from=builder /app/dist/meetup-data-scraper-angular /usr/share/nginx/html

EXPOSE 4200 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]