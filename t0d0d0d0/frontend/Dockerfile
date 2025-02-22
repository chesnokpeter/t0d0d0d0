FROM node:latest

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ../frontend .

RUN npm install && \
    npm run build

EXPOSE 8101

RUN useradd -m appuser
USER appuser

CMD ["node", "server.js"]