# frontend builder
FROM node:lts-alpine AS builder

RUN mkdir -p /app/frontend
WORKDIR /app/frontend

COPY frontend/package*.json /app/frontend/
RUN npm install

COPY frontend /app/frontend/
RUN npm run build


# final
FROM python:3.13-slim-bookworm

RUN mkdir -p /opt/pecoret
# only copy server code because we already build frontend
COPY server /opt/pecoret
WORKDIR /opt/pecoret

RUN apt update && apt install -y fonts-font-awesome libldap2-dev libsasl2-dev gcc libffi-dev\
    libcairo-gobject2 libpango-1.0-0 libpangoft2-1.0-0 git nginx

RUN pip install -r requirements.txt && \
    pip install gunicorn && \
    rm /etc/nginx/sites-enabled/default*


# fetch frontend from builder
COPY --from=builder /app/server/static/dist ./static/dist/

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
