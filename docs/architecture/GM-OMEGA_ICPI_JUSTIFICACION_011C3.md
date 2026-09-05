# GM-Ω · ICPI — JUSTIFICACIÓN DE LAS TRANSFORMACIONES  `011-C3`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/justificacion_transformaciones.py` barriendo el Gold Master completo y los documentos históricos de enero-abril.

> ### El encargo
> No es «¿qué fórmula nos parece mejor?». Es: **¿qué transformación fue declarada, cuál fue implementada, cuál alimenta efectivamente al ICPI, y qué evidencia justifica cada transición?**

```
  DECLARADO  ≠  IMPLEMENTADO  ≠  EFECTIVAMENTE UTILIZADO  ≠  JUSTIFICADO
```

⚠️ **No se tocó nada.** Ni `C_i`, ni `E_i`, ni `T_i`, ni la fórmula, ni las calibraciones, ni `Ci_Manual_2025`, ni `Ci_Adaptativo`. El Gold Master es inmutable y el baseline **27,4582 %** sigue congelado. `C3` levanta acta.

⚠️ **Y la regla que ordena la etapa** (`DOC-011`): una transición documentada **no autoriza a inventar su causa**. Reconstruir perfectamente CUÁNDO apareció algo no dice nada sobre POR QUÉ apareció. Donde no hay razón escrita, el resultado correcto es `NO DETERMINABLE` — y eso es un hallazgo, no un fallo del peritaje.

## ★ 0 · El documento que reordena `011-C3`

`metodologia.docx`, **creado el 2026-03-25** — es decir, **anterior al 27-abr-2026**. Define las **seis** variables con definición conceptual, fundamento normativo y **tabla de escala con criterio de verificación**:

| Variable | Título en la metodología | Definición conceptual |
|---|---|---|
| `P_i` | **Peso Presupuestario** | Proporción del presupuesto total de la muestra estratégica que corresponde a la meta i. Operacionaliza el mandato del artículo 54 del COPFP: las metas que consumen mayor proporción del presupuesto del PDOT tienen mayor peso en la  |
| `R_i` | **Relevancia Normativa** | Factor de ponderación que refleja la jerarquía constitucional y legal de las competencias municipales. Operacionaliza los artículos 54 y 55 del COOTAD en combinación con los artículos 12 y 14 de la Constitución. |
| `V_i` | **Inmutabilidad Documental** | Producto lógico AND que certifica la existencia de evidencia documental verificable en los cinco silos de verificación. Es la variable más importante del modelo porque operacionaliza el artículo 18 de la Constitución —derecho a in |
| `E_i` | **Fricción de Autonomía** | Factor que ajusta el ICPI según la modalidad de ejecución institucional, reconociendo que la ejecución delegada introduce fricciones de coordinación que reducen la trazabilidad directa del GAD sobre la inversión. Fundamentado en e |
| `T_i` | **Materialización Temporal** | Proporción del presupuesto codificado que fue efectivamente devengado al cierre del año fiscal. Operacionaliza los artículos 115 a 117 del COPFP, que distinguen entre compromiso —contrato firmado, obligación contraída pero prestac |
| `C_i` | **Imputabilidad Orgánica** | Grado de claridad en la asignación de responsabilidad sobre la meta según el Estatuto Orgánico de Gestión por Procesos del GAD. Operacionaliza el artículo 233 de la Constitución —responsabilidad ineludible de los servidores públic |

### ⚠️ Primera consecuencia · hay que corregir `007-B0`

`007-B0` concluyó que **`C_i` entró el 27-abr-2026**, apoyándose en `H01!A94`. Esa celda dice:

> ★ **Ci DETERMINISTA v1.0** (Javo Delgado Santana, 27-Abr-2026): Ci arranca en 1.00. Deducciones legales Sección L calculan Ci final.

Leída junto a una metodología del 2026-03-25 que **ya contiene `C_i`**, la fecha no dice lo que se le hizo decir:

| Lectura | Estado |
|---|---|
| «el 27-abr **nace** `C_i`» | 🔴 **INFERIDO y superada** |
| «el 27-abr nace **`Ci` DETERMINISTA v1.0**, una versión nueva de un factor preexistente» | ✅ **DEMOSTRADO** · lo dice la propia celda, y la metodología anterior lo prueba |

