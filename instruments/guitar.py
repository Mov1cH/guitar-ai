GUITAR_STRINGS_MIDI = [
    (64, 'e'), (59, 'B'), (55, 'G'), (50, 'D'), (45, 'A'), (40, 'E'),
]

ENHARMONICS = {
    'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'
}

BASE_FINGERINGS = {
    # C / C#
    'C':   {'tab': 'x 3 2 0 1 0', 'desc': 'Do majeur (ouvert)', 'fingers': 'x, Annulaire(3), Majeur(2), à vide, Index(1), à vide', 'bass': 'Corde de La (5e)'},
    'Cm':  {'tab': 'x 3 5 5 4 3', 'desc': 'Do mineur (barré 3)', 'fingers': 'Index barré 3, Annulaire(5), Auriculaire(5), Majeur(4)', 'bass': 'Corde de La (5e)'},
    'C7':  {'tab': 'x 3 2 3 1 0', 'desc': 'Do 7e', 'fingers': 'x, Annulaire(3), Majeur(2), Auriculaire(3), Index(1), à vide', 'bass': 'Corde de La (5e)'},
    'C#':  {'tab': 'x 4 3 1 2 1', 'desc': 'Do dièse majeur (forme ouverte)', 'fingers': 'x, Annulaire(4), Majeur(3), Index(1), Auriculaire(2), Index(1)', 'bass': 'Corde de La (5e)'},
    'C#m': {'tab': 'x x 2 1 2 0', 'desc': 'Do dièse mineur (facile sans barré)', 'fingers': 'x, x, Annulaire(2), Index(1), Majeur(2), à vide', 'bass': 'Corde de Ré (4e)'},
    'C#7': {'tab': 'x 4 3 4 2 x', 'desc': 'Do dièse 7e (forme C7 décalée)', 'fingers': 'x, Annulaire(4), Majeur(3), Auriculaire(4), Index(2), x', 'bass': 'Corde de La (5e)'},

    # D / D#
    'D':   {'tab': 'x x 0 2 3 2', 'desc': 'Ré majeur (ouvert)', 'fingers': 'x, x, à vide, Index(2), Annulaire(3), Majeur(2)', 'bass': 'Corde de Ré (4e)'},
    'Dm':  {'tab': 'x x 0 2 3 1', 'desc': 'Ré mineur (ouvert)', 'fingers': 'x, x, à vide, Majeur(2), Annulaire(3), Index(1)', 'bass': 'Corde de Ré (4e)'},
    'D7':  {'tab': 'x x 0 2 1 2', 'desc': 'Ré 7e', 'fingers': 'x, x, à vide, Majeur(2), Index(1), Annulaire(2)', 'bass': 'Corde de Ré (4e)'},
    'D#':  {'tab': 'x x 5 3 4 3', 'desc': 'Ré dièse majeur (ouvert aigu)', 'fingers': 'x, x, Annulaire(5), Index(3), Majeur(4), Index(3)', 'bass': 'Corde de Ré (4e)'},
    'D#m': {'tab': 'x x 4 3 4 2', 'desc': 'Ré dièse mineur (sans barré)', 'fingers': 'x, x, Annulaire(4), Majeur(3), Auriculaire(4), Index(2)', 'bass': 'Corde de Ré (4e)'},
    'D#7': {'tab': 'x x 1 3 2 3', 'desc': 'Ré dièse 7e (forme ouverte)', 'fingers': 'x, x, Index(1), Annulaire(3), Majeur(2), Auriculaire(3)', 'bass': 'Corde de Ré (4e)'},

    # E
    'E':   {'tab': '0 2 2 1 0 0', 'desc': 'Mi majeur (ouvert)', 'fingers': 'à vide, Majeur(2), Annulaire(2), Index(1), à vide, à vide', 'bass': 'Corde de Mi grave (6e)'},
    'Em':  {'tab': '0 2 2 0 0 0', 'desc': 'Mi mineur (ouvert)', 'fingers': 'à vide, Majeur(2), Annulaire(2), à vide, à vide, à vide', 'bass': 'Corde de Mi grave (6e)'},
    'E7':  {'tab': '0 2 0 1 0 0', 'desc': 'Mi 7e', 'fingers': 'à vide, Majeur(2), à vide, Index(1), à vide, à vide', 'bass': 'Corde de Mi grave (6e)'},

    # F / F#
    'F':   {'tab': 'x x 3 2 1 1', 'desc': 'Fa majeur (forme débutant)', 'fingers': 'x, x, Annulaire(3), Majeur(2), Index sur cordes 1 et 2 en case 1', 'bass': 'Corde de Ré (4e)'},
    'Fm':  {'tab': 'x x 3 1 1 1', 'desc': 'Fa mineur (forme facile)', 'fingers': 'x, x, Annulaire(3), Index plat sur cordes 1-2-3 en case 1', 'bass': 'Corde de Ré (4e)'},
    'F7':  {'tab': '1 3 1 2 1 1', 'desc': 'Fa 7e', 'fingers': 'Index barré 1, Annulaire(3), Majeur(2)', 'bass': 'Corde de Mi grave (6e)'},
    'F#':  {'tab': 'x x 4 3 2 2', 'desc': 'Fa dièse majeur (forme débutant)', 'fingers': 'x, x, Annulaire(4), Majeur(3), Index plat case 2', 'bass': 'Corde de Ré (4e)'},
    'F#m': {'tab': 'x x 4 2 2 2', 'desc': 'Fa dièse mineur (sans barré)', 'fingers': 'x, x, Annulaire(4), Index plat sur cordes 1-2-3 en case 2', 'bass': 'Corde de Ré (4e)'},
    'F#7': {'tab': 'x x 4 3 2 0', 'desc': 'Fa dièse 7e (ouvert avec Mi aigu)', 'fingers': 'x, x, Annulaire(4), Majeur(3), Index(2), à vide', 'bass': 'Corde de Ré (4e)'},

    # G / G#
    'G':   {'tab': '3 2 0 0 3 3', 'desc': 'Sol majeur (ouvert)', 'fingers': 'Majeur(3), Index(2), à vide, à vide, Annulaire(3), Auriculaire(3)', 'bass': 'Corde de Mi grave (6e)'},
    'Gm':  {'tab': 'x x 5 3 3 3', 'desc': 'Sol mineur (sans grand barré)', 'fingers': 'x, x, Annulaire(5), Index plat sur cordes 1-2-3 en case 3', 'bass': 'Corde de Ré (4e)'},
    'G7':  {'tab': '3 2 0 0 0 1', 'desc': 'Sol 7e', 'fingers': 'Annulaire(3), Majeur(2), à vide, à vide, à vide, Index(1)', 'bass': 'Corde de Mi grave (6e)'},
    'G#':  {'tab': '4 6 6 5 4 4', 'desc': 'Sol dièse majeur', 'fingers': 'Index barré 4, Annulaire(6), Auriculaire(6), Majeur(5)', 'bass': 'Corde de Mi grave (6e)'},
    'G#m': {'tab': 'x x 6 4 4 4', 'desc': 'Sol dièse mineur (facile)', 'fingers': 'x, x, Annulaire(6), Index plat sur cordes 1-2-3 en case 4', 'bass': 'Corde de Ré (4e)'},
    'G#7': {'tab': 'x x 1 1 1 2', 'desc': 'Sol dièse 7e (ouvert début de manche)', 'fingers': 'x, x, Index plat sur cordes 2-3-4 en case 1, Majeur(2)', 'bass': 'Corde de Ré (4e)'},

    # A / A#
    'A':   {'tab': 'x 0 2 2 2 0', 'desc': 'La majeur (ouvert)', 'fingers': 'x, à vide, Index(2), Majeur(2), Annulaire(2), à vide', 'bass': 'Corde de La (5e)'},
    'Am':  {'tab': 'x 0 2 2 1 0', 'desc': 'La mineur (ouvert)', 'fingers': 'x, à vide, Majeur(2), Annulaire(2), Index(1), à vide', 'bass': 'Corde de La (5e)'},
    'A7':  {'tab': 'x 0 2 0 2 0', 'desc': 'La 7e', 'fingers': 'x, à vide, Majeur(2), à vide, Annulaire(2), à vide', 'bass': 'Corde de La (5e)'},
    'A#':  {'tab': 'x 1 3 3 3 x', 'desc': 'La dièse majeur (sans barré Mi aigu)', 'fingers': 'x, Index(1), Annulaire(3), Auriculaire(3), Majeur(3), x', 'bass': 'Corde de La (5e)'},
    'A#m': {'tab': 'x 1 3 3 2 1', 'desc': 'La dièse mineur', 'fingers': 'Index barré 1, Majeur(2), Annulaire(3), Auriculaire(3)', 'bass': 'Corde de La (5e)'},
    'A#7': {'tab': 'x 1 3 1 3 x', 'desc': 'La dièse 7e (forme ouverte simple)', 'fingers': 'x, Index(1), Annulaire(3), Index(1), Auriculaire(3), x', 'bass': 'Corde de La (5e)'},

    # B
    'B':   {'tab': 'x 2 4 4 4 x', 'desc': 'Si majeur (sans barré Mi aigu)', 'fingers': 'x, Index(2), Annulaire plat sur cordes 4-3-2 en case 4, x', 'bass': 'Corde de La (5e)'},
    'Bm':  {'tab': 'x 2 4 4 3 2', 'desc': 'Si mineur', 'fingers': 'Index barré 2, Majeur(3), Annulaire(4), Auriculaire(4)', 'bass': 'Corde de La (5e)'},
    'B7':  {'tab': 'x 2 1 2 0 2', 'desc': 'Si 7e (ouvert)', 'fingers': 'Majeur(2), Index(1), Annulaire(2), à vide, Auriculaire(2)', 'bass': 'Corde de La (5e)'},
}

