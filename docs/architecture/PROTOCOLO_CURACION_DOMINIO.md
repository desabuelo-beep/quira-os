# PROTOCOLO DE CURACIÓN DE DOMINIO (PCD)

> **Doctrina (asesor + Javo · 2026-07-02):** No hacemos mantenimiento ni corregimos bugs.
> Hacemos **segunda ingeniería**: *auditar, curar y potenciar el ecosistema completo,
> empezando SIEMPRE desde el canon y siguiendo toda la cadena hasta la visualización final.*
> Se trabaja **dominio por dominio**, no pantalla por pantalla.

## 0 · El canon (fuente de verdad)
El canon NO es solo un archivo Excel. Es:
- **Gold Master (SIAP-ICPI v5.5)** — las **métricas** (ICPI/TGI/SAT, IPE, fidelidad `IF_n`, cumplimiento). Núcleo epistemológico del motor.
- **Corpus verificado (Supabase · SHA-256)** — los **documentos** (normativa, informes RDC, PDOT…).

Todo lo demás —snapshot, motores, cableado, UI, narrativa— **DERIVA** del canon. **Nunca inventa un segundo canon.**

## 1 · La cadena del dominio (nunca se saltan capas)
```
Gold Master / Corpus verificado
        │
        ▼
Auditoría metodológica  →  Corrección / potenciación del canon
        │
        ▼
Regeneración de dumps  →  Regeneración del snapshot
        │
        ▼
Motores matemáticos  →  Motores interpretativos (IA)
        │
        ▼
Cableado del cajón  →  Auditoría visual (UI/UX)
        │
        ▼
Patrón definitivo  →  PCD-DXX (documentación del dominio)
```

