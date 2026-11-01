"""Convierte los informes PDF de resultados/ a Markdown, para poder leerlos y citarlos.

Uso:  python codigo/pdf_a_md.py [pdf ...]      (sin argumentos: todos los de resultados/*/)

Escribe el .md junto al PDF. Por página: texto en orden de lectura, títulos detectados
por tamaño de letra (## y ###) y tablas como tablas Markdown. Cada página empieza con
un comentario <!-- página N --> para poder citar la fuente.

Es una extracción automática: los gráficos se pierden (solo queda su texto) y las tablas
complejas pueden salir mal. Para verificar una cifra, contrástala con el PDF.
Las etiquetas de los gráficos vienen invertidas en el PDF ("%87.36" es 63.78%): se corrigen.

Instalación (en Mac Intel con Python 3.14 no hay binarios de pypdfium2, que solo sirve para imágenes):
    pip install --only-binary :all: pdfminer.six && pip install --no-deps pdfplumber
"""
import re
import statistics
import sys
from pathlib import Path

import pdfplumber

from fundament import RAIZ


def tabla_md(filas: list) -> str:
    filas = [[" ".join(str(c or "").split()).replace("|", "\\|") for c in f] for f in filas if any(f)]
    if not filas:
        return ""
    ancho = max(len(f) for f in filas)
    filas = [f + [""] * (ancho - len(f)) for f in filas]
    lineas = ["| " + " | ".join(filas[0]) + " |", "|" + "---|" * ancho]
    lineas += ["| " + " | ".join(f) + " |" for f in filas[1:]]
    return "\n".join(lineas)


CIFRA_INVERTIDA = re.compile(r"%\d[\d.,]*")
SOLO_CIFRAS = re.compile(r"^[\d.,%\s+-]+$")


def enderezar(texto: str) -> str:
    """"%87.36" -> "63.78%": así salen las etiquetas de los gráficos."""
    return CIFRA_INVERTIDA.sub(lambda m: m.group(0)[::-1], texto)


def texto_md(region, cuerpo: float) -> str:
    """Líneas de una región; las de letra claramente mayor que el cuerpo se marcan como título."""
    salida = []
    for linea in region.extract_text_lines(keep_blank_chars=False):
        texto = enderezar(" ".join(linea["text"].split()))
        if not texto:
            continue
        tam = statistics.median(c["size"] for c in linea["chars"])
        if SOLO_CIFRAS.match(texto):
            salida.append(texto)  # etiqueta de gráfico, no título
        elif tam >= cuerpo * 1.6:
            salida.append(f"\n## {texto}\n")
        elif tam >= cuerpo * 1.2:
            salida.append(f"\n### {texto}\n")
        else:
            salida.append(texto)
    return "\n".join(salida)


def convertir(pdf: Path) -> Path:
    partes = [f"# {pdf.stem}\n", f"<!-- Convertido automáticamente desde {pdf.name} con codigo/pdf_a_md.py -->\n"]
    with pdfplumber.open(pdf) as doc:
        tamanos = [c["size"] for p in doc.pages for c in p.chars]
        cuerpo = statistics.median(tamanos) if tamanos else 10
        for n, pagina in enumerate(doc.pages, start=1):
            partes.append(f"\n<!-- página {n} -->\n")
            tablas = sorted(pagina.find_tables(), key=lambda t: t.bbox[1])
            cursor = 0
            for t in tablas:
                x0, top, x1, bottom = t.bbox
                if top > cursor:
                    partes.append(texto_md(pagina.crop((0, cursor, pagina.width, top)), cuerpo))
                partes.append("\n" + tabla_md(t.extract()) + "\n")
                cursor = bottom
            if cursor < pagina.height:
                partes.append(texto_md(pagina.crop((0, cursor, pagina.width, pagina.height)), cuerpo))
    destino = pdf.with_suffix(".md")
    destino.write_text("\n".join(p for p in partes if p.strip()) + "\n", encoding="utf-8")
    return destino


def main():
    pdfs = [Path(a) for a in sys.argv[1:]] or sorted((RAIZ / "resultados").glob("*/*.pdf"))
    for pdf in pdfs:
        destino = convertir(pdf.resolve())
        print(f"{destino.relative_to(RAIZ)}  ({destino.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
