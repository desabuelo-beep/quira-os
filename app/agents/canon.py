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
CARGA = "carga_el_yaml"        # el paquete abre `docs/brn/*.yaml` en ejecución
COMPILADO = "lee_el_compilado"  # lee `snapshot["brn_cno"]` o `brn_manifest.json`
COPIADO = "parametro_copiado"  # tiene un literal que la RO también declara
CITA = "solo_la_cita"          # el id aparece en prosa o como etiqueta
AUSENTE = "no_la_nombra"       # ni siquiera eso
SIN_RO = "sin_ro_vigente"      # no hay RO que consumir todavía

# ⚠️ TRES VÍAS, NO UNA — y esto fue un error de este módulo, no de los dominios.
# La primera versión medía sólo `CARGA` y con eso acusó a d01·d02·d03·d09 de «no
# cargar su RO». Falso: el canon define OTRA vía. `ADR-039`: *«el umbral 65% se
# especifica sólo en la RO-IV-001; el compilador lo materializa»*, y `ADR-038`
# quiere que «el Gold Master sólo conozca RO-IV-001 y la BRN le responda
# variable/fórmula/umbral». d02 —el que peor salía— es el que MEJOR se ajusta al
# diseño previsto.
#
# Las 13 RO están compiladas en `snapshot["brn_cno"]` con `umbral_vigente` y
# `vigencia_operativa`. El puente está tendido, firmado y al día. Lo que el
# inventario corregido mide es si alguien lo cruza.
_ORDEN = (AUSENTE, CITA, COPIADO, COMPILADO, CARGA)


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


def universo_del_dominio(dominio: str) -> list[Path]:
    """TODO el código que un dominio ejecuta — no sólo su carpeta.

    ⚠️ ESTE FUE EL ERROR. El universo de d02 no es `app/agents/d02/`: es eso
    **más `scripts/enrich_presupuesto.py`**, donde su motor delega. Mirar sólo la
    carpeta dejaba fuera exactamente el archivo donde vive el parámetro. Un
    inventario que no declara su universo puede afirmar cualquier cosa, porque
    nadie sabe sobre qué la afirmó.

    Los scripts delegados se DERIVAN del código del paquete —el `_ENRICHER_PATH`
    que el motor abre—, no de una lista escrita a mano que envejecería."""
    paq = AGENTES / dominio
    if not paq.is_dir():
        return []
    propios = [f for f in paq.rglob("*.py") if "__pycache__" not in f.parts]
    delegados: set[Path] = set()
    for f in propios:
        txt = f.read_text(encoding="utf-8", errors="replace")
        for rel in re.findall(r'"(scripts/[\w/]+\.py)"', txt):
            if (RAIZ / rel).exists():
                delegados.add(RAIZ / rel)
    return propios + sorted(delegados)


def _umbrales(ro: dict) -> list[dict]:
    """Los tramos de vigencia que la RO declara. Un umbral con fecha futura es
    una bomba de relojería si alguien lo copió: coincide hoy y miente mañana."""
    par = ro.get("parametros") or {}
    v = par.get("vigencia_operativa")
    return [t for t in v if isinstance(t, dict)] if isinstance(v, list) else []


def _vinculo_con_el_motor(dominio: str, ro_ids: list[str],
                          ros: dict) -> tuple[str, list[str], list[dict]]:
    """Por cuál de las tres vías —si alguna— llega la RO hasta el código.

    Devuelve la vía MÁS FUERTE encontrada, los archivos que la nombran y los
    parámetros que parecen copiados. La copia se reporta como **señal con su
    ubicación**, nunca como veredicto: un número puede coincidir por azar, y
    decidir si es una copia exige leer el código — es la misma separación
    ⛔ERROR/·SEÑAL del gate epistémico."""
    if not ro_ids:
        return SIN_RO, [], []
    archivos = universo_del_dominio(dominio)
    if not archivos:
        return AUSENTE, [], []

    citan, via, copias = [], AUSENTE, []
    for f in archivos:
        txt = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(RAIZ).as_posix()

        # Vía 3 · el parámetro normativo duplicado en el código.
        for rid in ro_ids:
            for tramo in _umbrales(ros.get(rid, {})):
                u = tramo.get("umbral")
                if u is None:
                    continue
                for m in re.finditer(rf"\b{re.escape(str(u))}\b", txt):
                    linea = txt[:m.start()].count("\n") + 1
                    ctx = txt.splitlines()[linea - 1].strip()[:90]
                    if re.search(r"umbral|piso|minim|m[ií]nimo|techo|limite",
                                 ctx, re.I):
                        copias.append({"ro": rid, "umbral": u, "archivo": rel,
                                       "linea": linea, "contexto": ctx,
                                       "desde": tramo.get("desde"),
                                       "hasta": tramo.get("hasta")})
        if any(rid in txt for rid in ro_ids):
            citan.append(rel)
            if re.search(r"docs[/\\]brn|BRN_DIR", txt):
                via = CARGA
            elif via != CARGA:
                via = CITA
        if via not in (CARGA,) and re.search(r"brn_cno|brn_manifest", txt):
            via = COMPILADO
    if via == AUSENTE and copias:
        via = COPIADO
    return via, sorted(set(citan)), copias


