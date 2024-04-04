#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static folder."""


from fabric.api import local
from datetime import datetime


def do_pack():
    """This function is responsible for generating the .tgz archive."""
    get_current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_file = 'versions'
    try:
        local("mkdir -p {}".format(archive_file))
        archive_name = "{}/web_static_{}.tgz".format(archive_file,
                                                     get_current_date)
        local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        return None
