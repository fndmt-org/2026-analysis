# Análisis Fundament · Estudio de Convivencia Social

```
codebook/     <edición>.yaml (fuente de verdad, una por edición) + codebook.qmd + README.md (formato)
codigo/       fundament.py (lógica común), limpiar.py, anonimizar.py y exportar.py
datos/        SHA256SUMS versionado; los brutos NO se versionan
tareas/       una pregunta de análisis por archivo + esquema de salida
referencia/   resultados de referencia calculados por el equipo
runs/         salidas de los modelos + metadatos
AGENTS.md     instrucciones comunes para todos los modelos
```

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Instalar Quarto: https://quarto.org (Positron ya lo incluye)
```

## Datos

Los datos brutos contienen IP, fingerprint y texto libre: nunca se suben al repositorio, tampoco si es privado.
Se guardan en el Drive de la asociación. Para pedir acceso, contacta con Pablo Grillo o Frank Hoeft.

Ediciones disponibles: 2022, 2023, 2024 y 2026 (la edición es la temporada; ver `codebook/README.md`).
Copia los brutos a `datos/brutos/` y comprueba que son la misma versión con la que se trabajó:

```bash
sha256sum -c datos/SHA256SUMS        # Linux
shasum -a 256 -c datos/SHA256SUMS    # macOS
```

Si los datos cambian, actualiza `SHA256SUMS` en el mismo commit que el codebook.

## Codebook

```bash
cd codebook
quarto preview codebook.qmd                                    # vista previa (2026)
FUNDAMENT_EDICION=2022 quarto render codebook.qmd --no-execute-daemon --output codebook_2022.html
FUNDAMENT_EDICION=2022 quarto render codebook.qmd --no-execute-daemon --to gfm --output codebook_2022.md   # para el harness
```

`--no-execute-daemon` evita que Quarto reutilice el kernel de un render anterior (y su edición).
El render falla si los datos no cuadran con el codebook. Es intencionado. `limpiar.py` aplica la misma
validación, así que el pipeline no depende de Quarto.

El formato del YAML y cómo añadir una edición están en `codebook/README.md`.

## Limpieza

```bash
python codigo/limpiar.py [edición]   # por defecto 2026
```

Genera `datos/intermedios/fundament_<edición>_limpio.csv` (fuera de git): códigos en vez de etiquetas,
sin IP, fingerprint ni ID de plataforma, con un `id_respuesta` estable y una columna `marca_<regla>` por regla de calidad.

- `excluida`: no entra en ningún análisis (menores, pruebas, no residentes, respuestas vacías).
- `sensibilidad`: el análisis se hace con y sin estas filas (incompletas, rápidas, dispositivo o IP repetidos).

El bruto no se modifica nunca. Las reglas están en `codebook/<edición>.yaml` y su lógica en `codigo/fundament.py`;
si no coinciden, el script falla.

## Anonimización de respuestas abiertas

```bash
python codigo/anonimizar.py [edición]   # después de limpiar.py
```

Afecta a las variables `texto_libre` con `a_modelos: anonimizado`. Tacha automáticamente correos,
teléfonos, URL, DNI/NIE y usuarios @. Las respuestas con indicios que no se pueden tachar a ciegas
(direcciones, nombres propios) van a `datos/intermedios/revision_textos_<edición>.csv`:

1. Abre el CSV (por ejemplo, en el visor de datos de Positron).
2. En cada fila, edita `texto_final` si hay que tachar algo (usa `[NOMBRE]`, `[LUGAR]`, `[NEGOCIO]`…) y pon `revisado` = `si`.
3. Vuelve a ejecutar el script.

Hasta que una fila está revisada, su texto sale como `[PENDIENTE DE REVISIÓN]` en
`datos/intermedios/fundament_<edición>_anonimizado.csv`. Las decisiones se conservan entre ejecuciones,
salvo que el texto original cambie. La revisión la hace una persona: ningún modelo ve los textos sin anonimizar.

## Exportación para modelos

```bash
python codigo/exportar.py [edición]     # después de anonimizar.py
```

Genera `datos/modelos/fundament_<edición>.csv` (fuera de git), el único archivo que puede ver un modelo.
Aplica `a_modelos` del codebook: quita las variables `"no"`, reduce `timestamp` a la semana y solo
incluye filas no excluidas, con `sensibilidad` y sus marcas. Falla si queda algún texto sin revisar.

Pipeline completo de una edición: `E=2022; python codigo/limpiar.py $E && python codigo/anonimizar.py $E && python codigo/exportar.py $E`

## Versiones

- Etiqueta el codebook al congelarlo: `git tag -a codebook-2026-v0.2 -m "..."` y sube `version_codebook` en su YAML.
- Cada ejecución en `runs/` debe registrar el commit, el modelo con su versión exacta, la fecha y los parámetros. Sin eso, la comparativa no es reproducible.
