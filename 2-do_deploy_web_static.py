#!/usr/bin/env bash

from datetime import datetime
from fabric.api import env, put, run
import os

# Update the env.hosts list with the IP addresses of the web servers
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path to SSH private key>'

def do_pack():
    """Creates a compressed archive of the web_static folder"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(timestamp)
        local('mkdir -p versions')
        local('tar -czvf {} web_static'.format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        filename = os.path.basename(archive_path)
        foldername = '/data/web_static/releases/' + filename[:-4]
        run('mkdir -p {}'.format(foldername))
        run('tar -xzf /tmp/{} -C {}'.format(filename, foldername))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Move files from /data/web_static/releases/<archive filename without extension>/web_static/ to /data/web_static/releases/<archive filename without extension>/
        run('mv {}/web_static/* {}'.format
