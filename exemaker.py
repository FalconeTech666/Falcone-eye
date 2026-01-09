import PyInstaller.__main__
from pathlib import Path

SCRIPT_NAME = "falcone_eye.py"

base_dir = Path(__file__).resolve().parent
script_path = base_dir / SCRIPT_NAME

PyInstaller.__main__.run([
    str(script_path),
    "--onefile",
    "--name", "falcone_eye2.0",
    "--noconsole",
])