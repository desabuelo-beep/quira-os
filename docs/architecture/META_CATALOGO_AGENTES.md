# Meta-Catálogo de Agentes — Organigrama Cognitivo de QUIRA IA

> **Estado:** vivo · 2026-07-22 (colega, Punto 7) · se amplía con cada DOM migrado
>
> ⚠️ **ESTE MAPA DEBE ACTUALIZARSE AL CERRAR CADA CAPACIDAD, no sólo al abrirla** (2026-08-18).
> El registro daba `NLP Video RDC Agent` por pendiente cuando llevaba tiempo ejecutado y d09
> cerrado con ese insumo; el director lo leyó como estado real y emitió un juicio equivocado
> sobre lo que QUIRA podía sostener públicamente. **Un mapa que miente sobre lo que existe es
> peor que no tenerlo:** induce a subestimar el sistema y a rehacer lo hecho.
> **Qué es:** el mapa de quién hace qué en QUIRA IA. Distingue lo **agéntico** (juicio, LLM,
> cuesta API) de lo **determinístico** (aritmética fija, gratis). Regla rectora de la sesión:
> *cada DOM es mayoritariamente IA en extracción/interpretación; solo el cálculo final es
> determinístico.*

## Distinción fundamental

| Tipo | Qué es | Cuándo corre | Costo |
|---|---|---|---|
| **IA** | navega, extrae, interpreta, cruza, redacta — requiere juicio | Fase 4/5 | Haiku/Sonnet |
| **Determinístico** | aritmética/lectura fija sobre datos ya limpios | siempre | gratis |

## Catálogo

