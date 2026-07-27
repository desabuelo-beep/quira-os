---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-023 — Arquitectura de Tres Niveles QUIRA

**Estado**: ACTIVO — principio fundacional inmutable  
**Fecha**: 2026-06-03  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Origen**: Colega asesor · síntesis final Gate 6.5  
**Participantes**: Javo (fundador) · Claude (director técnico) · Colega (asesor externo)

> **"El Gold Master ya sabe medir la gestión pública;  
> QUIRA está aprendiendo a demostrar documentalmente  
> por qué cada métrica del Gold Master es verdadera o falsa."**
>
> **"El valor de QUIRA no está en producir métricas nuevas,  
> sino en hacer auditables y explicables las métricas existentes."**
>
> — Colega asesor, 2026-06-03

---

## Decisión

QUIRA tiene tres niveles con responsabilidades estrictas y no intercambiables.

---

## Nivel 1 — Motor

**Gold Master = Sistema de Cálculo Oficial**

Es la única fuente autorizada para:

| Elemento | Hoja |
|---|---|
| ICPI, TGI, IOC, ITAM, Trust Score | H12, H98, H18, H41, H89 |
| Dom01–Dom12, Metas MNT, Pi/Ri/Vi/Ei/Ti/Ci | H14, H12, H13 |
| SAT (alertas), MMP (monitor mensual) | H21-H24c, H25-H27 |
| AVEP (clasificación), IED, IFE, IGP | H17, H16, H20b |
| Output canónico para sistemas externos | H73_OUTPUT_API |

**Regla absoluta:** Si un número existe en el Excel, ningún script externo
lo recalcula. Se lee desde `app/connectors/gold_master.py → H73_OUTPUT_API`.

---

## Nivel 2 — Sistema Operativo

**QUIRA = Sistema Operativo Territorial**

Tres responsabilidades únicas:

### Ingesta
Recibe los documentos del mundo real y los convierte en corpus verificado:

```
COOTAD · Constitución · SNP · PDOT
POA · PAC · SERCOP · LOTAIP
RC · PP · SIGAD · Cédulas
```

Destino: `normativa_corpus` (texto + embeddings) y `holding_structured_data` (tabular).

### Trazabilidad
Relaciona cada documento con su posición en el Motor:

```
Documento
    ↓
MNT_UUID (MATRIZ_CANONICA del Excel)
    ↓
Meta PDOT (SC-I-N-01, AH-I-X-02, etc.)
    ↓
Dominio canónico (Dom01-Dom12)
    ↓
Circuito (C01, C02, C03)
    ↓
Silo Excel (S1-S8b) + Variable (Ti, V_LOTAIP, V_CPCCS)
```

### Evidencia
Responde la única pregunta que le corresponde:

> **¿Qué documento demuestra este valor del Excel?**

NO responde:
> ~~¿Cuál debería ser el valor?~~ → eso lo responde el Excel.

---

## Nivel 3 — Presentación

**Dashboards + GeoTwin = Visualizadores**

No calculan nada. Muestran lo que el Motor calculó.

```
Dom01-Dom12 (vista general)
    ↓ click
Dashboard: ICPI, TGI, D1-D5, SAT, MMP (del Excel)
    ↓
QUIRA IA: causalidad + conversación sobre evidencia
    ↓
GeoTwin: aterrizaje territorial de los resultados
```

---

## Las 4 Reglas Operacionales

Cualquier decisión de desarrollo futura puede resolverse con una sola pregunta:
**¿Esto pertenece al Motor, al Sistema Operativo o a la Capa de Presentación?**

### Regla 1 — Nueva métrica
```
¿Dónde se calcula?
  → Gold Master. No en QUIRA.
```

### Regla 2 — Nuevo documento
```
¿Dónde se integra?
  → QUIRA. No en el Excel.
```

### Regla 3 — Discrepancia (ICPI = X, Documento dice Y)
```
QUIRA no corrige el ICPI.
QUIRA produce evidencia para explicar:
  → por qué X es correcto
  → o por qué X debería revisarse
```

