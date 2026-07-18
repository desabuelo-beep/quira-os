# BRN · Ciclo de Vida de una Regla y Molde CNO/RO

> **Qué es este documento.** Cierra los pasos **2 (ciclo de vida)** y **3 (molde CNO/RO)** del
> *Orden de trabajo* del ADR-038. Es el **contrato estable** sobre el que se construirá el piloto
> CNO-IV-001 y, después, todas las CNO. **El molde se considera estable:** cualquier modificación
> posterior constituye un **cambio arquitectónico mayor que requiere un ADR propio** (precisión del
> colega · 2026-07-18: en arquitectura se evitan los absolutos — no es un dogma, es una barrera de
> gobernanza). Si cambia tras migrar 80 CNO, se reconstruye todo (ADR-038 §227).

**Estado:** PROPUESTA · 2026-07-18 (director técnico redacta sobre ADR-038/039 · Javo valida)
**Relacionado:** ADR-038 (define CNO/RO/MDN · §8 ciclo, §221 las 7 preguntas) · ADR-039
(compilación de la RO al Gold Master · Estado≠Configuración) · ADR-035 §5 (la IA propone, el
humano valida) · Regla 1 (Excel=estado) · Regla 3 (sin SHA no hay dato) · Regla 9 (nace en canon).
**No es un ADR:** es la **especificación operativa** que los ADR decidieron. Si una decisión de
fondo cambia, se decide en un ADR y este documento la implementa — nunca al revés.

---

## Parte I — El ciclo de vida de una regla

Construir conocimiento jurídico y **gobernarlo** son procesos distintos (ADR-038 §8). Esta parte
nombra el segundo: cómo una regla **nace, vive, se audita y muere**, y cómo una reforma se propaga.

### 1. Los dos objetos versionan por razones distintas
| | **CNO** (Derecho) | **RO** (lógica) |
|---|---|---|
| Modela | la cadena normativa completa | variable · umbral · periodo · consecuencia |
| **Versiona cuando** | cambia la **cadena** (nuevo artículo, reforma, derogación) | cambia la **lógica** (umbral, periodo, variable, motor) |
| No se inmuta por | un cambio de umbral (eso es la RO) | un cambio de redacción que no toca la lógica |
| Identidad | `CNO-<dominio>-<n>` · versión `vN` | `RO-<dominio>-<n>` · versión `vN.M` |

**Independencia (la ventaja real · ADR-038 §107):** cambiar el umbral 65→70% mueve solo la **RO**;
agregar un artículo a la cadena mueve solo la **CNO**. Una reforma casi nunca toca ambas a la vez.

### 2. Estados de una CNO
```
        (extracción + validación humana)                 (reforma toca su cadena)
propuesta ─────────────────────────────▶ vigente ─────────────────────────────▶ en_reforma
                                            │                                        │
                                            │ (norma derogada sin reemplazo)         │ (nueva versión validada)
                                            ▼                                        ▼
                                         derogada ◀───────────────────────────── vigente vN+1
```
- **propuesta** — extraída del Corpus, aún sin promover. No la consume nadie.
- **vigente** — **solo Javo la promueve** (ADR-035 §5). Es la única que las RO pueden derivar.
- **en_reforma** — una reforma tocó su cadena; se está construyendo la versión siguiente. La
  versión anterior **sigue vigente para el cálculo** hasta que la nueva se valide (no hay vacío).
- **derogada** — su fundamento salió del ordenamiento sin reemplazo. Queda **archivada y auditable**
  (memoria normativa viva), nunca se borra: un informe de 2026 debe poder reconstruirse.

### 3. Estados de una RO
```
propuesta ──(validada)──▶ vigente ──(cambia la lógica)──▶ obsoleta   [reemplazada por RO vN.M+1]
                            │
                            └──(su CNO se deroga sin reemplazo)──▶ retirada
```
- **vigente** — es la que el Gold Master compila (ADR-039) y la SAT consume. **Una sola por regla.**
- **obsoleta** — reemplazada por una versión posterior; **se conserva** para responder *"¿con qué
  versión jurídica se calculó este ICPI en jun-2026?"* (ADR-039 §5).
