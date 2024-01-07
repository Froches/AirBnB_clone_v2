from fabric.api import local
from datetime import datetime
import os

def do_pack():
    # Define the current date and time for the archive name
    now = datetime.utcnow()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Name of the archive
    archive_name = f"web_static_{timestamp}.tgz"
    archive_path = f"versions/{archive_name}"

    # Create the .tgz archive
    result = local(f"tar -cvzf {archive_path} web_static")

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return archive_path
