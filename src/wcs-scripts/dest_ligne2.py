import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import dest
reload(dest)
if boite:
    result = '%(rue)s %(numero)s / %(boite)s' % dest.get(globals())
else:
    result = '%(rue)s %(numero)s' % dest.get(globals())
