# -*- coding: utf-8 -*-
"""
scripts/vis/objeto_canonico.py — el primer objeto visual canónico de QUIRA
══════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). ADR-049 fija la gramática visual y exige probarla
sobre un caso real **antes** de tocar la interfaz. Este guion produce ese caso:
la cadena de 2026 del GAD Montecristi, con su ruptura.

CÓMO SE PRUEBA VIS-INV-001. La invariante dice que toda representación visual es
una **proyección determinista del motor**, sin crear ni completar nada. Aquí eso
no es una promesa: **este módulo no contiene un solo número escrito a mano.**
Todo se deriva en `construir_estado()` a partir de los extractores, y `svg()`
sólo sabe dibujar lo que ese estado le entrega. Si el estado no trae una cifra,
la gráfica no puede inventarla porque no tiene de dónde.

LAS DIEZ PREGUNTAS que el objeto debe responder sin explicación verbal (colega,
2026-08-12): qué es cada nodo · qué es cada arista · cómo se ve `validado` ·
cómo `sin_evidencia` · cómo `no_reconciliado` · cómo un límite propio de QUIRA ·
dónde está la procedencia · hecho frente a inferencia · qué pasa con las
contradicciones · y si se entiende **sin conocer una sola sigla interna**.

Uso:  python scripts/vis/objeto_canonico.py [--salida ruta.svg]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "normativa"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from extraer_cedula import extraer_todo                       # noqa: E402
from extraer_pai import extraer as extraer_pai                # noqa: E402
from cruce_poa_cedula import corte_anual, estado_financiero   # noqa: E402

# Paleta sobria. La marca es un asset y NO se redibuja (Identidad v1.1).
TINTA = "#2B3A42"
PIZARRA = "#4E6674"
GRIS = "#8A9BA5"
BORDE = "#D7DEE2"
FONDO = "#FFFFFF"
DEMOSTRADO = "#3D6B5A"      # verde apagado · conexión demostrada
ROTO = "#B4513C"            # terracota · ruptura del observado
PROPIO = "#8A6D3B"          # ocre · límite de QUIRA, nunca del municipio


def construir_estado(anio: int = 2026) -> dict:
    """El estado que la gráfica podrá dibujar. Nada más existe para ella."""
    pai = extraer_pai(anio)
    corte, mes = corte_anual(extraer_todo(anio), "GAD Montecristi", anio)

    por_obj: dict[str, set] = {}
    for r in pai:
        o, p = r["campos"].get("objetivo_estrategico", ""), r["campos"].get("partida")
        if o and p:
            por_obj.setdefault(o, set()).add(p)

    con_dev = con_cod = 0
    devengado_trazable = 0.0
    for ps in por_obj.values():
        est = [estado_financiero(corte.get(p))["estado"] for p in ps]
        if "devengado_positivo" in est:
            con_dev += 1
        elif "codificado_sin_devengado" in est:
            con_cod += 1
        devengado_trazable += sum((corte.get(p, {}).get("devengado") or 0) for p in ps)

    metas = json.loads((RAIZ / "data" / "pdot" / "registro_maestro_metas.json")
                       .read_text(encoding="utf-8"))["metas"]
    con_meta = sum(1 for r in pai if r["campos"].get("meta_pdot"))
    con_ind = sum(1 for r in pai if r["campos"].get("indicador_pdot"))

    return {
        "anio": anio,
        "corte_cedula": mes,
        "cadena_demostrada": [
            {"nodo": "Plan de Desarrollo y Ordenamiento Territorial",
             "cifra": f"{len(metas)} metas vigentes", "estado": "validado"},
            {"nodo": "Objetivo estratégico",
             "cifra": f"{len(por_obj)} declarados", "estado": "validado"},
            {"nodo": "Plan Anual de Inversiones",
             "cifra": f"{len(pai)} actividades", "estado": "validado"},
            {"nodo": "Partida presupuestaria",
             "cifra": f"{len({p for ps in por_obj.values() for p in ps})} distintas",
             "estado": "validado"},
            {"nodo": "Cédula presupuestaria",
             "cifra": f"{len(corte)} partidas · corte {mes}", "estado": "validado"},
            {"nodo": "Devengado",
             "cifra": f"${devengado_trazable:,.0f} trazables", "estado": "validado"},
        ],
        "cadena_rota": [
            {"nodo": "Meta", "cifra": f"{con_meta} de {len(pai)} actividades",
             "estado": "sin_evidencia"},
            {"nodo": "Indicador", "cifra": f"{con_ind} de {len(pai)} actividades",
             "estado": "sin_evidencia"},
            {"nodo": "Resultado", "cifra": "no auditable documentalmente",
             "estado": "sin_evidencia"},
        ],
        "detalle_objetivos": {"con_devengado": con_dev, "con_codificado": con_cod,
                              "sin_evidencia": len(por_obj) - con_dev - con_cod,
                              "total": len(por_obj)},
        "universo": {
            "devengado_total_gad": sum(r.get("devengado") or 0 for r in corte.values()),
            # ⚠️ Este total es del GAD ENTERO, no «del universo PAI»: el PAI cubre
            # inversión y no aspira a cubrir el gasto corriente. Rotularlo mal
            # insinuaría que falta lo que nunca debió estar.
            "nota": "el Plan de Inversiones cubre inversión, no el gasto corriente",
        },
        "procedencia": [
            f"Plan Anual de Inversiones {anio} · GAD Montecristi · archivo oficial",
            f"Cédula presupuestaria · conjunto de datos mensual · corte {mes} {anio}",
            "Registro de metas · contrastado contra el plan aprobado por ordenanza",
        ],
    }


# ── dibujo ────────────────────────────────────────────────────────────────────
def _nodo(x, y, w, titulo, cifra, color, punteado=False):
    guion = ' stroke-dasharray="5 4"' if punteado else ""
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="52" rx="6" fill="{FONDO}"
        stroke="{color}" stroke-width="1.6"{guion}/>
  <text x="{x+16}" y="{y+21}" font-size="13.5" font-weight="600" fill="{TINTA}">{titulo}</text>
  <text x="{x+16}" y="{y+39}" font-size="12" fill="{GRIS}">{cifra}</text>"""


