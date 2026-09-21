def transcribe_notes(audio_path: str) -> list:
    from basic_pitch.inference import predict
    _, _, note_events = predict(audio_path)
    notes_sorted = sorted(note_events, key=lambda x: x[0])
    extracted = []
    for start, end, pitch, amp, _ in notes_sorted:
        if amp > 0.45:
            extracted.append((start, end, int(round(pitch))))
    return extracted