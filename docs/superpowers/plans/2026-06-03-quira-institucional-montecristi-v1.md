# QUIRA Institucional — Plan de Intervención · Montecristi v1.0

> **Para ejecución:** usar `superpowers:subagent-driven-development` o `superpowers:executing-plans` sprint por sprint.

**Goal:** Convertir QUIRA de 80% sistema / 20% producto → 80% producto / 20% sistema visible. Montecristi v1.0 completo antes de Gate 7 (Manta).

**Architecture:** app.py → env_gov.py (router puro) → páginas individuales. Cada sprint toca archivos específicos sin tocar el router. Bloomberg Firewall activo: nunca exponer ICPI/TGI/Ti/QTMP en labels públicos.

**Tech Stack:** Streamlit · Python · Claude Haiku (API) · Folium + streamlit-folium · Supabase · Neo4j · Gold Master vía `app/connectors/gold_master.py`

**UI Norte:** institucional · premium · territorial · ecuatoriana. NO SaaS genérico.

---

## ⚠️ CORRECCIONES AL ANÁLISIS DEL COLEGA

Antes de planificar, estas correcciones son necesarias:

### C1. GeoTwin NO es "desde cero"
`quira_pages/p4_geotwin.py` existe (327 líneas) con Folium + `data/parroquias_montecristi.geojson` funcional.
Sprint D = **conectar dominios al mapa existente**, no construir el mapa.
Alcance de D se reduce ~60%.

### C2. IED e ITAM — no confirmados en Gold Master
El colega los pone en la ficha cantonal. Gold Master confirma TGI 5D:
- D1 Trust Score = 83.5% (H89) ✅
- D2 ICPI = 69.93% ✅
- D3 Ti Inversión = 59.85% ✅
- D4 IET Rural = 44.79% (CRÍTICO) ✅
- D5 ICM SNP = 100% ✅

**IED e ITAM se eliminan de Sprint A hasta que Javo confirme su hoja en Gold Master.**
Si no están, no los inventamos — viola ADR-023.

### C3. Datos de Alcalde ya existen estáticos
`config.py` tiene: `ALCALDE = "Ing. Jonathan Toro Largacha"` · `GAD_PERIODO = "2023–2027"` · `CORTE = "Q1-2026"`.
El sitio web del GAD caído no bloquea Sprint A. La ficha arranca con datos estáticos, se etiqueta como "Corte Q1-2026".

### C4. #VALOR! en TGI Score del Excel
La celda TGI Score Global tiene `#VALOR!` en el Excel. El Gold Master connector puede devolver error.
Fix requerido: el conector debe calcular `16.70 + 13.99 + 14.96 + 11.20 + 10.00 = 66.85` o leer la suma directamente de H89.
Sprint A incluye este fix como Tarea 0.

### C5. Los 12 dominios EXISTEN en código
`_DOMAINS_12` en `p_command_center.py` tiene los 12 dominios con id, nombre, estado, métrica, narrativa y `mod` (página destino).
Sprint B = mejorar UX de navegación (puertas full-screen), no recrear la data.

---

## ROADMAP — 6 SPRINTS

```
Sprint A  →  Contexto Cantonal          (ficha viva · portada antes de los 12 dominios)
Sprint B  →  12 Puertas                 (cajones → navegación full-screen real)
Sprint C  →  Dashboard Dominio + IA     (QUIRA como analista, no chatbot)
Sprint D  →  GeoTwin Conectado          (dominio → mapa → parroquias relevantes)
Sprint E  →  QUIRA Operaciones          (módulo del técnico, sin Python/VSCode)
Sprint F  →  Montecristi v1.0           (integración, polish, UI review final)
           ↓
        GATE 7 — Manta (cuando el producto sea completo)
```

---

## SPRINT A — Contexto Cantonal

**Goal:** La pantalla de entrada de QUIRA muestra una ficha viva del cantón antes de los 12 dominios. El usuario entiende quién es Montecristi y su estado institucional en 10 segundos.

**Archivos:**
- Modificar: `quira_pages/p0_inicio.py` (252 líneas → reescribir layout)
- Modificar: `app/connectors/gold_master.py` → fix TGI Score #VALOR!
- Crear: `quira_pages/components/canton_card.py` (componente reutilizable)
- No tocar: `config.py`, `app.py`, `quira_pages/env_gov.py`

**Datos de la ficha (fuentes confirmadas):**

