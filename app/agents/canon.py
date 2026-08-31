"""
app/agents/canon.py — qué canon tiene cada dominio, y si su motor lo obedece
================================================================================
POR QUÉ EXISTE (2026-08-30). En una sola sesión, el director propuso tres veces
reconstruir cosas que ya estaban construidas:

    1 · «reconstruyamos la matriz jurídica de d09»  → existía, vigente, 10/10 SHA
    2 · «consultemos Supabase por los artículos»    → estaban en `docs/brn/`
    3 · «degrademos d09 a advisory»                 → su CNO ya lo modela como
                                                       obligación de hacer

Ninguno fue un descuido. Fueron el mismo error: **el estado de lo construido no
era consultable, había que recordarlo.** Javo lo nombró antes de que se viera el
tercero: *«hay que hacer algo para navegar toda la documentación y no perder
contexto de todo lo que tenemos construido»*.

LA RESPUESTA NO ES OTRO DOCUMENTO DE ESTADO. Los documentos envejecen en silencio
y BOOT ya vive contra su límite. La respuesta coherente con el resto del sistema
es la misma que se aplicó a las capacidades en `apropiacion.py`: **derivar el
estado de los artefactos, no declararlo**. Nadie escribe aquí un ✓ ni un ✗.

    CNO (puro Derecho, SHA por eslabón)
      └─ deriva_ro ─→ RO (métrica · parámetros · método) ─ opera_en ─→ dominio
                                                                        └─ motor

LO QUE ESTE MÓDULO NO HACE. No juzga si la RO es correcta ni si el motor la
implementa bien: dice si el motor **la tiene delante**. Es la misma distinción
que la escalera de apropiación aplicó a las pruebas — se acredita procedencia del
vínculo, no su calidad.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
BRN = RAIZ / "docs" / "brn"
AGENTES = RAIZ / "app" / "agents"

# Cómo se relaciona un motor con su Regla Operativa. TRES estados, no un bool
# —«estados, NO bool» es regla del sistema— porque la diferencia entre citar y
# cargar es precisamente la que se perdió de vista: `d09/fuentes.py` nombra
# RO-IX-001 en un docstring, y eso no es obedecerla.
CARGA = "carga_la_ro"          # el paquete abre el YAML en tiempo de ejecución
CITA = "solo_la_cita"          # el id aparece en prosa o como etiqueta
AUSENTE = "no_la_nombra"       # ni siquiera eso
SIN_RO = "sin_ro_vigente"      # no hay RO que consumir todavía

_ORDEN = (AUSENTE, CITA, CARGA)


@lru_cache(maxsize=1)
def _piezas() -> tuple[dict, dict]:
    """Los CNO y las RO tal como están en disco, sin interpretarlos."""
    import yaml
    cnos, ros = {}, {}
    for f in sorted(BRN.glob("*.yaml")):
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:                                # noqa: BLE001
            continue
        if not isinstance(d, dict) or not d.get("id"):
            continue
        (cnos if str(d["id"]).startswith("CNO") else ros)[d["id"]] = (d, f)
    return cnos, ros


def _sha_de_la_cadena(cno: dict) -> tuple[int, int]:
    """Cuántos eslabones de la cadena normativa están sellados.

    La cobertura no se declara: se cuenta sobre la cadena real. Un eslabón sin
    SHA es una norma citada que nadie puede comprobar — Regla de Oro 3."""
    cadena = cno.get("cadena") or []
    if not isinstance(cadena, list):
        return 0, 0
    con = sum(1 for e in cadena if isinstance(e, dict) and e.get("sha256"))
    return con, len(cadena)


def _vinculo_con_el_motor(dominio: str, ro_ids: list[str]) -> tuple[str, list[str]]:
    """¿El paquete del dominio carga su RO, la cita, o la ignora?

    Se deriva del código, no de una declaración. `carga` exige que algún módulo
    del paquete abra el directorio del BRN **y** nombre la RO: cualquiera de las
    dos cosas por separado se queda en `cita`, porque leer otro YAML no es leer
    su regla, y nombrarla en un comentario no es consultarla."""
    paq = AGENTES / dominio
    if not ro_ids:
        return SIN_RO, []
    if not paq.is_dir():
        return AUSENTE, []

    citan, carga = [], False
    for f in paq.rglob("*.py"):
        if "__pycache__" in f.parts:
            continue
        txt = f.read_text(encoding="utf-8", errors="replace")
        if not any(rid in txt for rid in ro_ids):
            continue
        citan.append(f.name)
        if re.search(r"docs[/\\]brn|BRN_DIR|brn\b.*\.yaml", txt):
            carga = True
    if not citan:
        return AUSENTE, []
    return (CARGA if carga else CITA), sorted(citan)


def _familia(pieza_id: str) -> str:
    """El numeral romano de un CNO/RO: `CNO-VIII-003` → `VIII`."""
    p = str(pieza_id).split("-")
    return p[1] if len(p) > 2 else ""


@lru_cache(maxsize=1)
def _familia_a_dominio() -> dict[str, str]:
    """Qué dominio corresponde a cada familia romana.

    ⚠️ El romano NO es el número del dominio —`CNO-IV` es d02— así que el mapeo
    se DERIVA de las RO, que sí declaran `opera_en`. Sin esto habría que
    adivinarlo, y adivinar el dueño de una cadena normativa es exactamente el
    tipo de inferencia que este sistema no se permite."""
    _, ros = _piezas()
    return {_familia(rid): str(d.get("opera_en"))
            for rid, (d, _) in ros.items() if str(d.get("opera_en", "")).startswith("d")}


def cno_huerfanos(dominio: str) -> list[str]:
    """CNO de este dominio que **ninguna RO reclama**.

    Un tramo ANTES del problema de d09: allí la regla existe y el motor no la
    carga; aquí la cadena normativa se modeló y nunca llegó a ser regla. Se
    detectan porque la navegación natural —dominio ← RO ← CNO— no los alcanza:
    sin RO que los derive son invisibles, que es como estuvieron los siete de
    d08 hasta que se buscó su ausencia a propósito."""
    cnos, ros = _piezas()
    reclamados = {str(d.get("deriva_de", "")).split()[0] for d, _ in ros.values()}
    fam = _familia_a_dominio()
    return sorted(cid for cid in cnos
                  if fam.get(_familia(cid)) == dominio and cid not in reclamados)


def estado_canonico(dominio: str) -> dict:
    """Qué canon tiene este dominio y si su motor lo tiene delante."""
    cnos, ros = _piezas()
    mios = {rid: d for rid, (d, _) in ros.items() if str(d.get("opera_en")) == dominio}
    vigentes = [rid for rid, d in mios.items() if d.get("estado") == "vigente"]

    # El CNO se alcanza por la RO que deriva de él: el vínculo lo declara el
    # canon, no se infiere del numeral romano (CNO-IV es d02, no d04).
    cno_ids = set()
    for d in mios.values():
        base = str(d.get("deriva_de", "")).split()[0]
        if base in cnos:
            cno_ids.add(base)
    huerfanos = cno_huerfanos(dominio)
    cno_ids |= set(huerfanos)

    con = tot = 0
    cno_vigentes = []
    for cid in sorted(cno_ids):
        cno = cnos[cid][0]
        c, t = _sha_de_la_cadena(cno)
        con, tot = con + c, tot + t
        if cno.get("estado") == "vigente":
            cno_vigentes.append(cid)

    vinculo, archivos = _vinculo_con_el_motor(dominio, list(mios))
    return {
        "dominio": dominio,
        "cno": sorted(cno_ids),
        "cno_vigentes": cno_vigentes,
        "cno_huerfanos": huerfanos,
        "sha_sellados": con,
        "sha_totales": tot,
        "ro": sorted(mios),
        "ro_vigentes": sorted(vigentes),
        "vinculo_con_el_motor": vinculo,
        "modulos_que_la_nombran": archivos,
        "tiene_motor": (AGENTES / dominio / "motor.py").exists(),
    }


def dominios_con_canon() -> list[str]:
    """Los dominios que alguna RO reclama. Derivado de `opera_en`."""
    _, ros = _piezas()
    return sorted({str(d.get("opera_en")) for d, _ in ros.values()
                   if str(d.get("opera_en", "")).startswith("d")})


def cobertura_canonica(dominios: list[str] | None = None) -> dict:
    """El inventario completo, con los ataques tomados de donde ya se cuentan.

    ⚠️ NO se recuenta nada que `apropiacion` ya derive. Dos formas de contar lo
    mismo divergen siempre —`test_12` se rompió cuatro veces por eso— y un
    inventario que se contradice con otro es peor que no tenerlo."""
    from app.agents import apropiacion as A

    doms = dominios or sorted(set(dominios_con_canon()) |
                              {p.name for p in AGENTES.glob("d*") if p.is_dir()})
    defensa = {f["dominio"]: f for f in A.cobertura_de_la_plataforma()["dominios"]}

    filas = []
    for d in doms:
        e = estado_canonico(d)
        e["ataques_ejecutados"] = defensa.get(d, {}).get("ataques_ejecutados", 0)
        e["estado_de_defensa"] = defensa.get(d, {}).get("estado", "")
        filas.append(e)

    huerfanos = [f["dominio"] for f in filas
                 if f["ro_vigentes"] and f["vinculo_con_el_motor"] != CARGA]
    return {
        "dominios": filas,
        "con_ro_vigente_sin_cargarla": sorted(huerfanos),
        "cno_sin_ro": sorted(c for f in filas for c in f["cno_huerfanos"]),
        "afirmacion_sostenible": _afirmar(filas, huerfanos),
    }


def _afirmar(filas: list[dict], huerfanos: list[str]) -> str:
    """La frase se COMPONE del estado medido; no se escribe a mano."""
    cargan = [f["dominio"] for f in filas if f["vinculo_con_el_motor"] == CARGA]
    base = (f"Consumen su Regla Operativa en tiempo de ejecución: "
            f"{', '.join(cargan) or 'ninguno'}.")
    if not huerfanos:
        return base + " Ningún dominio tiene canon vigente sin consumirlo."
    return (base + f" Tienen RO vigente y NO la cargan: {', '.join(huerfanos)} — "
            f"su motor puede coincidir con la regla, pero no la está leyendo, "
            f"así que la coincidencia no está garantizada por nada.")
