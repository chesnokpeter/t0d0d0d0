FROM nginx:latest

RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean

COPY nginx.conf /etc/nginx/nginx.conf

COPY init-letsencrypt.sh /scripts/init-letsencrypt.sh
RUN chmod +x /scripts/init-letsencrypt.sh

EXPOSE 80
EXPOSE 443

CMD /scripts/init-letsencrypt.sh && nginx -g 'daemon off;'