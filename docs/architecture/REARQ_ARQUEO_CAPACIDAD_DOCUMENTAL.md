---
id: REARQ-ARQUEO-001
authority:
  parent: REARQUITECTURA_QUIRA
  constitution_articles: [1, 2, 3, 9]
  type: ARQUEO
status: CONGELADO — preservación activa
fecha: 2026-09-09
---

# REARQ · Arqueo de la capacidad documental de Transparencia

> ## Principio de esta parte del expediente
>
> **La capacidad documental de Transparencia no se considera una capacidad perdida ni
> inexistente. Su existencia está demostrada por artefactos normativos, metodológicos,
> computacionales y documentales preservados. La cuestión abierta de `REARQ` no es su
> existencia, sino su residencia arquitectónica, grado de completitud, escalabilidad y
> eventual reutilización transversal.**

Este documento existe porque la Rearquitectura estuvo a punto de tratar como vacío algo que
llevaba semanas construido. Se registra el arqueo para que **no vuelva a ocurrir**.

## 1 · La secuencia obligatoria

```
ARQUEO → PRESERVACIÓN → RECONCILIACIÓN → DISEÑO REARQ → MIGRACIÓN
```

**Nunca al revés.** No se alinea un artefacto histórico con un diseño que todavía no existe.
Primero se establece qué hay, luego se protege, luego se reconcilia con el canon, y sólo
entonces se diseña. La migración es lo último.

## 2 · Artefactos protegidos · NO SE TOCAN

Hasta completar `RECONCILIACIÓN`, estos artefactos no se modifican «para alinearlos» con
`REARQ`. Se leen, se citan y se preservan.

| Artefacto | Naturaleza |
|---|---|
| `docs/pcd/PCD-D07_Transparencia.md` | expediente de curación · `EN CURACIÓN` |
| `docs/architecture/gm_dumps/H09_S7_TRANSPARENCIA_LOTAIP.md` | silo del motor |
| `docs/architecture/gm_dumps/H70_BITACORA_LOTAIP_OPACIDAD.md` | bitácora de opacidad |
| `docs/architecture/gm_dumps/H41_IOC_OPACIDAD_CRITICA.md` | índice de opacidad |
| `scripts/holding/ingest_lotaip.py` | ingestor |
| `quira_pages/p07_transparencia.py` | superficie del dominio |
| `docs/observations/OBS-009_Divergencia_SIGAD_LOTAIP_GAD_MCR.md` | observación `S6`↔`S7` |
| `data/lotaip/**` | **1.748** archivos · de ellos **936** en `descargas/` |
| `data/vault_backup_p2/02_NORMATIVA/11_LOTAIP` · `12_REGLAMENTO_LOTAIP` · `13_GUIAS_LOTAIP` | fuente del criterio |

## 3 · Lo que queda DEMOSTRADO por el arqueo

**1 · Existe el expediente específico**, y es el mayor del proyecto: 26.388 bytes, 440 líneas,
declarado `EN CURACIÓN` a propósito.

**2 · Existe evidencia documental real, no una especificación.** Inventario del 2026-08-18 con
**417/417 enlaces inspeccionados y cero fallos de red**:

```
417   enlaces publicados accesibles
        391  archivos individuales
         26  contenedores  →  935 artefactos dentro
──────────────────────────────────────────────
1.326  objetos físicos observados     el balance cuadra
```

Naturaleza determinada **por firma del archivo, no por su extensión**: 267 PDF · 123 imágenes ·
26 contenedores · 1 sin identificar. Trazabilidad por `SHA-256`. Identificación de escaneados:
**10 PDF únicos**, no las cifras infladas que produjeron los conteos anteriores.

**3 · Existe la norma técnica como fuente del criterio, con su SHA.** El *Instructivo para
evaluar el nivel de cumplimiento de los parámetros técnicos de la transparencia activa* (DPE
2024). La matriz del Anexo 1 vive en `matriz_calificacion.json` **con el SHA del Instructivo**, y
los parámetros llegan al motor desde la RO, nunca desde el código (`Regla de Oro 9`).

**4 · Existe el motor de evaluación**, auditado parámetro por parámetro contra el Instructivo:

| | Resultado |
|---|---|
| `SITA = (CTA+ETA+RP+CI)/4` | idéntico ✅ |
| `CTA` · `ETA` · `RP` | idénticos ✅ |
| `CI` | ⛔ el motor exigía los 3 parámetros a los 24 numerales; el Anexo 1 los asigna numeral por numeral → **corregido** |

Resultados: `SITA 2025 · 0,4646` · `SITA 2026 (ene-may) · 0,8382`. Base: 4 CNO · 46/46 SHA · 5 RO
· 936 archivos de evidencia con SHA · 36 pruebas de regresión.

**5 · Existe la separación metodológica** entre construir el canon de evaluación, ejecutar la
captura periódica, procesar evidencia y evaluar cumplimiento. Fijada por Javo el 2026-08-19:

> *«Claude no es QUIRA. Estamos construyendo un ecosistema que deberá reportar más adelante 222
> municipios, sin Claude, solo QUIRA.»*

> **Construcción del canon ≠ capacidad operativa.** La primera corre una vez, bajo criterio
> humano, y su producto se sella con SHA — *un sistema que reejecuta la extracción de su propia
> vara puede cambiarse el patrón con el que mide*. La segunda corre cada mes, en 222 municipios,
> sin nadie mirando.

**6 · Existe la opacidad como resultado analítico**, no como juicio político. El `IOC` ya está en
el motor (`H41`, 17,71 %). Y el ranking futuro es **compatible con la arquitectura**, bajo tres
reglas ya escritas:

| Norma | Qué establece |
|---|---|
| `ADR-024` | el Radar Nacional **es el producto principal** — 222 GAD · semáforo · ranking |
| `ADR-041` | exige el estado **`sin ciclo comparable`**: un GAD sin histórico *«aparecería con los peores indicadores por una razón que no tiene que ver con su gestión»*. Se registra, se muestra, **no se computa** |
| `ADR-043` | prohíbe el ranking **ideológico** y el juicio político — no el ranking de evidencia |

**7 · La ausencia de evidencia está tratada metodológicamente.** Un archivo que no puede
procesarse **no se convierte artificialmente en incumplimiento**:

- `Ordenanzas.zip` supera 500 MB → `cortado_por_tope_de_tamano` = *«captura incompleta del
  observador, jamás ausencia del sujeto obligado»*
- Numeral 10: 8 enlaces devuelven 404; se falsó el instrumento primero; los 7 restantes quedan
  **sin verificar**, no «inaccesibles»
- `RO-VII-005` nace `no_observable` — requiere otra fuente, no otro cálculo
- `RO-VII-004` sin solicitudes: *«no hay incumplimiento: hay ausencia de ejercicio del derecho»*

Este punto 7 es doctrina general de QUIRA, no un detalle de d07.

## 4 · La pregunta `REARQ` correcta

El problema **ya no es** «QUIRA no tiene capa de adquisición documental». La tiene, para LOTAIP.
La pregunta es otra:

> **¿La capacidad documental construida para Transparencia es sólo un componente de su dominio,
> o es el primer caso implementado de una capacidad transversal que otros dominios deben
> reutilizar?**

Porque un mismo documento institucional puede producir **múltiples evidencias para múltiples
dominios**:

```
Portal LOTAIP → documento → captura → SHA → extracción → verificación → evidencia canónica
                                                                            │
        ┌───────────────┬───────────────┬──────────────┬────────────────────┤
   Transparencia   Participación   Rendición de    Planificación      Gobernanza
   cumplimiento      actas y        cuentas         instrumentos       mandato
   y opacidad      mecanismos      informes        de planificación
```

La evidencia documental **no debería capturarse cinco veces porque cinco dominios la necesitan.**

### La finalidad, declarada por la dirección · 2026-09-09

> *«El dominio de Transparencia alimentará a los demás dominios de manera mensual. Pero para la
> construcción no hemos conectado: hemos construido dominio por dominio, sin conectar totalmente
> el ecosistema. De esa manera hemos estado trabajando todo este tiempo. Es una práctica no
> buena, y por eso —y todo lo demás— salió la idea de toda esta Rearquitectura y las auditorías
> previas: para tener un ecosistema totalmente eficiente en todo nivel y sentido.»*

Esto fija tres cosas que el arqueo no podía establecer por sí solo:

| | |
|---|---|
| **la cadencia** | **mensual** — no es una carga inicial, es un flujo recurrente |
| **la dirección** | de d07 **hacia** los demás dominios |
| **el diagnóstico de partida** | los dominios se desarrollaron **uno por uno, sin implementar las conexiones del ecosistema** |

Es un **requisito arquitectónico** que viene de la dirección del proyecto, no una hipótesis que
haya que descubrir en el código. Y la formulación que se conserva es la acotada:

> **La construcción histórica en silos constituye una condición de partida de `REARQ`: las
> capacidades de los dominios se desarrollaron sin implementar todas las conexiones interdominio
> que la arquitectura objetivo requiere. `REARQ` debe determinar y diseñar esas interfaces,
> dependencias, contratos de intercambio y cadencias.**

> ### ⚠️ Lo que NO se afirma
>
> Que los huecos hallados sean «todos el mismo síntoma». Sería convertir una declaración de
> diseño en explicación retrospectiva de cada defecto, y **eso no está demostrado**. Cuáles
> conexiones se previeron, cuáles se implementaron y cuáles nunca existieron es trabajo de
> arqueología —`Q-M2`—, no de inferencia desde esta cita.

### ★ Y la arqueología ya empezó a responder: las conexiones existen

Verificado el 2026-09-09, contra el código y el canon:

| evidencia | qué demuestra |
|---|---|
| `ADR-017` diseñó los circuitos `C01`, `C02`, `C03` | las interfaces **se previeron** |
| `ADR-026` **confirma `C01` en código** | y se **implementaron**, al menos una |
| `p07_transparencia.py:82-113, 118-139` — `_C01_NODES`, `_calcular_chs_c01()` | **d07 es ORIGEN del circuito**, con regla de colapso activa: *«Dom07 ORIGEN falla → CHS_C01 = 0.0»* |
| `ADR-026:455` | cadencia de d07 ya declarada: **«Mensual (publicación LOTAIP)»** |
| `ADR-026:104` | **d08** es «nodo de unión · mayor conectividad» — `IGP→D06`, `D08→D09` |
| `ADR-026:118` | **d06** «lee explícitamente de otros dominios»: `IGP` de d08, `IOC` de d07, `IET` de d10, `ISP` de d04/d02 |
| `ADR-026` · d09 | su checklist «referencia exclusivamente métricas de otros dominios» |

⚠️ **Cero imports cruzados entre `app/agents/dXX/`**, y las menciones de un dominio en otro son
docstrings. Las conexiones existentes **no viven en los agentes**: viven en el motor, en el canon
y en la capa de superficie. Dónde deben vivir es pregunta de `RECONCILIACIÓN`.

Y queda una tensión registrada, sin resolver: la dirección señala que las relaciones
interdominio están «entre los dominios creados antes de Transparencia», mientras `ADR-026`
documenta a d07 como origen de `C01`. Puede que ambas sean ciertas —d07 **emite** y no
**consume**— pero **el nombre no lo demuestra** y hace falta el inventario completo.

## 4-bis · ⛔ CORRECCIÓN MAYOR · d07 no es el proveedor universal

*(Javo, 2026-09-09, corrigiendo el planteamiento de este arqueo.)*

> *«No sólo es el dominio de transparencia el que alimenta. También el portal del CPCCS, con el
> informe de rendición de cuentas (anual); y el monitoreo del portal de SERCOP (mensual). Y quizá
> la página institucional de los GAD, para buscar PDOT, orgánico, POA, PAC y Presupuesto en sus
> formatos institucionales, fuera de los formatos determinados por transparencia.»*

Eso invalida la formulación «d07 alimenta a los demás dominios». La correcta:

> **QUIRA observa el Estado desde MÚLTIPLES fuentes institucionales externas. Transparencia es una
> de ellas —hoy la más desarrollada—, no la única ni necesariamente la principal.** Cada fuente
> produce evidencia potencialmente reutilizable; cada dominio conserva su propia interpretación
> metodológica.

Y el objeto de estudio deja de ser la relación entre dominios: es **cómo circula la evidencia**.
Las fuentes observan · la evidencia circula · los dominios interpretan · el Gold Master fija el
estado canónico.

### ⛔ El nombre del silo NO es su vía · cinco dimensiones, no dos

*(Modelo del colega, 2026-09-09, tras el caso `S5`.)* Una fuente no es una etiqueta: es una
**cadena de procedencia**. Confundir el sistema donde nace el dato con la puerta por donde QUIRA
lo obtiene es lo que produjo el error de `S5`.

```
SISTEMA DE ORIGEN → CANAL DE ADQUISICIÓN → ARTEFACTO OBSERVADO
                  → EVIDENCIA CANÓNICA → DOMINIO → REUTILIZACIÓN
```

### La matriz, verificada contra el disco el 2026-09-09

Estados: `DECLARADO → IMPLEMENTADO → CONECTADO → OPERATIVO → REUTILIZADO → PROBADO`

| Silo | Sistema de origen | Canal de adquisición | Artefacto · evidencia canónica | Cadencia | DOM | Estado |
|---|---|---|---|---|---|---|
| `S7` | GAD reporta al Comité de Transparencia | **① Portal DPE** `capturar_lotaip_dpe.py` → `dpe_montecristi.json`<br>**② Portal del GAD** `capturar_lotaip_portal.py` → `portal_montecristi.json` | 1.748 archivos · 1,8 GB · `artefactos/*.bin` **direccionados por hash** | **mensual e incremental** | d07 | **PROBADO** — 9 etapas con gates · 3 corridas selladas · 36 pruebas |
| `S4` | SERCOP | Portal SERCOP **OCDS** · `connectors/sercop.py` + 3 scripts | `data/scouting/` — 5 JSON | **mensual** | d03 | IMPLEMENTADO · operatividad **por verificar** |
| `S8` | CPCCS | Portal CPCCS · `connectors/cpccs.py` · `fetch_rdc_cpccs.py` | RDC en `motor_narrativo/` + normativa en vault | **anual** | d09 | IMPLEMENTADO · d09 cerró con este insumo |
| `S5` | **eSIGEF** — ⛔ caja negra, sin canal público | ① LOTAIP (`CD-06`) · ② transparencia **pasiva** (`OFICIO 0143-2026`) · ③ carga al Gold Master | cédula presupuestaria · `H07` | según publicación | d02 | OPERATIVO **por vía indirecta** |
| `S2`·`S3` | GAD (PDOT · POA) | por determinar | `data/pdot/` — 10 archivos · 1,1 MB | — | d01 | IMPLEMENTADO parcial |
| `S3b` | GAD · SERCOP | por determinar | — | — | d03 | DECLARADO |
| `S8b` | GAD (presupuesto participativo) | por determinar | actas en `ProyecT/` | — | d08 | IMPLEMENTADO parcial |
| `S1` | CNE | por determinar | `data/contraste_cne/` — 3 archivos | por ciclo electoral | 🔴 **sin curador** | DECLARADO |
| `S6` | SIGAD (autorreporte) | ⛔ ninguno | — | — | 🔴 **sin curador** | `ICM` no se calcula · `SAT-I` apagada |
| `S9` | Agenda ODS | ⛔ ninguno | — | — | 🔴 **sin curador** | DECLARADO |
| — | GAD · **web institucional** (PDOT · orgánico · POA · PAC · presupuesto en formato propio) | ⛔ **sin conector** — `despacho.py:108` · sólo se usa para contrastar LOTAIP | — | variable | varios | **DECLARADO SIN CONECTOR** · 4 agentes en Fase 4 |
| — | GAD · **respuesta a solicitud** (transparencia pasiva) | oficio ciudadano o de Dylus · `ADR-045 §4` **exigibilidad asistida** | `OFICIO 0143-2026` · cédulas 2023-2024 | eventual | d07 · d02 | IMPLEMENTADO como **precedente**, no como capacidad |
| — | **Aporte ciudadano** — QUIRA Ciudadana | ⛔ sin formulario construido · `ADR-046 §2` le da nombre y lugar | documentos, actas, fotos, geolocalización | eventual | todos | **CANON · 3 de 4 capacidades declaradas, sin superficie** |

### ★ `S7` ya tiene DOS canales, y la doctrina que los distingue

No es una hipótesis: está implementado y decidido. Javo, 2026-08-17, en el propio capturador:

> *«La evaluación de LOTAIP no se debe hacer desde la web del GAD, sino desde transparencia de la
> DPE. Ése es el reporte que ellos hacen con los filtros del Comité de Transparencia, que es quien
> avala la información que se reporta mensualmente.»*
>
> *«El repositorio del propio municipio sirve para **contrastar**; el acto sujeto a control es el
> que se registra ante la Defensoría del Pueblo. **Evaluar la copia en lugar del acto era medir el
> lugar equivocado.**»*

    canal ①  Portal DPE      →  el ACTO sujeto a control     →  se EVALÚA
    canal ②  Portal del GAD  →  la COPIA publicada           →  se CONTRASTA

Y al capturar el canal ② se descubrió que el portal del GAD sirve **dos orígenes distintos**:
`localYears 2019-2024` desde el propio GAD (`api/local-year.php`) y **2025-2026 desde la DPE**.
Un mismo portal, dos procedencias.

