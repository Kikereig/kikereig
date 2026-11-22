"""Genera las canciones infantiles (dominio público) como MIDI de 2 pistas:
  pista 1 = melodía (mano derecha), pista 2 = acompañamiento (mano izquierda, 1 o 2 teclas a la vez).
Sin dependencias.  Uso:  python3 tools/make_midis.py
Escribe los .mid en midis/ y los incrusta en index.html (entre SONGS-START y SONGS-END).
"""
import base64, os, re, struct

TPQ = 480  # ticks por negra
N = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

def p(name):
    """'C4' -> 60, 'Bb3' -> 58, 'F#4' -> 66"""
    m = re.fullmatch(r"([A-G])(b|#)?(\d)", name)
    base = N[m.group(1)] + (-1 if m.group(2) == "b" else 1 if m.group(2) == "#" else 0)
    return 12 * (int(m.group(3)) + 1) + base

def seq(text):
    """'C4:1 D4:0.5 ...' -> [(pitches, beats)]; acordes con '+': 'C3+G3:2'."""
    out = []
    for tok in text.split():
        if tok == "|":
            continue
        notes, beats = tok.split(":")
        out.append(([p(x) for x in notes.split("+")], float(beats)))
    return out

def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)

def track(events_seq, ch, name=None, start_beats=0.0, tempo=None, timesig=None):
    ev = bytearray()
    if name:
        ev += vlq(0) + b"\xFF\x03" + vlq(len(name.encode())) + name.encode()
    if tempo:
        ev += vlq(0) + b"\xFF\x51\x03" + (60_000_000 // tempo).to_bytes(3, "big")
    if timesig:
        ev += vlq(0) + b"\xFF\x58\x04" + bytes([timesig, 2, 24, 8])
    ev += vlq(0) + bytes([0xC0 | ch, 0])  # piano
    gap = int(start_beats * TPQ)
    for pitches, beats in events_seq:
        dur = int(beats * TPQ)
        on = int(dur * 0.9)  # pequeño hueco para que se oigan las notas repetidas
        for i, k in enumerate(pitches):
            ev += vlq(gap if i == 0 else 0) + bytes([0x90 | ch, k, 90 if ch == 0 else 70])
        for i, k in enumerate(pitches):
            ev += vlq(on if i == 0 else 0) + bytes([0x80 | ch, k, 0])
        gap = dur - on
    ev += vlq(gap) + b"\xFF\x2F\x00"
    return b"MTrk" + struct.pack(">I", len(ev)) + bytes(ev)

def midi(song):
    data = b"MThd" + struct.pack(">IHHH", 6, 1, 2, TPQ)
    data += track(seq(song["melody"]), 0, song["title"], 0, song["bpm"], song.get("beats", 4))
    data += track(seq(song["bass"]), 1, "Acompañamiento", song.get("pickup", 0))
    return data

# Cada compás separado por " | " solo para leerlo mejor.
SONGS = [
    {
        "id": "estrellita", "title": "Estrellita", "bpm": 80,
        "melody": """C4:1 C4:1 G4:1 G4:1 | A4:1 A4:1 G4:2 | F4:1 F4:1 E4:1 E4:1 | D4:1 D4:1 C4:2 |
                     G4:1 G4:1 F4:1 F4:1 | E4:1 E4:1 D4:2 | G4:1 G4:1 F4:1 F4:1 | E4:1 E4:1 D4:2 |
                     C4:1 C4:1 G4:1 G4:1 | A4:1 A4:1 G4:2 | F4:1 F4:1 E4:1 E4:1 | D4:1 D4:1 C4:2""",
        "bass":   """C3:4 | F3:2 C3:2 | F3:2 C3:2 | G3:2 C3:2 |
                     C3:2 F3:2 | C3:2 G3:2 | C3:2 F3:2 | C3:2 G3:2 |
                     C3:4 | F3:2 C3:2 | F3:2 C3:2 | G3:2 C3+G3:2""",
    },
    {
        "id": "himno", "title": "Himno de la alegría", "bpm": 84,
        "melody": """E4:1 E4:1 F4:1 G4:1 | G4:1 F4:1 E4:1 D4:1 | C4:1 C4:1 D4:1 E4:1 | E4:1.5 D4:0.5 D4:2 |
                     E4:1 E4:1 F4:1 G4:1 | G4:1 F4:1 E4:1 D4:1 | C4:1 C4:1 D4:1 E4:1 | D4:1.5 C4:0.5 C4:2""",
        "bass":   """C3:4 | G3:4 | C3:4 | C3:2 G3:2 |
                     C3:4 | G3:4 | C3:4 | G3:2 C3+G3:2""",
    },
    {
        "id": "martinillo", "title": "Martinillo", "bpm": 92,
        "melody": """C4:1 D4:1 E4:1 C4:1 | C4:1 D4:1 E4:1 C4:1 | E4:1 F4:1 G4:2 | E4:1 F4:1 G4:2 |
                     G4:0.5 A4:0.5 G4:0.5 F4:0.5 E4:1 C4:1 | G4:0.5 A4:0.5 G4:0.5 F4:0.5 E4:1 C4:1 |
                     C4:1 G3:1 C4:2 | C4:1 G3:1 C4:2""",
        "bass":   """C3:4 | C3:4 | C3:4 | C3:4 | C3:4 | C3:4 | C3:4 | C3:4""",
    },
    {
        "id": "mary", "title": "María tenía un corderito", "bpm": 92,
        "melody": """E4:1 D4:1 C4:1 D4:1 | E4:1 E4:1 E4:2 | D4:1 D4:1 D4:2 | E4:1 G4:1 G4:2 |
                     E4:1 D4:1 C4:1 D4:1 | E4:1 E4:1 E4:1 E4:1 | D4:1 D4:1 E4:1 D4:1 | C4:4""",
        "bass":   """C3:4 | C3:4 | G3:4 | C3:4 | C3:4 | C3:4 | G3:4 | C3+G3:4""",
    },
    {
        "id": "cumple", "title": "Cumpleaños feliz", "bpm": 96, "beats": 3, "pickup": 1,
        "melody": """C4:0.75 C4:0.25 | D4:1 C4:1 F4:1 | E4:2 C4:0.75 C4:0.25 | D4:1 C4:1 G4:1 | F4:2 C4:0.75 C4:0.25 |
                     C5:1 A4:1 F4:1 | E4:1 D4:1 Bb4:0.75 Bb4:0.25 | A4:1 F4:1 G4:1 | F4:3""",
        "bass":   """F3:3 | C3:3 | C3:3 | F3:3 | F3:3 | Bb3:3 | F3:1 C3:2 | C3+F3:3""",
    },
]

if __name__ == "__main__":
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    os.makedirs(os.path.join(root, "midis"), exist_ok=True)
    js = []
    for s in SONGS:
        mel = sum(b for _, b in seq(s["melody"]))
        bas = sum(b for _, b in seq(s["bass"])) + s.get("pickup", 0)
        assert abs(mel - bas) < 1e-6, f"{s['id']}: melodía {mel} tiempos, acompañamiento {bas}"
        data = midi(s)
        with open(os.path.join(root, "midis", s["id"] + ".mid"), "wb") as f:
            f.write(data)
        js.append(f'  {{ id: "{s["id"]}", title: "{s["title"]}", b64: "{base64.b64encode(data).decode()}" }},')
        print(f"ok {s['id']}.mid  {len(data)} bytes, {mel:g} tiempos")
    html_path = os.path.join(root, "index.html")
    html = open(html_path, encoding="utf-8").read()
    block = "// SONGS-START (generado por tools/make_midis.py)\nconst SONGS = [\n" + "\n".join(js) + "\n];\n// SONGS-END"
    html, n = re.subn(r"// SONGS-START.*?// SONGS-END", lambda _: block, html, flags=re.S)
    assert n == 1, "No encuentro SONGS-START/SONGS-END en index.html"
    open(html_path, "w", encoding="utf-8").write(html)
    print("index.html actualizado")