- **retirada** — su CNO se derogó; la SAT que la consumía queda sin control activo (se marca, no se borra).

### 4. Versionado — regla de numeración
- **CNO `vN`** (entero): sube cuando la **cadena** cambia. `v1 → v2` = se agregó/derogó/sustituyó un
  eslabón. Cada versión guarda el SHA de **cada** eslabón en ese momento.
- **RO `vN.M`**: **N** sube si cambia la **CNO de la que deriva** (herencia); **M** sube si cambia solo
  un parámetro de la lógica (umbral, periodo). Ej.: `RO-IV-001 v1.0` (65%) → `v1.1` (70%) = mismo
  Derecho, nuevo umbral; `RO-IV-001 v2.0` = la CNO subió a v2 y la RO se recolgó de ella.
- **Toda versión es inmutable una vez `vigente`.** No se edita: se crea la siguiente y la anterior
  pasa a `obsoleta`. Así la traza histórica nunca se pierde.

### 5. Propagación de una reforma — el caso "toca 12 SAT" (7ª pregunta · ADR-038 §226)
El MDN (grafo · ADR-038 §9) hace esto **determinista**:
```
1. Reforma publicada        → nuevo texto al Corpus (SHA nuevo)                [construcción]
2. El grafo señala impacto  → qué CNO citan el/los artículo(s) tocado(s)       [automático]
3. Cada CNO afectada         → pasa a 'en_reforma'; se propone su vN+1          [IA propone]
4. VALIDACIÓN HUMANA         → Javo revisa la nueva cadena y la promueve         [Javo · §156]
5. Las RO que derivan         → se revisa si su lógica cambió:
      • si solo cambió el umbral → RO vN.M+1 (recompila · ADR-039)
      • si la cadena no altera la lógica → la RO no cambia, solo re-apunta al SHA nuevo
6. Recompilación             → el compilador materializa las RO vigentes al Gold Master (ADR-039)
7. Recalculo                  → el Gold Master recomputa; SAT → DOM → dashboards → informes
```
**El humano interviene una sola vez (paso 4), sobre la CNO.** Lo demás es mecánico y trazable. La
reforma deja de decir *"cambió el Art. 198"* y dice *"cambió CNO-IV-001 → 3 RO → 7 SAT → 2 DOM →
12 dashboards"* (ADR-038 §201).

---

## Parte II — El molde de la CNO

### 6. Definición
Una **CNO (Cadena Normativa Operativa)** es la unidad viva que **consolida toda la cadena jurídica
que sostiene una regla**. Es **puro Derecho** (ADR-038 §67): la cadena y nada más. **No** contiene
variable, umbral, SAT ni motor — eso es la RO. Consultarla **obliga a recorrer toda su cadena**;
por diseño, es imposible tomar una porción.

### 7. Campos mínimos (el molde — no cambia)
```yaml
id:            CNO-IV-001              # CNO-<dominio_normativo>-<secuencia>
version:       2                       # entero; sube si cambia la cadena
titulo:        Regla de Asignación Mínima Prioritaria
objeto:        "la obligación del GAD de destinar un mínimo del presupuesto a inversión"
dominio_normativo: finanzas_publicas_municipales
cadena:                                # cada eslabón = evidencia con su SHA (Regla 3)
  - rol: fundamento_constitucional
    norma: CE            articulo: "271"        sha256: a76e4e0dea62…
  - rol: fundamento_legal
    norma: COOTAD        articulo: "192"        sha256: 42e8c07e33cb…   reformado_por: COOTAD-2026#3
  - rol: regla
    norma: COOTAD-2026   articulo: "198.1"      sha256: 66255f1d91…
  - rol: gasto_computable
    norma: COOTAD-2026   articulo: "198.2"      sha256: ab87de75…
  - rol: consecuencia
    norma: COOTAD-2026   articulo: "198.6"      sha256: e885aa00…
  - rol: disposicion_transitoria
    norma: COOTAD-2026   articulo: "Transitoria Primera"  sha256: e885aa00…
estado:        vigente                 # propuesta | vigente | en_reforma | derogada
vigencia:      { desde: "2026-02-21", hasta: null }
derogaciones:  { reemplaza_a: null, reemplazada_por: null }
deriva_ro:     [ RO-IV-001 ]           # qué RO cuelgan de esta CNO (bidireccional · MDN)
validada_por:  Javo                    # ADR-035 §5 — ninguna IA promueve
```
**Referencia al Corpus (pregunta c):** cada eslabón lleva `sha256`; la CNO **no recopia texto** —
apunta al Corpus verificado (ADR-038 §145). Si un SHA no existe en el Corpus, el eslabón no entra
(Regla 3). La cadena es la **prueba**; la CNO es el **camino**.