**Y el error tiene una forma reconocible:** se leyó la fecha del artefacto que documenta un cambio como si fuera la fecha del concepto. Es el escalón 7 de la escalera —**lo leído ≠ la fuente**— aplicado a una genealogía.

### ★ Segunda consecuencia · la transformación real de `C_i`

Lo que ocurrió el 27-abr **no fue una incorporación: fue una sustitución de mecanismo bajo el mismo nombre.**

```
  ANTES (metodología, 25-mar-2026)      DESPUÉS (motor, 27-abr-2026)
  ──────────────────────────────        ────────────────────────────
  C_i = IMPUTABILIDAD ORGÁNICA          C_i = CALIDAD DE PROCESO
  claridad de la asignación de          descuento por infracciones
  responsabilidad en el Estatuto        normativas verificadas

  Constitución 233 · NCI 200-04/401-01  LOSNCP · CGE · COPFP · CPCCS
  escala {1,00 · 0,90 · 0,75}           MAX(0,50 · 1,00 − Σ ded.)
  mínimo posible 0,75                   mínimo posible 0,50
```

| Afirmación | Grado |
|---|---|
| Son **dos constructos distintos** con el mismo nombre | **DEMOSTRADO** · definición, fundamento normativo, escala y rango difieren |
| El nuevo mecanismo admite valores que la escala original **no contemplaba** (`0,50`) | **DEMOSTRADO** |
| La **razón** de la sustitución | ⬜ **NO DETERMINABLE** · ningún documento la explica |

### ★ Tercera consecuencia · la Sección I es un vestigio del primero

`011-C2` no supo explicar por qué `H01` Sección I trae `Cod_Unidad`, `Dirección Responsable` y `Base Legal Estatuto` con escala «exclusivo / compartido / difuso». Ahora se explica solo: **eso es la implementación del `C_i` original**, la imputabilidad orgánica. Sigue viva dentro del libro, al lado del mecanismo que la sustituyó.

Y con eso las **cuatro divergencias de `011-C2` dejan de ser cuatro anomalías sueltas** y pasan a ser un único fenómeno con nombre:

> ### Dos generaciones del mismo factor conviven en el instrumento
>
> La Sección I implementa el constructo **original**; las Secciones L/M implementan el **nuevo**; y `Ci_Manual_2025` conserva los valores del original como fallback. Ninguna capa se retiró al añadirse la siguiente.

⚠️ **Esto no dice que el cambio fuera indebido.** Dice que ocurrió, que ninguna de las dos capas se retiró, y que **el instrumento no declara cuál gobierna**. La valoración es de `011-C4`.

### Las escalas originales, literales

**`E_i`** — según `metodologia.docx`:

| Modalidad de Ejecución | valor | Justificación |
|---|---|---|
| Ejecución directa por direcciones del GAD | 1,00 | Control total, rendición directa |
| Ejecución compartida mediante convenio interinstitucional | 0,90 | Coordinación documentada, responsabilidad compartida |
| Delegación a entidad adscrita (empresa pública municipal, patronato municipal, corporación) | 0,75 | Fricción por autonomía administrativa de la entidad |

**`C_i`** — según `metodologia.docx`:

| Claridad de Responsabilidad | valor | Criterio de Verificación |
|---|---|---|
| Responsable único identificado en Estatuto | 1,00 | Estatuto asigna responsabilidad exclusiva a una dirección |
| Responsabilidad compartida entre dos direcciones | 0,90 | Corresponsabilidad documentada, cumple NCI 401-01 separación de funciones |
| Responsabilidad difusa o no especificada | 0,75 | Ambigüedad organizativa, sin dueño claro del proceso |

> ### ★ Y aquí está la respuesta a `C3-09`
>
> `E_i` y `C_i` comparten escala `{1,00 · 0,90 · 0,75}` y vocabulario **porque ambas son escalas ordinales de tres grados sobre el mismo Estatuto Orgánico** — pero miden ejes distintos: `E_i` **quién EJECUTA**, `C_i` **quién RESPONDE**.

