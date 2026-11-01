"""Funciones comunes del análisis: carga, armonización, reglas de calidad y validación.

Las usan codebook/codebook.qmd y los scripts de codigo/, para que la validación
y la limpieza apliquen exactamente la misma lógica.

Todo lo que cambia entre ediciones está en codebook/<edición>.yaml: archivo y formato
de la fuente, nombre de cada columna, recodificación y reglas de calidad. Este módulo
no sabe nada de ninguna edición concreta.
"""
import argparse
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parent.parent
DIR_CODEBOOK = RAIZ / "codebook"
DIR_BRUTOS = RAIZ / "datos" / "brutos"
DIR_INTERMEDIOS = RAIZ / "datos" / "intermedios"
DIR_MODELOS = RAIZ / "datos" / "modelos"
EDICION_POR_DEFECTO = "2026"
NO_RESIDENTE = "No resido en Mallorca"
BLOQUES_NO_SUSTANTIVOS = {"paradatos", "tecnico", "captacion"}


def ediciones() -> list:
    return sorted(p.stem for p in DIR_CODEBOOK.glob("[0-9]*.yaml"))


def argumentos(descripcion: str, opciones: dict | None = None) -> argparse.Namespace:
    """Edición y opciones booleanas de la línea de comandos: `python codigo/exportar.py 2022 --sin-textos`."""
    parser = argparse.ArgumentParser(description=descripcion)
    parser.add_argument("edicion", nargs="?", default=EDICION_POR_DEFECTO, choices=ediciones(),
                        help=f"edición a procesar (por defecto {EDICION_POR_DEFECTO})")
    for nombre, ayuda in (opciones or {}).items():
        parser.add_argument(f"--{nombre}", action="store_true", help=ayuda)
    return parser.parse_args()


def edicion_cli(descripcion: str) -> str:
    """Lee la edición de la línea de comandos: `python codigo/limpiar.py 2022`."""
    return argumentos(descripcion).edicion


def cargar_codebook(edicion: str = EDICION_POR_DEFECTO) -> dict:
    return yaml.safe_load((DIR_CODEBOOK / f"{edicion}.yaml").read_text(encoding="utf-8"))


def ruta_bruto(cb: dict) -> Path:
    return DIR_BRUTOS / cb["fuente"]["archivo"]


def ruta_intermedio(cb: dict, etapa: str) -> Path:
    return DIR_INTERMEDIOS / f"fundament_{cb['edicion']}_{etapa}.csv"


# ── Carga ─────────────────────────────────────────────────────────

def _leer_csv(ruta: Path) -> pd.DataFrame:
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _leer_questionpro(ruta: Path, hoja: str | None) -> pd.DataFrame:
    """Exportación «Datos sin procesar» de QuestionPro (xlsx o csv).

    Dos filas de cabecera: pregunta y, en las matrices y los «Otro», subpregunta.
    El nombre de la columna es la subpregunta si existe; si no, la pregunta, con los espacios normalizados.
    Todo se lee como texto: los códigos se recodifican con `origen`.
    Se descartan las columnas vacías (encabezados de bloque, campos de QuestionPro sin uso).
    """
    if ruta.suffix == ".xlsx":
        crudo = pd.read_excel(ruta, sheet_name=hoja, header=None, dtype=str)
    else:
        crudo = pd.read_csv(ruta, header=None, dtype=str, encoding="utf-8-sig")
    nombres, vistos = [], {}
    for pregunta, sub in zip(crudo.iloc[0], crudo.iloc[1]):
        nombre = " ".join(str(sub if pd.notna(sub) else pregunta).split())  # incluye los espacios duros
        vistos[nombre] = vistos.get(nombre, -1) + 1
        nombres.append(nombre if vistos[nombre] == 0 else f"{nombre}.{vistos[nombre]}")
    df = crudo.iloc[2:].reset_index(drop=True)
    df.columns = nombres
    return df.dropna(axis=1, how="all")


LECTORES = {
    "csv": lambda ruta, fuente: _leer_csv(ruta),
    "questionpro": lambda ruta, fuente: _leer_questionpro(ruta, fuente.get("hoja")),
}


