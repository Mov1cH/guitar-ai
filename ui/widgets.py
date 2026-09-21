import streamlit.components.v1 as components

def render_pro_player(audio_b64: str, start_sec: float, end_sec: float, loop_start: int, loop_end: int):
    html = f"""
    <div style="background:linear-gradient(145deg, #151517, #101012); padding:20px; border-radius:14px; border:1px solid #29292e; margin-bottom:15px; font-family:'DM Sans', sans-serif;">
        <audio id="audioPro" src="data:audio/mp3;base64,{audio_b64}" controls preload="auto" style="width:100%; margin-bottom:14px; outline:none; filter: invert(0.9) hue-rotate(180deg);"></audio>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="font-size:11px; color:#9b9891; letter-spacing:0.12em; text-transform:uppercase; font-weight:700;">Vitesse</span>
                <button onclick="setRate(0.5)" class="pbtn">0.5×</button>
                <button onclick="setRate(0.75)" class="pbtn">0.75×</button>
                <button onclick="setRate(0.9)" class="pbtn">0.9×</button>
                <button onclick="setRate(1.0)" class="pbtn active" id="btn1">1.0×</button>
            </div>
            <div style="display:flex; gap:10px; align-items:center;">
                <label style="font-size:12px; color:#c8a96b; cursor:pointer; font-weight:600; letter-spacing:0.04em;">
                    <input type="checkbox" id="loopToggle" checked style="accent-color:#c8a96b;"> Boucle active (Mesures {loop_start} à {loop_end})
                </label>
            </div>
        </div>
    </div>
    <style>
        .pbtn {{ background:#0d0d0f; border:1px solid #29292e; color:#9b9891; border-radius:6px; padding:6px 14px; font-size:12px; cursor:pointer; font-weight:600; transition:0.2s; }}
        .pbtn:hover {{ border-color:#c8a96b; color:#f4f1ea; }}
        .pbtn.active {{ background:#c8a96b; border-color:#c8a96b; color:#14120f; font-weight:700; }}
    </style>
    <script>
        const aud = document.getElementById('audioPro');
        const loopToggle = document.getElementById('loopToggle');
        aud.addEventListener('timeupdate', () => {{
            if (loopToggle.checked) {{
                if (aud.currentTime < {start_sec} || aud.currentTime >= {end_sec}) {{
                    aud.currentTime = {start_sec};
                }}
            }}
        }});
        function setRate(rate) {{
            aud.playbackRate = rate;
            document.querySelectorAll('.pbtn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }}
    </script>
    """
    components.html(html, height=135)

def render_tuner():
    html = """
    <div style="display:flex; flex-direction:column; align-items:center; background:linear-gradient(145deg, #151517, #101012); border-radius:16px; border:1px solid #29292e; padding:32px; color:#f4f1ea; font-family:'DM Sans',sans-serif; max-width:440px; margin:auto;">
        <span style="color:#c8a96b; font-size:11px; text-transform:uppercase; letter-spacing:0.22em; font-weight:700;">Pitch continu</span>
        <div style="font-size:76px; font-weight:400; font-family:'Libre Baskerville',serif; color:#f4f1ea; margin:8px 0 2px 0;" id="noteDisplay">--</div>
        <div style="font-size:14px; color:#9b9891; font-family:monospace; margin-bottom:16px;" id="freqDisplay">0.0 Hz</div>
        <div style="width:100%; height:8px; background:#0d0d0f; border:1px solid #29292e; border-radius:4px; position:relative; margin:16px 0;">
            <div id="needle" style="width:4px; height:20px; background:#c8a96b; border-radius:2px; position:absolute; top:-6px; left:50%; transform:translateX(-50%); transition:left 0.08s ease;"></div>
        </div>
        <div style="font-size:13px; letter-spacing:0.08em; text-transform:uppercase; margin-top:8px; color:#9b9891;" id="statusText">Micro en attente</div>
        <button id="startTunerBtn" style="padding:12px 28px; font-size:13px; font-weight:700; border-radius:8px; border:none; cursor:pointer; background-color:#c8a96b; color:#14120f; margin-top:24px; letter-spacing:0.04em;">Activer le capteur</button>
    </div>
    <script>
        let audioCtx, analyser, micStream, isTuning = false;
        const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
        const noteDisplay = document.getElementById('noteDisplay');
        const freqDisplay = document.getElementById('freqDisplay');
        const needle = document.getElementById('needle');
        const statusText = document.getElementById('statusText');
        const btn = document.getElementById('startTunerBtn');

        function autoCorrelate(buf, sr) {
            let SIZE = buf.length, rms = 0;
            for (let i = 0; i < SIZE; i++) rms += buf[i] * buf[i];
            if (Math.sqrt(rms / SIZE) < 0.02) return -1;
            let r1 = 0, r2 = SIZE - 1, thres = 0.2;
            for (let i = 0; i < SIZE / 2; i++) { if (Math.abs(buf[i]) < thres) { r1 = i; break; } }
            for (let i = 1; i < SIZE / 2; i++) { if (Math.abs(buf[SIZE - i]) < thres) { r2 = SIZE - i; break; } }
            buf = buf.slice(r1, r2); SIZE = buf.length;
            let c = new Array(SIZE).fill(0);
            for (let i = 0; i < SIZE; i++) { for (let j = 0; j < SIZE - i; j++) { c[i] += buf[j] * buf[j + i]; } }
            let d = 0; while (c[d] > c[d + 1]) d++;
            let maxval = -1, maxpos = -1;
            for (let i = d; i < SIZE; i++) { if (c[i] > maxval) { maxval = c[i]; maxpos = i; } }
            return sr / maxpos;
        }

        function updatePitch() {
            if (!isTuning) return;
            const buffer = new Float32Array(2048);
            analyser.getFloatTimeDomainData(buffer);
            const pitch = autoCorrelate(buffer, audioCtx.sampleRate);
            if (pitch !== -1 && pitch > 60 && pitch < 500) {
                freqDisplay.textContent = pitch.toFixed(1) + " Hz";
                const noteNum = 12 * (Math.log(pitch / 440) / Math.log(2)) + 69;
                const rounded = Math.round(noteNum);
                const cents = Math.floor((noteNum - rounded) * 100);
                noteDisplay.textContent = notes[rounded % 12];
                needle.style.left = Math.min(Math.max(cents + 50, 0), 100) + "%";
                if (Math.abs(cents) < 6) {
                    statusText.textContent = "ACCORD PARFAIT"; statusText.style.color = "#8ea98a"; needle.style.background = "#8ea98a";
                } else if (cents < 0) {
                    statusText.textContent = "Trop bas"; statusText.style.color = "#c8a96b"; needle.style.background = "#c8a96b";
                } else {
                    statusText.textContent = "Trop haut"; statusText.style.color = "#b87979"; needle.style.background = "#b87979";
                }
            }
            requestAnimationFrame(updatePitch);
        }

        btn.onclick = async () => {
            if (!isTuning) {
                try {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    analyser = audioCtx.createAnalyser(); analyser.fftSize = 2048;
                    audioCtx.createMediaStreamSource(micStream).connect(analyser);
                    isTuning = true; btn.textContent = "Désactiver"; btn.style.backgroundColor = "transparent"; btn.style.border = "1px solid #29292e"; btn.style.color = "#f4f1ea";
                    statusText.textContent = "En écoute…"; updatePitch();
                } catch(e) { alert("Accès micro refusé."); }
            } else {
                isTuning = false; if (micStream) micStream.getTracks().forEach(t => t.stop());
                if (audioCtx) audioCtx.close();
                btn.textContent = "Activer le capteur"; btn.style.backgroundColor = "#c8a96b"; btn.style.border = "none"; btn.style.color = "#14120f";
                noteDisplay.textContent = "--"; freqDisplay.textContent = "0.0 Hz"; statusText.textContent = "Micro en attente";
            }
        };
    </script>
    """
    components.html(html, height=330)

