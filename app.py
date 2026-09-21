import streamlit as st
import os
import tempfile

from core.audio import download_youtube_audio, get_base64_audio
from core.harmony import analyze_track, transpose_chord
from core.separation import separate_tracks
from core.transcription import transcribe_notes

from instruments.guitar import FINGERINGS, generate_chord_svg, build_guitar_tab
from instruments.piano import PIANO_CHORDS, CHORD_FINGERS, generate_piano_svg, normalize_chord_name

from ui.widgets import render_pro_player, render_tuner, render_metronome

st.set_page_config(page_title="MovicH Studio", page_icon="𐠂", layout="wide")

# ==============================================================================
# INJECTION DU DESIGN RHEMA (CSS GLOBAL)
# ==============================================================================
RHEMA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

:root {
    --bg: #0b0b0c;
    --panel: #131315;
    --panel2: #18181b;
    --line: #29292e;
    --text: #f4f1ea;
    --muted: #9b9891;
    --gold: #c8a96b;
    --green: #8ea98a;
    --danger: #b87979;
}

/* Fond général et typographie de base */
.stApp {
    background: radial-gradient(circle at 75% -10%, #252017 0%, #0b0b0c 42%) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Titres en sérif éditoriale */
h1, h2, h3, .serif-title {
    font-family: 'Libre Baskerville', serif !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    letter-spacing: -0.02em;
}

p, span, label, div {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0e0e10 !important;
    border-right: 1px solid var(--line) !important;
}

/* Cartes & Panels */
.rhema-card {
    background: linear-gradient(145deg, #151517, #101012);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 24px;
    transition: border-color 0.2s ease;
}
.rhema-card:hover {
    border-color: #403621;
}

/* Eyebrows / micro-titres dorés */
.eyebrow {
    color: var(--gold);
    text-transform: uppercase;
    letter-spacing: 0.22em;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
    display: block;
}

/* Boutons Streamlit stylisés */
button[kind="primary"] {
    background-color: var(--gold) !important;
    color: #14120f !important;
    border: 0 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 10px 20px !important;
    transition: opacity 0.2s !important;
}
button[kind="primary"]:hover {
    opacity: 0.88 !important;
}

button[kind="secondary"] {
    background: transparent !important;
    color: var(--text) !important;
    border: 1px solid var(--line) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
button[kind="secondary"]:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

/* Entrées texte & selects */
input, textarea, [data-baseweb="select"] {
    background-color: #0d0d0f !important;
    border: 1px solid var(--line) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: var(--gold) !important;
}

/* Onglets */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    border-bottom: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 16px !important;
    font-size: 13px !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}

/* Métriques */
[data-testid="stMetricValue"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--gold) !important;
    font-weight: 600 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    font-size: 11px !important;
}
</style>
"""
st.markdown(RHEMA_CSS, unsafe_allow_html=True)

if "selected_instrument" not in st.session_state:
    st.session_state["selected_instrument"] = None

# ==============================================================================
# ÉCRAN D'ACCUEIL : CHOIX DE L'INSTRUMENT (STYLE RHEMA)
# ==============================================================================
if st.session_state["selected_instrument"] is None:
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #29292e; padding-bottom:18px; margin-bottom:42px;">
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="width:38px; height:38px; border:1px solid #c8a96b; border-radius:50%; display:grid; place-items:center; font-family:'Libre Baskerville',serif; color:#c8a96b; font-size:18px;">M</div>
                <div>
                    <strong style="letter-spacing:0.18em; font-size:14px;">MOVICH</strong>
                    <small style="display:block; color:#9b9891; letter-spacing:0.12em; font-size:10px; margin-top:2px;">STUDIO HARMONIQUE · ANALYSE & ÉCOUTE</small>
                </div>
            </div>
            <div style="display:flex; gap:8px;">
                <span style="width:7px; height:7px; border-radius:50%; background:#c8a96b; box-shadow:0 0 8px #c8a96b88;"></span>
                <span style="width:7px; height:7px; border-radius:50%; background:#3a3938;"></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<span class="eyebrow">01 · Sas d’entrée</span>', unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 46px; margin-bottom: 12px;'>Comprendre l’harmonie.<br>L’exécuter simplement.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9b9891; max-width: 660px; line-height: 1.6; font-size: 16px; margin-bottom: 36px;'>Sélectionne ton environnement de travail. La détection spectrale et les diagrammes d’accords s’ajusteront à la biomécanique de ton instrument.</p>", unsafe_allow_html=True)

    col_guit, col_piano = st.columns(2)

    with col_guit:
        st.markdown(
            """
            <div class="rhema-card">
                <span class="eyebrow">Option 01</span>
                <h2 style="font-size: 26px; margin: 0 0 10px 0;">Guitare acoustique & électrique</h2>
                <p style="color: #9b9891; font-size: 14px; line-height: 1.6; margin-bottom: 22px;">
                    Positions simplifiées sans barrés, calcul dynamique du capodastre idéal,
                    schémas de balayage au médiator et tablatures horizontales.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Configurer pour Guitare ➔", use_container_width=True, type="primary"):
            st.session_state["selected_instrument"] = "Guitare"
            st.rerun()

    with col_piano:
        st.markdown(
            """
            <div class="rhema-card">
                <span class="eyebrow">Option 02</span>
                <h2 style="font-size: 26px; margin: 0 0 10px 0;">Piano & Clavier</h2>
                <p style="color: #9b9891; font-size: 14px; line-height: 1.6; margin-bottom: 22px;">
                    Claviers panoramiques 2 octaves, pastilles de doigtés numérotées (1 à 5)
                    et dissociation rigoureuse Main Droite (accords) / Main Gauche (fondamentales).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button("Configurer pour Piano ➔", use_container_width=True, type="secondary"):
            st.session_state["selected_instrument"] = "Piano"
            st.rerun()

    st.stop()

# ==============================================================================
# ESPACE DE TRAVAIL
# ==============================================================================
instrument_choice = st.session_state["selected_instrument"]

# Header de travail
st.sidebar.markdown(
    f"""
    <div style="padding-bottom: 14px; border-bottom: 1px solid #29292e; margin-bottom: 18px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:28px; height:28px; border:1px solid #c8a96b; border-radius:50%; display:grid; place-items:center; font-family:'Libre Baskerville',serif; color:#c8a96b; font-size:13px;">M</div>
            <div>
                <strong style="letter-spacing:0.12em; font-size:12px; color:#f4f1ea;">MOVICH</strong>
                <small style="display:block; color:#c8a96b; font-size:10px; letter-spacing:0.08em;">{instrument_choice.upper()}</small>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("← Changer d’instrument", type="secondary"):
    st.session_state["selected_instrument"] = None
    st.rerun()

st.sidebar.write("")
page = st.sidebar.radio(
    "Navigation :",
    ["Studio d'Analyse", "Accordeur", "Métronome", "Dictionnaire d'Accords"]
)

# ==============================================================================
# MODULE 1 : STUDIO D'ANALYSE
# ==============================================================================
if page == "Studio d'Analyse":
    st.markdown(f'<span class="eyebrow">Espace d’entraînement · {instrument_choice}</span>', unsafe_allow_html=True)
    st.markdown("<h1>Décomposition & Harmonie</h1>", unsafe_allow_html=True)

    t_yt, t_file = st.tabs(["Lien YouTube", "Fichier audio local"])
    with t_yt:
        yt_url = st.text_input("URL de la source vidéo ou audio :", placeholder="https://www.youtube.com/watch?v=...")
        if yt_url and st.button("Extraire la source audio", type="primary"):
            with st.spinner("Extraction du signal audio en cours…"):
                try:
                    path, title = download_youtube_audio(yt_url)
                    st.session_state["audio_path"] = path
                    st.session_state["track_title"] = title
                    st.session_state["stems"] = None
                    st.session_state["analysis_data"] = None
                except Exception as e:
                    st.error(f"Erreur d’extraction : {e}")

    with t_file:
        up = st.file_uploader("Fichier non compressé ou masterisé (MP3, WAV, M4A) :", type=["mp3", "wav", "m4a"])
        if up is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(up.name)[1]) as tmp:
                tmp.write(up.read())
                st.session_state["audio_path"] = tmp.name
                st.session_state["track_title"] = up.name
                st.session_state["stems"] = None
                st.session_state["analysis_data"] = None

    curr_audio = st.session_state.get("audio_path")
    curr_title = st.session_state.get("track_title")

    if curr_audio and os.path.exists(curr_audio):
        st.write("")
        st.markdown(
            f"""
            <div class="rhema-card" style="margin-bottom:20px; padding:18px 22px;">
                <span class="eyebrow">Morceau chargé</span>
                <div style="font-family:'Libre Baskerville',serif; font-size:20px; color:#f4f1ea;">{curr_title}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Isolation des 6 pistes (Demucs)", expanded=False):
            if st.button("Lancer la séparation multitrack", type="secondary"):
                with st.spinner("Calcul des tiges audio via Apple Silicon…"):
                    try:
                        st.session_state["stems"] = separate_tracks(curr_audio)
                        st.success("Tiges audio séparées prêtes.")
                    except Exception as err:
                        st.error(f"Erreur de séparation : {err}")

            if st.session_state.get("stems"):
                cols = st.columns(3)
                for i, (name, path) in enumerate(st.session_state["stems"].items()):
                    with cols[i % 3]:
                        st.markdown(f"**{name}**")
                        st.audio(path)

        target_audio = curr_audio
        stem_instrument = "Guitare 🎸" if instrument_choice == "Guitare" else "Piano 🎹"
        if st.session_state.get("stems") and stem_instrument in st.session_state["stems"]:
            src = st.radio("Signal analysé :", ["Mix consolidé", f"{stem_instrument} isolée"], horizontal=True)
            if src == f"{stem_instrument} isolée":
                target_audio = st.session_state["stems"][stem_instrument]

        if st.button("Calculer la grille harmonique", type="primary"):
            with st.spinner("Calcul des chromatismes et segmentation temporelle…"):
                st.session_state["analysis_data"] = analyze_track(target_audio)

        data = st.session_state.get("analysis_data")
        if data:
            bpm = data["bpm"]
            duration = data["duration"]
            bars_data = data["bars_data"]
            best_capo = data["best_capo"]
            total_bars = len(bars_data)

            st.write("")
            c1, c2, c3 = st.columns(3)
            c1.metric("Pulsation", f"{bpm:.1f} BPM")
            c2.metric("Durée totale", f"{int(duration // 60)}m {int(duration % 60):02d}s")
            c3.metric("Mesures (4/4)", f"{total_bars}")

            # Lecteur d'entraînement
            st.write("")
            st.markdown('<span class="eyebrow">Lecteur de travail</span>', unsafe_allow_html=True)
            cl1, cl2 = st.columns(2)
            with cl1:
                loop_start = st.number_input("Début de la boucle :", min_value=1, max_value=total_bars, value=1)
            with cl2:
                loop_end = st.number_input("Fin de la boucle :", min_value=1, max_value=total_bars, value=min(4, total_bars))

            start_s = bars_data[loop_start - 1][0]
            end_s = bars_data[loop_end - 1][0] + (4 * (60.0 / bpm))
            render_pro_player(get_base64_audio(target_audio), start_s, end_s, loop_start, loop_end)

            # Guitare seule : Rythmiques & Riffs
            if instrument_choice == "Guitare":
                st.write("")
                st.markdown('<span class="eyebrow">Métrique & Balayage</span>', unsafe_allow_html=True)
                t_strum, t_arp = st.tabs(["Rythmique au médiator", "Arpège aux doigts"])

                with t_strum:
                    if bpm < 75:
                        st.markdown("**Balayage lent :** `1 & 2 & 3 & 4 &` — Mouvement : `⬇️ ⬇️ ⬆️ ⬇️ ⬆️`")
                    elif 75 <= bpm <= 115:
                        st.markdown("**Formule universelle :** `⬇️ ⬇️ ⬆️ ⬆️ ⬇️ ⬆️` *(Bas… Bas-Haut… Haut-Bas-Haut)*")
                    else:
                        st.markdown("**Balayage énergique :** `⬇️ ⬆️ ⬇️ ⬆️ ⬇️ ⬆️ ⬇️ ⬆️`")

                with t_arp:
                    vue = st.toggle("Inverser la tablature (Vue plongeante)", value=False)
                    if not vue:
                        st.code("e|------------(a)-----------|\nB|--------(m)-----(m)-------|\nG|----(i)-------------(i)---|\nD|--------------------------|\nA|--(P)---------------------|\nE|--------------------------|", language="text")
                    else:
                        st.code("E|--------------------------|\nA|--(P)---------------------|\nD|--------------------------|\nG|----(i)-------------(i)---|\nB|--------(m)-----(m)-------|\ne|------------(a)-----------|", language="text")

                with st.expander("Tablature du thème (Basic Pitch)", expanded=False):
                    if st.button("Transcrire le riff", type="secondary"):
                        with st.spinner("Extraction des hauteurs fondamentales…"):
                            raw_notes = transcribe_notes(target_audio)
                            tab_res = build_guitar_tab(raw_notes)
                            st.code(tab_res, language="text")

            # Grille d'accords
            st.write("")
            st.markdown(f'<span class="eyebrow">Partition · {instrument_choice}</span>', unsafe_allow_html=True)

            capo = 0
            hand_code = "MD"
            if instrument_choice == "Guitare":
                cc1, cc2 = st.columns([2, 3])
                with cc1:
                    capo = st.slider("Position du Capodastre :", 0, 7, best_capo)
                with cc2:
                    if best_capo > 0:
                        st.markdown(f"<div style='margin-top:20px; font-size:13px; color:#c8a96b;'>Capodastre en <b>case {best_capo}</b> recommandé pour éliminer les tensions musculaires.</div>", unsafe_allow_html=True)
            else:
                h_choice = st.radio(
                    "Main de référence :",
                    ["Main Droite (MD) · Accords", "Main Gauche (MG) · Fondamentales"],
                    horizontal=True
                )
                hand_code = "MD" if "Main Droite" in h_choice else "MG"

            cols_per_row = 4
            for r in range(0, len(bars_data), cols_per_row):
                cols = st.columns(cols_per_row)
                for c_idx, item in enumerate(bars_data[r:r + cols_per_row]):
                    b_num = r + c_idx + 1
                    t_s, _, dom = item
                    trans_dom = transpose_chord(dom, capo)

                    if instrument_choice == "Guitare":
                        f_info = FINGERINGS.get(trans_dom, {'tab': 'Position libre'})
                        diagram_svg = generate_chord_svg(f_info['tab'], max_width=95)
                        sub_text = f_info['tab']
                    else:
                        norm_chord = normalize_chord_name(trans_dom)
                        diagram_svg = generate_piano_svg(norm_chord, hand=hand_code, max_width=135)
                        notes = PIANO_CHORDS.get(norm_chord, [])
                        fingers = CHORD_FINGERS.get((norm_chord, hand_code), [])
                        sub_text = " · ".join([f"{n} ({f})" for n, f in zip(notes, fingers)]) if notes else "—"

                    is_in_loop = (loop_start <= b_num <= loop_end)
                    b_border = "1px solid #c8a96b" if is_in_loop else "1px solid #29292e"
                    b_bg = "#181612" if is_in_loop else "linear-gradient(145deg, #151517, #101012)"

                    with cols[c_idx]:
                        st.markdown(
                            f"""
                            <div style="border: {b_border}; border-radius: 12px; padding: 12px; margin-bottom: 14px; text-align: center; background: {b_bg};">
                                <span style="font-size: 10px; color: #9b9891; letter-spacing: 0.12em; text-transform: uppercase;">Mesure {b_num} · {int(t_s)}s</span>
                                <div style="font-family:'Libre Baskerville',serif; font-size: 22px; color: #f4f1ea; margin: 4px 0 2px 0;">{trans_dom}</div>
                                <div style="margin: 8px 0;">{diagram_svg}</div>
                                <div style="font-size: 11px; background: #0b0b0c; border: 1px solid #29292e; border-radius: 6px; padding: 4px 6px; color: #c8a96b; font-family: monospace;">{sub_text}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# ==============================================================================
# MODULE 2 : ACCORDEUR
# ==============================================================================
elif page == "Accordeur":
    st.markdown('<span class="eyebrow">Calibrage tonal</span>', unsafe_allow_html=True)
    st.markdown("<h1>Accordeur Chromatique</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9b9891; margin-bottom:28px;'>Vérifie la justesse de chaque corde à vide avant le début du travail harmonique.</p>", unsafe_allow_html=True)
    render_tuner()

# ==============================================================================
# MODULE 3 : MÉTRONOME
# ==============================================================================
elif page == "Métronome":
    st.markdown('<span class="eyebrow">Régularité temporelle</span>', unsafe_allow_html=True)
    st.markdown("<h1>Métronome de Précision</h1>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        bpm_val = st.slider("Pulsation (BPM) :", 40, 220, 90, 1)
    with col_m2:
        beats_val = st.selectbox("Métrique :", [4, 3, 2, 6], index=0)
    render_metronome(bpm_val, beats_val)

# ==============================================================================
# MODULE 4 : GUIDE D'ACCORDS
# ==============================================================================
elif page == "Dictionnaire d'Accords":
    st.markdown(f'<span class="eyebrow">Répertoire morphologique · {instrument_choice}</span>', unsafe_allow_html=True)
    st.markdown("<h1>Formes Fondamentales</h1>", unsafe_allow_html=True)

    if instrument_choice == "Guitare":
        chord_list = list(FINGERINGS.keys())
        sel_chord = st.selectbox("Sélectionne un accord :", chord_list, index=0)
        c_info1, c_info2 = st.columns([1, 2])
        with c_info1:
            c_data = FINGERINGS[sel_chord]
            diagram = generate_chord_svg(c_data['tab'], max_width=140)
            st.markdown(
                f"""
                <div class="rhema-card" style="text-align:center;">
                    <div style="font-family:'Libre Baskerville',serif; font-size:36px; color:#f4f1ea;">{sel_chord}</div>
                    <div style="margin: 12px 0;">{diagram}</div>
                    <div style="font-size: 13px; font-family: monospace; background: #0b0b0c; border: 1px solid #29292e; color: #c8a96b; padding: 6px; border-radius: 6px;">{c_data['tab']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_info2:
            st.markdown(
                f"""
                <div class="rhema-card">
                    <span class="eyebrow">Détails d’exécution</span>
                    <p><b>Placement :</b> {FINGERINGS[sel_chord]['fingers']}</p>
                    <p><b>Basse :</b> {FINGERINGS[sel_chord]['bass']}</p>
                    <p style="font-size:12px; color:#9b9891; margin:0;">✕ = corde étouffée · ○ = corde à vide · ● = point d’appui</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        chord_list = sorted(list(set([k[0] for k in CHORD_FINGERS.keys()])))
        sel_chord = st.selectbox("Sélectionne un accord :", chord_list, index=0)
        h_choice = st.radio("Main active :", ["Main Droite (MD)", "Main Gauche (MG)"], horizontal=True)
        hand_code = "MD" if "Main Droite" in h_choice else "MG"

        c_info1, c_info2 = st.columns([1, 2])
        with c_info1:
            diagram = generate_piano_svg(sel_chord, hand=hand_code, max_width=180)
            notes_arr = PIANO_CHORDS.get(sel_chord, [])
            fingers_arr = CHORD_FINGERS.get((sel_chord, hand_code), [])
            notes_str = " · ".join([f"{n} ({f})" for n, f in zip(notes_arr, fingers_arr)])
            st.markdown(
                f"""
                <div class="rhema-card" style="text-align:center;">
                    <div style="font-family:'Libre Baskerville',serif; font-size:36px; color:#f4f1ea;">{sel_chord}</div>
                    <div style="margin: 14px 0;">{diagram}</div>
                    <div style="font-size: 13px; font-family: monospace; background: #0b0b0c; border: 1px solid #29292e; color: #c8a96b; padding: 6px; border-radius: 6px;">{notes_str}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c_info2:
            st.markdown(
                f"""
                <div class="rhema-card">
                    <span class="eyebrow">Structure harmonique</span>
                    <p><b>Notes constitutives :</b> {', '.join(PIANO_CHORDS.get(sel_chord, []))}</p>
                    <p><b>Doigts :</b> 1 (Pouce), 2 (Index), 3 (Majeur), 5 (Auriculaire).</p>
                    <p style="font-size:12px; color:#9b9891; margin:0;">MD : le pouce prend la note grave · MG : l’auriculaire prend la note grave.</p>
                </div>
                """,
                unsafe_allow_html=True
            )