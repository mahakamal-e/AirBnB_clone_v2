#!/usr/bin/python3
""" Deletes out-of-date archives, using the function do_clean. """
from fabric.api import *
import os


env.user = "ubuntu"
env.hosts = ['3.85.1.33', '100.26.171.116']


def do_clean(number=0):
    """ Function that deletes out-of-date archives. """
    releases_path = '/data/web_static/releases'
    if number == '0':
        number = 2
    else:
        number = int(number) + 1

    local('cd versions; ls -t | tail -n +{} | xargs rm -rf'
          .format(number))
    run('cd {}; ls -t | tail -n +{} | sudo xargs rm -rf'
        .format(releases_path, number))
