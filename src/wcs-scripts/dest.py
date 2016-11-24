def get(variables):
    acceptation = variables.get('form_var_acceptation')
    liste_vars = ['xxx'] # make sure all attributes are set
    if acceptation in ('Simple', 'Gratuit'):
        liste_vars = ['demandeur_liegeois', 'demandeur_plus_lg', 'demandeur']
    elif acceptation in ('Tiers', ):
        liste_vars = ['perscon', 'perscon_plus_lg']
    result = {}
    for attribute in ('prenom', 'nom', 'rue', 'complement_adresse', 'numero', 'boite', 'codepostal', 'localite', 'pays'):
        for var in liste_vars:
            varname = 'form_var_%s_%s' % (attribute, var)
            result[attribute] = variables.get(varname) or ''
    return result
