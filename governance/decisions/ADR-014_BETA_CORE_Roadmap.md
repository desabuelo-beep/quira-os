# ADR-014 — BETA-CORE: Estrategia de Completación del Gemelo Institucional de Montecristi

**Estado:** Aceptado  
**Fecha:** 2026-06-01  
**Autores:** Dylus Lab — Director + Advisor (validado por colega arquitectónico externo)  
**Vigencia:** Activo hasta MILESTONE_002 — cambiar requiere nuevo ADR  
**Clasif.:** Interno · QUIRA Operaciones

---

## Contexto

Sprint 3 QUIRA Gov completó la infraestructura canónica de Layer 2:

- Patrón QTMP → Conector → Layer 2 validado operacionalmente (Dom10, Dom12)
- 7 circuitos con QTMP status al cierre del sprint (Dom02, Dom04, Dom06, Dom07, Dom08, Dom10, Dom12)
- QLEP corpus F0.1-F0.6: 136 artefactos (93 ACK + 14 REL-V + 29 REL-H)
- ADR-013 congela el mapeo QTMP → 12 Dominios canónicos

Un colega arquitectónico externo revisó el estado del proyecto y emitió la siguiente recomendación el 2026-06-01:

> "Montecristi completo primero. La arquitectura ya está validada — Alpha 1.0 demostró la cadena Norma → Cadena causal → Resultado → Explicación verificable. El riesgo ahora no es arquitectónico: es fragmentación. UI perfecta con 3 dominios reales y 9 dominios vacíos es un demo, no QUIRA. Sprints 4-12: un dominio por sprint, ADR-012 sin excepciones, secuencia Dom07→Dom01→Dom02→Dom03→Dom05→Dom04→Dom08→Dom09→Dom11."

El Director instruyó: **"revise valide, mejore, supere, ejecute, documente."**

Este ADR cumple esa instrucción.

---

## Evaluación de la Recomendación

### Tesis central: CORRECTA

1. La arquitectura está validada — no se re-valida, se escala.
2. El riesgo de fragmentación (QUIRA con dominios vacíos = demo) es el riesgo más alto activo.
3. ADR-012 como protocolo sin excepciones es la única garantía de completitud real.
4. La frase del colega es certera: "El primer gemelo institucional causal completo de un municipio latinoamericano es mucho más difícil de replicar que una interfaz."

### Correcciones al diagnóstico del colega

**Corrección 1 — Estado real vs. "3 circuitos"**

El colega describe el estado de partida como "3 circuitos" validados (Dom06, Dom10, Dom12).

Estado real al 2026-06-01:

| Dom | Circuito QTMP | Layer 2 | ADR-012 nivel | Brecha principal |
|-----|---------------|---------|---------------|-----------------|
| D01 | ❌ pendiente | ❌ | N1/N2 | QTMP + datos PDOT (F0.7) |
| D02 | ✅ CONTROL_PREV | ❌ | N1–N3 | Layer 2 + C9 dato real |
| D03 | ❌ pendiente | ❌ | N1/N2 | QTMP + CPFP Art. 44 (F0.7) |
| D04 | ✅ CONTROL_LEGAL | ❌ | N1–N3 | Layer 2 + C9 dato real |
| D05 | ❌ pendiente | ❌ | N1 parcial | QTMP + LOEP corpus (F0.8) |
| D06 | ✅ EQUIDAD | 🟡 m1_situacion | N1–N4 | Layer 2 upgrade + N5 C10 |
| D07 | 🟡 YAML materializado | ❌ | N1–N3 | Neo4j load + Layer 2 + dato real |
| D08 | ✅ PARTICIPACION | ❌ | N1–N3 | Layer 2 + C9 dato real |
| D09 | ❌ pendiente | ❌ | N1/N2 | QTMP + dependencias Dom01/Dom03 |
| D10 | ✅ AGUA_POTABLE | ✅ p10_territorio.py | **N1–N5 ✅** | **COMPLETO** |
| D11 | ❌ no existe | ❌ DISABLED | — | Fuera de MILESTONE_002 |
| D12 | ✅ GAP_10PCT | ✅ p19_genero.py | **N1–N5 ✅** | **COMPLETO** |

*Leyenda ADR-012: N1=Norma · N2=Pregunta bautismal · N3=Grafo Neo4j · N4=Resultado territorial · N5=C10 record*

**Conclusión**: 2 dominios completados, 5 con circuito parcial (no 0). La brecha real es 10/12, no 9/12 como implica el colega. El punto de partida es más sólido.

---

**Corrección 2 — Sprint 3 = COMPLETADO**

