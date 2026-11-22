# Piano Fácil (prototipo)

Piano roll para niños con la pantalla en **horizontal**: las notas **caen hacia abajo** hasta
el teclado de piano y la app escucha por el **micrófono** qué nota se toca.

- Abre `index.html` en el navegador (para el micrófono en móvil hace falta servirlo por **https**).
- 🎤 **Micrófono**: activa la detección de notas (una nota cada vez, algoritmo YIN).
- Las notas caen y **se paran en la línea hasta que tocas la nota correcta**. Teclado de 25 teclas como mínimo (2 octavas).
- 🔊 **Escuchar**: la app toca la canción para que el niño la oiga antes.
- 📂 **MIDI**: carga cualquier `.mid`.
- Sin piano: toca las teclas del piano en pantalla, o en el ordenador `A S D F G H J K` = Do Re Mi Fa Sol La Si Do.

Canción incluida: *Estrellita* (dominio público), generada con `python3 tools/make_midis.py` → `midis/estrellita.mid`.
