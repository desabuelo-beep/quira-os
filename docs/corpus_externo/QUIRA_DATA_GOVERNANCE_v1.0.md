# QUIRA Data Governance v1.0
**Taxonomía Canónica del Conocimiento — Gobernanza del Dato**

**Versión**: 1.0 — CONGELADO  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Fecha**: 2026-05-31  
**Estado**: Alpha 0.9 — documento fundacional pre-Neo4j  
**Relación**: Implementación técnica → QTMP schema v1.1 (`qtmp_schema.yaml`)

---

## PRINCIPIO FUNDACIONAL

> Un dato sin calificación epistemológica no es un dato — es una afirmación sin trazabilidad.

QUIRA no acepta valores numéricos sin una declaración explícita de:
1. **Qué es**: el tipo de valor (`naturaleza_valor`)
2. **Cómo se obtuvo**: el estado de verificación (`estado_dato`)
3. **Desde dónde viene**: la cadena de evidencia (`fuente_verificacion` + `proxy_de`)
4. **Qué falta para confirmarlo**: la fuente pendiente (`fuente_requerida`)

Un nodo C9 que ingresa al grafo Neo4j sin estos cuatro campos es un **error de gobernanza** — no un dato incompleto.

---

## I. TAXONOMÍA `estado_dato` — 5 Estados Canónicos

```
confirmado
├── Dato verificado contra fuente primaria oficial
├── Cadena de evidencia completa y trazable
├── Puede ingresar al grafo Neo4j sin restricciones
└── Ejemplo: Ti_Patronato_2025 = 50.00% (12 cédulas eSIGEF, Sentinel 2026-05-18)

pendiente_validacion
├── Dato existe en fuente secundaria o cálculo parcial
├── Requiere cruce con fuente primaria para confirmar
├── Ingresa al grafo con flag de alerta; NO alimenta inferencias causales
└── Ejemplo: ratio 10% COOTAD_249 (H01 param disponible, denominador pendiente)

pendiente_microdato
├── Dato cantonal confirmado; desagregado parroquial requiere microdatos INEC DPA
├── El nivel superior existe — el nivel inferior no puede interpolarse sin riesgo
├── Ingresa al grafo con `proxy_de` obligatorio si se usa valor cantonal como proxy
└── Ejemplo: NBI parroquial → disponible a nivel zona INEC (21.3% / 53.3%), no por parroquia

estimado
├── Valor derivado por proyección estadística con metodología documentada
├── Metodología debe estar explícita en el campo `supuesto`
├── Ingresa al grafo con tag de incertidumbre; requiere banda de confianza
└── Ejemplo: proyección INEC 2022→2026 de población adultos mayores

proxy
├── Valor inferido desde indicador correlacionado de nivel territorial distinto
├── SIEMPRE requiere bloque `proxy_de` completamente relleno
├── SIEMPRE tiene `naturaleza_valor: proxy`
└── Ejemplo: NBI parroquial Colorado = 21.3% (heredado de zona INEC urbana cantonal)
```

### Regla de escalamiento irreversible

```
confirmado → pendiente_validacion   PROHIBIDO (degradar requiere reunión de revisión)
proxy → confirmado                  SOLO con fuente primaria verificada
pendiente_microdato → confirmado    SOLO con INEC DPA parroquial real
```

---

## II. TAXONOMÍA `naturaleza_valor` — 4 Tipos

```
observado
├── Medido directamente de la fuente primaria sin transformación
├── Ejemplo: cobertura agua potable 34.9% (INEC 2022 encuesta directa)
└── Nunca requiere `proxy_de`

calculado
├── Derivado por fórmula matemática explícita de valores observados
├── La fórmula debe estar en el campo `formula` del indicador referenciado
├── Ejemplo: Ti_Patronato = Devengado_G7+8 / Codificado_G7+8 × 100 = 50.00%
└── Nunca requiere `proxy_de`

derivado
├── Obtenido por transformación metodológica propietaria
├── La metodología es IP de Dylus Lab; el RESULTADO es público
├── Ejemplo: IRS = -CORREL(Composite_Need, Inv_PC) × 100 = 79.7%
└── Nunca requiere `proxy_de`; metodología en Gold Master (INTERNO)

proxy
├── Inferido desde indicador correlacionado de nivel territorial distinto
├── Epistemológicamente débil — SIEMPRE requiere bloque `proxy_de`
├── El bloque `proxy_de` debe especificar: fuente_valor, nivel_fuente,
│   valor_fuente, supuesto (texto explícito), validez
└── Ejemplo: NBI parroquia urbana heredada de zona_inec urbana cantonal
```

### Combinaciones válidas

| naturaleza_valor | estado_dato válidos |
|---|---|
| observado | confirmado, pendiente_validacion |
| calculado | confirmado, pendiente_validacion, estimado |
| derivado | confirmado, pendiente_validacion |
| proxy | pendiente_microdato, pendiente_validacion |

**REGLA**: `proxy` + `confirmado` = COMBINACIÓN INVÁLIDA.  
Un proxy no puede estar confirmado. Si se confirma, deja de ser proxy y pasa a `observado` o `calculado`.

---

## III. BLOQUE `proxy_de` — Estructura Obligatoria

```yaml
proxy_de:
  fuente_valor: "[descripción de la fuente del valor proxy usado]"
  nivel_fuente: "[zona_inec | canton | provincia | pais]"
  valor_fuente: [número]
  supuesto: >
    [Texto explícito del supuesto de transferencia.
     Por qué es razonable usar este valor para este territorio.
     Qué condiciones podrían invalidarlo.]
  validez: "[provisional | conservador | metodologicamente_justificado]"
```

