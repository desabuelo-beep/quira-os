# QUIRA Territorial Semantics v1.0
**Ontología del Territorio — Definición Canónica de Unidades Territoriales**

**Versión**: 1.0 — CONGELADO  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Fecha**: 2026-05-31  
**Estado**: Alpha 0.9 — documento fundacional pre-Neo4j  
**Caso fundante**: Montecristi — descubrimiento Colorado/El Arroyo, ISM/GEA urbanas

---

## PRINCIPIO FUNDACIONAL

> La unidad territorial administrativa (COOTAD) y la unidad territorial censal (INEC) no son la misma cosa.
> Confundirlas produce datos incorrectos, políticas mal dirigidas e indicadores que mienten.

QUIRA mantiene dos sistemas de clasificación territorial en paralelo — sin colapsar uno en el otro:

```
Sistema COOTAD       ≠        Sistema INEC
─────────────────             ─────────────────
Función administrativa        Realidad censal medida
Parroquia urbana/rural        Zona área_urbana/área_rural
Definida por alcance          Definida por densidad
  de servicios                  de población/vivienda
Inmutable por decreto         Actualizable por censo
```

El PDOT es el único instrumento que ARTICULA ambos sistemas. Ver Sección VII.

---

## I. JERARQUÍA TERRITORIAL CANÓNICA — 7 NIVELES

```
Nivel 0  País                  Ecuador (ECU)
Nivel 1  Provincia             Manabí (13)
Nivel 2  Cantón                Montecristi (ECU-13-MONTECRISTI)
Nivel 3a Parroquia COOTAD      Colorado, La Pila, Isabel Muentes... (función administrativa)
Nivel 3b Zona INEC             área_urbana / área_rural (clasificación censal)
Nivel 4  Sector Censal INEC    ~200 viviendas (unidad básica CPV 2022)
Nivel 5  PUGS / Uso de suelo   (clasificación Plan de Uso y Gestión del Suelo)
Nivel 6  Comuna / Comunidad    El Arroyo, El Chorrillo, Los 3 Bajos... (unidad social informal)
Nivel 7  Manzana / Predio      (unidad catastral — GAD central)
```

---

## II. CANTÓN — Nivel 2

**Definición COOTAD**: Unidad político-administrativa con GAD Municipal. Tiene personería jurídica, presupuesto propio, autonomía administrativa.

**Identificador QUIRA**: `ECU-[código_provincia]-[NOMBRE]`  
Ejemplo: `ECU-13-MONTECRISTI`

**Dato canónico**:
- Indicadores de nivel cantonal son OBSERVADOS o CALCULADOS (nunca proxies de otro cantón)
- Ti de inversión, ICPI, IRS, NBI cantonal → fuente primaria

---

## III. PARROQUIA COOTAD — Nivel 3a

**Definición COOTAD Art. 24-27**: Unidad político-administrativa dentro del cantón. Puede ser:
- **Parroquia urbana**: ejerce funciones dentro del área urbana del cantón (servicios de infraestructura, transporte, aseo). No necesariamente densa ni continua.
- **Parroquia rural**: ejerce funciones en territorio rural, con competencias agropecuarias y comunitarias específicas (COOTAD 267).

**LO QUE ESTO NO SIGNIFICA** (error frecuente):
- Parroquia urbana ≠ toda la parroquia es área urbana INEC
- Parroquia rural ≠ toda la parroquia es área rural INEC

**Caso Montecristi — clasificación canónica**:

| Código | Parroquia | Tipo COOTAD | Nota |
|--------|-----------|-------------|------|
| MCU | Montecristi (cabecera) | urbana | contiene comunas rurales: Los 3 Bajos, Las Toallas, otros |
| LPL | La Pila | **rural** | ÚNICA parroquia rural del cantón |
| CLR | Colorado | urbana | contiene comunas rurales: El Arroyo, El Chorrillo |
| PRN | Leonidas Proaño | urbana | — |
| ANS | Aníbal San Andrés | urbana | — |
| GEA | General Eloy Alfaro | urbana | — |
| ISM | Isabel Muentes | urbana | mayor rezago cantonal: desechos 70%, agua precaria |

**Regla QUIRA**: La clasificación COOTAD de una parroquia no puede usarse como proxy de su NBI real. Las parroquias urbanas pueden tener NBI más alto que el promedio urbano si contienen comunas con características rurales.

---

## IV. ZONA INEC — Nivel 3b

**Definición INEC**: Clasificación censal (CPV 2022) que divide el territorio en:
- `area_urbana`: áreas con alta densidad, acceso a servicios básicos (agua, alcantarillado, electricidad), población ≥ determinada densidad
- `area_rural`: áreas con baja densidad, menor acceso a servicios, características productivas agropecuarias predominantes

**Diferencia crítica con COOTAD**:
La zona INEC es una MEDICIÓN de la realidad, no una designación administrativa.  
Una parroquia COOTAD urbana puede contener sectores censales de zona_inec rural.