| Campo | Fuente | Valor actual |
|---|---|---|
| Alcalde | config.py | Ing. Jonathan Toro Largacha |
| Período | config.py | 2023–2027 |
| Corte | config.py | Q1-2026 |
| TGI Score | Gold Master H89 vía gold_master.py | ≈66.85% 🟡 |
| Trust Score (D1) | Gold Master H89 | 83.5% 🟢 |
| Cumplimiento Metas (D2) | Gold Master (ICPI) | 69.93% 🟡 |
| Ti Inversión (D3) | Gold Master | 59.85% 🟡 |
| IET Rural (D4) | Gold Master | 44.79% 🔴 CRÍTICO |
| ICM SNP (D5) | Gold Master | 100% 🟢 |
| Alertas activas | Supabase snapshot | dinámico |

**Labels públicos (Bloomberg Firewall):**
- D2 ICPI → "Cumplimiento de Metas PDyOT"
- D3 Ti → "Eficiencia de Inversión"
- D4 IET → "Equidad Territorial Rural"
- D5 ICM → "Reporte al SNP"
- TGI → "Índice de Gobernanza Territorial"

### Tarea A0: Fix #VALOR! en Gold Master connector

**Archivos:** `app/connectors/gold_master.py`

- [ ] Abrir `app/connectors/gold_master.py` y ubicar la función que lee TGI Score Global
- [ ] Si devuelve `#VALOR!` o None, calcular fallback: `D1*0.20 + D2*0.20 + D3*0.25 + D4*0.25 + D5*0.10`
  ```python
  def _calc_tgi_fallback(d1, d2, d3, d4, d5) -> float:
      """Fallback si H89 TGI Score Global tiene #VALOR!"""
      try:
          return round(d1*0.20 + d2*0.20 + d3*0.25 + d4*0.25 + d5*0.10, 2)
      except (TypeError, ValueError):
          return None
  ```
- [ ] Escribir test: `tests/connectors/test_gold_master_tgi.py`
  ```python
  def test_tgi_fallback_montecristi():
      result = _calc_tgi_fallback(83.5, 69.93, 59.85, 44.79, 100.0)
      assert abs(result - 66.85) < 0.1  # ≈66.85%
  ```
- [ ] Correr test: `python -m pytest tests/connectors/test_gold_master_tgi.py -v`
- [ ] Commit: `[connector]: fix TGI Score #VALOR! con fallback 5D ponderado`

### Tarea A1: Componente canton_card.py

**Archivos:** crear `quira_pages/components/canton_card.py`

