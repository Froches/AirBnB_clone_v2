#!/usr/bin/python3
"""
Module documentation
"""
import Fabric



def do_deploy(archive_path):
    """
    Function documentation
    """

    if not exists "archive_path":
        return False

    # Upload the archive to the /tmp/ directory of the web server
    # Code goes here

    # Uncompress the archive to the folder
    # /data/web_static/releases/<archive filename without extension>
    # on the web server
    # Code goes here
