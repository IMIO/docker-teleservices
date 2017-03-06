lst_enfants_concernes = globals().get("form_var_tab_enfants_concernes")
enfants_concernes = ""
for e in lst_enfants_concernes:
    enfants_concernes = enfants_concernes + "-  " + e[0] + " né(e) à " + e[1] + " le " + e[2] + "\r\n"
result = enfants_concernes
