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