def cargar_brutos(cb: dict) -> pd.DataFrame:
    """Bruto con los nombres de variable del codebook y un id estable (orden de fila, desde 1).

    Renombra según `columna`, quita `columnas_ignoradas` y convierte tipos.
    No recodifica: eso lo hace `armonizar`.
    """
    fuente = cb["fuente"]
    df = LECTORES[fuente["formato"]](ruta_bruto(cb), fuente)
    ignoradas = [c["columna"] for c in cb.get("columnas_ignoradas", [])]
    df = df.drop(columns=[c for c in ignoradas if c in df.columns])
    df = df.rename(columns={v["columna"]: v["nombre"] for v in cb["variables"] if "columna" in v})
    for v in cb["variables"]:
        nombre = v["nombre"]
        if nombre not in df.columns:
            continue
        if v["tipo"].startswith("escala_") or v["tipo"] == "numerico":
            df[nombre] = pd.to_numeric(df[nombre])
        elif v["tipo"] == "fecha":
            formato = fuente.get("formato_fecha")
            df[nombre] = pd.to_datetime(df[nombre], format=formato) if formato else pd.to_datetime(df[nombre], utc=True)
    df.insert(0, "id_respuesta", range(1, len(df) + 1))
    return df


# ── Armonización ──────────────────────────────────────────────────

def es_otro(crudo: pd.Series, v: dict) -> pd.Series:
    """Respuestas «Otra - texto» guardadas en la misma celda que la opción (ver `otro` en el codebook)."""
    if "otro" not in v:
        return pd.Series(False, index=crudo.index)
    return crudo.astype("string").str.startswith(v["otro"]["prefijo"], na=False)


def armonizar(df: pd.DataFrame, cb: dict) -> pd.DataFrame:
    """Sustituye el texto o código crudo por los códigos del codebook.

    Con `otro`, separa «Otra - texto»: la variable recibe `otro.codigo` y el texto
    va a la variable `otro.texto`, que se inserta justo después.
    """
    out = df.copy()
    for v in cb["variables"]:
        nombre = v["nombre"]
        if "origen" not in v or nombre not in df:
            continue  # si falta la columna, lo detecta validar
        crudo = df[nombre]
        codigos = crudo.map(v["origen"])
        if "otro" in v:
            marca = es_otro(crudo, v)
            codigos = codigos.mask(marca, v["otro"]["codigo"])
            texto = crudo.astype("string").where(marca).str.slice(len(v["otro"]["prefijo"])).str.strip()
            out.insert(out.columns.get_loc(nombre) + 1, v["otro"]["texto"], texto)
        out[nombre] = codigos
    return out


# ── Reglas de calidad ─────────────────────────────────────────────
# Cada edición elige en `reglas_calidad` cuáles aplica y con qué acción.
# Aquí está la lógica de cada una; la `condicion` del YAML la describe para las personas.

def cerradas(cb: dict, h: pd.DataFrame) -> list:
    return [v["nombre"] for v in cb["variables"] if v["nombre"] in h
            and v["bloque"] not in BLOQUES_NO_SUSTANTIVOS and v["tipo"] != "texto_libre"]


def escalas(cb: dict) -> list:
    """Las escalas de opinión (bloque `escalas`), que es lo que deja sin responder quien abandona."""
    return [v["nombre"] for v in cb["variables"] if v["bloque"] == "escalas"]


REGLAS = {
    "menor_edad": lambda df, h, cb: h["age"] == 1,
    "prueba": lambda df, h, cb: df["utm_campaign"] == "prueba",
    "test_explicito": lambda df, h, cb: df["utm_source"] == "test",
    "no_residente": lambda df, h, cb: h["municipio"] == NO_RESIDENTE,
    "sin_respuestas": lambda df, h, cb: h[cerradas(cb, h)].isna().all(axis=1),
    "incompleta": lambda df, h, cb: h[escalas(cb)].isna().all(axis=1),
    # Todas las respuestas del dispositivo, también las anteriores a la tercera.
    "dispositivo_repetido": lambda df, h, cb: df["fingerprint"].map(df.groupby("fingerprint")["fp_seen"].max()) >= 3,
    "ip_repetida": lambda df, h, cb: df["ip"].map(df["ip"].value_counts()) >= 3,
    # `rapido` depende de las demás: se calcula aparte, en marcar_calidad.
}


