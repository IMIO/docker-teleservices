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

pub.cfg['admin-permissions'] = permissions
pub.write_cfg()

