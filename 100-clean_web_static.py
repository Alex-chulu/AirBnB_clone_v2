#!/usr/bin/env bash

"""Fabric script to delete out-of-date archives."""

from fabric.api import *
from os import path

env.hosts = ['35.153.78.21', '54.172.82.247']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Deletes out-of-date archives."""
    if int(number) < 2:
        number = 1
    else:
        number = int(number)

    with lcd('./versions'):
        local('ls -1t | tail -n +{} | xargs rm -f'.format(number + 1))

    with cd('/data/web_static/releases'):
        run('ls -1t | tail -n +{} | xargs rm -rf'.format(number + 1))

