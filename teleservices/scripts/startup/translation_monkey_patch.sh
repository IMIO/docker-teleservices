#!/bin/bash

prefix="✨ translation_monkey_patch.sh ·"
monkey_prefix="🐒Monkey-patching"


# iMio DE/FR translations monkey patch
# Should only run on Eupen or Kelmis
if [ -e /var/lib/wcs/tenants/eupen-formulaires.guichet-citoyen.be/ ] || [ -e /var/lib/wcs/tenants/kelmis-formulaires.guichet-citoyen.be/ ]; then
  echo "$prefix $monkey_prefix Monkey-patching translations files  (iMio DE/FR translations monkey patch)."
  echo "✨ Fetching raw file from GitHub for authentic..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/authentic2_django.po -o /usr/lib/python3/dist-packages/authentic2/locale/fr/LC_MESSAGES/django.po
  echo "Running django-admin compilemessages for authentic..."
  cd /usr/lib/python3/dist-packages/authentic2
  django-admin compilemessages
  cd -
  echo "✨ Restarting authentic..."
  service authentic2-multitenant restart
  echo "✨ Fetching raw file from GitHub for wcs..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/wcs_django.po -o /usr/lib/python3/dist-packages/wcs/locale/fr/LC_MESSAGES/django.po
  echo "✨ Running django-admin compilemessages for wcs..."
  cd /usr/lib/python3/dist-packages/wcs/
  django-admin compilemessages
  cd -
  echo "✨ Restarting wcs..."
  service wcs restart
  echo "✨ Fetching raw file from GitHub for combo..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/combo_django.po -o /usr/lib/python3/dist-packages/combo/locale/fr/LC_MESSAGES/django.po
  cd /usr/lib/python3/dist-packages/combo/
  echo "✨ Running django-admin compilemessages for combo..."
  django-admin compilemessages
  cd -
  service combo restart
  echo "✨ Fetching raw file from GitHub for auquotidien..."
  curl https://raw.githubusercontent.com/IMIO/teleservices-german-translations/main/auquotidien_django.po -o /usr/lib/python3/dist-packages/auquotidien/locale/fr/LC_MESSAGES/django.po
  echo "✨ Running django-admin compilemessages for auquotidien..."
  cd /usr/lib/python3/dist-packages/auquotidien
  django-admin compilemessages
  cd -
  echo "Restarting wcs..."
  service wcs restart
  echo "$prefix $monkey_prefix Monkey-patching translations files  (iMio DE/FR translations monkey patch) done! ✅"
fi