La superposición que `011-C2` midió **no es un accidente ni un defecto: es deliberada y está justificada en la metodología**. Y las divergencias son exactamente lo que cabría esperar — la propia tesis trae un caso:

> `M3` (Salud): ejecución **directa** del GAD (`E=1,00`) pero responsabilidad **compartida** entre Planificación —que formula— y Obras Públicas —que ejecuta— (`C=0,90`).

| Afirmación | Grado |
|---|---|
| La superposición de escala está **justificada documentalmente** | **DEMOSTRADO** |
| Que `E_i` y `C_i` puedan divergir en una misma meta es **conceptualmente esperable** | **DEMOSTRADO** · con caso ilustrado en la metodología |
| Que las **12 divergencias concretas del motor** respondan cada una a esa razón | ⬜ **NO DETERMINABLE** · exigiría la justificación meta a meta, que no existe |

⚠️ **La corrección que esto obliga a hacer a `011-C2`:** ahí se escribió que «**nada en el instrumento explica la diferencia**». Era cierto **del instrumento** y falso **del corpus**: la metodología sí explica por qué pueden diferir. Lo que sigue sin explicación es cada asignación concreta.

## 1 · La cadena de versiones, que es la columna vertebral

`H80_MODEL_REGISTRY` registra el versionado del motor con fecha, operador y versión anterior. Es la mejor fuente de genealogía del libro:

| Versión | Fecha | Operador | Estado | Anterior |
|---|---|---|---|---|
| `v1.0.0` | 2026-01-15 | DYLUS_LAB | ARCHIVADO | — |
| `v1.0.1` | 2026-02-28 | SIAP_ENGINE | ARCHIVADO | v1.0.0 |
| `v1.0.2` | 2026-03-31 | SIAP_ENGINE | ARCHIVADO | v1.0.1 |
| `v2.1 Gold Master` | 2026-05-01 | SIAP_ENGINE | ACTIVO | v1.0.2 |
| `REGLA` | Ningún RUN |  |  | — |
| `v2.2 RC-2AB + Histórico` | 2026-05-18 | QUIRA_OS_SENTINEL | ACTIVO | v2.1 Gold Master |

### ★ Lo que esta tabla revela sobre `C_i`

`011-C2` estableció que `C_i` se creó el **27-abr-2026** (`H01!A94`). Situado en la cadena:

```
  v1.0.2   31-mar-2026   ARCHIVADO
      │
      │     ⬅ 27-abr-2026 · nace C_i · NINGUNA VERSIÓN LO REGISTRA
      │
  v2.1     01-may-2026   ACTIVO
```

Dos observaciones, ambas verificables en la tabla:

| # | Observación | Grado |
|---|---|---|
| 1 | La incorporación de `C_i` cae **dentro del salto `v1.0.2 → v2.1`** y no tiene entrada propia en el registro | **DEMOSTRADO** |
| 2 | El salto de versión es `1.0.2 → 2.1`: se omiten `1.1` y `2.0` | **DEMOSTRADO** |
| 3 | Por qué la incorporación de un sexto factor no generó su propia entrada de versión | ⬜ **NO DETERMINABLE** |

⚠️ **Esto no es una acusación de mal versionado.** `P-05` del protocolo de gobernanza algorítmica exige versionado obligatorio, y el registro existe y es coherente. Lo que falta es **granularidad**: el salto que contiene el cambio más consecuente del motor —pasar de cinco a seis factores— se registra igual que cualquier otro.

## ★ 2 · Qué factores tienen justificación DECLARADA, y cuáles no

El hallazgo más limpio de `C3`, y no hubo que interpretarlo: `H14_PONDERADORES` **tiene columnas de justificación por meta**.

> `Justificación R_i`
> `Justificación P_i`

