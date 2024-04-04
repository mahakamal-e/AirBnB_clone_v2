#!/usr/bin/python3
""" a Fabric script distributes an archive to your web servers."""
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
    """ Function that distributes an archive to web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put("{}".format(archive_path), "/tmp/")
        filename = os.path.basename(archive_path)
        f_without_ext = os.path.splitext(filename)[0]
        release_dir = "/data/web_static/releases/{}".format(f_without_ext)

        run("mkdir -p {}".format(release_dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, release_dir))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {} /data/web_static/current".format(release_dir))

        return True
    except Exception as e:
        print(e)
        return False

def deploy():
    """ Creates and distributes an archive path """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
