# -*- coding: utf-8 -*-
# authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/cpt_auth_users.py -d lalouviere-auth.guichet-citoyen.be

from calendar import monthrange
from datetime import datetime
from dateutil import relativedelta
from django.contrib.auth import get_user_model

import pytz

User = get_user_model()
users = User.objects.all()

def cpt_all_users():
    return len(users)

def cpt_users_with_rights():
    cpt = 0
    for user in users:
        if user.roles.count() > 0:
            cpt = cpt + 1 
    return cpt

def cpt_users_with_recent_connexion(nb_month_return_to=1):
    cpt = 0
    utc = pytz.utc
    now = datetime.now()
    now = utc.localize(now)
    for user in users:
        if user.last_login is not None:
            delta = relativedelta.relativedelta(now, user.last_login)
            if delta.months < nb_month_return_to:
                if delta.days > 0:
                    cpt = cpt + 1
    return cpt

cpt_all_users = cpt_all_users()
cpt_users_with_rights = cpt_users_with_rights()
cpt_users_with_recent_connexion = cpt_users_with_recent_connexion(nb_month_return_to=3)

# Nombre d'utilisateurs totaux    
#print(cpt_all_users)

# Nombre d'utilisateurs avec au moins 1 droit
#print(cpt_users_with_rights)

# Nombre d'utilisateur avec une connection recente
#print(cpt_users_with_recent_connexion)


data = {'all_users':cpt_all_users,
        'users_with_rights':cpt_users_with_rights,
        'users_with_recent_connexion':cpt_users_with_recent_connexion
        }

print(data)
