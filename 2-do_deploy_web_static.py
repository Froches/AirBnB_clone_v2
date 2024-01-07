#!/usr/bin/python3
from fabric import task
from fabric import Connection
from os.path import exists
import os


env.hosts = ['ubuntu@52.91.120.5', 'ubuntu@54.237.33.167']
env.key_filename = '~/.ssh/id_rsa'

@task
def do_deploy(c, archive_path):
    """
    deploys to server
    """
    # Check if the archive exists
    if not exists(archive_path):
        print(f"Archive '{archive_path}' does not exist.")
        return False

    # Upload the archive to /tmp/ directory on the server
    upload_result = c.put(archive_path, '/tmp/')
    if upload_result.failed:
        print("Failed to upload the archive.")
        return False

    # Extract the archive to /data/web_static/releases/<archive filename without extension>
    archive_filename = os.path.basename(archive_path)
    folder_name = archive_filename.replace('.tgz', '').split('_')[0]
    releases_path = f'/data/web_static/releases/{folder_name}'

    # Create the releases directory if it doesn't exist
    c.sudo(f"mkdir -p {releases_path}")

    # Uncompress the archive
    c.sudo(f"tar -xzf /tmp/{archive_filename} -C {releases_path}")

    # Delete the archive from the server
    c.sudo(f"rm /tmp/{archive_filename}")

    # Delete the symbolic link /data/web_static/current
    c.sudo("rm -rf /data/web_static/current")

    # Create a new symbolic link
    c.sudo(f"ln -s {releases_path} /data/web_static/current")

    print("Deployment successful.")
    return True
