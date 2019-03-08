# create hobo variable "check_duplicate_nn" to test forms without checking duplicate nn in DB.
if globals().get('check_duplicate_nn') and str(globals().get('check_duplicate_nn')) == 'False':
    result = False
else:
    field_id = [x for x in form_objects.formdef.fields if x.varname == 'nn'][0].id
    result = bool(len([x for x in form_objects.formdef.data_class().select() if x.data.get(field_id) == form_var_nn and not x.is_draft()]) == 0)
