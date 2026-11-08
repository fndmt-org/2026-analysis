# Tarea 01 · Revisión de la «Verificación de datos 2026»

Prompt común para todos los modelos. Se lanza igual en cada uno, sin cambios, para poder comparar las respuestas.
Copia desde «Prompt» hasta el final.

## Antes de lanzar

- Codebook: etiqueta `codebook-v0.3` (commit d8b8804). Las ejecuciones del 2 y el 4 de nov. de 2026 se hicieron
  sobre ese commit; `codebook-v0.2` no incluye los cambios posteriores en los codebooks 2022–2024. Para cada edición: `limpiar.py`, `anonimizar.py` y `exportar.py`
  (2022–2024 con `--sin-textos`: sus textos abiertos no están revisados y esta tarea no los necesita).
- `python codigo/companero.py` genera la pertenencia de cada fila a la muestra del compañero.
- El modelo solo recibe archivos de esta lista. Nunca brutos, intermedios, `web/` ni el xlsx del compañero.
- Guarda cada respuesta en `runs/01-revision-verificacion/<modelo>-<AAAA-MM-DD>.json` sin editarla.

| Archivo | Qué es |
|---|---|
| `AGENTS.md` | Reglas de análisis |
| `codebook/2022.yaml` … `codebook/2026.yaml` | Pregunta, escala y códigos de cada edición |
| `datos/modelos/fundament_2026.csv` | Respuestas 2026 limpias (413 válidas) |
| `datos/modelos/fundament_2022_sin_textos.csv`, `_2023_`, `_2024_` | Ediciones anteriores, solo preguntas cerradas |
| `datos/modelos/companero_2026_filas.csv` | `id_respuesta`, `en_hoja_limpia` y `en_muestra` (su n = 405) |
| `referencia/Verificación datos 2026.html` | El documento a revisar (cifras en el objeto `V` del script) |
| `resultados/<año>/*.md` | Informes publicados 2022, 2023 y 2024 (texto con marcas `<!-- página N -->`) |

## Prompt

Eres revisor metodológico del Estudio de Convivencia Social de Fundament. Un miembro del equipo ha preparado una
«Verificación de datos 2026» (`referencia/Verificación datos 2026.html`) antes de publicar el informe. Tu trabajo es
encontrar diferencias con nuestros datos y sesgos o supuestos no justificados en ese documento. No escribas el
informe ni interpretes los resultados del estudio: revisa cómo se obtuvieron las cifras.

Lee primero `AGENTS.md` y aplícalo en todo. En particular: la muestra no es probabilística; cada cifra lleva su
base n; no calcules de memoria; si no puedes ejecutar código, dilo en `meta.pudo_ejecutar_codigo` y limita la
revisión a lo que se pueda comprobar leyendo.

Usa solo los archivos proporcionados. No uses conocimiento externo ni la web. Cada cifra que afirmes debe llevar
su fuente: archivo y ubicación (variable y filtro, página del informe o clave del objeto `V`). Si algo no se puede
comprobar con estos archivos, va a `no_verificable`, no a `hallazgos`.

Revisa, como mínimo, estos supuestos del documento:

1. Muestra y limpieza. ¿De dónde sale n = 405? Concílialo con nuestras 413 válidas usando
   `companero_2026_filas.csv` y las marcas de calidad. ¿Qué reglas aplica cada uno y con qué efecto?
2. Métrica. ¿Es adecuado resumir las escalas 0–10 como «% de acuerdo = 6 o más» y 5 como neutral? ¿Coinciden
   las etiquetas de los tramos con lo que cuentan? ¿Cambia alguna conclusión con otra métrica razonable?
3. Redacción de los ítems. Compara cada etiqueta del documento con la `pregunta` del codebook 2026. ¿Alguna
   añade una dirección o un matiz que la pregunta no tiene?
4. Histórico 2022–2026. Para cada ítem y año, comprueba en los codebooks si la pregunta, la escala y la dirección
   (afirmación o negación) coinciden con 2026, y si los años del documento son temporadas o años de publicación.
   Contrasta cada cifra 2022–2024 con la sección y la página del informe que cita. Si una escala tiene anclas en
   `TODO`, dilo: no supongas su dirección.
5. Representatividad. Evalúa las afirmaciones sobre margen de error, intervalos de confianza y tamaño mínimo.
6. Segmentación. Recalcula los cruces de intención de dejar la isla por vivienda y por edad × vivienda. ¿Hay
   celdas con n < 30? ¿Se presentan diferencias como si fueran causales?
7. Territorio. Recalcula el reparto por municipio y el índice de representación. ¿Hay municipios que no se
   podían elegir en el formulario? ¿Hay concentraciones en el tiempo que expliquen alguna sobrerrepresentación?
8. Análisis cualitativo. Sin la codificación respuesta a respuesta no se puede verificar: evalúa el método
   descrito y si los porcentajes son reproducibles.
9. Limitaciones. ¿Qué sesgos relevantes no menciona el documento?

Devuelve solo un JSON válido con esta estructura:

```json
{
  "meta": {
    "modelo": "", "version_modelo": "", "fecha": "AAAA-MM-DD",
    "pudo_ejecutar_codigo": true, "archivos_leidos": []
  },
  "muestra": {
    "n_companero": 405, "n_nuestras_validas": null,
    "conciliacion": [{"concepto": "", "filas": 0}],
    "reglas_companero": [], "reglas_nuestras": []
  },
  "hallazgos": [
    {
      "id": "H01",
      "seccion_documento": "1",
      "supuesto": "",
      "tipo": "diferencia_cifra | sesgo_muestral | comparabilidad | metrica | redaccion | afirmacion_no_sustentada | omision",
      "cifra_documento": "",
      "cifra_propia": "",
      "n": null,
      "evidencia": [{"fuente": "", "ubicacion": ""}],
      "impacto": "alto | medio | bajo",
      "confianza": "alta | media | baja",
      "recomendacion": ""
    }
  ],
  "comparabilidad_historica": [
    {
      "item": "", "anio": 2022, "variable": "", "pregunta": "", "escala": "",
      "direccion": "afirmacion | negacion | desconocida",
      "misma_pregunta_que_2026": false, "misma_escala_que_2026": false,
      "cifra_documento": null, "cifra_informe_publicado": null, "ubicacion_informe": "",
      "comparable": "si | no | con_reservas", "motivo": ""
    }
  ],
  "no_verificable": [{"que": "", "por_que": "", "que_haria_falta": ""}],
  "resumen": "Cinco líneas como máximo."
}
```

Ordena `hallazgos` de mayor a menor impacto. No inventes campos ni omitas los obligatorios; si un valor no aplica,
usa `null`.
