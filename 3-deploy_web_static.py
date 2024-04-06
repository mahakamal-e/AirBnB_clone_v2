#!/usr/bin/python3
"""A Fabric script distributes an archive to your web servers."""
import os
from fabric.api import *


do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy


def deploy():
    """deploy an archive to web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
