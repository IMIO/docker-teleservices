# -*- coding: utf-8 -*-
from authentic2.compat import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_rbac.utils import get_role_model, get_ou_model
from hobo.agent.authentic2.provisionning import provisionning
import hashlib


def create_authentic_user():
    User = get_user_model()
    OU = get_ou_model()
    Role = get_role_model()
    organisation_unit = OU.objects.get(default = True)
    with provisionning:
        # create default role in ts2.
        try:
            role_agent_fabriques = Role.objects.get(name='Agent ayant acces aux fabriques')
        except ObjectDoesNotExist:
            role_agent_fabriques = Role(name='Agent ayant acces aux fabriques', ou=organisation_unit)
            role_agent_fabriques.save()

        try:
            role_agent_traitant_pop = Role.objects.get(name='Agents traitants - Population, etat civil')
        except ObjectDoesNotExist:
            role_agent_traitant_pop = Role(name='Agents traitants - Population, etat civil', ou=organisation_unit)
            role_agent_traitant_pop.save()

        try:
            role_agent_traitant_trav = Role.objects.get(name='Agents traitants - Travaux')
        except ObjectDoesNotExist:
            role_agent_traitant_trav = Role(name='Agents traitants - Travaux', ou=organisation_unit)
            role_agent_traitant_trav.save()

        with open("/tmp/tmp_uuid_agent_fabriques.txt", 'w') as f:
            f.write(role_agent_fabriques.uuid)
            f.close()

        with open("/tmp/tmp_uuid_agent_traitant_pop.txt", 'w') as f:
            f.write(role_agent_traitant_pop.uuid)
            f.close()

        with open("/tmp/tmp_uuid_agent_traitant_trav.txt", 'w') as f:
            f.write(role_agent_traitant_trav.uuid)
            f.close()

        # GET or Create default user with default organisation unit.
        try:
            user_admin_commune = User.objects.get(username='admin_commune')
            user_admin_commune.email = "admin_commune@{}.be".format('COMMUNE_ID')
            user_admin_commune.first_name = "Admin"
            user_admin_commune.last_name = "Commune"

        except:
            user_admin_commune = User(username='admin_commune',
                                 first_name="Admin",
                                 last_name="Commune",
                                 email="admin_commune@{}.be".format('COMMUNE_ID'),
                                 ou=organisation_unit)
            user_admin_commune.set_password(create_password('COMMUNE_ID'))
        user_admin_commune.save()
        role_admin_user = Role.objects.get(name="Administrateur des utilisateurs")
        role_admin_role = Role.objects.get(name="Administrateur des rôles")
        role_admin_user.members.add(user_admin_commune)
        role_admin_role.members.add(user_admin_commune)
        role_agent_fabriques.members.add(user_admin_commune)

def create_password(commune_id):
    m = hashlib.md5(commune_id)
    return m.hexdigest()

create_authentic_user()
