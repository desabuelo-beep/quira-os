# CATALOGO_CANONICO_CD_D07_v1.0 — d07 Transparencia

> **Estado:** ✅ **CERRADO Y CONGELADO como baseline** · v1.0 · 2026-07-22
> **Declarado Single Source of Truth** (colega, 2026-07-22): a partir de esta versión, ningún
> cambio conceptual de d07 nace en el Excel, YAML, SQL, JSON o API — nace aquí y se propaga hacia
> esos artefactos (Regla 9). Numeración verificada contra LOTAIP vigente (corpus); campos de
> scoring detallado marcados honestamente "pendiente" hasta el levantamiento del Portal (Fase 4).
>
> Filtro aplicado: solo **Art. 19** (obligaciones generales, aplican a todo sujeto obligado) +
> **Art. 24** (obligaciones específicas de GAD). Se excluyen Art. 20/28/29/30 (Min. Finanzas,
> Partidos Políticos, Empresas Públicas nacionales, IESS) — no aplican a un GAD municipal.
>
> **Alcance ratificado (Javo, 2026-07-22): solo GAD.** Las EP (EPAM/Aseo) y desconcentradas
> (Bomberos, Patronato) del holding municipal de Montecristi **no entran a este catálogo** — cada
> una es sujeto obligado propio con su propio portal LOTAIP. Su transparencia se trabaja cuando se
> construya el **DOM de Holding Municipal** (d05, "Holding e Integración Municipal"), reusando este
> mismo Catálogo CD-XX y algoritmo SITA (son genéricos, aplican a cualquier sujeto obligado), no
> reconstruyendo el estándar de nuevo.

## Supuestos explícitos (colega, 2026-07-22 — para que nadie los confunda con "olvidos")

- **Alcance limitado a GAD municipal.** No incluye EP (EPAM, Aseo), no incluye desconcentradas
  (Bomberos, Patronato), no incluye Holding Municipal, no corresponde al dominio **d05**. Exclusión
  **deliberada**, no pendiente — se retoma cuando se construya d05, reusando este catálogo.
- **Filtro Art.19 + Art.24.** Excluye Art.20/28/29/30 (Min. Finanzas, Partidos, Empresas Públicas
  nacionales, IESS) — no aplican a un municipio.
- **Fase 4 (evidencia real de portal) suspendida por presupuesto de API** (2026-07-22, Javo): sin
  crédito Haiku hasta que Javo confirme recarga. Este documento queda **listo para ejecutar**, no
  se ejecuta hoy.

## Metamodelo CD (colega, 2026-07-22 — el esquema, no solo la tabla)

Cada CD es una instancia de este objeto (ya aplicado a CD-06 en METODOLOGIA_D07 §6b; aquí se
generaliza a los 23):

```
CD {
    Identificación:      código CD-XX, nombre, numeral(es) de ley
    Dominio:              d07 (± dominios cruzados, ver DOMINIOS_QUIRA en ACKs)
    Fuente normativa:     LOTAIP + RLOTAIP
    Fuente operativa:     GUIA-LOTAIP-MEC (id·SHA) + INST-TA-2024 (formato Anexo 1)
    Formato DPE:          nombre del formato oficial
    Componentes[]:        sub-partes internas si la ley las especifica (ej. CD-06, CD-01)
    Campos[]:             campos obligatorios del conjunto de datos (⬜ transcripción pendiente)
    Reglas[]:             CTA/ETA/RP/CI (genéricas, METODOLOGIA_D07 §4b)
    Evidencias[]:         {url, sha256, fecha_verificación} — por componente, Fase 4
    Validaciones[]:       vigencia/validez cuando aplique (Tablas 4/5 Instructivo)
    Score:                SITA agregado
    Estado de evidencia:  Normativa · Operativa · Empírica (tabla abajo)
    Observaciones:        libre
}
```
Este esquema es la definición formal de la fila — el YAML actual (`data/d07/catalogo_cd_d07_v1.0.0.yaml`)
implementa hoy el subconjunto ya poblado (Identificación, Dominio, Fuente, Componentes); `Campos[]`,
`Evidencias[]`, `Validaciones[]` existen en el metamodelo pero se materializan en Fase 4 (auditoría
2026-07-23: verificado, no es pérdida de datos, es diseño anticipado sin ejecutar aún).

