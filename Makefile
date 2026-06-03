clean:
		docker compose kill
		docker compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker compose up

build-bookworm-base:
		cd teleservices && \
		docker build --pull -f Dockerfile-base -t harbor.imio.be/teleservices-bookworm-base:latest \
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
	docker compose down -v
	sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

clone-src:
	mkdir -p src
	cd src && for repo in \
	    passerelle-imio-ia-tech \
	    passerelle-imio-ia-aes \
	    passerelle-imio-ia-delib \
	    passerelle-imio-keycloak \
	    passerelle-imio-focus \
	    passerelle-imio-abiware \
	    passerelle-imio-aes-health \
	    passerelle-imio-aes-meal \
	    passerelle-imio-apims-baec \
	    passerelle-imio-apims-casier-judiciaire \
	    passerelle-imio-apims-certificats-population \
	    passerelle-imio-membre \
	    passerelle-imio-sso-agents \
	    passerelle-imio-wca \
	    imio-townstreet \
	    imio-ts-aes \
	    imio-publik-themes \
	    teleservices-package \
	    teleservices-package-light \
	    teleservices-package-liaisons \
	    teleservices-package-certificats-population \
	    teleservices-iacitizen \
	    scripts-teleservices \
	    wcs-scripts-teleservices; do \
	        [ -d "$$repo" ] || git clone git@github.com:IMIO/$$repo.git; \
	    done

.PHONY: validation-tests
validation-tests:
		docker compose -f validation-tests/docker-compose.yml up --exit-code-from cypress
