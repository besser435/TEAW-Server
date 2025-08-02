from flask import Flask, request, send_file, abort, Response
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

    latest_file = max(zip_files, key=lambda f: f.stat().st_ctime)
    # st_ctime shows as deprecated on win32, but works on Linux

    return send_file(
        latest_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name=os.path.basename(latest_file)
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