El colega describe Sprint 3 como "establecer la infraestructura mínima para consumir causalidad."  
Sprint 3 está **COMPLETO** al cierre de esta sesión, menos el push a GitHub (Task #14).

Entregables Sprint 3:
- `quira_pages/p10_territorio.py` — Layer 2 Dom10 con QTMP AGUA_POTABLE ✅
- `quira_pages/p19_genero.py` (enriquecido Sprint 3) — Layer 2 Dom12 con QTMP GAP_10PCT ✅
- `data/qtmp/qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` — Dom07 cadena C3-C9 completa ✅
- `app/connectors/neo4j_qtmp.py` — TRANSPARENCIA circuit + AGUA_POTABLE modulo corregido ✅
- ADR-013 activo y congelado ✅
- Bloomberg Model firewall operativo (`_strip_internal()`) ✅

---

**Corrección 3 — Secuencia de sprints (corpus-optimized)**

La secuencia del colega: `Dom07→Dom01→Dom02→Dom03→Dom05→Dom04→Dom08→Dom09→Dom11`

Problema con Dom01 en segundo lugar: Dom01 requiere PDOT Montecristi como cadena causal (corpus F0.7 — aún no atomizado). Colocarlo en S5 bloquea el sprint por dependencia de datos, mientras Dom06 y Dom08 tienen circuitos ya cerrados en QLEP_CANONICO y solo requieren Layer 2.

La secuencia óptima prioriza circuitos ya cerrados (menor trabajo por dominio) antes de los que requieren corpus adicional:

---

## Decisión: BETA-CORE Activo

QUIRA Gov entra en fase **BETA-CORE** a partir de Sprint 4.

**Objetivo único hasta MILESTONE_002**: completar los 12 dominios de Montecristi según ADR-012.

**Reglas de operación BETA-CORE**:
1. Un dominio por sprint — sin excepciones.
2. ADR-012 N1→N5 es bloqueante: no se cierra un sprint sin C10 record del dominio.
3. Ningún sprint se dedica a UX nueva, funcionalidades adicionales, o expansión de entidad.
4. Los dominios se ejecutan en la secuencia fijada en este ADR — cambiar la secuencia requiere nuevo ADR.

---

## Secuencia de Sprints BETA-CORE

### Tier A — Circuito QTMP cerrado en QLEP_CANONICO; Layer 2 = único gap

*Estos sprints son los más rápidos: el grafo ya tiene la cadena, el conector ya tiene fallback, solo falta la página Layer 2 y el C10 record.*

| Sprint | Dom | Nombre | Estado QTMP | Trabajo principal |
|--------|-----|--------|-------------|-------------------|
| **S4** | D07 | Transparencia | 🟡 YAML ✅ · Neo4j pendiente | Cargar QTMP a Neo4j + Layer 2 LOTAIP (21 numerales) · calibrar C5a/C5b/C5c |

**Sprint 4 — Agenda de calibración (COR-QNKC-01 aplicado)**

La forma causal de Dom07 está derivada de P01 y no requiere diseño. Sprint 4 descubre únicamente los parámetros empíricos:

| Observable | Dimensión | Preguntas de calibración |
|-----------|-----------|--------------------------|
| **C5a — Accesibilidad** | ¿El enlace LOTAIP responde? | ¿HTTP 200? ¿Tiempo de respuesta? ¿Uptime histórico disponible en el período? |
| **C5b — Vigencia** | ¿El contenido es del período vigente? | ¿Fecha de publicación ≤ fecha de evaluación? ¿Período reportado = año en curso? ¿Consistencia mes evaluado? |
| **C5c — Inteligibilidad** | ¿Es comprensible para ciudadano? | ¿Estructura tabular LOTAIP? ¿OCR correcto (no imagen escaneada)? ¿Lenguaje claro? ¿WCAG básico? ← OBS-QNKC-01 activo |
| **Umbrales C8** | Semáforo resultante | ¿Verde ≥ X? ¿Amarillo ≥ Y? ¿Rojo < Y? Calibrar contra referencia real de los 21 artículos de Montecristi |

C5c es la dimensión más difícil — puede requerir checklist experta o score de legibilidad. OBS-QNKC-01 (Verificabilidad ≠ Comprensión) aplica directamente aquí.

La multiplicación `C8 = C4 × C5a × C5b × C5c` es la forma fijada. El sprint define los valores — no la estructura.

**Addendum calibración Sprint 4 — 2026-06-01 (OBS-QNKC-02):**

Hallazgo durante calibración: bajo LOTAIP 2.0 (reforma vigente), la fuente canónica de C5a y C5b para Dom07 **no es el portal institucional del GADMCM** sino el **portal regulatorio de la DPE**: `https://transparencia.dpe.gob.ec/`.

Las preguntas de calibración C5a y C5b se responden consultando el portal DPE para Montecristi, no `montecristi.gob.ec/lotaip`. El portal GAD puede tener información adicional pero no es autoritativo para verificación de cumplimiento LOTAIP.

**Protocolo de auditoría N4 (Matriz de calibración por numeral):**

Para cada numeral del Art. 19 LOTAIP, registrar:

| Numeral | C5a — Existe en DPE | C5b — Actualizado (período vigente) | C5c — Comprensible (lenguaje claro) |
|---------|--------------------|------------------------------------|-------------------------------------|
| 1       | ✓/✗                | ✓/✗                                | ✓/✗                                 |
| 2       | ✓/✗                | ✓/✗                                | ✓/✗                                 |
| ...     | ...                | ...                                | ...                                 |
| 21+     | ✓/✗                | ✓/✗                                | ✓/✗                                 |

*Nota: verificar si LOTAIP 2.0 amplió el número de numerales obligatorios — observaciones de navegación sugieren hasta 24; pendiente contraste con texto legal.*

Resultado de la matriz → C5a = (Σ C5a_i) / total · C5b = (Σ C5b_i) / C5a_i · C5c = evaluación por muestreo representativo → C8 = C4 × C5a × C5b × C5c.

Registrado como OBS-QNKC-02 en QNKC_PRINCIPIOS_INDEX.
| **S5** | D06 | Salud Institucional | ✅ EQUIDAD cerrado | Layer 2 upgrade: m1_situacion → Layer 2 completo |
| **S6** | D08 | Participación Ciudadana | ✅ PARTICIPACION cerrado | Layer 2 nueva página Dom08 |

### Tier B — Circuito QTMP parcial; corpus disponible; Layer 2 vacío

*Corpus fuerte, circuito QTMP parcialmente materializado. Requiere QTMP YAML completo + Layer 2.*

| Sprint | Dom | Nombre | Estado QTMP | Trabajo principal |
|--------|-----|--------|-------------|-------------------|
| **S7** | D02 | Presupuesto & Financiamiento | ✅ CONTROL_PREV · cadena presupuestal pendiente | QTMP completo + Layer 2 presupuesto |
| **S8** | D04 | Alertas Institucionales | ✅ CONTROL_LEGAL · cross-domain por naturaleza | Layer 2 dashboard alertas (depende de S7 Dom02) |

### Tier C — Corpus requiere atomización adicional (F0.7)

*Estos dominios necesitan PDOT Montecristi + CPFP antes de cerrar la cadena causal. Se ejecutan después de Tier A+B para aprovechar el tiempo de atomización.*

| Sprint | Dom | Nombre | Dependencia corpus | Trabajo principal |
|--------|-----|--------|-------------------|-------------------|
| **S9** | D01 | Planificación Estratégica | PDOT Montecristi + CPFP F0.7 | QTMP PDOT + Layer 2 metas PDOT |
| **S10** | D03 | Seguimiento de Metas | Dom01 completo + CPFP Art. 44 | QTMP seguimiento + Layer 2 semáforo metas |

### Tier D — Dependencias terminales

*Dominios que dependen del ciclo completo (Dom01+Dom03+Dom07) o del corpus más difícil (LOEP).*

| Sprint | Dom | Nombre | Dependencia | Trabajo principal |
|--------|-----|--------|-------------|-------------------|
| **S11** | D09 | Rendición de Cuentas | Dom01+Dom03+Dom07 completos | QTMP rendición + Layer 2 informe verificable |
| **S12** | D05 | Holding Municipal | LOEP F0.8 + Ti por entidad | QTMP holding + Layer 2 por EP (EMAI, Bomberos, Patronato, Aseo) |
| **Post-M002** | D11 | Ecosistema Productivo | corpus F0.7-F0.8 vacío · módulo DISABLED | Habilitar solo después de MILESTONE_002 |

---

## MILESTONE_002 — Definición Precisa

**Nombre**: Montecristi Gemelo Institucional Completo

El hito se alcanza cuando se cumplen **simultáneamente** las siguientes 5 condiciones:

1. **Completitud de dominio**: Los 12 dominios (excluyendo Dom11) tienen C10 record completo (ADR-012 N5).
2. **Respondibilidad bautismal**: Las 12 preguntas bautismales definidas en QLEP_CANONICO son respondibles en ≤60s con fuente trazable desde C1 hasta C9.
3. **Señales cross-domain activas**: Al menos 3 REL-H (circuitos horizontales) tienen dato real verificado — no solo nodo en grafo.
4. **Centro de Mando sin cajones vacíos**: Ningún módulo muestra estado "En Modelado" al alcalde. Los 12 dominios muestran semáforo con dato y narrativa.
5. **Trazabilidad pública completa**: Para cada dominio, la explicación que ve el alcalde puede rastrearse hasta la norma C1 sin exponer la metodología interna.

**Lo que MILESTONE_002 NO es**:
- "Todos los módulos funcionan" (criterio técnico, no institucional)
- "12 indicadores en verde" (el verde no es el objetivo — la veracidad es)
- "UI perfecta" (la UI es el envoltorio, el grafo es el contenido)

---

## Principio de Replicabilidad

Registro canónico para decisiones futuras de escala:

**El QLEP corpus N1 es nacional.** Las 221 normas base de los 12 dominios aplican a los 221 GAD Municipales de Ecuador sin modificación. La diferencia entre Montecristi y cualquier otro cantón es exclusivamente:

- `CANTON_ID` — identificador del cantón
- Datos C9 — resultados territoriales verificados (SIGEF, INEC, LOTAIP portal, SENAGUA, etc.)

La arquitectura ADR-012, el QLEP corpus, y la lógica de Layer 2 no se tocan. Replicar = cargar datos C9 del nuevo cantón y crear QTMP con el `CANTON_ID` correcto.

El colega dice: "el primer gemelo es el más difícil de replicar." Esto es correcto en tiempo — la arquitectura se construye una sola vez. Pero la dificultad no es arquitectónica: es la verificación de los datos C9 por primera vez. Una vez Montecristi está completo, la réplica es semanas, no meses.

**La ventaja competitiva de QUIRA no son los datos. Es la arquitectura que hace los datos accionables.**

---

## Prohibiciones BETA-CORE

Quedan prohibidas las siguientes acciones hasta que se declare MILESTONE_002:

1. **NO** iniciar módulos CAF (Canasta de Alerta Fiscal)
2. **NO** iniciar QUIRA Ciudadana en ninguna forma
3. **NO** expandir a nuevas entidades o cantones (ni como piloto)
4. **NO** agregar dominios o funcionalidades nuevas al Centro de Mando
5. **NO** saltar un sprint sin completar ADR-012 N1→N5 del sprint anterior — ninguna excepción
6. **NO** iniciar Dom11 (Ecosistema Productivo) — corpus vacío, módulo deshabilitado

Estas prohibiciones aplican aunque exista financiamiento disponible, demanda de stakeholders, o presión externa. BETA-CORE es una decisión arquitectónica, no un plan de trabajo flexible.

---

## Relación con ADRs previos

| ADR | Relación |
|-----|----------|
| ADR-013 | Mapeo QTMP→Dominio — congelado e inmutable. ADR-014 define cuándo y en qué orden se completan los dominios faltantes. |
| QLEP_CANONICO v1.0 | N1 y N2 congelados — fuente de verdad de la norma base y la pregunta bautismal por dominio. ADR-014 define la secuencia de activación. |

---

## Enmienda a ADR-013

El ADR-013 (2026-05-31) contiene dos errores tipográficos corregidos en código pero no en documento:

1. **AGUA_POTABLE módulo**: ADR-013 dice `p4_geotwin.py` — el módulo correcto es `p10_territorio.py` (corregido en `neo4j_qtmp.py` en Sprint 3).
2. **TRANSPARENCIA ausente**: ADR-013 no incluía el circuito TRANSPARENCIA → Dom07 → "municipal" (añadido en Sprint 3 esta sesión).

La tabla corregida del mapeo CIRCUIT_DOMAIN_MAP (fuente canónica en `app/connectors/neo4j_qtmp.py`):

| Circuito QTMP | Dominio | Nombre dominio | Módulo Streamlit |
|---------------|---------|----------------|------------------|
| `GAP_10PCT` | Dom12 | Protección Social & Grupos Prioritarios | `p19_genero.py` |
| `AGUA_POTABLE` | Dom10 | Territorio & Cobertura | `p10_territorio.py` |
| `EQUIDAD` | Dom06 | Salud Institucional | `m1_situacion.py` |
| `TRANSPARENCIA` | Dom07 | Transparencia | `[Layer 2 pendiente]` · placeholder: `municipal` |

Este ADR no reemplaza ADR-013 — solo registra la corrección de datos de implementación.

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"El primer gemelo institucional causal completo de un municipio latinoamericano. Montecristi primero. La escala viene después."*
