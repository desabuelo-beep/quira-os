---
id: OBS-029
authority:
  parent: ADR-047
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-12
dominio: d01 · d06 · motor
estado: VERIFICADA
---

# OBS-029 · Los otros tres verificadores — por qué no se pueden poblar hoy, y qué falta exactamente

> **Encargo de Javo (2026-08-12):** poblar `V_SERCOP`, `V_LOTAIP` y `V_CPCCS` para las metas
> restantes con la cadena que quedó funcionando en OBS-028.
>
> **Resultado: uno se deriva a medias y dos no se derivan.** Cada bloqueo tiene causa distinta y
> **acción concreta**. Ninguno se rellenó.

## El estado de los cuatro

| Verificador | Estado | Causa |
|---|---|---|
| `V_eSIGEF` | **derivado** · 46/66 | cadena POA → cédula operativa (OBS-028) |
| `V_SERCOP` | **parcial** · `0,5` para **42/66** | el PAC alcanza; la captura SERCOP no |
| `V_LOTAIP` | `sin_evidencia` | el monitoreo del portal nunca ha corrido |
| `V_CPCCS` | **no derivable** | la rendición de cuentas no cita las metas |

## 1 · `V_SERCOP` — la mitad sí, y la otra mitad sería falsa

El PAC resultó ser el puente que faltaba, y **no por analogía: el criterio de H13 para `V_SERCOP =
0,5` dice literalmente «proceso registrado en PAC»**. La cadena se extiende sola:

```
meta PDOT → POA (partida) → PAC (partida → objeto) → SERCOP (proceso adjudicado)
```

**PAC INICIAL 2025 GAD Montecristi** · 149 líneas · 64 partidas distintas · columna
`PARTIDA PRESUPUESTARIA` explícita.

| | |
|---|---|
| Partidas del POA presentes en el PAC | **62 / 143** |
| Partidas del PAC ausentes del POA | 2 |
| **Metas con al menos una línea de PAC** | **42 / 66** |
| Metas con partida pero sin línea de PAC | 4 |

Con eso `V_SERCOP = 0,5` queda **derivado deterministamente para 42 metas**.

### Por qué `1,0` y `0,0` se quedan sin derivar

La ingesta de SERCOP corrió **una sola vez** —`SERCOP_OCDS_API`, 2026-05-28— y su cobertura
temporal es parcial:

| Año | Procesos del GAD | Meses capturados | Monto |
|---|---|---|---|
| 2023 | 67 | 3,5,7–12 | $3,24 M |
| 2024 | **121** | 3–12 | $3,90 M |
| **2025** | **20** | **3–8** | $1,18 M |

**Faltan septiembre a diciembre de 2025**, y enero-febrero de todos los años.

> Una caída de 121 a 20 procesos no es un hallazgo sobre contratación: **es una captura
> incompleta.** Derivar `V_SERCOP = 0` de aquí afirmaría «no hubo proceso» cuando lo único cierto
> es «no lo capturamos» — el mismo defecto que OBS-028 acaba de documentar en los ceros de H13.

Dos límites adicionales, ambos verificados:

- **`estado` vale `por_verificar` en las 772 filas.** El campo del que depende el criterio
  «adjudicado» está sin poblar. Sólo 6 de 772 tienen proveedor.
- El enlace PAC → SERCOP por descripción alcanza **11 de 149 líneas**, y descansa en texto — con
  20 procesos disponibles no es medible si el método sirve o si sólo falta el dato.

## 2 · `V_LOTAIP` — no es un bloqueo, es una tarea pendiente

Se mantiene `sin_evidencia`, **que no es cero**. El criterio de H13 exige documento en URL pública
comprobada, y **el monitoreo del portal no se ha ejecutado ni una vez**. La Consola ya tiene el
mando (`app/observatorio/despacho.py` · procedimiento `transparencia`).

## 3 · `V_CPCCS` — la fuente existe y aun así no reconcilia

Corpus: **114 fragmentos · 317.432 caracteres** de los informes de rendición de cuentas 2023-2025.

| Prueba | Resultado |
|---|---|
| Metas cuyo enunciado aparece **literal** en la RDC | **0 / 66** |
| Metas con ≥3 términos sustantivos coincidentes | 36 / 66 |
| Metas con 1-2 términos | 28 / 66 |

**Ninguna meta del PDOT se cita literalmente en la rendición de cuentas.**

El 36/66 por términos coincidentes **no se usa**: es exactamente el emparejamiento por palabras
sueltas que OBS-026 descartó por no constituir evidencia. Usarlo aquí sería aplicar dos varas.

> **Estado: `no_reconciliado`, no `0`.** Que el informe no cite la meta no prueba que no la haya
> atendido; prueba que **el vínculo no es recuperable desde el instrumento publicado.**

### Y esto es, otra vez, un hallazgo sobre el instrumento

La rendición de cuentas es el acto por el cual el GAD informa sobre el cumplimiento de su plan. Que
**ninguna** de las 66 metas aparezca citada no es un detalle de redacción: significa que el informe
y el plan **no comparten identificadores ni enunciados**, y por tanto la correspondencia entre lo
rendido y lo planificado no puede reconstruirse documentalmente.

Es el mismo patrón de OBS-026 —el PDOT sin llave primaria— manifestándose un instrumento más
abajo. Y encaja en ADR-048: no es un defecto de gestión, es capacidad informacional.

## Lo que se necesita, en concreto

| Falta | Acción | Quién |
|---|---|---|
| SERCOP sep-dic 2025 y ene-feb de todos los años | **reejecutar la captura OCDS ampliando la ventana** | Consola · Operaciones |
| `estado` de adjudicación en 772 filas | poblarlo desde OCDS o marcarlo no disponible | Operaciones |
| `V_LOTAIP` | **primera corrida del monitoreo del portal** | Consola · `transparencia` |
| `V_CPCCS` | tabla de compromisos del CPCCS, o método distinto del textual | pendiente · sin fuente |

> Tres de los cuatro verificadores del motor no pueden completarse con las fuentes actuales, y
> **cada bloqueo tiene una acción nombrada**. Eso es un resultado de auditoría, no una carencia del
> trabajo: la ausencia de evidencia se declara, no se rellena.

## Trazabilidad

| Fuente | Carácter |
|---|---|
| `Varios/Oficiales/PAC INICIAL 2025 GAD MONTECRISTI…SUBSANADO (1).xlsx` | oficial · 149 líneas |
| `sercop_contratos` (Supabase) · 772 filas · `SERCOP_OCDS_API` 2026-05-28 | **cobertura parcial** |
| `normativa_corpus` · `tipo_documento='informe_rendicion'` · 114 fragmentos | oficial |
| `data/pdot/cruce_poa_cedula.json` | capa derivada |

---
*OBS-029 · Dylus Lab © 2026 · ningún verificador se pobló por conveniencia.*