def copias_caducas(copias: list[dict], ros: dict) -> list[dict]:
    """Copias que coinciden HOY y dejarán de coincidir en una fecha conocida.

    El caso de d02: `enrich_presupuesto.py` fija 65 y `RO-IV-001` declara 65
    hasta 2026-12-31 y **70 desde 2027-01-01**. Hoy no hay error de dato; el 1
    de enero de 2027 lo habrá, y nada avisaría. Poder decirlo antes es la
    diferencia entre un inventario y una alarma."""
    fuera = []
    for c in copias:
        tramos = _umbrales(ros.get(c["ro"], {}))
        futuros = {t.get("umbral") for t in tramos if t.get("umbral") != c["umbral"]}
        if futuros:
            fuera.append({**c, "cambia_a": sorted(x for x in futuros if x is not None)})
    return fuera


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

    vinculo, archivos, copias = _vinculo_con_el_motor(dominio, list(mios), mios)
    return {
        "dominio": dominio,
        # EL UNIVERSO, DECLARADO. Sin esto una afirmación no es comprobable:
        # nadie sabría sobre qué se hizo. Los tres errores de 2026-08-30 fueron
        # el mismo — afirmar sobre un universo que no se declaró.
        "universo": [p.relative_to(RAIZ).as_posix() for p in universo_del_dominio(dominio)],
        "parametros_copiados": copias,
        "copias_caducas": copias_caducas(copias, mios),
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

    sin_vinculo = [f["dominio"] for f in filas
                   if f["ro_vigentes"] and f["vinculo_con_el_motor"] in (CITA, AUSENTE)]
    return {
        "dominios": filas,
        "sin_vinculo_efectivo": sorted(sin_vinculo),
        "cno_sin_ro": sorted(c for f in filas for c in f["cno_huerfanos"]),
        "copias_caducas": [c for f in filas for c in f["copias_caducas"]],
        "afirmacion_sostenible": _afirmar(filas, sin_vinculo),
    }


def _afirmar(filas: list[dict], sin_vinculo: list[str]) -> str:
    """La frase se COMPONE del estado medido; no se escribe a mano."""
    por_via: dict[str, list[str]] = {}
    for f in filas:
        por_via.setdefault(f["vinculo_con_el_motor"], []).append(f["dominio"])
    partes = [f"{v}: {', '.join(sorted(d))}" for v, d in sorted(por_via.items())]
    base = "Vía por la que cada dominio alcanza su Regla Operativa — " + " · ".join(partes) + "."

    caducas = [c for f in filas for c in f["copias_caducas"]]
    if caducas:
        base += (" ⚠️ Parámetros normativos duplicados en el código que cambiarán "
                 "de valor en una fecha ya declarada por la RO: " +
                 ", ".join(f"{c['archivo']}:{c['linea']} ({c['umbral']}→"
                           f"{'/'.join(str(x) for x in c['cambia_a'])} el "
                           f"{[t for t in [c.get('hasta')] if t] or ['?']}) "
                           for c in caducas) +
                 " — coinciden hoy y dejarán de coincidir sin que nada avise.")
    if sin_vinculo:
        base += (f" Sin vínculo efectivo con su RO: {', '.join(sin_vinculo)} — la "
                 f"nombran o la ignoran, pero no la consultan.")
    return base
