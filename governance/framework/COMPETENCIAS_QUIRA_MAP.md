# COMPETENCIAS_QUIRA_MAP — Mapa Constitucional CE Art. 264 → Dominios QUIRA

**Estado:** Congelado — v1.0  
**Fecha:** 2026-06-01  
**Base normativa:** Constitución del Ecuador, Art. 264 — Competencias Exclusivas GAD Municipal  
**Clasif.:** Interno · QUIRA Operaciones

---

## Propósito

Establece la relación canónica entre las 14 competencias constitucionales exclusivas del GAD Municipal (CE Art. 264) y los 12 dominios operativos de QUIRA Gov.

**Dos taxonomías que coexisten sin competir:**

| Taxonomía | Propósito | Lenguaje |
|-----------|-----------|---------|
| 14 Competencias CE 264 | Legitimar — ancla constitucional del sistema | "Competencia Constitucional N.° 4" |
| 12 Dominios QUIRA | Gobernar — organiza la observación operativa | "Dom10 · Territorio & Cobertura" |

No son dos sistemas. Son dos vistas del mismo sistema.  
La competencia dice qué tiene autoridad de hacer el GAD.  
El dominio organiza cómo QUIRA observa si lo hizo y con qué resultado.

**Consecuencia institucional directa:** cuando CGE o CPCCS pregunta "¿cómo monitorean sus competencias?", la respuesta no es "tenemos Dom10" — es "tenemos observabilidad permanente de la Competencia Constitucional N.° 4, con trazabilidad desde la norma hasta el resultado territorial verificado."

---

## Mapa Competencia → Dominio(s) QUIRA

| # | Competencia CE Art. 264 | Dominio(s) QUIRA | Cobertura |
|---|------------------------|-----------------|-----------|
| 1 | Planificar el desarrollo cantonal y formular PDOT, articulado con planificación nacional, regional, provincial y parroquial | Dom01 (principal), Dom03 (seguimiento de metas PDOT) | ✅ |
| 2 | Ejercer el control sobre el uso y la ocupación del suelo del cantón | Dom10 (catastro, ordenamiento territorial), Dom04 (alertas de control) | ✅ |
| 3 | Planificar, construir y mantener la vialidad urbana | — | ⚠️ Sin dominio directo |
| 4 | Prestar los servicios públicos de agua potable, alcantarillado, depuración de aguas residuales, manejo de desechos sólidos, saneamiento ambiental | Dom10 (servicio territorial), Dom05 (EP Agua, EP Aseo — ejecutores), Dom12 (grupos sin acceso) | ✅ |
| 5 | Crear, modificar o suprimir mediante ordenanzas, tasas y contribuciones especiales de mejoras | Dom02 (principal — ingresos propios), Dom01 (ordenanzas como instrumento de planificación) | ✅ |
| 6 | Planificar, regular y controlar el tránsito y el transporte terrestre dentro de su circunscripción cantonal | — | ⚠️ Sin dominio directo |
| 7 | Planificar, construir y mantener la infraestructura física y los equipamientos de salud y educación, y los espacios públicos destinados al desarrollo social, cultural y deportivo | Dom05 (holding — ejecuta infraestructura), Dom12 (protección social — beneficiarios), Dom10 (territorio — dotación física) | ✅ |
| 8 | Preservar, mantener y difundir el patrimonio arquitectónico, cultural y natural del cantón y construir los espacios públicos para estos fines | Dom11 | ⚠️ Dom11 DISABLED — brecha activa |
| 9 | Formar y administrar los catastros inmobiliarios urbanos y rurales | Dom10 (territorio — catastro), Dom02 (ingresos prediales derivados del catastro) | ✅ |
| 10 | Delimitar, regular, autorizar y controlar el uso de las playas de mar, riberas y lechos de ríos, lagos y lagunas | Dom10 (territorio — recursos naturales), Dom04 (alertas de control ambiental) | ✅ |
| 11 | Preservar y garantizar el acceso efectivo de las personas al uso de las playas de mar, riberas de ríos, lagos y lagunas | Dom10 (territorio), Dom12 (grupos prioritarios — acceso equitativo) | ✅ |
| 12 | Regular, autorizar y controlar la explotación de materiales áridos y pétreos en lechos de ríos, lagos, playas y canteras | — | ⚠️ Sin dominio directo |
| 13 | Gestionar los servicios de prevención, protección, socorro y extinción de incendios | Dom05 (holding — Cuerpo de Bomberos), Dom12 (protección social — poblaciones en riesgo) | ✅ |
| 14 | Gestionar la cooperación internacional para el cumplimiento de sus competencias | Dom01 (planificación — cooperación en PDOT), Dom09 (rendición — reportes a cooperantes) | ✅ parcial |

---

## Análisis de Cobertura

### Cobertura operativa: 10/14 competencias con dominio QUIRA directo

### Brechas identificadas

**Sin dominio directo (3/14):**

| Comp. | Descripción | Cobertura interina | Contexto Montecristi | Prioridad post-M002 |
|-------|-------------|-------------------|---------------------|---------------------|
| 3 | Vialidad urbana | Dom04 (alertas) + Dom10 (infraestructura como proxy) | Competencia parcialmente delegada a MTOP en tramos intercantonales; GAD retiene vialidad local | Media |
| 6 | Tránsito y transporte | Dom04 (alertas de control) | Operación delegada a ANT; GAD retiene regulación y control local | Media |
| 12 | Áridos y pétreos | Dom02 (ingresos por concesión) + Dom04 (control) | Competencia técnica específica; no hay EP dedicada | Baja |