---

## Parte III — El molde de la Regla Operativa (RO)

### 8. Definición
Una **RO** es la **única representación operativa autorizada** de la lógica de una regla (ADR-039
§67). Traduce una CNO (Derecho) en lógica ejecutable (variable·umbral·periodo·consecuencia) sin
mezclar los planos. **No es "la verdad"** — la verdad es la norma; la RO es su representación
autorizada.

> **Principio de Neutralidad Operativa** (colega · 2026-07-18): *la RO **nunca interpreta** el
> Derecho; únicamente **operacionaliza una interpretación previamente validada por autoridad
> humana**.* Protege al proyecto de responsabilidad jurídica futura: si en cinco años alguien
> pregunta *"¿quién decidió que el umbral era 70?"*, la respuesta no es la RO, ni el compilador, ni
> la IA — **lo decidió la validación humana** (ADR-035 §5). La RO es el registro de esa decisión,
> no su autor.

### 9. Campos mínimos (el molde — no cambia)
```yaml
id:            RO-IV-001               # RO-<dominio>-<secuencia>
version:       "1.1"                   # N.M — N hereda de la CNO, M por cambio de parámetro
deriva_de:     CNO-IV-001 v2           # SIEMPRE nace de una CNO vigente (Regla 3)
variable:      Pct_Gasto_No_Permanente
umbral:        70                      # %  (v1.0 fue 65 · piso transitorio; v1.1 = 70 regla plena)
umbral_nota:   "piso transitorio 65% con seguimiento desde 1-dic-2026; regla plena 70%"
periodo:       { desde: "2026-06", hasta: "2026-12", frecuencia: mensual }
motor:         "Gold Master · H24_SAT-IV"    # quién computa (NO lo consulta · ADR-039)
consecuencia:  "Alerta fiscal preventiva"
consumida_por: [ SAT-IV-001 ]          # bidireccional (MDN)
opera_en:      d02                     # dominio funcional (no normativo)
estado:        vigente                 # propuesta | vigente | obsoleta | retirada
compilada:     { build: "2026.07.18", sha_artefacto: "…" }   # trazabilidad ADR-039 §5
```
**Cómo la SAT la referencia (pregunta d):** la SAT lleva **solo el ID de la RO** (`SAT-IV-001 →
RO-IV-001`); ya no conoce la ley (ADR-038 §118). Para justificar, sube a la CNO; para probar, al
Corpus (SHA).
**Cómo se compila al motor (ADR-039):** `RO vigente → [COMPILADOR] → tabla de parámetros del Gold
Master`. El compilador **no decide, materializa**; es determinista, reproducible e idempotente. El
Gold Master **nunca consulta la RO en runtime** — nace ya configurado. La Regla 1 queda intacta.

---

## Parte IV — Las 7 preguntas de diseño (ADR-038 §221) — respondidas

