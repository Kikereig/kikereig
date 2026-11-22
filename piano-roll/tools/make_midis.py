"""Genera MIDIs infantiles sencillos (dominio público) sin dependencias.
Uso: python3 tools/make_midis.py  -> escribe en midis/
"""
import os, struct

C4, D4, E4, F4, G4, A4 = 60, 62, 64, 65, 67, 69
TPQ = 480  # ticks por negra

def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)

def write_midi(path, notes, bpm=80, name="song"):
    """notes: lista de (nota_midi, duracion_en_negras)."""
    ev = bytearray()
    ev += vlq(0) + b"\xFF\x03" + vlq(len(name.encode())) + name.encode()
    ev += vlq(0) + b"\xFF\x51\x03" + (60_000_000 // bpm).to_bytes(3, "big")
    ev += vlq(0) + b"\xFF\x58\x04\x04\x02\x18\x08"
    ev += vlq(0) + b"\xC0\x00"  # piano
    gap = 0  # silencio pendiente antes de la siguiente nota
    for pitch, beats in notes:
        dur = int(beats * TPQ)
        on = int(dur * 0.9)  # pequeño hueco para que se oigan las notas repetidas
        ev += vlq(gap) + bytes([0x90, pitch, 90])
        ev += vlq(on) + bytes([0x80, pitch, 0])
        gap = dur - on
    ev += vlq(gap) + b"\xFF\x2F\x00"
    data = b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPQ)
    data += b"MTrk" + struct.pack(">I", len(ev)) + bytes(ev)
    with open(path, "wb") as f:
        f.write(data)

ESTRELLITA = [
    (C4,1),(C4,1),(G4,1),(G4,1),(A4,1),(A4,1),(G4,2),
    (F4,1),(F4,1),(E4,1),(E4,1),(D4,1),(D4,1),(C4,2),
    (G4,1),(G4,1),(F4,1),(F4,1),(E4,1),(E4,1),(D4,2),
    (G4,1),(G4,1),(F4,1),(F4,1),(E4,1),(E4,1),(D4,2),
    (C4,1),(C4,1),(G4,1),(G4,1),(A4,1),(A4,1),(G4,2),
    (F4,1),(F4,1),(E4,1),(E4,1),(D4,1),(D4,1),(C4,2),
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "midis", "estrellita.mid")
    write_midi(out, ESTRELLITA, bpm=80, name="Estrellita")
    print("ok", os.path.getsize(out), "bytes ->", os.path.normpath(out))
