# BRN v2 · Matriz de Cobertura del Molde

> **Qué es.** La tabla que mide **objetivamente** cuánto está validado el molde CNO/RO — para decidir
> con evidencia, no con percepción, cuándo está listo para escalar a los 222 cantones (recomendación
> del colega · 2026-07-18). Cada dominio prueba una faceta distinta del modelo. Se actualiza al
> cerrar cada CNO.

## Los 4 invariantes que cada dominio debe cumplir
1. **El molde sirve** para ese dominio (la cadena se modela como CNO; la lógica, como RO).
2. **El compilador no cambia al incorporar el dominio** (matiz del colega · 2026-07-18: el compilador
   *sí* evolucionó durante el diseño, y era normal; el criterio de generalidad es que **agregar d05,
   d06 o d222 no toque su lógica** — `if dominio==...` = fuga).
3. **El runtime tampoco cambia** (resuelve vigencia igual para todos).
4. **Solo cambia el contenido de la RO** (la estructura del molde se mantiene).

## Matriz
| Dominio | Naturaleza de la regla | CNO | RO | Compilador | Runtime | Estado |
|---|---|---|---|---|---|---|
| **d02 · Finanzas** | umbral cuantitativo (65/70%) | ✓ vigente · 6/6 SHA | ✓ vigente | ✓ compila | ✓ | **Conforme v2.1** |
| **d03 · Mandato** | congruencia programática (fidelidad ≥85%) | ✓ vigente · 9/9 SHA | ✓ vigente | ✓ compila (sin `if`) | ✓ | **Conforme v2.1** |
| **d09 · Rendición** | obligación de hacer: plazo · contenido mínimo · cierre público | ✓ vigente · 10/10 SHA | ✓ vigente | ✓ compila · **diff infra = 0** | ✓ | **Conforme v2.1** |
| d01 · Planificación | — | pendiente | | | | Pendiente |
| … | | | | | | |

> **Lenguaje (colega · 2026-07-20):** no se habla de "dominios certificados" sino de **dominios
> conformes al contrato BRN v2.1**. El objeto estable es el **contrato**; los dominios simplemente
> lo satisfacen. Eso mantiene la plataforma en el centro y evita que cada dominio se vuelva un caso especial.

## Ciclo repetible de incorporación (BRN v2.1)
Estabilizado tras d09; se repite igual para d01, d05… y para los 222 cantones:
```
1. Seleccionar dominio (por estrés arquitectónico, no por importancia)
2. Modelar CNO (puro Derecho · SHA por eslabón)      → docs/brn/CNO-*.yaml
3. Modelar RO (métrica · parámetros · método)        → docs/brn/RO-*.yaml
4. Ejecutar la suite (12/12 verde)
5. Verificar Infrastructure diff = 0 (check 12)
6. Aprobación formal de Javo → `vigente` → conforme al contrato BRN v2.1
```
**Los pasos 2-3 tocan SOLO `docs/brn/`.** Si en el paso 5 aparece diff en `scripts/`, se detiene la
incorporación y se abre un ADR de evolución de plataforma (v2.2/v3). Nunca un parche ad hoc.

## Lectura del examen d03 — los 4 invariantes CONFIRMADOS
d03 era la prueba dura: su regla **no** desemboca en un techo de gasto sino en un **procedimiento de
congruencia** (promesa→plan, ponderado). Resultado con ambas CNO/RO ya `vigentes` y compiladas:
1. **El molde sirve** ✅ — cadena de 9 eslabones (CE·COD·COOTAD·COPLAFIP·LOPC) con SHA verificado; la
   lógica de medición (umbral 85% + método estructurado) cabe en la RO sin forzar el molde.
2. **El compilador no cambió** ✅ — 0 ramas de dominio; el mismo `_parametros_de` (el **adaptador**,
   único punto que conoce la estructura YAML) procesó la RO del mandato y la financiera.
3. **El runtime** ✅ — el compilador emite ahora **2 RO vigentes → 3 filas** (d02 con 2 tramos, d03
   con 1); el runtime resuelve la vigencia igual para ambos.
4. **Solo cambió la RO** ✅ — molde, catálogo y compilador intactos; la suite de regresión (7/7) verde.

**Conclusión (con el matiz del colega · 2026-07-18):** el molde queda validado sobre **dos CLASES de
dominio** — el **financiero** (d02, umbral) y el **programático** (d03, congruencia). No se afirma que
sirva para *cualquier* dominio imaginable: se afirma, con evidencia, que sirve para estas dos clases,
y que la suite protege esa propiedad al añadir la siguiente. Es el salto de "caso de uso" a "modelo".

