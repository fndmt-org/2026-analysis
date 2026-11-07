# Artefactos de la revisión de la «Verificación de datos 2026»

Páginas HTML hechas con Claude Code a partir de la tarea 01, más los scripts que calcularon sus cifras.
No forman parte de las respuestas de la tarea: los JSON de `runs/01-revision-verificacion/` no se han tocado.

## Páginas

| Archivo | Qué contrasta | Publicada en | Estado |
|---|---|---|---|
| `contraste-verificacion-2026.html` | Todas las cifras del documento, histórico 2022–2024 incluido | https://claude.ai/code/artifact/a9a00788-bf0b-4d40-9617-b90313d16c32 | Privada. Tres pasadas, 2 y 4 nov. 2026 |
| `cifras-2026-contrastadas.html` | Solo las cifras de 2026, con el estilo de `DESIGN.md` | https://claude.ai/code/artifact/85bc4114-bfcc-47bd-b97e-36858c95de91 | Compartida por enlace. Tres pasadas, 4 nov. 2026 |

Las dos están publicadas desde la cuenta personal de Pableco. Otra cuenta (la de la asociación) puede verlas si
están compartidas, pero no actualizarlas en el mismo enlace. Para cambiarlas desde otra cuenta, edita estos
archivos y publícalos como página nueva. Los archivos empiezan en `<title>`: el publicador añade `<html>`, `<head>`
y `<body>`.

Fuente de las cifras: `datos/modelos/fundament_2026.csv`, `datos/modelos/companero_2026_filas.csv`,
`codebook/2026.yaml` y el objeto `V` de `referencia/Verificación datos 2026.html`, en el commit d8b8804.

## Scripts

Desde la raíz del repo, con los datos regenerados (ver `tareas/01-revision-verificacion-2026.md`):

```sh
.venv/bin/python -I runs/01-revision-verificacion/artefactos/scripts/rev01.py .    > rev01.json  # primera página
.venv/bin/python -I runs/01-revision-verificacion/artefactos/scripts/pasada1.py .  > p1.json     # segunda página, pasada 1
.venv/bin/python -I runs/01-revision-verificacion/artefactos/scripts/pasada2.py .                # segunda página, pasada 2
```

Comprobado el 7 nov. 2026: reproducen las cifras de las páginas. La pasada 3 de la segunda página fue un cruce
puntual de cada cifra escrita en el HTML contra `p1.json`, sin script guardado. Los scripts de las pasadas 2 y 3 de
la primera página tampoco se guardaron.

## Pendiente

- **Quién hizo la 2.ª pasada de la primera página.** La página la atribuye a Claude Fable 5.1, pero no está
  confirmado: en esa sesión se cambió de modelo con `/model`. Corregir el comentario del pie si no fue así.
- **Comentario del pie de la primera página.** Tras el texto de la 3.ª pasada sigue el de la 2.ª («Dos
  iteraciones…»). Conviene unificarlos.
- **`fundament_2026.csv` cambió de huella** al regenerarlo el 2 nov. (05a5355e… → 07684daf…) y no se guardó el
  anterior, así que no se sabe qué cambió. Detalle en `../claude-opus-5-5-2026-11-02.meta.json`.
- **Etiqueta del codebook.** La tarea pide `codebook-v0.2`, pero los codebooks 2022–2024 cambiaron después.
  Propuesta: etiquetar d8b8804 y citar esa etiqueta en la tarea.
- **No son lanzamientos en limpio.** El modelo tenía en contexto las notas del proyecto y, en la segunda página, la
  revisión anterior. No comparar estas páginas con las ejecuciones en limpio de otros modelos.
