FROM golang:1.20-alpine

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean


COPY ../sheduler/ .
RUN go mod download
RUN go build

ENV RABBIT_URL=""

CMD ["./sheduler"]