> ⚠️ **Y lo que NO se afirma.** Se escribió que esto era ya «triangulación documental» como
> capacidad general. **Se retira**: lo demostrado es que existen dos canales técnicamente
> diferenciados con doctrina de uso para la evaluación de transparencia. Que un artefacto del
> canal ① y otro del ② sean el mismo objeto, versiones distintas o evidencias complementarias
> **hay que determinarlo caso por caso** — con `NO DETERMINABLE` como salida legítima.
>
> Tampoco se eleva «DPE = original · GAD = copia» a regla ontológica. Es doctrina **de
> evaluación**, no de identidad documental.

### ⛔ Y la web del GAD NO es sólo el contraste de LOTAIP

*(Javo, 2026-09-09, insistiendo sobre una lectura estrecha de este arqueo.)*

> *«La web del GAD no es sólo para verificar si LOTAIP está bien, sino que nos sirve para sacar
> los documentos de PDOT, POA, PAC, Presupuesto, orgánico, y todos los otros documentos oficiales
> que no salgan de transparencia.»*

`capturar_lotaip_portal.py` la usa **para un solo fin**: contrastar la publicación LOTAIP. Eso es
un uso de la web institucional, **no su alcance**. Los cuatro agentes en Fase 4 —`PDOT`, `POA`,
`PAC`, `Resultado`— ya la declaran como entrada para documentos que **no pasan por transparencia**.

> **Es el canal de los documentos en formato institucional propio**, y hoy es el único identificado
> para los silos `S2`, `S3`, `S3b` y `S8b`, que la matriz tiene «por determinar».

### ★ El CANAL CIUDADANO · tercera vía, y ya es canon

*(Javo, 2026-09-09.)*

> *«Los ciudadanos, para realizar sus análisis, pueden subir sus documentos oficiales; y también
> pueden solicitar vía solicitud de transparencia al GAD para que este les entregue vía digital,
> para que QUIRA revise las firmas, sellos y, con la info, pueda realizar los análisis del
> ciudadano. Y a su vez esta info se queda con QUIRA para ampliar su labor a más municipios, con
> la ayuda de los ciudadanos.»*

Está **entero en `ADR-046`**, del 2026-08-10, con base legal:

| capacidad cívica | qué hace | estado |
|---|---|---|
| **Evidencia territorial** | documentos, actas, fotografías y geolocalización → evidencia estructurada y trazable | canon · `ADR-045 §3` |
| **Exigibilidad asistida** | **redacta el oficio, corre el cronómetro**, prepara el escalón siguiente | canon · `ADR-045 §4` |
| **Inteligencia cívica** | los 12 dominios legibles sin jerga | canon · `ADR-023` |
| **Acción territorial** | incidencia, control social, formulación de proyectos | admitida, sin construir |

Y las firmas y sellos que la dirección menciona tienen tabla y fundamento —`COA Art. 94`
(`SHA256 d306997e…`) · `LCEFEMD Art. 44` · `NCI-CGE` (`SHA256 37f338e2…`):

| qué es el documento | techo |
|---|---|
| acto con **firma electrónica certificada** por entidad acreditada | **institucional** |
| acto con **firma física y sello**, digitalizado | **institucional** |
| comunicación desde dominio institucional **sin firma** | institucional, **con reserva declarada** |
| evidencia propia del aportante (foto, factura, testimonio) | **parcial**, hasta corroborar |

### ★★ La regla que zanja la pregunta abierta · `ADR-046 §1`

La duda era si el canal determina lo que la evidencia acredita. **El canon ya lo resolvió, y en
sentido contrario:**

| | qué responde | qué determina |
|---|---|---|
| **Custodia** | ¿qué presenció QUIRA de la adquisición? | la **trazabilidad del ingreso** |
| **Acreditación** | ¿qué acredita el documento en sí mismo? | **el techo de verificabilidad** |

> **«Lo que se verifica es el certificado, no el portador. Un acto de la administración no deja de
> serlo porque lo entregue un vecino en vez de un scraper.»**

Luego DPE, web del GAD, vía pasiva y aporte ciudadano son **custodias distintas del mismo eje**, y
ninguna fija por sí sola el valor de la evidencia. Las tres custodias de `ADR-045 §3` —**captura
directa · adquisición asistida · aporte directo**— ya son el modelo de canales que esta matriz
estaba reconstruyendo.

### Y la respuesta a la escalabilidad de los 222, que también estaba escrita

> **«QUIRA observa 222 GAD, pero sólo calcula sobre lo que existe. Un municipio que no publica
> tiene sus doce dominios vacíos. Quien aporta la evidencia de su municipio enciende la lectura de
> su propio territorio.»** *(`ADR-046 §2.4`)*

Con la consecuencia de diseño ya declarada: *«la ciudadanía puede activar su cantón — que es la
**única vía realista** de llegar a 222 sin depender de la voluntad de 222 alcaldías»*.

Y la salvaguarda del §2.5, que impide el atajo perverso:

> **Que la ciudadanía llene el hueco no absuelve al GAD de haberlo dejado.** Cuando una evidencia
> entra por aporte ciudadano supliendo una publicación ausente, **el `IOC` sigue registrando que el
> GAD no publicó**. El dominio se enciende; el incumplimiento no se borra.

### Lo que esto corrige de este mismo arqueo

Se escribió que LOTAIP era **«la única puerta pública»** para la evidencia financiera. **Es
falso**, y se retira: existen al menos tres canales —LOTAIP, web institucional y transparencia
pasiva— y el propio LOTAIP tiene dos. La formulación correcta:

> **El dato financiero no tiene canal público directo desde su sistema de origen. Llega a QUIRA
> sólo por lo que el GAD publica o entrega, a través de varios canales cuya cobertura,
> periodicidad, integridad y confiabilidad hay que determinar por separado.**

Y de ahí la regla que el caso deja, aplicable a todos los silos:

> ### `SISTEMA_ORIGEN ≠ CANAL_DE_ADQUISICIÓN`
>
> Y su corolario de ausencia, que `DOC-035` ya gobierna: **no hallado en un canal ≠ no publicado ≠
> no existe ≠ no entregado por vía pasiva ≠ no procesable.** Cada canal tiene su propio universo,
> y la ausencia se declara respecto de los canales efectivamente inspeccionados.

### ⛔ `S5` · el nombre del silo no es su vía de adquisición

*(Javo, 2026-09-09.)*

> *«La vía eSIGEF no existe: es portal web y LOTAIP. El eSIGEF no tiene portal público para
> extraer información, es sólo para instituciones públicas. **Es la caja negra del Estado
> ecuatoriano.**»*

Verificado el 2026-09-09 en `app/connectors/`, `app/fetchers/`, `scripts/` y `app/`:

```
conectores de eSIGEF ....... 0
fetchers de eSIGEF ......... 0
scripts que capturen eSIGEF  0
```

Y el canon ya lo decía, si se leía con cuidado: `META_CATALOGO_AGENTES:45` declara que la entrada
de **«eSIGEF (Fuente)» es `Gold Master H07`** —el Excel, no el sistema—, mientras el **`Budget
Agent`** (línea 39) entra por **`portal transparencia (=CD-06 d07)`**.

> **`S5` se llama `H07_S5_FINANCIERO_eSIGEF` por el sistema donde NACE el dato, no por la puerta
> por donde QUIRA lo obtiene.** Y `V_eSIGEF` es un **verificador** de que el dato existe, no un
> conector que lo capture. Es `DOC-033` aplicado a los silos: **el nombre no acredita la vía.**

Las vías reales por las que el dato financiero ha entrado, todas verificables:

| vía | evidencia |
|---|---|
| **portal de transparencia** (LOTAIP) | `CD-06` · cédula presupuestaria · `Budget Agent` |
| **transparencia pasiva** (solicitud) | `OFICIO N.º 0143-2026-SG-JAMZ-GADMCM` — entrega de cédulas 2023-2024 reportadas al MEF |
| **carga al Gold Master** | `H07`, por gobernanza |

> ### ⚠️ Y la consecuencia para los 222 GAD, que es de primer orden
>
> La fórmula de `V_i` es `=SI(O(V_eSIGEF=0,V_SERCOP=0),0,…)`, justificada como *«sin núcleo
> financiero = sin score»*. Si el dato financiero **sólo puede llegar por lo que cada GAD publique
> o entregue**, entonces **QUIRA no tiene vía independiente para el núcleo financiero**: su
> disponibilidad depende del propio sujeto observado.
>
> Metodológicamente es correcto —no publicar es un resultado de auditoría, no una excusa—, pero
> **cambia el cálculo de escalabilidad**: replicar a 222 GAD no depende sólo de la capacidad
> técnica de QUIRA, sino del comportamiento publicador de cada municipio.
>
> ⚠️ Lo que **no** se sigue: que LOTAIP sea «la única puerta». Hay al menos tres canales, y el
> propio LOTAIP tiene dos. La pregunta correcta no es *«¿cuál es la puerta?»* sino **«¿qué
> canales permiten obtener evidencia sobre un mismo objeto institucional, y qué cobertura,
> periodicidad, integridad y confiabilidad aporta cada uno?»**
>
> Eso no es una decisión que tome este arqueo. Es una restricción del entorno que `REARQ` debe
> incorporar al diseño.