**Datos NBI INEC 2022 — Cantón Montecristi**:
```
NBI zona_inec área_urbana:  21.3%   (← aplica a sectores urbanos, no a parroquias urbanas)
NBI zona_inec área_rural:   53.3%   (← aplica a sectores rurales, incluyendo dentro de parroquias urbanas)
```

**Uso en QUIRA**:
- NBI por zona INEC = `observado` (fuente primaria INEC 2022)
- NBI por parroquia COOTAD = `proxy` si se deriva de zona INEC (hasta que existan microdatos DPA)
- `pendiente_microdato` = estado correcto para NBI parroquial no confirmado

---

## V. SECTOR CENSAL INEC — Nivel 4

**Definición**: Unidad básica de relevamiento censal. ~200 viviendas. Tiene código INEC único (DPA — División Político Administrativa).

**Relevancia QUIRA**:
- Es el nivel más granular con datos NBI reales disponibles (INEC microdatos DPA 2022)
- Permite calcular NBI por parroquia SIN proxy: agrupar sectores censales dentro de cada parroquia
- Es la fuente que convierte `pendiente_microdato` → `confirmado` para indicadores parroquiales
- Requiere procesamiento de microdatos INEC (archivo DPA 2022)

**Estado actual en Montecristi**: PENDIENTE — Red Académica (UEB/ESPAM) es el socio natural para procesar estos microdatos.

---

## VI. PUGS — Plan de Uso y Gestión del Suelo — Nivel 5

**Definición LOOTUGS / COOTAD**: Instrumento de planificación del uso del suelo que clasifica formalmente el territorio en categorías de uso, densidad y aprovechamiento.

**Relevancia QUIRA** (principio PDOT como Constitución Territorial — ver Sección VII):
- El PUGS es el instrumento que **reconoce formalmente** las zonas rurales dentro de parroquias urbanas
- Cuando el PUGS clasifica como "suelo rural de producción" una zona dentro de una parroquia urbana, esa clasificación tiene valor jurídico superior a la designación administrativa COOTAD
- El PUGS de Montecristi reconoce comunas como El Arroyo, Los 3 Bajos como territorios con características rurales

**Implicación para QUIRA**:
- El PUGS es fuente de verdad territorial para la capa GeoTwin
- Los 12 dominios deben mapearse sobre el PUGS, no solo sobre la división parroquial

---

## VII. EL PDOT COMO CONSTITUCIÓN TERRITORIAL — Principio Fundacional

**Definición operativa QUIRA**:

```
PDOT ≠ fuente de datos
PDOT = síntesis territorial oficial del cantón
```

El PDOT contiene:
```
Diagnóstico        → realidad territorial medida y documentada
Propuesta          → metas de intervención municipal por eje temático
Modelo de Gestión  → cómo el GAD estructura su acción territorial
PUGS               → clasificación formal del uso del suelo
```

**Implicación metodológica**:
- El diagnóstico PDOT es la realidad territorial canónica — incluye NBI, acceso a servicios, vulnerabilidades, y reconoce la realidad de comunas dentro de parroquias
- Las propuestas PDOT son las metas que QUIRA monitorea como Dom01-Dom12
- El PUGS PDOT es la capa base del GeoTwin
- El PDOT debe tratarse como la Constitución Territorial del cantón — así como QLEP atomiza la Constitución Nacional, QUIRA Territorial (fase post-Alpha) atomizará el PDOT

**La cadena PDOT→QUIRA**:
```
PDOT (diagnóstico)
    ↓ define la realidad que se debe subsanar
QUIRA (12 dominios)
    ↓ monitorea la intervención del GAD sobre esa realidad
GeoTwin (PDOT vivo)
    ↓ muestra territorialmente cada dominio
QUIRA IA
    ↓ conecta causalidades entre diagnóstico, intervención y resultado
```

---

## VIII. COMUNA / COMUNIDAD ANCESTRAL — Nivel 6

**Definición**: Unidad social y productiva de organización comunitaria. No es una parroquia COOTAD ni un sector censal INEC — es una unidad social con territorio histórico reconocido.

**Características**:
- Puede estar dentro de parroquias urbanas o rurales
- Puede cruzar límites de sectores censales INEC
- Algunas tienen características rurales aunque estén en parroquias urbanas COOTAD
- El PDOT las reconoce explícitamente en el diagnóstico territorial

**Caso Montecristi — comunas identificadas**:

| Parroquia COOTAD | Comunas identificadas | Naturaleza |
|---|---|---|
| Montecristi (MCU) | Los 3 Bajos, Las Toallas, Las Cárceles, otras | rural dentro de parroquia urbana |
| Colorado (CLR) | El Arroyo, El Chorrillo | rural dentro de parroquia urbana |
| La Pila (LPL) | — (parroquia rural completa) | rural |

**Relevancia QUIRA**: Las comunas explican por qué el NBI real de parroquias urbanas puede superar el promedio de la zona_inec urbana. Un proxy basado solo en zona_inec urbana subestima la necesidad de parroquias como Colorado.

---

## IX. REGLAS DE INTEROPERABILIDAD ENTRE NIVELES

