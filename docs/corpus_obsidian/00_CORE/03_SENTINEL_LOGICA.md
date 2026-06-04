---
name: "Sentinel — Lógica de Decisión"
description: "Capa de decisión del ecosistema QUIRA: convierte los outputs del SIAP Engine y el conocimiento de la KB en recomendaciones accionables. Sentinel no calcula el score — interpreta el score y lo transforma en acción institucional."
tipo: sentinel-logica
capa: "CAPA 5 — Action Layer"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
fecha: "2026-05-17"
tags: [sentinel, decision, accion, recomendacion, capa5, sat, matching, prioridad]
---

# Sentinel — Lógica de Decisión

> Sentinel no es un dashboard. Es la capa que convierte datos en acción. Cuando el Motor dice "D3=59.85%", Sentinel dice "activa PAC en Q2, prioriza alcantarillado Eloy Alfaro, reasigna USD 144K por punto recuperado." Esa es la diferencia entre inteligencia y conocimiento.

→ [[QUIRA_OS_Ontologia]] · [[00_QUIRA_GOV]] · [[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]]

---

## Posición en el Ecosistema

```
CAPA 3 — SIAP Engine        produce: TGI=66.85, D3=59.85%, IRS=79.7
    ↓
CAPA 4 — Obsidian KB        interpreta: ¿por qué? ¿qué normativa? ¿qué territorio?
    ↓
CAPA 5 — Sentinel  ◄─────  (este nodo) decide: ¿qué hacer? ¿cuándo? ¿con quién?
    ↓
Acción institucional:        POA ajustado · PAC activado · RdC informada
```

**Regla de oro de Sentinel:**
- Si el fondo existe pero no encaja con el actor, el territorio y la capacidad: no se recomienda aunque el tema sea atractivo.
- Si el score es alto pero la ejecución está bloqueada: la prioridad es desbloquear, no buscar fondos nuevos.

---

## El Vocabulario de Sentinel

Sentinel tiene un vocabulario preciso. Cada recomendación debe usar uno de estos estados:

| Estado | Significado | Condición de disparo |
|--------|-------------|---------------------|
| **APLICA** | El actor puede actuar ahora | Elegibilidad + capacidad + recursos confirmados |
| **NO APLICA** | No hay condiciones para actuar | Requisito crítico ausente o incompatible |
| **APLICA CON ALIANZA** | Requiere socio para cumplir condiciones | Brecha de capacidad o contrapartida |
| **REQUIERE PREPARACIÓN** | El camino existe, falta masa crítica | Score bajo pero recuperable con acciones específicas |
| **PRIORIDAD ALTA** | Umbral de urgencia superado | SAT-III o superior + brecha territorial crítica |
| **PRIORIDAD MEDIA** | Monitorear activamente | Tendencia negativa, aún dentro de zona tolerable |
| **PRIORIDAD BAJA** | Gestión de rutina | Sin alertas activas, dentro de parámetros normales |

---

## Los Cuatro Criterios de Decisión

Sentinel pondera cuatro dimensiones antes de emitir cualquier recomendación:

### 1. Elegibilidad del Actor

```
¿El GAD cumple los requisitos formales para actuar?
    ↓
Verifica:
  ├── D1 — Legalidad: ¿tiene respaldo normativo?
  ├── D5 — Capacidad: ¿puede operar el mecanismo?
  └── D2 — Planificación: ¿está en el PDyOT/POA?

Umbral mínimo: D1 ≥ 70% · D5 ≥ 80%
Estado actual Montecristi: D1=83.5% ✓ · D5=100% ✓
```

### 2. Brecha Territorial

```
¿La acción llega al territorio que más lo necesita?
    ↓
Verifica:
  ├── IRS — ¿inversión va hacia zonas pobres o ricas?
  ├── IET — ¿qué parroquia tiene mayor déficit?
  └── CN — ¿cuál es el Composite Need líder?

Umbral crítico: IRS > 70 → regresividad activa → priorizar rural
Estado actual Montecristi: IRS=79.7 → ALERTA ACTIVA
```

### 3. Capacidad de Ejecución

