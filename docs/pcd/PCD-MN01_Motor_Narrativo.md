# PCD-MN01 · Motor Narrativo de QUIRA

> **Expediente con ENTIDAD PROPIA** (asesor + Javo · 2026-07-06). El Motor Narrativo es un **MOTOR
> TRANSVERSAL** de QUIRA —**no un dominio**, no dispara el Protocolo de Expansión Ontológica—. Alimenta
> d09 (fidelidad narrativa RDC) y, al escalar, cualquier dominio + el grafo. Aquí vive todo: arquitectura,
> pipeline, Banco de Casos, ICN, validación, costos, rendimiento, versionado.
> **Cambio de fase (asesor):** de *construir* a **reducir incertidumbre** — calibración científica.

## 0 · La regla que NO se rompió (el mayor logro, según el asesor)
El **Gold Master sigue siendo el canon**. Canon → Motor → Resultados, **nunca al revés** (Regla 1).
El cruce **deriva**; no contamina el Excel. Eso era la mayor preocupación, y se respetó.

## 1 · Encuadre: es un MOTOR, no un dominio (Javo + asesor · 2026-07-06)
El Motor Narrativo es un **motor transversal** de la cadena de QUIRA (Matemático → Documental →
Relacional → **Narrativo** → Causal → Prospectivo → Conversacional). Por eso **NO dispara el Protocolo
de Expansión Ontológica** (Constitución §Mutabilidad: las capacidades transversales —como la Congruencia—
no son dominios ni disparan el gate). Se evaluaron igual las 6 condiciones: cumple **1/2/4** (exportabilidad
· masa crítica de información propia · ancla a fuente real), pero **no procede como dominio** porque (a) se
relaciona con d09 pero **no le pertenece** —allí se **descubrió** (fue el primer laboratorio), no *nació*
(corrección del asesor): el mismo motor verificará mañana un discurso presidencial, una rueda de prensa
ministerial o un informe del Banco Central—, y (b) el slot d04 es del **Macroeje 2 (Capacidad Operativa)**,
incoherente con la naturaleza de **Transparencia/Control Social** del motor. Un **dominio** responde *¿qué
área del Estado observo?* (vertical); un **motor** responde *¿cómo genero inteligencia sobre cualquier área?*
(horizontal). Son planos distintos: encuadrarlo como motor respeta la ontología.
- **Qué alimenta:** hoy d09 (fidelidad narrativa RDC · `H34b`); al escalar, cualquier dominio + el grafo.
- **Vista propia (si se construye):** decisión de UI aparte, en el **Macroeje 3**, **nunca en d04**.
- **d04 "Alertas Institucionales":** su eventual retiro es un tema **separado** (no lo resuelve este motor);
  el SAT es transversal y no depende de esa vista.
- **Nombres (asesor):** el motor = MVN/MIN/Narrativo (Javo define); el scoring = **ICN**.

## 2 · Arquitectura y pipeline (construido · RDC 2024)
```
Video → IDENTIDAD → TRANSCRIPCIÓN → UNIDADES NARRATIVAS
      → [Motor de Descomposición Semántica: NORMALIZACIÓN → CLAIMS]
      → CRUCE DE 5 CAPAS → RELACIONES → SCORING (ICN) → GRAFO → QUIRA IA → UI
```
Módulos en `scripts/motor_narrativo/`: `identidad.py` · `transcribir.py` · `unidades.py` ·
`cruzar_5capas.py`. Pendientes: `normalizar.py` (descomposición) · `scoring_icn.py`.

## 3 · ICN — Índice de Concordancia Narrativa (asesor · reemplaza "IF")
No se llama "IF" (se confunde con Fidelidad). El ICN mide la **concordancia entre la narrativa (discurso)
y la realidad documental (las 5 capas)**. Rúbrica y rango: **se definen en la calibración**, no antes.

## 4 · Disciplina CRÍTICA: NO exponer porcentajes (asesor · punto 1)
Los resultados preliminares (p. ej. el reparto de relaciones del RDC 2024) **NO se muestran** —ni en UI,
ni en reportes, ni en el cajón— **hasta tener la matriz de validación y conocer el error**. Regla dura.

## 5 · Motor de Descomposición Semántica (asesor · punto 5)
"Una unidad narrativa → varios claims" es **otro motor**, no del Narrativo: toma una narrativa y produce
múltiples objetos verificables. Es la etapa de normalización, elevada a motor propio.

## 6 · Banco de Casos (asesor · punto 4) — el activo real
Se construye **ya**. Por cada unidad: `Narrativa → Claims → Clasificación automática → Corrección humana
→ Explicación → Regla aprendida`. Es el **entrenamiento de QUIRA** (memoria metodológica, no fine-tuning).
Ubicación: `data/motor_narrativo/banco_casos/`. Las 98 unidades del 2024 son el primer lote.

## 7 · Matriz de validación → futura hoja canónica (asesor · punto 2)
`| Claim | Clasificación automática | Clasificación humana | Diferencia | Observación |` — el equivalente
del IPCI para el motor. Cuando el motor esté estable, la **clasificación humana** (input, no derivado)
se incorpora al Gold Master como hoja (no rompe Regla 1: es dato humano, como H10c).

