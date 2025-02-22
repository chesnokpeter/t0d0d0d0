FROM python:3.13.2-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --upgrade pip && \
    apt-get clean

COPY ../notyfier/requirements.txt /notyfier/requirements.txt

RUN pip install -r /notyfier/requirements.txt

COPY ../notyfier /notyfier
COPY ../app /app

ENV POSTGRES_URL=""
ENV SECRET_KEY=""
ENV RABBIT_URL=""

RUN useradd -m appuser
USER appuser
CMD ["faststream", "run", "notyfier.app:app"]