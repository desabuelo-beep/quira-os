---
id: ADR-059
authority:
  parent: ADR-043
  constitution_articles: [4, 6, 8]
  type: ARQUITECTONICA
status: PROPUESTO — pendiente del sello de Javo (ADR-035 §5) · revisión 1
fecha: 2026-09-19
complementa:
  - ADR-041 §4-ter (la licencia de gestión al GAD)
  - ADR-043 §4, fila «QUIRA Institucional»
---

# ADR-059 · El norte del ecosistema QUIRA · evidencia abierta, fronteras claras e independencia económica

> **Contexto.** Javo (2026-09-19), en un paréntesis durante `D1`: *“¿es viable aterrizar todas las QUIRA
> como un único ecosistema… cada quien desde sus espacios, fronteras, reglas y delimitaciones… un ecosistema
> abierto sin costos?”* Y después de leer al colega: *“quizá eliminar QUIRA Institucional, vender software a
> los municipios, deba eliminarse, y potenciar el marketplace / network effects como norte… debe quedar
> guardado… sin perder este norte.”*
>
> ⚖️ **Alcance.** Este ADR guarda un **norte** y ordena **cómo se financia** sin perder la independencia.
> **No amplía QUIRA 7, no crea dominios, no toca el motor ni el canon técnico y no autoriza ninguna
> implementación.** La copia que el colega guardó vive en su propio entorno; **ésta es la del repositorio.**
>
> 🔁 **Revisión 1 (2026-09-19).** Javo dudó de cerrar la licencia y del principio de independencia por los
> ingresos. Al releer la Hoja de Ruta, la dirección técnica encontró lo que había pasado por alto: QUIRA
> Institucional **no es sólo un producto; es el Motor 3 de adquisición** —“el GAD usuario entrega sus datos
> operativos directos”—. Cerrarla como se había propuesto habría cortado **un canal de evidencia**, no sólo un
> ingreso. **Cambian 2.1 y 2.2; se añade 2.4; el §3 registra la decisión de Javo sobre Impact.**

## 1 · No es una idea nueva: el canon ya la contiene

| la idea del paréntesis | dónde ya es canon |
|---|---|
| un ecosistema, no productos aislados | `docs/corpus_externo/QUIRA_ECOSYSTEM_2026_2030.md` (2026-05-31): “No es un software. Es una infraestructura independiente de observación territorial.” · `HOJA_DE_RUTA_MAESTRA §1` |
| cada QUIRA con su función, **sin su propia verdad** | `ADR-043 §3`, regla 3: “Ningún producto QUIRA constituye una fuente independiente de verdad.” · `ADR-041 §3`: un motor, dos entradas |
| ciudadanos, OSC y academia **aportan** evidencia | `ADR-045` y `ADR-046`: una superficie, tres custodias; el techo lo fija el documento, no quien lo trae |
| el GAD como fuente **voluntaria** del mejor dato | `HOJA_DE_RUTA_MAESTRA §0`, Motor 3: “donde el GAD coopera: dato ORO; donde no: Motores 1+2 lo cubren igual” |
| el conocimiento público es del territorio | Constitución Institucional, Art. 4 y Art. 6 |
| el GAD es sujeto observado, no cliente | `BOOT §LA TESIS` |

## 2 · Lo que se decide al sellar

### 2.1 · QUIRA Institucional se conserva; lo que se decide es **quién paga**

El canon le da dos papeles: **Motor 3 de adquisición** (`HOJA §0`) y **herramienta de gestión** (`ADR-041`,
`ADR-043`). Ninguno se cierra. La licencia sigue **diferida**, como ya dice `BOOT §LA TESIS` (“⛔ NO se
presenta hasta operar varios GAD”), y **quién paga** se decide con cobertura y datos, no ahora:

| quién paga la herramienta del GAD | independencia |
|---|---|
| **un tercero**: la cooperación financia el fortalecimiento institucional del GAD | la más alta — el GAD no es cliente |
| **nadie**: parte del bien público, financiado por las otras líneas | alta |
| **el GAD**, por licencia | sólo con las reglas de 2.2 y después de tener cobertura |

### 2.2 · Independencia económica — **tres reglas**

> 1. **Ningún ingreso depende de lo que una observación dice.**
> 2. **Ningún pago compra el alcance, el método ni el resultado de una observación.**
> 3. **Toda relación comercial con un sujeto observado es pública, y su observación es reproducible por
>    terceros** con las fuentes públicas y el método publicado.

**Por qué tres reglas y no “ningún dinero del observado”.** La versión estricta cierra también ingresos que no
compran influencia. Las lecciones conocidas no están en quién paga, sino en **qué compra el pago**:

- **las calificadoras de riesgo antes de 2008**: el emisor pagaba a quien lo calificaba, y la calificación se
  volvió complaciente → lo impide la **regla 2**;
- **los auditores después de Enron**: la ley de EE. UU. (Sarbanes-Oxley, 2002) prohibió al auditor vender
  ciertas consultorías a la empresa que audita → lo recoge **2.4**.

**Lo que QUIRA tiene y ellos no:** la **reproducibilidad**. Si un tercero —una universidad, vía Impact— puede
rehacer la observación con las fuentes públicas y el método publicado, cualquier sesgo comprado se vuelve
**detectable**. La regla 3 convierte esa propiedad técnica en garantía comercial.