def marcar_calidad(df: pd.DataFrame, h: pd.DataFrame, cb: dict) -> pd.DataFrame:
    """Una columna booleana por regla de `reglas_calidad`, en su orden. No borra filas."""
    acciones = {r["id"]: r["accion"] for r in cb["reglas_calidad"]}
    desconocidas = set(acciones) - set(REGLAS) - {"rapido"}
    if desconocidas:
        raise ValueError(f"Reglas del codebook sin implementar en fundament.REGLAS: {sorted(desconocidas)}")
    marcas = pd.DataFrame({r: REGLAS[r](df, h, cb) for r in acciones if r != "rapido"}, index=df.index)
    mediana = None
    if "rapido" in acciones:
        excluir = marcas[[r for r, a in acciones.items() if a == "excluir"]].any(axis=1)
        # Mediana y marca solo sobre las respuestas válidas y completas: abandonar no es responder rápido.
        completas = ~marcas.get("incompleta", False)
        mediana = df.loc[~excluir & completas, "duration_seconds"].median()
        marcas["rapido"] = (df["duration_seconds"] < mediana / 3) & completas
    marcas = marcas[list(acciones)]
    marcas.attrs["mediana_duracion"] = mediana
    return marcas


# ── Validación ────────────────────────────────────────────────────

def rango_escala(tipo: str) -> range:
    """`escala_0_10` -> range(0, 11)."""
    _, minimo, maximo = tipo.split("_")
    return range(int(minimo), int(maximo) + 1)


def validar(df: pd.DataFrame, h: pd.DataFrame, cb: dict) -> list:
    """Lista de discrepancias entre los datos y el codebook. Vacía si todo cuadra."""
    variables = {v["nombre"]: v for v in cb["variables"]}
    derivadas = {v["otro"]["texto"] for v in cb["variables"] if "otro" in v}
    versiones = {x["id"]: pd.Timestamp(x["desde"], tz="UTC") for x in cb.get("versiones_formulario", [])}
    errores = []

    for col in df.columns.drop("id_respuesta", errors="ignore"):
        if col not in variables:
            errores.append(f"`{col}` está en los datos pero no en el codebook")

    for nombre, v in variables.items():
        if nombre not in df.columns and nombre not in derivadas:
            errores.append(f"`{nombre}` está en el codebook pero no en los datos")
            continue
        if nombre in derivadas:
            if "depende_de" in v and (h[nombre].notna() & ~h.eval(v["depende_de"])).any():
                errores.append(f"`{nombre}`: respuestas sin cumplir `{v['depende_de']}`")
            continue
        s = df[nombre].dropna()

        # 1. Valores no previstos
        if "origen" in v:
            fuera = set(s[~es_otro(s, v)].astype(str)) - set(map(str, v["origen"]))
            destinos = set(v["origen"].values()) | ({v["otro"]["codigo"]} if "otro" in v else set())
            catalogo = set(v.get("valores", {})) | set(v.get("valores_validos", []))
            if destinos - catalogo:
                errores.append(f"`{nombre}`: códigos sin etiqueta {sorted(map(str, destinos - catalogo))}")
        elif "valores_validos" in v:
            fuera = set(s.astype(str)) - set(v["valores_validos"])
        elif v["tipo"].startswith("escala_"):
            fuera = set(s) - set(rango_escala(v["tipo"]))
        else:
            fuera = set()
        if fuera:
            errores.append(f"`{nombre}`: valores no previstos {sorted(map(str, fuera))}")

        # 2. Datos anteriores a la versión que introdujo la pregunta
        if "desde" in v:
            antes = (df["timestamp"] < versiones[v["desde"]]) & df[nombre].notna()
            if antes.any():
                errores.append(f"`{nombre}`: {antes.sum()} valores anteriores a {v['desde']}")

        # 3. Respuestas filtradas que aparecen donde no toca
        if "depende_de" in v:
            incoherentes = df[nombre].notna() & ~h.eval(v["depende_de"])
            if incoherentes.any():
                errores.append(f"`{nombre}`: {incoherentes.sum()} respuestas sin cumplir `{v['depende_de']}`")
    return errores


def comprobar(df: pd.DataFrame, h: pd.DataFrame, cb: dict):
    errores = validar(df, h, cb)
    if errores:
        raise SystemExit(f"El codebook {cb['edicion']} no cuadra con los datos:\n- " + "\n- ".join(errores))
