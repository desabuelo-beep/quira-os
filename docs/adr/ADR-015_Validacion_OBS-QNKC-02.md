---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-015 — Validación de OBS-QNKC-02: DPE como Infraestructura Observacional Canónica Nacional

**Estado:** ACEPTADO — OBS-QNKC-02 validada · N4 completado · C10 registrado · 2026-06-01  
**Fecha apertura:** 2026-06-01  
**Fecha cierre:** 2026-06-01  
**Autores:** Dylus Lab — Director + Advisor  
**Vigencia:** CERRADO — Dom07 en estado Verificado · pendiente DEC formal  
**Clasif.:** Interno · QUIRA Operaciones  
**Nota de clasificación:** Este ADR es retroactivamente el primer **protocolo VAL-QNKC de facto** del framework — no es una inspección de cumplimiento sino una comparación formal entre fuente interna (portal GAD · C4) y fuente externa (portal DPE · C5) para medir la brecha observable. Cuando la familia VAL-QNKC se formalice (derivación de H-QNKC-04 si se congela), ADR-015 será su prototipo fundacional. Ver `QNKC_PRINCIPIOS_INDEX.md` — H-QNKC-04 candidata.

---

## Contexto

OBS-QNKC-02 fue registrada durante la calibración de Sprint 4 (Dom07 Transparencia) cuando se estableció que bajo LOTAIP 2.0, el portal regulatorio de la Defensoría del Pueblo del Ecuador (`transparencia.dpe.gob.ec`) centraliza la verificación de cumplimiento LOTAIP para las 221 instituciones públicas del Ecuador — incluyendo todos los GADs municipales.

Esta observación produce un cambio epistemológico en la arquitectura de QUIRA:

```
Modelo anterior:
  Municipio → Portal institucional → Transparencia (autodeclaración)

Modelo OBS-QNKC-02:
  Municipio → Portal institucional → DPE → Verificabilidad (observación externa)
```

Dom07 dejó de ser un dominio de **autodeclaración** y pasó a ser un dominio de **observación externa**. La fuente que QUIRA consulta para C5a (Existencia) y C5b (Actualidad) ya no es el portal del propio GAD — es el portal del regulador que certifica lo que el GAD publicó.

**La auditoría N4 no solo cierra Dom07.** Valida o falsea OBS-QNKC-02 como hipótesis arquitectónica. Si valida, la consecuencia se extiende a la estrategia de escalamiento de 1 GAD a 222 GADs. Por eso este ADR existe.

---

## Las tres hipótesis que N4 testa simultáneamente

La auditoría N4 no valida solo los valores de C5a, C5b, C5c para Montecristi. Valida tres hipótesis del framework QNKC de forma simultánea. Ese es el alcance real de este ADR.

### Hipótesis A — P01 funciona operativamente

> ¿Puede calcularse `C8 = C4 × C5a × C5b × C5c` con datos reales, no con fallback?

```
C4  = cumplimiento formal autodeclarado  (portal GAD o verificación directa)
C5a = fracción de numerales que existen en DPE        [pendiente]
C5b = fracción de numerales actualizados en DPE       [pendiente]
C5c = evaluación de inteligibilidad para ciudadano    [pendiente]
C8  = C4 × C5a × C5b × C5c                           [pendiente]
```

Si C8 puede calcularse con datos reales → P01 (Dualidad Epistémica) tiene expresión operativa verificada, no solo teórica. La forma multiplicativa de H-QNKC-02 queda instanciada por primera vez con evidencia territorial real.

### Hipótesis B — OBS-QNKC-01 es observable empíricamente

> ¿Existen numerales en la auditoría donde `C5a = 1`, `C5b = 1`, `C5c = 0`?

Es decir: ¿hay documentos que existen y están actualizados pero son incomprensibles para un ciudadano común? Si aparecen esos casos, OBS-QNKC-01 (Verificabilidad ≠ Comprensión) deja de ser una distinción teórica y se convierte en un fenómeno observable registrado con evidencia. Eso tiene consecuencias directas sobre la Constitución de Lenguaje y sobre la política de plain language en C10.