```
Regla T1 — Dirección de proxy válida:
  zona_inec → parroquia COOTAD: PERMITIDO (con proxy_de explícito)
  cantón → parroquia: PERMITIDO (con proxy_de explícito)
  parroquia → sector censal: PROHIBIDO (sin microdatos reales)
  parroquia → parroquia: PROHIBIDO (territorios distintos, sin base empírica)

Regla T2 — COOTAD vs INEC:
  Nunca usar clasificación COOTAD para inferir NBI
  Nunca usar zona INEC para inferir competencias GAD
  El PDOT es el puente oficial entre ambos sistemas

Regla T3 — Parroquias urbanas con características rurales:
  Cuando el PUGS o el diagnóstico PDOT documenta comunas rurales
  dentro de una parroquia urbana, el proxy zona_inec urbana
  se declara con validez: "provisional" (NO conservador)
  Razón: subestima la necesidad real de esa parroquia

Regla T4 — Sector censal como unidad de confirmación:
  El único camino para convertir pendiente_microdato → confirmado
  en NBI parroquial es el cruce con microdatos INEC DPA 2022
  No existe atajo metodológico que no pase por los datos reales

Regla T5 — PDOT como referencia normativa:
  Cuando PDOT diagnóstico cita un valor (NBI, pobreza, servicios)
  ese valor es fuente de Nivel 2 (no primaria INEC, no proxy)
  Debe citarse como "Diagnóstico PDOT [año]" con estado_dato:
  pendiente_validacion hasta cruzar con INEC
```

---

## X. NODO NEO4J — TIPOLOGÍA DE ENTIDADES TERRITORIALES

```cypher
// Tipos de nodo territorial en el grafo QUIRA
(:Canton)         {id: 'ECU-13-MONTECRISTI', nombre: 'Montecristi', ...}
(:ParroquiaCOOTAD) {id: 'MCU', tipo_cootad: 'urbana', tiene_comunas_rurales: true}
(:ZonaINEC)       {id: 'INEC-UB-MCR', tipo: 'area_urbana', nbi_pct: 21.3}
(:SectorCensal)   {id: 'DPA-130801-001', viviendas: ~200}
(:PUGS)           {id: 'PUGS-MCR-CLR-RURAL', clasificacion: 'suelo_rural_produccion'}
(:Comuna)         {id: 'COM-EL-ARROYO', parroquia_id: 'CLR', naturaleza: 'rural'}

// Relaciones clave
(p:ParroquiaCOOTAD)-[:CONTIENE]->(c:Comuna)
(z:ZonaINEC)-[:SUPERPONE_CON]->(p:ParroquiaCOOTAD)
(s:SectorCensal)-[:PERTENECE_A]->(z:ZonaINEC)
(pugs:PUGS)-[:CLASIFICA]->(p:ParroquiaCOOTAD)
```

---

## XI. ANTI-PATRONES TERRITORIALES

| Anti-patrón | Efecto | Corrección |
|---|---|---|
| **COOTAD = INEC** | NBI parroquial incorrecto (subestima necesidad) | Declarar proxy + validez: provisional |
| **Parroquia urbana = zona urbana** | Comunas rurales invisibles para la política | Revisar PDOT/PUGS para comunas internas |
| **Proxy parroquia rural = 53.3%** para GEA/ISM | Error de clasificación — GEA/ISM son urbanas COOTAD | Ya corregido en QTMP v1.1 (2026-05-31) |
| **Agregar comunas en parroquia** sin base | No tiene fundamento legal sin PUGS | Documentar como referencia PDOT, no como límite |
| **Ignorar PDOT** en análisis territorial | Perder la síntesis oficial del cantón | PDOT es fuente Nivel 2, siempre referenciable |

---

## XII. ESTADO DE CONFIRMACIÓN — MONTECRISTI 2026-05-31

```
CONFIRMADOS (observado / calculado):
  NBI cantonal zona_urbana:  21.3%  ← INEC CPV 2022
  NBI cantonal zona_rural:   53.3%  ← INEC CPV 2022
  Parroquia La Pila = única rural COOTAD del cantón ← confirmado

PROXIES DOCUMENTADOS (pendiente_microdato):
  NBI parroquias urbanas (CLR, PRN, ANS, GEA, ISM): proxy = 21.3%
    → validez: provisional (excepto CLR: "baja confianza" por El Arroyo/El Chorrillo)
  NBI parroquia La Pila: proxy = 53.3%
    → validez: provisional, conservador (es la única rural)

PENDIENTE DE CONFIRMACIÓN (fuente_requerida: INEC_DPA_PARROQUIAL):
  Todos los nodos RES_EQUD_01_[parroquia]
  → Requiere: microdatos DPA 2022, procesamiento por sectores censales
  → Socio natural: Red Académica (UEB/ESPAM)
```

---

*QUIRA Territorial Semantics v1.0 — CONGELADO 2026-05-31*  
*Versión siguiente: v1.1 tras ingesta microdatos INEC DPA + PDOT atomizado*  
*Custodio: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO*
