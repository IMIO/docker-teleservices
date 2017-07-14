from quixote import get_publisher
import sys

pub = get_publisher()
with open("/tmp/tmp_uuid_agent_admin.txt", 'r') as file_aa:
    uuid_aa = file_aa.read()
    pub.cfg['admin-permissions'] = {'users':[uuid_aa],
                                    'roles':[],
                                    'settings':[],
                                    'bounces':[],
                                    'forms':[],
                                    'workflows':[],
                                    'categories':[]
                                   }
    pub.write_cfg()

with open("/tmp/tmp_uuid_agent_fabriques.txt", 'r') as file_aa:
    set_workflow = []
    uuid_aa = file_aa.read()
    if len(sys.argv) > 0 and sys.argv[1] == 'full':
        set_workflow = [uuid_aa]
    pub.cfg['admin-permissions'] = {'users':[],
                                    'roles':[],
                                    'settings':[],
                                    'bounces':[],
                                    'forms':[uuid_aa],
                                    'workflows':set_workflow,
                                    'categories':[uuid_aa]
                                   }
    pub.write_cfg()