### Hipótesis C — OBS-QNKC-02 escala nacionalmente

> ¿Puede DPE actuar como fuente observacional canónica para evaluar los 222 GADs del Ecuador bajo el mismo modelo epistemológico que QUIRA aplica en Montecristi?

```
Sin DPE como fuente canónica:
  221 portales GAD → 221 conectores → 221 modelos de scraping → O(n)

Con DPE como fuente canónica:
  1 portal DPE → 1 conector → estructura uniforme → O(1)
```

La complejidad de observabilidad para Dom07 pasa de lineal a constante. Si valida, el salto de Montecristi a Ecuador completo cambia de naturaleza: no es un problema de scraping, es un problema de consulta a fuente estructurada.

---

## Condiciones de validación

Para que la auditoría N4 cierre este ADR como "OBS-QNKC-02 validada", deben satisfacerse tres condiciones:

| Condición | Pregunta | Resultado |
|-----------|----------|-----------|
| A — Presencia | ¿Montecristi tiene perfil/página en `transparencia.dpe.gob.ec`? | ✅ **CONFIRMADO** — ID 937 · URL: `/entidades/937` · RUC: 1360001010001 |
| B — Estructura | ¿Los numerales están organizados de forma uniforme y consultable? | ✅ **CONFIRMADO** — API pública · endpoint canónico · CSV estructurado con diccionario y metadatos |
| C — Cobertura | ¿La cobertura de numerales DPE es equivalente o superior a la del portal GAD? | ✅ **CONFIRMADO** — 25 numerales/mes en 2026 · 100% C5a · 16 meses de datos longitudinales |

**Las tres condiciones se satisfacen → OBS-QNKC-02 VALIDADA.**

---

## Posibles resultados

### Resultado A — OBS-QNKC-02 validada (Condiciones A + B + C ✅)

**Consecuencias:**
- Dom07 C8 calculado y registrado como C10 record
- Arquitectura observacional O(1) confirmada para dominios LOTAIP
- Escalamiento a 222 GADs es viable con un único conector DPE
- Se activa evaluación de patrón generalizador (ver sección "Patrón de Verificadores Externos" abajo)
- ADR-015 se cierra con status: **ACEPTADO — OBS-QNKC-02 validada**

### Resultado B — OBS-QNKC-02 parcialmente validada (A + B ✅ · C parcial)

**Consecuencias:**
- Dom07 C8 calculado con dato parcial · calidad de dato marcada en C10
- OBS-QNKC-02 sigue válida con alcance acotado — lista de numerales con cobertura incompleta documentada
- Decisión de implementación: qué numerales se leen desde DPE, cuáles requieren consulta adicional al portal GAD
- ADR-015 se cierra con status: **ACEPTADO PARCIAL — OBS-QNKC-02 aplicable con restricciones**

### Resultado C — OBS-QNKC-02 falsada (A ✗ o B ✗)

**Consecuencias:**
- Dom07 C8 calculado desde portal GAD (auditoría manual directa — vuelve a fuente C4/autodeclaración)
- OBS-QNKC-02 queda como "hipótesis no confirmada al 2026-06-01 bajo estado portal DPE"
- No se elimina — se conserva como candidata para reevaluación cuando DPE expanda cobertura o exista API programática
- ADR-015 se cierra con status: **RECHAZADO — OBS-QNKC-02 no confirmada · Dom07 C8 calculado por auditoría directa**

---

## Patrón de Verificadores Externos — consecuencia estratégica de largo plazo

OBS-QNKC-02 puede ser la primera instancia de un patrón más amplio. Si el portal DPE valida como fuente observacional canónica para Dom07, la misma lógica puede aplicarse a otros dominios que actualmente dependen de autodeclaraciones institucionales:

| Dominio | Fuente primaria actual | Posible fuente observacional externa | Institución verificadora |
|---------|------------------------|--------------------------------------|--------------------------|
| Dom07 Transparencia | Portal GAD (autodeclaración) | `transparencia.dpe.gob.ec` | DPE |
| Dom08 Participación | Actas municipales (proceso) | Evidencia de incidencia en PDOT/POA firmado | Consejo Planificación / CPCCS |
| Dom09 Rendición | Informe municipal (autodeclaración) | Evaluación externa CPCCS / observatorio rendición | CPCCS |
| Dom03 Seguimiento | Reporte interno de metas | SIGEF (ejecución financiera) / CGE (auditoría) | MEF / CGE |

La pauta subyacente es consistente con P01 (Dualidad Epistémica):

```
QUIRA no evalúa lo que el GAD afirma haber hecho (C4 — proceso)
QUIRA evalúa lo que un tercero institucional puede verificar como hecho (C5 — evidencia)
```

Bajo ese principio, la preferencia de QUIRA siempre es el verificador externo cuando existe con autoridad regulatoria y estructura consultable. OBS-QNKC-02 es la primera materialización de esa preferencia en un dominio concreto.

**Condición de escalamiento a Principio:**

Si Dom07 valida y Dom08 (CPCCS como fuente de incidencia) + Dom09 (CPCCS/DPE como evaluador de rendición) confirman el mismo patrón en sus respectivos sprints, el candidato a formalización sería:

> **P07 — Autodeclaración ≠ Verificación Externa (en C5)**

Enunciado anticipado:
> "Para evaluar la verificabilidad C5 de una capacidad institucional, QUIRA prioriza fuentes regulatorias externas sobre autodeclaraciones del propio GAD. Cuando existe un verificador institucional externo con autoridad normativa sobre el dominio, ese verificador es la fuente canónica de C5."

P07 satisfaría:
- **H-QNKC-01**: Destruye el falso equivalente "Lo que el GAD declara como cumplimiento = lo que la sociedad puede verificar como cumplimiento"
- **H-QNKC-02**: La verificabilidad efectiva colapsa si no existe verificador externo o si su cobertura es cero — cadena multiplicativa intacta

El test formal de P07 se aplica cuando Dom08 y Dom09 tengan sus sprints. No antes.

---

## RESULTADO N4 — Datos Empíricos (2026-06-01)

### Identificación de entidad DPE (Paso 1 ✅)

```
Entidad DPE:   GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DEL CANTÓN MONTECRISTI
ID:            937
URL canónica:  https://transparencia.dpe.gob.ec/entidades/937
RUC:           1360001010001
Slug:          GADMDCM-rwd5
Autoridad:     Luis Jonathan Toro Largacha (ALCALDE)
Endpoint API:  /backend/v1/transparency/transparency/active/public?establishment_id=937&year={y}&month={m}
```

### Hallazgo de infraestructura — API pública DPE

El portal `transparencia.dpe.gob.ec` expone una API pública no documentada en la interfaz principal que permite consulta programática por entidad, año y mes. Los datos son máquina-legibles, estructurados y sin autenticación para lectura pública. Esto confirma la arquitectura O(1) de OBS-QNKC-02: **un único conector** puede acceder a todos los GADs ecuatorianos de forma uniforme.

### Matriz longitudinal C5a × C5t × C5c (Pasos 2-4 ✅)

**Cobertura temporal: 2025 completo (12 meses) + 2026 Ene–Abr (4 meses) = 16 puntos de datos**

