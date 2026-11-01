# Análisis Fundament · Estudio de Convivencia Social

```
codebook/     codebook.yaml (fuente de verdad) + codebook.qmd (valida y renderiza)
codigo/       fundament.py (lógica común), limpiar.py y anonimizar.py
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

Copia el CSV a `datos/brutos/` y comprueba que es la misma versión con la que se trabajó:

```bash
sha256sum -c datos/SHA256SUMS        # Linux
shasum -a 256 -c datos/SHA256SUMS    # macOS
```

Si los datos cambian, actualiza `SHA256SUMS` en el mismo commit que el codebook.

## Codebook

```bash
cd codebook
quarto preview codebook.qmd          # vista previa con recarga
quarto render codebook.qmd           # HTML para personas
quarto render codebook.qmd --to gfm  # Markdown para el harness
```

El render falla si los datos no cuadran con el codebook. Es intencionado.

## Limpieza

```bash
python codigo/limpiar.py
```

Genera `datos/intermedios/fundament_2026_limpio.csv` (fuera de git): códigos en vez de etiquetas,
sin `ip` ni `fingerprint`, con un `id_respuesta` estable y una columna `marca_<regla>` por regla de calidad.

- `excluida`: no entra en ningún análisis (menores y pruebas).
- `sensibilidad`: el análisis se hace con y sin estas filas (respuestas rápidas y dispositivos repetidos).

El bruto no se modifica nunca. Las reglas están en `codebook.yaml` y su lógica en `codigo/fundament.py`;
si no coinciden, el script falla.

## Anonimización de respuestas abiertas

```bash
python codigo/anonimizar.py          # después de limpiar.py
```

Afecta a las variables `texto_libre` con `a_modelos: anonimizado`. Tacha automáticamente correos,
teléfonos, URL, DNI/NIE y usuarios @. Las respuestas con indicios que no se pueden tachar a ciegas
(direcciones, nombres propios) van a `datos/intermedios/revision_textos.csv`:

1. Abre el CSV (por ejemplo, en el visor de datos de Positron).
2. En cada fila, edita `texto_final` si hay que tachar algo (usa `[NOMBRE]`, `[LUGAR]`, `[NEGOCIO]`…) y pon `revisado` = `si`.
3. Vuelve a ejecutar el script.

Hasta que una fila está revisada, su texto sale como `[PENDIENTE DE REVISIÓN]` en
`datos/intermedios/fundament_2026_anonimizado.csv`. Las decisiones se conservan entre ejecuciones,
salvo que el texto original cambie. La revisión la hace una persona: ningún modelo ve los textos sin anonimizar.

## Versiones

- Etiqueta el codebook al congelarlo: `git tag -a codebook-v0.2 -m "..."` y sube `version_codebook` en el YAML.
- Cada ejecución en `runs/` debe registrar el commit, el modelo con su versión exacta, la fecha y los parámetros. Sin eso, la comparativa no es reproducible.
