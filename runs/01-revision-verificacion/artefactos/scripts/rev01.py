"""Tarea 01: recálculo de las cifras de «Verificación datos 2026» (artefacto «Contraste de la verificación 2026»).
Solo lee datos/modelos/*.csv y codebook/2026.yaml.
Uso: python -I rev01.py <raíz del repo>
"""
import sys, json
from pathlib import Path
import pandas as pd, numpy as np, yaml

R = Path(sys.argv[1])
cb = yaml.safe_load((R / "codebook/2026.yaml").read_text())
d = pd.read_csv(R / "datos/modelos/fundament_2026.csv")
c = pd.read_csv(R / "datos/modelos/companero_2026_filas.csv")
d = d.merge(c, on="id_respuesta", how="left")
Q = [v["nombre"] for v in cb["variables"] if v["tipo"] == "escala_0_10" and v["nombre"].startswith("q_")]

bases = {
    "nuestras_413": d,
    "sin_marcas_346": d[~d.sensibilidad],
    "comp_404": d[d.en_muestra],          # su muestra menos la fila excluida por nosotros
}

def tramos(s):
    s = s[s.notna() & ~s.isin([98, 99])]
    n = len(s)
    r = {"n": n, "nr_98_99": None,
         "0_4": int((s <= 4).sum()), "0": int((s == 0).sum()), "5": int((s == 5).sum()),
         "6_10": int((s >= 6).sum()), "7_10": int((s >= 7).sum()), "8_10": int((s >= 8).sum()),
         "10": int((s == 10).sum()), "media": round(s.mean(), 2), "mediana": float(s.median())}
    for k in ["0_4", "5", "6_10", "7_10", "8_10", "10"]:
        r[k + "_pct"] = round(100 * r[k] / n, 1)
    return r

out = {"likert": {}}
for q in Q:
    out["likert"][q] = {b: tramos(df[q]) for b, df in bases.items()}
    out["likert"][q]["nr_98_99"] = int(d[q].isin([98, 99]).sum())
    out["likert"][q]["na"] = int(d[q].isna().sum())
    out["likert"][q]["valores_unicos"] = sorted(d[q].dropna().unique().tolist())

# Segmentación
def seg(df):
    t = pd.crosstab(df.vivienda, df.q_abandono, margins=True)
    return t
out["seg_viv"] = {b: seg(df).to_dict() for b, df in bases.items()}
def edad3(a):
    return {2: "18–35", 3: "18–35", 4: "36–55", 5: "36–55", 6: "56+", 7: "56+", 8: "56+"}.get(a)
et = {}
for b, df in bases.items():
    x = df.assign(e=df.age.map(edad3), si=df.q_abandono >= 1)
    g = x.groupby(["e", "vivienda"]).agg(n=("si", "size"), si=("si", "sum"), na=("q_abandono", lambda s: int(s.isna().sum())))
    g["sip"] = (100 * g.si / g.n).round(0)
    et[b] = g.reset_index().to_dict("records")
out["edad_ten"] = et

# Demografía
demo = {}
for v in ["gender", "age", "nacionalidad", "lang", "situacion", "convivencia", "vivienda",
          "tourism_dependencia", "manifestacion", "responsable", "q_abandono"]:
    demo[v] = {b: df[v].value_counts(dropna=False).sort_index().to_dict() for b, df in bases.items()}
out["demo"] = demo
out["sit_eco"] = {b: {"dist": df.situacion_economica.value_counts().sort_index().to_dict(),
                      "media": round(df.situacion_economica.mean(), 2), "n": int(df.situacion_economica.notna().sum())}
                  for b, df in bases.items()}
out["municipio"] = {b: df.municipio.value_counts(dropna=False).to_dict() for b, df in bases.items()}
validos = set(cb["variables"][[v["nombre"] for v in cb["variables"]].index("municipio")]["valores_validos"])
out["municipios_formulario"] = len(validos)
out["municipios_fuera_lista"] = sorted(set(d.municipio.dropna()) - validos)

# Tiempo × municipio
d["mun2"] = d.municipio.where(d.municipio.isin(["Palma", "Valldemossa", "Santanyí"]), "Resto")
out["tiempo_mun"] = pd.crosstab(d.timestamp, d.mun2, margins=True).to_dict()
out["tiempo_mun_comp"] = pd.crosstab(d[d.en_muestra].timestamp, d[d.en_muestra].mun2, margins=True).to_dict()

json.dump(out, sys.stdout, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
