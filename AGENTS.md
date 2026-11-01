# Instrucciones para agentes · Análisis Fundament

Válidas para cualquier modelo. Sin sintaxis específica de ningún proveedor.

## Contexto

Estudio de Convivencia Social de Fundament. Encuesta online anual sobre las percepciones del turismo de las personas residentes en Mallorca que la respondieron.
Ediciones (temporada): 2022, 2023, 2024 y 2026. La edición principal es 2026: 429 respuestas en castellano y catalán, recogidas entre junio y septiembre de 2026.
Si la tarea no indica la edición, es 2026.

## Fuente de verdad

`codebook/<edición>.yaml` define cada variable de esa edición: pregunta, códigos, filtros y qué puede usarse. No deduzcas el significado de una variable por su nombre, tampoco porque se llame igual en otra edición. Si una escala tiene las anclas en `TODO`, no interpretes su dirección: dilo explícitamente.

## Reglas de análisis

1. La muestra no es probabilística (difusión online y en redes). No extrapoles a la población: habla de "personas encuestadas".
2. Los códigos 98 (no sabe) y 99 (prefiere no decirlo) son no-respuesta. Exclúyelos de medias y porcentajes e informa de cuántos hay.
3. Respeta `desde` y `depende_de`: quien no vio una pregunta no es un dato perdido.
4. Aplica las reglas de `reglas_calidad`, declara cuáles aplicas y con cuántas filas trabajas al final.
5. Acompaña cada porcentaje de su base (n). Advierte si n < 30.
6. Los datos son transversales: no atribuyas causas.
7. No calcules de memoria. Si no puedes ejecutar código sobre los datos, dilo y limítate a interpretar las tablas proporcionadas.
8. Nunca uses ni solicites variables con `a_modelos: no`.
9. Las ediciones no son directamente comparables: cambian las preguntas, las escalas (1–5, 1–10, 0–10), las categorías y la difusión. Compara solo si la tarea lo pide, variable a variable, tras comprobar en los dos codebooks que la pregunta y la escala coinciden, y declara las diferencias.

## Salida

El formato lo define cada tarea en `tareas/`. Si no se indica: JSON con las cifras y un resumen de cinco líneas como máximo.
