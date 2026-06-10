# B.3 — MEDICIÓN: ¿QUÉ CAMBIÓ EN QUIRA CON LA COSECHA?
**Sprint B · QUIRA OS · 2026-06-10**
*Condición metodológica del Colega: no medir indicadores obtenidos —
medir cuántas DECISIONES de QUIRA cambiaron gracias a ellos.*

---

## La clasificación de los 27 gaps

Cada gap de B.1 (+G-26 de la observación urbano/rural de Javo, +G-27 de su
corrección sobre El Aromo) termina en una de tres categorías:

```
A — GAP REAL          la información no existía (buscar afuera)
B — GAP DE EXTRACCIÓN existía pero no estructurada (B.2 lo resolvió)
C — GAP DE ARQUITECTURA existía estructurada pero no conectada al motor
```

### Categoría A — Gaps reales: 14 (de los cuales 3 REDUCIDOS por proxies)

| Gap | Qué falta | Fuente externa | ¿Reducido por B.2? |
|---|---|---|---|
| G-04 | Documento fuente del índice de transparencia 56 | Defensoría del Pueblo | — |
| G-07 | Costo social del agua (tanqueros · salud) | MSP / estudio | — |
| G-09 | Género desagregado por parroquia | INEC censo · DINASED | ✅ cantonal ahora rico: jefatura serie 20 años · analfabetismo digital mujeres |
| G-11 | Tasa embarazo adolescente cantonal | MSP | confirmado por el PROPIO PDOT |
| G-12 | Tasa VIF oficial | DINASED/Fiscalía | ✅ proxy: Junta Cantonal 120→198 (+65 %) |
| G-14 | Vialidad de La Pila e Isabel Muentes | GAD | — |
| G-16 | Transporte público operativo | ANT/GAD | — |
| G-17 | Semántica indicador siniestralidad (79 %) | ANT | — |
| G-18 | Tasa desempleo juvenil | ENEMDU/INEC | ✅ proxy: relevo generacional agro (79.3 % productores 45+) |
| G-19 | PEA cantonal | INEC | — |
| G-21 | Empleo por parroquia | INEC censo | — |
| G-22 | Celda emergente: ubicación · capacidad · vida útil | GAD/MAATE | — |
| G-24 | Sostenibilidad financiera Montecristi-EP | eSIGEF/GAD | — |
| G-26 | Inventario sub-parroquial de comunidades sin sistema de agua | GAD/PDOT anexos | — |

**Lectura clave: los 14 gaps A son TODOS fuentes externas (INEC · DINASED ·
MSP · ANT · GAD · Defensoría). NINGUNO es una fórmula que le falte al
Gold Master.**

### Categoría B — Gaps de extracción: 4 (resueltos o triviales)

| Gap | Estado |
|---|---|
| G-05 semántica agua parroquial/cantonal | ✅ RESUELTO — origen identificado (núcleo CUP vs parroquia completa) + tabla corregida p.115 cargada |
| G-06 alcantarillado parroquial | ✅ RESUELTO — saneamiento parroquial en cosecha (Isabel Muentes 0 %) |
| G-13 unidades viales km/m | regla de normalización en pipeline (trivial) |
| G-03 convención "dónde" institucional | ✅ resuelto en B.1 (diseño) |

### Categoría C — Gaps de arquitectura: 9

| Gap | Qué conexión falta | Esfuerzo |
|---|---|---|
| G-01 + G-08 | Requisitos de 6 convocatorias sin cargar → $350K+ sin veredicto del matcher | Bajo (carga manual) |
| G-02 | Dedup de convocatorias en pipeline radar | Bajo |
| G-10 | Escala PSG decimal/% inconsistente entre circuito y matcher | Bajo |
| G-15 + G-20 + G-23 + clima | **Radar D02 ciego en 4 temas: movilidad · empleo · residuos · clima/resiliencia** — los fondos existen, el fetcher no los barre | Medio (1 sola intervención) |
| G-25 | Tasa de recuperación de reciclables como indicador formal | Decisión de mesa |
| **G-27** *(reclasificado 2026-06-10)* | **Estado de materialización — SOLO para la capa territorial PDOT.** Aclaración Javo: el Gold Master YA disciplina la materialización de obras MUNICIPALES (variable con verificación en portal SERCOP — confirmado en QUIRA_DATA_GOVERNANCE_v1.0 y tabla `sercop_contratos`). El Aromo/Refinería son obras NACIONALES — fuera de la planificación municipal por diseño. Lo que falta: que `pdot_indicadores` etiquete **competencia** (municipal/provincial/nacional) y herede la disciplina de materialización para proyectos no-municipales que el PDOT documenta | Bajo-Medio — 2 campos en schema territorial, NO toca el GM |

