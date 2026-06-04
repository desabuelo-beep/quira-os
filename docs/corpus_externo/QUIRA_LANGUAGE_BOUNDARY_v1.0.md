# QUIRA — Frontera de Lenguaje: Interno vs. Público
## Versión 1.0

**Estado**: CONGELADO  
**Fecha**: 2026-05-31  
**Custodio**: QUIRA Operaciones · Dylus Lab  
**Propósito**: Canonizar qué vocabulario puede aparecer en cada capa del sistema.  
**Precedencia**: Este documento aplica a todo código, UI, API, reporte, demo y comunicación externa.

> El mundo ve el espejo.
> La metodología, la matemática y la arquitectura son del laboratorio.
> Esta frontera no se negocia.

---

## I. LA REGLA FUNDAMENTAL

```
CAPA INTERNA          CAPA PÚBLICA
(Dylus Lab · Operaciones)    (UI · API · Demo · Reportes externos)

Puede usar:           SOLO puede usar:
  Nomenclatura canónica   Lenguaje de gobernanza territorial
  IDs de nodos (QTMP)     Nombres de dominios (Dom01-Dom12)
  Nombres de hojas Excel  Indicadores en lenguaje ciudadano
  Fórmulas ICPI           Valores + semáforo + fuente pública
  Schema QTMP             Narrativa causal en español común
  Gold Master             —
  H01, H12, H41, etc.     —
  ICPI, IFE, IED, IOC...  —
  Ti, Vi, Pi, Ri, Ei...   —
  QNKC-002, ACK, etc.     —
```

**Si una palabra o sigla no puede explicarse a un ciudadano en 10 segundos sin mencionar la metodología → es interna.**

---

## II. LO QUE NUNCA APARECE EN LA UI / API / REPORTES EXTERNOS

| Prohibido en capa pública | Razón |
|---|---|
| Nombre del Gold Master | Secreto de empresa |
| Nombres de hojas (H01, H12, H41, etc.) | Nomenclatura interna |
| Siglas de índices (ICPI, IFE, IED, ITAM, IGP, IPE, PSG, ISP, IOC, IET) | Nomenclatura metodológica |
| Variables de fórmula (Vi, Pi, Ei, Ti, Ri) | Matemática interna |
| IDs de nodos QTMP (SP_G10P_MCR, RES_G10P_01_MCR, etc.) | Schema interno |
| Nombres de relaciones Cypher (MATERIALIZA_VIA, HABILITA, EXPLICA) | Arquitectura interna |
| QTMP, ACK, QLEP, QNKC-002 | Nombres de protocolos internos |
| "Gold Master" | Secreto de empresa |
| Nombres de circuitos internos (GAP_10PCT, etc.) | Nomenclatura interna |

---

## III. LOS 12 CAJONES — La capa pública canónica del frontend

Los 12 cajones (dominios) son el vocabulario oficial del frontend de QUIRA Gov.
Dentro de cada cajón pueden aparecer indicadores con:
- Valor numérico o porcentual
- Semáforo (verde / amarillo / rojo)
- Fuente pública (nombre del documento oficial, no de la hoja Excel)
- Narrativa en lenguaje de gobernanza

**Lo que NO aparece en los cajones:**
- El nombre interno del índice que calcula ese valor
- La fórmula que lo produce
- El ID del nodo Neo4j correspondiente
- El nombre de la hoja del Gold Master

**Ejemplo correcto en UI:**
> "Ejecución presupuestaria del Patronato Municipal: 50% — ROJO — persistente 3 años"  
> Fuente: Sistema Integrado de Gestión Financiera — noviembre 2025

**Ejemplo incorrecto en UI:**
> "Ti_Patronato_2025 = 50% (H07b_Ti_INVERSIÓN fila 18)"

---

## IV. QUIRA IMPACT — FRONTERA DE LENGUAJE EN COMUNICACIONES MULTILATERALES

**Producto**: QUIRA Impact  
**Verbo**: TRAZAR  
**Audiencia**: CAF, BID, BM, PNUD, UE, GIZ, JICA — organismos de cooperación internacional  
**Fuente canónica del producto**: QUIRA_ECOSYSTEM_2026_2030.md

La misma regla fundamental (Sección I) aplica a los cinco productos sin excepción.

En comunicaciones de QUIRA Impact hacia organismos multilaterales, aparece:
- Cadenas causales en lenguaje de gobernanza territorial (no nomenclatura interna)
- Indicadores con valor + fuente pública + semáforo de avance
- Trazabilidad de fondos cooperación → resultado territorial (marcos ODS/SDG)
- Métricas de impacto en lenguaje institucional — nunca fórmulas de cálculo

No aparece (aplica la misma prohibición de Sección I):
- Gold Master, schema QTMP, IDs de nodos, fórmulas de cálculo interno
- Nomenclatura interna (ICPI, IOC, H-series, Vi/Pi/Ti/Ri)
- Arquitectura interna del grafo, relaciones Cypher, nombres de circuitos

---

## V. VOCABULARIO APROBADO POR CAPA

### Capa interna (Dylus Lab · QUIRA Operaciones)
Puede usar toda la nomenclatura canónica sin restricción.
Esto incluye ADRs, governance docs, QUIRA_STATE, QTMP schemas, Gold Master, scripts.

### Capa de presentación interna (Panel Estratégico — usuarios autenticados GAD)
Usa lenguaje de gestión pública institucional:
- "Ejecución presupuestaria"
- "Cobertura de servicio"
- "Brecha territorial"
- "Cumplimiento normativo"
- "Grupos de atención prioritaria"
- Dominios: Dom01-Dom12 pueden usarse como etiquetas internas de navegación
- Semáforo: VERDE / AMARILLO / ROJO (no los valores de fórmula)

### Capa pública (QUIRA Ciudadana — ciudadanos, prensa, candidatos)
Lenguaje ciudadano estricto:
- "El Patronato ejecutó el 50% de su presupuesto — tres años en rojo"
- "El 34.9% de los hogares tiene acceso a agua potable"
- "La brecha entre zonas urbanas y rurales es de 32 puntos porcentuales"
- Nunca: fórmulas, IDs, siglas metodológicas, nombres de hojas

---

## VI. CÓMO VERIFICAR ANTES DE PUBLICAR

Antes de escribir cualquier string que aparezca en UI, API response, reporte externo o demo:

1. ¿Contiene un nombre de hoja (H00-H73)? → **ELIMINAR**
2. ¿Contiene una sigla de índice que no sea autoexplicativa (ICPI, IOC, IGP...)? → **ELIMINAR**
3. ¿Contiene un ID de nodo QTMP? → **ELIMINAR**
4. ¿Contiene la palabra "Gold Master"? → **ELIMINAR**
5. ¿Contiene una variable de fórmula (Vi, Pi, Ti...)? → **ELIMINAR**
6. ¿Puede entenderse sin conocer la metodología? → **APROBADO**

---

## Ver también

QUIRA_EPISTEMIC_FRAMEWORK_v1.0 (Sección IV — Bloomberg model),  
QUIRA_PRODUCT_ARCHITECTURE_v1.0, ADR-011, QUIRA_DATA_GOVERNANCE_v1.0

---

*QUIRA_LANGUAGE_BOUNDARY v1.0 — Registrado 2026-05-31*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
