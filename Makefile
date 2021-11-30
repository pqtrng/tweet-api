ifneq (,$(wildcard ./.env))
    include .env
    export
endif

clean:
	docker rm $(BACKEND_CONTAINER_NAME) -vf || true
	docker image rm $(BACKEND_CONTAINER_IMAGE) -f || true
	docker rm $(DATABASE_CONTAINER_NAME) -vf || true
	docker image rm $(DATABASE_CONTAINER_IMAGE) -f || true
	docker image ls

requirements:
	pip install --upgrade pip
	pip install -r requirements.txt

local: requirements
	uvicorn app.main:app --reload

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

down-v:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down -v

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
	docker logs $(BACKEND_CONTAINER_NAME) -f

log:
	docker logs $(BACKEND_CONTAINER_NAME) -f

bash:
	docker exec -it $(BACKEND_CONTAINER_NAME) bash

test:
	pytest -v -s --disable-warnings -x