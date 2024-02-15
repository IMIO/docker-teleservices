#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
# SUP-35051 · I added this docstring to make maintenability easier.
This Python script performs a series of text replacements in a translation file for the French language, specifically
for the Authentic 2 application. The purpose of these replacements is to standardize the terminology used within the
application, particularly standardizing the French terms for "email" and addressing some spelling preferences
"""


import os
import os.path
import subprocess

if os.path.isfile("/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po"):
    contents = open("/usr/share/pyshared/authentic2/locale/fr/LC_MESSAGES/django.po").read()
else:
    contents = open("/usr/lib/python3/dist-packages/authentic2/locale/fr/LC_MESSAGES/django.po").read()
contents = (
    # SUP-35051 · There was a bug that induced "adresse adresse" appearing
    # somewhere. That is whty I rewrited the following. It may seems redundant
    # but it was manually checked and explicitely placed in this order so it
    # does not produce inexpected effects. Please follow this approach for
    # further modifications.
    contents.replace("adresse de courriel", "adresse mail")
    .replace("adresses de courriel", "adresses mail")
    .replace("Nouveau courriel", "Nouvelle adresse mail")
    .replace("envois de courriels", "envois de mails")
    .replace("une même addresse de courriel", "une même adresse mail")
    .replace("Propager les courriels", "Propager les mails")
    .replace("d’un courriel", "d’un mail")
    .replace("Courriel vérifié", "Adresse mail vérifiée")
    .replace("Courriel non vérifié", "Adresse mail non vérifiée")
    .replace("Courriel (email)", "Adresse mail")
    .replace("Courriel ou", "Adresse mail ou")
    .replace("Courriel : %(email)s", "Adresse mail : %(email)s")
    .replace("Courriel d’alerte", "Mail d’alerte")
    .replace("Courriel :", "Adresse mail :")
    .replace("Courriels", "Adresses mail")
    .replace('msgstr "Courriel"', 'msgstr "Adresse mail"')
    .replace("Le courriel doit être unique", "L’adresse mail doit être unique")
    .replace("Le courriel est obligatoire", "L’adresse mail est obligatoire")
    .replace("des courriels envoyés", "des mails envoyés")
    .replace("Les courriels doivent être séparés", "Les adresses mail doivent être séparées")
    .replace("un courriel envoyé", "un mail envoyé")
    .replace("envoyer un courriel", "envoyer un mail")
    .replace("un courriel", "un mail")
    .replace("Un courriel", "Un mail")
    .replace("ce courriel", "ce mail")
    .replace("courriel vérifié", "mail vérifié")
    .replace("Votre adresse courriel", "Votre adresse mail")
    .replace("le courriel", "le mail")
    .replace("Plusieurs courriels", "Plusieurs mails")
    .replace("Les envois de nouveaux courriels sont bloqués", "Les envois de nouveaux mails sont bloqués")
    .replace("Adresse de courriel invalide", "Adresse mail invalide")
    .replace("Adresse de courriel: %(email)s", "Adresse mail: %(email)s")
    .replace("par courriel", "par mail")
    .replace("vérification du courriel", "vérification du mail")
    .replace("une adresse courriel", "une adresse mail")
    .replace("Votre compte n’a pas de courriel associé", "Votre compte n’a pas d’adresse mail associée")
    .replace("Nouveau courriel", "Nouveau mail")
    .replace("dresse de courriel", "dresse mail")
    .replace('msgstr "courriel"', 'msgstr "mail"')
    .replace("courriel d’initialisation", "mail d’initialisation")
    .replace("courriel comme clé.", "mail comme clé.")
    .replace("pour cette adresse courriel", "pour cette adresse mail")
    .replace("à cette adresse courriel", "à cette adresse mail")
    .replace("courriel de validation", "mail de validation")
    .replace("de courriels", "de mails")
    .replace("du courriel", "du mail")
    .replace("ré-initialiser", "réinitialiser")
    .replace("Ré-initialiser", "Réinitialiser")
    .replace("Ré-initialisez", "Réinitialisez")
)
fd = open("/var/lib/authentic2/locale/fr/LC_MESSAGES/authentic.po", "w")
fd.write(contents)
fd.close()

# SUP-35051 · I added the following explanations to make maintenability easier.
# msgcat: This is a command-line utility that concatenates and manipulates gettext PO (Portable Object) files.
# PO files are used in software development for internationalization; they contain source texts and their corresponding
# translations.
# --use-first: This option tells msgcat to use the first found translation when the same source text occurs more than
# once across the files being concatenated.
# The paths /var/lib/authentic2/locale/fr/LC_MESSAGES/overrides.po and
# /var/lib/authentic2/locale/fr/LC_MESSAGES/authentic.po specify the PO files to be concatenated. The first file likely
# contains custom or overridden translations specific to the local deployment, while the second file contains the
# default translations provided with the Authentic 2 software.
# --output: This option specifies the output file path.
# The output file path /var/lib/authentic2/locale/fr/LC_MESSAGES/django.po indicates where the concatenated PO file will
# be saved. This file now contains a merged set of translations that will be used by the Django application (as
# Authentic 2 is a Django-based application).
subprocess.call(
    [
        "msgcat",
        "--use-first",
        "/var/lib/authentic2/locale/fr/LC_MESSAGES/overrides.po",
        "/var/lib/authentic2/locale/fr/LC_MESSAGES/authentic.po",
        "--output",
        "/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po",
    ]
)

# SUP-35051 · I added the following explanations to make maintenability easier.
# msgfmt: This utility compiles PO files into binary MO (Machine Object) files. MO files are used by gettext, a
# localization framework, at runtime to provide the appropriate translations based on the user's language settings.
# -o: This option specifies the output MO file path.
# The input PO file path /var/lib/authentic2/locale/fr/LC_MESSAGES/django.po is the file generated by the previous
# msgcat command.
# The output MO file path /var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo is where the compiled translation file is
# saved. This binary file is what the Django application will use to display the French translations.
subprocess.call(
    [
        "msgfmt",
        "-o",
        "/var/lib/authentic2/locale/fr/LC_MESSAGES/django.mo",
        "/var/lib/authentic2/locale/fr/LC_MESSAGES/django.po",
    ]
)
