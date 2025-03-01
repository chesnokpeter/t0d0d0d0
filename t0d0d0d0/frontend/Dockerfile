FROM node:20-alpine as builder

WORKDIR /app

COPY ./t0d0d0d0/frontend/package*.json .

RUN npm ci --force

COPY ./t0d0d0d0/frontend .

RUN npm run build

FROM gcr.io/distroless/nodejs20-debian12

WORKDIR /app

COPY --from=builder /app/dist ./app
COPY --from=builder /app/node_modules ./app/node_modules
COPY --from=builder /app/server.js ./app

EXPOSE 8101

CMD ["app/server.js"]