### La web institucional: declarada, y con su razón escrita

`app/observatorio/despacho.py:108` lo dice sin rodeos:

```python
"web_gad": "Sin conector. Cada municipio publica en su propio formato."
```

Y `META_CATALOGO_AGENTES` ya declara **cuatro agentes** cuya entrada es `web GAD`, todos en
`⬜ Fase 4`: `PDOT Agent` · `POA Agent` · `PAC Agent` (`SERCOP / web GAD`) · `Resultado Agent`
(`web GAD / transparencia`). Están en pausa por presupuesto de API, con vía alternativa ya
identificada (inferencia local con `llama-cpp-python`).

> ⚠️ Luego la intuición de la dirección **no abre un frente nuevo: reactiva uno declarado y
> pausado**. Lo que falta no es decidir que la web del GAD es fuente — ya lo es en el canon —
> sino resolver el problema que la dejó sin conector: **cada municipio publica en su propio
> formato**, y eso no escala a 222 GAD por conector individual.

### Y la pregunta que esto abre, sin resolver

Un mismo documento —el PDOT, el PAC, el presupuesto— puede aparecer **en el portal de
transparencia y en la web institucional**. Formulada por el colega:

> **¿Son dos copias de la misma evidencia, o dos observaciones independientes del mismo
> documento?**

De la respuesta dependen la deduplicación, la validación cruzada, la procedencia, el tratamiento
de discrepancias de fecha o versión, y qué significa que una de las dos falte. `PCD-D07` ya
resolvió la mitad interna del problema —`publicación ≠ artefacto`, con SHA-256— y esa distinción
es probablemente el punto de partida. **No se decide aquí.**

## 4-ter · Las tres verificaciones de canal · 2026-09-09

*(Encargo cerrado del asesor: determinar por evidencia, no por declaración.)*
**Universo inspeccionado:** repo `quira-os` completo incluidos `worktrees`, y `Dylus Lab/ProyecT/`.

### V1 · QUIRA Ciudadana — **canon sí, código no**

| | |
|---|---|
| canon | `ADR-046 §2` le da nombre, lugar y 4 capacidades · base legal con SHA |
| superficie de aporte | ⛔ **no existe** |
| flujo de acreditación | ⛔ **no existe** |
| lo que sí hay | `m1_situacion.py:107` — la narrativa que **invita** a aportar (`ADR-046 §2.4`) |

Los dos `st.file_uploader` del repositorio (`p_carga.py:118`, `p_ingesta.py:327`) se montan en
**`env_ops.py`** y son del **Técnico**: *«permite al Técnico actualizar el snapshot maestro»*. No
son superficie ciudadana.

> **La capacidad está decidida y no está construida.** `ADR-046` advertía exactamente contra esto:
> *«una capacidad sin fecha, sin lugar y sin nombre es abandono con otro nombre»*. Tiene nombre y
> lugar; le falta lo demás.

### V2 · Transparencia pasiva — el artefacto existe, **sin cadena de procedencia**

```
ProyecT/Holding_Municipal_Montecristi/
    OFICIO N. 0143-2026-SG-JAMZ-GADMCM-A  Sr. Ronald Delgado-signed.pdf
```

Está **firmado** —lo que por `ADR-046` le daría techo **institucional**—, pero:

- **no tiene SHA registrado** en ningún artefacto de evidencia de QUIRA
- no aparece en `data/`, sólo citado en prosa en `PROTOCOLO_CURACION_DOMINIO:255`
- y ese mismo protocolo lo declaró así a propósito: *«se registra como prueba de viabilidad del
  canal, nada más — no se audita aquí»*

> Luego la vía pasiva tiene **un precedente acreditado, no una capacidad operativa**. La distinción
> es de `ADR-051`: el programa existe ≠ QUIRA lo ejecuta ≠ es reproducible.

### V3 · Web institucional — dónde viven realmente los documentos

Recuento por tipo, `2026-09-09`:

| documento | `ProyecT/` | `quira-os/data/` |
|---|---:|---:|
| POA | **32** | 4 |
| PAC | **29** | 6 |
| Presupuesto | **18** | 5 |
| PDOT | 14 | 11 |
| Orgánico | **11** | 1 |
| **Audiencias** | **49** | **0** |
| **Ordenanzas** | **2** | **0** |

⚠️ **Y la lectura fácil de esa tabla es falsa.** `ProyecT/` **no está fuera del sistema**: es la
**frontera de datos declarada**, accedida por `config.DATOS_DIR`, con su propio gate
—`scripts/ci/check_portabilidad.py`, `_FRONTERA = "ProyecT"`— y **trinquete en cero** desde el
2026-08-25 (`frontera_fija 0/0`). Los enrichers leen de ahí: `enrich_poa_multianio`,
`enrich_mandato`, `d08/extraer_demandas`, `d08/cruzar_demandas`.

### ★ La diferencia real: con o sin cadena de procedencia

No es «dentro / fuera del sistema». Es esto:

| | `S7` · DPE | todo lo demás |
|---|---|---|
| captura | automatizada, con etapas y gates | manual, previa al sistema |
| SHA por artefacto | ✅ **422 entradas** en `inventario_documental.json` | ⛔ ninguno — `poa_multianio.json` no contiene SHA |
| registro de captura | `descargas_indice.json` · `enlaces.json` | ⛔ ninguno |
| invalidación | por cambio de SHA del insumo | ⛔ ninguna |
| reproducibilidad | 1 etapa `validada`, 2 en `ejecución` (`ADR-051`) | ⛔ no medida |

> **QUIRA tiene una sola cadena de adquisición completa —`S7`/DPE— y un régimen sin procedencia
> por artefacto para todo lo demás.** Es exactamente el criterio 2 de `ADR-053 §5`: *«procedencia
> en el artefacto, escrita por el generador»*, cumplido en un canal y pendiente en el resto.

### V4 · SERCOP — ⛔ CORRECCIÓN: sin SHA **no** significa sin procedencia

La formulación anterior —«un régimen sin procedencia para el resto»— **era falsa**, y el asesor lo
señaló antes de que se consolidara. Verificado en `data/scouting/`:

```
sercop_2026_parcial.json       fuente: "SERCOP OCDS · montecristi"
                               fecha_corte: 2026-08-12 · estado_captura: "completa"
sercop_estado_contractual.json _meta.generado: 2026-08-17
                               _meta.fuente: https://datosabiertos.compraspublicas.gob…
sercop_holding.json            _meta.generado: 2026-08-12 · _meta.fuente: URL
sercop_montecristi_2026.json   fuente + fecha_corte: 2026-06-24
sercop_sprint0_holding.json    fecha: 2026-05-28T20:02:55Z
```

Canal: **API OCDS** (`/PLATAFORMA/api/search_ocds` + `/record`), no scraping. Con doctrina
declarada en el propio script: *«el Excel es la base. Este conector trae el dato limpio del SERCOP
para ingerirlo al silo `H06`; el cajón cablea desde el Excel, no desde la API.»*

> **Hay procedencia: fuente, URL, fecha de corte y hasta estado de captura. Lo que no hay es
> identidad ni integridad por artefacto.**

### V5 · CPCCS — doctrina dual, y una mitad que exige un humano

Canal: portal `rendiciondecuentas.cpccs.gob.ec`. Marco legal declarado: `LOPC Arts. 88-95` ·
`COOTAD Art. 302` · `Res. CPCCS-004-2026`. Y **dos componentes verificables por separado**:

| | qué es | estado verificado |
|---|---|---|
| **A · Informe Técnico** | lo que el GAD sube al portal — auto-declarativo pero verificable | bloque llega al snapshot (`rendicion.cpccs`), con `brecha_compromisos` **vacío** |
| **B · Evento Público** | vídeo en YouTube/Facebook — **evidencia independiente** de que el acto ocurrió | ⛔ *«MANUAL REQUERIDO»*, dicho por el propio script |

⚠️ **No existe ningún `rdc_*.json` en `data/scouting/`**: la vía de artefacto independiente no se
ha ejecutado. Y el insumo con el que `d09` cerró llegó por **otra vía** —`enrich_rdc_docx.py` sobre
los informes en `ProyecT/`—, no por este conector.

> El componente B es notable por sí mismo: **contrastar la declaración institucional contra
> evidencia performativa externa.** Es la idea más avanzada del arqueo y hoy la ejecuta una
> persona.

### V6 · Las cadenas cerradas · consumo, reutilización y prueba

**SERCOP**

```
API OCDS → fetch_sercop.py → data/scouting/*.json (con fuente · fecha_corte · estado_captura)
                           → snapshot_pipeline._step_fetch_sercop  ← llama al CONECTOR EN VIVO
```

⚠️ Dos precisiones que sólo aparecen al recorrer la cadena entera:

- el pipeline **no lee los JSON guardados**: invoca `fetch_sercop_data(ruc, year)` en vivo
  (`snapshot_pipeline.py:174`). Los artefactos de `scouting/` son **registro de captura, no insumo
  del pipeline**
- **no existe ninguna prueba** que ejercite este canal (universo: `tests/`)

**CPCCS — y aquí se confirma la distinción que el asesor anticipó**

```
conector      app/connectors/cpccs.py  →  snapshot_pipeline.py:189   ✅ está en el pipeline
d09 en cambio  motor.py → _ENRICHER_PATH = scripts/enrich_rdc.py
                        → _SNAPSHOT_PATH = data/gm_snapshot.json     ⛔ NO usa el conector
```

> **«El conector existe» y «el dominio se alimenta de ese conector» son dos afirmaciones
> distintas.** Aquí la primera es verdadera y la segunda **falsa**: `d09` se alimenta del enricher
> y del snapshot, no del portal CPCCS.

Y el `Componente B` —el vídeo del acto— sigue diciendo `MANUAL REQUERIDO` en el propio script. La
formulación que la evidencia autoriza:

> **El diseño contempla dos componentes de evidencia potencialmente independientes —declaración
> institucional y evidencia externa del acto—. La integración efectiva de ambos en el flujo
> operativo NO está demostrada.** No se le llama «triangulación» hasta que lo esté.

### ★ Cuatro niveles de procedencia, y ninguno es «sin procedencia»

| nivel | qué acredita | quién lo tiene hoy |
|---|---|---|
| **por artefacto** | identidad e integridad · invalidación por cambio de contenido | `S7`/DPE — **422 entradas con SHA-256** |
| **por dataset/corte** | fuente, URL, fecha de corte, estado de captura | **SERCOP** |
| **por insumo y motor** | SHA del Excel de origen **y del script que lo lee** | `d09/motor.py` — `evidencia_sha256` · `motor_sha256` |
| **histórica documentable** | quién, cuándo, con qué fin y por qué vías — **conocido, anterior al sistema** | `ProyecT/` |

⚠️ Y sobre el último nivel, la precisión que corrige una formulación anterior de este arqueo:

> No es lo mismo **«no conocemos de dónde vino»** que **«conocemos su historia de adquisición, pero
> esa historia no fue registrada por el sistema porque el sistema aún no existía»**. `ProyecT/` es
> lo segundo, y por declaración directa de quien lo reunió: fecha de inicio, autor, finalidad,
> cuatro vías y tipos de fuente. Eso es **proveniencia histórica documentable**, no ausencia.

> ### ⛔ Y lo que NO se hará con ello
>
> `ProyecT/` **no es deuda a saldar retroactivamente**. La pregunta de `REARQ` no es *«¿cómo
> hacemos que febrero de 2026 parezca una captura automatizada?»* sino:
>
> **¿Qué propiedades de aquella adquisición humana deben conservarse como conocimiento histórico,
> y qué propiedades del sistema posterior hay que construir para que esa labor sea reproducible y
> escalable a 222 GAD?**
>
> Eso separa **genealogía** de **arquitectura futura**, y las dos se pierden si se confunden.

### ★★ Qué es `ProyecT/` · declarado por su autor, 2026-09-09

> *«Es la carpeta que yo creé para alojar toda la información que obtuve de la solicitud de acceso
> a la información; de la búsqueda en su página web; de técnicos municipales; y de portales
> institucionales como SERCOP, CPCCS, etc. Se desarrolló de esa manera para poder construir el
> Excel Gold Master y realizar su validación empírica del modelo. Eso fue febrero… ni idea que
> íbamos a terminar construyendo una QUIRA.»*

Eso reencuadra todo el hallazgo:

> **`ProyecT/` no es un régimen de adquisición defectuoso: es el CORPUS FUNDACIONAL.** Reunido a
> mano desde febrero de 2026 por cuatro vías —solicitud de acceso · web del GAD · técnicos
> municipales · portales institucionales— con un fin explícito: **construir el Gold Master y
> validar empíricamente el modelo**. Precede al sistema que hoy lo consume.

De ahí que su procedencia **exista y no esté registrada**: cuando esos documentos se reunieron, no
había sistema que registrara nada. **No es deuda técnica; es la condición de origen** — y la
distinción importa, porque una deuda se salda y una condición de origen se documenta.

⚠️ Lo que sí es consecuencia arquitectónica: **ese método no escala a 222 GAD.** Una persona
reuniendo documentos por cuatro vías produce un corpus fundacional excelente y **un solo
municipio**. Lo que escala es lo que `S7` demostró, y lo que `ADR-046 §2.4` propone por la vía
ciudadana.

### Respuesta provisional a la gran pregunta de `Q-M2`

> *¿QUIRA posee una arquitectura transversal de evidencia, o sólo piezas distribuidas
> históricamente entre dominios y mecanismos de adquisición?*

Con los seis canales ya inspeccionados, la formulación que la evidencia autoriza:

> **La arquitectura CONCEPTUAL es transversal y está acreditada** —custodia ≠ acreditación, tres
> modalidades, techo por documento, ocho estados de captura (`ADR-045`/`046`/`042`)—. Lo que la
> implementación muestra **no es ausencia, sino GRADOS DE MADUREZ DISTINTOS de una misma
> arquitectura**: procedencia por artefacto en un canal, por corte en otro, humana no formalizada
> en el corpus fundacional, y declarada sin construir en el canal ciudadano.

⛔ **No se cierra la hipótesis.** Queda formulada, no concluida:

| canal | arquitectura de adquisición | procedencia | consumo | reutilización |
|---|---|---|---|---|
| **DPE** | completa · 9 etapas con gates | **por artefacto** (SHA · 422) | d07 | por determinar |
| **Web GAD** | sin conector · uso limitado a contraste | por artefacto, **por determinar** | varios, vía `ProyecT/` | por determinar |
| **Pasiva** | caso demostrado, no capacidad | artefacto firmado, **sin ingesta** | por determinar | por determinar |
| **Ciudadana** | **declarada, sin construir** | no aplica todavía | ninguno | ninguno |
| **SERCOP** | API OCDS · captura automatizada | **por corte** (fuente · fecha · estado) | pipeline, **en vivo** — no lee los JSON | ⛔ **sin prueba** |
| **CPCCS** | portal · dos componentes, uno manual | bloque al snapshot, sin artefacto | ⛔ **d09 NO usa el conector** | por determinar |

Lo que falta para cerrarla: **reutilización efectiva en cada fila**, y el recorrido artefacto por
artefacto de `ProyecT/` —qué se descargó, cuándo, de qué URL, si es exactamente lo publicado—.
Ninguna celda se rellena por inferencia.

⚠️ Y esta respuesta **no se apoya en la suite de pruebas**: 930 pruebas verdes acreditan salud del
software, **no conexión operacional de un canal**. Son cosas distintas y se citan por separado.

## 4-quater · SÍNTESIS INTERMEDIA DE `Q-M2` · 2026-09-09

> **La conclusión que ordena todo lo demás:**
>
> **QUIRA no nació con una arquitectura de adquisición. Nació con un CORPUS EMPÍRICO, y después
> empezó a construir una arquitectura capaz de adquirir, acreditar y reutilizar evidencia.**

Eso explica la mayor parte de las diferencias entre DPE, SERCOP, CPCCS, Web GAD, pasiva y
Ciudadana. No son incoherencias: son **capas de una historia**.

### Dos fases, y no deben compararse entre sí

```
FASE GENEALÓGICA · pre-QUIRA          FASE SISTÉMICA · post-QUIRA
    persona                               fuente
      ↓                                     ↓
    solicitud · web · técnico · portal    capturador
      ↓                                     ↓
    documento                             artefacto
      ↓                                     ↓
    corpus ProyecT                        identidad · SHA
      ↓                                     ↓
    Gold Master                           inventario → evidencia → dominio
      ↓
    QUIRA
```

> ⚠️ **No tiene sentido exigirle a febrero de 2026 un mecanismo de SHA que no existía.** Comparar
> `ProyecT/` con `S7` como si fueran dos implementaciones del mismo diseño es un error de método.

### `SERCOP` · qué es realmente el JSON de `scouting/`

Recorrida la cadena entera: **el conector no lee ni escribe JSON**. Llama a
`build_contratacion_block(year, search, buyer)` y devuelve un `dict` en memoria al pipeline
(`status` · `source_id` · `reliability 0.95` · `data` · `error`), degradando la fiabilidad a la
mitad si la API responde parcial. Hay **dos caminos que no se encuentran**:

```
CLI       fetch_sercop.py --out  →  data/scouting/*.json      registro de una captura manual
PIPELINE  connectors/sercop.py   →  dict en memoria → snapshot insumo real del sistema
```

> Respuesta a la pregunta: **el JSON de `scouting/` no es artefacto canónico ni insumo del
> pipeline. Es registro de exploración** — y el nombre del directorio ya lo decía.

