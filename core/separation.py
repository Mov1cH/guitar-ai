import sys
import subprocess
import tempfile
from pathlib import Path

def separate_tracks(audio_file_path: str) -> dict:
    output_dir = Path(tempfile.mkdtemp())
    cmd = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs_6s",
        "--mp3",
        "-o", str(output_dir),
        audio_file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Erreur de séparation Demucs : {res.stderr}")

    track_name = Path(audio_file_path).stem
    stems_dir = output_dir / "htdemucs_6s" / track_name
    stems = {
        "Guitare 🎸": stems_dir / "guitar.mp3",
        "Voix 🎤": stems_dir / "vocals.mp3",
        "Batterie 🥁": stems_dir / "drums.mp3",
        "Basse 🎸": stems_dir / "bass.mp3",
        "Piano 🎹": stems_dir / "piano.mp3",
        "Autre 🎶": stems_dir / "other.mp3",
    }
    return {k: str(v) for k, v in stems.items() if v.exists()}