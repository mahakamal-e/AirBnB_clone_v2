#!/usr/bin/python3
"""creates and distributes
archive to my servers
"""
from os.path import exists
from datetime import datetime
from fabric.api import local, env, put, run

env.user = 'ubuntu'
env.hosts = ['54.237.101.225', '18.207.1.65']


def do_pack():
    """generates archive from folder"""
    try:
        fdate = datetime.now().strftime('%Y%m%d%H%M%S')
        fileN = f'web_static_{fdate}.tgz'
        local('mkdir -p versions')
        local(f'tar -cvzf versions/{fileN} web_static')
        return f'versions/{fileN}'
    except Exception:
        return None

def do_deploy(archive_path):
    """distribute archive
    to web servers
    """
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split('/')[-1]
        no_exten = file_name.split('.')[0]
        path = '/data/web_static/releases/'
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_exten))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_exten))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_exten))
        run('rm -rf {}{}/web_static'.format(path, no_exten))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_exten))
        return True
    except Exception:
        return False

def deploy():
    """creates and distributes an archive
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