## 8 · Orden de trabajo (asesor · punto 8 — se acata)
**RDC 2024 → calibración → Banco de Casos → ICN → validación (precisión, FP/FN) → SOLO ENTONCES
RDC 2025 → presidentes/ministros/entidades.** No repetir errores antes de estabilizar.

## 9 · El grafo narrativo (asesor · punto 9)
Hoy el grafo conecta documentos; mañana conecta **narrativas**:
`Alcalde → Promesa → Obra → Contrato → Pago → Fotografía → Indicador → Ciudadano`. El discurso se vuelve
**red verificable**.

## 10 · Decisiones diferidas
- **Embeddings propios (asesor · punto 7):** no ahora. Con 3.000-10.000 claims validados → entrenar
  embeddings GovTech Ecuador (el mejor corpus del país). Hoy: embeddings generales.
- **youtube-transcript-api (asesor · punto 6):** confirmado como acierto (más velocidad, menos costo,
  más escalabilidad que Whisper; sin GPU).

## Costos · Rendimiento · Versionado
- **Costos (RDC 2024):** transcripción **$0** (auto-captions) · extracción de 98 unidades ≈ 76K tokens
  Haiku ≈ **$0.06**. Cruce: local (embeddings) $0.
- **Rendimiento:** pipeline 2024 end-to-end ≈ 5 min.
- **Versionado:** `3de6a6c` diseño v0.2 → `e8e78f2` identidad → `50a9fcb` transcripción → `f44cd57`
  98 unidades → `d452682` cruce 5 capas.

## 11 · Actualización del asesor (2026-07-06) — el corpus doctrinario propio
El **activo más valioso** que se construye (Javo + asesor): los 98 casos del RDC 2024 **no son solo
validación** — son el **nacimiento del corpus de entrenamiento propio de QUIRA**. Con él, la plataforma
dejará de depender de modelos generalistas: tendrá **doctrina, jurisprudencia, banco de casos y lenguaje**
propios. Vale más que cualquier ajuste de prompts.

**Nombre (asesor):** "Motor Narrativo" queda pequeño → **MIN** (Motor de Inteligencia Narrativa) o **MCN**
(Motor de Congruencia Narrativa): analiza *Narrativa → Evidencia → Congruencia → Integridad*. Scoring =
**ICN**. Javo define el definitivo.

**Banco de Casos — estructura ampliada (asesor):**
`CASO → Narrativa original → Unidad narrativa → Claims → Evidencia encontrada → Relaciones encontradas →
Resultado automático → Corrección humana → Explicación → Regla aprendida → Versión del algoritmo`.

### Propuestas ontológicas (para consenso de mesa + propagación — NO ejecutadas)
- **d04 se REDEFINE, no se elimina:** "Alertas Institucionales" era pobre → **"Inteligencia Institucional"**:
  una **vista transversal** (no un dominio operativo) donde confluyen SAT · alertas · Motor Narrativo · Motor
  Causal · riesgos · tendencias · predicciones. El centro de inteligencia institucional. *(Cambio de dominio →
  dispara propagación Protocolo cond.5 + consenso cond.6 → se ejecuta con Javo.)*
- **Institucionalizar los Motores Cognitivos (asesor 2026-07-06):** existen de facto sin rango formal.
  **NO se edita la Constitución aún** —registra hechos consolidados, no hipótesis en calibración—. Se abre
  un **expediente de arquitectura** propio —*Propuesta de Institucionalización de Motores Cognitivos*— que
  madura mientras el motor se calibra (por qué existen · qué los distingue de un dominio · reglas para
  crear/retirar/propagar motores). Cuando el motor supere la Fase A, la Constitución **absorbe** ese
  trabajo (Fase D). Evita que cada motor futuro (Causal · Prospectivo · Jurídico · Conversacional) repita
  la duda "¿cajón o motor?".

## 12 · Hoja de ruta A/B/C/D (asesor · refinada 2026-07-06)
- **Fase A — Calibración científica (ACTUAL · misión única):** (1) Banco de Casos completo ✅ · (2)
  corrección humana **una por una** · (3) reglas aprendidas · (4) clasificación de errores · (5) matriz
  FP/FN · (6) ICN · (7) precisión/recall/F1. **Objetivo: conocer exactamente el comportamiento del motor.**
  *Se detiene TODO lo demás (gráficos · Neo4j · UI · 2025) hasta cerrar esta fase.*
- **Fase B — Generalización** (solo con motor estable): RDC 2025 · comparación 2024↔2025 · otros discursos
  (eventos · entrevistas · cadenas · debates) → luego prefectos · ministros · presidente.
- **Fase C — Inteligencia:** relaciones visibles/invisibles · contradicciones · silencios institucionales ·
  promesas recicladas · evolución narrativa · grafos narrativos.
- **Fase D — Ontología (al final):** formalizar los Motores Cognitivos en la Constitución · redefinir
  d04 → Inteligencia Institucional · propagación completa.