| Factor | ¿Tiene justificación declarada en el libro? |
|---|---|
| `P_i` | ✅ **sí** · `H14` columna «Justificación P_i», meta a meta |
| `R_i` | ✅ **sí** · `H14` columna «Justificación R_i», meta a meta |
| `V_i` | 🟡 parcial · la regla de combinación está en `H13`, sin columna de justificación |
| `T_i` | 🟡 parcial · jerarquía de fuentes declarada en el glosario |
| `E_i` | 🔴 **no** · literal en `H12`, sin fórmula ni columna |
| `C_i` | 🔴 **no** · `H01` Sección I trae `Base Legal Estatuto` por meta, pero **eso justifica la IMPUTACIÓN, no el VALOR** |

> ### Las dos dimensiones sin justificación por meta son exactamente las dos que `011-C2` encontró superpuestas

No es casualidad interpretable, y `C3` no la interpreta. Es un hecho con dos lecturas posibles y ninguna evidencia para elegir:

| Lectura | Qué implicaría |
|---|---|
| `P_i` y `R_i` se justificaron porque **son las que la tesis desarrolló** | la justificación siguió al trabajo teórico |
| `E_i` y `C_i` se incorporaron **en fase de construcción**, cuando el hábito de justificar por meta ya no se aplicó | la justificación siguió al calendario |

Cuál de las dos ocurrió: ⬜ **NO DETERMINABLE**.

## 3 · Las nueve preguntas, con su evidencia

Cada bloque muestra **la evidencia encontrada**, no un resumen de ella. Y separa su procedencia, porque no valen lo mismo:

| Procedencia | Qué acredita |
|---|---|
| **El libro** | lo que el instrumento **declara** de sí mismo |
| **Los documentos** de enero-abril | lo que se **escribió** al construirlo — la única fuente que puede justificar |

### C3-01 · ¿Quién introdujo `C_i`, cuándo y en qué versión?

**En el libro:**

- `H01_PARÁMETROS` — ★ Ci DETERMINISTA v1.0 (Javo Delgado Santana, 27-Abr-2026): Ci arranca en 1.00. Deducciones legales Sección L calculan Ci final. Ci_Base columna E es FÓRMULA de Sección M — NO hardcodeado. Nombres de Dirección = H02b exacto (Res. 040-2025).
- `H02_GLOSARIO_QUIRA` — SIAP-ICPI Metodología v1.0 — DECISIÓN Javo Delgado Santana, 27-Abr-2026
- `H02_GLOSARIO_QUIRA` — Estatuto Orgánico GAD Montecristi 2025 — Decisión Javo Delgado Santana, 27-Abr-2026
- `H02b_ORGÁNICO_CLASIFICADOR` — ★ DECISIÓN ARQUITECTÓNICA v1.0 (Javo Delgado Santana, 27-Abr-2026): TIPO_FINANCIAMIENTO es atributo de la META (H04 col O / H07c), NO de la dirección. INTANGIBLE_FLAG es atributo de la META (H13), NO de la dirección. Una misma unidad puede tener metas tangibles e intangibles y distintos tipos de fin

**En los documentos históricos:**

- `Metodología Integral SIAP-ICPI v2.4 (Maestra) (1).docx` — …v2.4 Ecosistema de Integridad Algorítmica Preventiva Desarrollado por Quadrum GovTech | Autor: Ronald Javier Delgado Santana CAPÍTULO I: FUNDAMENTOS Y GOBERNANZA PREVENTIVA 1.1. Propósito y Alcance (Ref: H38) El Sistema de Integridad Algorítmica Preventiva (TERRA SIAP-ICPI) es una arquitectura de su…
- `anexo 0.docx` — …GOVTECH 2026 ANEXO 0 INGENIERÍA FINANCIERA Y VENTANA DE OPORTUNIDAD Investigador Principal: Ronald Javier Delgado Santana Creador Metodología ICPI y Protocolo QUADRUM Febrero 2026 Versión 2.0 Documento Confidencial 0.1. INGENIERÍA FINANCIERA: La viabilidad financiera de QUADRUM se sustenta en modelo…
- `ANEXO L MANUAL TECNICO QUADRUM FINAL v5.0.docx` — …cias ──────────────────────────────────────────────────────────── Investigador Principal: Ronald Javier Delgado Santana Creador Metodología ICPI y Protocolo QUADRUM Febrero 2026 ÍNDICE GENERAL PARTE I: FUNDAMENTOS METODOLÓGICOS L.1. Propósito y Alcance del Protocolo L.2. Del SIAP-ICPI a QUADRUM: Evo…

