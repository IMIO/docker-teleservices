# -*- coding: utf-8 -*-
from decimal import Decimal
import os
import sys


if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))


def cout_accueil(data):
    try:
        return str(Decimal(data.get('form_option_cout_garderie')) * len((data.get('form_var_garderie_s1_raw') or [] if "du 1er juillet au 5 juillet 2019" in data.get('form_var_semainestage') else []) + (data.get('form_var_garderie_s2_raw') or [] if "du 8 juillet au 12 juillet 2019" in data.get('form_var_semainestage') else []) + (data.get('form_var_garderie_s3_raw') or [] if "du 15 juillet au 19 juillet 2019" in data.get('form_var_semainestage') else []) + (data.get('form_var_garderie_s4_raw') or [] if "du 22 juillet au 26 juillet 2019" in data.get('form_var_semainestage') else []) + (data.get('form_var_garderie_s5_raw') or [] if "du 29 juillet au 2 août 2019" in data.get('form_var_semainestage') else []) + (data.get('form_var_garderie_s6_raw') or [] if "du 5 août au 9 août 2019" in data.get('form_var_semainestage') else [])))
    except:
        return '-1'

def cout_reservation(data):
    try:
        return str(Decimal(data.get('form_option_cout_resident') if data.get('form_var_code_postal') == "1325" else data.get('form_option_cout_non_resident')) * len(data.get('form_var_semainestage_raw')))
    except:
        return '-1'

if args[0] == "coutaccueil":
    result = cout_accueil(vars())

if args[0] == "coutreservation":
    result = cout_reservation(vars())