- [ ] Crear el archivo:
  ```python
  """
  QUIRA — Componente Ficha Cantonal
  Muestra identidad + TGI 5D del GAD activo.
  Fuente de datos: config.py (estático) + Gold Master connector (métricas).
  Bloomberg Firewall: nunca usar ICPI/TGI/Ti como label público.
  """
  from __future__ import annotations
  import streamlit as st
  from config import GAD_NOMBRE, GAD_PERIODO, ALCALDE, CORTE
  
  _SEMAFORO = {
      "verde":   ("#22C55E", "🟢"),
      "amarillo":("#F59E0B", "🟡"),
      "rojo":    ("#EF4444", "🔴"),
  }
  
  def _color(pct: float | None) -> tuple[str, str]:
      if pct is None:   return _SEMAFORO["rojo"]
      if pct >= 75:     return _SEMAFORO["verde"]
      if pct >= 55:     return _SEMAFORO["amarillo"]
      return _SEMAFORO["rojo"]
  
  def render_canton_header(tgi_data: dict | None = None) -> None:
      """
      Renderiza la ficha cantonal completa.
      tgi_data: dict con keys d1,d2,d3,d4,d5,tgi_score (floats 0-100)
                Si None, muestra esqueleto con '—'.
      """
      d = tgi_data or {}
      tgi   = d.get("tgi_score")
      d1    = d.get("d1")  # Trust Score
      d2    = d.get("d2")  # ICPI → "Cumplimiento Metas"
      d3    = d.get("d3")  # Ti   → "Eficiencia Inversión"
      d4    = d.get("d4")  # IET  → "Equidad Territorial"
      d5    = d.get("d5")  # ICM  → "Reporte SNP"
  
      tgi_color, tgi_ico = _color(tgi)
      tgi_str = f"{tgi:.2f}%" if tgi else "—"
  
      # ── Ficha header ──────────────────────────────────────────────────────
      st.markdown(f"""
  <div style="background:linear-gradient(135deg,rgba(0,30,60,.97),rgba(0,15,35,.99));
              border:1px solid rgba(0,212,255,.15);border-radius:16px;
              padding:24px 28px;margin-bottom:20px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                flex-wrap:wrap;gap:16px">
      <!-- Identidad -->
      <div>
        <div style="font-size:9px;font-weight:700;letter-spacing:.12em;
                    color:rgba(0,212,255,.5);text-transform:uppercase;
                    margin-bottom:6px">GAD MUNICIPAL · PROVINCIA DE MANABÍ</div>
        <div style="font-size:1.6rem;font-weight:900;color:#E2E8F0;
                    letter-spacing:-.03em;line-height:1.1">MONTECRISTI</div>
        <div style="font-size:11px;color:rgba(255,255,255,.4);margin-top:4px">
            👤 {ALCALDE} &nbsp;·&nbsp; 📅 {GAD_PERIODO} &nbsp;·&nbsp; 📊 Corte {CORTE}</div>
      </div>
      <!-- TGI Score -->
      <div style="text-align:right">
        <div style="font-size:9px;font-weight:700;letter-spacing:.1em;
                    color:rgba(255,255,255,.3);text-transform:uppercase;
                    margin-bottom:4px">Índice de Gobernanza Territorial</div>
        <div style="font-size:2.4rem;font-weight:900;color:{tgi_color};
                    font-family:'JetBrains Mono',monospace;letter-spacing:-.04em">
            {tgi_ico} {tgi_str}</div>
        <div style="font-size:10px;color:rgba(255,255,255,.3);margin-top:2px">
            🟡 Transición con Riesgos</div>
      </div>
    </div>
    <!-- 5 dimensiones -->
    <div style="display:flex;gap:8px;margin-top:20px;flex-wrap:wrap">
  """ + _dim_pill("Gobernanza Metodológica", d1, "D1") +
        _dim_pill("Cumplimiento de Metas", d2, "D2") +
        _dim_pill("Eficiencia de Inversión", d3, "D3", critico=(d3 is not None and d3 < 55)) +
        _dim_pill("Equidad Territorial Rural", d4, "D4", critico=True) +
        _dim_pill("Reporte al SNP", d5, "D5") + """
    </div>
  </div>
  """, unsafe_allow_html=True)
  
  
  def _dim_pill(label: str, pct: float | None, dim: str, critico: bool = False) -> str:
      color, ico = _color(pct)
      val_str = f"{pct:.1f}%" if pct is not None else "—"
      border = f"border:1px solid {color}44;" if not critico else f"border:1px solid {color};box-shadow:0 0 8px {color}33;"
      return f"""
  <div style="flex:1;min-width:120px;background:rgba(255,255,255,.03);
              {border}border-radius:10px;padding:10px 14px">
    <div style="font-size:8px;font-weight:700;letter-spacing:.08em;
                color:rgba(255,255,255,.3);text-transform:uppercase;
                margin-bottom:5px">{dim} · {label}</div>
    <div style="font-size:1.2rem;font-weight:900;color:{color};
                font-family:'JetBrains Mono',monospace">{ico} {val_str}</div>
    {"<div style='font-size:8px;color:#EF4444;margin-top:3px;font-weight:700'>⚠ DIMENSIÓN CRÍTICA</div>" if critico else ""}
  </div>"""
  ```
- [ ] Correr Streamlit localmente y verificar que el componente renderiza sin error
- [ ] Commit: `[ui/sprint-a]: componente canton_card ficha viva Montecristi`

### Tarea A2: Reescribir p0_inicio.py

**Archivos:** modificar `quira_pages/p0_inicio.py`

- [ ] Reemplazar el layout actual por:
  1. `render_canton_header(tgi_data)` arriba — toda la pantalla
  2. Debajo: 4 KPI tiles (Alertas SAT · Fondos en riesgo · Cobertura Holding · Próxima acción)
  3. Botón prominente: "Ver análisis por dominio →" → navega a `p_command_center`
  4. Eliminar el layout anterior de ICPI + SAT cards genéricas
- [ ] Cargar tgi_data desde gold_master connector:
  ```python
  from app.connectors.gold_master import get_tgi_snapshot
  tgi_data = get_tgi_snapshot()  # dict con d1-d5 + tgi_score
  ```
- [ ] Verificar que todos los labels son Bloomberg-safe (no exponer ICPI, TGI, Ti crudos)
- [ ] Probar con usuario "Ejecutivo" y con usuario "Técnico" — misma pantalla para ambos
- [ ] Commit: `[ui/sprint-a]: p0_inicio reemplazado por ficha cantonal viva`

### Tarea A3: UI Review Sprint A

