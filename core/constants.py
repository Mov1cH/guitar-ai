import numpy as np

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Profils spectraux (Chroma templates)
CHORD_TEMPLATES = {
    '': np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], dtype=float),       # Majeur
    'm': np.array([1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0], dtype=float),      # Mineur
    '7': np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0], dtype=float),      # 7e dominante
}

# Accords ouverts faciles pour débuter
EASY_OPEN_CHORDS = {'C', 'G', 'D', 'A', 'E', 'Am', 'Em', 'Dm', 'C7', 'G7', 'D7', 'A7', 'E7'}