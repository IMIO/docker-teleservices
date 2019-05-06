
def cout_accueil():
    return str(Decimal(form_option_cout_garderie) * (len((form_var_garderie0107_0507_raw if "du 1er juillet au 5 juillet 2019" in form_var_semainestage else [])                                       + (form_var_garderie0807_1207_raw if "du 8 juillet au 12 juillet 2019" in form_var_semainestage else [])                                       + (form_var_garderie1507_1907_raw if "du 15 juillet au 19 juillet 2019" in form_var_semainestage else [])                                       + (form_var_garderie2207_2607_raw if "du 22 juillet au 26 juillet 2019" in form_var_semainestage else [])                                       + (form_var_garderie2907_0208_raw if "du 29 juillet au 2 août 2019" in form_var_semainestage else [])                                       + (form_var_garderie0508_0908_raw if "du 5 août au 9 août 2019" in form_var_semainestage else []))))


def cout_reservation():
    return str(Decimal(form_option_cout_resident if form_var_code_postal == "1325" else form_option_cout_non_resident) * len(form_var_semainestage_raw))

if args[0] == "cout_accueil":
    result = cout_accueil

if args[0] == "cout_reservation":
    result = cout_reservation
