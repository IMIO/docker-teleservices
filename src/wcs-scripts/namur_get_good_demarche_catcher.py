if globals().get("form_var_nom_tiers") is not None:
    result = "{} {}".format(globals().get("form_var_nom_tiers"), globals().get("form_var_prenom_tiers"))
else:
    result = "{} {}".format(globals().get("form_var_nom_demandeur"), globals().get("form_var_prenom_demandeur"))