- [ ] Verificar en móvil (Chrome DevTools 375px): ficha responde bien
- [ ] Verificar en desktop (1440px): no se ve genérico
- [ ] Screenshot de antes/después
- [ ] Commit: `[ui/sprint-a]: ajustes responsive ficha cantonal`

---

## SPRINT B — 12 Puertas (resumen — plan detallado al iniciar)

**Goal:** Los 12 cajones de `p_command_center.py` se comportan como puertas, no como cards informativas. Click → pantalla completa del dominio. No modal. No popup.

**Archivos clave:**
- `quira_pages/p_command_center.py` (1022 líneas) — los `_DOMAINS_12` ya existen
- `quira_pages/env_gov.py` — agregar rutas de dominio en el router
- `quira_pages/components/domain_door.py` — nuevo componente de puerta

**Cambio clave vs. hoy:** hoy cada dominio navega a un módulo genérico (m1_situacion, m2_alertas). Sprint B crea rutas dedicadas `d01` → `d12` que cargarán el dashboard de dominio (Sprint C).

---

## SPRINT C — Dashboard por Dominio + QUIRA IA (resumen)

**Goal:** Cada dominio tiene su pantalla completa con métricas, documentos, hallazgos y QUIRA IA como analista territorial. No como chatbot.

**Archivos clave:**
- `quira_pages/components/domain_dashboard.py` — template compartido
- `quira_pages/domain_views/d01_planificacion.py` … `d12_proteccion.py` (12 archivos)
- Integración Claude Haiku (ya en stack) vía `app/services/` nuevo `quira_ia_domain.py`

**QUIRA IA:** genera análisis contextual por dominio consultando:
1. Métricas del Gold Master para ese dominio
2. Documentos trackeados en Supabase (corpus MNT_UUID de ese dominio)
3. Hallazgos de OBS-008/009
Resultado: párrafo de 3-5 líneas como analista, no como chatbot de preguntas.

---

## SPRINT D — GeoTwin Conectado (resumen)

**Goal:** El mapa de Montecristi (Folium + parroquias GeoJSON — ya existe) se conecta a los dominios. Seleccionar un dominio en el dashboard → el mapa ilumina las parroquias relevantes.

**Archivos clave:**
- `quira_pages/p4_geotwin.py` (327 líneas — base existente, NO reescribir)
- Agregar: capa de filtro por dominio
- Agregar: tooltip con datos del dominio por parroquia

**Alcance real (no el del colega):**
- Sprint D v1: mapa cantonal + filtro dominio → parroquias coloreadas por estado
- Sprint D v2 (futuro): geodatos de cobertura por barrio (requiere datos que no tenemos hoy)

---

## SPRINT E — QUIRA Operaciones (resumen)

**Goal:** El técnico municipal puede subir documentos, ejecutar el pipeline, ver cobertura y monitorear el sistema sin tocar Python ni VSCode.

**Archivos clave:**
- `quira_pages/env_ops.py` — extender con módulo de operaciones
- `quira_pages/ops/upload_wizard.py` — wizard de ingesta documentos
- `quira_pages/ops/coverage_dashboard.py` — estado de silos, cobertura MNT_UUID
- `quira_pages/ops/pipeline_runner.py` — ejecutar scripts via subprocess con feedback en UI

**Regla:** QUIRA Operaciones NO recalcula métricas (ADR-023). Solo ingest + tag + monitor.

---

## SPRINT F — Montecristi v1.0 (resumen)

**Goal:** Integración final. Todos los sprints funcionan juntos. UI consistency pass. Deploy a quiraholding.streamlit.app.

**Checklist:**
- [ ] Flujo completo: Ficha → Dominios → Dashboard → GeoTwin
- [ ] Bloomberg Firewall verificado en todos los módulos
- [ ] QUIRA Operaciones funcional con documento de prueba
- [ ] Health check verde (python scripts/ci/check_health.py)
- [ ] Tag `montecristi-v1.0` en git

---

## DECISIONES PENDIENTES DE JAVO

1. **IED e ITAM** — ¿están en alguna hoja del Gold Master? Si sí, ¿cuál? Si no, se eliminan de la ficha para siempre.
2. **Sprint B vs C orden** — ¿preferís tener las puertas funcionando (B) antes que el dashboard completo (C), o arrancamos C en paralelo?
3. **QUIRA Ciudadana** — confirmamos que va DESPUÉS de Sprint E (post-Operaciones). ¿De acuerdo?

---

*Plan v1.0 · Dylus Lab · 2026-06-03 · Director Técnico: Claude*
*Gate 7 (Manta) congelado hasta completar Sprint F*
