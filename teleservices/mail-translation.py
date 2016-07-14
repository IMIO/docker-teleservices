#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

contents = open('/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po').read()
contents = contents.replace('adresse de courriel', 'adresse e-mail'
                  ).replace('Nouveau courriel', 'Nouvelle adresse e-mail'
                  ).replace('"Courriel"', '"Adresse e-mail"')
fd = open('/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po', 'w')
fd.write(contents)

print >> fd, """
#, python-format
msgid ""
"Please enter a correct %(username)s and password. Note that both fields may "
"be case-sensitive."
msgstr ""
"L’adresse e-mail et le mot de passe que vous avez saisis ne correspondent "
"pas. Si vous n'avez pas encore créé de compte, cliquez sur le lien "
"« Enregistrez-vous »."
"""

fd.close()

os.system('msgfmt -o /var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo /var/lib/authentic2/locale/fr/LC_MESSAGES/django.po')