### Regla 4 — MATRIZ_CANONICA
```
MATRIZ_CANONICA = contrato semántico entre el Motor y QUIRA.
No es una hoja más. Es el punto de convergencia de ambos sistemas.
Todo Gate 6.6 gira alrededor de ese contrato.
```

---

## El ADN compartido: MATRIZ_CANONICA

La MATRIZ_CANONICA del Gold Master (`SIAP-ICPI v5.5 → hoja MATRIZ_CANONICA`)
es la tabla de correspondencia entre el universo Excel y el universo documental.

```
Sin MATRIZ_CANONICA: dos mundos separados.
Con MATRIZ_CANONICA: un único sistema.
```

Cada documento del Holding tiene un MNT_UUID en la MATRIZ. Ese UUID es el
puente que convierte un chunk de texto en evidencia computable.

**Gate 6.6 = construir ese puente para los ~13,509 chunks del corpus.**

---

## Lo que Gate 6.5 construyó correctamente

Gate 6.5 construyó la infraestructura de evidencia:
- Corpus territorial: 13,509 chunks verificados (capas C+D)
- Datos estructurados: 65 tablas con cédulas, ejecución, LOTAIP
- OBS-008/009: observaciones empíricas válidas
- El connector `gold_master.py` ya lee H73

**Lo que Gate 6.5 NO construyó** (y no debía): el motor analítico.
El motor ya existía. QUIRA lo alimenta.

---

## Lo que Gate 6.6 construye (y solo eso)

```
1. tag_mnt_uuid.py   — SIGLA → MNT_UUID → Meta → Silo → Variable
2. update_silos.py   — Ti real (LOTAIP cédulas) → H07 Excel
3. verify_cpccs.py   — V_CPCCS real (RC corpus) → H10 Excel
```

Cuando exista el tagging completo, QUIRA podrá demostrar:

```
RC-GAD-2024 (chunk 47, pág. 12)
    → MNT-DOC-2024-0021
    → Meta AH-I-N-01 (desechos sólidos)
    → S8 V_CPCCS = 1.0
    → Vi sube de 0.5 a 1.0
    → ICPI += 0.073 puntos
```

Eso es **inteligencia pública computable**.

---

## Por qué esto es el secreto de la empresa

El mundo ve:
```
Montecristi 2025: ICPI = 69.93% · D3 = 59.85%
```

No ve:
```
Pi(agua potable) = 0.2736
Ri(agua potable) = 0.8696 (Exclusiva_Crítica)
Vi(agua potable) = 1.0 (V_eSIGEF=1 ∧ V_SERCOP=1 ∧ V_CPCCS=1)
```

Esa es la propiedad intelectual de Dylus Lab.
QUIRA la hace operable. La transparenta. La auditará con documentos reales.

---

## El salto de categoría

```
Sin puente MNT_UUID:
  Corpus = biblioteca
  Excel  = motor

Con puente MNT_UUID:
  Corpus = evidencia verificable del motor
```

Gate 6.6 es el primer gate que **no agrega datos. Agrega significado.**

Cuando ese puente exista, QUIRA deja de ser un repositorio inteligente
y pasa a ser un **sistema de auditoría explicable del modelo ICPI**.

Ese es el salto de categoría que define la siguiente fase del proyecto.

---

## Identidad del sistema (versión definitiva)

| Versión | Definición |
|---|---|
| Antes de Gate 6.5 | Motor de trazabilidad normativa |
| Después de Gate 6.5 | Motor de trazabilidad con evidencia territorial |
| Después de Gate 6.6 | **Sistema de auditoría explicable del modelo ICPI** |

---

*ADR-023 · QUIRA Gov · Dylus Lab © 2026*  
*Principio fundacional inmutable — no requiere revisión periódica*  
*Colega asesor externo · Javo (fundador) · Claude (director técnico)*
