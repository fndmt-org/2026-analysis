"""Genera el conjunto limpio a partir del bruto de una edición.

Uso:  python codigo/limpiar.py [edición]      (por defecto 2026; ver codebook/*.yaml)

- Comprueba que el bruto coincide con datos/SHA256SUMS.
- Valida los datos contra el codebook y se detiene si no cuadran.
- Armoniza las etiquetas o códigos de la fuente a los códigos del codebook.
- Añade una columna `marca_<regla>` por cada regla de calidad.
- `excluida`: alguna regla con acción `excluir`. Estas filas no entran en ningún análisis.
- `sensibilidad`: alguna regla con acción `sensibilidad`. El análisis se hace con y sin ellas.
- Quita las variables sensibles que no van a modelos (ip, fingerprint…): solo servían para las reglas.

Escribe datos/intermedios/fundament_<edición>_limpio.csv (fuera de git) e imprime el resumen.
"""
import hashlib
import subprocess

from fundament import (RAIZ, armonizar, cargar_brutos, cargar_codebook, comprobar, edicion_cli,
                       marcar_calidad, ruta_bruto, ruta_intermedio)


def comprobar_huella(cb):
    ruta = ruta_bruto(cb)
    relativa = str(ruta.relative_to(RAIZ))
    esperadas = {}
    for linea in (RAIZ / "datos" / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if linea.strip():
            huella, archivo = linea.split(maxsplit=1)
            esperadas[archivo.strip()] = huella
    if relativa not in esperadas:
        raise SystemExit(f"{relativa} no está en datos/SHA256SUMS")
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != esperadas[relativa]:
        raise SystemExit(f"El bruto no coincide con datos/SHA256SUMS ({real[:12]}… ≠ {esperadas[relativa][:12]}…)")


def version_codigo():
    try:
        return subprocess.check_output(["git", "describe", "--tags", "--always", "--dirty"],
                                       cwd=RAIZ, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconocida"


def main():
    cb = cargar_codebook(edicion_cli(__doc__.splitlines()[0]))
    comprobar_huella(cb)
    df = cargar_brutos(cb)
    h = armonizar(df, cb)
    comprobar(df, h, cb)
    marcas = marcar_calidad(df, h, cb)
    acciones = {r["id"]: r["accion"] for r in cb["reglas_calidad"]}
    fuera = [v["nombre"] for v in cb["variables"]
             if v.get("sensible") and v["a_modelos"] == "no" and v["tipo"] != "texto_libre" and v["nombre"] in h]

    limpio = h.drop(columns=fuera)
    for regla in marcas:
        limpio[f"marca_{regla}"] = marcas[regla]
    limpio["excluida"] = marcas[[r for r, a in acciones.items() if a == "excluir"]].any(axis=1)
    limpio["sensibilidad"] = marcas[[r for r, a in acciones.items() if a == "sensibilidad"]].any(axis=1) & ~limpio["excluida"]

    salida = ruta_intermedio(cb, "limpio")
    salida.parent.mkdir(parents=True, exist_ok=True)
    limpio.to_csv(salida, index=False)

    validas = ~limpio["excluida"]
    print(f"Edición {cb['edicion']} · codebook {cb['version_codebook']} · código {version_codigo()}")
    print(f"Filas en el bruto: {len(df)} · variables quitadas: {', '.join(fuera) or 'ninguna'}")
    for regla, accion in acciones.items():
        solo_validas = (marcas[regla] & validas).sum() if accion != "excluir" else ""
        print(f"  {regla:<22} {accion:<13} {marcas[regla].sum():>4} filas" +
              (f" ({solo_validas} entre las válidas)" if accion != "excluir" else ""))
    if marcas.attrs["mediana_duracion"] is not None:
        print(f"Mediana de duración (válidas): {marcas.attrs['mediana_duracion']:.0f} s")
    print(f"Excluidas: {limpio['excluida'].sum()}")
    print(f"Válidas: {validas.sum()} (de ellas {limpio['sensibilidad'].sum()} marcadas para sensibilidad;"
          f" {(validas & ~limpio['sensibilidad']).sum()} sin ninguna marca)")
    print(f"Escrito: {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