| Agente / Módulo | DOM | Entrada | Salida | Tipo | Estado | Reutilizable | Dependencias (lo usan) |
|---|---|---|---|---|---|---|---|
| **Portal Navigator** | d07 | Portal DPE (URL por CD) | página/archivo localizado | ~~IA~~ → **Determinístico** | ✅ `evidencia.levantar_evidencia_local` — **la DPE es API, no portal que navegar** (OBS-QNKC-02) | ✅ genérico; la vía IA sobrevive en `levantar_evidencia_portal` para GAD que publiquen fuera de la DPE | d07 hoy; candidato d01/d02 web-GAD |
| **Evidence Collector** | d07 | índice de la API DPE | archivo descargado + SHA256 | ~~IA~~ → **Determinístico** | ✅ `scripts/normativa/descargar_lotaip.py` — 936/936, reanudable, anti-colisión | ✅ genérico | d07 |
| **Evidence Interpreter** | d07 | archivo | ¿legible? ¿campos? ¿ausencia declarada? ¿enlace vivo? | ~~IA~~ → **Determinístico** | ✅ `analizar_contenido_lotaip.py` + `verificar_enlaces_lotaip.py` | ✅ genérico | d07 |
| **Verificador Documental** | d07 | enlace del conjunto de datos | clase de acto · correlativo · metadato vs documento | **Determinístico** | ✅ `documentos.py` (2026-08-18) — abre el PDF; la norma pide el **acta** y se publica el certificado de resoluciones (0 actas en 51) | ✅ genérico (cualquier universo documental normado) | d07; candidato d08/d09 (actas) |
| **Verificador de Cobertura Material** | d07 | `componentes` del catálogo + evidencia | dimensión cubierta / no hallada / no determinable | **Determinístico** | ✅ `componentes.py` (2026-08-18) — CD-06 exige `Ingresos` desde julio y **0 filas en 8 períodos** | ✅ genérico (usa los `componentes` de cualquier catálogo) | d07; candidato d01/d02 |
| **Orquestador d07** | d07 | ejercicio + meses | corrida con `run_id`, gates y hallazgos | **Determinístico** | ✅ `orquestador.py` (2026-08-18) — gates CANON/CATALOGO/EVIDENCIA/INTEGRIDAD **detienen** la corrida | ✅ patrón replicable a todo DOM | d07; plantilla para d01/d02/d03/d08/d09 |
| **Compliance Evaluator** | d07 | evidencia juzgada | CTA/ETA/RP/CI (0-1) | **Determinístico** | ✅ `scoring.py` | parcial (reglas SITA son de d07) | d07 |
| **SITA Engine** | d07 | CTA/ETA/RP/CI | SITA = promedio/4 | **Determinístico** | ✅ `scoring.py` | ❌ específico LOTAIP | d07 |
| **Report Generator** | d07 | score + evidencia | narrativa (Regla Oro 2) | IA | ⬜ Fase 5 | ✅ genérico (cambia solo el prompt) | d07, candidato todos |
| **PDOT Agent** | d01 | web GAD | JSON PDOT (metas) | IA | ⬜ Fase 4 | ✅ genérico (Portal Navigator especializado) | d01 |
| **POA Agent** | d01 | web GAD | JSON POA (programación) | IA | ⬜ Fase 4 | ✅ genérico | d01 |
| **PAC Agent** | d01 | SERCOP / web GAD | JSON PAC | IA | ⬜ Fase 4 | ✅ genérico | d01 |
| **SERCOP Agent** | d01 | portal compras públicas | contratación real ejecutada | IA | ⬜ Fase 4 | ✅ genérico | d01, candidato d02 (compras) |
| **Budget Agent** | d01 | portal transparencia (=CD-06 d07) | cédula presupuestaria | IA | ⬜ Fase 4 · **reuso d07** | ✅ **YA compartido** | **d01 + d02 + d07 + d09** |
| **Alignment Agent** | d01 | PDOT+POA+PAC+SERCOP | hallazgos RO-I-001/002 | IA | ⬜ Fase 4 (`articulacion.py`) | ❌ específico (reglas RO de cada CNO) | d01 |
| **Motor IPE (lectura)** | d01 | Gold Master H16b | IPE, cobertura | **Determinístico** | ✅ `motor.py` (LEE, no calcula) | ❌ específico (celda propia) | d01 |
| **ICPI Engine** | Core | índices | ICPI (H12!B33) | **Determinístico** | ✅ Gold Master (INMUTABLE) | — (único, no se replica) | todos los DOM lo consumen |
| **Motor Capacidades (lectura)** | d02 | Gold Master (H19/H07/H20c/H11) | ISP·Ti·fondos·PND | **Determinístico** | ✅ `motor.py` envuelve `enrich_presupuesto.py` ya en producción | ❌ específico (4 celdas propias) | d02 |
| **Resultado Agent** | d02 | web GAD / transparencia | ¿existe medición de impacto? | IA | ⬜ Fase 4 (`fuentes.py`) | ✅ genérico (Portal Navigator) | d02, único hueco agéntico real del dominio |
| **eSIGEF (Fuente)** | d02 | Gold Master H07 | cédula ejecución | — | ✅ reuso confirmado | ✅ **YA compartido** | **d02 = d01 Presupuesto = d07 CD-06** (misma cédula) |
| **Motor Mandato (lectura)** | d03 | Gold Master H03/H16 | incorporación%, calidad_IFE%, centinela | **Determinístico** | ✅ `motor.py` envuelve `enrich_mandato.py` ya en producción | ❌ específico (2 métricas propias) | d03 |
| **Contraste Documental Agent** | d03 | Plan CNE original + SCHEMA_CNE | promesa verificada / autoridad actualizada | IA | ⬜ Fase 4 (`fuentes.py`) | ✅ genérico (Portal Navigator) | d03, único hueco agéntico real del dominio |
| **Motor RDC (lectura mixta)** | d09 | Gold Master H34b/H31 (vivo) + snapshot persistido (DOCX+embeddings) | fidelidad narrativa, cpccs, serie, cumplimiento, aportes | **Determinístico** | ✅ `motor.py` envuelve `enrich_rdc.py` + lee `enrich_rdc_docx.py`/`enrich_aportes.py` persistidos | ❌ específico (única fuente triple del catálogo) | d09 |
| **Trazabilidad de Aportes Agent** | d09 | H10c aportes + POA (embeddings locales) | aporte↔obra ejecutada, nivel de atención | IA/ML (semiautomático) | ✅ `enrich_aportes.py` ya en producción (metodología v0.3 pendiente aval formal) | ❌ específico (cruce semántico propio) | d09 |
| **Contenido Mínimo Agent** | d09 | informe RDC + Reglamento Art.10 | ¿cumple contenido mínimo? | IA | ⬜ Fase 4 (`fuentes.py`) | ✅ genérico (Evidence Interpreter) | d09 |
| **NLP Video RDC Agent** | d09 | video oficial rendición | discurso→afirmaciones (fidelidad narrativa) | IA | ✅ **EJECUTADO** — el discurso del video de RDC fue extraído y procesado; d09 cerró con ese insumo (Javo · 2026-08-18, corrigiendo este registro) | ❌ específico (NLP de video) | d09 |
| **Motor Integridad (lectura+evaluación)** | d08 | catálogo d08 (evidencia clasificada, 7 instancias) | verificabilidad documental por instancia | **Determinístico** | ✅ `motor.py::evaluar_integridad` | ❌ específico (criterios propios RO-VIII-001) | d08 |
| **Motor IGP (lectura diagnóstica)** | d08 | Gold Master H20b | IGP + 3 componentes + hallazgos OBS-015 | **Determinístico** | ✅ `motor.py::leer_igp_diagnostico` — NO canónico aún (modelo de cálculo a reconstruir fase 2) | ❌ específico | d08 |
| **Extracción de Actas de Participación Agent** | d08 | actas PP/audiencias/cabildos (docx/pdf) | aportes ciudadanos↔ejecución (RO-VIII-003) | IA | ⬜ Fase 4 (`fuentes.py`) — motor propio, NO reusa `enrich_aportes.py` (ese es d09/RDC, OBS-016 frontera) | ❌ específico | d08 |
| **Extractor de Demandas** | d08 | actas PP/audiencias/cabildo (docx·pdf·txt) | catálogo de 223 demandas con trazabilidad al documento | **Determinístico** | ✅ `scripts/d08/extraer_demandas.py` (Fase 1) | ✅ genérico (cualquier acta de participación) | d08 |
| **Trazabilidad Biográfica** | d08 | demandas + POA (XLSX oficial) | correspondencias con ESTADO EPISTÉMICO (Horizonte de Verdad) | IA/ML local (sin API) | ✅ `scripts/d08/cruzar_demandas.py` (Fase 2) | ✅ genérico (demanda→ejecución en cualquier DOM) | d08, candidato d01/d02 |
| **OCR Certificado Agent** | d08 → **compartido d07** | PDF escaneado oficial (16 audiencias d08; **10 artefactos únicos d07**) | texto probatorio | **Determinístico local** (Tesseract, sin API) | ⬜ ningún motor instalado — **no bloquea d07**: el universo real son 10 escaneos únicos, no 123 (2026-08-18: se contaban apariciones, no artefactos) | ✅ genérico (cualquier PDF escaneado oficial) | **d08 + d07**; candidato todos |
| **Cadena de Adquisición d07** | d07 | orden de medir | evidencia recolectada, con sello de insumos | **Determinístico** | ✅ `etapas.py` (2026-08-19) — el orquestador la invoca; **nadie abre una terminal**. Invalida por SHA, no por fecha: rehacer sin cambios no propaga trabajo | ✅ patrón replicable a todo DOM con fuente externa | d07; plantilla para d01/d02/d08 |
| **Puerta Normativa d07** | d07 | id de Regla Operativa | parámetros (cadencia, plazo, fórmulas de ausencia) | **Determinístico** | ✅ `reglas.py` (2026-08-18) — única vía por la que el DOM conoce la norma; si falta la RO **lanza error, no usa un default** | ✅ genérico (todo DOM consume RO, no Derecho) | d07; obligatorio en todo DOM nuevo |

