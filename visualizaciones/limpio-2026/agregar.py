"""Agregados para la página «Panorama 2026».

Uso, desde la raíz del repo:
    .venv/bin/python -I visualizaciones/limpio-2026/agregar.py . > visualizaciones/limpio-2026/agregados.json

Base: datos/limpios/fundament survey - 2026 - Respuestas limpio.csv (hoja «Respuestas limpio», 405 filas).
Sin filtros: se usan las 405 filas tal cual, también la de la persona menor de edad (decisión del
8 nov. 2026). No se usan variables con a_modelos: no (ip, fingerprint, fp_*,
duration_seconds, utm_*, gclid), así que las reglas de calidad del codebook no se aplican.
Textos libres fuera. Municipios con n < 5 se agrupan.
"""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

raiz = Path(sys.argv[1])
cb = {v["nombre"]: v for v in yaml.safe_load((raiz / "codebook/2026.yaml").read_text())["variables"]}
bruto = pd.read_csv(raiz / "datos/limpios/fundament survey - 2026 - Respuestas limpio.csv")

def codifica(var):
    origen = cb[var]["origen"]
    s = bruto[var].map(origen)
    sin_mapa = bruto[var][s.isna() & bruto[var].notna()].unique().tolist()
    assert not sin_mapa, (var, sin_mapa)
    return s

ruta = raiz / "datos/limpios/fundament survey - 2026 - Respuestas limpio.csv"
codifica("age")  # comprueba que todas las edades tienen código
filas = bruto
NR = {98, 99}
out = {"archivo_sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(), "filas_archivo": len(bruto),
       "menores_incluidos": int((codifica("age") == 1).sum()), "n": len(filas)}

# Escalas 0–10
escalas = [v for v in cb.values() if v.get("tipo") == "escala_0_10"]
out["escalas"] = []
for v in escalas:
    s = filas[v["nombre"]]
    assert s.between(0, 10).all()
    dist = s.value_counts().reindex(range(11), fill_value=0)
    n = int(s.notna().sum())
    out["escalas"].append({
        "var": v["nombre"], "pregunta": v["pregunta"], "n": n,
        "dist": [int(x) for x in dist],
        "bajo": round(100 * (s <= 4).sum() / n, 1),
        "cinco": round(100 * (s == 5).sum() / n, 1),
        "alto": round(100 * (s >= 6).sum() / n, 1),
        "media": round(float(s.mean()), 2),
    })

def categorica(var, orden=None):
    v = cb[var]
    c = filas[var].map(v["origen"]) if "origen" in v else filas[var]
    vacias = int(c.isna().sum())
    nr = int(c.isin(NR).sum())
    validas = c[c.notna() & ~c.isin(NR)]
    cods = orden or [k for k in v["valores"] if k not in NR]
    base = len(validas)
    return {"var": var, "pregunta": v["pregunta"], "base": base, "no_respuesta": nr, "vacias": vacias,
            "cats": [{"cod": k, "etq": v["valores"][k], "n": int((validas == k).sum()),
                      "pct": round(100 * (validas == k).sum() / base, 1)} for k in cods]}

out["perfil"] = [categorica(x) for x in ["gender", "age", "nacionalidad", "lang", "situacion", "convivencia",
                                          "vivienda", "tourism_dependencia", "manifestacion", "responsable"]]
out["abandono"] = categorica("q_abandono")

ab = filas["q_abandono"].map(cb["q_abandono"]["origen"])
viv = filas["vivienda"].map(cb["vivienda"]["origen"])
out["abandono_vivienda"] = []
for k, etq in cb["vivienda"]["valores"].items():
    s = ab[(viv == k) & ab.notna()]
    out["abandono_vivienda"].append({"etq": etq, "n": len(s),
        "cats": [{"etq": cb["q_abandono"]["valores"][j], "n": int((s == j).sum()),
                  "pct": round(100 * (s == j).sum() / len(s), 1)} for j in (0, 1, 2)]})

# Situación económica ya está en escalas (escala_0_10)

mun = filas["municipio"].value_counts()
grandes = mun[mun >= 5]
out["municipio"] = {"total_municipios": int(len(mun)),
    "filas": [{"etq": m, "n": int(n), "pct": round(100 * n / len(filas), 1)} for m, n in grandes.items()],
    "resto": {"municipios": int((mun < 5).sum()), "n": int(mun[mun < 5].sum())}}

semana = pd.to_datetime(filas["timestamp"], utc=True).dt.tz_convert("Europe/Madrid").dt.tz_localize(None).dt.to_period("W-SUN").dt.start_time
sc = semana.value_counts().sort_index()
out["semanas"] = [{"semana": s.strftime("%Y-%m-%d"), "n": int(n)} for s, n in sc.items()]

json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
