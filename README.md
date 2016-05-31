This repo is a package of some [entr'ouvert](https://www.entrouvert.com) products.
It's a docker-compose based project to allow locally usage of e-guichet project.

Requirements:
docker-compose 1.6 or above

Usage:
sudo sh -c "echo '127.0.0.1 local-hobo.example.net local-auth.example.net local-formulaires.example.net local.example.net local-portail-agent.example.net local-documents.example.net local-passerelle.example.net' >> /etc/hosts"

docker-compose run
And go to http://local.example.net with you favorite browser(admin/password)
