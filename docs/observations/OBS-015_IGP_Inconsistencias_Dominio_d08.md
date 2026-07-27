---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-015 · IGP del Gold Master — inconsistencias respecto al dominio d08

**Fecha:** 2026-07-24 · **Contexto:** definición del dominio d08 (Participación Ciudadana).
**Naturaleza:** hallazgo de curación (Regla 8) · **NO se modifica nada** — insumo para la
reconstrucción del IGP cuando se opere el Gold Master (fase posterior, con evidencia).

## Dónde vive el IGP
`H20b_IGP_GOBERNANZA_PARTICIPATIVA` → expuesto en `H73_OUTPUT_API` (contrato canónico):
- `IGP_2026_ACTUAL` = 0.4833 (48.33%) ← `H20b_IGP!B9`
- `IGP_REF_2025` = 0.2798 (27.98%) ← `H20b_IGP!B11`

Composición actual (3 componentes):
| Componente | Valor | Dominio real |
|---|---|---|
| IGP_1 · Asamblea CPCCS | 0.54 | d08 (participación) |
| IGP_2 · Presupuesto Participativo | **0.00** | d08 (participación) |
| IGP_3 · Fidelidad Narrativa MFN | 0.91 | **d09 (rendición de cuentas)** |

## Hallazgo 1 — el IGP mezcla dos dominios (d08 + d09)
El componente `IGP_3` (Fidelidad Narrativa MFN, hoja H34b) pertenece a **Rendición de Cuentas
(d09 · control social)**, no a Participación Ciudadana (d08). El IGP —indicador madre de d08—
incorpora una variable de otro dominio, cruzando la frontera doctrinal d08/d09 que el propio
dominio acaba de establecer (participación ≠ control social, en términos LOPC).
- **Estado:** no es error de cálculo; es una decisión de composición previa a la separación de
  dominios. Requiere revisión metodológica al reconstruir el IGP.
- **Nota histórica:** el IGP se concibió como base de d08 cuando RDC aún no se había abierto por
  su propia frontera. Al separarse d09, el componente MFN debería migrar/retirarse.

## Hallazgo 2 — IGP_2 (Presupuesto Participativo) = 0 pese a evidencia documental
El componente `IGP_2` está en 0.00, pero existe evidencia documental de PP para **tres años**:
`GAD Montecristi Informe Presupuesto Participativo 2024 / 2025 / 2026` (docx+pdf, procesables) —
y en el corpus (`PP-GAD-2024/2025/2026`). La propia nota del Excel (H20b!A13) lo reconoce:
*"refleja la ausencia de actividad formal de participación registrada en CPCCS y presupuesto
participativo"*.
- **Diagnóstico:** el motor no tiene cargado el dato del PP que sí existe en la evidencia. El
  IGP está **subestimado** por un input faltante, no por una falla real de participación.
- **Consecuencia:** cuando d08 procese los informes de PP, la evidencia contradirá el `IGP_2=0`.
  Esa brecha (evidencia sí / motor 0) es exactamente lo que QUIRA existe para demostrar.

## Hallazgo 3 — las señales SAT de participación no existen en el Excel (salvo una)
Las 7 señales que el canon define (SAT-VIII-001..007, una por instancia/mecanismo) son diseño
BRN; su MATERIALIZACIÓN como señal calculada es **Excel canónico** (aporte de Javo · 2026-07-24)
y hoy solo existe **una**: `H24c_SAT-VI_DESVÍO_PP` — y de naturaleza FISCAL (desvío del PP),
distinta de la señal DOCUMENTAL de verificabilidad que d08 requiere. Además está sin datos
(`Hay_Datos_PP = NO`, "FALLA 17"). Las señales de las demás instancias (Sistema, Asamblea,
Consejo, Audiencia, Cabildo, Silla) hay que **crearlas en el Excel** en la misma operación de
fase 2. El grafo las lleva como diseño con `materializacion_excel: pendiente`.

## Qué NO se hace aquí (Regla 1/4)
No se toca el Gold Master. La corrección —cuando se decida— se hará **sobre copia, con evidencia,
con aprobación de Javo**, como se curó d02 (bug ICPI÷100) y d03. Este OBS es el **insumo**.

## Precisión conceptual (asesor · 2026-07-24)
No se "reconstruye el IGP" — se **reconstruye el MODELO DE CÁLCULO del IGP**. El indicador sigue
siendo el mismo IGP; lo que cambia es la arquitectura que lo alimenta:
`Norma → Dominio ontológico → Evidencia documental → Variables → Modelo de cálculo → IGP`.
Esto mantiene la estabilidad conceptual: el IGP nunca deja de ser el IGP; mejora su modelo.

## Principio que este hallazgo consagra
El índice (IGP) y sus señales (SAT) se **derivan** del dominio (norma → evidencia → modelo →
índice), nunca al revés. El diseño de d08 nació del corpus normativo, no del IGP. El IGP es el
**indicador madre** del dominio —lo que d08 demuestra documentalmente— pero se **lee**, no se
recalcula, y su **modelo de cálculo se reconstruye desde el dominio** cuando este revela que está
mal compuesto. Es lo que ocurre aquí.

---
*OBS-015 · Dylus Lab © 2026 · el dominio bien definido audita su propio índice.*
