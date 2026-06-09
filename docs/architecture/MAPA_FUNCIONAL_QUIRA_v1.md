# MAPA FUNCIONAL QUIRA v1.0

**Fecha:** 2026-06-09
**Origen:** ADR-026 v1.2 — Topología Funcional · Fase 0 Arqueología Funcional completada
**Propósito:** Guía visual de circuitos y flujos antes de Sprint B. No reemplaza ADR-026 — lo traduce.
**Audiencia:** Equipo Dylus Lab (Javo + Claude + Colega) · arquitectos de Sprint B

---

## La transformación que hace QUIRA

```
EVIDENCIA BRUTA
      ↓
  [D01 · D05]  ←── Norma: define qué significa "cumplir"
      ↓
  [D02..D12]   ←── Observación: captura evidencia verificable contra la norma
      ↓
    [D06]       ←── Interpretación: sintetiza estado institucional
      ↓
    [D09]       ←── Validación: arbitraje externo (CPCCS)
      ↓
    [D02]       ←── Consecuencia: traduce estado en dinero disponible / bloqueado
      ↓
GOBERNANZA EXPLICABLE
```

QUIRA no es un dashboard. Es un **sistema de transformación de evidencia en gobernanza**.

---

## Circuito C01 — Cadena Constitucional (ADR-017)

```
D07  Transparencia    ──ORIGEN · peso 1.5──►  D08  Participación  ──INTER · peso 1.0──►  D04  Planificación
(IOC · C8 formula)                            (IGP · 6 mecanismos)                        (SAT · alertas)

REGLA DE COLAPSO: Dom07 falla → CHS_C01 = 0.0 (implementada en p07_transparencia.py)
Fundamento: sin transparencia no hay participación real; sin participación no hay planificación legítima
```

---

## Circuito C-RDC — Convergencia Anual de Rendición (ADR-026)

```
D07 (IOC · LOTAIP)    ─┐
D08 (IGP · PP)        ─┤
D02 (ISP · cooprac)   ─┤
D03 (IFE-A · metas)   ─┼──► D09  Rendición de Cuentas ──► CPCCS ──► V=0 / V≥70
D04 (SAT · alertas)   ─┤         (checklist 20 ítems)    (árbitro externo)
D10 (agua · IET)      ─┤
D12 (PSG · IGM)       ─┘

Escala: ANUAL · activación: Mayo → Agosto (ejecución) → Septiembre (calificación CPCCS)
D09 es CONVERGENTE — no causal. Todos deben pasar; ninguno recibe de D09.
```

---

## Flujos de agregación → D06 (Sintetizador)

```
D07 ──► IOC  (-3.1 actual) ─┐
D08 ──► IGP  (-4.1 actual) ─┤
D10 ──► IET  (-2.8 actual) ─┼──► D06 (ICPI síntesis · 6 vectores causales)
D02 ──► ISP  (-8.2 actual) ─┤         ↑
D02 ──► IED  (-6.8 actual) ─┤    Lee del Gold Master — NO calcula
D12 ──► PSG  (-2.4 actual) ─┘    Es consecuencia, no producto
```

D06 no tiene fuentes propias. Si todos sus vectores están en verde, D06 está en verde.
**ICM/ICPI gap** (brecha propuesta de valor): ICM self-report = 100% · ICPI verificado = 57–70%.

---

## Flujos de consecuencia → D02 (Motor de elegibilidad financiera)

```
D12  PSG = 12.83% ─┐  < 30%  → BID Gender Bond BLOQUEADO
D10  ISP = 14.58% ─┤  < 65%  → BDE Crédito BLOQUEADO
D07  ITAM = 56%   ─┤  < 65%  → CAF Ciudades EN GESTIÓN       ──► D02 ──► Elegibilidad financiera
(otros vectores)  ─┘                                                       (snapshot dinámico)

D02 = Generador con función de consecuencia financiera.
Su output traduce el estado institucional en acceso/bloqueo a financiamiento externo.
Actualización: skill /fondos-radar (~15 días) · entidades: GAD · ONG · OSC · Academia · Startup · Coaliciones
```

---

## Cadena IFE — Integridad del Mandato Electoral (D03)

```
PLAN DE GOBIERNO CNE  ──ingesta MNT_UUID──►  IFE_CNE tag (D08/S1)
(66 promesas · alcalde)                      PLAN-GOB-MCR · PLAN-BICENTENARIO-MCR

         ↓ IFE-A (activo · H73_OUTPUT_API)

PDOT D05  ──Tipo D corpus──►  25 metas PDOT formalizadas
                               48/66 promesas vinculadas = 72.73% IFE-A

         ↓ IFE-E (pendiente Q2-2026)

POA → PAC → eSIGEF  ──►  ¿Las metas PDOT se ejecutaron con presupuesto real?
                          trazabilidad verificable por eSIGEF

PREGUNTA DE D03: ¿Las promesas electorales se convirtieron en instituciones,
                 y esas instituciones se convirtieron en ejecución real?
```

