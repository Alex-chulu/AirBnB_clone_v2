#!/usr/bin/env bash

from fabric.api import env, put, run, sudo
import os.path

env.hosts = ['35.153.78.21', '54.172.82.247']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'

def do_deploy(versions/web_static.tgz):
    """Distribute an archive to web servers."""
    if not os.path.exists(versions/web_static.tgz):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(versions/web_static.tgz, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/<archive 
	# filename without extension> on the web server
        filename = os.path.basename(versions/web_static.tgz)
        directory = "/data/web_static/releases/" + filename.split(".")[0]
        sudo("mkdir -p {}".format(directory))
        sudo("tar -xzf /tmp/{} -C {} --strip-components 1".format(filename, directory))

        # Delete the archive from the web server
        sudo("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current from the web server
        sudo("rm -f /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server, 
	# linked to the new version of your code
        sudo("ln -s {} /data/web_static/current".format(directory))

        # Return True if successful
        return True
    except:
        # Return False if unsuccessful
        return False

