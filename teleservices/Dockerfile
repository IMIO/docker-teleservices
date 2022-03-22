ARG DEBIAN_VERSION
FROM debian:${DEBIAN_VERSION} as prod-image
ARG DEBIAN_VERSION
ARG IMIO_TS_AES_VERSION=1.0
ARG PASSERELLE_IMIO_IA_AES_VERSION=1.0
# Setting ENV variables
ENV DEBIAN_FRONTEND=noninteractive \
  APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn \
  LANG=C.UTF-8 \
  LC_ALL=C.UTF-8

# Setting APT parameters
RUN echo "APT::Install-Suggests \"false\";\nAPT::Install-Recommends \"false\";" >> /etc/apt/apt.conf

# Don't allow services to start when building the image
RUN echo "#!/bin/sh\nexit 101" > /usr/sbin/policy-rc.d \
  && chmod +x /usr/sbin/policy-rc.d \
  && sed -i "s%httpredir.debian.org%debian.mirrors.ovh.net%g" /etc/apt/sources.list

RUN apt update && apt install -y \
  apt-transport-https \
  bash-completion \
  ca-certificates \
  cron \
  curl \
  debian-archive-keyring \
  gettext \
  gnupg \
  lftp \
  libreoffice \
  locales \
  nginx \
  procps \
  rsyslog \
  vim-nox

# Configure extra repositories
RUN export && echo ${DEBIAN_VERSION}  && echo "deb http://deb.entrouvert.org/ ${DEBIAN_VERSION} main" > /etc/apt/sources.list.d/entrouvert-local.list \
  && echo "deb http://debian.mirrors.ovh.net/debian ${DEBIAN_VERSION}-backports main" > /etc/apt/sources.list.d/backports.list \
  && echo "deb [trusted=yes] https://nexus.imio.be/repository/${DEBIAN_VERSION} ${DEBIAN_VERSION} main" > /etc/apt/sources.list.d/imio.list \
  && cat /etc/apt/sources.list.d/*

RUN curl https://static.imio.be/imio.gpg | apt-key add - \
  && curl https://deb.entrouvert.org/entrouvert.gpg | apt-key add -

RUN cat /etc/apt/sources.list.d/imio.list && apt update && apt install -y \
  entrouvert-repository \
  entrouvert-repository-eobuilder \
  entrouvert-repository-hotfix \
  && apt update && rm /etc/apt/sources.list.d/entrouvert-local.list 

RUN echo "Package: *\nPin: release a=$DEBIAN_VERSION-eobuilder\nPin-Priority: 400" > /etc/apt/preferences.d/entrouvert-eobuilder

# Install extra modules
RUN apt install -y \
  authentic2-multitenant \
  bijoe \
  combo \
  chrono \
  fargo \
  hobo \
  passerelle \
  publik-base-theme \
  poppler-utils \
  python-magic \
  python3-authentic2-auth-fedict \
  python3-passerelle \
  python3-dns \
  python3-docutils \
  python3-qrcode \
  python3-magic \
  python3-workalendar \
  wcs-au-quotidien \
  && apt install -y \
  imio-publik-themes \
  publik-imio-industrialisation \
  python3-combo-plugin-imio-townstreet \
  python3-passerelle-imio-extra-fees \
  python3-passerelle-imio-liege-lisrue \
  python3-passerelle-imio-liege-rn \
  python3-passerelle-imio-ts1-datasources
RUN apt install -y \
  -t $DEBIAN_VERSION-eobuilder \
  && apt install -y \
  imio-townstreet \
  imio-town-time \
  "imio-ts-aes=$IMIO_TS_AES_VERSION*" \
  passerelle-imio-aes-meal \
  passerelle-imio-aes-health \
  "passerelle-imio-ia-aes=$PASSERELLE_IMIO_IA_AES_VERSION*" \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-sso-agents \
  scripts-teleservices \
  teleservices-package \
  wcs-scripts-teleservices \
  --allow-unauthenticated

# Allow services to start, this is necessary as hobo-agent postinst will fail
# if supervisord is not running
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d \
  && echo "server_names_hash_bucket_size 128;" > /etc/nginx/conf.d/server_names.conf \
  && apt install -y hobo-agent

# Change cron time of authentic2 cleanup
RUN sed -i "s/5 \*/5 1/g" /etc/cron.d/authentic2-multitenant

# Cleanup
RUN rm -f /etc/default/authentic2-multitenant \
  && apt-get -y remove python-dev \
  && apt-get -y autoremove

RUN mkdir -p /var/lib/authentic2/locale/fr/LC_MESSAGES

COPY mail-translation.py overrides.po /var/lib/authentic2/locale/fr/LC_MESSAGES/
COPY run.sh /
COPY hooks /opt/publik/hooks
COPY screenrc /opt/publik/

ADD bash-vim.tar.gz /

RUN ln -sf /usr/share/zoneinfo/Europe/Brussels /etc/localtime

# Run
CMD ["/run.sh"]

FROM prod-image as dev-image
ARG DEBIAN_VERSION
RUN echo "deb [trusted=yes] https://nexus.imio.be/repository/${DEBIAN_VERSION}-test ${DEBIAN_VERSION}-test main" > /etc/apt/sources.list.d/imio-test.list \
  && cat /etc/apt/sources.list.d/*

RUN apt update && apt install -y imio-townstreet \
  imio-town-time \
  imio-ts-aes \
  passerelle-imio-aes-meal \
  passerelle-imio-aes-health \
  passerelle-imio-ia-aes \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-sso-agents \
  scripts-teleservices \
  teleservices-package \
  wcs-scripts-teleservices \
  --allow-unauthenticated