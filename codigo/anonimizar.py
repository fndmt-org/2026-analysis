"""Anonimiza las respuestas abiertas (variables `a_modelos: anonimizado`).

Uso:  python codigo/anonimizar.py      (después de codigo/limpiar.py)

Dos pasos:
1. Automático: sustituye correos, teléfonos, URL, DNI/NIE y usuarios @ por una etiqueta.
2. Revisión humana: las respuestas con indicios que no se pueden tachar a ciegas
   (direcciones, nombres propios) van a datos/intermedios/revision_textos.csv.
   Para cada fila, edita `texto_final` si hay que tachar algo y pon `revisado` = si.
   Las decisiones se conservan entre ejecuciones.

Mientras una respuesta sospechosa no esté revisada, en la salida aparece como
[PENDIENTE DE REVISIÓN]: por defecto no sale nada que no haya visto una persona.

Escribe datos/intermedios/fundament_2026_anonimizado.csv (solo filas no excluidas).
"""
import re

import pandas as pd

from fundament import RAIZ, cargar_codebook

ENTRADA = RAIZ / "datos" / "intermedios" / "fundament_2026_limpio.csv"
REVISION = RAIZ / "datos" / "intermedios" / "revision_textos.csv"
SALIDA = RAIZ / "datos" / "intermedios" / "fundament_2026_anonimizado.csv"
PENDIENTE = "[PENDIENTE DE REVISIÓN]"

# Paso 1: patrones que se tachan siempre.
TACHAR = {
    "[EMAIL]": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "[URL]": r"https?://\S+|www\.\S+",
    "[TELÉFONO]": r"(?<!\d)(?:\+?34[\s-]?)?[6789]\d{2}[\s-]?\d{3}[\s-]?\d{3}(?!\d)",
    "[DNI]": r"\b\d{8}[A-Za-z]\b|\b[XYZxyz]\d{7}[A-Za-z]\b",
    "[USUARIO]": r"(?<![\w.])@\w{3,}",
}

# Paso 2: indicios que decide una persona.
DIRECCION = re.compile(r"\b(?:c/|calle|carrer|avda\.?|avenida|avinguda|plaza|plaça|camí|camino)\b", re.IGNORECASE)
# Palabra en mayúscula que no va a principio de frase.
NOMBRE_PROPIO = re.compile(r"(?<![.!?¿¡:\n]\s)(?<=\s)([A-ZÁÉÍÓÚÀÈÒÏÜÑÇ][\w'’-]{2,})")
# Mayúsculas habituales que no identifican a nadie. Amplíala si hace falta.
COMUNES = {
    "Mallorca", "Mallorques", "Mallorquines", "Baleares", "Balears", "Illes", "Islas", "España",
    "Espanya", "Europa", "Gobierno", "Govern", "Consell", "Ayuntamiento", "Ajuntament", "Estado",
    "Airbnb", "Booking", "Tramuntana", "Serra", "Sierra", "Ses", "Sa", "Son", "Pobla", "Salines",
    "Porreres", "Llorenç", "Cardassar", "Palmesanos", "Ibiza", "Eivissa", "Menorca", "Formentera",
    "Alemania", "Alemanes", "Ingleses", "Británicos", "Uber", "TIB", "EMT", "PP", "PSOE", "Vox",
}


def tachar(texto: str) -> str:
    for etiqueta, patron in TACHAR.items():
        texto = re.sub(patron, etiqueta, texto)
    return texto


def indicios(texto: str, lugares: set) -> list:
    motivos = []
    if DIRECCION.search(texto):
        motivos.append("dirección")
    nombres = sorted({m for m in NOMBRE_PROPIO.findall(texto) if m not in COMUNES and m not in lugares})
    if nombres:
        motivos.append("mayúsculas: " + ", ".join(nombres))
    return motivos


def main():
    cb = cargar_codebook()
    campos = [v["nombre"] for v in cb["variables"]
              if v.get("tipo") == "texto_libre" and v["a_modelos"] == "anonimizado"]
    municipio = next(v for v in cb["variables"] if v["nombre"] == "municipio")
    lugares = {parte for m in municipio["valores_validos"] for parte in re.split(r"[\s,]+", m) if parte}

    df = pd.read_csv(ENTRADA)
    df = df[~df["excluida"]].copy()

    # Decisiones ya tomadas en revisiones anteriores.
    previas = {}
    if REVISION.exists():
        rev = pd.read_csv(REVISION, dtype=str, keep_default_na=False)
        for fila in rev.itertuples():
            previas[(int(fila.id_respuesta), fila.campo)] = fila

    filas_revision, pendientes, automaticas = [], 0, 0
    for campo in campos:
        for i, texto in df[campo].dropna().astype(str).items():
            id_resp = int(df.at[i, "id_respuesta"])
            limpio = tachar(texto)
            automaticas += limpio != texto
            motivos = indicios(limpio, lugares)
            if not motivos:
                df.at[i, campo] = limpio
                continue
            previa = previas.get((id_resp, campo))
            # Si el texto original cambió desde la revisión, la decisión ya no vale.
            vigente = previa is not None and previa.texto_auto == limpio
            revisado = vigente and previa.revisado.strip().lower() == "si"
            final = previa.texto_final if vigente else limpio
            filas_revision.append({
                "id_respuesta": id_resp, "campo": campo, "motivo": "; ".join(motivos),
                "texto_auto": limpio, "texto_final": final, "revisado": "si" if revisado else "",
            })
            df.at[i, campo] = final if revisado else PENDIENTE
            pendientes += not revisado

    pd.DataFrame(filas_revision, columns=["id_respuesta", "campo", "motivo", "texto_auto", "texto_final", "revisado"]) \
        .to_csv(REVISION, index=False)
    df.to_csv(SALIDA, index=False)

    print(f"Campos: {', '.join(campos)}")
    print(f"Respuestas con tachado automático: {automaticas}")
    print(f"Respuestas para revisión humana: {len(filas_revision)} ({pendientes} pendientes)")
    print(f"Escrito: {SALIDA.relative_to(RAIZ)} y {REVISION.relative_to(RAIZ)}")
    if pendientes:
        print(f"AVISO: {pendientes} respuestas salen como {PENDIENTE} hasta que se revisen.")


if __name__ == "__main__":
    main()
