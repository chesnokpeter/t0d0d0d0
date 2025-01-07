from __future__ import annotations

import os

postgres_url = os.environ.get('POSTGRES_URL')
redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
rabbit_url = os.environ.get('RABBIT_URL')
bot_token = os.environ.get('BOT_TOKEN')
secret_key = os.environ.get('SECRET_KEY')
