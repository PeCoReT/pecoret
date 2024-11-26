FROM node:lts-alpine as builder

RUN mkdir /app
WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY . /app/

RUN npm run build

FROM nginx:mainline-alpine

# add init script
COPY ./docker/nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html

COPY --from=builder /app/dist/ .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]