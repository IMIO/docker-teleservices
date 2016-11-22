import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import dest
reload(dest)
result = '%(rue)s %(numero)s %(boite)s' % dest.get(globals())
