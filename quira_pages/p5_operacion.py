"""
QUIRA OS v0.1 — P-05 Operación Técnica
P-17 Ingesta · P-18 Validador · P-19 HITL
Fiel al DEMO.html P-17/18/19 · st.components.v1.html() render
Dylus Lab © 2026
"""
import streamlit as st
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ─── P-17 INGESTA DE CUMPLIMIENTO ────────────────────────────────────────────
def _p17_html(show_tech: bool) -> str:
    hdr = page_header(
        "⑦ OPERACIÓN TÉCNICA · BACKOFFICE",
        "Ingesta de Cumplimiento",
        "Carga mensual de reportes · 6 Direcciones + Adscritas · Protocolo HITL · QUIRA OS",
    )

    banner = """
<div style="padding:12px 16px;background:rgba(124,92,252,.07);
            border:1px solid rgba(124,92,252,.25);border-radius:10px;
            margin-bottom:16px;display:flex;align-items:center;gap:12px">
  <div style="font-size:28px">📥</div>
  <div style="flex:1">
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:3px">
      QUIRA OS · Backoffice Operativo · Streamlit v0.1
    </div>
    <div style="font-size:11px;color:var(--muted)">
      Este módulo operará en <strong style="color:var(--white)">QUIRA OS (Streamlit)</strong> —
      no en el HTML institucional. Aquí: protocolo, arquitectura y estado de ingesta del sistema
      mensualizado.
    </div>
  </div>
  <span class="badge" style="background:rgba(124,92,252,.2);color:var(--purple);
                              font-size:9px;white-space:nowrap">En construcción</span>
</div>"""

    pasos = """
<div class="card">
  <div class="card-title">Protocolo de Ingesta · 4 pasos mensuales</div>
  <div style="display:flex;flex-direction:column;gap:8px">
    <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;
                background:rgba(0,212,255,.05);border-radius:8px;border-left:3px solid var(--cyan)">
      <div style="font-size:15px;font-weight:800;color:var(--cyan);min-width:20px">①</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:var(--cyan)">Carga de informe</div>
        <div style="font-size:11px;color:var(--muted)">
          Responsable de dirección sube PDF firmado + avance de meta + evidencias eSIGEF.
        </div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;
                background:rgba(0,224,150,.05);border-radius:8px;border-left:3px solid var(--green)">
      <div style="font-size:15px;font-weight:800;color:var(--green);min-width:20px">②</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:var(--green)">Extracción IA</div>
        <div style="font-size:11px;color:var(--muted)">
          SENTINEL extrae KPIs, detecta incoherencias y compara con el mes anterior.
          Genera borrador de validación automática.
        </div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;
                background:rgba(255,183,0,.05);border-radius:8px;border-left:3px solid var(--amber)">
      <div style="font-size:15px;font-weight:800;color:var(--amber);min-width:20px">③</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:var(--amber)">Revisión HITL</div>
        <div style="font-size:11px;color:var(--muted)">
          Técnico de Planificación revisa el borrador: aprueba, rechaza o agrega observaciones.
          Sin validación humana, ningún dato entra al motor.
        </div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:flex-start;padding:10px;
                background:rgba(124,92,252,.05);border-radius:8px;border-left:3px solid var(--purple)">
      <div style="font-size:15px;font-weight:800;color:var(--purple);min-width:20px">④</div>
      <div>
        <div style="font-size:12px;font-weight:700;color:var(--purple)">Actualización ICGI-T</div>
        <div style="font-size:11px;color:var(--muted)">
          Motor SIAP-ICPI recalcula el índice. QUIRA Gov se actualiza.
          Trazabilidad SHA-256 generada.
        </div>
      </div>
    </div>
  </div>
</div>"""

    tabla_ingesta = """
<div class="card">
  <div class="card-title">
    Estado de Ingesta · Mayo 2026
    <span class="badge badge-amber" style="float:right">mockup</span>
  </div>
  <table class="tbl">
    <thead><tr><th>Unidad</th><th>Informe</th><th>eSIGEF</th><th>Estado</th></tr></thead>
    <tbody>
      <tr>
        <td><span style="color:var(--cyan);font-weight:700">DAPS-01</span>
            <span style="font-size:9px;color:var(--muted)"> Agua y Saneamiento</span></td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td><span style="font-size:9px;color:var(--amber)">Pendiente</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--cyan);font-weight:700">DOP-01</span>
            <span style="font-size:9px;color:var(--muted)"> Obras Públicas</span></td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td><span style="font-size:9px;color:var(--amber)">Pendiente</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--cyan);font-weight:700">FIN-01</span>
            <span style="font-size:9px;color:var(--muted)"> Dir. Financiera</span></td>
        <td style="text-align:center;color:var(--green)">✅</td>
        <td style="text-align:center;color:var(--green)">✅</td>
        <td><span style="font-size:9px;color:var(--green)">Validado</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--cyan);font-weight:700">RR.HH-01</span>
            <span style="font-size:9px;color:var(--muted)"> Recursos Humanos</span></td>
        <td style="text-align:center;color:var(--red)">❌</td>
        <td style="text-align:center;color:var(--muted)">—</td>
        <td><span style="font-size:9px;color:var(--red)">Sin carga</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--green);font-weight:700">🚒 BOMB</span>
            <span style="font-size:9px;color:var(--muted)"> Bomberos</span></td>
        <td style="text-align:center;color:var(--green)">✅</td>
        <td style="text-align:center;color:var(--green)">✅</td>
        <td><span style="font-size:9px;color:var(--green)">Validado</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--amber);font-weight:700">🗑️ EP ASEO</span>
            <span style="font-size:9px;color:var(--muted)"> EP Aseo Municipal</span></td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td style="text-align:center;color:var(--red)">❌</td>
        <td><span style="font-size:9px;color:var(--red)">Incompleto</span></td>
      </tr>
      <tr>
        <td><span style="color:var(--green);font-weight:700">🤝 PAT</span>
            <span style="font-size:9px;color:var(--muted)"> Patronato</span></td>
        <td style="text-align:center;color:var(--green)">✅</td>
        <td style="text-align:center;color:var(--amber)">⏳</td>
        <td><span style="font-size:9px;color:var(--amber)">En revisión</span></td>
      </tr>
    </tbody>
  </table>
  <div style="margin-top:8px;padding:8px;background:rgba(124,92,252,.05);border-radius:6px;
              font-size:10px;color:var(--muted)">
    ℹ️ Lógica real de cargas y validación disponible en
    <strong style="color:var(--purple)">QUIRA OS · Streamlit v0.1</strong>.
    Este mockup muestra la estructura operativa del sistema.
  </div>
  <div style="display:inline-block;margin-top:12px;padding:8px 12px;
              background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
              border-radius:8px;font-size:12px;color:var(--cyan)">
    🔧 SENTINEL · Protocolo de ingesta
  </div>
</div>"""

    grid = (
        f'<div class="grid-2" style="align-items:start;gap:14px">'
        f'{pasos}{tabla_ingesta}'
        f'</div>'
    )

    return hdr + banner + grid