### C3-02 · ¿Qué fenómeno se dijo que medía?

**En el libro:**

- `H01_PARÁMETROS` — ▌ SECCIÓN I — TABLA Ci — CALIDAD DE PROCESO ORGÁNICO POR META
- `H02_GLOSARIO_QUIRA` — Variable que mide la calidad institucional del proceso orgánico responsable de una meta. ★ DETERMINISTA v1.0: Ci = MAX(1.00 - Σ deducciones normativas, 0). El proceso nace con Ci=1.00 (presunción de legalidad). Las infracciones CGE/SERCOP/COPFP/CPCCS deducen puntos. Fuente: H01 Sección L. Marco lega

**En los documentos históricos:**

- `memoriaa algo quira.docx` — …✅ VIVO AVEP 🟢/🟠 CININ — Cadena de Integridad Intersistémica ✅ VIVO como... Trazabilidad Intersistémica D1→D5 Responsabilidad Orgánica Vinculante (Ci) ✅ VIVO como... H07c: firma Director activa Ti_V Erosión del Compromiso ✅ VIVO como... Deterioro institucional en RC-M Brecha de Integridad Intersistém…
- `metodologia.docx` — …de los servidores públicos por sus actos y omisiones. Este artículo fundamenta la variable C_i del modelo: la imputabilidad orgánica que el SIAP-ICPI asigna a cada ruptura de la cadena de congruencia tiene base constitucional directa. 2.6.3. Régimen de Planificación Obligatoria El Código Orgánico de…
- `metodologia.docx` — …Potable de Montecristi, entidad adscrita con personería jurídica y presupuesto propio. 3.4.6. Variable C_i: Imputabilidad Orgánica Definición conceptual: Grado de claridad en la asignación de responsabilidad sobre la meta según el Estatuto Orgánico de Gestión por Procesos del GAD. Operacionaliza el …

### C3-03 · ¿Por qué se pasó de 5 a 6 factores?

**En los documentos históricos:**

- `memoriaa algo quira.docx` — …como se operativiza el sistema. SI ME EQUIVOCO DIGAME PORFA QUIRA_Gov_v1.1_DEMO.html Archivo estamos listos, se incorporo el índice de participación? estamos listo o mal mas cambios estratégico al demo? cual opcion? es normal que quira y tgi estan unidos por otras lineas y no directo? --- name: "TGI…
- `memoriaa algo quira.docx` — …e "dominio observable" a "dominio jurídicamente completo". Sobre el scorecard Coincido con tu corrección. La nueva dimensión: Fundamento Constitucional Computable es real y distinta de Neo4j Operativo. Porque: Neo4j Operativo ≠ Capacidad de explicar una conclusión mediante una cadena constitucional …
- `memoriaa algo quira.docx` — …inio observable" a "dominio jurídicamente completo". --- ## Sobre el scorecard Coincido con tu corrección. La nueva dimensión: Fundamento Constitucional Computable es real y distinta de Neo4j Operativo. Porque: Neo4j Operativo ≠ Capacidad de explicar una conclusión mediante una cadena constitucional…

### C3-04 · ¿Por qué esos cuatro eventos (CGE · SERCOP · POA · CPCCS)?

**En el libro:**

- `H00_ÍNDICE` — Grupo 1 — Silo S2 / Diagnóstico social PDOT 2023-2027
- `H00_ÍNDICE` — Base de conocimiento PDOT — 1578 entradas diagnóstico
- `H02_GLOSARIO_QUIRA` — Variable que mide la calidad institucional del proceso orgánico responsable de una meta. ★ DETERMINISTA v1.0: Ci = MAX(1.00 - Σ deducciones normativas, 0). El proceso nace con Ci=1.00 (presunción de legalidad). Las infracciones CGE/SERCOP/COPFP/CPCCS deducen puntos. Fuente: H01 Sección L. Marco lega
- `H02_GLOSARIO_QUIRA` — Código Orgánico de Organización Territorial, Autonomía y Descentralización. Marco legal principal de los GADs municipales.

