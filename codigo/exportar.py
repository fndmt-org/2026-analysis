"""Genera el único archivo que puede ver un modelo.

Uso:  python codigo/exportar.py      (después de limpiar.py y anonimizar.py)

Aplica `a_modelos` del codebook:
- si / anonimizado: la variable sale tal cual (los textos ya vienen anonimizados).
- agregado: sale transformada con la función de AGREGAR.
- no: no sale.

Solo incluye filas no excluidas. Añade `sensibilidad` y sus marcas para que el análisis
pueda hacerse con y sin esas filas.

Falla si queda algún texto sin revisar o si una variable `agregado` no tiene transformación.
Escribe datos/modelos/fundament_2026.csv (fuera de git).
"""
import pandas as pd

from fundament import RAIZ, cargar_codebook

ENTRADA = RAIZ / "datos" / "intermedios" / "fundament_2026_anonimizado.csv"
SALIDA = RAIZ / "datos" / "modelos" / "fundament_2026.csv"
EXTRA = ["id_respuesta", "sensibilidad", "marca_rapido", "marca_dispositivo_repetido"]


def semana(s: pd.Series) -> pd.Series:
    """Fecha del lunes de la semana de respuesta."""
    t = pd.to_datetime(s, utc=True, format="ISO8601")
    return (t.dt.normalize() - pd.to_timedelta(t.dt.weekday, unit="D")).dt.strftime("%Y-%m-%d")


AGREGAR = {"timestamp": semana}


def main():
    cb = cargar_codebook()
    df = pd.read_csv(ENTRADA)

    pendientes = df.astype(str).apply(lambda c: c.str.contains("PENDIENTE DE REVISIÓN", regex=False)).sum().sum()
    if pendientes:
        raise SystemExit(f"Hay {pendientes} textos sin revisar. Ejecuta anonimizar.py tras la revisión.")

    salida = df[EXTRA].copy()
    resumen = {"si": [], "anonimizado": [], "agregado": [], "no": []}
    for v in cb["variables"]:
        nombre, nivel = v["nombre"], v["a_modelos"]
        resumen[nivel].append(nombre)
        if nivel in ("si", "anonimizado"):
            salida[nombre] = df[nombre]
        elif nivel == "agregado":
            if nombre not in AGREGAR:
                raise SystemExit(f"`{nombre}` es a_modelos: agregado pero no tiene transformación en AGREGAR")
            salida[nombre] = AGREGAR[nombre](df[nombre])

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    salida.to_csv(SALIDA, index=False)

    print(f"Codebook {cb['version_codebook']} · {len(salida)} filas · {salida.shape[1]} columnas")
    for nivel, nombres in resumen.items():
        print(f"  {nivel:<12} {len(nombres):>2}: {', '.join(nombres)}")
    print(f"Escrito: {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
