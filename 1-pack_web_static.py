#!/usr/bin/python3
"""
Creates new archive
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Creates new archive from contents of the web static folder
    """

    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    if not os.path.exists("versions"):
        os.makedirs("versions")

    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"

    result = local(f"tar -cvzf {archive_path} web_static")

    if result.failed:
        return None
    else:
        return archive_path
