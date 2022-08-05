clean:
		docker-compose kill
		docker-compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker-compose up

build-buster:
		cd teleservices && \
		docker build --target prod-image -t teleservices/buster:latest \
		--build-arg DEBIAN_VERSION=buster \
		.

build-buster-test:
		cd teleservices && \
		docker build --target dev-image -t teleservices/buster-test:latest \
		--build-arg DEBIAN_VERSION=buster \
		.

build-buster-odoo9:
		cd teleservices && \
		docker build --target prod-image -t teleservices/buster-odoo9:latest \
		--build-arg DEBIAN_VERSION=buster \
		--build-arg IMIO_TS_AES_VERSION=0.2 \
		--build-arg PASSERELLE_IMIO_IA_AES_VERSION=0.2 \
		.

build-bullseye:
		cd teleservices && \
		docker build --target prod-image -t teleservices/bullseye:latest \
		--build-arg DEBIAN_VERSION=bullseye \
		.

build-bullseye-test:
		cd teleservices && \
		docker build --target dev-image -t teleservices/bullseye-test:latest \
		--build-arg DEBIAN_VERSION=bullseye \
		.

build-no-cache-buster:
		cd teleservices && \
		docker build --no-cache --target prod-image -t teleservices/buster:latest \
		--build-arg DEBIAN_VERSION=buster \
		.

build-no-cache-buster-test:
		cd teleservices && \
		docker build --no-cache --target dev-image -t teleservices/buster-test:latest \
		--build-arg DEBIAN_VERSION=buster \
		.

build-no-cache-buster-odoo9:
		cd teleservices && \
		docker build --no-cache --target prod-image -t teleservices/buster-odoo9:latest \
		--build-arg DEBIAN_VERSION=buster \
		--build-arg IMIO_TS_AES_VERSION=0.2 \
		--build-arg PASSERELLE_IMIO_IA_AES_VERSION=0.2 \
		.

build-no-cache-bullseye:
		cd teleservices && \
		docker build --no-cache --target prod-image -t teleservices/bullseye:latest \
		--build-arg DEBIAN_VERSION=bullseye \
		.

build-no-cache-bullseye-test:
		cd teleservices && \
		docker build --no-cache --target dev-image -t teleservices/bullseye-test:latest \
		--build-arg DEBIAN_VERSION=bullseye \
		.

run-buster-test:
		make run branch=buster-test

run-bullseye-test:
		make run branch=bullseye-test

fast-clean:
	docker-compose down -v
	sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd
