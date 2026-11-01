"""Funciones comunes del análisis: carga, armonización y reglas de calidad.

Las usan codebook/codebook.qmd y codigo/limpiar.py, para que la validación
y la limpieza apliquen exactamente la misma lógica.
"""
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CODEBOOK = RAIZ / "codebook" / "codebook.yaml"
RUTA_BRUTOS = RAIZ / "datos" / "brutos" / "fundament_survey_-_2026_-_Respuestas_brutas.csv"


def cargar_codebook() -> dict:
    return yaml.safe_load(RUTA_CODEBOOK.read_text(encoding="utf-8"))


def cargar_brutos() -> pd.DataFrame:
    """CSV bruto tal cual, con un id estable (orden de fila, empezando en 1)."""
    df = pd.read_csv(RUTA_BRUTOS)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df.insert(0, "id_respuesta", range(1, len(df) + 1))
    return df


def armonizar(df: pd.DataFrame, cb: dict) -> pd.DataFrame:
    """Sustituye el texto crudo (es/ca/variantes) por códigos."""
    out = df.copy()
    for v in cb["variables"]:
        if "origen" in v:
            out[v["nombre"]] = df[v["nombre"]].map(v["origen"])
    return out


def marcar_calidad(df: pd.DataFrame, h: pd.DataFrame, cb: dict) -> pd.DataFrame:
    """Una columna booleana por regla de `reglas_calidad`. No borra filas."""
    excluir = (h["age"] == 1) | (df["utm_campaign"] == "prueba") | (df["utm_source"] == "test")
    # La mediana se calcula solo sobre las respuestas válidas, sin pruebas ni menores.
    mediana = df.loc[~excluir, "duration_seconds"].median()
    marcas = pd.DataFrame({
        "menor_edad": h["age"] == 1,
        "prueba": df["utm_campaign"] == "prueba",
        "test_explicito": df["utm_source"] == "test",
        "rapido": df["duration_seconds"] < mediana / 3,
        "dispositivo_repetido": df["fp_flagged"] == True,  # noqa: E712 (columna con NaN)
    }, index=df.index)
    ids_codebook = [r["id"] for r in cb["reglas_calidad"]]
    if list(marcas) != ids_codebook:
        raise ValueError(f"Las reglas del código {list(marcas)} no coinciden con el codebook {ids_codebook}")
    marcas.attrs["mediana_duracion"] = mediana
    return marcas
