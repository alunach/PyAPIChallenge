.PHONY: install test lint run db-init db-upgrade

install:
	python -m pip install -r requirements.txt

test:
	pytest -q --disable-warnings --maxfail=1 --cov=app --cov-report=term-missing

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

db-init:
	alembic revision --autogenerate -m "init"

db-upgrade:
	alembic upgrade head
