# -*- coding: utf-8 -*-
DEBUG = False
# ex_places : Determne ou dans le tableau, on parle de nombre d'exemplaire.
if DEBUG:
    acte_divorce = {'doc': [['Boul', 'Ch', '07/01/1979', '07/01/2000', '1', '1', ''],
                            ['Boulanger', 'Christophe', '07/01/1979', '07/01/2000', '2', '3', '']], 'ex_places':(4,5)}
    acte_deces = {'doc': [['dfd', 'dddd', '07/01/1979', '07/01/2090', '2', '2', '']], 'ex_places':(4,5)}
    acte_mariage = {'doc': [['dfg', 'dfg', '10/01/1980', '10/10/2019', '2', '3', '']], 'ex_places':(4,5)}
    acte_naissance = {'doc': [['sdfsdf', 'sdfsdf', '07/01/1979', '1', '4', '1']], 'ex_places':(3,4)}
    certif_cohab_legale = {'doc': [['fdgdfg', 'dfgdfg', '07/01/1979', '3', '3', '1']], 'ex_places':(3,4)}
    certif_nationalite = {'doc': [['dfg', 'dfg', '10/10/2010', '2', '1']], 'ex_places':(3,4)}
    certif_residence = {'doc': [['dfg', 'dfg', '10/10/2010', '2', '3', '1']], 'ex_places':(3,4)}
    certif_residence_natio = {'doc': [['sfdgdfg', 'dfgdfg', '10/12/2050', '2', '1', '1']], 'ex_places':(3,4)}
    certif_residence_histo = {'doc': [['sdf', 'sdfsdf', '10/10/1978', '2', '1', '1']], 'ex_places':(3,4)}
    certif_vie = {'doc': [['sdfsdf', 'sdfsdf', '10/12/2016', '2', '1']], 'ex_places':(3,4)}
    compo_menage = {'doc': [['sdsdf', 'sdfsdf', '10/10/2000', '2', '1', '1']], 'ex_places':(3,4)}
    genealogie = {'doc': [['dfgdfg', 'dfgdfg', '10/10/2010', '2', '2', '1']], 'ex_places':(3,4)}
else:
    acte_divorce = {'doc': globals().get("form_var_tab_acte_divorce"), 'ex_places':(4,)}
    acte_deces = {'doc': globals().get("form_var_tab_acte_deces"), 'ex_places':(4,)}
    acte_mariage = {'doc': globals().get("form_var_tab_acte_mariage"), 'ex_places':(4,)}
    acte_naissance = {'doc': globals().get("form_var_tab_acte_naissance"), 'ex_places':(3,)}
    certif_cohab_legale = {'doc': globals().get("form_var_tab_cohab_legale"), 'ex_places':(3,)}
    certif_nationalite = {'doc': globals().get("form_var_tab_nationalite"), 'ex_places':(3,)}
    certif_residence = {'doc': globals().get("form_var_tab_residence"), 'ex_places':(3,)}
    certif_residence_natio = {'doc': globals().get("form_var_tab_residence_nationalite"), 'ex_places':(3,)}
    certif_residence_histo = {'doc': globals().get("form_var_tab_residence_histo"), 'ex_places':(3,)}
    certif_vie = {'doc': globals().get("form_var_tab_certif_vie"), 'ex_places':(3,)}
    compo_menage = {'doc': globals().get("form_var_tab_compo_menage"), 'ex_places':(3,)}
    genealogie = {'doc': globals().get("form_var_tab_genealogie"), 'ex_places':(3,)}

documents = {
    'Acte de divorce' : acte_divorce,
    'Acte de décès': acte_deces,
    'Acte de mariage': acte_mariage,
    'acte_naissance' : acte_naissance,
    'Certificat de cohabitation légale': certif_cohab_legale,
    'Certificat de nationalité': certif_nationalite,
    'Certificat de résidence' : certif_residence,
    'Certificat de résidence et nationalité': certif_residence_natio,
    'Certificat de résidence (historique)': certif_residence_histo,
    'Certificat de vie' : certif_vie,
    'Composition de ménage': compo_menage,
    'Demande de généalie' : genealogie
}

retour = ""
nom_prenom = ""
for key, tab_curr_document in documents.items():
    if tab_curr_document['doc'] is not None:
        for row in tab_curr_document['doc']:
            nom_prenom = "{} {}".format(row[0], row[1])
            nb_ex_doc = sum(int(row[ex_place]) for ex_place in tab_curr_document['ex_places'])
            retour = '{}{} copie(s) du formulaire : "{}" pour "{}" {}{}'.format(retour, nb_ex_doc, key, nom_prenom, chr(13), chr(10) )
result = retour