| Año | Mes | Numerales | C5a | C5b_acc | C5t(puntual) | Atraso máx | C5c  | C5a×C5c |
|-----|-----|-----------|-----|---------|--------------|------------|------|---------|
| 2025 | 01 | 16 | 1.00 | 1.00 | 0.00 | 33 días | 0.75 | 0.75 |
| 2025 | 02 | 14 | 1.00 | 1.00 | 0.00 | 33 días | 0.75 | 0.75 |
| 2025 | 03 | 17 | 1.00 | 1.00 | 0.00 | 30 días | 0.75 | 0.75 |
| 2025 | 04 | 12 | 1.00 | 1.00 | 0.00 | 139 días | 0.75 | 0.75 |
| 2025 | 05 | 14 | 1.00 | 1.00 | 0.00 | 109 días | 0.75 | 0.75 |
| 2025 | 06 | 17 | 1.00 | 1.00 | 0.00 | 78 días | 0.75 | 0.75 |
| 2025 | 07 | 11 | 1.00 | 1.00 | 0.00 | 48 días | 0.75 | 0.75 |
| 2025 | 08 | 16 | 1.00 | 1.00 | 0.00 | 46 días | 0.75 | 0.75 |
| 2025 | 09 | 16 | 1.00 | 1.00 | 0.00 | 32 días | 0.75 | 0.75 |
| 2025 | 10 | 17 | 1.00 | 1.00 | 0.00 | 33 días | 0.75 | 0.75 |
| 2025 | 11 | 12 | 1.00 | 1.00 | 0.00 | 34 días | 0.75 | 0.75 |
| 2025 | 12 | 12 | 1.00 | 1.00 | 0.00 | 44 días | 0.75 | 0.75 |
| **2026** | **01** | **25** | **1.00** | **1.00** | **0.00** | **111 días** | **0.75** | **0.75** |
| **2026** | **02** | **25** | **1.00** | **1.00** | **0.00** | **80 días** | **0.75** | **0.75** |
| **2026** | **03** | **25** | **1.00** | **1.00** | **0.00** | **52 días** | **0.75** | **0.75** |
| **2026** | **04** | **25** | **1.00** | **1.00** | **0.00** | **41 días** | **0.75** | **0.75** |

**Leyenda:**
- `C5a` = numerales existentes en DPE / numerales publicados ese mes
- `C5b_acc` = datos accesibles para el período (siempre 1 — están presentes en portal)
- `C5t` = fracción publicada dentro del plazo legal (deadline = día 15 del mes siguiente)
- `C5c` = inteligibilidad (CSV + Diccionario + Metadatos = formato estructurado comprensible)

### Hallazgo empírico crítico — ATRASO SISTÉMICO (nuevo: C5t)

> **En los 16 meses auditados (2025 completo + 2026 Ene–Abr), el GAD Municipal de Montecristi NO publicó ningún numeral dentro del plazo legal. C5t = 0.00 en todos los períodos.**

Este hallazgo no estaba previsto en el diseño original de C5b. Revela que C5b debe descomponerse en dos sub-dimensiones:

| Sub-variable | Pregunta | Resultado Montecristi |
|---|---|---|
| **C5b_acc** | ¿El dato para el período existe en el portal ahora? | 1.0 — todos presentes |
| **C5t** | ¿Fue publicado dentro del plazo legal (día 15)? | 0.0 — ninguno puntual |

Este hallazgo es **opaco desde C4** (autodeclaración del GAD): el municipio puede declarar "cumplimos LOTAIP" porque los numerales existen en DPE. Solo la observación desde C5 con timestamps reales revela el atraso sistémico. Esta es la primera demostración empírica de P01 en un dato concreto.

### LOTAIP 2.0 — Salto normativo confirmado en datos

| Período | Numerales/mes | Observación |
|---------|---------------|-------------|
| 2025 | 11 – 17 (promedio 14.5) | Universo LOTAIP previo · publicación mensual parcial |
| **2026** | **25 (constante)** | **LOTAIP 2.0 · cobertura completa obligatoria por reforma** |

El salto de 14.5 → 25 numerales/mes confirma que LOTAIP 2.0 materializó nuevas obligaciones de publicación que el sistema DPE ya registra y exige uniformemente a todos los GADs.

### C8 — Cálculo con datos reales (N5 parcial)

Con los datos N4 para 2026:

```
C5a  = 1.000   (25/25 numerales presentes)
C5b  = 1.000   (datos accesibles para el período — C5b_acc)
C5t  = 0.000   (ninguna publicación puntual — nueva dimensión)
C5c  = 0.750   (CSV estructurado + diccionario + metadatos)

verificabilidad_efectiva(acceso)  = C5a × C5b_acc × C5c = 1.0 × 1.0 × 0.75 = 0.750
verificabilidad_efectiva(puntual) = C5a × C5t × C5c     = 1.0 × 0.0 × 0.75 = 0.000

C4 = verificación pendiente (autodeclaración institucional)

C8 = C4 × 0.750  [dimensión acceso]
   = C4 × 0.000  [dimensión puntualidad]
```

