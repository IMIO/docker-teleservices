result = str(Decimal(globals().get('form_option_cout_d_une_demande')) * int(globals().get('form_var_nb_exemplaire'))) if globals().get('form_var_objectif_raw') == "autre"  else "0"
