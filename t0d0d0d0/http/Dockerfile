FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

RUN ls

COPY ./t0d0d0d0/http/requirements.txt /t0d0d0d0/http/requirements.txt

RUN pip install -r /t0d0d0d0/http/requirements.txt

COPY ./t0d0d0d0/http ./t0d0d0d0/http
COPY ./t0d0d0d0/app ./t0d0d0d0/app

ENV POSTGRES_URL=""
ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV SECRET_KEY=""
ENV RABBIT_URL=""

EXPOSE 8011

RUN useradd -m appuser
USER appuser
CMD ["uvicorn", "--factory", "t0d0d0d0.http.app:create_app", "--port", "8011"]