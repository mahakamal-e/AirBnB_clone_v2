#!/usr/bin/python3
"""A Fabric script distributes an archive to your web servers."""
from fabric.api import *
import os
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['3.85.1.33', '100.26.171.116']


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


def do_deploy(archive_path):
    """ a Faunction that deplys an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = archive_path.split("/")[-1]
        f_without_ext = filename.split(".")[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(f_without_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, f_without_ext))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(f_without_ext,
                                                  f_without_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(no_extension))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(no_extension))
        return True

    except Exception as e:
        return False


def deploy():
    """ creates & distributes archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