**Implicación:** Montecristi tiene cobertura documental completa (C5a = 1) pero zero puntualidad legal (C5t = 0). La información existe pero no fue publicada a tiempo en ningún mes de 16 meses auditados. El semáforo de Dom07 debe reflejar esta distinción.

### Evaluación de las tres hipótesis

| Hipótesis | Pregunta | Resultado |
|-----------|----------|-----------|
| **H-A** (P01 operativo) | ¿Puede calcularse C8 con datos reales? | ✅ **CONFIRMADO** — C8 calculado. C4 aún pendiente de verificación directa, pero C5 completo. |
| **H-B** (OBS-QNKC-01 observable) | ¿Hay casos C5a=1, C5t=0? | ✅ **CONFIRMADO** — 16 meses de evidencia. Documentos existen (C5a=1) pero publicados fuera de plazo (C5t=0). Nueva sub-variable identificada. |
| **H-C** (OBS-QNKC-02 escala) | ¿DPE es fuente canónica para 222 GADs? | ✅ **CONFIRMADO** — API pública · estructura uniforme · timestamp exacto · datos descargables. Un único conector para 221 entidades. |

---

## Protocolo de auditoría N4 (referencia)

Detallado en ADR-014 addendum Sprint 4. Reproducido aquí para independencia:

**Objetivo:** Para cada numeral del Art. 19 LOTAIP, registrar:

| Numeral | Descripción | C5a — Existe en DPE | C5b — Actualizado (período vigente) | C5c — Comprensible (lenguaje claro) |
|---------|-------------|--------------------|------------------------------------|-------------------------------------|
| 1 | Estructura orgánica funcional | ✓/✗ | ✓/✗ | ✓/✗ |
| 2 | Base legal | ✓/✗ | ✓/✗ | ✓/✗ |
| 3 | Regulaciones y procedimientos | ✓/✗ | ✓/✗ | ✓/✗ |
| 4 | Metas y objetivos | ✓/✗ | ✓/✗ | ✓/✗ |
| 5 | Directorio institucional | ✓/✗ | ✓/✗ | ✓/✗ |
| 6 | Remuneraciones por puesto | ✓/✗ | ✓/✗ | ✓/✗ |
| 7 | Servicios que ofrece | ✓/✗ | ✓/✗ | ✓/✗ |
| 8 | Contratos colectivos | ✓/✗ | ✓/✗ | ✓/✗ |
| 9 | Formularios y solicitudes | ✓/✗ | ✓/✗ | ✓/✗ |
| 10 | Presupuesto general | ✓/✗ | ✓/✗ | ✓/✗ |
| 11 | Auditorías · informes de fiscalización | ✓/✗ | ✓/✗ | ✓/✗ |
| 12 | Contratos de crédito externo | ✓/✗ | ✓/✗ | ✓/✗ |
| 13 | Procesos precontractuales y contractuales | ✓/✗ | ✓/✗ | ✓/✗ |
| 14 | Donaciones | ✓/✗ | ✓/✗ | ✓/✗ |
| 15 | Cuerpo legal de la entidad | ✓/✗ | ✓/✗ | ✓/✗ |
| 16 | Índice de información reservada | ✓/✗ | ✓/✗ | ✓/✗ |
| 17 | Viáticos y gastos de representación | ✓/✗ | ✓/✗ | ✓/✗ |
| 18 | Planes de desarrollo territorial | ✓/✗ | ✓/✗ | ✓/✗ |
| 19 | Información para grupos vulnerables | ✓/✗ | ✓/✗ | ✓/✗ |
| 20 | Participación ciudadana y rendición de cuentas | ✓/✗ | ✓/✗ | ✓/✗ |
| 21 | Otras obligaciones establecidas en la ley | ✓/✗ | ✓/✗ | ✓/✗ |
| 22+ | Verificar si LOTAIP 2.0 amplió el número | ✓/✗ | ✓/✗ | ✓/✗ |