## Prueba de transversalidad — d09 (2026-07-20)
d09 se eligió **por capacidad de estrés arquitectónico**, no por importancia (criterio del colega):
d01 comparte demasiada semántica con d03 y habría validado poco. d09 introduce una naturaleza que
**ninguno de los dos anteriores ejercía**: una obligación de **hacer** (plazo · contenido mínimo ·
deliberación pública · consecuencia por incumplimiento), sobre una cadena que suma el Reglamento
CPCCS al bloque constitucional y legal.

**Resultado:** cadena de **10 eslabones íntegros**; la RO cupo en el molde de tres planos con
`umbral: 100` (obligación que no admite cumplimiento parcial) y método de verificación documental.
**`Infrastructure diff = 0`** — no se tocó adaptador, compilador, contrato ni catálogo. Suite 12/12.

**Ciclo de 6 pasos cerrado por primera vez completo (2026-07-20)** — con la condición que lo hace
válido cumplida (precisión del colega): la **aprobación formal de Javo promovió** CNO-IX-001 y
RO-IX-001 a `vigente`. El compilador pasó de 2 a **3 RO vigentes (4 filas)** sin una línea de cambio
en `scripts/`. La documentación no anticipó el estado: lo registró cuando ocurrió.

**Formulación prudente (precisión del colega · 2026-07-20):** *la evidencia empírica disponible
muestra que el contrato BRN v2.1 ha incorporado satisfactoriamente **tres clases distintas de reglas**
—cuantitativa, programática y obligación de hacer— **sin requerir modificaciones de infraestructura**.*
No se afirma generalidad absoluta ni "transversalidad demostrada": tres dominios son evidencia
sustancialmente más fuerte que uno, pero no una demostración. Cada dominio nuevo **fortalece —o
eventualmente cuestiona—** el modelo; el lenguaje debe dejar espacio para lo segundo sin obligar a
retractarse de afirmaciones excesivas.

## Criterio de escalamiento a 222 cantones
El molde se considera **suficientemente respaldado para escalar** cuando ≥2 dominios de **clase
distinta** cumplen los invariantes con CNO/RO `vigentes` y compiladas. **Estado hoy: cumplido** —
d02 (cuantitativa) y d03 (programática) conformes; d09 (obligación de hacer) incorporado con
`diff = 0`, pendiente de aprobación formal. El siguiente dominio ya no *valida* la arquitectura: la
*ejerce*. No se escala por percepción — esta tabla lo muestra, y admite que la evidencia siga creciendo.

## Evolución prevista (colega · 2026-07-18 · refinamiento, no fundamento)
No urgente; se abordará cuando aparezca la necesidad, cada una con su ADR si toca decisión:
- **Método estructurado** — ✅ hecho (RO-III-001: `metodo.tipo` + `criterios` como lista de objetos,
  extensibles con peso/obligatorio/origen sin romper compatibilidad).
- **Adaptador formalizado** — ✅ hecho (`brn_ro_adapter.py`: `RO YAML → ROModel estable → compilador·
  catálogo`). Único punto que conoce el YAML; si BRN v3 cambia claves, solo cambia el adaptador.
- **Pruebas semánticas** — ✅ hecho (suite checks 8-10: vigencia por fecha, medición real, esquema).
- **Gobernanza de estados** — ✅ documentada (molde §3b: revisión técnica ≠ aprobación formal).
- **Artefacto multi-consumidor** — cuando haya más consumidores (Dashboard·API·Auditor·IA), el
  artefacto podría estructurarse en `runtime · metadata · provenance · schema`.
- **BRN Readiness Index** — convertir esta matriz en un índice con puntaje por dominio (Corpus·CNO·
  RO·SAT·Compilación·Validación·Runtime·Evidencia) para medir objetivamente la madurez de producción.
- **Tipos de métrica** (candidato **v3** · colega 2026-07-20) — hoy toda métrica se expresa como
  porcentaje, y `umbral: 100` en d09 fuerza una obligación jurídica a forma porcentual. Una obligación
  de hacer es naturalmente **booleana**. El contrato podría admitir
  `metrica.tipo: porcentaje | booleana | ordinal | cardinal` (d02/d03 porcentaje · d09 booleana o
  índice compuesto). **No se cambia hoy**: exigiría tocar adaptador y compilador → ADR de evolución.
- **ROAdapter → parser formal** (candidato v2.2/v3 · colega) — evolucionar de adaptador a parser con
  fases explícitas: `YAML → validaciones estructurales → validaciones semánticas → ROModel`. Permitiría
  errores expresivos ("falta criterio obligatorio", "vigencia mal formada") **sin afectar al compilador**.

---
*BRN v2 · Matriz de Cobertura · Dylus Lab © 2026 · "El molde no está validado porque funcione una vez, sino cuando dos reglas de naturaleza distinta pasan por él sin que el compilador se entere de la diferencia. Ese punto ya se cruzó."*
