# QUIRA Intelligence — Arquitectura Canónica PMV
**Documento de contención arquitectónica — CANON OFICIAL**
*Decisión tomada: 2026-05-25 · Sprint 3 · Pivot estratégico validado por equipo QUIRA*

> Este documento existe para evitar desbordamiento doctrinal.
> Toda nueva feature, módulo, pantalla o índice debe responder a una pregunta antes de existir:
> **¿En qué ambiente vive? ¿Alimenta el ciclo mensual longitudinal?**
> Si la respuesta no es clara: es futuro, no PMV.

---

## 1. Propósito

QUIRA Intelligence es una **infraestructura de monitoreo institucional preventivo y prospectivo** para gobiernos locales del Ecuador.

En su fase PMV, es operada centralmente por el equipo QUIRA. Su función es detectar:
- deterioro institucional,
- brechas de ejecución,
- opacidad y desviaciones del mandato,
- riesgos de gobernanza,

**antes de que se conviertan en crisis administrativas o políticas.**

El municipio es actor observado y colaborador documental — no operador del sistema.

---

## 2. Actores del PMV

| Rol | Descripción | Ambientes accesibles |
|---|---|---|
| **Viewer** | Consulta análisis y reportes | GOV, Impact |
| **Analyst** | Análisis avanzado, comparativos longitudinales | GOV, Impact |
| **Operator** | Ejecuta pipeline, gestiona snapshots | GOV, Ops |
| **Admin** | Configuración total, governance, Gold Master | Todos |

> **DEPRECATED desde 2026-05-25:** Los roles Alcalde / Concejal / Técnico corresponden
> al modelo SaaS municipal que fue descartado para el PMV.
> No usar, no recuperar, no reintroducir.

---

## 3. Los 4 Ambientes

```
┌─────────────────────────────────────────────────────┐
│                QUIRA Intelligence                   │
│  Un pipeline · Un snapshot · Un RC-M · Un SAT       │
└───────┬──────────┬───────────────┬──────────────────┘
        │          │               │                │
   🏛 GOV  🌎 Civic       📑 Impact        ⚙ Ops
   (núcleo)    (ciudadanía)   (cooperación)    (interno)
   PMV AHORA   PMV FUTURO     PMV FUTURO       PMV AHORA
```

### 🏛 GOV — El producto hoy
El corazón. Todo lo que el municipio necesita saber sobre su trayectoria institucional.

Tabs del PMV:
| Tab | Contenido |
|---|---|
| Estado Municipal | ICPI global, TGI 5D, AVEP nivel, riesgo SAT |
| RC-M Longitudinal | Tabla de evolución mensual, gráfico de tendencia |
| Alertas SAT | SAT activas, clasificación, base legal, protocolo |
| Comparación de Períodos | Diff Engine: MEJORA/DETERIORO/RUPTURA/RECUPERACIÓN |
| Ejecución Presupuestaria | D3 Ti, devengado, holding consolidado |
| Trazabilidad | Fuentes, reliability scores, cadena evidencial |

### 🌎 Civic — Futuro (placeholder en PMV)
Vista pública participativa. Ciudadanía comprende, compara y aporta evidencia documental faltante (PAC, POA, rendiciones). Evidencia ciudadana entra como `evidence_source = citizen_uploaded` con reliability_score propio. **No construir hasta que GOV esté estable en producción.**

### 📑 Impact — Futuro (placeholder en PMV)
Outputs estratégicos. Reportes ejecutivos, exportaciones para cooperación (BID, PNUD, CAF), policy briefs, dashboards para multilaterales. **No construir hasta que haya al menos 6 meses de datos longitudinales.**

### ⚙ Ops — Infraestructura interna
Solo equipo QUIRA. Nunca visible para el municipio.

Tabs del PMV:
| Tab | Contenido |
|---|---|
| Pipeline | Ejecutar snapshot, ver logs, estado conectores |
| Snapshots | Registry, historial, validación |
| Reliability | Scores por fuente, trazabilidad longitudinal |
| Gold Master | Estado v6.0, sheets implementadas, changelog |
| Configuración | config.py, parámetros, conexiones |

---

## 4. Flujo Mensual Longitudinal — El Producto Real

El dashboard es la interfaz. El ciclo mensual es el producto.

```
Cada mes:

  1. QUIRA ejecuta pipeline automático
         │
         ▼
  2. Pipeline lee fuentes públicas
     (SERCOP · DPE · CPCCS · transparencia · PAC)
         │
         ▼
  3. Se genera snapshot canónico (JSON → Supabase)
         │
         ▼
  4. RC-M actualiza trayectoria longitudinal
         │
         ▼
  5. SAT evalúa riesgo y reincidencia
         │
         ▼
  6. Diff Engine clasifica el período
     (MEJORA / DETERIORO / ESTABLE / RUPTURA / RECUPERACIÓN)
         │
         ▼
  7. [Futuro - Civic] Ciudadanía aporta evidencia faltante
         │
         ▼
  8. [Futuro - Impact] Reportes institucionales generados
         │
         ▼
  9. Memoria longitudinal persistida en Supabase
     (indestructible, auditable, prospectable)
```

**Esta secuencia es el núcleo diferencial de QUIRA.** Todo lo demás sirve a este ciclo o es futuro.

---

## 5. Responsabilidades en el PMV

| Actor | Hace | No hace |
|---|---|---|
| **Equipo QUIRA** | Opera pipeline, valida datos, produce análisis, entrega alertas, genera informes | No depende del municipio para obtener datos de fuentes públicas |
| **Municipio** | Recibe análisis, valida observaciones, aporta documentos opcionales | No opera el sistema, no llena formularios complejos, no gestiona alertas |

---

## 6. Lo que el PMV NO hace — Contención Activa

Esta lista es contención activa. Si algo de aquí aparece en un sprint, preguntar: *¿por qué ahora?*

| Fuera del PMV | Razón |
|---|---|
| Workflow municipal interno (Directors upload) | Requiere onboarding complejo — modelo SaaS |
| ERP de gobernanza / formularios por dirección | No es el producto — es desbordamiento |
| ODS mapping y Agenda 2030 | Pertenece a Impact — futuro |
| GeoTwin territorial | Requiere datos GIS que no existen aún |
| Simulador de escenarios | Pertenece a Impact — futuro |
| Perspectiva de género / etaria | Datos no disponibles en fuentes conectadas |
| Cooperación internacional (módulo) | Pertenece a Impact — futuro |
| Sistema multi-usuario complejo | PMV es operado por el equipo — roles simples |
| Multi-municipio completo | Montecristi primero — luego replicabilidad |
| QUIRA Audit / QUIRA Funds / QUIRA Climate | Módulos futuros del ecosistema QUIRA |

---

## 7. Reglas de Contención Arquitectónica

1. **Toda feature nueva vive en uno de los 4 ambientes** o no existe en PMV.
2. **GOV recibe vistas nuevas como tabs** — nunca como ambiente nuevo.
3. **Civic y Impact son placeholders** hasta estar en roadmap con fecha.
4. **El backend es el núcleo** — el frontend es su interfaz, no al revés.
5. **Ante duda:** si no alimenta el ciclo mensual longitudinal, es futuro.
6. **El Excel v6.0 es motor metodológico** — no sistema total. Governance/longitudinal/evidencia van a Python/Supabase.
7. **Los roles QUIRA son Viewer/Analyst/Operator/Admin** — nunca Alcalde/Concejal/Técnico en PMV.

---

*QUIRA Intelligence — Dylus Lab © 2026*
*Decisión del equipo: 2026-05-25 · Sprint 3 Pivot*