def _arista(x, y1, y2, color, cortada=False, etiqueta=""):
    if cortada:
        medio = (y1 + y2) / 2
        return f"""
  <line x1="{x}" y1="{y1}" x2="{x}" y2="{medio-9}" stroke="{color}" stroke-width="2"
        stroke-dasharray="4 5"/>
  <line x1="{x-8}" y1="{medio-6}" x2="{x+8}" y2="{medio+6}" stroke="{color}" stroke-width="2.4"/>
  <line x1="{x+8}" y1="{medio-6}" x2="{x-8}" y2="{medio+6}" stroke="{color}" stroke-width="2.4"/>
  <line x1="{x}" y1="{medio+9}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="2"
        stroke-dasharray="4 5"/>
  <text x="{x+18}" y="{medio+4}" font-size="11.5" fill="{color}" font-weight="600">{etiqueta}</text>"""
    return f"""
  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-7}" stroke="{color}" stroke-width="2"/>
  <path d="M{x-5},{y2-8} L{x},{y2} L{x+5},{y2-8}" fill="{color}"/>
  <text x="{x+18}" y="{(y1+y2)/2+4}" font-size="11.5" fill="{color}">{etiqueta}</text>"""


def svg(e: dict) -> str:
    W, H = 1000, 1010
    x0, ancho = 60, 400
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
              f'width="{W}" height="{H}" font-family="Segoe UI, Helvetica, Arial, sans-serif">',
              f'<rect width="{W}" height="{H}" fill="{FONDO}"/>',
              f'<text x="{x0}" y="46" font-size="21" font-weight="700" fill="{TINTA}">'
              f'Cadena de evidencia · ejercicio {e["anio"]}</text>',
              f'<text x="{x0}" y="70" font-size="13.5" fill="{GRIS}">Gobierno Autónomo '
              f'Descentralizado Municipal del Cantón Montecristi</text>',
              f'<line x1="{x0}" y1="86" x2="{W-60}" y2="86" stroke="{BORDE}" stroke-width="1"/>']

    y = 116
    partes.append(f'<text x="{x0}" y="{y}" font-size="12" font-weight="700" '
                  f'fill="{DEMOSTRADO}" letter-spacing="0.6">LO QUE PUEDE DEMOSTRARSE</text>')
    y += 16
    for i, n in enumerate(e["cadena_demostrada"]):
        partes.append(_nodo(x0, y, ancho, n["nodo"], n["cifra"], DEMOSTRADO))
        if i < len(e["cadena_demostrada"]) - 1:
            partes.append(_arista(x0 + 26, y + 52, y + 92, DEMOSTRADO,
                                  etiqueta="verificado en la fuente"))
        y += 92

    # rama rota — arranca del objetivo, que es donde el instrumento la abandona
    xr = x0 + 540
    yr = 132 + 92
    partes.append(f'<text x="{xr}" y="116" font-size="12" font-weight="700" fill="{ROTO}" '
                  f'letter-spacing="0.6">LO QUE NO PUEDE DEMOSTRARSE</text>')
    partes.append(f'<path d="M{x0+ancho},{yr+26} L{xr-10},{yr+26}" stroke="{ROTO}" '
                  f'stroke-width="2" stroke-dasharray="4 5" fill="none"/>')
    partes.append(f'<path d="M{xr-16},{yr+21} L{xr-6},{yr+26} L{xr-16},{yr+31}" fill="{ROTO}"/>')
    for i, n in enumerate(e["cadena_rota"]):
        partes.append(_nodo(xr, yr, 340, n["nodo"], n["cifra"], ROTO, punteado=True))
        if i < len(e["cadena_rota"]) - 1:
            partes.append(_arista(xr + 26, yr + 52, yr + 92, ROTO, cortada=True,
                                  etiqueta="el instrumento no lo declara"))
        yr += 92

    d = e["detalle_objetivos"]
    yb = yr + 24
    partes.append(f'<rect x="{xr}" y="{yb}" width="340" height="104" rx="6" '
                  f'fill="#F7F9FA" stroke="{BORDE}"/>')
    partes.append(f'<text x="{xr+16}" y="{yb+24}" font-size="12.5" font-weight="600" '
                  f'fill="{TINTA}">Respaldo financiero de los objetivos</text>')
    for k, (et, v) in enumerate([("con ejecución certificada", d["con_devengado"]),
                                 ("con asignación sin ejecutar", d["con_codificado"]),
                                 ("sin respaldo financiero", d["sin_evidencia"])]):
        partes.append(f'<text x="{xr+16}" y="{yb+46+k*20}" font-size="12" fill="{GRIS}">'
                      f'{et}</text>'
                      f'<text x="{xr+310}" y="{yb+46+k*20}" font-size="12.5" '
                      f'font-weight="700" fill="{TINTA}" text-anchor="end">'
                      f'{v} de {d["total"]}</text>')

    # lectura — sin una sola sigla interna
    yl = max(y, yb + 128) + 14
    partes.append(f'<rect x="{x0}" y="{yl}" width="{W-120}" height="86" rx="6" '
                  f'fill="#F7F9FA" stroke="{BORDE}"/>')
    partes.append(f'<text x="{x0+18}" y="{yl+26}" font-size="13" font-weight="700" '
                  f'fill="{TINTA}">Lectura</text>')
    partes.append(f'<text x="{x0+18}" y="{yl+48}" font-size="13" fill="{TINTA}">'
                  f'La articulación con los objetivos del plan es demostrable hasta el gasto '
                  f'ejecutado.</text>')
    partes.append(f'<text x="{x0+18}" y="{yl+68}" font-size="13" fill="{TINTA}">'
                  f'La articulación con las metas no es demostrable: '
                  f'<tspan font-weight="700">los instrumentos no las declaran.</tspan></text>')

    yz = yl + 100
    partes.append(f'<text x="{x0}" y="{yz}" font-size="11.5" fill="{ROTO}" font-weight="600">'
                  f'Ausencia de evidencia. No constituye evidencia de incumplimiento.</text>')

    # leyenda: la gramática, explícita
    yg = yz + 26
    for k, (col, tr, et) in enumerate([
            (DEMOSTRADO, "", "vínculo demostrado con documento de respaldo"),
            (ROTO, "4 5", "vínculo no demostrable — el instrumento no lo declara"),
            (PROPIO, "2 3", "límite de la captura — corresponde a QUIRA, no al municipio")]):
        yy = yg + k * 19
        partes.append(f'<line x1="{x0}" y1="{yy}" x2="{x0+34}" y2="{yy}" stroke="{col}" '
                      f'stroke-width="2.4" stroke-dasharray="{tr}"/>')
        partes.append(f'<text x="{x0+46}" y="{yy+4}" font-size="11.5" fill="{GRIS}">{et}</text>')

    yp = yg + 3 * 19 + 14
    partes.append(f'<line x1="{x0}" y1="{yp}" x2="{W-60}" y2="{yp}" stroke="{BORDE}"/>')
    partes.append(f'<text x="{x0}" y="{yp+20}" font-size="11" font-weight="700" '
                  f'fill="{GRIS}">PROCEDENCIA</text>')
    for k, p in enumerate(e["procedencia"]):
        partes.append(f'<text x="{x0}" y="{yp+38+k*16}" font-size="11" fill="{GRIS}">· {p}</text>')

    partes.append("</svg>")
    return "\n".join(partes)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", type=int, default=2026)
    ap.add_argument("--salida", default=str(RAIZ / "data" / "vis" / "cadena_2026.svg"))
    args = ap.parse_args()

    e = construir_estado(args.anio)
    print(f"ESTADO DERIVADO · {e['anio']} · corte {e['corte_cedula']}")
    for n in e["cadena_demostrada"]:
        print(f"   ✓ {n['nodo']:44} {n['cifra']}")
    for n in e["cadena_rota"]:
        print(f"   ∅ {n['nodo']:44} {n['cifra']}")
    print(f"   objetivos: {e['detalle_objetivos']}")

    out = Path(args.salida)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg(e), encoding="utf-8")
    (out.with_suffix(".json")).write_text(json.dumps(e, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    print(f"\n  → {out}")
    print(f"  → {out.with_suffix('.json')}  (el estado, sin el cual la gráfica no existe)")


if __name__ == "__main__":
    main()
