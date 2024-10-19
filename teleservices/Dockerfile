ARG DEBIAN_VERSION
FROM harbor.imio.be/teleservices/teleservices-${DEBIAN_VERSION}-base:latest as prod-image
ARG DEBIAN_VERSION

RUN apt-get update && apt-get install -y \
  imio-townstreet \
  imio-ts-aes \
  passerelle-imio-abiware \
  passerelle-imio-aes-health \
  passerelle-imio-aes-meal \
  passerelle-imio-apims-baec \
  passerelle-imio-apims-casier-judiciaire \
  passerelle-imio-apims-certificats-population \
  passerelle-imio-focus \
  passerelle-imio-ia-aes \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-membre \
  passerelle-imio-sso-agents \
  passerelle-imio-wca \
  scripts-teleservices \
  teleservices-iacitizen \
  teleservices-package \
  teleservices-package-certificats-population \
  teleservices-package-liaisons \
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
COPY scripts /opt/publik/scripts
COPY hooks /opt/publik/hooks
COPY screenrc /opt/publik/

ADD bash-vim.tar.gz /

RUN ln -sf /usr/share/zoneinfo/Europe/Brussels /etc/localtime

# Run
CMD ["/run.sh"]

FROM prod-image AS dev-image
ARG DEBIAN_VERSION
RUN echo "deb [signed-by=/etc/apt/keyrings/imio.gpg] https://nexus.imio.be/repository/${DEBIAN_VERSION}-test ${DEBIAN_VERSION}-test main" > /etc/apt/sources.list.d/imio-test.list \
  && cat /etc/apt/sources.list.d/*

RUN apt-get update && apt-get install -y \
  python3-pip \
  imio-townstreet \
  imio-ts-aes \
  passerelle-imio-aes-health \
  passerelle-imio-aes-meal \
  passerelle-imio-apims-baec \
  passerelle-imio-apims-certificats-population \
  passerelle-imio-focus \
  passerelle-imio-ia-aes \
  passerelle-imio-ia-delib \
  passerelle-imio-ia-tech \
  passerelle-imio-membre \
  passerelle-imio-sso-agents \
  passerelle-imio-wca \
  python3-pip \
  scripts-teleservices \
  teleservices-package \
  teleservices-package-certificats-population \
  teleservices-package-liaisons \
  teleservices-package-light \
  wcs-scripts-teleservices \
  --allow-unauthenticated

RUN pip3 install sentry-sdk uwsgitop --break-system-packages
COPY prometheus_uwsgi_exporter.py /usr/bin/
RUN crontab -l | { cat; echo "* * * * * /usr/bin/python3 /usr/bin/prometheus_uwsgi_exporter.py"; } | crontab -
