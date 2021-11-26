requirements:
	pip install --upgrade pip
	pip install -r requirements.txt

local:
	uvicorn app.main:app --reload

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build