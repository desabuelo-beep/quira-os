# QUIRA — Beta Backlog
**Registro de deudas metodológicas y descubrimientos diferidos**

**Formato**: C10 → hallazgo → tarea Beta  
**Principio**: Ningún ítem aquí invalida Alpha. Son profundizaciones, no correcciones.  
**Custodio**: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO

---

## Cómo usar este backlog

Cada ítem nació de un hallazgo C10 (Reflexión Institucional) durante Alpha.  
El ítem documenta el hallazgo, su impacto en Alpha (si aplica) y la tarea Beta necesaria.  
Los ítems NO se tocan durante Alpha excepto para agregar nuevas entradas.

---

## DOMINIO 12 — Protección Social y Grupos Prioritarios

### BETA-DOM12-001 — Índices Complementarios de Impacto Social

**Hallazgo C10 (2026-05-31):**  
`Ti_G7+G8` mide ejecución presupuestaria (Piso 1 — compliance financiero).  
No mide cobertura efectiva, intensidad de atención, ni continuidad de servicio (Piso 2 — impacto territorial).

En servicios sociales intensivos en capital humano (diálisis, psicología, atención gerontológica, nutrición, educación inicial), puede coexistir:
- Ti financiero 🔴 ROJO + cobertura real 🟢 VERDE
- Ti financiero 🟢 VERDE + cobertura real 🔴 ROJO

**Impacto en Alpha:** ninguno. Ti=50% Patronato es correcto en su capa.

