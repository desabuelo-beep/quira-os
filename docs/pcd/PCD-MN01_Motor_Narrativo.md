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

## 16 · Construcción v0.2 y v0.3 (2026-07-07)
**v0.2** (`motor_v2.py`, LOCKED como benchmark): R1 filtro proceso + R2 validación de eje.
Comparación A4 sobre el mismo corpus (verdad humana): **v0.1 36% → v0.2 70%**.

**v0.3** (`motor_v3.py`): suma la **capa PAC/SERCOP (R7)** — el "¿es paja?" de Javo. Extracción del
PAC desde DOCX (`extract_pac_docx.py`; PDF sale con glyphs scrambled). Una unidad sin correlato en el
POA se cruza contra el PAC del **periodo** (2024+2025+2026, no solo el año: una obra anunciada en la
rendición 2024 se contrata en 2025). Clase nueva **`en_contratacion`** (real, verificable, aún no
ejecutada) vs `sin_correlato` (no aparece en POA ni PAC).

Dos técnicas nacidas del diagnóstico del corpus (no intuición):
- **Guard de integridad** — `en_contratacion` solo con proceso tipo **Obra/Consultoría**, no compras
  (Bien/Servicio). Filtró 2 falsos positivos (insumos quirúrgicos, refrigerios que matcheaban una obra
  anunciada). Principio QUIRA: no afirmar contratación sin respaldo del tipo correcto.
- **Override por nombre de obra** — el embedding puro diluye nombres propios ("Parque La Huella"
  matcheaba 0.356 < umbral). Si el PAC nombra la misma obra (≥2 tokens propios compartidos) con eje y
  tipo coincidentes → match. Recuperó el 079.

**Resultado v0.3:** 71% (rúbrica más estricta: `verificar_pac` exige verificación positiva en POA o PAC,
no basta "no encontrado"). **Los 3 casos R7 correctos** (078+079 `en_contratacion`, 087 `coherente`),
`en_contratacion` = 2, **cero falsos positivos**.

**Corrección honesta:** el Parque La Huella NO era "paja". La primera lectura ("no aparece en SERCOP")
fue artefacto de un PAC 2025 sucio (print del portal, texto fragmentado). Javo mejoró los DOCX 2025/2026
→ la obra sí existe como proceso. El motor con datos limpios la verifica. Lección: la calidad de la
fuente determina el veredicto — de ahí la Regla 3 (sin evidencia verificada, no hay dato).

## 17 · Capa CPCCS — informe escrito (2026-07-07)
Javo (aval): usar el **informe escrito de rendición** (CPCCS) de dos formas ("Ambas"):
**(A) evidencia** — corroborar el discurso del video contra lo declarado por escrito; **(B) fuente** —
cuando una rendición NO tiene video (ej. Aseo EP/Bomberos/Patronato 2024) el informe es la ENTRADA.
Fuentes: `Rendición de cuentas 2023-2025/<entidad>/*.docx` (Javo pasó todo el holding de PDF a
Word/Excel). Años: informe 2024 (evento 2025) e informe 2025 (evento 2026).

**(A) implementada** (`extract_informe_docx.py` + flag `en_informe` en `motor_v3.py`): la matriz de
rendición viene fragmentada en celdas → se une el texto y se corta en ventanas deslizantes (modo
documento). Corrobora **41/98** unidades del discurso 2024. Aditiva: NO cambia las clases de
verificación (POA/PAC), añade la voz escrita del actor. **Hallazgo de auditoría:** en cifras/cobertura
la corroboración es baja (cifra_financiera 2/13, cobertura 3/7) → el alcalde menciona cifras en el
video que **no siempre reescribe en el informe formal**. Eso ES una señal (dicho vs documentado).

**Pendiente:** (B) fuente-sin-video (plumbing + extracción Haiku de unidades del informe) · R6 patronato · ICN.

## 18 · Capa R4 — cifras financieras vs cédula oficial (2026-07-07)
Decisión de Javo: verificar la EJECUCIÓN presupuestaria del discurso. **Hallazgo al entrar al canon:** el
Gold Master expone `PSG_EJECUCION`=2.83%, que es OTRA métrica (sub-índice analítico), **no** la ejecución
presupuestaria general que dijo el alcalde (84%). Esa ejecución general NO es output del canon → vive en
el documento fuente (**cédula de gastos**). Por eso R4 la verifica **documentalmente** contra la cédula,
sin recalcular ninguna métrica del Gold Master (Regla 1/4 intactas · solo lectura · cifras públicas de
presupuesto). Javo confirmó la ruta documental.

Implementada (`extract_cedula_xls.py` + `_r4` en `motor_v3.py`): lee el total de gastos de la cédula
oficial (codificado $27.9M / devengado $23.5M) → **ejecución 2024 = 84.32%**. Verifica los claims de
ejecución general del año contra ese dato; ingresos/deuda/histórico → `requiere_registro` (sin fuente aún).