⛔ **Y eso NO es «SERCOP resuelto».** Lo resuelto es el **rol ontológico de un artefacto**. La
cadena sigue abierta:

| SERCOP | estado |
|---|---|
| clasificación del JSON de `scouting/` | ✅ **RESUELTA** |
| cadena `API → respuesta → dict → consumidor → resultado → persistencia → reutilización → prueba` | ⬜ **PENDIENTE DE CIERRE** |

### A · La cadena SERCOP · **CERRADA COMO ARQUEOLOGÍA DE CAPACIDAD/CADENA**

> ⛔ **No leer esto como «SERCOP cerrado».** Lo cerrado es el **expediente de arqueología**: qué
> existe, hasta dónde llega y qué no está demostrado. **No acredita que SERCOP sea hoy una ruta
> activa del estado canónico de QUIRA.**

| elemento | estado |
|---|---|
| genealogía del JSON de `scouting/` | **RESUELTA** |
| canal → API → respuesta | **DEMOSTRADO** |
| normalización | **DEMOSTRADA** |
| materialización en la ruta del pipeline | **DEMOSTRADA COMO CÓDIGO** |
| presencia en el snapshot **vigente** | 🔴 **NO DEMOSTRADA** |
| evidencia canónica | 🔴 **NO DEMOSTRADA** |
| reutilización *downstream* | 🔴 **NO DEMOSTRADA** |
| prueba contra el canal real | 🔴 **NO DEMOSTRADA** (sólo mock) |
| merge por colisión de claves | **RESUELTO · ∅** |
| solapamiento semántico | ⬜ **ABIERTO PARA CANON** |
| múltiples productores del snapshot | **DEMOSTRADO** |
| productor canónico | ⬜ **ABIERTO** |

### El detalle de los tramos · 2026-09-09

| # | tramo | estado | evidencia |
|---|---|---|---|
| 1 | sistema de origen → **canal** | **DEMOSTRADO** | API OCDS `/PLATAFORMA/api/search_ocds` + `/record`, endpoint subsanado y validado en vivo el 2026-06-24 |
| 2 | canal → **respuesta** | **DEMOSTRADO** | `build_contratacion_block(year, search, buyer)` |
| 3 | respuesta → **construcción del objeto** | **DEMOSTRADO** | `dict` con `status` · `source_id` · `reliability 0.95` · `data` · `error`; **degrada a 0,475 si la API responde parcial** y a 0,0 si falla |
| 4 | objeto → **consumidor** | **DEMOSTRADO** | `_step_fetch_sercop` → `_results["sercop"]` → `_step_normalize_sources` (conserva el envoltorio íntegro, no aplana) |
| 5 | objeto → **normalización** | **DEMOSTRADO** | `_step_normalize_sources` conserva el envoltorio íntegro, no aplana |
| 6 | normalización → **materialización** | ⚠️ **PARCIALMENTE DEMOSTRADO** | existe en código —`snapshot_pipeline:364`, `{**gm_cont, **sources["sercop"]["data"]}`— pero **el snapshot vigente no la contiene** |
| 7 | materialización → **evidencia canónica** | 🔴 **NO DEMOSTRADO** | ⚠️ entrar al snapshot demuestra **materialización del dato**, no que sea evidencia acreditada. Nada verificado le asigna techo, custodia ni acreditación |
| 8 | evidencia → **dominio** | 🔴 **NO DEMOSTRADO** | ningún dominio verificado que la consuma |
| 9 | dominio → **inferencia / reutilización** | 🔴 **NO DEMOSTRADO** | — |
| 10 | → **prueba** | ⚠️ **PARCIALMENTE DEMOSTRADO** | `test_pipeline_smoke.py` la ejercita con `@patch` y `_SERCOP_MOCK`: acredita la **integración del pipeline**, no el canal contra la API real |

> ### ⛔ La corrección que separa el tramo 6 del 7
>
> La versión anterior encadenaba `materialización → evidencia/resultado` como un solo paso. **Es
> un salto conceptual**, y precisamente el que este expediente existe para impedir:
>
> **dato disponible ≠ evidencia acreditada.** Que un valor entre al snapshot demuestra que el
> dato se materializó; no que tenga techo de acreditación, custodia declarada ni procedencia
> suficiente para sostener una inferencia. Son transiciones distintas y cada una necesita su
> propia demostración.
>
> Lo que sí aporta SERCOP al resultado —y es real— es su `reliability` graduada: pesa `0.35` en
> `TRACEABILITY_SCORE` y cuenta en `coverage`. Pero **sólo si el snapshot lo genera el pipeline**,
> que no es el caso del vigente.

### ★ Lo que sólo aparece al recorrer la cadena entera: hay DOS generadores de snapshot

```
scripts/_update_snapshot.py      Gold Master H73_OUTPUT_API → snapshot   ← EL VIGENTE
app/pipelines/snapshot_pipeline  conectores DPE·SERCOP·CPCCS → snapshot   ← el que consume SERCOP
```

El snapshot vigente lo delata su propio `_meta`:

```
fuente        SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx — H73_OUTPUT_API
_pipeline     ausente  ← el pipeline lo añadiría en su paso 9
contratacion  la clave NO EXISTE en el snapshot vigente
```

> **El pipeline que consume SERCOP no es el que produjo el estado vigente.** La cadena está
> construida y hoy no está ejercida: el `snapshot` que el sistema usa viene del Gold Master, y por
> eso la contratación de SERCOP no aparece en él.

### El merge de `:364`, auditado clave por clave

Se dijo que el solapamiento «parece improbable». **Eso no era una auditoría.** Hecha:

```
GM.contratacion   pac_publicado · procesos_adjudicados · procesos_cancelados · cancelados_pct
SERCOP.data       year · fuente · fecha_corte · n_procesos · total_usd · conteos_por_etapa
                  procesos · alertas · via_api · transporte · estado_captura

INTERSECCIÓN DE CLAVES  =  ∅
```

| categoría | resultado |
|---|---|
| sin colisión | **las 15 claves son disjuntas** |
| colisión semánticamente compatible | — |
| colisión con **autoridad distinta** | ⚠️ **ninguna por nombre · SÍ por semántica** |
| no determinable | — |

> **No hay colisión de claves, pero sí SOLAPAMIENTO SEMÁNTICO sin autoridad declarada.**
> `procesos_adjudicados` y `procesos_cancelados` (Gold Master) describen el mismo fenómeno que
> `conteos_por_etapa` y `procesos` (SERCOP), por vías distintas y con cortes temporales distintos.

Con esa precisión, la lectura del merge cambia:

    GM      = estado canónico certificado
    SERCOP  = enriquecimiento con el corte externo vivo

y la operación **es legítima hoy** — el `dict` no pisa nada. Lo que queda abierto no es el orden
del merge sino la pregunta de fondo:

> Si el Gold Master dice `procesos_adjudicados = X` y SERCOP entrega `conteos_por_etapa` con otro
> número para el mismo período, **el snapshot llevaría ambos sin declarar cuál tiene autoridad**.
> Eso se resuelve por canon, **no por el orden de un `dict`**.

**No se toca: se registra para `REARQ`.**

### El JSON de `scouting/` conserva valor probatorio · no operativo ≠ irrelevante

| artefacto | fecha | fuente | estado captura | resultados |
|---|---|---|---|---|
| `sercop_2026_parcial` | `fecha_corte 2026-08-12` | `SERCOP OCDS · montecristi` | **completa** | 26 procesos |
| `sercop_estado_contractual` | `generado 2026-08-17` | **URL de la API** | — | — |
| `sercop_holding` | `generado 2026-08-12` | URL de la API | — | — |
| `sercop_montecristi_2026` | `fecha_corte 2026-06-24` | con comprador | — | 7 procesos |
| `sercop_sprint0_holding` | `2026-05-28T20:02:55Z` | — | — | — |

> **Genealogía de adquisición presente y desigual.** Formulación forense, que sustituye a la
> anterior:
>
> **Los artefactos examinados muestran un incremento temporal en la granularidad de los metadatos
> de captura registrados. La causa de esa evolución no se determina a partir de los JSON.**

⛔ Se retira *«la procedencia maduró junto con el sistema»*: describía una **narrativa causal** que
los artefactos no acreditan. Lo observable es la evolución de la información registrada; atribuirla
a una maduración deliberada del sistema exigiría evidencia distinta —decisiones, commits, ADR— que
no se buscó aquí.

Ninguno lleva la URL exacta de la consulta ni los parámetros como campo propio (van embebidos en
el string `fuente`), y ninguno lleva identificador que lo relacione con una ejecución posterior.
Eso es lo que impide hoy usarlos como **genealogía formal** en lugar de como registro.

### `Web GAD` · consumidores por tipo — y lo que eso **no** demuestra

