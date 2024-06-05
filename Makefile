clean:
		docker-compose kill
		docker-compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker-compose up

build-bookworm-base:
		cd teleservices && \
		docker build --pull -f Dockerfile-base -t imiobe/teleservices-bookworm-base:latest \
		--build-arg DEBIAN_VERSION=bookworm \
		.

build-bookworm:
		cd teleservices && \
		docker build --pull --target prod-image -t teleservices/bookworm:latest \
		--build-arg DEBIAN_VERSION=bookworm \
		.

build-bookworm-test:
		cd teleservices && \
		docker build --pull --target dev-image -t teleservices/bookworm-test:latest \
		--build-arg DEBIAN_VERSION=bookworm \
		.

build-no-cache-bookworm:
		cd teleservices && \
		docker build --pull --no-cache --target prod-image -t teleservices/bookworm:latest \
		--build-arg DEBIAN_VERSION=bookworm \
		.

build-no-cache-bookworm-test:
		cd teleservices && \
		docker build --pull --no-cache --target dev-image -t teleservices/bookworm-test:latest \
		--build-arg DEBIAN_VERSION=bookworm \
		.

run-bookworm-test:
		make run branch=bookworm-test

fast-clean:
	docker-compose down -v
	sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

.PHONY: validation-tests
validation-tests:
		docker-compose -f validation-tests/docker-compose.yml up --exit-code-from cypress
