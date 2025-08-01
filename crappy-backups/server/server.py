from flask import Flask, request, send_file, abort
import os
import server_config as conf
from pathlib import Path

app = Flask(__name__)

@app.route("/backups/latest", methods=["GET"])
def download_latest_backup():
    token = request.headers.get("Authorization")
    if token != f"Bearer {conf.AUTH_TOKEN}":
        abort(401)

    backup_dir = Path(conf.BACKUP_DIR)
    if not backup_dir.exists() or not backup_dir.is_dir():
        abort(500, description="Backup directory does not exist.")

    zip_files = list(backup_dir.glob("*.zip"))
    if not zip_files:
        abort(404, description="No backup files found.")

    latest_file = max(zip_files, key=lambda f: f.stat().st_birthtime)

    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