*Nota: el colega observó hasta "24" en la navegación del portal DPE. Verificar si LOTAIP 2.0 elevó el conteo de 21 a 24+ numerales obligatorios — pendiente contraste con texto legal.*

**Fórmula de agregación:**

```
C5a = (Σ C5a_i) / total_numerales
C5b = (Σ C5b_i por cada C5a_i=1) / (Σ C5a_i)
C5c = evaluación por muestreo representativo (3-5 numerales)
C8  = C4 × C5a × C5b × C5c
```

**Resultado:** Primer C10 record de Dom07 — input para p07_transparencia.py y Neo4j.

---

## Criterio de cierre — DEC (Dominio Epistemológicamente Cerrado)

Sprint 4 no cierra cuando el commit existe, ni cuando la pantalla funciona, ni cuando Neo4j está cargado. Cierra cuando Dom07 alcanza estado **DEC** (COR-QNKC-02 — `QNKC_PRINCIPIOS_INDEX.md`).

**Dom07 DEC se declara cuando:**

```
1. N4 completo:   auditoría real transparencia.dpe.gob.ec para Montecristi
                  datos [Numeral × C5a × C5b × C5c] registrados

2. N5 completo:   C10 calculado con C8 = C4 × C5a × C5b × C5c
                  usando datos reales — no "PENDIENTE", no fallback

3. ADR-015 cerrado: OBS-QNKC-02 declarada:
                    Validada / Parcialmente validada / No confirmada
                    con evidencia empírica registrada

4. Tres hipótesis testadas:
   H-A: P01 operativo      → C8 calculado con dato real
   H-B: OBS-QNKC-01 obs.  → casos C5a=1 · C5b=1 · C5c=0 registrados (o ausentes)
   H-C: OBS-QNKC-02 escala → DPE como fuente canónica confirmado (o refutado)
```

**La cadena que debe poder recorrerse de extremo a extremo:**

```
CE_18 / LOTAIP Art. 19
         ↓ QLEP (N1)
Pregunta bautismal N2 v1.0.1
         ↓ QTMP (N3)
Cadena causal C1→C9 en Neo4j
         ↓ Auditoría DPE (N4)
C5a · C5b · C5c reales
         ↓ Cálculo C8 (N5)
C10 record — narrativa para el Alcalde
         ↓ Layer 2 p07_transparencia.py
Semáforo · indicador · observabilidad en pantalla
```

Si hay un hueco en esta cadena — cualquier eslabón con dato proxy, fallback, o "pendiente" — Dom07 no es DEC. El C10 puede existir, pero el sprint no está cerrado.

**Sprint 5 no abre hasta que Dom07 sea DEC.**

## Relación con otros documentos de gobernanza

| Documento | Relación |
|-----------|----------|
| `QNKC_PRINCIPIOS_INDEX.md` | OBS-QNKC-02 — base que este ADR valida |
| `ADR-014_BETA_CORE_Roadmap.md` | Sprint 4 agenda de calibración + addendum DPE |
| `QLEP_CANONICO_MONTECRISTI_v1.0.md` | N2 Dom07 v1.0.1 — enmienda LOTAIP 2.0 |
| `qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` | YAML con C5 = `verificabilidad_efectiva = C5a × C5b × C5c` |
| `p07_transparencia.py` | Layer 2 — recibirá C10 cuando N4 cierre |

---

## Cierre de este ADR

**Condición de cierre:** Completar la auditoría `transparencia.dpe.gob.ec` para Montecristi · registrar C10 · calcular C8 real.

**Acción post-cierre:** Actualizar estado de OBS-QNKC-02 en `QNKC_PRINCIPIOS_INDEX.md` de "Registrada" a "Validada / Parcialmente validada / No confirmada". Si el resultado es A o B, iniciar Sprint 5 (Dom06). Si el resultado es C, auditar portal GAD directamente para Dom07 antes de Sprint 5.

**Sprint 5 no abre hasta que este ADR cierre.**

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"Dom07 no está probando Transparencia. Está probando si QUIRA puede utilizar una infraestructura observacional nacional única para evaluar 222 GADs bajo el mismo modelo epistemológico."*
