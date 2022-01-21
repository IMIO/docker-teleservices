clean:
		docker-compose kill
		docker-compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker-compose up

build-buster:
		cd teleservices && docker build -t teleservices/buster --build-arg DEBIAN_VERSION=buster .
build-bullseye:
		cd teleservices && docker build -t teleservices/bullseye --build-arg DEBIAN_VERSION=bullseye .

run-buster-test:
		make run branch=buster-test
build-buster-test:
		make build branch=buster-test
build-no-cache-buster-test:
		make build-no-cache branch=buster-test
