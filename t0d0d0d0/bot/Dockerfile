FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./t0d0d0d0/bot/requirements.txt /t0d0d0d0/bot/requirements.txt

RUN pip install -r /t0d0d0d0/bot/requirements.txt

COPY ./t0d0d0d0/bot /t0d0d0d0/bot
COPY ./t0d0d0d0/app /t0d0d0d0/app

ENV POSTGRES_URL=""
ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV RABBIT_URL=""
ENV BOT_TOKEN=""

RUN useradd -m appuser
USER appuser
CMD ["python", "-m", "t0d0d0d0.bot"]