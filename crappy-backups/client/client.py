import os
import requests
from pathlib import Path
from datetime import datetime
import client_config as conf
import re
import sys

def download_latest_backup():
    Path(conf.LOCAL_BACKUP_DIR).mkdir(exist_ok=True)

    headers = {
        "Authorization": f"Bearer {conf.AUTH_TOKEN}"
    }

    url = f"{conf.BACKUP_SERVER}/backups/latest"
    print(f"Requesting latest backup from {url}...")

    with requests.get(url, headers=headers, stream=True) as response:
        if response.status_code != 200:
            print(f"Failed to download: {response.status_code} - {response.text}")
            return

        filename = extract_filename_from_headers(response.headers)
        if not filename:
            filename = f"backup_{datetime.now()}.zip"

        local_path = f"{conf.LOCAL_BACKUP_DIR}/{filename}"
        total_size = int(response.headers.get('Content-Length', 0))
        chunk_size = chunk_size = 65536 # Download in 8 KB chunks

        print(f"Downloading {filename} ({total_size / 1024 / 1024:.2f} MB) started at {datetime.now()}")

        bytes_downloaded = 0
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    show_progress(bytes_downloaded, total_size)

        print(f"\nDownloaded to {local_path} completed at {datetime.now()}")

    prune_old_backups()

def show_progress(downloaded, total):
    if total > 0:
        percent = downloaded / total * 100
        sys.stdout.write(f"\rProgress: {percent:6.2f}% ({downloaded / 1024 / 1024:.2f} MB / {total / 1024 / 1024:.2f} MB)")
    else:
        sys.stdout.write(f"\rProgress: {downloaded / 1024 / 1024:.2f} MB")
    sys.stdout.flush()

def extract_filename_from_headers(headers):
    content_disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', content_disposition)
    return match.group(1) if match else None


def prune_old_backups():
    files = sorted(Path(conf.LOCAL_BACKUP_DIR).glob("*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_file in files[conf.MAX_BACKUPS:]:
        print(f"Removing old backup: {old_file.name}")
        old_file.unlink()

if __name__ == '__main__':
    download_latest_backup()