# ─── P-18 VALIDADOR CRUZADO ───────────────────────────────────────────────────
def _p18_html(show_tech: bool) -> str:
    hdr = page_header(
        "⑦ OPERACIÓN TÉCNICA · BACKOFFICE",
        "Validador Cruzado",
        "¿Lo reportado coincide con lo oficialmente ejecutado? · Doble filtro QUIRA · QUIRA OS",
    )

    banner = """
<div style="padding:12px 16px;background:rgba(124,92,252,.07);
            border:1px solid rgba(124,92,252,.25);border-radius:10px;
            margin-bottom:16px;display:flex;align-items:center;gap:12px">
  <div style="font-size:28px">🔍</div>
  <div>
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:3px">
      QUIRA OS · Validador Cruzado · Streamlit v0.1
    </div>
    <div style="font-size:11px;color:var(--muted)">
      Cruza <strong style="color:var(--white)">4 fuentes</strong> ×
      <strong style="color:var(--white)">25 metas</strong> ×
      <strong style="color:var(--white)">6 direcciones</strong>.
      Detecta brechas antes de que lleguen al índice y generen riesgo institucional.
    </div>
  </div>
</div>"""

    fuentes = """
<div class="grid-4" style="margin-bottom:14px">
  <div style="padding:11px;background:var(--navy-card);border-radius:8px;
              border-top:3px solid var(--cyan);text-align:center">
    <div style="font-size:20px;margin-bottom:5px">📄</div>
    <div style="font-size:11px;font-weight:700;color:var(--cyan)">Informe humano</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">
      Lo que el director dice que ejecutó
    </div>
  </div>
  <div style="padding:11px;background:var(--navy-card);border-radius:8px;
              border-top:3px solid var(--green);text-align:center">
    <div style="font-size:20px;margin-bottom:5px">📋</div>
    <div style="font-size:11px;font-weight:700;color:var(--green)">PAC SERCOP</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Procesos contratados oficialmente</div>
  </div>
  <div style="padding:11px;background:var(--navy-card);border-radius:8px;
              border-top:3px solid var(--amber);text-align:center">
    <div style="font-size:20px;margin-bottom:5px">💰</div>
    <div style="font-size:11px;font-weight:700;color:var(--amber)">Devengado eSIGEF</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Lo que realmente se pagó</div>
  </div>
  <div style="padding:11px;background:var(--navy-card);border-radius:8px;
              border-top:3px solid var(--red);text-align:center">
    <div style="font-size:20px;margin-bottom:5px">🏛️</div>
    <div style="font-size:11px;font-weight:700;color:var(--red)">Presupuesto aprobado</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Lo que el Concejo autorizó</div>
  </div>
</div>"""

    pregunta = """
<div style="padding:14px 18px;
            background:linear-gradient(135deg,rgba(124,92,252,.08) 0%,rgba(0,212,255,.05) 100%);
            border:1px solid rgba(124,92,252,.2);border-radius:10px;
            margin-bottom:14px;text-align:center">
  <div style="font-size:14px;font-weight:800;color:var(--white);font-style:italic">
    "¿Lo reportado coincide con lo oficialmente ejecutado?"
  </div>
  <div style="font-size:11px;color:var(--muted);margin-top:6px">
    Si la respuesta es NO en cualquier fuente →
    alerta automática → revisión HITL → trazabilidad SHA-256
  </div>
</div>"""

    brechas = """
<div class="card">
  <div class="card-title">4 tipos de brecha que detecta</div>
  <div style="display:flex;flex-direction:column;gap:7px">
    <div style="padding:8px;background:rgba(255,77,109,.05);border-radius:6px;
                border-left:3px solid var(--red);font-size:11px;color:var(--muted)">
      <strong style="color:var(--red)">C1 — Gasto no reportado:</strong>
      eSIGEF muestra devengado pero no hay informe de dirección correspondiente.
    </div>
    <div style="padding:8px;background:rgba(255,183,0,.05);border-radius:6px;
                border-left:3px solid var(--amber);font-size:11px;color:var(--muted)">
      <strong style="color:var(--amber)">C2 — PAC fantasma:</strong>
      Proceso en PAC sin respaldo en devengado eSIGEF. Posible proceso no ejecutado.
    </div>
    <div style="padding:8px;background:rgba(255,77,109,.05);border-radius:6px;
                border-left:3px solid var(--red);font-size:11px;color:var(--muted)">
      <strong style="color:var(--red)">C3 — Sobrereporte:</strong>
      Informe humano declara avance superior al devengado real.
    </div>
    <div style="padding:8px;background:rgba(255,183,0,.05);border-radius:6px;
                border-left:3px solid var(--amber);font-size:11px;color:var(--muted)">
      <strong style="color:var(--amber)">C4 — Gasto ciego:</strong>
      Devengado sin proceso PAC ni SHA-256.
      <strong style="color:var(--red)">24 activos Q1-2026 · SAT-0 activo.</strong>
    </div>
  </div>
</div>"""

    flujo = """
<div class="card">
  <div class="card-title">Flujo de validación QUIRA</div>
  <div style="display:flex;flex-direction:column;gap:0">
    <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;color:var(--muted)">
      <span style="color:var(--cyan);font-weight:700;min-width:18px">①</span>
      Carga de fuentes (H05 POA · H05b PAC · H07 eSIGEF · Informe PDF)
    </div>
    <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;color:var(--muted)">
      <span style="color:var(--cyan);font-weight:700;min-width:18px">②</span>
      Cruce automático: 4 fuentes × 25 metas × 6 direcciones
    </div>
    <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;color:var(--muted)">
      <span style="color:var(--amber);font-weight:700;min-width:18px">③</span>
      Brechas detectadas → clasificadas C1/C2/C3/C4 → notificación HITL
    </div>
    <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                border-bottom:1px solid rgba(255,255,255,.05);font-size:11px;color:var(--muted)">
      <span style="color:var(--green);font-weight:700;min-width:18px">④</span>
      Técnico resuelve cada brecha → registro SHA-256
    </div>
    <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
                font-size:11px;color:var(--muted)">
      <span style="color:var(--purple);font-weight:700;min-width:18px">⑤</span>
      Motor ICGI-T recalcula → QUIRA Gov se actualiza → PDF certificado
    </div>
  </div>
  <div style="margin-top:10px;padding:8px;background:rgba(124,92,252,.05);border-radius:6px;
              font-size:10px;color:var(--muted)">
    ℹ️ Implementación completa en
    <strong style="color:var(--purple)">QUIRA OS · Streamlit v0.1</strong>
  </div>
  <div style="display:inline-block;margin-top:12px;padding:8px 12px;
              background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
              border-radius:8px;font-size:12px;color:var(--cyan)">
    🔍 SENTINEL · Análisis de brechas cruzadas
  </div>
</div>"""

    grid = (
        f'<div class="grid-2" style="align-items:start;gap:14px">'
        f'{brechas}{flujo}'
        f'</div>'
    )

    return hdr + banner + fuentes + pregunta + grid