> ⚠️ **A revisar antes de ofrecerla:** `HOJA §0` cuenta la **“certificación de integridad”** en el negocio
> central. Si la paga el certificado, es exactamente el modelo de las calificadoras y **no pasa la regla 2**
> tal como está planteada.

### 2.3 · El norte: la **red**; el marketplace es el último piso, no el primero

| capa | qué es | costo |
|---|---|---|
| **evidencia pública** | dato, evidencia, indicador y metodología publicados | **abierta** — Constitución Institucional, Art. 4 |
| **capacidad de trabajar sobre ella a escala** | acceso avanzado, series y método reproducible, expedientes | servicio — contratos de **Impact** y **Cooperación** (`ADR-043 §4`) |
| **red** (*network effects*) | actores que encuentran oportunidades sobre evidencia común | el **norte** |

La Constitución Institucional ya describe el efecto de red: su Art. 6 dice que cada incorporación incrementa
el patrimonio cognitivo colectivo. **La red es el norte; lo que se decide es el orden de los ingresos:**

| etapa | ingresos | paga |
|---|---|---|
| **hoy** | consultoría de formulación (2.4) · fondos de cooperación para QUIRA como bien público | clientes de la consultoría · cooperación |
| **con varios GAD observados** | **Cooperación** (elegibilidad, expediente, seguimiento) · **Impact** (datos, series, método a escala) | financiadores · academia, ONG, observatorios |
| **con cobertura nacional** | la **red** | **membresía** de los participantes — **no comisión por conexión**: una comisión por cada necesidad conectada haría ganar más cuanta más necesidad se muestre, y eso toca la observación (regla 1) |

### 2.4 · La consultoría de formulación: **fuera de QUIRA, dentro de Dylus Lab**

La formulación de proyectos de financiamiento —el oficio que hoy genera ingresos— **no se pierde: se ubica.**

- **No dentro de QUIRA Cooperación.** Cooperación sirve al **financiador** (`ADR-043 §4`). Si también
  formulara para quien pide el financiamiento, QUIRA estaría **a los dos lados de la misma operación**.
- **No con la marca QUIRA.** La marca QUIRA *es* la independencia; prestarla a un servicio pagado por
  entidades observadas la gasta. Una línea de **Dylus Lab** con nombre propio.
- **Cuatro reglas:**
  1. usa **la misma evidencia pública** que cualquiera — ningún acceso privilegiado;
  2. **no ve antes ni influye** en la observación de sus clientes;
  3. **sus clientes son públicos** (regla 3 de 2.2);
  4. **nunca a los dos lados** de una misma operación de financiamiento.
- **Sin conflicto alguno:** ONG, OSC, organizaciones comunitarias, y los GAD parroquiales y provinciales
  mientras estén fuera del universo observado.
- ⚠️ **Honorarios por éxito:** muchos financiadores no admiten pagarlos con los fondos del proyecto —
  verificarlo con cada uno.
- La **forma jurídica y tributaria** (misma empresa o sociedad aparte) se define con un contador o abogado
  local.

## 3 · Las diferencias con el texto del colega

| tema | resolución |
|---|---|
| **Impact** como medición de resultados (MRV) que devuelve evidencia al Observatorio | ✅ **Decidido por Javo (2026-09-19): Impact conserva la misión de `ADR-043`** —abrir el conocimiento a escrutinio; “NO genera evidencia primaria”—. El seguimiento de lo financiado es de Cooperación, y la evidencia de resultados **vuelve a entrar por las custodias del Observatorio** |
| la familia de cuatro QUIRA | **Economic** sigue como línea futura (`ADR-043 §4`: “no se elimina y no se fusiona con Cooperación”) |

## 4 · Lo que decide la dirección

| # | decisión | recomendación de la dirección técnica |
|---|---|---|
| 1 | **Institucional**: se conserva como Motor 3 y como herramienta; la licencia sigue diferida; quién paga se decide con cobertura (2.1) | **sellar** |
| 2 | **independencia económica**: las tres reglas (2.2) | **sellar** |
| 3 | **consultoría**: línea de Dylus Lab, fuera de QUIRA, con cuatro reglas (2.4) | **sellar** |
| 4 | **Impact** conserva su misión | ✅ **decidido** |
| 5 | **norte = red**, con el orden de ingresos de 2.3 y membresía en lugar de comisión | **sellar como horizonte** |
| 6 | **certificación de integridad** de `HOJA §0` | **revisar** con la regla 2 antes de ofrecerla |

## 5 · Qué cambia cuando se selle — y no antes

| dónde | cambio |
|---|---|
| `BOOT §LA TESIS` | «Licencia de gestión al GAD SÍ (§4-ter)» → **licencia diferida; quién paga: ADR-059 §2.1** |
| `governance/QUIRA_MASTER_INDEX.md` | ADR-059 como rector del norte del ecosistema |
| `HOJA_DE_RUTA_MAESTRA §0` | la certificación de integridad, a revisar (punto 6) |
| `ADR-041 §4-ter` y `ADR-043 §4` | se **complementan**, no se editan (`ADR-043 §6-bis`) |
| QUIRA 7 | **nada nuevo**: el trabajo de sujeto + dominio + evidencia + tiempo **ya es** el sustrato común que este norte necesita; `D1` sigue su curso |

---
*ADR-059 · Dylus Lab © 2026 · propuesto por la dirección técnica sobre el paréntesis de Javo y la lectura del
colega · deriva de ADR-043 · **PROPUESTO, sin sellar** · revisión 1.*
