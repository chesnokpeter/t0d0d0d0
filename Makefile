PY ?= python3

install_rest:
	$(PY) -m venv ./scripts/envs/restback
	@(\
		. scripts/envs/restback/bin/activate && \
		pip install -r t0d0d0d0/restback/requirements.txt \
	)

rest:
	@( \
		. scripts/envs/restback/bin/activate && \
		uvicorn t0d0d0d0.restback.app:app --reload --port 8012 \
	)



install_bot:
	$(PY) -m venv ./scripts/envs/bot
	@(\
		. scripts/envs/bot/bin/activate && \
		pip install -r t0d0d0d0/bot/requirements.txt \
	)

bot:
	@( \
		. scripts/envs/bot/bin/activate && \
		python -m t0d0d0d0.bot \
	)



install_notyfier:
	$(PY) -m venv ./scripts/envs/notyfier
	@(\
		. scripts/envs/notyfier/bin/activate && \
		pip install faststream aiogram aio_pika \
	)

notyfier:
	@(\
		. scripts/envs/notyfier/bin/activate && \
		faststream run t0d0d0d0.notyfier.app:app \
	)



install_front:
	cd t0d0d0d0/frontend && npm install --force


front:
	cd t0d0d0d0/frontend && npm run dev



migration:
	python -m alembic revision --autogenerate
	python -m alembic upgrade head

mypy:
	mypy app.py

ruff:
	ruff format
