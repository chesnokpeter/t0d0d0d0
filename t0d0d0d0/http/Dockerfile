FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

RUN ls

COPY ../http/requirements.txt /http/requirements.txt

RUN pip install -r /http/requirements.txt

COPY ../http ./http
COPY ../app ./app

ENV POSTGRES_URL=""
ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV SECRET_KEY=""
ENV RABBIT_URL=""

EXPOSE 8011

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "--factory", "http.app:create_app", "--port", "8011"]