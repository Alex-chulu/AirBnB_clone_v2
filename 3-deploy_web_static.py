#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import *
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['35.153.78.21', '54.172.82.247']

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""

    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path)
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""

    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        archive_filename = os.path.basename(archive_path)
        archive_foldername = os.path.splitext(archive_filename)[0]
        remote_path = "/data/web_static/releases/{}".format(archive_foldername)
        run("sudo mkdir -p {}".format(remote_path))
        run("sudo tar -xzf /tmp/{} -C {}".
            format(archive_filename, remote_path))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move the contents of the web_static folder up one level
        run("sudo mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("sudo rm -rf {}/web_static".format(remote_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("sudo rm -rf /data/web_static/current")

        # Create a new the symbolic link
        run("sudo ln -s {} /data/web_static/current".
            format(remote_path))

        return True
    except:
        return False

def deploy():
    """Creates and distributes an archive to the web servers"""

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

