# Piano Fácil (prototipo)

Piano roll **horizontal** para niños: las notas llegan de derecha a izquierda hasta la
línea amarilla y la app escucha por el **micrófono** qué nota se toca.

- Abre `index.html` en el navegador (para el micrófono en móvil hace falta servirlo por **https**).
- 🎤 **Micrófono**: activa la detección de notas (una nota cada vez, algoritmo YIN).
- ⏳ **Me espera**: la canción se para hasta que tocas la nota correcta. 🥁 **Con ritmo**: no se para.
- 🔊 **Escuchar**: la app toca la canción para que el niño la oiga antes.
- 📂 **MIDI**: carga cualquier `.mid`.
- Sin piano: toca las teclas de la izquierda en pantalla, o en el ordenador `A S D F G H J K` = Do Re Mi Fa Sol La Si Do.

Canción incluida: *Estrellita* (dominio público), generada con `python3 tools/make_midis.py` → `midis/estrellita.mid`.