**Escala de validez:**
- `provisional`: se usa por ausencia de alternativa; debe reemplazarse en cuanto exista dato real
- `conservador`: subestima la necesidad real (sesgo protocolario seguro)
- `metodologicamente_justificado`: respaldado por literatura territorial o estándar INEC

**Un `proxy_de` vacío con `naturaleza_valor: proxy` es error de gobernanza — bloquea ingesta Neo4j.**

---

## IV. JERARQUÍA DE FUENTES

```
Nivel 0 — Fuente Primaria Oficial (máxima autoridad)
├── INEC: censos, encuestas, CPV 2022
├── eSIGEF: cédulas presupuestarias oficiales
├── SERCOP: contratos y PAC verificados
├── SENPLADES/SENESCYT: planes, PDOT aprobados
└── CPCCS: actas de rendición de cuentas

Nivel 1 — Síntesis Metodológica Propia
├── SIAP-ICPI Gold Master (INTERNO — IP Dylus Lab)
├── Indicadores calculados por fórmula documentada
└── Ti_Inversión: Devengado_G7+8 / Codificado_G7+8

Nivel 2 — Documentos Institucionales de Contexto
├── RDC (Rendición de Cuentas): contexto, no Ti canónico
├── Informes de gestión: contexto, no fuente primaria
└── POA: planificación, no ejecución

Nivel 3 — Proxy Metodológico
├── Transferencia cantonal→parroquial (zona INEC)
├── Proyecciones estadísticas documentadas
└── Siempre calificado como `proxy` + `proxy_de` completo
```

**REGLA CRÍTICA**: RDC (Rendición de Cuentas) de Holding (EMAI/Bomberos/Patronato) es CONTEXTO DOCUMENTAL, NO fuente de Ti canónico. El Ti de estas entidades proviene SIEMPRE del Gold Master (cédulas eSIGEF). Ver: `[feedback_fuente_ti_holding.md]`.

---

## V. ÁRBOL DE DECISIÓN — ¿QUÉ TIPO ES ESTE DATO?

```
¿Se midió directamente en la fuente primaria sin transformación?
    SÍ → naturaleza_valor: observado
    NO → continuar

¿Se calculó con una fórmula matemática explícita de valores observados?
    SÍ → naturaleza_valor: calculado
    NO → continuar

¿Se obtuvo con metodología propietaria documentada (IRS, IFE, ICPI)?
    SÍ → naturaleza_valor: derivado
    NO → continuar

¿Se infirió transfiriendo un valor de otro nivel territorial?
    SÍ → naturaleza_valor: proxy
         → OBLIGATORIO: bloque proxy_de completo
         → estado_dato: pendiente_microdato o pendiente_validacion (NUNCA confirmado)
```

---

## VI. ANTI-PATRONES — Lo que QUIRA Rechaza

| Anti-patrón | Descripción | Corrección |
|---|---|---|
| **Proxy silencioso** | Usar valor cantonal para parroquia sin declararlo | Declarar `naturaleza_valor: proxy` + `proxy_de` completo |
| **Confirmado sin fuente** | `estado_dato: confirmado` sin `fuente_verificacion` | Añadir fuente primaria o degradar a `pendiente_validacion` |
| **proxy + confirmado** | Combinación ontológicamente inválida | Cambiar a `pendiente_microdato` o conseguir fuente primaria |
| **COOTAD = INEC** | Asumir que parroquia urbana COOTAD = zona urbana INEC | Ver QUIRA Territorial Semantics v1.0 |
| **RDC como Ti** | Usar cifras de RDC para calcular Ti de inversión | Ti siempre de cédula eSIGEF vía Gold Master |
| **Valor nulo sin fuente_requerida** | Nodo C9 con valor=null y sin indicar qué falta | Añadir `fuente_requerida` explícita |
| **Alucinación de artículos** | Citar Art. X sin verificación contra texto oficial | `revisado_por_experto: false` + verificación obligatoria |

---

## VII. FLUJO DE VALIDACIÓN CANÓNICO — De Norma a Grafo

```
ACK (Átomo QLEP)
    ↓ define obligación verificable
C8 Indicador (IND_XXX)
    ↓ con fórmula, umbrales, fuente_dato
C9 Resultado Territorial (RES_XXX)
    ↓ con valor + naturaleza_valor + estado_dato + fuente_verificacion
    ↓
¿estado_dato = confirmado?
    SÍ → ingesta Neo4j (relación MIDE activa)
    NO → Neo4j con flag pendiente; no activa inferencias causales
```

---

## VIII. RELACIÓN CON OTROS DOCUMENTOS FUNDACIONALES

| Documento | Relación |
|---|---|
| QTMP schema v1.1 | Implementación técnica de este marco en YAML |
| QLEP SKILL.md | Fuente canónica de ACKs que alimentan la cadena C1→C9 |
| QUIRA Territorial Semantics v1.0 | Define qué significa cada `nivel_territorial` |
| QUIRA Causal Model v1.0 | Define cómo los C9 confirmados activan inferencias causales |
| SIAP-ICPI Gold Master | Fuente primaria de Ti para todo el Holding (INTERNO) |

---

## IX. REGLA DE ORO

> **Un nodo C9 con `naturaleza_valor: proxy` y `proxy_de` vacío no ingresa al grafo Neo4j.**  
> Un nodo C9 con `estado_dato: confirmado` sin cadena de fuente verificable es una mentira institucional.  
> QUIRA produce confianza — no produce cifras convenientes.

---

*QUIRA Data Governance v1.0 — CONGELADO 2026-05-31*  
*Versión siguiente: v1.1 tras primer ciclo Neo4j + consultas causales reales*  
*Custodio: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO*
