import sys
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import dest
reload(dest)
result = '%(complement_adresse)s' % dest.get(globals())
