import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import dest
reload(dest)
result = '%(codepostal)s %(localite)s' % dest.get(globals())
