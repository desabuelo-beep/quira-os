# FICHA DE EXPLICABILIDAD QUIRA — 01
**Caso: Transparencia Activa Municipal · Cantón Montecristi · 2026**
*Sprint B.1 Diagnóstico · 2026-06-09*

---

## Caso

Transparencia activa del GAD Municipal de Montecristi: publicación de la
información obligatoria de gestión pública y su efecto sobre el ciclo de
rendición de cuentas 2026 y el acceso a financiamiento.

---

## ¿Qué pasa?

El índice de transparencia activa municipal (ITAM) de Montecristi se sitúa en
**56 sobre 100** (referencia 2025). La información obligatoria se publica de
forma **parcial** y el portal institucional está **desactualizado**.

El estándar exigido para superar el ciclo de rendición de cuentas 2026 es
**80 puntos**: la brecha actual es de **−24 puntos**. El indicador complementario
de opacidad confirma el cuadro: 17.7 en escala invertida, en zona de ruptura.

**Semáforo: 🔴 — nodo crítico en rojo del circuito de rendición de cuentas.**

## ¿Por qué pasa?

La publicación activa de información es la **condición de entrada** del ciclo
de rendición de cuentas: sin información publicada y actualizada, la ciudadanía
no puede participar de forma informada, y la rendición no alcanza el estándar
exigido por el órgano de control.

QUIRA modela la rendición de cuentas como un **circuito convergente de 6
condiciones** que deben cumplirse simultáneamente. Hoy solo **2 de 6** se
cumplen y el circuito está **BLOQUEADO**. La transparencia es una de las dos
condiciones críticas en rojo que mantienen el bloqueo (la otra es la
sostenibilidad fiscal).

## ¿Dónde pasa?

**Convención institucional** (este es un caso de capacidad institucional, no
de brecha territorial): el déficit se localiza en la **sede institucional del
GAD y su portal web**, con impacto **cantonal uniforme** — la opacidad afecta
por igual a todas las parroquias porque restringe el derecho de acceso a la
información de toda la población.

No corresponde capa territorial parroquial para este caso (ver Gap G-03).

## ¿Cuánto cuesta no resolverlo?

**Costo directo medible — USD 400,000:** la convocatoria AECID Gobernanza
Participativa LAT 2026 evalúa a Montecristi como *elegible con brecha*: exige
transparencia ≥ 65 y el cantón tiene 56 (**brecha exacta: −9 puntos**). Subir
9 puntos de transparencia desbloquea USD 400K hoy.

**Costo sistémico — USD 5,300,000:** mientras el circuito de rendición de
cuentas permanezca bloqueado, los dos fondos mayores identificados para el
cantón no tienen ruta de acceso:
- Crédito Agua Potable y Saneamiento (BDE): USD 5,000,000
- Fondo Mujeres Rurales (ONU Mujeres): USD 300,000

La transparencia no es la causa única del bloqueo sistémico (las brechas
fiscal y de presupuesto de género tienen pesos propios), pero es una de las
dos condiciones críticas sin las cuales el circuito no se desbloquea.

## ¿Qué recursos existen?

| Fondo | Monto | Estado para Montecristi |
|---|---|---|
| PNUD — Gobernanza Local Democrática 2026 | USD 500,000 | ✅ elegible hoy |
| Ford Foundation — Democracia y Mandato Local 2026 | USD 400,000 | ✅ elegible hoy |
| AECID — Gobernanza Participativa LAT 2026 | USD 400,000 | 🟡 elegible con brecha (−9 transparencia) |
| AECID — Transparencia y Gobierno Abierto 2026 | USD 200,000 | ⬜ sin evaluar (Gap G-01) |
| BID Lab — Cooperación Técnica Gobernanza 2026 | USD 150,000 | ⬜ sin evaluar (Gap G-01) |

**Lectura ejecutiva:** Montecristi tiene **USD 900K elegibles HOY** en
gobernanza sin requisito de mejora previa, **USD 400K adicionales** al subir
9 puntos de transparencia, y **USD 350K pendientes de evaluación**. Existe
financiamiento específico para resolver exactamente el problema diagnosticado.

---

## Evidencia

1. Índices institucionales de referencia 2025 (transparencia 56.00 · opacidad 17.71)
2. Evaluación viva del circuito de rendición de cuentas 2026 — grafo de
   gobernanza (estado BLOQUEADO · 2/6 condiciones · verificado en línea)
3. Evaluación de elegibilidad de fondos para MCR-001 — base de fondos
   (5 convocatorias evaluadas · brechas cuantificadas por requisito)
4. Radar de fondos: 6 convocatorias adicionales detectadas ciclo jun-2026

## Nivel de confianza

| Pregunta | Confianza | Razón |
|---|---|---|
| ¿Qué pasa? | **Alta** | Indicador con valor y umbral verificados en dos fuentes del sistema |
| ¿Por qué? | **Media** | La causa "publicación parcial + portal desactualizado" está registrada, pero falta el desglose documental por obligación específica (qué literal se incumple y desde cuándo) |
| ¿Dónde? | **Alta** | Convención institucional aplicada (decisión de diseño, ver G-03) |
| ¿Cuánto? | **Alta** | Brecha AECID exacta (−9) y bloqueo sistémico leídos del motor en vivo |
| ¿Recursos? | **Media** | 5 convocatorias evaluadas, 6 sin evaluar por requisitos faltantes (G-01) |

## Gaps detectados

| ID | Tipo | Descripción | Dónde debería vivir | Esfuerzo |
|---|---|---|---|---|
| G-01 | Dato | 6 convocatorias del radar (ciclo jun-2026) sin requisitos cargados → el matcher no las evalúa. USD 350K sin veredicto en este caso | `fondos_conv_requisitos` (carga manual o asistida) | Bajo |
| G-02 | Dato | Convocatoria PNUD Gobernanza duplicada (semilla + radar) — falta deduplicación por código/nombre en el pipeline de inserción | `app/fetchers/fondos_radar_runner.py` | Bajo |
| G-03 | Diseño | "¿Dónde pasa?" no estaba definida para casos de capacidad institucional. Resuelta en esta ficha con la convención "sede institucional / impacto cantonal uniforme" → formalizar en plantilla | `docs/sprint-b/README.md` (ya aplicado) | Hecho |
| G-04 | Trazabilidad | El valor de transparencia 56 figura como "Referencia 2025" sin documento fuente con hash en el corpus. La explicación del "por qué" (qué obligación se incumple, por literal) requiere la evidencia documental del dominio de transparencia | Corpus + mapeo de evidencia documental | Medio |

## Acción propuesta (ejecutar en B.2 — no ahora)

1. **G-01** — cargar requisitos de las 6 convocatorias del radar (desbloquea
   evaluación de USD 350K+ y mejora la pregunta 5 de TODOS los casos).
2. **G-04** — vincular el valor de transparencia a su documento fuente en el
   corpus y desglosar el incumplimiento por obligación específica (sube
   "¿Por qué?" de Media → Alta).
3. **G-02** — deduplicación en el pipeline del radar.

---

*Referencia interna (omitir en versión demo): demo_data.INDICES[ITAM·IOC] ·
EVAL_CRDC_MCR_2026 (Neo4j AuraDB live) · fondos_elegibilidad gad_id=MCR-001
(Supabase) · brechas_json AECID={"ITAM":-9.0} BDE={"ISP":-64.97}
ONU={"PSG":-19.97} · migración 002 + fetcher ciclo 2026-06.*
*Ficha 1/5 · Sprint B.1 · QUIRA OS · Dylus Lab © 2026*
