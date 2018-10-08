from quixote import get_publisher
import sys
pub = get_publisher()
permissions = {
    'users':[],
    'roles':[],
    'settings':[],
    'bounces':[],
    'forms':[],
    'workflows':[],
    'categories':[]
}

with open("/tmp/tmp_uuid_agent_fabriques.txt", 'r') as file_aa:
    uuid_aa = file_aa.read()
    permissions['forms'].append(uuid_aa)
    permissions['categories'].append(uuid_aa)
    if len(sys.argv) > 1 and sys.argv[1] == 'full':
        permissions['workflows'].append(uuid_aa)
    file_aa.close()

with open("/tmp/tmp_uuid_debug.txt", 'r') as file_debug:
    uuid_debug = file_debug.read()
    permissions['forms'].append(uuid_debug)
    permissions['categories'].append(uuid_debug)
    permissions['workflows'].append(uuid_debug)
    permissions['settings'].append(uuid_debug)
    permissions['bounces'].append(uuid_debug)

pub.cfg['admin-permissions'] = permissions
pub.write_cfg()