## Grado de apropiación (ADR-051 §2d) — cómo leer la columna «Estado»

Una capacidad puede estar en tres grados, y **el sistema los deriva; nadie los declara**
(`app/agents/apropiacion.py` — **transversal**, no de d07):

| Grado | Qué acredita | Cómo se demuestra |
|---|---|---|
| **capacidad** | el programa existe | está declarado y disponible |
| **ejecución** | QUIRA lo invoca y corre | hay sello de una corrida hecha **por el agente** |
| **validado** | es reproducible | se borra el resultado y el agente lo rehace **idéntico** |

Estado de d07 al 2026-08-19: **1 validada** (`contenido`) · **2 en ejecución** (`contenedores`, `documentos`) · 4 en `capacidad`. La
prueba de origen —`fuente → captura → descarga → SHA`— está **escrita y desactivada**: se activa
con `QUIRA_PRUEBA_DE_ORIGEN=1`, porque golpear el portal del GAD en cada corrida de pruebas sería
usar al sujeto observado como banco de ensayo.

⚠️ **Este catálogo no acredita nada por sí solo.** Que una fila diga ✅ significa que la pieza
existe, no que se haya demostrado reproducible. La acreditación vive en el código y en la suite.

## Sujeto observado — el instrumento lo recibe, no lo contiene (OBS-032)

