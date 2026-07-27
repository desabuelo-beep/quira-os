---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-007 — Dos Circuitos de Trazabilidad Pública Municipal

**Estado**: ACTIVO — formulacion arquitectonica pendiente de validacion con Fases 2-4  
**Fecha**: 2026-06-03  
**Origen**: Analisis colega asesor sobre completitud del ciclo PP→RC  
**Candidato**: ADR-022 (abrir si patron persiste tras Fases 2-4)

> *"Sin las cedulas no sabes si se contrato pero no se ejecuto, si se ejecuto parcialmente,
> si se devengó pero no se pagó, si hubo arrastre. La RC te cuenta la historia.
> La cedula te muestra la evidencia financiera." — Colega asesor, 2026-06-03*

---

## Contexto

Al analizar OBS-005 (ciclo PP→RC→PP), el colega asesor identificó que
el ciclo tiene en realidad DOS estructuras paralelas con distintas preguntas:

---

## Circuito A — Democratico

```
PP (participacion)
    ↓ PRIORIZA
POA (planificacion)
    ↓ OPERACIONALIZA
PAC (contratacion)
    ↓ FORMALIZA
RC (rendicion)
    ↓ RETROALIMENTA
PP siguiente
```

**Pregunta central**: ¿La ciudadanía participó y el GAD rindió cuentas sobre
lo que prometió al comenzar el ciclo?

**Evidencia necesaria**:
- PP informes (demandas ciudadanas con barrio y proyecto) ← Fase 1 ✅
- POA (metas y actividades planificadas) ← Fase 2
- PAC (procesos de contratacion) ← Fase 3
- RC informes (cumplimiento reportado al CPCCS) ← Fase 1 ✅

**Estado**: Fase 1 completada (RC+PP). Fases 2-3 pendientes.

---

## Circuito B — Financiero-Operativo

```
POA (planificacion con metas y presupuesto)
    ↓ CONTRATA
PAC (procesos de contratacion formalizados)
    ↓ EJECUTA
Comprometido → Devengado → Pagado
(cedulas presupuestarias mensualizadas)
    ↓ EVALUA
RC (resultados financieros y de gestion)
```

**Pregunta central**: ¿Lo que se planificó y contrató fue realmente ejecutado
y pagado en los plazos esperados?

**Evidencia necesaria**:
- POA ← Fase 2
- PAC ← Fase 3
- Cédulas presupuestarias / ejecución mensualizada (XLSX) ← Fase 4 (NUEVO)
- RC informes ← Fase 1 ✅

**Estado**: Solo RC disponible. Fases 2-4 pendientes.

---

## La Caja Negra que los Circuitos Eliminan

Sin las cédulas presupuestarias, QUIRA enfrenta esta brecha:

```
PAC (lo que se contrató)
        ↓
    ??? CAJA NEGRA ???
        ↓
RC (lo que se reportó)
```

No se puede saber si:
- Se contrató pero no se ejecutó
- Se ejecutó parcialmente (% devengado < % comprometido)
- Se reformó el presupuesto durante el ejercicio
- Hay proyectos en arrastre al siguiente año
- El devengado ≠ pagado (deuda flotante)

**Las cédulas mensualizadas cierran esta caja negra.**

---

## Estructura de Datos Requerida por Circuito

| Instrumento | Circuito | Formato | Destino Supabase |
|---|---|---|---|
| PP informe | A | PDF | normativa_corpus (Capa D) |
| POA | A+B | DOCX/PDF | normativa_corpus (Capa C) |
| PAC | A+B | DOCX/PDF | normativa_corpus (Capa C) |
| Cédula presupuestaria | B | XLS/XLSX | holding_structured_data |
| Ejecucion mensualizada | B | XLSX | holding_structured_data |
| RC informe | A+B | DOCX/PDF | normativa_corpus (Capa D) |

---

## Relacion con la Doctrina "El Excel es el Estado"

El Gold Master (Excel Canonico) contiene las cifras finales de ejecucion (Ti).
Las cedulas presupuestarias son la **evidencia primaria** de donde el Gold Master
deriva esos numeros.

La jerarquia epistemica es:
```
Cedula presupuestaria (fuente L0-digital)
    ↓ sintetiza
Gold Master (calculo canonico)
    ↓ informa
PMV / QUIRA (visualizacion y analisis)
```

Las cedulas estan en `Presupuestos 2023-2026/` del Holding MCR:
- GAD Montecristi: cédulas anuales 2023, 2024, 2025
- Aseo EP: presupuesto mensualizado 2024, 2025
- Bomberos: presupuesto mensualizado 2023-2026
- Patronato: presupuesto mensualizado 2023-2026

---

## Revision de Fases Gate 6.5

Con esta arquitectura de dos circuitos, el orden correcto es:

```
Fase 1  ✅  RC + PP          → normativa_corpus Capa D
Fase 2  ⏳  POA + PAI        → normativa_corpus Capa C
Fase 3  ⏳  PAC              → normativa_corpus Capa C
Fase 4  ⏳  Cedulas (XLSX)   → holding_structured_data
Fase 5  ⏳  SIGAD            → normativa_corpus Capa D
```

Las cédulas suben en prioridad (Fase 4 antes que SIGAD) porque son el
puente entre PAC (lo contratado) y RC (lo reportado).

---

## Condicion para ADR-022

Abrir ADR-022 después de Gate 6.5 Fases 2-4, cuando se pueda verificar
si el patron PP→POA→PAC→Cedulas→RC→PP aparece como circuito cerrado
en los datos reales de Montecristi.

Si el patron persiste, ADR-022 formalizara:
1. Los dos circuitos como entidades arquitectónicas de QUIRA
2. El método de verificación multicapa (A + computacional + documental + financiero)
3. Los criterios para el gap A≠D medible

---

*OBS-007 · QUIRA Gov · Dylus Lab · 2026-06-03*  
*"El circuito democratico y el circuito financiero no son lo mismo.*  
*El primero responde: ¿participaron? El segundo: ¿ejecutaron?"*
