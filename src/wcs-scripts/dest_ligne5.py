import sys
try:
    from importlib import reload
except ImportError:
    pass
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import dest
reload(dest)
result = '%(pays)s' % dest.get(globals())
