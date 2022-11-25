ARG DEBIAN_VERSION
FROM imiobe/teleservices-${DEBIAN_VERSION}-base as prod-image
ARG DEBIAN_VERSION

RUN apt update && apt install -y \
  imio-townstreet \
  imio-ts-aes \
  passerelle-imio-abiware \
  passerelle-imio-aes-meal \
  passerelle-imio-aes-health \
  passerelle-imio-apims-baec \
  passerelle-imio-ia-aes \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-sso-agents \
  passerelle-imio-wca \
  python3-passerelle-imio-extra-fees/*-eobuilder \
  python3-passerelle-imio-ts1-datasources \
  scripts-teleservices \
  teleservices-iacitizen \
  teleservices-package \
  teleservices-package-light \
  wcs-scripts-teleservices \
  --allow-unauthenticated

# Allow services to run
RUN rm /usr/sbin/policy-rc.d

RUN echo "server_names_hash_bucket_size 128;" > /etc/nginx/conf.d/server_names.conf

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
  imio-ts-aes \
  passerelle-imio-aes-meal \
  passerelle-imio-aes-health \
  passerelle-imio-apims-baec \
  passerelle-imio-ia-aes \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-sso-agents \
  python3-pip \
  scripts-teleservices \
  teleservices-package \
  wcs-scripts-teleservices \
  --allow-unauthenticated

RUN pip3 install sentry-sdk uwsgitop
COPY prometheus_uwsgi_exporter.py /usr/bin/
RUN crontab -l | { cat; echo "* * * * * /usr/bin/prometheus_uwsgi_exporter.py"; } | crontab -