# Duplication automatique pour les bémols équivalents (Bb, Eb, Ab...)
FINGERINGS = dict(BASE_FINGERINGS)
for flat_root, sharp_root in ENHARMONICS.items():
    for quality in ['', 'm', '7']:
        sharp_k = f"{sharp_root}{quality}"
        flat_k = f"{flat_root}{quality}"
        if sharp_k in BASE_FINGERINGS:
            entry = dict(BASE_FINGERINGS[sharp_k])
            entry['desc'] = entry['desc'].replace(sharp_root, flat_root)
            FINGERINGS[flat_k] = entry

def generate_chord_svg(tab_str: str, max_width: int = 110) -> str:
    if not tab_str or tab_str == "Position libre":
        return ""
    tokens = tab_str.split('(')[0].strip().split()
    if len(tokens) != 6:
        return ""

    num_frets = [int(t) for t in tokens if t.isdigit()]
    max_f = max(num_frets) if num_frets else 0
    min_f = min([f for f in num_frets if f > 0]) if any(f > 0 for f in num_frets) else 1

    base_fret = 1 if max_f <= 4 else min_f
    nb_frets = 4
    x_start, y_start = 25, 32
    x_spacing, y_spacing = 15, 18

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 125 125" style="max-width:{max_width}px; width:100%; height:auto; display:block; margin:auto;">']

    if base_fret > 1:
        svg.append(f'<text x="6" y="{y_start + 14}" font-size="10" fill="#FFEB3B" font-family="monospace" font-weight="bold">{base_fret}fr</text>')
        top_style = 'stroke="#777" stroke-width="1.5"'
    else:
        top_style = 'stroke="#ffffff" stroke-width="3.5"'

    svg.append(f'<line x1="{x_start}" y1="{y_start}" x2="{x_start + 5 * x_spacing}" y2="{y_start}" {top_style} />')

    for j in range(1, nb_frets + 1):
        y = y_start + j * y_spacing
        svg.append(f'<line x1="{x_start}" y1="{y}" x2="{x_start + 5 * x_spacing}" y2="{y}" stroke="#444" stroke-width="1.2" />')

    for i in range(6):
        x = x_start + i * x_spacing
        w = 2.0 - (i * 0.22)
        svg.append(f'<line x1="{x}" y1="{y_start}" x2="{x}" y2="{y_start + nb_frets * y_spacing}" stroke="#888" stroke-width="{w:.1f}" />')

    for i, token in enumerate(tokens):
        x = x_start + i * x_spacing
        if token.lower() == 'x':
            svg.append(f'<text x="{x}" y="{y_start - 7}" font-size="10" fill="#ff5252" font-family="sans-serif" text-anchor="middle" font-weight="bold">✕</text>')
        elif token == '0':
            svg.append(f'<circle cx="{x}" cy="{y_start - 10}" r="3.5" fill="none" stroke="#4CAF50" stroke-width="1.5" />')
        elif token.isdigit():
            rel_f = int(token) - base_fret + 1
            if 1 <= rel_f <= nb_frets:
                cy = y_start + (rel_f - 0.5) * y_spacing
                svg.append(f'<circle cx="{x}" cy="{cy}" r="5.2" fill="#4CAF50" stroke="#fff" stroke-width="1" />')

    svg.append('</svg>')
    return "".join(svg)

def midi_to_guitar_tab(midi_pitch: int):
    best = None
    for str_idx, (open_pitch, str_name) in enumerate(GUITAR_STRINGS_MIDI):
        fret = midi_pitch - open_pitch
        if 0 <= fret <= 15:
            if best is None or (fret < best[1]):
                best = (str_name, fret, str_idx)
    return best

def build_guitar_tab(raw_notes: list, max_notes: int = 28) -> str:
    strings = {'e': [], 'B': [], 'G': [], 'D': [], 'A': [], 'E': []}
    notes_mapped = []
    for start, end, pitch in raw_notes:
        pos = midi_to_guitar_tab(pitch)
        if pos:
            notes_mapped.append(pos)
        if len(notes_mapped) >= max_notes:
            break

    for str_name, fret, _ in notes_mapped:
        for s in strings:
            if s == str_name:
                strings[s].append(f"-{fret}-")
            else:
                strings[s].append("---")

    lines = [f"{s}|" + "".join(strings[s]) + "|" for s in ['e', 'B', 'G', 'D', 'A', 'E']]
    return "\n".join(lines)