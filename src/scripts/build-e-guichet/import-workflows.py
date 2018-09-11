import os
import sys
from wcs.workflows import Workflow
# for wf in Workflow.select():
#    print wf

# default path : "/opt/publik/scripts/build-e-guichet/workflows/"
folder_path = sys.argv[1]
for fichier in os.listdir(folder_path):
    if fichier[-4:] == ".wcs":
        print "{}{}".format(folder_path, fichier)
        fd = open("{}{}".format(folder_path, fichier))
        wf = Workflow.import_from_xml(fd)
        wf.store()