**Tarea Beta:**  
Recuperar índices complementarios de impacto social desde:  
`C:\Users\DELL\Desktop\Javo\Dylus Lab\Refactorización\varios\metodologicos antiguos\`
- `Metodologia SIAP-ICPI Final.md`
- `SIAP-ICPI_VERSION_CON_METODOLOGIA.xlsx`
- `TESIS DE LICENCIATURA EN CIENCIAS POLÍTICAS menos punitiva.docx`

Diseñar C8 de Piso 2 para Dom12:
- Cobertura adultos mayores (atendidos / población objetivo)
- Pacientes en programa diálisis (continuidad)
- NNA con seguimiento activo (JCPD + Patronato)
- Cobertura nutricional (beneficiarios / estimación INEC)

---

### BETA-DOM12-002 — Desagregación Ti por tipo de ejecución

**Hallazgo C10 (2026-05-31):**  
`Ti_G7+G8` agrega G71 (personal inversión) + G73 (programas/servicios) + otros.  
G71 y G73 cuentan historias diferentes:

```
G71 (personal inversión): Ti=67.60%  — estructura institucional presente
G73 (bienes/servicios):   Ti=29.73%  — ejecución de programas: CRISIS
```

Un Patronato puede pagar a su personal (G71) sin ejecutar los programas que ese personal debería entregar (G73). El Ti global oculta esta distinción.

**Impacto en Alpha:** ninguno. Ti=50% global sigue siendo correcto como indicador de compliance.

**Tarea Beta:**  
Crear sub-indicadores en IND_G10P_04:
- `Ti_personal_inversion` (G71 aislado)
- `Ti_programas` (G73+G77 aislado)
- `Ti_transferencias` (G78 aislado — transferencias a organismos de atención)

Umbral diferenciado: Ti_programas < 40% → señal de QUIRA de estructura sin funcionamiento.

---

### BETA-DOM12-003 — Efecto COOTAD reforma clasificación corriente/inversión

**Hallazgo C10 (2026-05-31):**  
La última reforma COOTAD cambió la clasificación de gastos corriente/inversión.  
Personal de programas sociales migró de G51 (corriente) a G71 (inversión).  
Esto puede haber:
1. Inflado el denominador Ti (más G71 = Ti más difícil de alcanzar)
2. Cambiado el ratio COOTAD_249 (el 10% aplica sobre una base diferente)
3. Creado incentivo para mostrar "inversión" que es en realidad nómina reclasificada

**Impacto en Alpha:** ninguno. La reforma no afecta la validez de los datos 2025.

**Tarea Beta:**  
Comparar estructura G51/G71 Patronato pre y post reforma.  
Verificar si H01 param Gold Master recalibró el piso COOTAD_249 para la nueva clasificación.  
Revisar si otros Patronatos manabitas tienen estructura similar → benchmarking.

---

## DOMINIO 4 — Planificación Territorial

### BETA-DOM04-001 — PDOT Montecristi atomizado

**Hallazgo C10 (implícito en Alpha 0.9):**  
El PDOT es la "Constitución Territorial" de Montecristi (Territorial Semantics v1.0, Sec. VII).  
Actualmente QUIRA usa el PDOT como referencia normativa general pero no como fuente estructurada de metas.  
Las propuestas PDOT (Dom01-Dom12) son las metas que QUIRA debería monitorear directamente.

**Impacto en Alpha:** ninguno. Las metas de referencia actuales son válidas.

**Tarea Beta:**  
Atomizar PDOT Montecristi con QLEP (extensión para documentos de planificación).  
Crear ACK tipo `meta_pdot` para cada propuesta del PDOT.  
Conectar C9 de cada QTMP a la meta PDOT correspondiente.  
Esto convierte "semáforo ROJO" en "regresión respecto a meta PDOT oficial".

---

## TERRITORIO

### BETA-TERRITORIO-001 — Microdatos INEC DPA 2022

**Hallazgo C10 (Territorial Semantics v1.0 — Sec. V):**  
El NBI parroquial en Montecristi está en estado `pendiente_microdato`.  
Los proxies disponibles (21.3% urbano / 53.3% rural) son zonales, no parroquiales.  
Parroquias urbanas con comunas rurales internas (CLR, MCU) tienen NBI subestimado.

**Impacto en Alpha:** ninguno. Proxies están documentados como `pendiente_microdato` + `validez: provisional`.

**Tarea Beta:**  
Alianza Red Académica (UEB/ESPAM) para procesar microdatos DPA 2022.  
Cruzar sectores censales con parroquias COOTAD.  
Convertir proxies en valores confirmados para RES_RES_EQUD_01_[parroquia].

---

## METODOLOGÍA GENERAL

### BETA-METODO-001 — Calibración indicadores con Red Académica

**Hallazgo C10 (Causal Model v1.0 — Sec. XIV):**  
Las hipótesis causales H1-H8 no tienen validación metodológica externa.  
Son plausibles y bien fundadas, pero no están calibradas con literatura territorial ni estándares INEC.

**Impacto en Alpha:** ninguno. Las hipótesis H están claramente marcadas como `estado: hipotesis`.

**Tarea Beta:**  
Presentar H1-H8 a Red Académica (FLACSO / IAEN preferidos para causalidad institucional).  
Solicitar revisión metodológica de: (a) validez de las cadenas, (b) estándar de confirmación.  
Resultado esperado: H confirmadas pasan a `estado: validado_academico`.  
Publicación potencial: artículo metodológico QUIRA / SIAP-ICPI.

---

## Registro de entradas

| ID | Dominio | Fecha | Origen | estado_metodologico |
|---|---|---|---|---|
| BETA-DOM12-001 | Dom12 | 2026-05-31 | Análisis Patronato G73 Ti=29% | pendiente_academia |
| BETA-DOM12-002 | Dom12 | 2026-05-31 | Ti=50% oculta G71 vs G73 | pendiente_academia |
| BETA-DOM12-003 | Dom12 | 2026-05-31 | Reforma COOTAD clasificación | pendiente_academia |
| BETA-DOM04-001 | Dom04 | 2026-05-31 | PDOT como Constitución Territorial | pendiente_construccion |
| BETA-TERRITORIO-001 | Territorial | 2026-05-31 | INEC DPA microdatos parroquiales | pendiente_datos |
| BETA-METODO-001 | Metodología | 2026-05-31 | Hipótesis H1-H8 sin validación externa | pendiente_academia |

**Valores de `estado_metodologico`:**  
`pendiente_academia` → hipótesis que requiere validación Red Académica  
`pendiente_datos` → espera microdatos o fuente primaria no disponible  
`pendiente_construccion` → requiere sprint de desarrollo  
`validado_academico` → confirmado por Red Académica  
`refutado` → invalidado, registrar aprendizaje  
`requiere_investigacion` → abierto como línea de investigación formal

---

*QUIRA Beta Backlog — iniciado 2026-05-31*  
*Formato vivo — agregar entradas según ciclos C10 — Dylus Lab*
