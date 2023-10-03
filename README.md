This repo is a package of some [entr'ouvert](https://www.entrouvert.com) products.
It's a docker-compose based project to allow locally usage of e-guichet project.

### Requirements

docker-compose 1.6 or above

### Usage

* Add required host names to your /etc/hosts file, for example:

    sudo sh -c "echo '127.0.0.1 local-hobo.example.net local-auth.example.net local-formulaires.example.net local.example.net local-portail-agent.example.net local-documents.example.net local-passerelle.example.net local-agendas.example.net' >> /etc/hosts"

* Compose and run the container image

    docker-compose run localteleservices

* Go to http://local.example.net with you favorite browser, an admin account is
  setup, username is "admin" and password is "password" (without the quotes).

### Development

You can clone modules into the src/ directory and they will automatically be
used in the container environment.

Supported modules are:

* combo
* imio-publik-themes (hence publik-base-theme)
* passerelle
* passerelle-imio-tax-compute
* passerelle-imio-ia-aes

Services will be run in django-runserver mode, and can be seen in a screen
session running in the container.

    docker exec -ti dockerteleservices_localteleservices_1 bash
    script -c "screen -r"
