branch=use-modules-from-git-clones

pull:
		docker-compose pull

clean:
		docker-compose kill
		docker-compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker-compose -f docker-compose-$(branch).yml up

build:
		docker-compose -f docker-compose-$(branch).yml build
build-no-cache:
		docker-compose -f docker-compose-$(branch).yml build --no-cache

run-wheezy:
		make run branch=wheezy
build-wheezy:
		make build branch=wheezy
build-no-cache-wheezy:
		make build-no-cache branch=wheezy

run-jessie:
		make run branch=jessie
build-jessie:
		make build branch=jessie
build-no-cache-jessie:
		make build-no-cache branch=jessie
