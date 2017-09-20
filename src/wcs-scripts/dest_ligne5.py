import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
import dest
reload(dest)
result = '%(pays)s' % dest.get(globals())
