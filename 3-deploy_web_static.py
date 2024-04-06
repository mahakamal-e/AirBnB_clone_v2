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
    """Function that used to deploy to web servers"""
    if not os.path.exists(archive_path):
        return False

    base_path = '/data/web_static/releases/'
    tmp = archive_path.split('.')[0]
    file_name = tmp.split('/')[1]
    deployment_dir = base_path + file_name

    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(deployment_dir))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(file_name,
                                                     deployment_dir))
        run('sudo rm -f /tmp/{}.tgz'.format(file_name))
        run('sudo mv {}/web_static/* {}/'.format(deployment_dir,
                                                 deployment_dir))
        run('sudo rm -rf {}/web_static'.format(deployment_dir))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(deployment_dir))
        return True
    except:
        return False

def deploy():
    """ creates & distributes archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
