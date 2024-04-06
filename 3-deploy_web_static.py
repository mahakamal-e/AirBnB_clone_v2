#!/usr/bin/python3
"""A Fabric script distributes an archive to your web servers."""
from fabric.api import *
from fabric.contrib import files
import os
from os.path import exists
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
    """Function for deploy"""
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    name = tmp.split('/')[1]
    dest = data_path + name

    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(dest))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(name, dest))
        run('sudo rm -f /tmp/{}.tgz'.format(name))
        run('sudo mv {}/web_static/* {}/'.format(dest, dest))
        run('sudo rm -rf {}/web_static'.format(dest))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(dest))
        return True
    except SpecificException as e:
        return False


def deploy():
    """ creates & distributes archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
