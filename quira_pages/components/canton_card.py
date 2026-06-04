"""
QUIRA — Componente Ficha Cantonal (Sprint A)

Renderiza la identidad institucional del GAD activo.
Solo datos administrativos — sin índices metodológicos (Bloomberg Firewall).
Índices y dimensiones van en Sprint C (dashboards por dominio).

Fuentes:
  - config.py: GAD_NOMBRE, ALCALDE, GAD_PERIODO, CORTE
  - Constantes estáticas Sprint A (datos demográficos/presupuestarios verificados)
"""
from __future__ import annotations

import streamlit as st
from config import GAD_NOMBRE, ALCALDE, GAD_PERIODO, CORTE

# Datos estáticos Montecristi — verificados PDOT 2020-2035 y SIGEF año fiscal 2025
_CANTON = {
    "nombre":        "MONTECRISTI",
    "provincia":     "Manabí",
    "tipo":          "GAD Municipal",
    "poblacion":     "~32.000 hab.",
    "parroquias":    7,
    "parroquias_lst":"Montecristi · Chirijos · Leónidas Proaño · La Pila · Gral. Eloy Alfaro · Colorado · Isabel Muentes",
    "presupuesto":   "$54,2M",
    "presupuesto_lbl":"Presupuesto codificado año fiscal 2025 · Fuente: SIGEF",
    "pdot":          "PDOT 2020–2035 vigente · PUGS vigente",
}


def _kv_chip(label: str, value: str) -> str:
    return f"""
<div style="display:flex;flex-direction:column;gap:3px;
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.09);
            border-radius:10px;padding:12px 16px;flex:1;min-width:140px">
    <span style="font-size:9px;font-weight:700;letter-spacing:.1em;
                 color:rgba(255,255,255,.35);text-transform:uppercase">{label}</span>
    <span style="font-size:13px;font-weight:700;color:#E2E8F0;line-height:1.3">{value}</span>
</div>"""


def render_canton_header(sat_count: int = 0) -> None:
    """
    Renderiza la ficha cantonal de identidad institucional.

    sat_count: número de alertas SAT activas (se muestra si > 0).
    """
    c = _CANTON
    sat_html = ""
    if sat_count > 0:
        sat_html = f"""
<div style="display:inline-flex;align-items:center;gap:6px;
            background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.35);
            border-radius:6px;padding:4px 10px;margin-top:10px">
    <span style="font-size:11px;color:#EF4444;font-weight:700">
        🚨 {sat_count} alerta{"s" if sat_count > 1 else ""} de gestión activa{"s" if sat_count > 1 else ""}
    </span>
</div>"""

    st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(0,25,55,.97),rgba(0,12,30,.99));
            border:1px solid rgba(0,212,255,.12);border-radius:18px;
            padding:28px 32px;margin-bottom:24px">

  <!-- Cabecera: identidad + corte -->
  <div style="display:flex;justify-content:space-between;
              align-items:flex-start;flex-wrap:wrap;gap:12px;
              margin-bottom:20px">
    <div>
      <div style="font-size:9px;font-weight:700;letter-spacing:.14em;
                  color:rgba(0,212,255,.45);text-transform:uppercase;
                  margin-bottom:6px">{c["tipo"]} · PROVINCIA DE {c["provincia"].upper()}</div>
      <div style="font-size:1.75rem;font-weight:900;color:#F1F5F9;
                  letter-spacing:-.04em;line-height:1">{c["nombre"]}</div>
      <div style="font-size:12px;color:rgba(255,255,255,.45);margin-top:8px;
                  display:flex;flex-wrap:wrap;gap:8px;align-items:center">
        <span>👤 {ALCALDE}</span>
        <span style="color:rgba(255,255,255,.2)">·</span>
        <span>📅 Período {GAD_PERIODO}</span>
        <span style="color:rgba(255,255,255,.2)">·</span>
        <span>📊 Corte {CORTE}</span>
      </div>
      {sat_html}
    </div>
    <!-- Presupuesto destacado -->
    <div style="text-align:right">
      <div style="font-size:9px;font-weight:700;letter-spacing:.1em;
                  color:rgba(255,255,255,.3);text-transform:uppercase;
                  margin-bottom:4px">Presupuesto Anual</div>
      <div style="font-size:2.2rem;font-weight:900;color:#00D4FF;
                  letter-spacing:-.04em;line-height:1">{c["presupuesto"]}</div>
      <div style="font-size:9px;color:rgba(255,255,255,.25);margin-top:4px">
          Codificado · SIGEF · Año fiscal 2025</div>
    </div>
  </div>

  <!-- KPIs administrativos -->
  <div style="display:flex;gap:10px;flex-wrap:wrap">
    {_kv_chip("Población estimada", c["poblacion"])}
    {_kv_chip("Parroquias", str(c["parroquias"]) + " (1 urbana · 6 rurales)")}
    {_kv_chip("Planificación territorial", c["pdot"])}
    {_kv_chip("Municipio 001", "Laboratorio piloto · QUIRA v1.0")}
  </div>

  <!-- Parroquias -->
  <div style="margin-top:14px;padding-top:14px;
              border-top:1px solid rgba(255,255,255,.06)">
    <span style="font-size:9px;font-weight:700;letter-spacing:.1em;
                 color:rgba(255,255,255,.3);text-transform:uppercase">
        Parroquias
    </span>
    <span style="font-size:11px;color:rgba(255,255,255,.4);margin-left:10px">
        {c["parroquias_lst"]}
    </span>
  </div>

</div>
""", unsafe_allow_html=True)
