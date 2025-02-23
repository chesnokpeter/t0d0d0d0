FROM node:latest

RUN apt-get update && apt-get install -y --no-install-recommends && \
    apt-get clean

COPY ./t0d0d0d0/frontend .

RUN npm install --force && \
    npm run build

EXPOSE 8101

RUN useradd -m appuser
USER appuser

CMD ["node", "server.js"]