## Contrato de la Evaluación mensual (colega, 2026-07-22 — diseñar ahora, llenar con Haiku después)

**Clave lógica** (misma granularidad para Neo4j, JSON, Excel, reportes y hallazgos):
```
EvaluationID = Municipio + Dominio + CD + Periodo(AAAA-MM)
```
El CD es la unidad de estándar; la **evaluación** es `CD × mes`. Un CD produce N filas (una por mes de 2025-2026), no una.

**Esquema de fila de evaluación** (estructura DEFINITIVA; los `Score` nacen vacíos hasta el 1er piloto Haiku):

| Campo | Tipo | Origen | Estado hoy |
|---|---|---|---|
| `evaluation_id` | clave | Municipio+DOM+CD+Periodo | definido |
| `municipio` · `dominio` · `cd` · `periodo` | dimensiones | fijas | definido |
| `fuente` | url/formato | Portal (Navigator) | ⬜ Fase 4 |
| `cta` · `eta` · `rp` · `ci` | score 0-1 | Interpreter → reglas §4b | ⬜ Fase 4 (vacío) |
| `sita_cd` | 0-1 | (cta+eta+rp+ci)/4 | ⬜ deriva de lo anterior |
| `estado` | LEGACY \| VERIFIED \| PENDIENTE | motor | **LEGACY** hoy |
| `evidencia` | {url, sha256, fecha} | Collector | ⬜ Fase 4 |
| `observacion` | narrativa | Report Generator (IA) | ⬜ Fase 5 |

**Lo que NO se diseña todavía** (nace del 1er piloto, no de supuestos): columnas auxiliares,
observaciones específicas, excepciones, categorías nuevas. La estructura base está fija; los
detalles emergentes esperan evidencia real.

## Ficha tipo (por CD)

| Campo | Fuente |
|---|---|
| Código | convención `CD-XX` (Diccionario de Siglas) |
| Nombre | Guía Metodológica / Instructivo |
| Artículo(s) de ley | LOTAIP Art.19 (verificado contra corpus 2026-07-22) |
| Formato oficial | Anexo 1, Instructivo `INST-TA-2024` |
| Fuente normativa | LOTAIP + RLOTAIP |
| Fuente operativa | `GUIA-LOTAIP-MEC` + `INST-TA-2024` |
| Campos obligatorios | ⬜ pendiente (Fase 4 — requiere el formato/diccionario de datos real) |
| Reglas CTA/ETA/RP/CI | genéricas, ya reconstruidas (METODOLOGIA_D07 §4b) — se aplican igual a todo CD |
| Evidencia requerida | ⬜ pendiente (URL portal + SHA, por CD) |
| Score SITA | ⬜ pendiente (Fase 4, Montecristi) |
| Observaciones | libre |

## Catálogo (Art. 19 · 23 CD + Art. 24 · 1 CD)

**Tres niveles de evidencia (colega, 2026-07-22 — reemplaza el estado único anterior):**
- **Normativa** = Ley + Reglamento (obligación jurídica, general para todo el Art.19)
- **Operativa** = Guía + Instructivo (id·SHA propio por CD, extraído 2026-07-22)
- **Empírica** = evidencia real del portal Montecristi (Fase 4, suspendida por presupuesto)

