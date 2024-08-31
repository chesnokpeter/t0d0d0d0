bot:
	python -m t0d0d0d0.bot
back:
	uvicorn t0d0d0d0.restback.app:app --reload --port 8011

mypy:
	mypy app.py

front:
	cd t0d0d0d0/clients/frontend && npm run dev

migration:
	python -m alembic revision --autogenerate
	python -m alembic upgrade head


npminstall:
	cd t0d0d0d0/frontend