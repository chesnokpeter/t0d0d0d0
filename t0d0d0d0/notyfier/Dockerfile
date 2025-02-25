FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ./t0d0d0d0/notyfier/requirements.txt /t0d0d0d0/notyfier/requirements.txt

RUN pip install -r /t0d0d0d0/notyfier/requirements.txt

COPY ./t0d0d0d0/notyfier /t0d0d0d0/notyfier
COPY ./t0d0d0d0/app /t0d0d0d0/app

ENV BOT_TOKEN=""
ENV RABBIT_URL=""

RUN useradd -m appuser
USER appuser
CMD ["faststream", "run", "t0d0d0d0.notyfier.app:app"]