---

## Corpus Fundacional → alimenta el sistema (Tipo D)

```
D01  Marco Legal  ──► ACK Registry (relaciones causales entre artículos)
(vectorizado C1)       → contexto normativo para todos los dominios

D05  PDOT         ──► meta_pdot_2027 ──► D10 (agua · vialidad · residuos)
(vectorizado C1)   ──► METAS_PDOT    ──► D03 (M-01..M-10)
                   ──► IFE_CNE       ──► D03 (capa CNE)
                   ──► GeoTwin       ──► p4_geotwin.py (territorialización Layer 3)
                   ──► mecanismos PP ──► D08 (participación parroquial)
                   ──► checklist RDC ──► D09 (preparación rendición)
```

Tipo D no tiene puerta operacional. Su "interfaz" es Supabase C1 (ingest) y los campos `meta_pdot_2027`, `METAS_PDOT`, `IFE_CNE` que los Generadores leen.

---

## Mapa completo de tipos y conexiones

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CAPA 0 — NORMA (Tipo D)                                                    │
│  D01 Marco Legal ·  D05 PDOT  (Supabase C1 vectorizado)                     │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ define estándar · alimenta como referencia
┌──────────────────────────────▼──────────────────────────────────────────────┐
│  CAPA 1 — OBSERVACIÓN (Tipo A · 7 generadores)                              │
│                                                                             │
│  D04 SAT/Alertas      D07 Transparencia   D08 Participación                 │
│  D10 Territorio       D12 Género/Ambiente D03 Metas·IFE     D02 Cooperación │
│                                                                             │
│  Circuitos activos: C01 (D07→D08→D04) · C-RDC (todos→D09)                  │
└──────────┬─────────────────────────────────────────────┬────────────────────┘
           │ vectores causales IOC·IGP·IET·ISP·IED·PSG   │ PSG·ISP·ITAM
┌──────────▼──────────────────┐               ┌──────────▼────────────────────┐
│  CAPA 2 — INTERPRETACIÓN    │               │  CAPA 4 — CONSECUENCIA        │
│  D06 Sintetizador (Tipo B)  │               │  D02 Motor elegibilidad        │
│  ICPI síntesis · 6 vectores │               │  financiamiento (Tipo A²)     │
└─────────────────────────────┘               └───────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│  CAPA 3 — VALIDACIÓN (Tipo C)                                               │
│  D09 Rendición de Cuentas · checklist 20 ítems · CPCCS árbitro · anual     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Deudas activas que bloquean Sprint B

| Deuda | Módulo | Riesgo | Acción |
|---|---|---|---|
| Bloomberg violations | p9_sat · p7_brecha · p10_inversion | Exposición pública métricas internas | Auditar y corregir |
| Código muerto activo | p15_transparencia.py | Puede activarse accidentalmente · Bloomberg | Deprecar → governance/historico/ |
| Sin ruta sidebar | p8_metas.py (D03) | IFE-A inaccesible desde UI | Agregar ruta en env_gov.py |
| Datos faltantes D12 | IGM-A · B · C · F | Puerta vacía en Sprint B | Definir fuentes (RRHH · DAF · CNE · PNUD) |
| Portfolio D02 desactualizado | p18_cooperacion.py | Datos sin base Excel · bonds sin fundamento | Rediseñar con skill /fondos-radar |
| C-RDC sin Neo4j | spec en ADR-026 | Circuito definido pero no implementado | Ejecutar Cypher spec ADR-026 |

---

## Regla de uso de este mapa

> Antes de diseñar cualquier puerta en Sprint B, localiza el dominio en este mapa.
> El tipo funcional del dominio determina el tipo de puerta:
> - Tipo A → monitor (¿qué evidencia existe hoy?)
> - Tipo B → diagnóstico (¿qué dice la síntesis?)
> - Tipo C → preparador (¿qué falta para que el protocolo pase?)
> - Tipo D → no hay puerta operacional · hay entrada de corpus

---

*MAPA_FUNCIONAL_QUIRA_v1.0 · Dylus Lab © 2026*
*Derivado de ADR-026 v1.2 · Fase 0 Arqueología Funcional completada 2026-06-09*
*Actualizar cuando se modifique ADR-026 o se añadan circuitos nuevos*
