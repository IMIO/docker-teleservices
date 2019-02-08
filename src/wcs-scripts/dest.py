def get(variables):
    acceptation = variables.get('form_var_acceptation') or 'Simple'
    liste_vars = ['xxx'] # make sure all attributes are set
    if acceptation in ('Simple', 'Gratuit'):
        liste_vars = ['demandeur_liegeois', 'demandeur_plus_lg', 'demandeur',
                'demandeur_rad', 'demandeur_new_lg_etranger',
                'demandeur_new_lg_belgique', '']
    elif acceptation in ('Tiers', ):
        liste_vars = ['perscon', 'perscon_plus_lg']
    result = {}
    for attribute in ('prenom', 'nom', 'rue', 'complement_adresse', 'numero', 'boite', 'codepostal', 'localite', 'pays'):
        for var in liste_vars:
            if var != '':
                varname = 'form_var_%s_%s' % (attribute, var)
            else:
                varname = 'form_var_%s' % (attribute)
            result[attribute] = variables.get(varname) or result.get(attribute) or ''
            if result[attribute] == 'None':
                result[attribute] = ''
    return result
