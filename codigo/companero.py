"""Qué filas del bruto 2026 entran en la muestra de la «Verificación de datos 2026».

Uso:  python codigo/companero.py      (necesita web/fundament survey - 2026.xlsx, fuera de git)

El compañero limpió en la hoja «Respuestas limpio» (408 filas) y en su informe retira además
las 3 que quedaban con utm_campaign = prueba: n = 405. Se casan sus filas con las del bruto por
timestamp (al segundo), huella y duración, y se escribe solo el id y la pertenencia, sin ningún
dato de la respuesta, en datos/modelos/companero_2026_filas.csv.
"""
import pandas as pd

from fundament import DIR_MODELOS, RAIZ, cargar_brutos, cargar_codebook

ORIGEN = RAIZ / "web" / "fundament survey - 2026.xlsx"
SALIDA = DIR_MODELOS / "companero_2026_filas.csv"


def clave(df: pd.DataFrame) -> pd.Series:
    segundo = pd.to_datetime(df["timestamp"], utc=True, format="mixed").dt.strftime("%Y-%m-%dT%H:%M:%S")
    # fillna: las primeras pruebas no tienen huella ni duración, y un nulo anularía la clave entera.
    return (segundo + "|" + df["fingerprint"].astype("string").fillna("") + "|"
            + pd.to_numeric(df["duration_seconds"]).astype("string").fillna(""))


def main():
    bruto = cargar_brutos(cargar_codebook("2026"))
    limpio = pd.read_excel(ORIGEN, sheet_name="Respuestas limpio")
    k_bruto, k_limpio = clave(bruto), clave(limpio)
    if k_bruto.duplicated().any() or k_limpio.duplicated().any():
        raise SystemExit("La clave timestamp|huella|duración no es única: no se pueden casar las filas.")
    if not k_limpio.isin(k_bruto).all():
        raise SystemExit(f"{(~k_limpio.isin(k_bruto)).sum()} filas de su hoja no están en el bruto.")

    filas = pd.DataFrame({"id_respuesta": bruto["id_respuesta"], "en_hoja_limpia": k_bruto.isin(k_limpio)})
    filas["en_muestra"] = filas["en_hoja_limpia"] & (bruto["utm_campaign"] != "prueba")
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    filas.to_csv(SALIDA, index=False)
    print(f"En su hoja limpia: {filas['en_hoja_limpia'].sum()} · en su muestra: {filas['en_muestra'].sum()} de {len(filas)}")
    print(f"Escrito: {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