**En los documentos históricos:**

- `historial conversacional de Quira.docx` — …n territorial del cantón Así como QLEP atomiza la Constitución Nacional. QUIRA Territorial deberá atomizar: Diagnóstico Propuesta Modelo de Gestión PUGS del PDOT. Ese probablemente sea el siguiente gran salto metodológico después de Alpha. 3. No cargaría Neo4j todavía Y aquí voy a ser un poco contra…
- `historial conversacional de Quira.docx` — …un analista de datos de alguien que entiende cómo funciona una institución social. Y la respuesta cambia el diagnóstico. Tengo los datos del Patronato noviembre 2025 (11 meses) desglosados por grupo. Veamos lo que realmente está pasando: Lo que esconde Ti=50% Grupo Descripción Cod ($) Dev ($) Ti ───…
- `historial conversacional de Quira.docx` — …→ ejecución de programas: CRISIS Ti_estructura_capital (G84): 38.6% → infraestructura del servicio: baja El diagnóstico real no es "el Patronato no gasta". Es: El Patronato paga personal pero no ejecuta programas. Eso es mucho más grave. Significa que hay una estructura institucional que consume rec…

### C3-05 · ¿Por qué esos pesos (0,10 · 0,15 · 0,05/0,20 · 0,50)?

**En el libro:**

- `H95_LIMITACIONES` — Los pesos de las 5 dimensiones (20/20/25/25/10) son definidos por criterio experto (Dylus Lab), no por análisis de componentes principales (PCA) o regresión sobre resultados.

### C3-06 · ¿Por qué el piso `MÁX(0,50; …)`?

**En el libro:**

- `H77_DATA_DICTIONARY` — Leer: Ci_final = MAX(0.50, 1.00 - Σ(INF_i × deducción_i))

### C3-07 · ¿Por qué existe `Ci_Manual_2025` en 2026?

**En el libro:**

- `H02_GLOSARIO_QUIRA` — Técnica de reverse engineering que inyecta los valores históricos 2025 de infracciones normativas en H01 Sección L para que el algoritmo Ci reproduzca exactamente el ICPI canónico 69.9309%. Distribución 2025: 11 metas Ci=1.00 / 9 metas Ci=0.90 / 5 metas Ci=0.75. En 2026, los valores reales sustituye
- `H12c_ICPI_HISTÓRICO_ANUAL` — ✅ ICPI_Real_2025 = 69.9309% — primer resultado auditado bajo metodología SIAP-ICPI completa (calibración retroactiva Ci 2025).
- `H39_AUTOCONTROL_ECOSISTEMA` — Nota #22 Critico: Si INFs=0 y axioma falla, revisar valores Ci_Manual_2025 en Seccion M de H01_PARAMETROS.

### C3-08 · ¿Qué es `Ci_Adaptativo` y por qué no se conecta?

**En el libro:**

- `H01_PARÁMETROS` — ▮ SECCIÓN C — PARÁMETROS FISCALES Y DISCRIMINACIÓN POSITIVA
- `H02_GLOSARIO_QUIRA` — Versión calculada del Ci que incorpora modificadores según TIPO_FINANCIAMIENTO e INTANGIBLE_FLAG. Fórmula: Ci_adaptativo = MIN(Ci_base × Modificador, 1.0). El Ci_base siempre viene de H01 Sección I. Calculado en H12.
- `H02_GLOSARIO_QUIRA` — Tipo de financiamiento de fondos externos no reembolsables obtenidos por concurso competitivo. Su captura exitosa activa discriminación positiva en Ci (×1.15). No impacta presupuesto propio del GAD.
- `H02_GLOSARIO_QUIRA` — Hoja H02b_ORGÁNICO_CLASIFICADOR. ADN institucional del sistema SIAP-ICPI. Contiene la clasificación de 20 unidades del GAD por TIPO_PROCESO, ROL_INSTITUCIONAL y EVIDENCIA_PREDOMINANTE. ★ ARQUITECTURA v1.0: clasifica UNIDADES ORGÁNICAS. CLASE_PRODUCTO, INTANGIBLE_FLAG y TIPO_FINANCIAMIENTO son atribu

