FROM golang:1.22.2-alpine

WORKDIR /

COPY ./t0d0d0d0/sheduler/ .
RUN go mod download
RUN go build

ENV RABBIT_URL=""

CMD ["./sheduler"]


