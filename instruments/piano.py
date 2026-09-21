NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Équivalences bémols / dièses
ENHARMONICS = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#',
}

# Intervalles (demi-tons) et doigtés selon la main
INTERVALS = {
    '': {
        'semitones': [0, 4, 7],
        'MD': [1, 3, 5],      # Pouce, Majeur, Auriculaire
        'MG': [5, 3, 1],      # Auriculaire, Majeur, Pouce
    },
    'm': {
        'semitones': [0, 3, 7],
        'MD': [1, 3, 5],
        'MG': [5, 3, 1],
    },
    '7': {
        'semitones': [0, 4, 7, 10],
        'MD': [1, 2, 3, 5],   # Pouce, Index, Majeur, Auriculaire
        'MG': [5, 3, 2, 1],   # Auriculaire, Majeur, Index, Pouce
    },
    'm7': {
        'semitones': [0, 3, 7, 10],
        'MD': [1, 2, 3, 5],
        'MG': [5, 3, 2, 1],
    },
    'maj7': {
        'semitones': [0, 4, 7, 11],
        'MD': [1, 2, 3, 5],
        'MG': [5, 3, 2, 1],
    },
}

# Génération exhaustive de toutes les notes et doigtés pour chaque accord
PIANO_CHORDS = {}
CHORD_FINGERS = {}

for root_idx, root in enumerate(NOTES):
    for quality, data in INTERVALS.items():
        chord_key = f"{root}{quality}"
        PIANO_CHORDS[chord_key] = [NOTES[(root_idx + s) % 12] for s in data['semitones']]
        CHORD_FINGERS[(chord_key, 'MD')] = data['MD']
        CHORD_FINGERS[(chord_key, 'MG')] = data['MG']

def normalize_chord_name(chord_str: str) -> str:
    """Traduit les bémols en dièses et sépare tonique/qualité."""
    if not chord_str or chord_str == "N.C.":
        return "N.C."
    for flat, sharp in ENHARMONICS.items():
        if chord_str.startswith(flat):
            chord_str = chord_str.replace(flat, sharp, 1)
            break
    return chord_str

def get_key_position(semitone_abs: int):
    """Calcule les coordonnées X/Y exactes pour un clavier 2 octaves (0 à 23)."""
    octave = semitone_abs // 12
    semi = semitone_abs % 12
    w_width = 14
    bw_width = 9

    white_indices = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}
    black_slots = {1: 1, 3: 2, 6: 4, 8: 5, 10: 6}

    if semi in white_indices:
        x = (octave * 7 + white_indices[semi]) * w_width
        return False, x, x + (w_width / 2), 48
    else:
        x = (octave * 7 + black_slots[semi]) * w_width - (bw_width / 2)
        return True, x, x + (bw_width / 2), 26

def generate_piano_svg(chord_name: str, hand: str = 'MD', max_width: int = 210) -> str:
    """Génère un clavier 2 octaves en SVG avec pastilles numérotées par doigt."""
    norm_name = normalize_chord_name(chord_name)
    if norm_name not in PIANO_CHORDS:
        return ""

    root = norm_name[:2] if len(norm_name) > 1 and norm_name[1] == '#' else norm_name[0]
    quality = norm_name[2:] if len(norm_name) > 1 and norm_name[1] == '#' else norm_name[1:]
    
    if root not in NOTES:
        return ""
    root_idx = NOTES.index(root)

    cfg = INTERVALS.get(quality, INTERVALS[''])
    semitones = cfg['semitones']
    fingers = cfg[hand]

    active_semitones = [root_idx + s for s in semitones]
    finger_map = {root_idx + s: fingers[i] for i, s in enumerate(semitones)}

    w_width, w_height = 14, 60
    b_width, b_height = 9, 36
    total_width = 14 * w_width  # 196px

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} 72" style="max-width:{max_width}px; width:100%; height:auto; display:block; margin:auto;">']

    # Badge de main (MD ou MG)
    hand_badge_color = "#2196F3" if hand == "MD" else "#FF9800"
    svg.append(f'<text x="6" y="10" font-size="9" fill="{hand_badge_color}" font-family="sans-serif" font-weight="bold">{hand}</text>')

    # 1. Dessin des 14 touches blanches
    for k in range(14):
        oct_k = k // 7
        semi_k = [0, 2, 4, 5, 7, 9, 11][k % 7]
        s_abs = oct_k * 12 + semi_k
        is_active = s_abs in active_semitones
        fill = "#4CAF50" if is_active else "#ffffff"
        svg.append(f'<rect x="{k * w_width}" y="12" width="{w_width}" height="{w_height}" fill="{fill}" stroke="#333" stroke-width="0.8" rx="1"/>')

    # 2. Dessin des 10 touches noires
    for oct_idx in (0, 1):
        for semi_val, slot in [(1, 1), (3, 2), (6, 4), (8, 5), (10, 6)]:
            s_abs = oct_idx * 12 + semi_val
            x = (oct_idx * 7 + slot) * w_width - (b_width / 2)
            is_active = s_abs in active_semitones
            fill = "#2E7D32" if is_active else "#181818"
            svg.append(f'<rect x="{x}" y="12" width="{b_width}" height="{b_height}" fill="{fill}" stroke="#000" stroke-width="0.8" rx="1"/>')

    # 3. Pastilles jaunes avec numérotation des doigts (1, 2, 3, 5)
    for s_abs in active_semitones:
        _, _, cx, cy = get_key_position(s_abs)
        f_num = finger_map[s_abs]
        # Décalage de 12px vers le bas pour compenser le header
        cy_adj = cy + 12
        svg.append(f'<circle cx="{cx}" cy="{cy_adj}" r="4.8" fill="#FFEB3B" stroke="#000" stroke-width="0.8"/>')
        svg.append(f'<text x="{cx}" y="{cy_adj + 3.2}" font-size="8" font-family="sans-serif" font-weight="bold" fill="#000" text-anchor="middle">{f_num}</text>')

    svg.append('</svg>')
    return "".join(svg)