**En los documentos históricos:**

- `Metodologia_SIAP_ICPI.docx` — …iento tiene menor impacto sobre derechos constitucionales básicos. Adicionalmente, el sistema aplica bonos de discriminación positiva que elevan el Rᵢ de ciertas metas para reconocer su importancia en el marco de la Agenda 2030: Multiplicador de Género (× 1.15): aplicable a metas alineadas con el OD…
- `Metodología Integral SIAP-ICPI v2.4 (Maestra) (1).docx` — …(CPCCS): Rendición de cuentas y participación ciudadana. S10 (ODS): Alineación con la Agenda 2030 y bonos de discriminación positiva. CAPÍTULO III: EL MOTOR CANÓNICO Y LA MATEMÁTICA DEL ICPI 3.1. La Fórmula Maestra (Ref: H12) El núcleo del sistema es un modelo de suma de productos normalizado que ca…

### C3-09 · ¿Por qué `E_i` y `C_i` divergen donde divergen?

**En el libro:**

- `H01_PARÁMETROS` — Res.040-2025 — proceso exclusivo Grupo 7+8
- `H01_PARÁMETROS` — Res.040-2025 — proceso exclusivo LOSEP Art.52
- `H01_PARÁMETROS` — Res.040-2025 — proceso compartido con Dir. Administrativa (U-15)
- `H01_PARÁMETROS` — Res.040-2025 — proceso exclusivo Grupos 7+8

**En los documentos históricos:**

- `Metodologia_SIAP_ICPI.docx` — …s criterios exactos de calificación de cada componente, tal como están implementados en H13, son: 3.3.4. Eᵢ — Autonomía Orgánica Mide el grado de control que la dirección responsable tiene sobre la ejecución de la meta, considerando si depende de factores externos incontrolables. Se asigna manualmen…
- `Metodologia_SIAP_ICPI.docx` — …de devengado financiero certificado por el Ministerio de Economía y Finanzas sobre el presupuesto codificado. Autonomía Orgánica (Eᵢ): variable que mide el control del director sobre la ejecución de la meta. Valores: 1.0 autónomo, 0.9 compartido, 0.75 difuso. Calidad del Proceso (Cᵢ): variable que e…
- `Metodologia_SIAP_ICPI.docx` — …utonomía Orgánica (Eᵢ): variable que mide el control del director sobre la ejecución de la meta. Valores: 1.0 autónomo, 0.9 compartido, 0.75 difuso. Calidad del Proceso (Cᵢ): variable que evalúa la limpieza administrativa del expediente. Valores: 1.0 limpio, 0.9 regular, 0.75 ambiguo; reducción a 0.…

## ★ Dictamen de `011-C3` · las nueve, por grado de certeza

| # | Pregunta | Respuesta | Grado |
|---|---|---|---|
| **C3-01** | ¿quién y cuándo? | Javo Delgado Santana. El **concepto** existe al menos desde el **2026-03-25**; la versión **determinista**, el 27-abr-2026 | **DEMOSTRADO** |
| **C3-02** | ¿qué fenómeno? | **dos**, sucesivamente: imputabilidad orgánica → calidad jurídica del proceso | **DEMOSTRADO** |
| **C3-03** | ¿por qué de 5 a 6 factores? | **la pregunta estaba mal planteada**: la metodología ya tenía 6. Lo que cambió fue el mecanismo, no el número | **DEMOSTRADO** |
| **C3-03b** | ¿por qué se sustituyó el mecanismo? | — | ⬜ **NO DETERMINABLE** · ningún documento lo explica |
| **C3-04** | ¿por qué esos cuatro eventos? | la Sección L los declara «framework jurídico agnóstico» y escalable a otros países; **la razón de estos cuatro y no otros no consta** | **DECLARADO** parcial |
| **C3-05** | ¿por qué esos pesos? | no constan en la metodología —que no tenía deducciones—. El único precedente es `H95` `L-07`: los pesos del TGI son «**criterio experto (Dylus Lab)**, no PCA ni regresión» | ⬜ **NO DETERMINABLE** para `C_i` |
| **C3-06** | ¿por qué el piso `0,50`? | tampoco consta. Y **cambia el rango**: la escala original tenía mínimo `0,75` | ⬜ **NO DETERMINABLE** |
| **C3-07** | ¿por qué `Ci_Manual_2025` en 2026? | el instrumento declara que preserva el ICPI de referencia en estado vacío; **por qué 2025 puede representar 2026 no consta** | **DECLARADO** parcial |
| **C3-08** | ¿qué es `Ci_Adaptativo`? | definido, no conectado. Las cinco lecturas causales siguen abiertas | ⬜ **NO DETERMINABLE** |
| **C3-09** | ¿por qué `E_i` y `C_i` comparten escala y divergen? | **son dos ejes del mismo Estatuto**: quién ejecuta vs. quién responde. La superposición es deliberada y justificada | **DEMOSTRADO** · salvo cada asignación concreta, que es `NO DETERMINABLE` |

