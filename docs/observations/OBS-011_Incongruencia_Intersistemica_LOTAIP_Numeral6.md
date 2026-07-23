# OBS-011 — Incongruencia Intersistémica: Numeral 6 LOTAIP (Cédula de Ingresos)

**Estado**: CONFIRMED — evidencia documental de tres fuentes independientes (norma · corpus · correspondencia oficial)
**Fecha**: 2026-07-21
**Origen**: Gestión propia de Javo (Delegación DPE Manabí, jul-2026) + auditoría del corpus normativo (dominio d07)
**Ancla normativa**: `LOTAIP_19_6` (canon QLEP, `data/acks/lotaip_f02.yaml`) — este OBS es evidencia institucional
complementaria, **no forma parte del ACK** (separación canon normativo / evidencia institucional, ver Principio del colega abajo).

---

## Hallazgo central

El GAD Municipal de Montecristi (y, según correspondencia oficial de la DPE, el patrón se
replica a nivel nacional — no verificado empíricamente por QUIRA fuera de Montecristi) publica
en el Portal Nacional de Transparencia únicamente la **cédula presupuestaria de egresos** del
numeral 6, Art. 19 LOTAIP. La cédula de **ingresos y financiamiento** está ausente.

La obligación legal exige ambas. La guía metodológica vigente también. El portal técnico que
las opera no lo permite. Es una ruptura entre eslabones de la misma cadena, no un hecho aislado.

## Cadena de autoridad para d07 (jerárquicamente correcta, ratificada)

```
1. Constitución (CE — derecho de acceso a la información pública)
2. LOTAIP (Ley)
3. Reglamento General LOTAIP
4. Guía Metodológica de Mecanismos — DPE 2024 (GUIA-LOTAIP-MEC, vigente)
5. Guía Cumplimiento Entidades Obligadas — DPE 2018 (GUIA-LOTAIP-ENT, histórica, no vigente)
```

## Evidencia por fuente

### 1 · Norma — obligación jurídica (existe, en la LEY misma)
Texto **literal** de la LOTAIP Art. 19 numeral 6 (verificado en el corpus, sigla LOTAIP, 2026-07-22):
> *"Información total sobre el presupuesto anual que administra la entidad, así como el asignado a
> cada área, programa o función, **especificando ingresos, gastos, financiamiento y resultados
> operativos** de conformidad con los clasificadores presupuestales, así como liquidación del
> presupuesto, especificando destinatarios de la entrega de recursos públicos."*

La obligación de publicar **ingresos** no está solo en la Guía — está en el texto expreso de la Ley.
La Guía y el Instructivo la operativizan; el Portal la incumple. No admite lectura parcial.

### 2 · Guía Metodológica vigente — la reconoce (existe)
Corpus v1.0, sigla `GUIA-LOTAIP-MEC`, chunk `id=14342`, `sha256=9b50ff15923172cb570c115c9544022019adbc81d2d350efad8c746fcdce022e`:
> *"para obtener el porcentaje de ejecución presupuestaria, las entidades tomarán los montos del
> codificado de **ingresos** y para los gastos se tomará la información del devengado, de esta
> manera se brindará información **completa** de la ejecución presupuestaria a la población."*

### 3 · Portal Nacional de Transparencia — evidencia faltante (no permite cumplir)
CSV oficial descargado del portal (`2026-Mayo-Numeral 6-datos6.csv`, Holding GADM Montecristi
completo: GAD + Patronato + EP Aseo + Bomberos): 75 registros, **100%** de cuentas inician con
"5" o "8" (gastos corrientes/capital). **0 registros** con cuentas "1"/"2"/"3" (ingresos
corrientes/capital/financiamiento). El formulario técnico no tiene campos para ingresos.

### 4 · Correspondencia oficial DPE — discrepancia reconocida institucionalmente
- Mónica Prado Calderón (Especialista DD.HH., Delegación Provincial Manabí, DPE), 2026-07-08:
  confirma que el GAD y su holding "están igual, solo suben egresos" y remite el hallazgo a
  Dirección Nacional para explicación.
- Dirección Nacional de Promoción y Monitoreo de la Transparencia Activa (DPE), 2026-07-09,
  respuesta oficial por correo: *"se encuentra actualizando la normativa aplicable y la
  plataforma tecnológica institucional... entre estas se encuentra la relacionada con el
  numeral 6 del artículo 19 de la LOTAIP, específicamente respecto de la publicación de la
  cédula presupuestaria de **ingresos**."*

## Clasificación del caso — lenguaje objetivo (acuerdo Javo/colega/Claude, 2026-07-21)

QUIRA certifica verificabilidad, no culpabilidad (Principio Rector, `CLAUDE.md`). El motor no
concluye automáticamente "incumplimiento" ni "vulneración de derechos" — esas son calificaciones
jurídicas que corresponden al lector experto o al órgano de control. Lo que sí es enteramente
verificable y objetivo:

| Componente | Estado |
|---|---|
| Obligación jurídica (Ley + Reglamento + Guía vigente) | Existe, sin ambigüedad |
| Evidencia publicada | Cédula de egresos, mensual |
| Evidencia faltante | Cédula de ingresos y financiamiento |

**Salida tipo para el motor/UI (nunca lenguaje acusatorio, Regla de Oro 2):**
> *Resultado: existe una brecha documental respecto del estándar previsto en el artículo 19
> numeral 6 de la LOTAIP.*
> *Observación metodológica: la DPE reconoció oficialmente una discrepancia entre el estándar
> legal y la parametrización operativa del Portal Nacional de Transparencia (correspondencia
> oficial, 2026-07-09).*

## El patrón — Erosión de Integridad Intersistémica (propuesta del colega, sin ratificar aún)

```
Ley  →  Reglamento  →  Guía Metodológica 2024  →  Portal Nacional  →  Sujetos Obligados
 ✅        ✅                  ✅ (exige)           ❌ (no permite)        déficit resultante
```

No es un incumplimiento aislado de Montecristi: es una ruptura en la cadena de sistemas que
debía operativizar la ley, con causa documentada aguas arriba del sujeto obligado. El colega
propone nombrar este patrón "Erosión de Integridad Intersistémica" como categoría descriptiva
del caso — **no se ratifica todavía como categoría formal de la Constitución Ontológica**
(`docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md`, Principio Rector: independiente · institucional
· parcial · sin evidencia · contradicción); por ahora este caso se lee como una variante de
**contradicción** (norma+guía vs. implementación técnica). Decisión de fondo pendiente de Javo.

## Impacto en d07 (Transparencia)

- El Gold Master (`H09_S7_TRANSPARENCIA_LOTAIP`) mide *disponibilidad* de información, no
  *completitud metodológica por literal* (nota propia del Excel, celda B9: "Score refleja
  DISPONIBILIDAD de información, no COMPLETITUD metodológica") — coherente con este hallazgo,
  no lo contradice.
- Antes de tipificar esta brecha como "incumplimiento simple" del GAD en cualquier dashboard
  o narrativa de d07, debe citarse esta cadena completa (Capa 7 — Narrativa del Protocolo de
  Curación de Dominio).

---

*OBS-011 · QUIRA Gov · Dylus Lab © 2026*
