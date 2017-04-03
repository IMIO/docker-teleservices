from quixote import get_publisher
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
