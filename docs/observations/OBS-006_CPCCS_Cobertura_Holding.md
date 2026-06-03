# OBS-006 — Cobertura CPCCS y Ejecucion Presupuestaria del Holding

**Estado**: CONFIRMED
**Fecha**: 2026-06-03
**Origen**: Gate 6.5A · Semantic Mining Q03 + Q05
**Dominio**: Dom09 (Rendicion de Cuentas)
**Circuitos**: C01 (transparencia), C02 (presupuesto)

---

## Hallazgo 1 — Entidades del Holding con Informe RC verificado

Todas las entidades del Holding Municipal de Montecristi han rendido cuentas
ante el CPCCS para los periodos 2023 y 2024:

| Entidad | RC 2023 | RC 2024 | Num. Informe |
|---|---|---|---|
| GAD Montecristi | Si (DOCX) | Si (DOCX) | N 17649 (2023) |
| EP Aseo | Si (PDF) | Si (PDF) | N 13057 (2023) |
| Bomberos | Si (PDF) | Si (PDF) | Verificado en corpus |
| Patronato | Si (DOCX) | Si (DOCX) | Verificado en corpus |

**Significado para Dom09**: el circuito RC tiene evidencia de cierre en todos
los nodos del Holding. No hay entidad que haya evadido la obligacion de COOTAD_266.

## Hallazgo 2 — Datos de Ejecucion Presupuestaria Disponibles

Los RC contienen cifras de ejecucion presupuestaria con estructura:
- Codificado (presupuesto modificado)
- Ejecutado (gasto real)
- Planificado (meta original)

Ejemplo verificado (RC-ASEO-2023):
```
CODIFICADO: $1,813,011.57
EJECUTADO:  $285,86x.xx  (parcial visible en chunk)
```

**Gap A!=C detectado**: el Gold Master ya tiene las cifras de ejecucion.
Los RC las confirman narrativamente pero con distintos formatos.
Gate 6.5 Fase 3 (POA + cedulas) cerrara este gap con datos completos.

## Significado para ADR-019

La evidencia de CPCCS compliance en el corpus confirma que Dom09 (Rendicion)
opera como DESTINO real en el circuito constitucional C01.
No es solo un dominio teorico — tiene evidencia documental para Montecristi.

Esto fortalece el criterio C3 de ADR-019 que estaba pendiente de Dom09 completo.

---

*OBS-006 · QUIRA Gov · Dylus Lab · 2026-06-03*
*El Holding Municipal de Montecristi tiene cobertura RC 100pct para 2023-2024.*