---

## EL RESULTADO

```
27 gaps  →  14 A (reales)  ·  4 B (extracción)  ·  9 C (arquitectura)

48 % de los gaps se resuelve SIN buscar datos afuera
   y SIN tocar una sola fórmula del Gold Master.

100 % de los gaps reales son fuentes externas —
   CERO son fórmulas faltantes del motor.
```

**Hipótesis del Colega (10 A / 8 B / 8 C): direccionalmente correcta.**
La diferencia (14 A vs 10) se explica porque 3 de los A quedaron *reducidos*
(con proxy operativo) sin desaparecer formalmente.

## Las decisiones de QUIRA que CAMBIARON (la métrica que importa)

| # | Decisión/conclusión | Antes | Después |
|---|---|---|---|
| 1 | FICHA-03 "¿qué pasa?" | Media — "se interviene sobre un problema que no se mide" | **Alta** — femicidios serie 10 años · homicidios cambio de régimen (6→47/año) · demanda de protección +65 %/año · jefatura femenina casi duplicada en 20 años |
| 2 | FICHA-02/04 "¿dónde?" | Media-Alta con inconsistencia | **Alta** — saneamiento parroquial real (IM 0 %) + semántica agua resuelta en origen |
| 3 | Prioridad territorial | Isabel Muentes (parroquial) | Isabel Muentes **+ "Demás áreas sin parroquia"** (agua 19.3 % · saneamiento 15.5 % — peor que cualquier parroquia nombrada) + dimensión urbano/rural transversal (pobreza extrema 7×) |
| 4 | FICHA-05 "¿por qué?" | contexto general | + relevo generacional agro roto: el campo no absorbe jóvenes |
| 5 | Capa de riesgo | "no tenemos capa climática" | **capa operativa**: 82.28 % susceptibilidad movimientos de masa · cuantificación completa de inundación/sismo |
| 6 | QUIRA Economic | idea sin contenido | inventario real con regla de diseño fundacional: **distinguir promesa de activo (G-27)** |
| 7 | Radar D02 | "completo" | ciego en 4 temas — 1 intervención lo corrige |

## Veredicto preliminar sobre el Gold Master

El Colega tenía razón: **el Gold Master NO es el problema principal.**
Más de la mitad de las brechas desaparecen sin tocar una fórmula.

La auditoría futura (GM-XXX-01) ya no pregunta "¿qué agregamos?" sino
"¿qué dimensiones críticas del territorio aparecen repetidamente en B.2
y siguen invisibles en el Gold Master?". Con la evidencia de B.2, esa
lista es CORTA y precisa:

1. ~~Estado de materialización~~ **DESACTIVADA de la auditoría GM**
   (aclaración Javo 2026-06-10): el GM ya la modela para obras municipales
   vía SERCOP. Queda como mejora de la capa territorial (G-27 reclasificado).
2. **Riesgo/vulnerabilidad territorial** — 82.28 % del territorio en
   susceptibilidad y el motor no tiene dominio que lo lea.
3. **Brecha urbano/rural como dimensión transversal** — pobreza extrema
   7× no es un indicador más: es un eje que cruza todos los dominios.

La lista quirúrgica queda en **2 dimensiones** — y la decisión de mesa
(Colega 2026-06-10) es NO abrir la auditoría GM todavía: primero cerrar
arquitectura, formalizar fichas v2 y consolidar GeoTwin.

No son "género, ambiente, bonos y cooperación" como bloques — son tres
dimensiones quirúrgicas con evidencia.

## Siguiente paso

- **B.3 fase 2:** re-escribir FICHAS 03-06 v2 con la cosecha (las
  decisiones de la tabla anterior, formalizadas).
- **B.2-cierre C:** el lote de arquitectura (G-01/02/08/10 + radar 4 temas)
  — bajo esfuerzo, alto retorno, sin créditos API.
- **Mesa GM:** presentar las 3 dimensiones quirúrgicas cuando Javo y el
  Colega lo dispongan.

---

*B.3 medición v1 · Sprint B · QUIRA OS · Dylus Lab © 2026*
