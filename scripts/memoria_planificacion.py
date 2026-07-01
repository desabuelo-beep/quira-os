# -*- coding: utf-8 -*-
"""
scripts/memoria_planificacion.py — Cable Memoria del MCD Planificación (Opción A)
═══════════════════════════════════════════════════════════════════════════════
ADR-031 capacidad MEMORIA. Corrección (revisión 2026-06-30): la memoria de DISEÑO
—el porqué de las decisiones— NO vive en el vault Obsidian (que es dominio, se solapa
con Supabase, y trae jerga interna sensible al Firewall) sino en el REPO: los ADRs +
BOOT + governance/historico. Este cable LEE ese registro de diseño (Regla 1) y escribe
planificacion.memoria_diseno; el cajón muestra el "porqué QUIRA lee el plan así".

Firewall: los principios se expresan en lenguaje de gestión pública (curados, verificados
contra los ADRs reales del repo); las fuentes ADR quedan como trazabilidad interna.
Uso:  python scripts/memoria_planificacion.py
Dylus Lab © 2026
"""
import json
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
ADR_DIR = REPO / "docs" / "adr"

# Los registros de diseño que gobiernan CÓMO se lee este cajón (verificables en el repo)
FUENTES = [
    "ADR-031_Modelos_Canonicos_Dominio_MCIP.md",
    "ADR-025_Principio_Alertas_QUIRA_Coherencia_Institucional.md",
    "ADR-030_Manual_Canonico_Interfaces_QUIRA.md",
    "ADR-023_Arquitectura_Tres_Niveles_QUIRA.md",
]

# El "porqué" — principios de diseño, en lenguaje de gestión pública (Firewall-safe)
PRINCIPIOS = [
    "Preventiva, no forense: QUIRA señala dónde cerrar la coherencia ANTES de que el plan se "
    "erosione en el camino al gasto — no juzga el pasado.",
    "El cajón es un modelo, no un tablero: integra las capas del ecosistema (Canon, datos vivos, "
    "relaciones, normativa, criterio) para responder UNA sola pregunta del dominio.",
    "Lenguaje de gestión pública, nunca acusatorio: se muestran coherencias y brechas, jamás culpables.",
    "QUIRA lee y conecta lo que ya existe; no inventa cifras ni estructuras — la verdad vive "
    "verificada en el Canon, la IA solo razona sobre ella.",
]


def main() -> int:
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    plan = snap.get("planificacion", {})
    if not plan:
        print("[ERR] sin bloque 'planificacion'"); return 1

    fuentes, faltan = [], []
    for f in FUENTES:
        p = ADR_DIR / f
        if p.exists():
            first = p.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
            titulo = (first[0].lstrip("# ").strip() if first else f)[:80]
            fuentes.append({"adr": f.split("_")[0], "titulo": titulo})
        else:
            faltan.append(f)

    n_adrs = len(list(ADR_DIR.glob("ADR-*.md")))
    plan["memoria_diseno"] = {
        "fuente": "Registro de diseño del repo (ADRs · BOOT · governance/historico) — no el vault de dominio",
        "fecha": date.today().isoformat(),
        "principios": PRINCIPIOS,
        "fuentes": fuentes,
        "n_decisiones_documentadas": n_adrs,
    }
    snap["planificacion"] = plan
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK — memoria de diseño escrita: {len(PRINCIPIOS)} principios · {len(fuentes)} fuentes verificadas "
          f"· {n_adrs} decisiones de diseño documentadas en el repo.")
    if faltan:
        print(f"  (aviso: no se hallaron {faltan})")
    for fu in fuentes:
        print(f"  {fu['adr']}: {fu['titulo'][:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