**Nota sobre Comp. 3 y 6:** en Montecristi la competencia es real pero la operación plena está coordinada con el nivel central. La brecha de observabilidad existe pero su urgencia es menor que las competencias de servicio directo a la población (Comp. 4, 7, 13).

**Brecha activa — módulo deshabilitado (1/14):**

| Comp. | Descripción | Estado |
|-------|-------------|--------|
| 8 | Patrimonio arquitectónico, cultural y natural | Dom11 DISABLED — corpus F0.7-F0.8 vacío — habilitación post-MILESTONE_002 |

---

## Dominios Transversales

Cuatro dominios QUIRA no derivan de una competencia específica de CE Art. 264. Derivan de obligaciones constitucionales transversales que aplican sobre el ejercicio de **todas** las competencias simultáneamente:

| Dom | Nombre | Base normativa | Función en el sistema |
|-----|--------|---------------|----------------------|
| Dom06 | Salud Institucional | CE 226 + COOTAD 228 | Mide el estado agregado de cumplimiento — es el indicador sintético del sistema completo |
| Dom07 | Transparencia | CE 18 + LOTAIP | Observa si el ejercicio de las competencias es público y verificable por terceros |
| Dom08 | Participación Ciudadana | CE 95 + COOTAD 304 | Verifica si la ciudadanía incide realmente en las decisiones competenciales |
| Dom09 | Rendición de Cuentas | CE 209 + COOTAD 302 | Cierra el ciclo: ¿puede el GAD demostrar el ejercicio de sus competencias con trazabilidad? |

Estos dominios son **habilitantes sistémicos**: sin ellos, los otros 8 dominios son opacos a su propio funcionamiento. Dom07 en particular es condición de existencia de Dom08 y Dom09 — sin información pública, no hay participación real ni rendición verificable.

---

## Lectura inversa — Dominio → Competencia(s)

| Dom | Nombre QUIRA | Competencias CE 264 que observa |
|-----|-------------|--------------------------------|
| Dom01 | Planificación Estratégica | Comp. 1, Comp. 14 |
| Dom02 | Presupuesto & Financiamiento | Comp. 5, Comp. 9 |
| Dom03 | Seguimiento de Metas | Comp. 1 (derivado) |
| Dom04 | Alertas Institucionales | Comp. 2, Comp. 6, Comp. 10, Comp. 12 (control) |
| Dom05 | Holding Municipal | Comp. 4, Comp. 7, Comp. 13 |
| Dom06 | Salud Institucional | Transversal — todas las competencias |
| Dom07 | Transparencia | Transversal — todas las competencias |
| Dom08 | Participación Ciudadana | Transversal — todas las competencias |
| Dom09 | Rendición de Cuentas | Transversal — todas las competencias |
| Dom10 | Territorio & Cobertura | Comp. 2, Comp. 4, Comp. 9, Comp. 10, Comp. 11 |
| Dom11 | Ecosistema Productivo | Comp. 8 (DISABLED) |
| Dom12 | Protección Social | Comp. 4, Comp. 7, Comp. 11, Comp. 13 |

---

## Visión GeoTwin — Modo Competencias Constitucionales

**Registro de semilla arquitectónica — implementación post-MILESTONE_002.**

Después de completar el Gemelo Institucional de Montecristi, GeoTwin puede ofrecer dos modos de entrada al territorio:

**Vista A — Por Dominio QUIRA** (actual)  
Entrada por Dom01...Dom12. Lenguaje de gobernanza operativa.  
Audiencia: Director QUIRA, equipo técnico del GAD.

**Vista B — Por Competencia Constitucional** (futura)  
Entrada por Competencia 1...14. Lenguaje constitucional de la CE.  
Audiencia: Alcalde, CGE, CPCCS, ciudadanía, organismos de cooperación.

**Ejemplo de Vista B — Competencia 4:**
> ¿Cómo está Montecristi en la Competencia Constitucional N.° 4?

GeoTwin agrega en una sola vista:
- Dom10: cobertura de agua potable por zona (34.9% — ROJO)
- Dom05: estado de EP Agua (ejecutor del servicio)
- Dom12: grupos prioritarios en zonas sin cobertura
- Dom04: alertas activas de incumplimiento en saneamiento
- Inversión ejecutada vs. asignada vinculada a esta competencia

**Consecuencia política:** el alcalde responde al ciudadano y a los órganos de control en el lenguaje que la Constitución usa — no en el lenguaje interno de QUIRA. La legitimidad institucional del sistema aumenta sin exponer la metodología interna.

**Valor de escala:** la Vista B también habilita comparación entre cantones — "¿cómo están todos los GAD Municipales en Competencia 4?" — usando el lenguaje constitucional común sin revelar metodología. Este documento es la base de datos de esa comparación.

**Habilitador técnico:** el mapa Competencia → Dominio → QTMP → C9 de este documento es la lógica de agregación que alimenta la Vista B. La semilla está plantada.

---

## Relación con otros documentos de gobernanza

| Documento | Relación |
|-----------|----------|
| `QLEP_CANONICO_MONTECRISTI_v1.0.md` | Fuente de N1 (norma base) y N2 (pregunta bautismal) por dominio |
| `ADR-013_Mapeo_QTMP_Dominios.md` | Mapeo QTMP circuit → dominio (nivel operativo) |
| `ADR-014_BETA_CORE_Roadmap.md` | Secuencia de activación de dominios — determina cuándo cada competencia tiene observabilidad completa |
| `QNKC_P01_Dominios_Observacionales.md` | Principio de diseño para Dom07, Dom08, Dom09 — los tres dominios transversales observacionales |

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"La Constitución es el mapa. QUIRA es el instrumento que lee ese mapa en el territorio."*
