# D.3 — Pantalla Principal (Centro de Mando)
## QUIRA OS · Sprint D · GAD Montecristi

**Estado:** D.3a ✅ DESPLEGADO  
**Fecha:** 2026-05-28  
**Archivo:** `quira_pages/p_command_center.py`  
**Router:** `env_gov.py` — módulo "inicio" → `p_command_center`  

---

## D.3a — Skeleton Operacional ✅

### Qué se construyó

**BANDA VITAL** (top, thin)
- 4 chips de pulso: Cumplimiento Municipal · Alertas Activas · Holding Municipal · Fondos en Riesgo
- Datos desde snapshot + Gold Master JSON (fallback)
- Tipografía monoespaciada (JetBrains Mono) para valores numéricos
- Colores del semáforo canónico QUIRA (C.sem())
- Fondos en Riesgo: $3.66M fijo en D.3a (D.3b+ desde p18 live)

**MAPA VIVO** (center, dominant, full-width)
- Folium + CartoDB Dark Matter tiles (elegante, minimal)
- 7 puntos: círculos de estado coloreados por temperatura institucional
- Anillo exterior (glow) en estados EMERGENCIA / PRIORIDAD
- Tooltip HTML: nombre · estado · tipo · habitantes · inversión · agua
- Click en parroquia → navega a GeoTwin (técnico) o Situación (directivo)
- Height: 460px — gravedad visual máxima

**CINTURÓN DE CAPAS** (bottom)
- 4 columnas: POLÍTICA · EJECUTIVA · RENDICIÓN · TERRITORIAL
- 13 dominios con temperatura (color) · gravedad (tamaño) · actividad (dot animado)
- Actividad: activo = pulse animation · monitoreo = dot estático · pasivo = dim
- Dominios técnico-only: visible pero dimmed para rol Directivo
- Botón "→" por dominio accesible → navegación a módulo correcto

**Router actualizado**
- `env_gov.py` → "inicio" ahora renderiza `p_command_center`
- Label sidebar: "Inicio" → "Centro de Mando"
- `_MODULE_RENDER` label actualizado

### Paleta D.3a
```
Fondo base:      #050A12 (C.BG)
Crítico:         #EF4444 (C.RUPTURA)
Alerta:          #F97316 (C.ALERTA)
Normal/Accent:   #00D4FF (C.ACCENT)
Verde:           #22C55E (C.SOSTENIB)
Fondos/Fondos:   #7C5CFC (C.PURPLE)
Números:         JetBrains Mono, 900 weight
```

### Estados fijos D.3a (hardcoded → live en D.3b+)
| Dominio                   | Temperatura | Gravedad | Actividad |
|---------------------------|-------------|----------|-----------|
| Salud Institucional       | critico     | 3        | activo    |
| Fidelidad Política        | normal      | 1        | pasivo    |
| Planificación y Ejecución | alerta      | 2        | monitoreo |
| Holding Municipal         | alerta      | 2        | activo    |
| Eficiencia Operacional    | normal      | 1        | monitoreo |
| Equidad Territorial       | alerta      | 2        | activo    |
| Transparencia             | normal      | 1        | pasivo    |
| Participación Ciudadana   | normal      | 1        | pasivo    |
| Género y Equidad Social   | critico     | 2        | activo    |
| Ambiente y Sostenibilidad | critico     | 2        | activo    |
| Cooperación Internacional | funds       | 3        | activo    |
| Agenda 2030               | normal      | 1        | monitoreo |
| Observabilidad Longitudinal | verde     | 1        | pasivo    |

---

## D.3b — Primer Dominio Completo (PENDIENTE)

**Dominio elegido:** Cooperación Internacional  
**Por qué:** Mayor densidad · más conflicto · más vida · más causalidad · más valor político  
**Datos disponibles:** $3.66M bloqueados · 3 fuentes activas · ISP 14.58% · PSG 12.83% · llaves maestras documentadas  
**Módulo destino:** `p18_cooperacion.py` (refactorizar para D.3b)  

### Lo que D.3b debe agregar al dominio Cooperación:
- Estado live desde `p18_cooperacion._FONDOS`
- Visualización de las llaves maestras (ISP 14.58%→65% desbloquea BDE; PSG 12.83%→30% desbloquea Gender Bond)
- Causaliudad: ISP ↓ → BDE riesgo ↑ → inversión rural ↓ → metas PDOT ↓
- Cards de fondos con barra de progreso hacia umbral
- Sensación: "esto es dinero real que depende de decisiones concretas"

---

## D.3c — Sistema de Exploración (PENDIENTE)

Cuando el alcalde hace click en un dominio:
- No debe abrir "otra página"
- Debe sentirse como: entrar a otra capa institucional
- Transición visual suave hacia el módulo
- Breadcrumb de retorno: "← Centro de Mando"
- Contexto territorial preservado

---

## Notas de Implementación

**Dato en conflicto (geojson vs doctrina):**
El `parroquias_montecristi.geojson` clasifica varias parroquias como "Rural" (Eloy Alfaro, Leónidas Plaza, La Pila, Colorado, Aníbal San Andrés, Isabel Muentes). Pero la doctrina canónica dice "La única rural es La Pila". Este conflicto está documentado como deuda técnica. Corrección pendiente al actualizar el Gold Master y regenerar el geojson.

**Hold_avg hardcodeado:**
`hold_avg = 68.7` es el promedio HPT-M de D.3a. En D.3b+ se calculará desde el snapshot en vivo.

**Navegación desde mapa:**
Click en parroquia → GeoTwin (técnico) o Situación Institucional (directivo). D.3b+ permitirá selección de parroquia como filtro persistente.

---

*D.3a cerrado. Sistema operacional en producción.*  
*Siguiente: D.3b — Primer dominio completo (Cooperación Internacional)*
