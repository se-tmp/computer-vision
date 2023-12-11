all: up

up:
	docker-compose -f ./docker-compose.yml up -d
down:
	docker-compose -f ./docker-compose.yml down
re:
	bash ./clean.sh
	docker-compose -f ./docker-compose.yml build --parallel
	docker-compose -f ./docker-compose.yml up -d
clean:
	bash clean.sh