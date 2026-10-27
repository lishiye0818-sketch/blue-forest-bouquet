"""Expand verified source archives when deployment files are uploaded in a browser."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import runpy
import sys
from zipfile import ZipFile


def file_digest(path):
    checksum = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def materialize_bundle(root):
    root = Path(root).resolve()
    manifest = json.loads((root / "bundle.json").read_text())
    destination = root / ".blueforest-app"
    marker = destination / ".source-sha256"
    identity = hashlib.sha256(json.dumps(manifest["archives"], sort_keys=True).encode()).hexdigest()
    if marker.is_file() and marker.read_text() == identity:
        return destination
    for name, expected in manifest["archives"].items():
        if Path(name).name != name or file_digest(root / name) != expected:
            raise ValueError("The uploaded application archive is incomplete or changed.")
        with ZipFile(root / name) as archive:
            for member in archive.infolist():
                path = PurePosixPath(member.filename)
                if path.is_absolute() or ".." in path.parts or "\\" in member.filename:
                    raise ValueError("Unsafe application archive path.")
    destination.mkdir(exist_ok=True)
    for name in manifest["archives"]:
        with ZipFile(root / name) as archive:
            archive.extractall(destination)
    marker.write_text(identity)
    return destination


if __name__ == "__main__":
    app = materialize_bundle(Path(__file__).resolve().parent)
    sys.path.insert(0, str(app))
    runpy.run_path(str(app / "streamlit_app.py"), run_name="__main__")
