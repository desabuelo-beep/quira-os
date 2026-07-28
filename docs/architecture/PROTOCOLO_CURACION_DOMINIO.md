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

- **R-F · La solicitud se rige por el ESTADO DE CONOCIMIENTO del universo documental.** *(Javo · 2026-07-29, precisado el mismo día.)*

  > **Pedirle un documento a un GAD es legítimo. Lo que NO es legítimo es pedir un dato que ya
  > sabemos que no existe** — porque entonces el GAD lo construye para responder, y ese documento
  > nace DESPUÉS de la pregunta: deja de ser evidencia de gestión y pasa a ser evidencia de
  > reacción a QUIRA.

  **La regla depende de si conocemos el universo documental del GAD, no del acto de pedir:**

  | # | Estado del universo | ¿Solicitar? | Fundamento |
  |---|---|---|---|
  | **1** | **CONOCIDO** · el documento **existe** pero está mal publicado *(POA en XLSX limpio, publicado en PDF escaneado)* | ✅ **sí** | recupera un documento **preexistente**; no crea nada |
  | **2** | **CONOCIDO** · el dato **no existe** *(Montecristi: el PP puntúa prioridad, no establece costo)* | ⛔ **no** | **induciría su creación** |
  | **3** | **NO CONOCIDO** · GAD sin documentos hallables en web ni en transparencia | ✅ **sí — es obligatorio** | **la solicitud es el instrumento que determina si estamos en el caso 1 o en el 2** |

  ### El caso 3 es el que hace escalable a QUIRA

  En un GAD cuyo universo documental **aún no conocemos**, no se puede saber si el documento
  existe y está mal publicado (caso 1) o si nunca se produjo (caso 2). **La solicitud es el único
  modo de averiguarlo — y su resultado es, en sí mismo, evidencia:**

  ```
  se solicita  →  entregan documento con fecha anterior  →  EXISTÍA: caso 1 · mide su publicación
               →  no entregan / silencio administrativo  →  evidencia de opacidad (IOC)
               →  entregan algo construido al momento    →  NO EXISTÍA: caso 2 · se anota y no se usa
  ```

  **Canal obligatorio:** la solicitud se cursa desde el **Observatorio QUIRA** o **QUIRA
  Ciudadana**, ejerciendo el **derecho de acceso a la información pública**. Nunca como QUIRA
  pidiéndole insumos al auditado: eso convertiría al GAD en proveedor y disolvería su condición
  de **sujeto observado** (BOOT §LA TESIS).

  ### Estado por GAD

  | GAD | Universo documental | Régimen |
  |---|---|---|
  | **Montecristi (001)** | ✅ **CONOCIDO y CERRADO** — se sabe qué documentos existen y cuáles no | **casos 1 y 2** · no se solicita lo inexistente |
  | **Los otros 221** | ❌ no conocido | **caso 3** · se solicita vía Observatorio cuando no haya documento hallable |

  **Hecho verificado sobre Montecristi (Javo · 15 años en gestión GAD):** los documentos de
  Presupuesto Participativo **puntúan la prioridad de cada obra o servicio, pero no establecen su
  costo económico**. No es una suposición sobre lo que el GAD tendría: es conocimiento del
  instrumento. Por eso `IGP_2 = 0` está **medido**, no pendiente.

  ### Por qué es regla y no criterio

  1. **Preserva la validez.** Medir lo que el GAD produjo ≠ medir lo que produce cuando se le pregunta.
  2. **Preserva la comparabilidad entre los 222 GAD.** El CVI solo compara si todos se miden por la
     misma superficie: **la evidencia pública realmente existente**.
  3. **Preserva al sujeto observado.** El canal (Observatorio · derecho de acceso) mantiene la frontera.

  **Complementa** al concepto *"el silencio como dato"*: aquél dice cómo **interpretar** una
  ausencia; éste dice cómo **no fabricarla ni destruirla**.

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
