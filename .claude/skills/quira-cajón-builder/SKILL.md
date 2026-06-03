# /quira-cajón-builder — Constructor Canónico de Layer 2

Guía paso a paso para construir el dashboard (Layer 2) de cualquier cajón del Centro de Mando.
Aplica ADR-012: cada dominio debe pasar los 5 niveles antes de considerarse cerrado.

## Cuándo usar este skill

Cuando el usuario dice:
- "construir el cajón D0X"
- "enriquecer pXX_*.py con la vista ejecutiva"
- "hacer Layer 2 del dominio Y"
- "agregar la cadena causal a la vista de Z"

## Inputs requeridos

Antes de construir, pedir o verificar:

1. **Número de dominio** (D01-D12)
2. **Archivo del módulo** (pXX_*.py o mX_*.py)
3. **QTMP disponible?** Revisar `quira-os/data/qtmp/` — si hay circuito .yaml para este dominio
4. **Datos verificados?** Valores confirmados en Gold Master (estado: confirmado vs pendiente_validacion)
5. **Estado ADR-012** — qué niveles están completos para este dominio

## Proceso de construcción

### Nivel 0: Verificación ADR-012

```
¿Tiene norma identificada (C1, C2)?         → SÍ / NO
¿Tiene pregunta bautismal Cypher?           → SÍ / NO
¿Tiene cadena causal C3→C8 en QTMP?        → SÍ / NO
¿Tiene C9 verificable con fuente pública?   → SÍ / NO
¿Tiene C10 registrado en Beta Backlog?      → SÍ / NO
```

Si algún nivel es NO → documentar en Beta Backlog y proceder con los datos disponibles, marcando el estado epistémico.

### Nivel 1: Template de Layer 2

Todo módulo de dominio DEBE tener esta estructura:

```python
def render() -> None:
    """
    Layer 2 — [Nombre del Dominio]
    Dominio [DXX] · [Nombre largo]
    Sprint 3 Panel Estratégico
    """
    from utils.session import is_ejecutivo
    from utils.cache_quira import cargar_snapshot, cargar_gm_snapshot
    from utils.css_tokens import C

    # ── Banda de retorno al Centro de Mando (siempre arriba) ──────────────────
    _render_return_band()

    # ── Datos ─────────────────────────────────────────────────────────────────
    snap, _ = cargar_snapshot()
    gm      = cargar_gm_snapshot()

    # ── Sección 1: Semáforo y métrica principal ───────────────────────────────
    # [valor] [color semáforo] [label en lenguaje gobernanza]
    # SIN nomenclatura interna

    # ── Sección 2: Narrativa causal (lenguaje gobernanza) ────────────────────
    # "La norma [nombre ley] establece que [institución] debe [obligación]..."
    # "El resultado al corte [fecha] muestra [situación territorial]..."

    # ── Sección 3: Indicadores clave ─────────────────────────────────────────
    # Máximo 3-4 indicadores. Cada uno con valor + fuente pública.

    # ── Sección 4: Visualización ──────────────────────────────────────────────
    # Progress bar, barras comparativas, timeline — según el dominio

    # ── Sección 5: Pie de página con fuente ──────────────────────────────────
    # "Fuente: [nombre sistema oficial] · [fecha corte]"
    # NUNCA: Gold Master, H-series, ICPI, QTMP IDs
```

### Nivel 2: Banda de retorno obligatoria

```python
def _render_return_band() -> None:
    """Banda superior de retorno — persiste en drill-down Ejecutivo."""
    from utils.session import is_ejecutivo
    import streamlit as st

    if is_ejecutivo():
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("← Centro de Mando", key="back_to_cc"):
                st.session_state["gov_module"] = "inicio"
                st.rerun()
```

### Nivel 3: Semáforo canónico