### Lo que `C3` cambia respecto de lo que se creía

| Se creía | Ahora consta |
|---|---|
| `C_i` se incorporó el 27-abr-2026 | el **concepto** es anterior; esa fecha data su **versión determinista** |
| `E_i` y `C_i` se superponen sin explicación | la superposición está **justificada en la metodología**: ejes distintos, escala común |
| las cuatro divergencias de `C2` eran anomalías sueltas | son **un solo fenómeno**: dos generaciones del factor conviviendo |
| `E_i` carece de biografía | tiene definición, fundamento (`COOTAD 54` · `NCI 200-04`), escala y **ejemplos de aplicación** |

### ⚠️ Y una corrección que `C3` le debe a `009` y a `D-014`

`011-C2` concluyó que **ninguna variable del ICPI contempla la entrega material**. La metodología obliga a matizarlo, y el matiz importa porque **rescata parcialmente la intuición de Javo, reubicándola**:

> `T_i` — Materialización Temporal — se define sobre el **devengado y no el compromiso**, y la metodología justifica esa elección así: el devengado exige «**factura válida, acta de entrega-recepción firmada e informe de conformidad del fiscalizador**» según el Acuerdo Ministerial 067 del MEF. Y lo dice con todas las letras: **«neutraliza una forma frecuente de gaming: reportar contratos firmados en diciembre como metas ejecutadas cuando la obra apenas comienza en enero»**.

Es decir: **la defensa contra el maquillaje de fin de ejercicio SÍ está en el constructo — pero en `T_i`, no en `C_i`**. Javo señalaba un mecanismo real; se equivocó de variable.

Ahora bien, la protección tiene un límite que hay que decir igual de claro:

| Nivel | Estado |
|---|---|
| El devengado **presupone normativamente** acta de entrega-recepción | ✅ Acuerdo 067 MEF |
| El motor **verifica de forma independiente** que esa acta exista | 🔴 **no** · lee la columna «Devengado» de la cédula eSIGEF |

> La protección es **normativa, no verificada por el motor**. Si una entidad devenga sin acta bien formada, el ICPI no puede detectarlo — confía en que el dato eSIGEF cumpla el Acuerdo 067.

Eso reformula `D-014`: no es que el constructo ignore la entrega material, sino que **la delega en la corrección del dato de origen**. Si esa delegación es suficiente lo juzga `011-C4`.

> ### GM-Ω-011-C3 — CERRADO COMO RECONSTRUCCIÓN CAUSAL
>
> Se estableció **qué se declaró, qué se implementó y qué alimenta efectivamente al ICPI**. La cadena está documentada hasta el mecanismo; **se corta en la razón**: por qué se sustituyó el constructo de `C_i`, por qué esos pesos y por qué ese piso **no constan en ninguna fuente**.
>
> Eso es un **resultado**, no una carencia del peritaje: la razón no está porque **nunca se escribió** (`DOC-022`), y las decisiones conversacionales no dejan rastro. Inventarla sería el error que `DOC-011` prohíbe.
>
> **No dictamina** si las transformaciones fueron correctas. `011-C4`.

---
*GM-Ω-ICPI-011-C3 · 123 hojas barridas · 15 documentos históricos · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