| tipo | consumidor verificado |
|---|---|
| PDOT · POA · PAC | `analysis/explainability_report` · `metrics_mcr` · `tag_domains` |
| Cédulas presupuestarias | `enrich_poa_multianio` · `ingest_presupuesto_h07` · `motor_narrativo/extract_cedula_xls` |
| Orgánico | `holding/manifest_holding` · `normativa/manifest` |
| Ordenanzas | `normativa/manifest` · `vis/objeto_canonico` |
| Audiencias · Participación | `d08/extraer_demandas` · `enrich_participacion` · `normativa/extend_lopc_neo4j` |
| Actas | `d08/extraer_demandas` · `neo4j_load_qtmp` · `normativa/analizar_documentos_lotaip` |

⛔ **«Ningún tipo huérfano» era una conclusión más fuerte de lo que esa tabla permite.** Lo
verificado es que existe **código que menciona y consume cada tipo documental**. Son cuatro
preguntas distintas y sólo una está respondida:

| pregunta | estado |
|---|---|
| ¿existe código que consuma ese tipo documental? | ✅ **sí**, verificado |
| ¿hay evidencia de que se **buscó** en la web del GAD? | ⬜ por determinar, por tipo |
| ¿hay evidencia de que fue **capturado** desde ahí? | ⬜ por determinar, por tipo |
| ¿ese consumidor recibe evidencia **proveniente del canal Web GAD**? | ⬜ **debe demostrarse** |

> ### La distinción que impide el salto
>
> *«`enrich_poa_multianio.py` lee POA desde `ProyecT/`»* **no equivale** a *«Web GAD → captura →
> POA → `enrich_poa_multianio.py`»*.
>
> `ProyecT/` es el corpus fundacional y puede contener material obtenido por **cualquiera de las
> cuatro vías**: solicitud de información, web municipal, técnico municipal o portal
> institucional. **Consumidor del documento ≠ consumidor demostrado del canal.**

Lo que falta para cerrar Web GAD es la matriz por tipo, con una columna que hoy no tenemos:
**procedencia del artefacto conocida**.

### CINCO dimensiones de procedencia **observadas** · el `SHA` es una, no todas

⚠️ Se las llama **dimensiones observadas en el corpus**, no una ontología canónica. Todavía hay
que demostrar si son cinco dimensiones independientes, cinco granularidades de lo mismo, o
combinaciones. Lo que **sí** está sólido:

> **La procedencia en QUIRA no se reduce al `SHA`. El corpus evidencia mecanismos de procedencia
> de distinta granularidad y naturaleza.**

| dimensión | qué acredita | dónde se observa hoy |
|---|---|---|
| **de artefacto** | identidad e integridad · invalidación por contenido | `S7`/DPE — 422 con SHA-256 |
| **de dataset** | fuente, corte temporal, estado de captura | SERCOP |
| **de insumo y motor** | SHA del insumo **y del proceso que lo transforma** | `d09/motor.py` |
| **histórica** | quién, cuándo, con qué fin y por qué vías — sin registro de máquina | `ProyecT/` |
| **de custodia** | quién obtuvo, aportó o transmitió el documento | `ADR-045 §3` · `ADR-046 §1.1` |

> **El `SHA` acredita identidad e integridad de un artefacto. No es toda la genealogía del dato.**
> Tomarlo como sinónimo de procedencia fue el error que este arqueo tuvo que corregir dos veces.

### La pregunta de `Q-M2`, reformulada · y su respuesta graduada

Ya no es *«¿existe una arquitectura transversal de evidencia?»* —binaria y por eso engañosa—. Es:

> **¿En qué medida QUIRA ha transformado la adquisición histórica y heterogénea de evidencia en
> una infraestructura común de evidencia canónica, procedencia y reutilización interdominio?**

Con cuatro respuestas posibles, **ninguna elegida todavía**:

| | |
|---|---|
| **A** | ya existe transversalmente |
| **B** | existe parcialmente y **está emergiendo desde varios patrones** |
| **C** | existe sólo en determinados canales |
| **D** | los patrones son conceptualmente compatibles, pero **no hay infraestructura común** |

### Lo que la evidencia autoriza a decir hoy, con esa precisión

> **En el universo examinado, `S7` presenta el mayor nivel de formalización sistémica de la
> procedencia entre los canales estudiados. Los demás muestran mecanismos de procedencia de
> distinta granularidad o antigüedad que aún deben reconciliarse.**

⛔ Se retira la inferencia anterior —*«el canal más maduro es el único construido después de existir
el sistema»*—: es sugerente y **demasiado general**. SERCOP sí tiene procedencia, `d09` sí tiene
una forma de sellado, y `ProyecT/` tiene historia de adquisición conocida.

> ### El método que está funcionando
>
> **Cada vez que una clasificación resulta demasiado binaria, la evidencia obliga a reemplazarla
> por una distinción mejor.** Ocurrió con procedencia sí/no → cinco dimensiones; con canal único →
> seis canales; con dentro/fuera del sistema → grados de formalización. Eso es conocimiento
> arquitectónico, no inventario de archivos.

### Cierre provisional de `Q-M2` — la formulación que se sella

> **QUIRA no nació con una arquitectura homogénea de adquisición de evidencia. Nació de un corpus
> empírico construido mediante modalidades heterogéneas de adquisición. La arquitectura posterior
> ha comenzado a transformar esas prácticas en mecanismos sistémicos de captura, custodia,
> procedencia y reutilización, pero la cobertura y uniformidad de esa transformación aún deben
> demostrarse canal por canal.**

### ⛔ Lo que NO se cierra · lista explícita

Para que ninguna de estas frases aparezca en un informe posterior como si estuviera demostrada:

- «SERCOP está completamente cerrado»
- «todos los tipos de Web GAD tienen consumidor»
- «todos los tipos de Web GAD están integrados al canal Web GAD»
- «QUIRA ya posee una infraestructura transversal homogénea de evidencia»
- «`ProyecT/` tiene procedencia sistémica completa»
- «la arquitectura documental transversal ya está demostrada»

### Orden de trabajo pendiente

```
A · SERCOP    cerrar la cadena completa (no volver a discutir el JSON)
B · Web GAD   matriz por tipo, con la columna PROCEDENCIA DEL ARTEFACTO CONOCIDA
C · síntesis  ¿en qué medida QUIRA transforma evidencia de distintos orígenes,
              canales y custodias en evidencia canónica reutilizable, conservando
              procedencia suficiente para sostener las inferencias posteriores?
D · ProyecT   recién entonces, con una vara arquitectónica explícita en la mano
```

> **`D` va al final a propósito**: recorrer el corpus histórico antes de tener la vara obligaría a
> inventarla mientras se recorre, que es cómo se fabrican criterios a medida del hallazgo.

## 4-sexies · B · WEB GAD · matriz por tipo documental · 2026-09-10

**Universo declarado:** `scripts/` y `app/` en `*.py`. **Términos:** por tipo documental en el
nombre del archivo, cruzados con `requests` · `httpx` · `urllib.request` · `playwright` ·
`selenium` · `aiohttp`. **Exclusiones:** ninguna.

### B.1 · ¿Existe captura desde la web del GAD?

| tipo | script con captura HTTP propia |
|---|---|
| PDOT · POA · PAC · Presupuesto · Orgánico | ⛔ **NINGUNO** |
| Actas de Concejo · Ordenanzas · Audiencias · Ppto. participativo | ⛔ **NINGUNO** |

**Cero capturadores para los nueve tipos.** El único script que toca `montecristi.gob.ec` es
`capturar_lotaip_portal.py`, y lo hace **sólo para contrastar LOTAIP**.

### B.2 · ¿De dónde lee cada consumidor?

| tipo | consumidor | origen real de lectura |
|---|---|---|
| PDOT | `enrich_planificacion.py` · `data/pdot_context.py` | **frontera `ProyecT/`** · Gold Master |
| POA | `enrich_poa_multianio.py` · `extract_poa_pdf.py` | **frontera `ProyecT/`** |
| Presupuesto | `enrich_presupuesto.py` · `ingest_presupuesto_h07.py` | **frontera `ProyecT/`** |
| Orgánico | `holding/manifest_holding.py` | **frontera `ProyecT/`** |
| Ordenanzas | `normativa/manifest.py` | **frontera `ProyecT/`** |
| Audiencias | `d08/extraer_demandas.py` · `enrich_participacion.py` | **frontera `ProyecT/`** · `data/` |
| Ppto. participativo | `d08/cruzar_demandas.py` | **frontera `ProyecT/`** |
| PAC | `capturar_sercop_holding.py` | ⚠ no determinado en este barrido |

**Ocho de nueve leen de la frontera `ProyecT/`.**

### ★ B.3 · La conclusión, con la distinción que la hace válida

> **CONSUMO: demostrado para los nueve tipos. ADQUISICIÓN desde el canal Web GAD: NO demostrada
> para ninguno.**

Y por tanto la formulación que la evidencia autoriza:

> **«Web GAD» no es hoy un canal de adquisición de QUIRA. Es el origen histórico de parte del
> corpus fundacional, sin ruta reproducible desde el sistema.** Los artefactos entraron por las
> cuatro vías de febrero de 2026 y viven en la frontera de datos, donde los enrichers los leen.

⛔ **Ningún tipo se cierra por estar presente en `ProyecT/`.** Presencia histórica ≠ adquisición
por el canal. Es la regla que `A` dejó y que aquí decide las nueve filas.

### B.4 · Y la excepción que el barrido encontró

`scripts/rc_scout.py` —motor de exploración municipal, endpoints de la DPE obtenidos por
ingeniería inversa— **sí adquiere presupuesto de forma automatizada**:

```
GET  /admin/public/establishment/list?function=7     → lista TODOS los GAD
GET  /admin/public/establishment/{id}                → detalle de entidad
POST /public/public/presupuesto {ruc, year, month}   → PRESUPUESTO MENSUAL
GET  /transparency/anual-report/establishment?…      → informe anual
```

Con productos ya materializados: `gad_municipales_all.json` (21) · `manabi_scan.json` (50).

> ⚠️ **Pero eso no es «Web GAD»: es DPE.** El presupuesto tiene canal automatizado y multi-GAD
> — por el portal nacional, no por la web municipal. Y es la única capacidad verificada hoy que
> opera sobre **más de un municipio**.
>
> `discovery.json` lo confirma por omisión: sus `portals` sólo contienen la DPE, con `selectors`
> y `notes` **vacíos**. El descubridor de portales existe y sólo ha explorado uno.

### B.5 · Productor del estado canónico

| tipo | productor del estado que llega al canon |
|---|---|
| los nueve | **`scripts/enrich_*.py` → Gold Master → `_update_snapshot.py`** |

Ninguno pasa por `snapshot_pipeline`. Coherente con el hallazgo transversal de abajo: **el
productor del estado vigente es el Gold Master, no la ruta de conectores.**

## 4-quinquies · ⚠️ HALLAZGO TRANSVERSAL · multiplicidad de productores del snapshot

> **Estado: ABIERTO · REQUIERE RECONCILIACIÓN.** No se declara defecto.

Salió al recorrer SERCOP, **pero no pertenece a SERCOP**: afecta al artefacto central del sistema.

```
        Gold Master                    SERCOP · DPE · CPCCS
             │                                  │
     _update_snapshot.py                snapshot_pipeline.py
             ↓                                  ↓
      snapshot VIGENTE                    otro snapshot
```

Y el `DEPENDENCY_ATLAS` ya listaba **tres** escritores del snapshot —`_update_snapshot` ·
`snapshot_pipeline` · `p_carga` (consola Dylus)— sin declarar cuál es el canónico.

> **¿Cuál es el generador canónico de `gm_snapshot.json`, y bajo qué condiciones puede existir
> más de una ruta de producción del mismo artefacto?**

Tener dos productores **no es necesariamente incorrecto**: puede haber razones históricas,
operativas o de compatibilidad. Pero es una **tensión arquitectónica demostrada**, y exactamente
el tipo de cosa que `REARQ` debe encontrar.

Las diez preguntas que la reconciliación debe responder, **antes de tocar una línea de código**:

| # | pregunta |
|---|---|
| 1 | ¿cuál es el snapshot canónico? |
| 2 | ¿cuál es el productor **normativo**? |
| 3 | ¿cuál es **histórico**? |
| 4 | ¿cuál es **operativo**? |
| 5 | ¿puede producirse el mismo archivo por dos rutas legítimas? |
| 6 | si sí, ¿qué relación existe entre ambas? |
| 7 | ¿qué fuente tiene **autoridad sobre cada campo**? |
| 8 | ¿cómo se **detecta divergencia** entre productores? |
| 9 | ¿qué consumidor *downstream* recibe cada versión? |
| 10 | ¿existe un **único punto de publicación**? |

⚠️ La pregunta 7 conecta con el solapamiento semántico del merge de `:364`: si dos productores
pueden escribir el mismo atributo semántico por vías distintas, la autoridad **debe estar
declarada en el canon**, no emerger del orden de un `dict` ni de cuál script se ejecutó último.

## 5 · La distinción que se conserva

| | |
|---|---|
| **DOMINIO DE TRANSPARENCIA** | evalúa transparencia · sectorial · producto |
| **CAPACIDAD DOCUMENTAL REUTILIZABLE** | captura, verifica y sella evidencia · posible infraestructura transversal |

> Que ambas estén **hoy implementadas juntas no demuestra que deban permanecer juntas. Tampoco
> demuestra que deban separarse.** Ese es exactamente el tipo de cuestión que `REARQ` resuelve, y
> no se decide en este arqueo.

## 6 · Clasificación · lo que NO es

**No es `RECONSTRUIR`.** Ese destino queda descartado por la evidencia de este arqueo.

Que hoy exista OCR manual para 10 artefactos **no significa que la arquitectura documental esté
ausente**: significa que su **automatización y escalabilidad** están incompletas. Es una
diferencia de grado de madurez, no de existencia.

Destinos que siguen abiertos, sin elegir ninguno:

| Destino | Sobre qué recaería |
|---|---|
| `CONSERVAR` | el canon de evaluación, la trazabilidad, el tratamiento de la ausencia |
| `MEJORAR` | OCR y procesamiento · escalabilidad a 222 GAD |
| `DESCOMPONER` | separar capacidad transversal de lógica específica de Transparencia |
| `TRASLADAR` | llevar componentes de captura/sellado a infraestructura común |

## 7 · Correcciones que este arqueo registra

**Se retira el hallazgo «existe una capacidad de sistema sin dominio asignado».** Es falso. La
capacidad tiene dominio, expediente, norma con SHA, código, 1.748 descargas y 936 archivos de
evidencia.

**Se corrige además una cifra de este mismo arqueo.** La primera redacción atribuyó los 1.748
archivos a `data/lotaip/descargas/`. El reparto real es **1.748 en `data/lotaip/`, de los cuales
936 están en `descargas/`** — y 936 es justamente la cifra de evidencia con SHA que `PCD-D07`
declara. Es el mismo error que ese expediente cazó cuatro veces: **una cifra parcial con
apariencia de total**.

**Causa del error, y la regla que deja:**

> ### `DOC-035` · El alcance de una búsqueda es parte de su resultado
>
> La búsqueda que produjo el falso vacío **excluyó rutas** (`worktrees`) y **buscó por el número
> del dominio** en vez de por el nombre del trabajo. Ninguna de las dos cosas se declaró al
> reportar el resultado.
>
> **Una búsqueda acotada no autoriza a declarar ausencia.** Quien informa un vacío debe declarar
> qué rutas incluyó, qué términos usó y qué excluyó — igual que `d07` declara
> `cortado_por_tope_de_tamano` en lugar de afirmar que el archivo no existe.
>
> Es `DOC-034` aplicado al observador: **no haber mirado bien no es haber mirado.**

**Numeración · verificado, no resuelto.** La hipótesis de renumeración por la baja de `d04` es
**falsa**: el código conserva `QINV-001..013` sin renumerar — `QINV-006` es Salud Institucional
(`m1_situacion.py`) y `QINV-007` es Transparencia (`p07_transparencia.py`). La dirección se
refiere al dominio de Transparencia como `DOM06`. **La discrepancia se registra y no se resuelve
aquí** (`DOC-033`: el nombre no demuestra la correspondencia).

**Lo que sí queda en pie, con la formulación corregida.** Se dijo «`d06` sin silo `S6`», y es
una inferencia de las que este mismo documento prohíbe. El canon dice otra cosa:
`MATRIZ_CABLEADO_CANONICO:71` **asigna `S6` (`H08_S6_AUTOREPORTE_SIGAD`) a `d06`**, y lo que
declara ausente es el agente — *«`d00`, `d05` y `d06` no existen en `app/agents/`»*.

> El silo **existe y está asignado**. Lo que falta es quien lo cure.

Formulación que se conserva:

> **El estado y la función de `S6`/`QINV-006`, y su relación con el dominio hoy denominado
> `d06`, requieren reconciliación ontológica y funcional.**

Hechos verificados que la acompañan: `ICM` no se calcula y `SAT-I` sigue apagada
(`app/services/sat_evaluator.py:297`, comprobado el 2026-09-08). `OBS-009` documenta la
divergencia `SIGAD`↔`LOTAIP`, es decir entre `S6` y `S7` — y **`S7` (`H09_S7_TRANSPARENCIA_LOTAIP`)
es el silo de `d07`**, con `V_LOTAIP` y `H18_ITAM`, según esa misma matriz.

---
*REARQ · Arqueo `001` · Dylus Lab © 2026 · el Gold Master no se modificó · baseline 27,4582 %
congelado · preservación activa sobre 9 clases de artefacto.*
