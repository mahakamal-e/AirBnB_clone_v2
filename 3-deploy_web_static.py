#!/usr/bin/python3
"""A Fabric script distributes an archive to your web servers."""
from fabric.contrib import files
from fabric.api import *
from os.path import exists
from datetime import datetime
import os


env.user = 'ubuntu'
env.hosts = ['3.85.1.33', '100.26.171.116']


def do_pack():
    """Script that generates a .tgz from the contents of the web_static"""
    dir_name = "web_static_" + datetime.strftime(datetime.now(),
                                                 "%Y%m%d%H%M%S")
    archive_path = 'versions/{:s}.tgz'.format(dir_name)

    try:
        local('mkdir -p versions')
        local('tar -czvf {:s} web_static'.format(archive_path))
    except Exception:
        return None

    return archive_path


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
        run('sudo ln -sf {} /data/web_static/current'.format(dest))
        return True
    except SpecificException as e:
        return False


def deploy():
    """ creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
        result = do_deploy(new_archive_path)
        return result
