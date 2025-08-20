import subprocess
import logging
import watchtower
import socket
import datetime
import os
import sys
from dotenv import load_dotenv

# ---------------------------
# Notes
# ---------------------------
# - require to set ENV below
#   - ENABLE_MONITOR_STORAGE=TRUE
#   - AWS_DEFAULT_REGION
#   - AWS_ACCESS_KEY_ID
#   - AWS_SECRET_ACCESS_KEY

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    watchtower.CloudWatchLogHandler(
        log_group='typesense_poc',
        stream_name="monitor_storage"
    )
)

if os.environ.get("ENABLE_MONITOR_STORAGE") != "TRUE":
    sys.exit(0)

def check_storage_usage():
    output = subprocess.check_output(['df', '-h']).decode('utf-8')
    lines = output.strip().split('\n')
    mount_points = {'/': 'N/A', '/app': 'N/A', '/data': 'N/A'}
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 6:
            mount = parts[-1]
            if mount in mount_points:
                mount_points[mount] = f"{parts[2]}/{parts[1]} ({parts[4]})"
    usage_str = " | ".join([f"{mnt}: {usage}" for mnt, usage in mount_points.items()])
    logger.info(f"Storage usage: {usage_str}")
    return usage_str

if __name__ == "__main__":
    check_storage_usage()
