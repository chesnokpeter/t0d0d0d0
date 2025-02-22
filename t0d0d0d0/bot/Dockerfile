FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ../bot/requirements.txt /bot/requirements.txt

RUN pip install -r /bot/requirements.txt

COPY ../bot /bot
COPY ../app /app

ENV POSTGRES_URL=""
ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV SECRET_KEY=""
ENV RABBIT_URL=""
ENV BOT_TOKEN=""

RUN useradd -m appuser
USER appuser
CMD ["python", "-m", "bot"]