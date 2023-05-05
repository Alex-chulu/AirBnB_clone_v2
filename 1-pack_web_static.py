#!/usr/bin/python3

from fabric.api import local
from datetime import datetime

def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    try:
        # Create a 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Create the filename with the current timestamp
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "web_static_{}.tgz".format(now)

        # Compress the contents of the 'web_static' folder
        local("tar -czvf versions/{} web_static".format(filename))

        # Return the archive path if successful
        return "versions/{}".format(filename)
    except:
        # Return None if unsuccessful
        return None