| CD | Numeral(es) | Nombre | Normativa | Operativa (Guía id·SHA) | Empírica | Observaciones |
|---|---|---|---|---|---|---|
| CD-01 | 1 | Estructura orgánica + base legal + metas | ✔ | ✔ id 14333/14335/14337 | ☐ | **árbol de 3 sub-formatos**, un solo CD |
| CD-02 | 2 | Directorio y distributivo de personal | ✔ | ✔ id 14338·`47d5c63d41` | ☐ | — |
| CD-03 | 3 | Remuneraciones salariales | ✔ | ✔ id 14339·`fbbcdf5f0e` | ☐ | CI valida "Total ingresos adicionales" = suma componentes (Instructivo Tabla 5) |
| CD-04 | 4 | Licencias/comisión de servicio | ✔ | ✔ id 14340·`d9d1a19288` | ☐ | — |
| **CD-05** | **5+22** | Servicios + formularios de trámites | ✔ | ✔ id 14341·`5e27a9a3d7` | ☐ | **corrección 2026-07-22:** el propio "Conjunto de datos" de la Guía ya incluye el enlace a formularios — la Guía SÍ une 5+22, no solo el Instructivo |
| **CD-06** | **6** | Presupuesto Institucional | ✔ | ✔ id 14342·`9b50ff1592` | **✔** | **árbol+entidad** (§6b). Ingresos ausente en Montecristi (OBS-011). Sin video de capacitación (§5b) |
| CD-07 | 7 | Auditorías internas/gubernamentales | ✔ | ✔ id 14343·`e9f4d38340` | ☐ | — |
| CD-08 | 8 | Contratación (precontractual→liquidación) | ✔ | ✔ id 14344·`be252c5009` | ☐ | — |
| CD-09 | 9 | Empresas que incumplieron contratos | ✔ | ✔ id 14345·`ec64c0df9d` | ☐ | — |
| CD-10 | 10 | Planes y programas | ✔ | ✔ id 14346·`c51d4955ac` | ☐ | — |
| CD-11 | 11 | Contratos de crédito | ✔ | ✔ id 14347·`cf2ef7f783` | ☐ | — |
| CD-12 | 12 | Mecanismos de rendición de cuentas | ✔ | ✔ id 14348·`1fc319d264` | ☐ | conecta con d09 |
| CD-13 | 13 | Viáticos | ✔ | ✔ id 14349·`414116b17d` | ☐ | — |
| CD-14 | 14 | Responsable de acceso a la información | ✔ | ✔ id 14350·`123c0c355d` | ☐ | — |
| CD-15 | 15 | Contratos colectivos vigentes | ✔ | ✔ id 14351·`e7c409c65c` | ☐ | — |
| CD-16 | 16 | Índice de información reservada | ✔ | ✔ id 14352·`a7bd15f17f` | ☐ | CI valida vigencia (Instructivo Tabla 4) |
| CD-17 | 17 | Audiencias y reuniones de autoridades | ✔ | ✔ id 14353·`46eab0be54` | ☐ | — |
| CD-18 | 18 | Convenios nacionales/internacionales | ✔ | ✔ id 14354·`984b95ca6d` | ☐ | CI valida vigencia (Instructivo Tabla 4) |
| CD-19 | 19 | Donativos oficiales y protocolares | ✔ | ✔ id 14355·`bcb7cbd47a` | ☐ | — |
| CD-20 | 20 | Registro de activos de información | ✔ | ✔ id 14356·`a93dda6314` | ☐ | — |
| CD-21 | 21 | Políticas públicas / grupo específico | ✔ | ✔ id 14357·`17bbfd0611` | ☐ | — |
| CD-23 | 23 | Cuotas laborales (discapacidad/pueblos) | ✔ | ✔ id 14358·`14b51ad72f` | ☐ | — |
| CD-24 | 24 | Información relevante adicional (ODS) | ✔ | ✔ id 14359·`f64155a202` | ☐ | — |
| **CD-A24** | Art.24 (GAD) | Ordenanzas/actas de sesión/contratación | ✔(Ley) | ☐ pendiente | ☐ | específico de GAD, fuera del rango extraído hoy |

**Lectura:** 22/23 CD con Normativa+Operativa completas. Solo CD-06 tiene Empírica (evidencia real
Montecristi). CD-A24 es el único con Operativa pendiente. Esto **es** la lista de trabajo exacta
de Fase 4 cuando haya presupuesto: recorrer la columna Empírica de arriba a abajo.

**Nota de numeración (corregida 2026-07-22 tras validar contra el grafo real, 24 nodos `:CD`):** el
numeral 22 de la ley no genera un CD propio — se fusiona en CD-05. El Art.19 tiene 23 numerales
únicos tras esa fusión (1-21, 23, 24), no 22 — error aritmético detectado al cargar Neo4j y
corregido aquí. El catálogo tiene **23 CD del Art.19 + 1 del Art.24 = 24 CD totales**.

## Producto C.5 — Validación cruzada (colega, 2026-07-22) — ✅ CERRADA

No genera documentos nuevos: verifica cada CD contra sus 4 fuentes.

