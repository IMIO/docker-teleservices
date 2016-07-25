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

run-wheezy:
		make run branch=wheezy
build-wheezy:
		make build branch=wheezy

run-jessie:
		make run branch=jessie
build-jessie:
		make build branch=jessie
