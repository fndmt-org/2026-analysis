"""Genera el único archivo que puede ver un modelo.

Uso:  python codigo/exportar.py [edición] [--sin-textos]
      (después de limpiar.py y anonimizar.py; por defecto 2026)

Aplica `a_modelos` del codebook:
- si / anonimizado: la variable sale tal cual (los textos ya vienen anonimizados).
- agregado: sale transformada con la función de AGREGAR.
- no: no sale.

Solo incluye filas no excluidas. Añade `sensibilidad` y sus marcas para que el análisis
pueda hacerse con y sin esas filas.

Falla si queda algún texto sin revisar o si una variable `agregado` no tiene transformación.
Escribe datos/modelos/fundament_<edición>.csv (fuera de git).

Con --sin-textos no sale ninguna variable de texto libre, así que no hace falta haberlas revisado.
Escribe datos/modelos/fundament_<edición>_sin_textos.csv: el nombre avisa de que faltan.
"""
import pandas as pd

from fundament import DIR_MODELOS, RAIZ, argumentos, cargar_codebook, ruta_intermedio


def semana(s: pd.Series) -> pd.Series:
    """Fecha del lunes de la semana de respuesta."""
    t = pd.to_datetime(s, utc=True, format="ISO8601")
    return (t.dt.normalize() - pd.to_timedelta(t.dt.weekday, unit="D")).dt.strftime("%Y-%m-%d")


AGREGAR = {"timestamp": semana}


def main():
    args = argumentos(__doc__.splitlines()[0], {"sin-textos": "no exporta las variables de texto libre"})
    cb = cargar_codebook(args.edicion)
    df = pd.read_csv(ruta_intermedio(cb, "anonimizado"))
    sufijo = "_sin_textos" if args.sin_textos else ""
    salida_csv = DIR_MODELOS / f"fundament_{cb['edicion']}{sufijo}.csv"
    extra = ["id_respuesta", "sensibilidad"] + [f"marca_{r['id']}" for r in cb["reglas_calidad"] if r["accion"] == "sensibilidad"]
    textos = [v["nombre"] for v in cb["variables"] if v["tipo"] == "texto_libre"] if args.sin_textos else []

    pendientes = df.drop(columns=textos, errors="ignore").astype(str) \
        .apply(lambda c: c.str.contains("PENDIENTE DE REVISIÓN", regex=False)).sum().sum()
    if pendientes:
        raise SystemExit(f"Hay {pendientes} textos sin revisar. Revísalos y ejecuta anonimizar.py, o usa --sin-textos.")

    salida = df[extra].copy()
    resumen = {"si": [], "anonimizado": [], "agregado": [], "no": []}
    for v in cb["variables"]:
        nombre, nivel = v["nombre"], v["a_modelos"]
        if nombre in textos:
            nivel = "no"  # --sin-textos
        resumen[nivel].append(nombre)
        if nivel in ("si", "anonimizado"):
            salida[nombre] = df[nombre]
        elif nivel == "agregado":
            if nombre not in AGREGAR:
                raise SystemExit(f"`{nombre}` es a_modelos: agregado pero no tiene transformación en AGREGAR")
            salida[nombre] = AGREGAR[nombre](df[nombre])

    salida_csv.parent.mkdir(parents=True, exist_ok=True)
    salida.to_csv(salida_csv, index=False)

    print(f"Edición {cb['edicion']} · codebook {cb['version_codebook']} · {len(salida)} filas · {salida.shape[1]} columnas")
    for nivel, nombres in resumen.items():
        print(f"  {nivel:<12} {len(nombres):>2}: {', '.join(nombres)}")
    print(f"Escrito: {salida_csv.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
