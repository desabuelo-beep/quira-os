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


# Valores que NO se pueden buscar en código sin ahogar la señal en ruido: `100`
# aparece en cualquier porcentaje, `0`/`1` en cualquier índice, `3` en cualquier
# rango. Se declaran como límite del detector en vez de fingir que los cubre —
# un inventario que no dice qué NO puede ver está afirmando de más.
_INDISTINGUIBLES = {0, 1, 100, 0.0, 0.5, 1.0}


def parametros_de(ro: dict) -> list[dict]:
    """TODO parámetro numérico que la RO declara, no sólo los tramos de vigencia.

    El primer detector sólo miraba `vigencia_operativa[].umbral` y por eso sólo
    podía ver el caso de d02. Los demás dominios declaran su parámetro en
    `parametros.umbral`, en plazos, en escalas — y ninguno de esos se estaba
    buscando: el detector tenía el mismo defecto que perseguía."""
    salida: list[dict] = []

    def caminar(o, ruta=""):
        if isinstance(o, dict):
            for k, v in o.items():
                caminar(v, f"{ruta}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                caminar(v, f"{ruta}[{i}]")
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            salida.append({"ruta": ruta.lstrip("."), "valor": o})

    caminar({k: v for k, v in ro.items() if k in ("parametros", "produce")})
    return salida



def _solo_codigo(fuente: str) -> str:
    """El archivo sin docstrings ni comentarios — para no confundir la
    documentación de un umbral con su duplicación.

    ⚠️ NACIÓ DE UN FALSO POSITIVO PROPIO. Al conectar d02 al puente quedaron
    tres «copias» que eran un docstring y dos comentarios explicando la norma:
    *«Piso TRANSITORIO 2026 (65%)…»*. Documentar un umbral no lo duplica: lo
    explica. El texto no es el código, otra vez.

    Las líneas se conservan —se sustituyen por vacías— para que los números
    reportados sigan siendo los del archivo real."""
    def _blanquear(m):
        return "\n" * m.group(0).count("\n")

    sin_doc = re.sub(r'("""|\'\'\')[\s\S]*?\1', _blanquear, fuente)
    return "\n".join("" if ln.strip().startswith("#") else ln
                     for ln in sin_doc.splitlines())


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
        crudo = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(RAIZ).as_posix()

        # ⚠️ UN COMENTARIO NO ES UNA COPIA. Al conectar d02 al puente quedaron
        # tres «copias» que eran un docstring y dos comentarios explicando la
        # norma —«Piso TRANSITORIO 2026 (65%)…»—. Documentar el umbral no lo
        # duplica: lo explica. El texto no es el código, otra vez.
        #
        # Se buscan los parámetros SOLO en líneas ejecutables: fuera docstrings
        # y fuera comentarios. Lo que queda tras esta poda es código de verdad.
        txt = _solo_codigo(crudo)

        # Vía 3 · el parámetro normativo duplicado en el código.
        for rid in ro_ids:
            ro = ros.get(rid, {})
            tramos = {t.get("umbral"): t for t in _umbrales(ro)}
            for par in parametros_de(ro):
                u = par["valor"]
                if u in _INDISTINGUIBLES:
                    continue
                for m in re.finditer(rf"(?<![\w.]){re.escape(str(u))}(?![\w.])", txt):
                    linea = txt[:m.start()].count("\n") + 1
                    ctx = txt.splitlines()[linea - 1].strip()[:90]
                    if not re.search(r"umbral|piso|m[ií]nim|techo|limite|plazo|"
                                     r"dias|plena|plen[oa]|plazo|plaz", ctx, re.I):
                        continue
                    t = tramos.get(u, {})
                    copias.append({"ro": rid, "umbral": u, "ruta": par["ruta"],
                                   "archivo": rel, "linea": linea, "contexto": ctx,
                                   "desde": t.get("desde"), "hasta": t.get("hasta")})
        # ⚠️ LA PODA VALE SOLO PARA LOS PARÁMETROS. Citar una RO en un docstring
        # ES citarla —eso es lo que `solo_la_cita` significa— y medir el vínculo
        # sobre el texto podado degradó a d07 de `carga_el_yaml` a `solo_la_cita`
        # en cuanto se introdujo. El vínculo se mide sobre el crudo.
        if any(rid in crudo for rid in ro_ids):
            citan.append(rel)
            if re.search(r"docs[/\\]brn|BRN_DIR", crudo):
                via = CARGA
            elif via != CARGA:
                via = CITA
        if via not in (CARGA,) and re.search(r"brn_cno|brn_manifest", crudo):
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
    no_verif = [{"ro": rid, "ruta": p["ruta"], "valor": p["valor"]}
                for rid, ro in mios.items() for p in parametros_de(ro)
                if p["valor"] in _INDISTINGUIBLES]
    return {
        "dominio": dominio,
        # ⚠️ LIMPIO ≠ NO COMPROBABLE, y confundirlos sería repetir adentro el
        # error que el dominio persigue afuera. d03 declara umbral 85 —un valor
        # buscable— y no aparece copiado: está limpio **y demostrado**. d01 y d09
        # declaran 100, indistinguible del ruido: no se halló nada porque no se
        # pudo buscar. La segunda no es una absolución.
        "veredicto_parametros": (
            "con_copias" if copias else
            "no_comprobable" if no_verif else
            "limpio_comprobado" if mios else "sin_ro"),
        # EL UNIVERSO, DECLARADO. Sin esto una afirmación no es comprobable:
        # nadie sabría sobre qué se hizo. Los tres errores de 2026-08-30 fueron
        # el mismo — afirmar sobre un universo que no se declaró.
        "universo": [p.relative_to(RAIZ).as_posix() for p in universo_del_dominio(dominio)],
        "parametros_copiados": copias,
        "copias_caducas": copias_caducas(copias, mios),
        # EL LÍMITE DEL DETECTOR, declarado junto al resultado. Estos parámetros
        # existen en la RO y **no se pueden buscar en código**: su valor es
        # indistinguible del ruido. Decir que el dominio está limpio sin decir
        # esto sería afirmar sobre un universo recortado en silencio — el error
        # que este módulo entero existe para no repetir.
        "parametros_no_verificables": no_verif,
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
        # EL UNIVERSO DEL INVENTARIO ENTERO, no sólo el de cada dominio. Este
        # módulo declaraba el universo por fila y no el suyo propio: sabía sobre
        # qué archivos miraba cada dominio, pero no decía **qué dominios pudo no
        # haber visto**. La regla se cumple hacia dentro y no hacia sí misma.
        "universo": {
            "que": "dominios reclamados por alguna RO, más los que tienen paquete",
            "donde": "docs/brn/*.yaml + app/agents/d*/",
            "como": "`opera_en` de cada RO (declarado por el canon) unido al "
                    "listado de directorios; el numeral romano NUNCA se usa "
                    "para inferir el dominio",
            "hallados": len(filas),
            "mecanismo": {
                "tipo": "derivado",
                "operacion": "glob",
                "por_que": "los dominios salen de `opera_en` en las RO y del listado de paquetes; ninguna lista fija los enumera",
            },
            "exclusiones": [],

            "fuera_de_alcance": [
                "CNO cuya familia romana ninguna RO reclama: sin `opera_en` que "
                "los ancle, no se les puede asignar dominio y no aparecen",
                "parámetros de valor indistinguible del ruido (0·1·100·0.5): "
                "se listan en `parametros_no_verificables`, no se buscan",
                "vías de consumo distintas de las tres medidas, si existieran",
            ],
        },
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