## 2 · La auditoría de 7 capas (reemplaza a "auditoría visual")
1. **Gold Master** — fórmulas · relaciones · consistencia · duplicados · métricas · lógica.
2. **Metodológica** — ¿la metodología sigue siendo la mejor? Si hoy sabemos algo mejor, se incorpora. **Nunca se rompe compatibilidad** (H12!B33 inmutable).
3. **Matemática** — ¿el indicador representa de verdad lo que dice? *No se acepta un proxy solo porque "funciona"* (caso IPE: ×0.84 → fórmula nativa `SUMAPRODUCTO`).
4. **Semántica** — nombres · conceptos · definiciones · relaciones · eliminar redundancias (Regla #7 anti-inflación).
5. **Cableado** — que la información viaje Excel/Corpus → Snapshot → Motor → Pantalla **sin pérdidas**.
6. **Visual (UI/UX)** — recién aquí entra la UI. No antes.
7. **Narrativa** — que el texto **explique** el dato (no adorne), a nivel de administración pública, con fundamento legal verificado.

## 3 · Reglas que nacen de este protocolo
- **R-A · Segunda ingeniería:** el propósito es *curar y potenciar todo*, no mantener.
- **R-B · Ningún cambio nace en Python.** Todo cambio **conceptual** (métrica, fórmula, definición) nace en el **canon** (Gold Master o corpus verificado). Python solo **implementa o deriva**. El código es reflejo del canon, jamás un segundo canon.
  *(Corolario: las cruces que "el Excel no cruza solo" —puentes de partidas, SERCOP— DERIVAN de datos del canon; no inventan verdad. Si una cruz se vuelve métrica de record, se estampa/formula en el canon, como el IPE.)*

- **R-C · Deslinde de dominios: el propietario califica, el consumidor solo usa.** *(Javo · 2026-07-29 — generaliza el precedente d07 de `TEORIA_EVIDENCIA_PUBLICA_VERIFICABLE.md`.)*

  > **El dominio propietario del instrumento evalúa la CALIDAD del instrumento; los dominios
  > consumidores solo evalúan su CAPACIDAD DE USO.**

  | Dominio | Rol frente a la evidencia | Qué califica |
  |---|---|---|
  | **d01 Planificación** | **propietario** del POA | el **CVI** del instrumento (estructura) |
  | **d07 Transparencia** | **publicador** | el **ICEP** de la publicación (formato) |
  | **d08 Participación** | **consumidor** | nada del instrumento — solo reporta **qué no pudo verificar** |

  **Por qué es una regla y no una preferencia:** sin ella, un dominio consumidor emite juicios
  sobre defectos que pertenecen a otro, y el mismo hallazgo termina duplicado —o contradicho—
  en dos dominios. Es **Subsidiariedad Normativa** (Carta Art. 1.2) aplicada a la frontera entre
  dominios: la regla vive en el nivel más bajo que la contiene por completo.

  **Caso que la originó:** OBS-020 nació en d08 (cruce demanda↔POA) pero su objeto es el POA,
  instrumento de d01. Anclaje corregido; d08 conserva solo el efecto (sus `sin_correlato`
  quedan explicados por causa externa).

- **R-D · Antes de corregir el motor, determinar de quién es la limitación.** *(extiende el
  Principio 6 · Autocuración Metodológica del Modelo Causal, mayo-2026.)*

  El ciclo original asumía que toda anomalía detectada era una limitación **del modelo**:
  `construir → observar → detectar limitación → documentar (C10) → mejorar`. Falta la
  bifurcación:

  ```
  el motor detecta una inconsistencia
        ↓
  ¿la limitación es del ALGORITMO o del INSTRUMENTO observado?
        ├── del algoritmo   → se corrige el motor (+ test de regresión)
        └── del instrumento → NO se corrige el motor: se MIDE y se registra
                              como hallazgo sobre el sujeto observado (CVI)
  ```

  **Evidencia de que la bifurcación hacía falta:** el cruce d08 se rompió cuatro veces. Las
  tres primeras eran del algoritmo (membrete · unidad ejecutora · homógrafo) y se corrigieron.
  La cuarta era del instrumento, y **corregirla habría sido el error**: parchar el programa
  presupuestario habría ocultado que el POA no localiza el gasto. Se midió en vez de parchar,
  y de ahí salió OBS-020.

- **R-E · Montecristi es el ÚNICO universo activo hasta cerrar el ecosistema.** *(Javo · 2026-07-29 — **"eso es ley"**.)*

  > **No se incorpora un segundo GAD sin haber terminado y validado empíricamente todo el
  > ecosistema en Montecristi.** Las réplicas quedan para cuando Montecristi esté cerrado, y
  > desde ahí se avanza **progresivamente** hacia los 222 GAD del país.

  | | |
  |---|---|
  | **Universo activo** | GAD Montecristi (`Municipio 001`) — POA 2023-2026 · actas PP · audiencias · contratos |
  | **Estado de los demás GAD** | ⛔ **fuera de alcance** — no se ingiere, no se mide, no se compara |
  | **Condición de apertura** | ecosistema Montecristi **cerrado y validado en las 7 capas** |

  **Por qué es regla y no preferencia:** un segundo municipio incorporado antes de cerrar el
  molde **multiplica el trabajo sin validar el método**. Montecristi no es un caso de estudio:
  es **el molde** (BOOT §LA TESIS). Un molde a medio construir replicado 222 veces produce 222
  errores, no 222 auditorías.

  > ⚠️ **Consecuencia sobre OBS-020 §10.** El protocolo de elevación del CVI mantiene sus 4
  > pasos, pero **el paso 2 (segundo GAD) queda BLOQUEADO por R-E**. La afirmación sobre el
  > *"instrumento nacional"* no solo requiere replicación: requiere **primero** cerrar
  > Montecristi. Ese hallazgo permanece como **C10 · incertidumbre estructurada**, sin fecha.

- **R-F · Las TRES vías canónicas de ingesta — solicitar es ejercer la norma, no contaminar el objeto.** *(Javo · 2026-07-29, corrige la versión anterior.)*

  > ⚠️ **CORRECCIÓN DE FONDO.** La primera R-F trataba la solicitud como *contaminación de la
  > muestra* — reactividad, efecto observador. **Ese marco no corresponde al objeto.** QUIRA no
  > realiza un experimento de laboratorio: **operacionaliza un derecho público**. El error fue de
  > la dirección técnica al adoptar un encuadre sociológico sobre un objeto jurídico.

  ### Fundamento normativo

  | Norma | Qué establece |
  |---|---|
  | **Constitución Art. 226** | principio de legalidad — en el sector público **solo se hace lo que la ley manda** |
  | **Constitución Art. 18** | toda información generada con recursos públicos es **pública** |
  | **LOTAIP** | fija el **procedimiento** de acceso: **10 días término + 5 de prórroga** |
  | **Acción constitucional de acceso** | si no entregan, la vía judicial **avala la exigencia** |

  **En los GAD no existe reserva de Estado.** La información reservada corresponde a seguridad
  nacional y fuerzas del orden. Todo expediente, acta, comprobante o plano municipal es documento
  público **de pleno derecho**. Pedirlo no es un favor: es ejercer una garantía.

  ### Las tres vías canónicas

  ```
                            EVIDENCIA PÚBLICA
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
  TRANSPARENCIA ACTIVA      SILOS INTERSISTÉMICOS      TRANSPARENCIA PASIVA
  portal GAD · LOTAIP       CPCCS · SERCOP · e-SIGEF   LOTAIP 10+5 · vía judicial
  (lo que publican)         (lo que reportan al Estado) (lo que están obligados a entregar)
  ```

  **Las tres son oficiales y legítimas.** QUIRA no espera a ver qué decide subir la secretaría al
  portal: agota las tres.

  ### Separación de planos: la Guía LOTAIP NO es canon QUIRA *(Javo · 2026-07-29)*

  Javo preguntó si el procedimiento de transparencia es trabajo operativo de d07. **No se
  equivoca: lo es.** Y de ahí se sigue una separación que debe quedar explícita para que el
  procedimiento legal no se confunda nunca con el procedimiento analítico.

  | Capa | Qué es | Quién la opera |
  |---|---|---|
  | **A · Jurídica** | Const. 18 · 226 → **LOTAIP** → **Guía Metodológica Integral LOTAIP 2024** *(en el corpus · es LEY del Estado)* | marco legal — **QUIRA no lo modifica ni lo interpreta** |
  | **B · Operativa** | ejecuta las 3 vías: portal · silos · **oficios LOTAIP 10+5** | **d07 Transparencia** |
  | **C · Analítica** | **no tramita oficios**: recibe la evidencia, verifica **trazabilidad del acto administrativo** y calcula CVI · ICEP · MRSPP | motor QUIRA |

  > **La Guía regula CÓMO SE SOLICITA. QUIRA regula CÓMO SE AUDITA lo obtenido.** Son planos
  > distintos y no se fusionan. Todo aporte metodológico que QUIRA cree se registra **diferenciado**
  > de la norma —nunca mezclado con ella— conforme al principio de legalidad (Const. 226).

  Es **R-C aplicado al canal de ingesta**: d07 es propietario del procedimiento de acceso; los
  demás dominios **consumen** la evidencia que ese canal produce.

  ### Lo que se controla no es SI se pide, sino cómo se califica lo que llega

  El riesgo del documento fabricado *ex post* **no se resuelve absteniéndose de pedir** — se
  resuelve verificando la **trazabilidad del acto administrativo**. Las tres respuestas posibles
  son evidencia:

  | Respuesta del GAD | Verificación | Estatus |
  |---|---|---|
  | entrega documento con **fe de presentación · fe de recepción · fe de acta · partida e-SIGEF · Gaceta**, de **fecha anterior** | consta el acto | ✅ **evidencia de gestión, 100% válida** |
  | entrega un borrador **sin respaldo formal** | no consta acto administrativo | ⚠️ **ausencia de habilitación formal** — no se usa como dato |
  | **vencen los 10 + 5 días sin entregar** | plazo legal incumplido | ❌ **opacidad crítica + incumplimiento LOTAIP**, con respaldo legal |

  > **La fecha del acto administrativo es el discriminador objetivo** — no una suposición sobre
  > intenciones. Eso es lo que preserva la integridad sin renunciar al derecho.

  ### Lo único que sobrevive de la versión anterior

  **No se pide lo que ya se sabe inexistente por conocimiento verificado del instrumento** — no
  porque contamine, sino porque es **redundante**. Caso Montecristi/PP: se conoce que el
  instrumento puntúa prioridad y no fija costo.

  > ⚠️ **Y aun así, solicitarlo MEJORARÍA el hallazgo.** Una respuesta oficial del GAD declarando
  > que el PP no desagrega montos convierte el hallazgo de *inferido documentalmente* a
  > **declarado oficialmente**. Es una decisión de oportunidad de Javo, no un impedimento
  > metodológico. Ver la nota sobre la condición 2 del UDC más abajo.

  **Complementa** al concepto *"el silencio como dato"*: aquél dice cómo **interpretar** una
  ausencia; éste dice **por qué vías se agota la búsqueda antes de declararla**.

  ---

  ### R-F.1 · UDC — Universo Documental Cerrado *(definición operativa · asesoría 2026-07-29)*

  Un universo entra en **UDC** solo cuando se cumplen las **tres condiciones verificables**:

  | # | Condición | Verificación |
  |---|---|---|
  | 1 | **Transparencia activa agotada** | portal LOTAIP auditado y procesado |
  | 2 | **Transparencia pasiva agotada** | solicitud cursada y **respondida, o vencido el plazo 10+5** |
  | 3 | **Silos intersistémicos agotados** | CPCCS · SERCOP · e-SIGEF revisados · sin repositorios pendientes |

  **Las tres condiciones son las tres vías de R-F.** Alcanzado el UDC, toda información no hallada
  **deja de buscarse** y se registra como *ausencia documental* o *limitación del instrumento*.

  > **Distinción que el UDC vuelve operable:** *ausencia de evidencia* (universo cerrado, el dato
  > no existe) ≠ *evidencia no encontrada* (universo abierto, aún no se agotaron las vías).
  > Confundirlas es afirmar un hallazgo sobre un vacío de método.

  #### Dos niveles: UDC-I (operativo) y UDC-G (derivado) *(asesoría · 2026-07-29)*

  El UDC **no es binario por municipio**. Se declara en dos niveles jerárquicos, y el segundo se
  **deriva** del primero por conjunción — no por juicio:

  | Nivel | Qué es | Cómo se declara |
  |---|---|---|
  | **UDC-I** *(Instrumento)* | estado **operativo** de cada instrumento: POA · PP · actas · LOTAIP… | se verifica contra las 3 condiciones |
  | **UDC-G** *(GAD)* | estado **derivado** del municipio | `UDC-G = UDC-I₁ ∧ UDC-I₂ ∧ … ∧ UDC-Iₙ` |

  > **UDC-G es verdadero si y solo si TODOS los instrumentos obligatorios cumplen UDC-I.** No es
  > una apreciación: es una conjunción booleana. Eso elimina toda declaración prematura de cierre.

  **Por qué importa el cambio:** convierte un concepto binario en uno **gradual y medible**. La
  pregunta deja de ser *"¿el GAD está cerrado?"* y pasa a ser **"¿qué instrumentos siguen
  abiertos?"** — que sí permite medir progreso.

  ### Tablero UDC · Montecristi (`GAD-001`) — revisado 2026-07-29 tras la corrección de R-F

  > ⚠️ **Este tablero BAJA de nivel respecto de la versión anterior, y es correcto que baje.**
  > Al incorporar la transparencia pasiva como condición 2, el estándar se volvió **más
  > exigente**: no basta con tener los documentos que el GAD publicó. **Hay que haber agotado las
  > tres vías.** Varios ✅ anteriores se apoyaban solo en la vía 1.

  | Instrumento | Vía 1 activa | Vía 2 silos | Vía 3 pasiva | UDC-I | Nota |
  |---|:---:|:---:|:---:|:---:|---|
  | **POA 2023-2026** | ✅ 4 XLSX nativos | ✅ | **n/a** | ✅ | sin vacío pendiente: la vía 3 no tiene objeto |
  | **Cabildo popular** | ✅ | ✅ | **n/a** | ✅ | universo conocido, sin vacío |
  | **Presupuesto Participativo** | ✅ actas completas | ✅ | ❌ **no cursada** | ⚠️ | **vacío conocido**: desglose de montos |
  | **Audiencias públicas** | ✅ 28/28 actas | ✅ | ❌ **no cursada** | ⚠️ | **vacío conocido**: resoluciones Art. 75 |
  | **Portal LOTAIP / transparencia** | ❌ d07 abierto | — | — | ❌ | instrumento sin auditar |
  | **Actas de sesión del Concejo** | ❌ | — | ❌ **no cursada** | ❌ | no obran en nuestro poder |
  | **Holding municipal** | ❌ | ❌ | ❌ | ❌ | repositorios no localizados |
  | **`GAD-001` conjunto** | | | | **❌ UDC-G = FALSO** | 4 / 12 dominios cerrados |

  **`n/a`** = no aplica porque **no existe vacío documental que solicitar**. La vía 3 se exige solo
  cuando las vías 1 y 2 dejan un hueco identificado.

  ### ★ La vía 3 YA fue ejercida en Montecristi — y el oficio no cubre lo que se supuso

  **`OFICIO N.º 0143-2026-SG-JAMZ-GADMCM`** · leído íntegro 2026-07-29.

  | Campo | Contenido verificado |
  |---|---|
  | **Solicitud** | Oficio S/N de **10-feb-2026** · Ronald Javier Delgado Santana |
  | **Respuesta** | **17-mar-2026** · Abg. Jonathan Alfredo Mero Zamora, Secretario General y de Concejo |
  | **Vía interna** | MEMORANDUM 0511-CNCV-DF-GADMCM-2026 · Ing. Carlos Vélez Cedeño, Director Financiero |
  | **Lo entregado** | *"documentación correspondiente al **numeral 2** del requerimiento: **cédulas presupuestarias de gastos reportadas al Ministerio de Economía y Finanzas, periodos fiscales 2023 y 2024**"* |
  | **Adjuntos localizados** | ✅ `Cedulas Presupuestarias 2023-2026/Presupuestos 2023|2024/*.xls` |

  #### Tres correcciones al tablero propuesto por la asesoría

  | Afirmación | Veredicto |
  |---|---|
  | *"Presupuesto Participativo (Vía 1 + Vía 3)"* | ❌ **falso** — el oficio entrega **cédulas presupuestarias**, instrumento de **d02**. No menciona PP |
  | *"Audiencias públicas cubiertas"* | ❌ **falso** — no aparecen en el oficio |
  | *"ICD ≈ 50%"* | ❌ **no se sigue** — el oficio cierra un instrumento de d02, no dos de d08 |

  **Lo que el oficio SÍ acredita, y es valioso:**

  1. **La vía 3 funciona en Montecristi.** Existe precedente de solicitud cursada y **respondida con
     entrega documental**. Deja de ser hipótesis operativa.
  2. **Cédulas presupuestarias de gastos 2023-2024** → instrumento de **d02** con **vía 3 ejercida y
     satisfecha**, con trazabilidad completa: número de oficio · fecha · firma electrónica ·
     memorando interno · dirección responsable. Es el estándar de prueba más alto disponible.

  #### Dos observaciones que el oficio abre — ninguna afirmable todavía

  - **Respuesta parcial.** El texto dice *"correspondiente al **numeral 2** del requerimiento"*, lo
    que implica que el requerimiento tenía **más numerales**. Los demás **no constan respondidos en
    este oficio**. ⚠️ **No se puede evaluar la completitud sin la solicitud original**
    (Oficio S/N de 10-feb-2026), que **no obra en el repositorio**. Es documento de Javo, no del GAD.
  - **Plazo aparentemente excedido.** Del 10-feb al 17-mar median ~25 días término, frente a los
    **10 + 5** que fija la LOTAIP. ⚠️ **Verificable por d07**, no afirmable aquí: habría que
    descontar feriados y comprobar si hubo prórroga notificada.

  ### Tablero UDC actualizado con el oficio

  | Instrumento | Vía 1 | Vía 2 | Vía 3 | UDC-I |
  |---|:---:|:---:|:---:|:---:|
  | **Cédulas presupuestarias 2023-2024** (d02) | ✅ | ✅ | ✅ **oficio 0143-2026** | ✅ **cerrado con respuesta oficial** |
  | POA 2023-2026 · Cabildo popular | ✅ | ✅ | n/a | ✅ |
  | Presupuesto Participativo | ✅ | ✅ | ❌ | ⚠️ vacío: desglose de montos |
  | Audiencias públicas | ✅ | ✅ | ❌ | ⚠️ vacío: resoluciones Art. 75 |
  | Portal LOTAIP · Actas de Concejo · Holding | ❌ | — | ❌ | ❌ |

  **`ICD = 3 / 8 ≈ 38%`** *(cédulas, POA y cabildo cerrados)*. **UDC-G = FALSO.**

  ### ICD · Índice de Cierre Documental *(asesoría · 2026-07-29)*

  El UDC-G es booleano y no permite ver avance. Se añade una medida **continua** que no lo
  sustituye:

  ```
  ICD = instrumentos con UDC-I / instrumentos totales
  ```

  **Montecristi hoy: ICD = 2/7 ≈ 29%** *(POA y cabildo cerrados; PP y audiencias parciales)*.
  Sirve para gestionar el avance sin relajar el criterio lógico de cierre.

  > **R-E y UDC no se sustituyen.** R-E fija *dónde se trabaja* (solo Montecristi). El UDC fija
  > *cuándo una ausencia puede afirmarse*. Montecristi es el único universo activo **y** conserva
  > instrumentos abiertos: es exactamente la situación de hoy.

*(Ratificación de R-A/R-B como Reglas de Oro en `CLAUDE.md` / `BOOT.md`: pendiente de Javo — son archivos congelados, Regla 5.)*

## 4 · Plantilla PCD-DXX (cada dominio cierra con su documento)
Cada cajón termina con `docs/pcd/PCD-DXX_<Dominio>.md`, con secciones:
- **Estado inicial** — cómo estaba el dominio.
- **Hallazgos** — lo que la auditoría de 7 capas reveló.
- **Cambios** — metodológicos · matemáticos · semánticos · visuales · narrativos.
- **Cambios en el canon** — Gold Master (hojas/fórmulas) · Corpus · Snapshot · Motores · UI.
- **Validación** — verificación (dumps, gates B33/guardián, Excel↔Python, render, firewall).
- **Estado final** — cómo quedó, y por qué quedó exactamente así.

Objetivo: que dentro de un año cualquiera pueda responder *"¿por qué este dominio quedó así?"* con trazabilidad completa.

## 5 · Estado de aplicación
| Dominio | PCD | Estado |
|---|---|---|
| d01 Planificación | [`PCD-D01`](../pcd/PCD-D01_Planificacion.md) ✅ redactado | Cerrado de cabo a rabo · IPE nativo en Excel |
| d09 Rendición de Cuentas | [`PCD-D09`](../pcd/PCD-D09_Rendicion_Cuentas.md) ✅ redactado | Cerrado · 7 capas · fix cableado `cpccs.fecha_rdc` · canon sin cirugía (sin artefacto) |

---
*Protocolo de Curación de Dominio · Dylus Lab © 2026 · asesor externo + Javo + Claude (director técnico).*