```
¿El GAD puede convertir la decisión en obra real?
    ↓
Verifica:
  ├── D3 — ¿ritmo de ejecución suficiente?
  ├── PAC — ¿procesos publicados y activos?
  └── eSIGEF — ¿presupuesto disponible en grupos 7+8?

Umbral crítico: D3 < 60% → riesgo de absorción
Estado actual Montecristi: D3=59.85% → LÍMITE INFERIOR
```

### 4. Alineación Estratégica

```
¿La acción responde a un compromiso formal?
    ↓
Verifica:
  ├── CNE — ¿está en el plan de gobierno?
  ├── PDyOT — ¿tiene meta estratégica?
  ├── POA — ¿fue programada para este año?
  └── ICPI — ¿impacta las metas del Motor?

Umbral mínimo: presencia en al menos 2 de los 4 instrumentos
```

---

## El Sistema de Alertas — SAT (Sistema de Alerta Temprana)

Sentinel no espera a que el problema sea irreversible. El SAT emite alertas por grados:

| Nivel | Nombre | Condición | Recomendación |
|-------|--------|-----------|---------------|
| SAT-0 | Verde | TGI ≥ 75% · sin alertas | Gestión de rutina |
| SAT-I | Amarillo | TGI 65-75% ó 1 D en rojo | Monitoreo activo mensual |
| SAT-II | Naranja | TGI 55-65% ó 2 D en rojo | Plan de mejora en 60 días |
| SAT-III | Rojo | TGI < 55% ó D3 < 50% | Intervención urgente |
| SAT-IV | Crítico | Ejecución < 30% a Q3 | Alerta a autoridad superior |
| SAT-V | Sistémico | IRS > 85% + D3 < 45% | Auditoría y reestructuración |

**Estado actual Montecristi (mayo 2026):**
```
TGI = 66.85 → SAT-I (Amarillo)
D3  = 59.85% → SAT-II (Naranja) — dimensión crítica
IRS = 79.7  → Alerta Equidad activa
```

→ [[ALERTA-D3_Ejecucion_Critica]] · [[ALERTA-Regresividad_IRS79]]

---

## Sentinel en Acción — Casos Montecristi

### Caso 1 — D3=59.85% CRÍTICO

```
Input Sentinel:
  D3 = 59.85% | PAC 2026 parcialmente publicado | eSIGEF grupos 7+8

Proceso:
  ├── Elegibilidad: D5=100% → puede actuar ✓
  ├── Brecha: IRS=79.7 → orientar hacia rural
  ├── Capacidad: D3 en SAT-II → riesgo de absorción
  └── Alineación: alcantarillado en Plan CNE + PDyOT + POA ✓

Output Sentinel:
  ESTADO: PRIORIDAD ALTA
  ACCIÓN: Activar PAC Q2 2026 · Publicar procesos alcantarillado
  IMPACTO: Cada punto D3 = USD 144,000 en inversión ejecutada
  PLAZO: Máximo 45 días para publicación de procesos
```

### Caso 2 — IRS=79.7 REGRESIVIDAD

```
Input Sentinel:
  IRS = 79.7 | Isabel Muentes NBI=61.2% | Brecha USD 1.79M

Proceso:
  ├── Elegibilidad: Plan CNE comprometió inversión rural ✓
  ├── Brecha: Isabel Muentes = Composite Need líder
  ├── Capacidad: D5=100% → puede redirigir inversión
  └── Alineación: PDyOT + Ppto Participativo 2024/2025 ✓

Output Sentinel:
  ESTADO: PRIORIDAD ALTA
  ACCIÓN: Reasignar PAC hacia parroquias con IET bajo
  IMPACTO: USD 1.79M de brecha que debe cerrarse gradualmente
  ALIANZA: Posible BDE/CAF para agua potable rural
```

### Caso 3 — D2 ICPI=69.93% FRICCIÓN

```
Input Sentinel:
  ICPI = 69.93% | ICM = 100% | Fricción = 30.07 pp

Proceso:
  ├── Elegibilidad: D1=83.5% → marco legal sólido ✓
  ├── Brecha: 8 de 25 metas PDyOT sin presupuesto operativo
  ├── Capacidad: D5=100% → puede reformular POA
  └── Alineación: metas incumplidas identificadas en ICPI ✓

Output Sentinel:
  ESTADO: REQUIERE PREPARACIÓN
  ACCIÓN: Reformular POA 2026 incorporando las 8 metas ausentes
  PLAZO: Reforma presupuestaria Q2 ante el Concejo
  RIESGO: Si ICM sigue en 100% pero ICPI no mejora → fricción crece
```

