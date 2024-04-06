#!/usr/bin/python3
""" Deletes out-of-date archives, using the function do_clean. """
from fabric.api import *
import os


env.hosts = ['3.85.1.33', '100.26.171.116']


def do_clean(number=0):
    """clean up old versions"""
    try:
        number = int(number)
        if number < 0:
            return False
        if number == 0 or number == 1:
            number = 1
        local(f'cd versions; ls -t | tail -n +{number} | xargs rm -rf --')
        for host in env.hosts:
            env.host_string = host
            run(f'cd /data/web_static/releases; ls -t | tail -n +{number} | xargs rm -rf --')
        return True
    except Exception as e:
        return False
