# -*- coding: utf-8 -*-
"""
scripts/brn_cno.py — BRN v2 · Catálogo de Cadenas Normativas Operativas (CNO)
═══════════════════════════════════════════════════════════════════════════════════
La evolución de `brn_catalogo.py` (que cataloga reglas-artículo) hacia el nodo real de la
BRN v2: la CNO (ADR-038 §234). Aquí el nodo ya no es un artículo — es una REGLA con toda
su cadena. Este módulo NO calcula ni decide: carga las CNO/RO del canon, VERIFICA cada
eslabón contra el corpus (SHA256) y materializa el Modelo de Dependencias Normativas (MDN)
como datos: CNO ↔ RO ↔ SAT (ADR-038 §9).

QUÉ HACE (y qué NO):
  · Carga  docs/brn/CNO-*.yaml y RO-*.yaml (el canon vivo · molde en BRN_CICLO_VIDA_Y_MOLDE).
  · Verifica: para cada eslabón, el SHA del YAML DEBE coincidir con el del corpus (Regla 3).
    Si no coincide o el artículo no existe, el eslabón se marca `no_verificado` y la CNO no
    puede ser `vigente` — el error del "65% = Art. 192" se vuelve imposible por construcción.
  · Enlaza el MDN: qué RO derivan de cada CNO, qué SAT consumen cada RO, en qué DOM operan.
  · Escribe snapshot["brn_cno"]. NO promueve estados: respeta `propuesta` (ADR-035 §5).

LÍMITE DURO (ADR-038 §207): la BRN traza el motor, no lo alimenta. Este módulo NO toca el
Gold Master ni escribe umbrales en él — solo registra la relación `umbral ← funda en → CNO`.

Uso:  python scripts/brn_cno.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

import yaml

from brn_ro_adapter import adaptar, umbral_en

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
SECRETS = REPO / ".streamlit" / "secrets.toml"
BRN_DIR = REPO / "docs" / "brn"


def _umbral_vigente(ro: dict, hoy: str) -> tuple:
    """Umbral del tramo vigente a la fecha (molde §4b), vía el ROAdapter (contrato estable).
    Devuelve (umbral_hoy, tramos_serializados)."""
    model = adaptar(ro)
    umbral = umbral_en(model, hoy)
    tramos = [{"desde": t.desde, "hasta": t.hasta, "umbral": t.umbral} for t in model.tramos]
    # si es umbral plano (un tramo sin fechas), no se reporta como vigencia_operativa
    if len(tramos) == 1 and tramos[0]["desde"] is None:
        tramos = None
    return umbral, tramos


def _uri() -> str:
    try:
        return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        return ""


def _cargar(patron: str) -> list[dict]:
    """Carga los YAML del canon BRN que casan con el patrón (CNO-*, RO-*)."""
    out = []
    for p in sorted(BRN_DIR.glob(patron)):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
            if isinstance(d, dict) and d.get("id"):
                d["_archivo"] = p.name
                out.append(d)
        except Exception as e:
            print(f"   [WARN] {p.name}: no se pudo leer ({str(e)[:60]})")
    return out


def _verificar_cadena(cur, cadena: list[dict]) -> tuple[list[dict], bool]:
    """El SHA ES la prueba (Regla 3). Se verifica que el SHA del YAML exista en el corpus
    Y que pertenezca a la norma declarada. No se confía en el número/rótulo del artículo —
    varios sub-artículos comparten chunk (198.6 y la Transitoria viven en el mismo Art. 7).
    Devuelve (eslabones_anotados, cadena_integra)."""
    anotada, integra = [], True
    for esl in cadena or []:
        norma = esl.get("norma", "")
        sha_yaml = str(esl.get("sha256", "")).strip().rstrip("…").lower()
        estado = "no_verificado"
        if sha_yaml:
            # ¿existe ese SHA en el corpus, bajo esa norma? (el SHA identifica el texto verificado)
            cur.execute("SELECT norma_sigla FROM public.normativa_corpus "
                        "WHERE lower(sha256) LIKE %s LIMIT 1", (sha_yaml + "%",))
            row = cur.fetchone()
            if row:
                estado = "verificado" if row[0] == norma else "norma_divergente"
        if estado != "verificado":
            integra = False
        anotada.append({**{k: v for k, v in esl.items() if k != "sha256"},
                        "sha256": sha_yaml, "verificacion": estado})
    return anotada, integra



def _leer_sello(canon_sha: str) -> dict:
    """La validación humana del catálogo, leída del artefacto de gobernanza.

    ⚠️ ESTE COMPILADOR NUNCA ESCRIBE EL SELLO, y es la propiedad que lo hace
    valer algo: si lo escribiera, **cada recompilación lo renovaría sola** y un
    sello que se firma solo no acredita nada — el mismo defecto que el literal
    que vino a sustituir, con otro disfraz.

    Y CADUCA. El sello está atado al `canon_sha256` que validó: si el canon de
    entrada cambia, describe otra compilación y el catálogo vuelve a
    `no_consta`. Es el mecanismo del escalón 5 —un testimonio que no caduca es
    un testimonio que dejó de mirar el objeto— aplicado al acto de gobierno."""
    f = REPO / "docs" / "registry" / "sello_catalogo_brn.json"
    if not f.exists():
        return {"estado": "no_consta",
                "por_que": "no hay artefacto de sello en docs/registry/"}
    try:
        s = json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"estado": "no_consta", "por_que": "el sello no es legible"}
    if s.get("canon_sha256_validado") != canon_sha:
        return {"estado": "no_consta",
                "por_que": f"el sello valida el canon {s.get('canon_sha256_validado')} "
                           f"y el actual es {canon_sha}: describe otra compilación",
                "sello_caducado_de": s.get("validado_por"),
                "fecha_del_sello_caducado": s.get("fecha_validacion")}
    return {"estado": s.get("estado", "no_consta"),
            "validado_por": s.get("validado_por"),
            "fecha_validacion": s.get("fecha_validacion"),
            "alcance": s.get("alcance", "")}


def main() -> int:
    uri = _uri()
    if not uri:
        print("[skip] sin supabase_uri — la BRN no puede verificar sus cadenas (Regla 3)")
        return 0
    cnos = _cargar("CNO-*.yaml")
    ros = _cargar("RO-*.yaml")
    if not cnos:
        print(f"[skip] sin CNO en {BRN_DIR} — nada que catalogar")
        return 0

    import psycopg2
    cur = psycopg2.connect(uri, connect_timeout=25).cursor()

    # Índice de RO por CNO de la que derivan (MDN · trazabilidad bidireccional)
    ro_por_cno: dict[str, list[dict]] = {}
    for ro in ros:
        cno_id = adaptar(ro).cno_id                      # vía ROAdapter (contrato · nunca el YAML crudo)
        ro_por_cno.setdefault(cno_id, []).append(ro)

    catalogo, integras = [], 0
    for cno in cnos:
        cadena, integra = _verificar_cadena(cur, cno.get("cadena", []))
        if integra:
            integras += 1
        ro_ligadas = []
        hoy = date.today().isoformat()
        for ro in ro_por_cno.get(cno["id"], []):
            # CONTRATO (colega · 2026-07-20): ningún módulo salvo el ROAdapter lee el YAML de una RO.
            # Todo lo de abajo sale del modelo interno estable.
            m = adaptar(ro)
            umbral_hoy, tramos = _umbral_vigente(ro, hoy)
            ro_ligadas.append({
                "id": m.id, "version": m.version,
                "variable": m.metrica,
                "umbral_vigente": umbral_hoy,            # el del tramo vigente a la fecha (§4b)
                "vigencia_operativa": tramos,            # todos los tramos (transición, no reforma)
                "consume": list(m.consume), "opera_en": m.opera_en,
                "estado": m.estado,
            })
        catalogo.append({
            "id": cno["id"], "version": cno.get("version"), "titulo": cno.get("titulo"),
            "dominio_normativo": cno.get("dominio_normativo"),
            "estado": cno.get("estado", "propuesta"),
            "cadena_integra": integra,          # ¿todos los eslabones verificados? (Regla 3)
            "n_eslabones": len(cadena),
            "cadena": cadena,
            "deriva_ro": ro_ligadas,            # MDN: CNO → RO → SAT
            "vigencia": cno.get("vigencia", {}),
        })

    cur.connection.close()

    # ── EL ESTADO DEL CATÁLOGO SE DERIVA · D-003 (2026-09-01) ────────────────
    # Aquí había un literal: `"propuesta · pendiente de validación humana"`,
    # fijo. Ninguna validación podía moverlo — un campo que nunca puede ser
    # verdadero no informa. Y mentía: el 26-ago se promovieron a `vigente` las
    # nueve piezas de d07 y el catálogo del 19-ago seguía llamándolas propuesta.
    #
    # Javo: *«que herede el estado de sus piezas»*. El colega, a la vez:
    # *«la validación de las piezas y la validación del acto de compilación son
    # cosas distintas»*. **Las dos cosas son ciertas y caben juntas**: el estado
    # de las piezas se DERIVA —deja de mentir— y la validación humana del
    # catálogo se declara aparte, porque ADR-035 §5 exige un acto humano que
    # ningún conteo puede sustituir.
    from collections import Counter
    import hashlib

    por_estado = Counter(c["estado"] for c in catalogo)
    ro_por_estado = Counter(r["estado"] for c in catalogo for r in c["deriva_ro"])

    # HUELLA DEL CANON DE ENTRADA. Con esto, un compilado desfasado deja de ser
    # invisible: quien lo lea puede rehacer el hash de `docs/brn/` y saber si
    # describe el canon de hoy. Es el escalón 7 aplicado al compilador — el
    # derivado señala el origen del que salió.
    h = hashlib.sha256()
    for f in sorted(BRN_DIR.glob("*.yaml")):
        h.update(f.name.encode()); h.update(f.read_bytes())
    canon_sha = h.hexdigest()[:16]

    bloque = {
        "_fuente": "Canon BRN (docs/brn/*.yaml) verificado contra el corpus (SHA256)",
        "_doctrina": "El nodo es la REGLA (CNO), no el artículo. La cadena íntegra o no entra "
                     "(Regla 3). La IA propone, el humano valida (ADR-035 §5).",
        "_modelo": "MDN — Modelo de Dependencias Normativas (ADR-038 §9): CNO ↔ RO ↔ SAT.",
        "fecha": date.today().isoformat(),
        "total_cno": len(catalogo), "cadenas_integras": integras,
        "total_ro": len(ros),
        # DERIVADO · lo que de verdad hay dentro
        "estado_piezas_cno": dict(por_estado),
        "estado_piezas_ro": dict(ro_por_estado),
        "integridad_compilacion": {
            "piezas_cno": f"{integras}/{len(catalogo)}",
            "piezas_ro": f"{len(ros)}/{len(ros)}",
        },
        "canon_sha256": canon_sha,
        # DECLARADO · el acto de compilar es otra cosa que las piezas.
        # Se LEE del sello de gobernanza; este compilador nunca lo escribe.
        "validacion_humana_del_catalogo": _leer_sello(canon_sha),
        "por_que": "ADR-035 §5 exige un acto humano de validación. Que las "
                   "piezas estén vigentes NO valida el acto de compilarlas: son "
                   "afirmaciones distintas y este campo no las colapsa.",
        "cno": catalogo,
    }
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    snap["brn_cno"] = bloque
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK — BRN v2 · catálogo de CNO: {len(catalogo)} cadena(s) · {integras} íntegra(s) · {len(ros)} RO")
    for c in catalogo:
        marca = "✓ íntegra" if c["cadena_integra"] else "✗ REVISAR"
        ros_ids = ", ".join(r["id"] for r in c["deriva_ro"]) or "—"
        print(f'   {c["id"]:12} v{c["version"]} [{marca}] {c["n_eslabones"]} eslabones → RO: {ros_ids} ({c["estado"]})')
        for esl in c["cadena"]:
            vs = {"verificado": "✓", "sha_divergente": "✗ SHA≠", "no_verificado": "✗ falta"}.get(esl["verificacion"], "?")
            print(f'        {vs} {esl.get("norma",""):12} {str(esl.get("articulo","")):14} [{esl["verificacion"]}]')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