def render_metronome(bpm: int, beats_per_bar: int):
    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; background:linear-gradient(145deg, #151517, #101012); border-radius:16px; border:1px solid #29292e; padding:24px; color:#f4f1ea; font-family:'DM Sans',sans-serif; max-width:440px; margin:auto;">
        <span style="color:#c8a96b; font-size:11px; text-transform:uppercase; letter-spacing:0.22em; font-weight:700;">Cadence ({beats_per_bar}/4)</span>
        <div style="display:flex; gap:10px; margin:22px 0;" id="dots"></div>
        <button id="toggleBtn" style="padding:12px 28px; font-size:13px; font-weight:700; border-radius:8px; border:none; cursor:pointer; background-color:#c8a96b; color:#14120f; letter-spacing:0.04em;">Lancer le cycle</button>
    </div>
    <style>
        .dot {{ width:14px; height:14px; border-radius:50%; background:#29292e; transition:0.05s; }}
        .dot.active {{ background:#8ea98a; box-shadow:0 0 8px #8ea98a88; transform:scale(1.2); }}
        .dot.first.active {{ background:#c8a96b; box-shadow:0 0 10px #c8a96b88; transform:scale(1.25); }}
    </style>
    <script>
        let audioCtx, isRunning = false, currentBeat = 0, timerId;
        const dots = document.getElementById('dots'), btn = document.getElementById('toggleBtn');
        for (let i = 0; i < {beats_per_bar}; i++) {{
            const d = document.createElement('div');
            d.className = 'dot' + (i === 0 ? ' first' : '');
            dots.appendChild(d);
        }}
        function playClick(isFirst) {{
            const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.frequency.value = isFirst ? 920 : 540;
            gain.gain.setValueAtTime(1, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.04);
            osc.start(); osc.stop(audioCtx.currentTime + 0.045);
        }}
        function tick() {{
            document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === currentBeat));
            playClick(currentBeat === 0);
            currentBeat = (currentBeat + 1) % {beats_per_bar};
        }}
        btn.onclick = () => {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (isRunning) {{
                clearInterval(timerId); isRunning = false; btn.textContent = 'Lancer le cycle'; btn.style.backgroundColor = '#c8a96b'; btn.style.color = '#14120f';
                document.querySelectorAll('.dot').forEach(d => d.classList.remove('active')); currentBeat = 0;
            }} else {{
                audioCtx.resume(); isRunning = true; btn.textContent = 'Interrompre'; btn.style.backgroundColor = 'transparent'; btn.style.border = '1px solid #29292e'; btn.style.color = '#f4f1ea';
                tick(); timerId = setInterval(tick, (60 / {bpm}) * 1000);
            }}
        }};
    </script>
    """
    components.html(html, height=180)