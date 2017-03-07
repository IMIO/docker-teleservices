import os
from wcs.workflows import Workflow

path = "/opt/publik/scripts/workflows-samples/"
dirs = os.listdir(path)

# print existing workflows
for wf in Workflow.select():
    print wf

# add new workflows into e-guichet instance.
for currfile in dirs:
    print "{}{}".format(path, currfile)
    fd = open("{}{}".format(path, currfile))
    wf = Workflow.import_from_xml(fd)
    wf.store()