| Agente / Módulo | DOM | Entrada | Salida | Tipo | Estado |
|---|---|---|---|---|---|
| **Perfil de Sujeto Observado** | transversal | código territorial | identidad en fuentes (DPE id · dominios · nombre) | **Determinístico** | ✅ `app/agents/sujeto.py` + `data/sujetos/` (2026-08-19) — 6 de 11 puntos de acoplamiento retirados; prueba impide que suban |
| **Escalera de Apropiación** | transversal | hechos del dominio | grado capacidad·ejecución·validación | **Determinístico** | ✅ `app/agents/apropiacion.py` — el grado se **deriva**, nunca se declara |

Sujetos declarados hoy: **1** (`130801` Montecristi). Esa cifra es el alcance real del sistema,
no una aspiración del roadmap: los 222 se declaran ahí, uno por archivo, sin tocar código.

## Lecturas del catálogo (lo que revela)

- **Solo 8 piezas son determinísticas** (Compliance Evaluator, SITA Engine, Motor IPE-lectura, Motor
  Mandato-lectura, Motor RDC-lectura, Motor Integridad-d08, Motor IGP-lectura, ICPI Engine). Todo lo
  demás — la mayoría — es IA. Confirma la doctrina: QUIRA IA es un ecosistema de agentes, no un
  motor de scripts con un extractor aislado.
- **Los índices/SAT se LEEN, nunca se recalculan, y su modelo de cálculo se reconstruye desde el
  dominio cuando está mal compuesto** (OBS-015/016, d08): el IGP mezclaba d09 y tenía PP=0 pese a
  evidencia; las "SAT por mecanismo" no existían así en el Gold Master (las SAT reales son
  SAT-0..VIII por dimensión TGI, no 1:1 con cada CNO). Verificar contra el motor real
  (`SAT_Catalogo`), no contra una nomenclatura propia — mismo rigor que el SHA256 normativo.
- **El ICPI Engine es el único intocable** (Regla 1). Todos los demás determinísticos LEEN o
  agregan; ninguno redefine el motor canónico.
- **Budget Agent se comparte** (d01 lo consume, d07 lo produce) — es la memoria operacional de
  Neo4j en acción: la cédula se extrae una vez (`MISMA_FUENTE_QUE`), no dos.
- **Patrón replicable**: cuando se migren d02/d03/d09, cada uno añade sus agentes de extracción
  (IA) + su lectura de motor (determinística) — misma forma, distinta sustancia.
- **Columnas Reutilizable/Dependencias (colega, 2026-07-23):** Navigator/Collector/Interpreter/
  Report Generator son **genéricos** — no leen la ley, leen el Catálogo del DOM que los invoca
  (`app/agents/d0X/catalogo.py`). Lo específico de cada DOM son sus reglas de scoring (SITA≠IPE)
  y su Alignment Agent. Esto es lo que hace viable el DOM_TEMPLATE (ver §DOM_TEMPLATE en
  `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md` o el módulo `app/agents/_template/`).

## Agente d07 · dónde, cómo y cuándo se ejecuta (2026-08-18)

Javo: *«tenemos una nómina de agentes que utilizan los otros dominios; este agente del DOM de
transparencia debe incorporarse a esa nómina, para saber dónde, cómo y cuándo se deben ejecutar»*.