| Fuente | Cobertura final | Cómo se verificó |
|---|---|---|
| **Ley** (LOTAIP Art.19) | ✔ **23/23 CD** | texto literal consultado directo en el corpus (un solo artículo continuo) |
| **Reglamento** (RLOTAIP) | ✔ **general**, no por CD individual | Art.11/12 consultados directo en corpus 2026-07-22 — confirman lo citado por el Instructivo; el Reglamento no desglosa por numeral, no aplica verificación CD-por-CD |
| **Guía** (`GUIA-LOTAIP-MEC`) | ✔ **23/23 CD** | **extracción dirigida por posición secuencial** (ids 14332-14359, un solo query 2026-07-22) — cada "Conjunto de datos" mapeado a su numeral por orden real de aparición en el documento, con id+SHA256 propios |
| **Instructivo** (`INST-TA-2024`) | ✔ **23/23 CD** | Anexo 1, Tablas 6-19, nombre de formato extraído literal para cada numeral |
| **Formato/evidencia real** | ✔ solo **CD-06** (CSV oficial del portal) · ⬜ 22 restantes | pendiente Fase 4 (levantamiento portal Montecristi) |

**Matriz resultante:**

| CD | Ley | Reglamento | Guía | Instructivo | Formato real | Estado |
|---|---|---|---|---|---|---|
| CD-06 | ✔ | ✔(general) | ✔ | ✔ | ✔ | **Validado (Montecristi)** |
| CD-05 | ✔ | ✔(general) | ✔ | ✔ | ✖ | Estándar completo |
| resto (21 CD) | ✔ | ✔(general) | ✔ | ✔ | ✖ | Estándar completo |
| CD-A24 | ✔(Art.24) | — | ⬜ | ⬜ | ✖ | Pendiente |

**Conclusión de la validación cruzada:** el estándar oficial (Ley+Reglamento+Guía+Instructivo)
queda **reconstruido al 100%** para los 23 CD del Art.19 (CD-A24 del Art.24 GAD queda pendiente,
fuera del rango extraído hoy). Lo único que falta para cualquier CD, salvo CD-06, es la
**evidencia real del portal** — que es tarea de Fase 4, no de reconstrucción del estándar. El
Producto C ya no tiene un eslabón débil documental: **se declara cerrado.**

## Pendiente explícito (no se inventa, se declara) — queda para Fase 4, no bloquea el cierre de Producto C

- **CD-A24** (Art.24 GAD) — Guía/Instructivo aún no extraídos para este artículo; el resto (23 CD
  del Art.19) sí está completo.
- **Campos obligatorios completos por CD** — tengo el texto íntegro de cada chunk de Guía (id+SHA
  ya fijados); falta el desglose campo-por-campo formal en esta ficha — es transcripción, no
  investigación nueva.
- **Evidencia (URL/SHA) real de portal por CD** — se levanta en la Fase 4 sobre Montecristi.
- **Reglas de vigencia (Tabla 4 Instructivo)** aplican solo a CD-16, CD-18 y formatos del Art.21
  (fuera de este filtro GAD) — confirmado con evidencia, resto de CD no las requiere.
- **CD-03** es el único con regla de **validez** documentada explícitamente en el Instructivo
  (Tabla 5, "Total ingresos adicionales") — no se generaliza a otros CD sin evidencia igual.

## Cierre — Producto C

**CATALOGO_CANONICO_CD_D07_v1.0.0 queda congelado como baseline y Single Source of Truth de d07.**

**Regla de gobernanza (colega, 2026-07-22):** Gold Master v1.0 (d07) deriva de Catálogo v1.0.0.
Cualquier modificación futura (nuevo CD, cambio de agrupamiento, nueva regla SITA) requiere un
**ADR explícito** antes de tocar Excel/YAML/SQL/JSON/API — nunca se edita el Excel primero. Cada
cambio incrementa versión (`v1.1.0`, `v2.0.0`...), nunca se sobrescribe v1.0.0 en silencio.

Roadmap siguiente: **Producto D — Metodología definitiva d07** (consolidación de este Catálogo +
METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP.md en un solo documento de cierre) — **en pausa** hasta
recargar presupuesto de API (Fase 4 la alimenta directamente).

---
*CATALOGO_CANONICO_CD_D07_v1.0 · Fase 0 Producto C · CERRADO 2026-07-22 · Dylus Lab © 2026*
