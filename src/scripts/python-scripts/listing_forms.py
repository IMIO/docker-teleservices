# -*- coding: utf-8 -*-
# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=COMMUNE-formulaires.guichet-citoyen.be listing_forms.py COMMUNE

import csv
import re
import sys
from time import mktime
from datetime import datetime
from wcs.formdef import FormDef

cpt = 0
html = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf8\" /></head>"
datasources_existantes = []
categories_existantes = []
for formdef in FormDef.select(order_by='category_id'):
    current_category = "SANS CATEGORIE" if formdef.category is None else formdef.category.name.upper()
    if current_category not in categories_existantes:
        html = "{}<hr><h2>{}</h2>".format(html, current_category)
    categories_existantes.append(current_category)
    html = "{}<h3 style='margin-left:2em;'>{} ({})</h2>".format(html,formdef.name, "PUBLIE" if formdef.disabled is True else "DESACTIVE")
    html = "{}<p style='margin-left:3em;'>Workflow = {}</p>".format(html, formdef.workflow.name)
    html = "{}<p style='margin-left:3em;'>Source de donnees :</p><ul style='margin-left:4em;'>".format(html)
    for field in formdef.fields:
        if (hasattr(field, 'data_source') and field.data_source is not None and 
        len(field.data_source) > 0 and 
        field.data_source.get('type') not in datasources_existantes):
            datasources_existantes.append(field.data_source.get('type'))
            html = "{}<li>{}{}</li>".format(html, field.data_source.get('type'), 
                    ":{}".format(field.data_source.get('value')) if field.data_source.get('value') is not None else '')
    html = "{}</ul>".format(html)
    datasources_existantes = []
html = "{}</body></html>".format(html)

print html