**Resultado:** de 13 cifras financieras, **2 VERIFICADAS** contra la cédula (MN2024-030 "84%" y 032
"84.32%" ↔ cédula 84.32%, exacto) · 9 `requiere_registro` · 2 sin cifra explícita. Aggregate **70%**
(mantiene, con capacidad nueva). Guard: un claim financiero necesita una cifra (%/millones/$) para entrar
a R4. El motor hoy: 4 capas de verificación (POA·PAC·R4) + corroboración CPCCS + filtro proceso.

**Ingresos/deuda = NO públicos** (la DPE solo publica cédula de gastos, no de ingresos · confirmado por
Javo). Esas 9 cifras son `sin_evidencia_publica`: un **HALLAZGO de transparencia, no un pendiente**. Ver §19.

## 19 · Reencuadre — Taxonomía de Evidencia Pública (2026-07-07)
Al no existir cédula de ingresos pública (ni registros de deuda; patronato 2024 solo sep–dic), Javo y el
asesor deciden **no cambiar el rumbo**: la restricción no debilita el motor, **cambia la naturaleza de la
evidencia**. Tesis afinada:

> **QUIRA no certifica verdad: certifica el NIVEL DE VERIFICABILIDAD PÚBLICA de cada afirmación.**

Nunca rellena un vacío documental; lo DOCUMENTA (Regla 3). La ausencia de respaldo público es un
HALLAZGO irrebatible: no decimos "mintió", decimos "el ciudadano no puede comprobarlo con lo público".

Taxonomía por afirmación (`nivel_evidencia` en `motor_v3.py`, derivada de qué capa la respaldó):
| Nivel | Significado | Capa |
|---|---|---|
| **independiente** | registro administrativo EXTERNO verificable | POA · PAC/SERCOP · cédula de gastos |
| **institucional** | solo en el documento del propio actor | informe CPCCS |
| **parcial** | evidencia con ventana temporal limitada | R6 patronato (sep–dic 2024) — próximo |
| **sin_evidencia_publica** | no hay documento público (incl. no publicado) | ingresos/deuda |
| **contradiccion** | hay evidencia pública y contradice lo dicho | R4 discrepancia |

Resultado RDC 2024 (78 afirmaciones sustantivas, 20 proceso filtradas): **45 independiente · 13
institucional · 20 sin evidencia pública**. Ese gradiente, en lenguaje de gobernanza, ES el veredicto.

**R8 (jurisprudencia):** la ausencia de respaldo público es un hallazgo, no una falla; se marca en
lenguaje no acusatorio; JAMÁS se fabrica verificación.

**Frontera arquitectónica (Javo):** el Motor (transversal) produce el `nivel_evidencia` por afirmación.
El **Índice de Evidencia Pública (IEP)** —agregado que mide la calidad democrática de la información— y
el hallazgo "el GAD publica gastos pero oculta ingresos" pertenecen al **dominio TRANSPARENCIA, NO a
RDC**. Como métrica nueva, el IEP **nace en el CANON, no en Python** (Regla 9). Aquí queda el insumo
(los niveles por afirmación); el IEP se define en Transparencia.

## 20 · Capa R6 — coberturas vs registro Literal D del patronato (2026-07-07)
Fuente (Javo): `Literal D servicios institucionales/Patronato/*.xlsx` (LOTAIP Numeral 5-22) — registro
oficial MENSUAL: servicio → "número de personas que acceden". No está en el canon ni en Supabase → se
lee directo (`extract_literal_d_xls.py`). **Ventana honesta (aval Javo):** 2024 solo sep–dic (34,804
personas/4 meses); 2025 completo (114,559/12 meses). JAMÁS se extrapola al año.

Implementada (`_r6` en `motor_v3.py`): cruza las coberturas del discurso contra los servicios del
registro. Match → `verif_cobertura` (nivel **parcial**: ventana + métrica distinta — el registro mide
"personas", el discurso "atenciones"; se reporta el dato real sin igualar). Resultado (7 coberturas):
**1 verificada** (059 Centro Diurno del Buen Vivir), 6 `sin_evidencia_publica` (Acción Social y servicios
que no cruzan; las obras-beneficio 090/097 no son servicios del patronato). Honesto: la cobertura anual/
atenciones no es plenamente verificable con un registro de ventana parcial.

**Bug corregido:** el `\b` FINAL en las regex `_FIN`/`_COB` rompía el match por prefijo
(atenci≠atenciones); removido → los claims de cobertura ya entran a R6.

**Estado del motor — 5 capas + taxonomía:** POA · PAC/SERCOP · R4 cédula · R6 patronato + corroboración
CPCCS → `nivel_evidencia` por afirmación. RDC 2024 (78 sustantivas): **45 independiente · 12 institucional
· 2 parcial · 19 sin evidencia pública** (+20 proceso). R4-ingresos/deuda = sin fuente pública (§19).

---
*PCD-MN01 · Dylus Lab © 2026 · el Motor Narrativo, motor transversal (v0.1 LOCKED · v0.3 con capa PAC) · corpus doctrinario propio.*
