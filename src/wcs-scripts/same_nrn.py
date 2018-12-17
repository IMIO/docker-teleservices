from wcs.qommon import misc
from wcs.qommon.storage import Contains

def find_same_nrn(formdef, context, *args):
    result = False
    applied_filters = ['wf-%s' % x.id for x in formdef.workflow.get_not_endpoint_status()]
    formdatas = formdef.data_class().select([Contains('status', applied_filters)])
    for formdata in formdatas:
        for field in formdef.get_all_fields():
            if field.varname is not None and ('nrn' in field.varname or 'nn' in field.varname):
                field_value = formdata.get_field_view_value(field)
                if field_value in args:
                    return True
    return result

if __name__ in ('__builtin__') and 'form_objects' in vars():
    result = find_same_nrn(form_objects.formdef, vars(), *args)
