#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

contents = open('/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po').read()
contents = contents.replace('adresse de courriel', 'adresse e-mail'
                  ).replace('Nouveau courriel', 'Nouvelle adresse e-mail'
                  ).replace('"Courriel"', '"Adresse e-mail"')
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
