from fabric.api import local
from fabric import Connection
from os.path import exists
import os

env.hosts = ['330540-web-01', '330540-web-02']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_pack():
    """
    Creates a new archive from contents of the web_static folder
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


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """

    # Check if the archive exists
    if not exists(archive_path):
        print(f"Archive '{archive_path}' does not exist.")
        return False

    with Connection(env.hosts[0]) as conn:
        # Upload the archive to /tmp/ directory on the server
        upload_result = conn.put(archive_path, '/tmp/')
        if upload_result.failed:
            print("Failed to upload the archive.")
            return False

        # Extract the archive to /data/web_static/releases/<archive filename without extension>
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.replace('.tgz', '').split('_')[1]
        releases_path = f'/data/web_static/releases/{folder_name}'

        # Create the releases directory if it doesn't exist
        conn.sudo(f"mkdir -p {releases_path}")

        # Uncompress the archive
        conn.sudo(f"tar -xzf /tmp/{archive_filename} -C {releases_path}")

        # Delete the archive from the server
        conn.sudo(f"rm /tmp/{archive_filename}")

        # Delete the symbolic link /data/web_static/current
        conn.sudo("rm -rf /data/web_static/current")

        # Create a new symbolic link
        conn.sudo(f"ln -s {releases_path} /data/web_static/current")

    print("Deployment successful.")
    return True

