# -*- coding: utf-8 -*-
"""
enrich_participacion — bloque `participacion_dom` del snapshot (DOM d08 · Dylus Lab © 2026).

Regla 1/4: NO calcula el índice madre — lo LEE del vector que ya publica el Gold Master
(`vectores.igp`). Lo que sí consolida es la EVIDENCIA DOCUMENTAL que lo sostiene, en las
tres dimensiones que el canon declara (catálogo d08 v1.0.0 · RO-VIII-001/002/003):

  1. INTEGRIDAD NORMATIVA   (RO-VIII-001) — ¿existe / se instaló / se documentó cada instancia?
  2. VITALIDAD DEMOCRÁTICA  (RO-VIII-002) — ¿cuántos participaron, con qué diversidad?  [DISEÑO]
  3. EFECTIVIDAD/INCIDENCIA (RO-VIII-003) — ¿lo pedido se volvió POA/presupuesto/obra?

DESGLOSE DE DOS CAUSAS (pedido de Javo · lo que evita el lenguaje acusatorio): una demanda
sin correlato NO prueba desatención. Se parte en dos, y la partición es reproducible:
  (a) la demanda se ancla en un LUGAR del cantón → su verificación exige que el proyecto
      declare territorio, y el POA lo declara en el 1,1% de sus filas (OBS-020) →
      **inverificable por el instrumento**, no negada.
  (b) la demanda no nombra lugar → el rechazo fue temático: ningún proyecto con rubro
      compatible → **sin correspondencia temática acreditada** en el expediente.

Fuentes (ninguna se recalcula aquí):
  · data/d08/trazabilidad_demandas.json   — motor propio de d08 (cruzar_demandas.py)
  · data/d08/catalogo_d08_v1.0.0.yaml     — SSoT del dominio (instancias + evidencia)
  · docs/brn/RO-VIII-003.yaml             — la señal preventiva que la regla PRODUCE
  · data/gm_snapshot.json → vectores.igp  — índice madre (Gold Master)

Uso:  python scripts/enrich_participacion.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import yaml

_RAIZ = Path(__file__).resolve().parents[1]
_SNAP = _RAIZ / "data" / "gm_snapshot.json"
_TRAZA = _RAIZ / "data" / "d08" / "trazabilidad_demandas.json"
_CATALOGO = _RAIZ / "data" / "d08" / "catalogo_d08_v1.0.0.yaml"
_RO_003 = _RAIZ / "docs" / "brn" / "RO-VIII-003.yaml"

sys.path.insert(0, str(_RAIZ / "scripts" / "d08"))
from filtro_ontologico import _territorios  # noqa: E402  (motor de d08, función pura de texto)

# ── GUARDIÁN OBS-020 · NO RECALCULAR ──────────────────────────────────────────
# El 1,1% es un HECHO MEDIDO y certificado bajo el protocolo de OBS-020 (dos métodos
# independientes y convergentes sobre el POA oficial). No es un parámetro de ajuste ni un
# valor a estimar en tiempo de ejecución: modificarlo sin una recalibración oficial de
# OBS-020 rompería la trazabilidad de todo el desglose de causas que descansa sobre él.
# Se cambia SOLO si la auditoría OBS-020 se rehace y publica otro número.
_POA_LOCALIZA_PCT = 1.1

# Rótulo público de cada mecanismo (frontera de lenguaje · Regla 2).
_MECANISMOS = {
    "sistema_cantonal": ("Sistema Cantonal de Participación", "LOPC 64-65 · COOTAD 304"),
    "asamblea_ciudadana": ("Asamblea Ciudadana Cantonal", "COOTAD 306 · LOPC 56"),
    "consejo_planificacion": ("Consejo de Planificación", "COPFP 28-29"),
    "audiencia_publica": ("Audiencias Públicas", "LOPC 73-75"),
    "presupuesto_participativo": ("Presupuesto Participativo", "COOTAD 238 · LOPC 67-71"),
    "cabildo_popular": ("Cabildo Popular", "LOPC 76"),
    "silla_vacia": ("Silla Vacía", "CE 101 · COOTAD 311"),
}

# Estado de la evidencia → (rótulo público, semáforo). El semáforo NO juzga al GAD:
# juzga si el expediente permite verificar. Ausencia de evidencia = resultado, no culpa.
_ESTADO_EV = {
    "estructura_verificable_por_ley": ("Verificable por ley", "ok"),
    "procesable": ("Documentado y procesable", "ok"),
    "evidencia_indirecta": ("Evidencia indirecta", "wn"),
    "normada_operacion_no_evidenciada": ("Normada · operación sin constancia", "wn"),
    "parcial": ("Documentación parcial", "wn"),
    "ocr_certificado": ("Requiere digitalización certificada", "wn"),
    "no_localizada": ("Sin constancia documental", "no"),
}


def _leer_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _leer_yaml(p: Path) -> dict:
    """Lectura con parser real. La primera versión de este script usó expresiones regulares
    bajo la premisa —FALSA, verificada 2026-08-05— de que el catálogo tenía bloques que un
    parser estricto rechazaba: `yaml.safe_load` lo carga entero. El regex habría dejado de
    encontrar campos ante un cambio de sangría o un comentario movido; el parser no."""
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def _instancias_del_catalogo(cat: dict) -> list[dict]:
    """Las 7 instancias/mecanismos con el estado de su evidencia documental."""
    out: list[dict] = []
    for i in cat.get("instancias") or []:
        ev = i.get("evidencia") or {}
        out.append({
            "cno": i.get("cno", ""), "mecanismo": i.get("mecanismo", ""),
            "tipo": i.get("tipo", ""),
            "estado_evidencia": ev.get("estado", ""),
            "acreditacion": ev.get("acreditacion", ""),
            "cobertura": ev.get("cobertura", ""),
            "formato": ev.get("formato", ""),
            "n_documentos": len(ev.get("documentos") or []),
        })
    return out


def _naturaleza_verificacion(cat: dict) -> dict[str, str]:
    """estructural / operativa / mixta — la doctrina que evita marcar 'sin evidencia'
    algo que la Ley ya define (regla de oro del catálogo)."""
    clas = ((cat.get("naturaleza_verificacion") or {}).get("clasificacion_d08")) or {}
    return {mec: clase for clase, mecs in clas.items() for mec in (mecs or [])}


def _senal_ro003(ro: dict) -> dict:
    """La señal preventiva que RO-VIII-003 declara producir (ADR-038 §1b: umbral y peso
    viven en la regla, no en el Excel — el motor solo la refleja).

    ⚠️ D-006 · EL UMBRAL SE PUBLICA SOLO SI LA REGLA ESTÁ ACREDITADA (2026-09-02).

    Este enricher hacía bien la mitad difícil: leía el YAML de la regla en vez de
    copiar el número, que es la vía canónica `carga_el_yaml`. Pero tomaba
    `umbral_activacion: 0.50` **sin mirar que `RO-VIII-003` está en `estado:
    propuesta` con `validada_por: null`** — y el snapshot publicaba una señal
    ENCENDIDA (0,848 ≥ 0,50) sobre una regla que el canon declara no acreditada.

        D-005 fue: el umbral correcto, pero copiado.
        D-006 es: el umbral bien leído, de una regla que nadie validó.

    La reparación NO es promover la regla —eso es canon y lo decide Javo—, ni
    fabricar un umbral. Es respetar el estado: el puente BRN dice si la regla
    puede consumirse, y si no puede, **la medición se publica y el veredicto no**.

    Y la frontera de ADR-047 se mantiene: el lector certifica la CONDICIÓN de
    consumo; el detalle de la señal sigue viniendo del YAML, que es de d08. El
    puente no interpreta la regla, sólo dice si está acreditada."""
    prod = (ro.get("produce") or [{}])[0]
    med = prod.get("medicion_2026") or {}
    base = {
        "nombre": prod.get("nombre", ""),
        "valor": float(med.get("valor") or 0),
        "numerador": int(med.get("numerador") or 0),
        "denominador": int(med.get("denominador") or 0),
        "regla": "más de la mitad de lo exigible sin correspondencia verificable",
        "frontera": ("No acredita desatención: acredita ausencia de habilitación documental. "
                     "La causa dominante es que el instrumento no localiza el gasto."),
    }

    sys.path.insert(0, str(_RAIZ))
    from app.agents import brn_lector as L                  # noqa: PLC0415

    r = L.regla("RO-VIII-003")
    if r is None or not r.es_consumible_como_vigente:
        estado = getattr(r, "estado_pieza", "ausente_del_catalogo")
        # La medición SÍ se publica: 162 de 191 es un hecho de d08, verificable
        # contra el POA. Lo que no se publica es el veredicto «señal activa»,
        # que es lo que carecía de autoridad. Callar las dos cosas habría
        # convertido «no puedo decidir» en «no hay nada que ver».
        return {**base, "umbral": None, "estado_umbral": "no_consumible",
                "por_que": (f"RO-VIII-003 está en «{estado}» y el umbral de "
                            f"activación no puede sostener un veredicto público. "
                            f"La medición se mantiene; la decisión de encender la "
                            f"señal exige una regla acreditada.")}
    return {**base, "umbral": float(prod.get("umbral_activacion") or 0),
            "estado_umbral": "consumible",
            "por_que": f"RO-VIII-003 vigente y acreditada por {r.sello.validado_por}"}


def construir() -> dict:
    traza = _leer_json(_TRAZA)
    cat = _leer_yaml(_CATALOGO)
    ro = _leer_yaml(_RO_003)
    snap = _leer_json(_SNAP)

    # ── 1 · INTEGRIDAD NORMATIVA ────────────────────────────────────────────────
    nat = _naturaleza_verificacion(cat)
    instancias = []
    for i in _instancias_del_catalogo(cat):
        rot, norma = _MECANISMOS.get(i["mecanismo"], (i["mecanismo"], ""))
        lbl, sem = _ESTADO_EV.get(i["estado_evidencia"], ("Estado por clasificar", "wn"))
        instancias.append({
            "nombre": rot, "norma": norma,
            "naturaleza": nat.get(i["mecanismo"], "operativa"),
            "estado": lbl, "semaforo": sem,
            "cobertura": i["cobertura"], "n_documentos": i["n_documentos"],
        })
    n_ok = sum(1 for x in instancias if x["semaforo"] == "ok")

    # ── 2 · EFECTIVIDAD / INCIDENCIA ────────────────────────────────────────────
    regs = traza["trazabilidad"]
    vinc = [r for r in regs if r["naturaleza_juridica"] == "vinculante"]
    sin_corr_v = [r for r in vinc if r["estado_epistemico"] == "sin_correlato"]

    # Las DOS causas — partición reproducible sobre el texto de la demanda.
    con_lugar = [r for r in sin_corr_v if _territorios(r["demanda"])]
    sin_lugar = [r for r in sin_corr_v if not _territorios(r["demanda"])]

    def _muestra(estado: str, n: int) -> list[dict]:
        sel = sorted((r for r in regs if r["estado_epistemico"] == estado),
                     key=lambda r: -r["similitud"])[:n]
        return [{
            "demanda": r["demanda"][:150],
            "mecanismo": _MECANISMOS.get(r["mecanismo"], (r["mecanismo"], ""))[0],
            "anio": r["anio_demanda"],
            "vinculante": r["naturaleza_juridica"] == "vinculante",
            "proyecto": (r["proyecto_poa_mas_proximo"] or "")[:180],
            "fuente_poa": r["fuente_poa"],
            "estado": estado,
            "con_lugar": bool(_territorios(r["demanda"])),
        } for r in sel]

    efectividad = {
        "total_demandas": traza["total_demandas"],
        "registros_poa_contrastados": traza["registros_poa_contrastados"],
        "vinculantes": len(vinc),
        "advisory": len(regs) - len(vinc),
        "por_estado": traza["por_estado_epistemico"],
        "vinculantes_por_estado": traza["vinculantes_por_estado"],
        "por_mecanismo": {_MECANISMOS.get(k, (k, ""))[0]: v
                          for k, v in Counter(r["mecanismo"] for r in regs).most_common()},
        "por_anio": dict(sorted(Counter(r["anio_demanda"] for r in regs).items())),
        "causas": {
            "inverificable_instrumento": len(con_lugar),
            "sin_correspondencia_tematica": len(sin_lugar),
            "poa_localiza_pct": _POA_LOCALIZA_PCT,
        },
        "muestra": _muestra("hipotesis", 3) + _muestra("pendiente_validacion", 9) + _muestra("sin_correlato", 9),
        "generado": traza["generado"],
    }

    # ── 3 · VITALIDAD DEMOCRÁTICA — declarada en diseño, no se rellena ──────────
    serie_rdc = (snap.get("rendicion") or {}).get("serie") or []
    vitalidad = {
        "estado": "diseno",
        "motivo": ("El índice nace en el motor del canon, no en esta plataforma (Regla 1/4). "
                   "Aquí se declara qué medirá y con qué fundamento, sin anticipar un número."),
        "componentes": [
            ("Cobertura poblacional", "participantes sobre población cantonal", "LOPC 64"),
            ("Diversidad territorial", "barrios, parroquias y comunas representadas", "COOTAD 306 · LOPC 57"),
            ("Equidad de género", "participación por género", "LOPC 57"),
            ("Equidad generacional", "participación por grupo etario", "LOPC 57"),
        ],
        "dato_disponible": [{"periodo": s.get("periodo"), "asistentes": s.get("asistentes")}
                            for s in serie_rdc if s.get("asistentes")],
        "bloqueo": ("Las hojas de registro de audiencias están escaneadas: sin digitalización "
                    "certificada no son dato probatorio."),
    }

    return {
        "_fuente": "enrich_participacion.py · catálogo d08 v1.0.0 + RO-VIII-001/002/003 + motor propio d08",
        "corte": traza["generado"],
        "indice_madre": (snap.get("vectores") or {}).get("igp") or {},
        "integridad": {
            "instancias": instancias,
            "n_total": len(instancias),
            "n_documentadas": n_ok,
            "hallazgo_audiencias": {"n": 28, "citan_norma": 28, "con_resolucion": 0},
        },
        "vitalidad": vitalidad,
        "efectividad": efectividad,
        "senal": _senal_ro003(ro),
    }


def main() -> int:
    bloque = construir()
    snap = _leer_json(_SNAP)
    snap["participacion_dom"] = bloque
    _SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")

    ef, ca = bloque["efectividad"], bloque["efectividad"]["causas"]
    print("participacion_dom → data/gm_snapshot.json")
    print(f"  índice madre        : {bloque['indice_madre'].get('valor')}%")
    print(f"  instancias          : {bloque['integridad']['n_documentadas']}/{bloque['integridad']['n_total']} documentadas")
    print(f"  demandas            : {ef['total_demandas']} ({ef['vinculantes']} vinculantes)")
    print(f"  sin correlato (vinc): {ef['vinculantes_por_estado']['sin_correlato']}")
    print(f"    · inverificable por el instrumento : {ca['inverificable_instrumento']}")
    print(f"    · sin correspondencia temática     : {ca['sin_correspondencia_tematica']}")
    _s = bloque["senal"]
    _u = (f"umbral {_s['umbral']}" if _s.get("umbral") is not None
          else f"SIN UMBRAL ACREDITADO · {_s.get('estado_umbral')}")
    print(f"  señal preventiva    : {_s['valor']:.3f} ({_u})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
