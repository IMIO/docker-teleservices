branch=jessie

pull:
		docker-compose pull

clean:
		docker-compose kill
		docker-compose rm
		sudo rm -fr data/*/*/ data/wcs/config.pck data/wcs/.rnd

run:
		docker-compose -f docker-compose-$(branch).yml up

base:
		docker image build -f teleservices/Dockerfile-jessie -t teleservices-jessie:latest teleservices

LIST=hobo combo bijoe fargo authentic wcs passerelle

build: base $(LIST)

$(LIST):
		docker image build -f teleservices/Dockerfile-$@ -t teleservices-jessie-$@:latest teleservices

build-no-cache:
		docker-compose -f docker-compose-$(branch).yml build --no-cache

run-jessie:
		make run branch=jessie
build-jessie:
		make build branch=jessie
build-no-cache-jessie:
		make build-no-cache branch=jessie