---

## Sentinel como Auditor Cognitivo

En su versión avanzada (hoja de ruta QUIRA), Sentinel es capaz de:

```
Leer automáticamente:
  ├── PDOT (25 metas)
  ├── POA (programación anual)
  ├── PAC (procesos publicados en SERCOP)
  └── eSIGEF (devengado real)

Detectar automáticamente:
  ├── Inconsistencias POA↔PAC (procesos no alineados)
  ├── Partidas codificadas sin proceso de contratación
  ├── Metas PDyOT sin asignación presupuestaria
  └── Parroquias con inversión regresiva

Emitir automáticamente:
  ├── Recomendaciones priorizadas por urgencia
  ├── Alertas SAT con plazo de intervención
  ├── Proyección de TGI si se ejecutan las recomendaciones
  └── Informe ejecutivo para Alcaldía
```

→ [[MOTOR_04_Ecosistema_Digital]] — QUIRA Audit como evolución de Sentinel

---

## Matching de Fondos — Sentinel como Motor de Elegibilidad

Sentinel también opera como motor de matching entre brechas territoriales y fuentes de financiamiento:

```
ENTRADA:
  ├── Brecha activa (IRS=79.7, Isabel Muentes NBI=61.2%)
  ├── Capacidad GAD (D5=100%, D3=59.85%)
  ├── Requisitos fondo (contrapartida, documentos, score mínimo)
  └── Alineación estratégica (PDyOT, Plan CNE, ODS)

PROCESO:
  ├── Score general TGI=66.85 → elegible para fondos con umbral ≥60
  ├── Capacidad absorción D3=59.85% → riesgo de subutilización
  ├── D5=100% → garantía institucional para desembolsos
  └── IRS=79.7 → fondo de equidad territorial: APLICA CON PREPARACIÓN

SALIDA:
  ├── Fondo BDE Agua Rural: APLICA — D5 ✓, brecha ✓, PDyOT ✓
  ├── Fondo CAF Infraestructura: APLICA CON ALIANZA — requiere estudio previo
  ├── Fondo BEI/PROGAPSA: REQUIERE PREPARACIÓN — D3 debe subir a ≥65%
  └── PNUD Equidad: APLICA — IRS=79.7 como evidencia de brecha
```

→ [[06_Fuentes_Financiamiento]] — fondos activos mapeados

---

## Reglas Inmutables de Sentinel

```
1. Sentinel no inventa datos.
   Todo output tiene fuente verificable en SIAP Engine o KB.

2. Sentinel no reemplaza la decisión humana.
   Recomienda — la Alcaldía, el Concejo y los directores deciden.

3. Sentinel no calcula el score.
   El score viene del SIAP Engine. Sentinel lo interpreta.

4. Sentinel prioriza territorio antes que cumplimiento.
   Un municipio que ejecuta bien pero regresivamente
   recibe alertas de Sentinel aunque su D3 sea alto.

5. Sentinel respeta la cadena jurídica.
   Ninguna recomendación viola COOTAD, COPFP o LOSNCP.
```

---

## Notas Sentinel Activas — Montecristi 2026

| Alerta | Score | Estado | Acción recomendada |
|--------|-------|--------|-------------------|
| [[ALERTA-D3_Ejecucion_Critica]] | D3=59.85% | SAT-II | Activar PAC Q2 · publicar procesos |
| [[ALERTA-Regresividad_IRS79]] | IRS=79.7 | Alta | Reasignar inversión rural |
| [[ALERTA-Isabel_Muentes]] | NBI=61.2% | Alta | Priorizar agua potable · BDE |
| [[ALERTA-Brecha_Rural_1.79M]] | USD 1.79M | Alta | Matching fondos cooperación |

---

*Sentinel · Lógica de Decisión · QUIRA OS · CAPA 5 · Dylus Lab © 2026*
