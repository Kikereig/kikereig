# Piano Fácil (prototipo)

Piano roll para niños con la pantalla en **horizontal**: las notas **caen hacia abajo** hasta
el teclado de piano y la app escucha por el **micrófono** qué nota se toca.

- Abre `index.html` en el navegador (para el micrófono en móvil hace falta servirlo por **https**).
- 🎤 **Micrófono**: activa la detección de notas (una nota cada vez, algoritmo YIN).
- Las notas caen y **se paran en la línea hasta que tocas la nota correcta**. Teclado de 25 teclas como mínimo (2 octavas).
- 🔊 **Escuchar**: la app toca la canción para que el niño la oiga antes.
- 📂 **MIDI**: carga cualquier `.mid`.
- Sin piano: toca las teclas del piano en pantalla, o en el ordenador `A S D F G H J K` = Do Re Mi Fa Sol La Si Do.

## Canciones incluidas (dominio público)

1. Estrellita · 2. Himno de la alegría · 3. Martinillo · 4. María tenía un corderito · 5. Cumpleaños feliz

Cada una tiene **melodía** (mano derecha, notas rellenas) y **acompañamiento** de 1 o 2 teclas como máximo
(mano izquierda, notas huecas). El botón 🙌 **2 manos** / ☝️ **1 mano** quita o pone el acompañamiento.

Para añadir o cambiar canciones: edita `SONGS` en `tools/make_midis.py` y ejecuta `python3 tools/make_midis.py`.
Genera los `.mid` en `midis/` y los incrusta en `index.html`.
