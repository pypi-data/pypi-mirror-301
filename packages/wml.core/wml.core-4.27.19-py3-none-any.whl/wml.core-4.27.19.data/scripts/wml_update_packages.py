#!python


import pkg_resources
from subprocess import call

packages = [dist.project_name for dist in pkg_resources.working_set]
packages = [x for x in packages if x.startswith("wml")]
call(
    "wml_nexus.py pip3 install --trusted-host localhost --extra-index https://localhost:5443/repository/ml-py-repo/simple/ --upgrade "
    + " ".join(packages),
    shell=True,
)
