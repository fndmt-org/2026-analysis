"""Genera el conjunto limpio a partir del CSV bruto.

Uso:  python codigo/limpiar.py

- Comprueba que el bruto coincide con datos/SHA256SUMS.
- Armoniza las etiquetas a códigos según el codebook.
- Añade una columna `marca_<regla>` por cada regla de calidad.
- `excluida`: alguna regla con acción `excluir`. Estas filas no entran en ningún análisis.
- `sensibilidad`: alguna regla con acción `sensibilidad`. El análisis se hace con y sin ellas.
- Quita ip y fingerprint: solo servían para las reglas.

Escribe datos/intermedios/fundament_2026_limpio.csv (fuera de git) e imprime el resumen.
"""
import hashlib
import subprocess

from fundament import RAIZ, RUTA_BRUTOS, armonizar, cargar_brutos, cargar_codebook, marcar_calidad

SALIDA = RAIZ / "datos" / "intermedios" / "fundament_2026_limpio.csv"
COLUMNAS_FUERA = ["ip", "fingerprint"]


def comprobar_huella():
    esperada = (RAIZ / "datos" / "SHA256SUMS").read_text().split()[0]
    real = hashlib.sha256(RUTA_BRUTOS.read_bytes()).hexdigest()
    if real != esperada:
        raise SystemExit(f"El CSV bruto no coincide con datos/SHA256SUMS ({real[:12]}… ≠ {esperada[:12]}…)")


def version_codigo():
    try:
        return subprocess.check_output(["git", "describe", "--tags", "--always", "--dirty"],
                                       cwd=RAIZ, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconocida"


def main():
    comprobar_huella()
    cb = cargar_codebook()
    df = cargar_brutos()
    h = armonizar(df, cb)
    marcas = marcar_calidad(df, h, cb)
    acciones = {r["id"]: r["accion"] for r in cb["reglas_calidad"]}

    limpio = h.drop(columns=COLUMNAS_FUERA)
    for regla in marcas:
        limpio[f"marca_{regla}"] = marcas[regla]
    limpio["excluida"] = marcas[[r for r, a in acciones.items() if a == "excluir"]].any(axis=1)
    limpio["sensibilidad"] = marcas[[r for r, a in acciones.items() if a == "sensibilidad"]].any(axis=1) & ~limpio["excluida"]

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    limpio.to_csv(SALIDA, index=False)

    validas = ~limpio["excluida"]
    print(f"Codebook {cb['version_codebook']} · código {version_codigo()}")
    print(f"Filas en el bruto: {len(df)}")
    for regla, accion in acciones.items():
        solo_validas = (marcas[regla] & validas).sum() if accion != "excluir" else ""
        print(f"  {regla:<22} {accion:<13} {marcas[regla].sum():>4} filas" +
              (f" ({solo_validas} entre las válidas)" if accion != "excluir" else ""))
    print(f"Mediana de duración (válidas): {marcas.attrs['mediana_duracion']:.0f} s")
    print(f"Excluidas: {limpio['excluida'].sum()}")
    print(f"Válidas: {validas.sum()} (de ellas {limpio['sensibilidad'].sum()} marcadas para sensibilidad;"
          f" {(validas & ~limpio['sensibilidad']).sum()} sin ninguna marca)")
    print(f"Escrito: {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
