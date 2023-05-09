from fabric.api import local
from datetime import datetime

def do_pack():
    """Create a compressed archive of the web_static folder."""
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")
    # Generate the timestamp string
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    # Create the archive filename
    archive_filename = "web_static_{}.tgz".format(timestamp)
    # Create the archive command
    archive_command = "tar -czvf versions/{} web_static".format(archive_filename)
    # Run the archive command
    result = local(archive_command)
    # Return the path to the archive if it was created successfully
    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_filename)