## 13 · Jurisprudencia algorítmica (asesor 2026-07-06) — el pilar
El Banco de Casos **no es una base de datos**: es el comienzo de una **jurisprudencia algorítmica**. Cada
caso validado responde *¿qué entiende QUIRA por una promesa? ¿qué es evidencia suficiente? ¿cuándo una
narrativa es coherente? ¿cuándo hay contradicción? ¿qué es un silencio institucional?* Con el tiempo, cada
decisión se **fundamenta en casos anteriores** → el motor se vuelve consistente, explicable y auditable.
Es el activo que **independiza a QUIRA de los modelos generalistas**. La misión de la Fase A.

## 14 · Directiva metodológica (asesor + Javo · 2026-07-06) — CONGELAR v0.1
**El motor v0.1 se CONGELA — estado `LOCKED`:** no se toca, no se mejora, no se cambian prompts ni
embeddings. Es el **sujeto experimental**. Modificarlo con 45/98 calibrado destruiría la capacidad de
medir su error real. **NO se construye el v0.2 todavía.**

**Propósito del motor (Javo):** NO interesa *cómo se llevó el proceso* de rendición —eso lo custodian el
CPCCS y la asamblea ciudadana—. Interesa el **discurso de la autoridad y sus cumplimientos**. Por eso R1
(filtrar proceso) es **doctrina**, no una simple mejora.

**Sub-etapas de la estabilización del motor (asesor · dentro de la Fase A):**
- **A1 — Banco de Casos 100%:** terminar los **98/98** sin tocar el algoritmo *(actual: 45/98)*.
- **A2 — Matriz de confusión + taxonomía de errores:** precisión · recall · F1 · sensibilidad ·
  especificidad. Recién con los 98.
- **A3 — Diseño del Motor v0.2 (con evidencia, no intuición):** (1) filtro proceso/gestión [R1] · (2) capa
  **PRESUPUESTO/eSIGEF** [R4] · (3) capa **PAC/SERCOP** (Javo: verificar si lo dicho tiene contrato en el
  portal; si no, es **"paja"**) · (4) validar coincidencia de eje [R2].
- **A4 — Comparación v0.1 vs v0.2** sobre el **mismo corpus** → demostrar científicamente la mejora.

**NO calcular el ICN todavía (asesor):** depende de pesos/categorías/umbrales aún no estabilizados. Primero
se descubre el comportamiento, luego se diseña el índice. Nunca al revés.

**NO tocar d04 (asesor):** ni eliminar ni redefinir. Que el motor sea el centro transversal de inteligencia
es aún **hipótesis**. Primero motor validado, después Constitución.

**Banco de Casos — 16 campos (asesor):** ID · Video · Timestamp · Narrativa original · Unidad narrativa ·
Claims derivados · Clasificación automática · Clasificación humana · Nivel de discrepancia · Tipo de error ·
Fuente documental utilizada · Fuente documental faltante · Explicación · Regla aplicada · Regla nueva ·
Versión del algoritmo · Fecha · Evaluador. *No es un dataset: es un **corpus doctrinario** —difícil de
replicar, uno de los activos intelectuales más valiosos de QUIRA.*

## 15 · Resultado de la Fase A — matriz de confusión (2026-07-06)
Los **98 casos** del RDC 2024 calibrados uno por uno (motor v0.1 `LOCKED`). Verdad humana: 36 OK ·
20 proceso_rendición · 14 falso_positivo_evidencia · 13 cifra_financiera · 7 logro_cobertura ·
5 meta_narrativa · 3 verificar_pac.

**Precisión global: 37% (36/98).** Lectura clave: **48/98 son categorías que el POA no cubre** (proceso,
cifras financieras, cobertura de servicios, contratación, retórica). De los **50 casos que sí son obra
verificable contra el POA, el motor acierta 36 = 72%**. El núcleo del cruce es sólido; el error está en las
**fuentes documentales que faltan**, no en el algoritmo base.

**Roadmap del Motor v0.2 — con evidencia dura (no intuición):**

| Mejora | Regla | Efecto medido en el corpus |
|---|---|---|
| Filtro proceso/gestión | R1 | −20 falsos positivos |
| Validar coincidencia de eje | R2 | −14 falsos positivos |
| Capa PRESUPUESTO / eSIGEF | R4 | +13 cifras financieras verificables |
| Registro de programa (patronato, acción social) | R6 | +7 coberturas de servicio |
| Capa PAC/SERCOP (punto de Javo) | R7 | +3 obras en contratación ("¿es paja?") |
| Filtro meta-narrativa | R3 | −5 retórica de marco |

**Estado Fase A:** A1 (Banco 98/98) ✅ · A2 (matriz + taxonomía) ✅ · sigue **A3 (diseño v0.2 con esta
evidencia)** · A4 (comparación v0.1↔v0.2 mismo corpus). El ICN se diseña **después** de A3 (asesor).

---
*PCD-MN01 · Dylus Lab © 2026 · el Motor Narrativo, motor transversal (v0.1 LOCKED) · corpus doctrinario propio · Fase A cerrada.*
