import os
import requests
from pathlib import Path
from datetime import datetime
import client_config as conf
import re

def download_latest_backup():
    Path(conf.LOCAL_BACKUP_DIR).mkdir(exist_ok=True)

    headers = {
        "Authorization": f"Bearer {conf.AUTH_TOKEN}"
    }

    url = f"{conf.BACKUP_SERVER}/backups/latest"
    print(f"Requesting latest backup from {url}...")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        filename = extract_filename_from_headers(response.headers)
        if not filename:
            filename = f"backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"

        local_path = conf.LOCAL_BACKUP_DIR / filename

        with open(local_path, "wb") as f:
            print(f"Downloading {filename}, started at {datetime.now()}")
            f.write(response.content)
        print(f"Downloaded to {local_path} completed at {datetime.now()}")
    else:
        print(f"Failed to download: {response.status_code} - {response.text}")
        return

    prune_old_backups()

def extract_filename_from_headers(headers):
    content_disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="(.+?)"', content_disposition)
    return match.group(1) if match else None

def prune_old_backups():
    files = sorted(conf.LOCAL_BACKUP_DIR.glob("*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_file in files[conf.MAX_BACKUPS:]:
        print(f"Removing old backup: {old_file.name}")
        old_file.unlink()

if __name__ == '__main__':
    download_latest_backup()