# ─── P-19 AUDITOR HITL ────────────────────────────────────────────────────────
def _p19_html(show_tech: bool) -> str:
    hdr = page_header(
        "⑦ OPERACIÓN TÉCNICA · BACKOFFICE",
        "Auditor HITL",
        "Human-in-the-Loop · IA propone · Técnico decide · Trazabilidad total · QUIRA OS",
    )

    banner = """
<div style="padding:12px 16px;background:rgba(124,92,252,.07);
            border:1px solid rgba(124,92,252,.25);border-radius:10px;
            margin-bottom:16px;display:flex;align-items:center;gap:12px">
  <div style="font-size:28px">🧠</div>
  <div>
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:3px">
      HITL — Human-in-the-Loop · QUIRA OS · Streamlit v0.1
    </div>
    <div style="font-size:11px;color:var(--muted)">
      La IA detecta inconsistencias y propone clasificaciones. El técnico aprueba, rechaza o comenta.
      <strong style="color:var(--white)">Sin validación humana, ningún dato entra al motor ICGI-T.</strong>
    </div>
  </div>
</div>"""

    principio = """
<div style="padding:14px 18px;
            background:linear-gradient(135deg,rgba(0,224,150,.07) 0%,rgba(124,92,252,.04) 100%);
            border:1px solid rgba(0,224,150,.18);border-radius:10px;margin-bottom:14px">
  <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:10px">
    ⚖️ Principio HITL de QUIRA
  </div>
  <div style="display:grid;grid-template-columns:1fr 40px 1fr;gap:8px;align-items:center;text-align:center">
    <div style="padding:10px;background:rgba(0,212,255,.06);border-radius:8px;
                border:1px solid rgba(0,212,255,.15)">
      <div style="font-size:20px;margin-bottom:4px">🤖</div>
      <div style="font-size:11px;font-weight:700;color:var(--cyan)">IA propone</div>
      <div style="font-size:10px;color:var(--muted)">Detecta · Clasifica · Sugiere</div>
    </div>
    <div style="font-size:20px;color:var(--purple)">⟷</div>
    <div style="padding:10px;background:rgba(0,224,150,.06);border-radius:8px;
                border:1px solid rgba(0,224,150,.15)">
      <div style="font-size:20px;margin-bottom:4px">👤</div>
      <div style="font-size:11px;font-weight:700;color:var(--green)">Técnico decide</div>
      <div style="font-size:10px;color:var(--muted)">Aprueba · Rechaza · Comenta</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:11px;color:var(--muted);text-align:center">
    El HITL reduce la carga manual ≥70% y garantiza que la experiencia institucional del técnico
    nunca sea reemplazada — sino amplificada.
  </div>
</div>"""

    ejemplo = """
<div class="card">
  <div class="card-title">
    Ejemplo · Hallazgo IA + Decisión HITL
    <span class="badge badge-amber" style="float:right">mockup</span>
  </div>
  <div style="padding:10px;background:rgba(255,77,109,.06);border-radius:8px;
              border:1px solid rgba(255,77,109,.2);margin-bottom:10px">
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-bottom:4px">
      🤖 SENTINEL detectó — Mayo 2026
    </div>
    <div style="font-size:11px;color:var(--white);margin-bottom:4px">
      EP Aseo reporta ejecución $280K en informe de dirección, pero eSIGEF registra solo
      $118K devengado. Brecha: $162K sin trazabilidad.
    </div>
    <div style="font-size:10px;color:var(--amber)">
      Clasificación automática: Brecha C3 · Sobrereporte · Requiere evidencia adicional
    </div>
  </div>
  <div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;
              letter-spacing:.08em;margin-bottom:7px">Decisión del técnico:</div>
  <div style="display:flex;gap:6px;margin-bottom:10px">
    <div style="padding:6px 12px;background:rgba(0,224,150,.1);
                border:1px solid rgba(0,224,150,.3);border-radius:6px;
                font-size:11px;color:var(--green)">✅ Aprobar</div>
    <div style="padding:6px 12px;background:rgba(255,77,109,.1);
                border:1px solid rgba(255,77,109,.3);border-radius:6px;
                font-size:11px;color:var(--red)">❌ Rechazar</div>
    <div style="padding:6px 12px;background:rgba(255,183,0,.1);
                border:1px solid rgba(255,183,0,.3);border-radius:6px;
                font-size:11px;color:var(--amber)">💬 Comentar</div>
  </div>
  <div style="padding:8px;background:rgba(0,0,0,.15);border-radius:6px;
              font-size:10px;color:var(--muted);font-style:italic">
    "EP Aseo incluye $162K de contrato pendiente de certificación.
     Adjunto acta de recepción provisional..."
  </div>
  <div style="margin-top:8px;font-size:10px;color:var(--green);padding:6px;
              background:rgba(0,224,150,.04);border-radius:6px">
    → Resolución registrada · SHA-256 generado · Motor ICGI-T actualiza EP Aseo 58.4% → recalcula
  </div>
</div>"""

    roles = """
<div class="card">
  <div class="card-title">3 roles que operan el HITL</div>
  <div style="display:flex;flex-direction:column;gap:8px">
    <div style="display:flex;gap:10px;align-items:center;padding:8px;
                background:rgba(0,212,255,.05);border-radius:6px">
      <div style="font-size:16px">🔧</div>
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--cyan)">Técnico de Planificación</div>
        <div style="font-size:10px;color:var(--muted)">Valida metas, avances POA y evidencias documentales</div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;padding:8px;
                background:rgba(0,224,150,.05);border-radius:6px">
      <div style="font-size:16px">💰</div>
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--green)">Director Financiero</div>
        <div style="font-size:10px;color:var(--muted)">Certifica devengados eSIGEF y partidas presupuestarias</div>
      </div>
    </div>
    <div style="display:flex;gap:10px;align-items:center;padding:8px;
                background:rgba(255,183,0,.05);border-radius:6px">
      <div style="font-size:16px">📋</div>
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--amber)">Responsable de Compras</div>
        <div style="font-size:10px;color:var(--muted)">Verifica procesos PAC, SHA-256 y contratos SERCOP</div>
      </div>
    </div>
  </div>
</div>"""

    roadmap = """
<div class="card">
  <div class="card-title">Roadmap QUIRA</div>
  <div style="display:flex;flex-direction:column;gap:6px;font-size:11px;color:var(--muted)">
    <div style="display:flex;gap:8px;align-items:center">
      <span style="color:var(--green)">✅</span>
      <span><strong style="color:var(--white)">QUIRA Gov v1.0</strong>
            · HTML institucional · Freeze</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <span style="color:var(--amber)">🔄</span>
      <span><strong style="color:var(--white)">QUIRA OS v0.1</strong>
            · Streamlit · Dashboard + SENTINEL + GeoTwin + Backoffice</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <span style="color:var(--purple)">⏳</span>
      <span>QUIRA OS v0.2 · Ingesta P-17 + Validador P-18 + HITL P-19 completos</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
      <span style="color:var(--muted)">⏳</span>
      <span>QUIRA Citizen · PMV-2 · Auditoría social aumentada</span>
    </div>
  </div>
</div>"""

    right_col = (
        f'<div style="display:flex;flex-direction:column;gap:12px">'
        f'{roles}{roadmap}'
        f'<div style="display:inline-block;padding:8px 12px;'
        f'background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);'
        f'border-radius:8px;font-size:12px;color:var(--cyan)">'
        f'🧠 SENTINEL · Protocolo HITL completo'
        f'</div>'
        f'</div>'
    )

    grid = (
        f'<div class="grid-2" style="align-items:start;gap:14px">'
        f'{ejemplo}{right_col}'
        f'</div>'
    )

    return hdr + banner + principio + grid


