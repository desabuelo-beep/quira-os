# ADR-001 — PDOT Montecristi es la fuente canónica territorial

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

QUIRA necesita una fuente única de referencia para metas territoriales, límites parroquiales, vocaciones productivas y compromisos de planificación del GAD de Montecristi. Múltiples documentos hacen referencia al territorio de formas distintas (COOTAD, PDOT, PND, Agenda 2030, SIGEF).

La pregunta era: ¿cuál es la "Constitución Territorial" de Montecristi que establece las metas contra las cuales QUIRA evalúa?

## Decisión

**El PDOT Montecristi 2023-2027 es la fuente canónica territorial del GAD Municipal de Montecristi.**

- Es el instrumento legal de planificación territorial obligatorio (COOTAD Art. 295)
- Establece las metas de desarrollo que el GAD está obligado a cumplir
- Es el único documento que vincula normativa nacional con realidad local parroquial
- Los dominios Dom01-Dom12 de QUIRA se alinean con las propuestas del PDOT

Ruta canónica: `ProyecT\Documentos_Montecristi\PDOT_MONTECRISTI_KB.xlsx` (estructurado)  
Ruta app: `quira-os\data\PDOT_MONTECRISTI_KB.xlsx`

## Consecuencias

- Un semáforo ROJO en QUIRA no es solo "incumplimiento normativo" — es "regresión respecto a meta PDOT oficial"
- Los C9 (Resultados Territoriales) se anclan al PDOT, no solo a la ley
- En Beta: los QTMP tendrán `meta_pdot` como campo obligatorio para cada C9

## Normas aplicables

COOTAD Art. 295-297 (planificación territorial); COPLAFIP Art. 5 (coherencia de planificación)
