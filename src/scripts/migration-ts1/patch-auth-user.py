# -*- coding: utf-8 -*-
from authentic2.compat import get_user_model
from django_rbac.utils import get_role_model, get_ou_model
from hobo.agent.authentic2.provisionning import provisionning
import hashlib


def patch_authentic_user():
    User = get_user_model()
    OU = get_ou_model()
    Role = get_role_model()
    organisation_unit = OU.objects.get(default = True)
    with provisionning:

        role_agent_fabriques = Role(name='Agent ayant accès aux fabriques', ou=organisation_unit)
        role_agent_fabriques.save()

        with open("/tmp/tmp_uuid_agent_fabriques.txt", 'w') as f:
            f.write(role_agent_fabriques.uuid)

        # Set role to user
        role_agent_fabriques.members.add(user_admin_commune)

patch_authentic_user()
