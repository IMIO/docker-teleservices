#! /usr/bin/env python

import os

contents = open('/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po').read()
contents = contents.replace('adresse de courriel', 'adresse e-mail'
                  ).replace('Nouveau courriel', 'Nouvelle adresse e-mail'
                  ).replace('"Courriel"', '"Adresse e-mail"')
fd = open('/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po', 'w')
fd.write(contents)
fd.close()

os.system('msgfmt -o /var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo /var/lib/authentic2/locale/fr/LC_MESSAGES/django.po')

