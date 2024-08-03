bot:
	python -m t0d0d0d0.bot
back:
	uvicorn t0d0d0d0.backend.app:app --reload --port 8011

front:
	cd t0d0d0d0/frontend && npm run dev

migration:
	python -m alembic revision --autogenerate
	python -m alembic upgrade head


init:
	source .bash