| | Pregunta | Respuesta estable |
|---|---|---|
| **a** | ¿Qué es una CNO? | La cadena jurídica completa de **una** regla, puro Derecho; consultarla obliga a recorrerla entera (Parte II §6). |
| **b** | ¿Info mínima? | El molde YAML de §7 (id, versión, objeto, cadena con SHA por eslabón, estado, vigencia, derogaciones, RO derivadas, validador). |
| **c** | ¿Cómo referencia al Corpus? | Cada eslabón guarda `sha256`; no recopia texto, apunta al Corpus. Sin SHA, no entra (Regla 3). |
| **d** | ¿Cómo una SAT referencia su RO? | Con el **ID de la RO** y nada más; el fundamento jurídico vive en la CNO detrás (ADR-038 §120). |
| **e** | ¿Cómo QUIRA IA consulta una CNO? | RO/CNO primero (responde), Corpus después (prueba): `RO → CNO → Corpus (SHA)` (ADR-038 §56). Nunca responde sin traza al texto verificado. |
| **f** | ¿Cómo se versiona ante una norma nueva? | CNO `vN` si cambia la cadena; RO `vN.M` si cambia la lógica; toda versión vigente es inmutable, la anterior pasa a obsoleta/derogada (Parte I §4). |
| **g** | ¿Y si una reforma afecta 12 SAT? | El MDN propaga en 7 pasos deterministas con **una** validación humana sobre la CNO (Parte I §5). |

---

## Parte V — Invariantes del molde (principios estables · cambiarlos exige ADR)
1. **CNO = Derecho; RO = lógica; SAT = medición.** Nunca se mezclan los tres planos.
   La RO **operacionaliza, no interpreta** (Principio de Neutralidad Operativa · Parte III).
2. **Toda CNO apunta al Corpus con SHA por eslabón.** Sin SHA, no hay eslabón (Regla 3).
3. **Solo Javo promueve a `vigente`.** Ninguna IA deriva ni declara vigencia (ADR-035 §5).
4. **Las versiones vigentes son inmutables.** Se crea la siguiente; la anterior se conserva.
5. **El Gold Master no consulta la BRN.** Recibe configuración **compilada**; la traza va del motor
   hacia la BRN (explicar), nunca de la BRN hacia el motor (dictar) (ADR-038 §207 · ADR-039).
6. **Trazabilidad bidireccional siempre** (Principio de Dependencia Normativa · ADR-038 §189).

---

## Parte VI — Gobernanza: propietario y estabilidad de cada artefacto (colega · 2026-07-18)

Saber qué hace cada pieza no basta; hay que dejar claro **quién la gobierna** y **cada cuánto cambia**.

| Artefacto | Propietario | Frecuencia de cambio esperada |
|---|---|---|
| **Corpus** | el Estado (fuente jurídica oficial) | **alta** — reformas, resoluciones, metodologías |
| **CNO** | Dylus · validación **jurídica** (Javo promueve) | **media** — cambia con la cadena normativa |
| **RO** | Dylus · **operacionalización** (Javo valida) | **media** — cambia con umbral/periodo |
| **Compilación** | proceso (no software · ADR-039) | **baja** — el contrato del compilador es estable |
| **Gold Master** | motor matemático (fórmula `H12!B33` inmutable) | **muy baja** — Regla 1 |
| **SAT** | consumidor (lleva solo el ID de la RO) | **casi nunca** — solo si cambia qué regla consume |

Dos lecturas de la tabla: **la propiedad** dice a quién reclamar cuando algo falla; **la frecuencia**
dice dónde concentrar el mantenimiento (arriba se mueve seguido, abajo casi nunca). El Corpus cambia
constante y el Gold Master casi nunca — por eso la BRN existe entre ambos: absorbe el cambio jurídico
sin tocar el motor.

## Siguiente paso
Cerrados el ciclo y el molde, procede — en este orden (ADR-038 §216):
1. **Piloto CNO-IV-001** (asignación mínima prioritaria) sobre este molde — la misma regla que
   rompió la v1, ahora estructuralmente a prueba de porciones.
2. Reconstruir `brn_catalogo.py` como **catálogo de CNO** (enlazar SAT → RO → CNO).
3. Escribir el **plano maestro "Arquitectura General de la BRN v2"** (ADR-039 nota) que mapee cómo
   se relacionan ADR-035/037/038/039 y este documento.

*BRN · Ciclo de Vida y Molde · Dylus Lab © 2026 · "Una regla nace de una cadena, se representa en una lógica, se mide en un motor y se explica en un dominio. El molde es el mismo para las 80 que vendrán — por eso se decide una vez, y cambiarlo después es un ADR, no un parche."*
