# -*- coding: utf-8 -*-
"""
scripts/ia_criterio_planificacion.py — Cable de Interpretación (QUIRA IA · Haiku 4.5)
═══════════════════════════════════════════════════════════════════════════════════
ADR-031 capacidad INTERPRETACIÓN: QUIRA IA produce CRITERIO, no describe gráficos
(ADR-030 §4). Lee el estado VERIFICADO del MCD Planificación (snapshot) y emite el
peritaje metodológico que responde la pregunta del dominio.

  · Regla 1/3: NO inventa cifras — usa SOLO el dato del Canon (vía snapshot).
  · Firewall: lenguaje de gestión pública; cero jerga interna (SAT-x, índices, hojas).
  · Genera al ENRIQUECER (no en cada render UI): escribe planificacion.criterio_ia;
    el cajón solo lo lee. Fallback elegante: sin key/falla → no escribe → peritaje estático.

Modelo escudo Haiku 4.5 (claude-haiku-4-5 · $1/$5 · QUIRA_IA_BUCLES_AGENTICOS.md).
Uso:  python scripts/ia_criterio_planificacion.py
Dylus Lab © 2026
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
HAIKU_MODEL = "claude-haiku-4-5"

PREGUNTA = ("¿La institución sostiene la correspondencia con sus metas plurianuales, "
            "o registra desviaciones en su senda de desarrollo?")

_SYSTEM = (
    "Eres el perito metodológico de QUIRA — Centro de Inteligencia Territorial. Lees el estado "
    "VERIFICADO de la planificación estratégica de un municipio y emites un CRITERIO profesional: "
    "el juicio que responde la pregunta del dominio.\n"
    "REGLAS INVIOLABLES:\n"
    "1. NO inventes cifras ni hechos. Usa SOLO los datos provistos. Si algo no está, no lo afirmes.\n"
    "2. Lenguaje de gestión pública, claro para un alcalde. Prohibido: jerga técnica interna, siglas de "
    "índices, códigos de hoja o nombres de sistemas internos.\n"
    "3. Tono preventivo, NO acusatorio. Señala coherencias y brechas; nunca 'incumplió/violó/ilegal'.\n"
    "4. Conciso: 2 párrafos cortos. SIN encabezados markdown (# / ##) ni líneas divisorias (---); "
    "solo **negrita** para destacar 2-3 ideas.\n"
    "5. Cierra con una línea que empiece exactamente con '**Recomendación:**' seguida de UNA acción concreta."
)

_TEMP = {
    "verde": "coherencia sostenida entre plan y ejecución",
    "alerta": "señal preventiva activa — conviene revisar la coherencia plan↔contratación",
    "critico": "brecha crítica de coherencia que requiere atención",
    "dim": "señal aún sin determinar",
}


def _key() -> str:
    k = os.environ.get("ANTHROPIC_API_KEY", "")
    if k:
        return k
    try:
        p = REPO / ".streamlit" / "secrets.toml"
        if p.exists():
            m = re.search(r"(sk-ant-[A-Za-z0-9\-_]{20,})", p.read_text(encoding="utf-8"))
            if m:
                return m.group(1)
    except Exception:
        pass
    return ""


def _datos_firewall(p: dict) -> str:
    pac = p.get("pac", {}) or {}
    pub = p.get("publicado", {}) or {}
    cr = pub.get("cruce", {}) or {}
    pre = p.get("presupuesto", {}) or {}
    sat = p.get("sat0", {}) or {}
    comp = p.get("competencia", [])
    crit = sum(c.get("n", 0) for c in comp if "Crítica" in c.get("label", ""))
    poa_t = sum(x.get("anual", 0) for x in p.get("poa_proyectos", []))
    return "\n".join([
        f"- Metas del Plan de Desarrollo (PDOT) 2023-2027: {p.get('metas_total', 0)} "
        f"(de competencia crítica: {crit}).",
        f"- Plan Operativo Anual (POA) 2026: {len(p.get('poa_proyectos', []))} proyectos por ${poa_t:,.0f} "
        f"(monto operativo total — es MAYOR que la inversión codificada; no confundir ambos montos).",
        f"- Inversión codificada 2026: ${pre.get('codificado_inversion', 0):,.0f}. "
        f"Ejecución de esa inversión al corte: {pre.get('ti_pct', 0)}%.",
        f"- Plan Anual de Contratación (PAC) 2026: ${pac.get('total_usd', 0):,.0f} — cubre el 98.6% "
        f"de la inversión codificada (la línea anterior), NO del monto del POA.",
        f"- Publicado en contratación pública al corte: {pub.get('n_procesos', 0)} procesos por "
        f"${pub.get('total_usd', 0):,.0f} — el {cr.get('cobertura_pct', 0)}% del plan de contratación (PAC).",
        f"- Señal de coherencia plan↔contratación: {_TEMP.get(sat.get('global_temp', 'dim'), 'sin señal')}.",
    ])


def main() -> int:
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    plan = snap.get("planificacion", {})
    if not plan:
        print("[ERR] sin bloque 'planificacion' — corre enrich_planificacion.py")
        return 1
    key = _key()
    if not key:
        print("[skip] sin ANTHROPIC_API_KEY — el cajón usa el peritaje estático")
        return 0
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        datos = _datos_firewall(plan)
        user = (f"Pregunta del dominio:\n{PREGUNTA}\n\n"
                f"Estado verificado de la planificación 2026 (GAD Montecristi):\n{datos}\n\n"
                "Emite tu criterio metodológico (2 párrafos cortos + una recomendación accionable).")
        msg = client.messages.create(
            model=HAIKU_MODEL, max_tokens=600, system=_SYSTEM,
            messages=[{"role": "user", "content": user}])
        texto = msg.content[0].text.strip()
        # Limpieza defensiva (embebe en la card · independiente de si Haiku respetó el formato)
        texto = re.sub(r"(?m)^#{1,6}\s+.*$", "", texto)     # encabezados markdown
        texto = re.sub(r"(?m)^\s*-{3,}\s*$", "", texto)     # divisores ---
        texto = re.sub(r"\n{3,}", "\n\n", texto).strip()    # colapsa líneas en blanco
    except Exception as e:
        print(f"[skip] Haiku no disponible ({str(e)[:80]}) — el cajón usa el peritaje estático")
        return 0

    plan["criterio_ia"] = {"texto": texto, "modelo": HAIKU_MODEL, "fecha": date.today().isoformat()}
    snap["planificacion"] = plan
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — criterio IA generado ({len(texto)} chars) y escrito en el snapshot.")
    print("─" * 64)
    print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