```python
# Colores canónicos QUIRA
VERDE   = "#22C55E"   # ≥ umbral — en ruta
ALERTA  = "#F97316"   # próximo al umbral — monitoreo
CRITICO = "#EF4444"   # < umbral — brecha activa

def _semaforo_badge(valor: float, umbral: float, label: str) -> str:
    if valor >= umbral:
        color, estado = VERDE, "EN RUTA"
    elif valor >= umbral * 0.85:
        color, estado = ALERTA, "BAJO OBJETIVO"
    else:
        color, estado = CRITICO, "BRECHA CRÍTICA"

    return f"""
<div style="background:{color}18;border:1px solid {color}44;border-left:3px solid {color};
            border-radius:8px;padding:12px 16px;margin:8px 0">
  <span style="font-size:1.8rem;font-weight:900;color:{color}">{valor:.1f}%</span>
  <span style="font-size:0.75rem;color:{color};margin-left:8px;font-weight:700">{estado}</span>
  <div style="font-size:0.7rem;color:rgba(255,255,255,.4);margin-top:4px">{label}</div>
</div>"""
```

### Nivel 4: Narrativa causal canónica

La narrativa de cada dominio debe seguir este patrón:

```
"[Norma] establece que [Actor obligado] debe [Obligación específica].
Al corte [fecha], [Indicador observable en lenguaje ciudadano]: [valor].
[Interpretación territorial sin lenguaje acusatorio].
Fuente: [Sistema oficial público]."
```

Ejemplos correctos:
```
D12: "El Art. 35 de la Constitución establece que el Estado debe garantizar
     atención prioritaria a grupos vulnerables. Al corte noviembre 2025,
     el Patronato Municipal ejecutó el 50% de su presupuesto de inversión social.
     La inversión en programas de atención directa representa el 12.83% del
     presupuesto municipal total — 17.2 puntos bajo el umbral de referencia.
     Fuente: Sistema Integrado de Gestión Financiera (SIGEF) · noviembre 2025."
```

### Nivel 5: Estado epistémico en datos

Si un valor NO está confirmado, marcar visualmente:

```python
# Valor confirmado → mostrar con fuente
st.metric("Ejecución presupuestaria", "50.0%")
st.caption("Fuente: SIGEF · noviembre 2025 · 11 meses")

# Valor pendiente de validación → mostrar con asterisco
st.metric("Asignación normativa", "20.84% *")
st.caption("* Pendiente confirmación diciembre 2025 · Dirección Financiera GADMCM")

# Hipótesis → mostrar con badge
st.warning("Hipótesis en validación académica (H6): La baja ejecución del Patronato "
           "correlaciona con la brecha de servicios en Dom12. Pendiente: Red Académica.")
```

## Checklist de cierre de cajón

Antes de marcar el cajón como completo:

- [ ] Narrativa en lenguaje de gobernanza (sin términos internos)
- [ ] Semáforo con valor y fuente pública
- [ ] Banda de retorno al Centro de Mando funcional
- [ ] `/quira-language-guard` ejecutado — 0 violaciones
- [ ] Estado epistémico marcado (confirmado / pendiente / hipótesis)
- [ ] C10 registrado en Beta Backlog si hay incertidumbre metodológica
- [ ] Probado con rol Ejecutivo (sin sidebar, sin técnico)

## Dominios por prioridad de construcción

```
SPRINT 3 (Panel Estratégico):
  1. D12 — Protección Social     ← PRIMERO (único con QTMP completo)
  2. D06 — Salud Institucional   ← segunda prioridad (featured, ICPI)
  3. D05 — Holding Municipal     ← datos Holding disponibles
  4. D04 — Alertas               ← SAT ya operativo
  5. D09 — Rendición de Cuentas  ← checklist CPCCS disponible

BETA (cuando haya QTMP nuevo):
  6. D10 — Territorio            ← requiere QTMP EQUIDAD + vista Ejecutivo
  7. D03 — Seguimiento de Metas  ← PDOT atomizado (BETA-DOM04-001)
  8. D08 — Participación         ← datos presupuesto participativo
  9. D07 — Transparencia         ← LOTAIP verificado
  10. D01 — Planificación        ← PDOT + ODS Tracker
  11. D02 — Presupuesto          ← fondos cooperación
  12. D11 — Ecosistema           ← EN CONSTRUCCIÓN (Sin datos aún)
```
