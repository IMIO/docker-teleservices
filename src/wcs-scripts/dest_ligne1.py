import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import dest
reload(dest)
result = '%(prenom)s %(nom)s' % dest.get(globals())
