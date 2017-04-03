# -*- coding: utf-8 -*-
from authentic2.compat import get_user_model
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
        role_agent_admin = Role(name='Agent administrateur des utilisateurs', ou=organisation_unit)
        role_agent_admin.save()

        role_agent_traitant_pop = Role(name='Agents traitants - Population, etat civil', ou=organisation_unit)
        role_agent_traitant_pop.save()

        role_agent_traitant_trav = Role(name='Agents traitants - Travaux', ou=organisation_unit)
        role_agent_traitant_trav.save()

        with open("/tmp/tmp_uuid_agent_admin.txt", 'w') as f:
            f.write(role_agent_admin.uuid)

        with open("/tmp/tmp_uuid_agent_traitant_pop.txt", 'w') as f:
            f.write(role_agent_traitant_pop.uuid)

        with open("/tmp/tmp_uuid_agent_traitant_trav.txt", 'w') as f:
            f.write(role_agent_traitant_trav.uuid)

        # Create default user with default organisation unit.
        user_admin_commune = User(username='admin_commune', ou=organisation_unit)
        user_admin_commune.set_password(create_password('COMMUNE_ID'))
        user_admin_commune.save()

        # Set role to user
        role_agent_admin.members.add(user_admin_commune)

def create_password(commune_id):
    m = hashlib.md5(commune_id)
    return m.hexdigest()[10]

create_authentic_user()
