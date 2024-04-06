#!/usr/bin/python3
""" a Fabric script distributes an archive to your web servers. """
from fabric.api import *
import os

env.user = 'ubuntu'
env.hosts = ['3.85.1.33', '100.26.171.116']


def do_deploy(archive_path):
    """Deploys an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        f_without_ext = os.path.splitext(filename)[0]
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(f_without_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, f_without_ext))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(f_without_ext,
                                                  f_without_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(f_without_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(f_without_ext))
        return True

    except Exception as e:
        print(e)
        return False