**Dónde.** `app/agents/d07/orquestador.py`. Se despacha desde el Observatorio
(`quira_pages/env_obs.py` → «Verificación por dominio») o por línea de comandos:
`python -m app.agents.d07.orquestador --anio 2026 --meses 1-5 --guardar`.

**Cómo.** Nueve etapas encadenadas con gates que **detienen** en vez de informar. Una corrida que
no puede probar la integridad de su evidencia no publica un resultado peor: no publica ninguno.

| # | Etapa | Módulo | Gate |
|---|---|---|---|
| 1 | Canon sellado | `VARA_SELLO.json` + catálogo v1.1.0 | **CANON** · la vara no se mueve a mitad de prueba |
| 2 | Captura de la fuente | `capturar_lotaip_dpe.py` | transporte declarado (OBS-030) |
| 3 | Adquisición | `descargar_lotaip.py` | **INTEGRIDAD** · rutas únicas, SHA por archivo |
| 4 | Contenido | `analizar_contenido_lotaip.py` | legibilidad, campos, regla de ausencia |
| 5 | Enlaces | `verificar_enlaces_lotaip.py` | procedencia institucional · Nextcloud `/download` |
| 6 | Documentos | `documentos.py` | clase de acto · correlativo · metadato vs documento |
| 7 | Cobertura material | `componentes.py` | sólo declara ausencia con regla objetiva |
| 8 | Calificación | `scoring.py` | CTA/ETA/RP/CI → SITA (Instructivo) |
| 9 | Persistencia | `orquestador.ejecutar(guardar=True)` | corrida con `run_id` y canon usado |

**Cuándo.** Carga inicial pesada una vez por GAD; luego **mensual e incremental** —lo ya
descargado con SHA estable no se vuelve a pedir—. Es lo que hace viable el barrido progresivo de
los 222 GAD sin repetir trabajo.

**Costo: cero.** Ninguna etapa llama a un modelo. Las tres que el catálogo daba por agénticas
resultaron determinísticas para la fuente canónica, porque la DPE es una API estructurada y no un
portal que haya que navegar. La única pieza que sigue exigiendo una capacidad ausente es el OCR
—y su vía es local (Tesseract), no de API.

> **d07 abastece al resto del sistema.** Javo (2026-08-18): *«de este DOM depende toda la
> información que entra a todo el sistema de QUIRA para poder trabajar u operar su gestión; si
> este DOM no cumple las condiciones necesarias, QUIRA no podrá desarrollar su labor»*. El
> catálogo ya lo reflejaba: `Budget Agent` marca la cédula presupuestaria como **compartida
> d01+d02+d07+d09** y `eSIGEF (Fuente)` la declara la misma fuente para los tres. Cuando otro
> dominio pregunte por un instrumento, d07 debe responder con **estado tipado** —publicado ·
> declarado ausente · no hallado · no procesable— y nunca con silencio.

## Opción para despausar la Fase 4 sin costo de API (registrado · 2026-07-24)
Los agentes IA (Navigator/Interpreter/Report Generator/etc.) están en pausa por presupuesto de
Haiku. Camino identificado al revisar **dashAI** (herramienta abierta de la U. de Chile/CENIA,
respaldo ANID): **inferencia local con `llama-cpp-python` + modelos GGUF** (Mistral/Qwen…),
100% local, sin nube ni API keys — el mismo stack que dashAI usa por debajo. QUIRA adoptaría la
**librería** (no la app de escritorio, que no encaja con nuestro pipeline de agentes) directo en
Fase 4. Caveats: (1) un LLM local pequeño en CPU es **menos capaz que Haiku** para interpretación
legal fina — sirve para clasificar/extraer campos; la interpretación compleja hay que probarla;
(2) verificar **licencia** antes de integrar. NO se adopta hoy: queda como **vía preferente para
reactivar la Fase 4** cuando se decida, sin depender del presupuesto de API. (Idea de Javo.)

---
*Meta-Catálogo de Agentes · Dylus Lab © 2026 · "El organigrama cognitivo: quién razona, quién solo calcula."*
