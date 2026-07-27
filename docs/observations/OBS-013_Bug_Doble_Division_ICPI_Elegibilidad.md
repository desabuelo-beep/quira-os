---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-013 — Bug de doble división ICPI/100 en H69/H08/H19b/H85

**Estado**: RESUELTO — corregido el mismo día · 2026-07-23
**Origen**: hallado al identificar la hoja del Gold Master para migrar d02 al patrón de plataforma (checklist `app/agents/_template/README.md`, paso 1: "verificar primero si el Gold Master ya calcula la métrica").

## Hallazgo

`H12_MOTOR_ICPI_CANÓNICO!B33` (el ICPI canónico) es una **fracción decimal**
(`0.27458226534062735` = 27.46%) — el formato que usa todo el Gold Master. 13 celdas en 4 hojas
lo dividían **otra vez** por 100, asumiendo por error que B33 era un entero-porcentaje:

| Hoja | Celdas | Efecto |
|---|---|---|
| `H69_ELEGIBILIDAD_FONDOS` | B6, C6, C19, D12-D16, B21 (9 celdas) | mostraba ICPI=0.27% en vez de 27.46% en la tabla de elegibilidad a fondos internacionales |
| `H08_S6_AUTOREPORTE_SIGAD` | B9 | mismo bug |
| `H19b_IE_EP_EA` | E7, F7 | mismo bug |
| `H85_ALERTS_LOG` | D20, F20 | el propio *chequeo de sincronización* comparaba dos valores con el mismo bug → reportaba falsamente "✅ SINCRONIZADO" |

**Impacto real en este caso concreto: ninguno en el resultado categórico** — ni con 0.27% ni con
27.46% se supera el umbral mínimo (60%) de ningún fondo listado, así que "0 de 5 elegibles" era
correcto por casualidad. **Impacto potencial:** si el ICPI real algún día se acerca al umbral
(p. ej. sube a 61%), este bug seguiría mostrando 0.61% y **ocultaría elegibilidad real** — que es
precisamente la pregunta que d02 existe para responder ("¿el municipio puede recibir el dinero
del mundo?", PCD-D02).

## Corrección

13 fórmulas corregidas (quitado el `/100` duplicado) + 2 textos descriptivos actualizados.
Verificado con recálculo COM tras cada tanda de cambios:
- Guardián `H12!B33` idéntico al backup en cada paso.
- `H73_OUTPUT_API` (contrato de salida real) con 0 diffs en todos los pasos — el bug vivía fuera
  del contrato que consume la UI/API.
- `H85!D20` pasó de comparar-mal-contra-sí-mismo a comparar correctamente: sigue diciendo
  "✅ SINCRONIZADO", ahora porque de verdad lo está.

## Lección

Apareció al hacer el primer paso del checklist del DOM_TEMPLATE para d02 ("verificar si el Gold
Master ya calcula la métrica antes de escribir código") — confirma que ese paso no es formalidad:
sin él, `app/agents/d02/motor.py` habría heredado un bug de escala real sin saberlo.

---
*OBS-013 · QUIRA Gov · Dylus Lab © 2026*
