bot:
	python -m t0d0d0d0.bot
back:
	uvicorn t0d0d0d0.restback.app:app --reload --port 8012

mypy:
	mypy app.py

front:
	cd t0d0d0d0/frontend && npm run dev

migration:
	python -m alembic revision --autogenerate
	python -m alembic upgrade head


npminstall:
	cd t0d0d0d0/frontend

notyfier:
	faststream run t0d0d0d0.notyfier.app:app

sheluder:
