import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import dest
reload(dest)
if dest.get(globals()).get('boite'):
    result = '%(rue)s %(numero)s / %(boite)s' % dest.get(globals())
else:
    result = '%(rue)s %(numero)s' % dest.get(globals())