# ─── MAIN RENDER ─────────────────────────────────────────────────────────────
def render() -> None:
    show_tech = is_tecnico()

    # Access check — only técnico roles
    if not show_tech:
        st.html("""
        <div style="background:rgba(229,62,62,0.08);border:1px solid rgba(229,62,62,0.25);
                    border-radius:12px;padding:20px 24px;margin:20px 0;text-align:center">
            <div style="font-size:1.2rem;margin-bottom:8px">🔒</div>
            <div style="font-size:14px;font-weight:700;color:#FC8181">Acceso Restringido</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-top:4px">
                Módulo disponible solo para el rol Técnico
            </div>
        </div>""")
        return

    tab1, tab2, tab3 = st.tabs([
        "📥 P-17 · Ingesta",
        "🔍 P-18 · Validador",
        "🧠 P-19 · Auditor HITL",
    ])

    with tab1:
        render_page(_p17_html(show_tech), show_tech=show_tech, height=900)

    with tab2:
        render_page(_p18_html(show_tech), show_tech=show_tech, height=950)

    with tab3:
        render_page(_p19_html(show_tech), show_tech=show_tech, height=950)

    st.html("<div style='height:8px'></div>")
    if st.button("🔮 Consultar SENTINEL sobre operación técnica", use_container_width=True):
        st.session_state["page"] = "sentinel"
        st.rerun()
