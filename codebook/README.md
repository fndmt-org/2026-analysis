# Formato de los codebooks

Un archivo por edición: `codebook/<edición>.yaml`. La edición es la **temporada** que estudia la encuesta,
no el año en que se exportaron los datos (la encuesta de la temporada 2022 se cerró en 2023).

| Edición | Fuente | Plataforma | Filas |
|---|---|---|---|
| 2022 | `QuestionPro-SR-RawData-10431095-…xlsx` | QuestionPro | 454 |
| 2023 | `RawData 20240310 MERGED  - RAW Geo.csv` | QuestionPro (dos encuestas unidas) | 497 |
| 2024 | `raw_data_survey_2024.csv` | Desconocida (ya procesado, sin paradatos) | 440 |
| 2026 | `fundament_survey_-_2026_-_Respuestas_brutas.csv` | Formulario propio | 429 |

Los detalles y problemas de cada fuente están en la cabecera de su YAML.

## Claves de nivel superior

```yaml
edicion: 2022
fuente:
  archivo: "…"                 # en datos/brutos/, con su huella en datos/SHA256SUMS
  formato: questionpro         # csv | questionpro
  hoja: "Datos sin procesar"   # solo xlsx
  formato_fecha: "%d/%m/%Y %H:%M"   # opcional; sin él, la fecha se lee como ISO en UTC
reglas_calidad: [...]          # ver abajo
columnas_ignoradas:            # columnas de la fuente que no son variables, con el motivo
  - {columna: "Seq. Número", motivo: "Constante"}
versiones_formulario: [...]    # opcional; lo usa `desde`
variables: [...]
```

Formatos de fuente:

- `csv`: una fila de cabecera. Se quitan los espacios al principio y al final de los nombres.
- `questionpro`: exportación «Datos sin procesar». Dos filas de cabecera; el nombre de cada columna es la
  subpregunta (matrices, «Otro») o, si no hay, la pregunta, con los espacios normalizados.
  Se descartan las columnas vacías. Una cabecera repetida recibe el sufijo `.1`.

## Variables

| Clave | Para qué |
|---|---|
| `nombre` | Nombre en los datos limpios. Usa el de 2026 solo si la pregunta y las categorías son las mismas. |
| `columna` | Nombre de la columna en la fuente, si no coincide con `nombre`. |
| `bloque` | `sociodemografico`, `escalas`, `opinion`, `abiertas`, `paradatos`, `tecnico`, `captacion`. |
| `tipo` | `nominal`, `ordinal`, `binaria`, `escala_<min>_<max>`, `texto_libre`, `fecha`, `numerico`, `booleano`, `identificador`, `nominal_libre`. |
| `valores` | Código → etiqueta canónica. |
| `valores_validos` | Lista cerrada de textos válidos (municipio). |
| `origen` | Valor EXACTO en la fuente → código. Los códigos numéricos de QuestionPro van entre comillas (`"1": 1`). |
| `otro` | La fuente guarda «Otra - texto» en la misma celda: `{prefijo: "Otra - ", codigo: 6, texto: nacionalidad_otro}`. La variable `texto` se declara aparte, sin `columna`. |
| `anclas` | Etiquetas de los extremos de una escala, o `"TODO"` si no se conocen. |
| `depende_de` / `desde` | Filtro de la pregunta / versión del formulario que la introdujo. |
| `sensible`, `cuasi_identificador` | Riesgo para la privacidad. |
| `a_modelos` | `si`, `no`, `anonimizado` o `agregado`. |
| `nota`, `decision` | Texto libre. `TODO` marca lo que falta por decidir. |

Al limpiar se quitan las variables con `sensible: true` y `a_modelos: "no"` que no son texto libre (IP, fingerprint, ID de la plataforma).

## Reglas de calidad

Cada edición elige las reglas que puede aplicar y su acción (`excluir` o `sensibilidad`).
La lógica está en `codigo/fundament.py` (`REGLAS`); la `condicion` del YAML la describe para las personas.

| Regla | Lógica | Necesita |
|---|---|---|
| `menor_edad` | `age == 1` | `age` |
| `no_residente` | `municipio == "No resido en Mallorca"` | `municipio` |
| `sin_respuestas` | Ninguna pregunta cerrada respondida | — |
| `incompleta` | Ninguna variable del bloque `escalas` respondida | — |
| `rapido` | Duración < mediana/3, en respuestas completas; mediana de las válidas y completas | `duration_seconds` |
| `prueba`, `test_explicito` | `utm_campaign == "prueba"`, `utm_source == "test"` | UTM |
| `dispositivo_repetido` | `fp_flagged == True` | fingerprint |
| `ip_repetida` | La misma IP en 3 o más respuestas | `ip` |

Una regla nueva se añade en `REGLAS` y en esta tabla.

## Añadir una edición

1. Copia el bruto a `datos/brutos/` y añade su huella: `shasum -a 256 "datos/brutos/<archivo>" >> datos/SHA256SUMS`.
2. Crea `codebook/<edición>.yaml` partiendo del de la edición más parecida.
3. Si los códigos son numéricos, comprueba código ↔ etiqueta con una fuente independiente
   (en QuestionPro, las hojas de frecuencias del xlsx). No los deduzcas del orden de las opciones sin verificarlo.
4. Ejecuta `python codigo/limpiar.py <edición>` hasta que la validación no dé errores. No relajes la validación
   para que pase: corrige el codebook o documenta el problema en él.
5. Deja como `TODO` lo que no se pueda deducir de los datos (anclas, fechas, decisiones de privacidad).
