"""Monta panorama-2026.html a partir de plantilla.html, agregados.json y los SVG de marca de DESIGN.md.

Uso, desde la raíz del repo: .venv/bin/python -I visualizaciones/limpio-2026/construir.py .
"""
import re
import sys
from pathlib import Path

raiz = Path(sys.argv[1])
aqui = raiz / "visualizaciones/limpio-2026"
design = (raiz / "DESIGN.md").read_text()
svgs = re.findall(r"```html\n(<svg.*?</svg>)\n```", design, re.S)
logo, mark = svgs[0], svgs[1]
t = (aqui / "plantilla.html").read_text()
t = t.replace("{{LOGO}}", logo).replace("{{MARK}}", mark).replace("{{DATOS}}", (aqui / "agregados.json").read_text().strip())
assert "{{" not in t
(aqui / "panorama-2026.html").write_text(t)
