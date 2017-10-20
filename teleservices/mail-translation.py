#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import subprocess

if os.path.isfile('/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po'):
    contents = open('/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po').read()
else:
    contents = open('/usr/lib/python2.7/dist-packages/authentic2/locale/fr/LC_MESSAGES/django.po').read()
contents = contents.replace('adresse de courriel', 'adresse e-mail'
                  ).replace('Nouveau courriel', 'Nouvelle adresse e-mail'
                  ).replace('dans ce courriel', 'dans cet e-mail'
                  ).replace('courriel de validation', 'e-mail de validation'
                  ).replace('un courriel', 'un e-mail'
                  ).replace('un mail', 'un e-mail'
                  ).replace('courriel', 'adresse e-mail'
                  ).replace('Courriel', 'Adresse e-mail'
                  ).replace('ré-initialiser', 'réinitialiser'
                  ).replace('Ré-initialiser', 'Réinitialiser')
                  ).replace('Ré-initialisez', 'Réinitialisez')
fd = open('/var/lib/authentic2/locale/fr/LC_MESSAGES/authentic.po', 'w')
fd.write(contents)
fd.close()

subprocess.call([
    'msgcat',
    '--use-first',
    '/var/lib/authentic2/locale/fr/LC_MESSAGES/overrides.po',
    '/var/lib/authentic2/locale/fr/LC_MESSAGES/authentic.po',
    '--output',
    '/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po'])

subprocess.call([
    'msgfmt',
    '-o',
    '/var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo',
    '/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po'])
