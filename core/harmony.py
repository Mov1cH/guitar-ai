import librosa
import numpy as np
from core.constants import NOTES, CHORD_TEMPLATES, EASY_OPEN_CHORDS

def identify_chord(chroma_vector: np.ndarray) -> str:
    norm = np.linalg.norm(chroma_vector)
    if norm == 0:
        return "N.C."
    chroma_norm = chroma_vector / norm
    best_chord, best_score = "N.C.", -1.0
    for root_idx, root_name in enumerate(NOTES):
        for quality, template in CHORD_TEMPLATES.items():
            rolled = np.roll(template, root_idx)
            rolled /= np.linalg.norm(rolled)
            score = np.dot(chroma_norm, rolled)
            if score > best_score:
                best_score = score
                best_chord = f"{root_name}{quality}"
    return best_chord

def transpose_chord(chord_str: str, semitones: int) -> str:
    if chord_str == "N.C." or not chord_str:
        return chord_str
    if len(chord_str) > 1 and chord_str[1] == '#':
        root, quality = chord_str[:2], chord_str[2:]
    else:
        root, quality = chord_str[0], chord_str[1:]
    if root not in NOTES:
        return chord_str
    new_idx = (NOTES.index(root) - semitones) % 12
    return f"{NOTES[new_idx]}{quality}"

def find_best_capo(chords_list: list) -> int:
    """Calcule la frette de capodastre éliminant en priorité absolue les barrés."""
    best_capo = 0
    best_score = -9999

    for capo in range(8):
        score = 0
        for c in chords_list:
            transposed = transpose_chord(c, capo)
            if transposed in EASY_OPEN_CHORDS:
                score += 4  # Bonus fort pour les positions ouvertes standard (C, G, D, Am, Em...)
            elif '#' in transposed or 'b' in transposed:
                score -= 6  # Malus dissuasif pour toute frette laissant des barrés / dièses
            else:
                score -= 2  # Malus modéré pour accord non altéré mais avec barré (ex: F, Bm)

        if score > best_score:
            best_score = score
            best_capo = capo

    return best_capo

def analyze_track(audio_path: str):
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512)
    chroma_sync = librosa.util.sync(chroma, beat_frames, aggregate=np.median)

    raw_chords, bars_data, cur_bar = [], [], []
    for i in range(chroma_sync.shape[1]):
        c = identify_chord(chroma_sync[:, i])
        cur_bar.append(c)
        if len(cur_bar) == 4:
            t_sec = beat_times[i - 3] if (i - 3) >= 0 else 0.0
            dom = max(set(cur_bar), key=cur_bar.count)
            raw_chords.append(dom)
            bars_data.append((t_sec, cur_bar.copy(), dom))
            cur_bar = []

    best_capo = find_best_capo(raw_chords)
    return {
        "bpm": bpm,
        "duration": duration,
        "bars_data": bars_data,
        "raw_chords": raw_chords,
        "best_capo": best_capo
    }