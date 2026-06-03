# GATE-007 — Programa de Validación Externa: Municipio #2

**Estado**: PENDIENTE — decisión de Javo (fundador)  
**Fecha de definición**: 2026-06-03  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Origen**: Colega asesor · síntesis estratégica post-Gate 6.6

> *"La diferencia entre un caso exitoso y un modelo exportable
> es exactamente un segundo municipio."*
> — Colega asesor, 2026-06-03

---

## Por qué Gate 7 cambia la naturaleza del proyecto

Hasta Gate 6.6, la pregunta era: **¿Funciona QUIRA?**

La respuesta quedó demostrada:

```
Documento → Sigla → MNT_UUID → Dominio → Silo → Variable ICPI → Indicador
```

51/51 siglas trazadas. 0 huérfanos. ICPI 2025 explicable automáticamente.

Ahora la pregunta es: **¿Qué tan generalizable es QUIRA?**

Eso solo se responde con un segundo municipio.

---

## Objetivo único

> Replicar exactamente el pipeline en un segundo GAD.
> Nada más.

**NO** es construir nuevas features.  
**NO** es mejorar el sistema.  
**ES** intentar romperlo.

Si sobrevive: QUIRA deja de ser una solución para Montecristi  
y pasa a ser **una solución para los 221 GAD del Ecuador**.

---

## Candidatos (selección: Javo)

| GAD | Provincia | Razón |
|---|---|---|
| Portoviejo | Manabí | Capital provincial · mayor disponibilidad documental |
| Manta | Manabí | Ciudad puerto · fuerte presencia institucional |
| Jipijapa | Manabí | Misma provincia que MCR → comparación directa |
| Santa Ana | Manabí | Mismo contexto territorial |
| Chone | Manabí | Similar escala a MCR |

**Criterio de selección:** el GAD con mejor disponibilidad de:
1. SIGAD reportes (S6)
2. LOTAIP mensual (S5)
3. RC documentos (S8)
4. POA/PAC (S3/S3b)

---

## Las 3 métricas de validación

### Métrica 1 — Cobertura automática del pipeline
```
¿Cuántas siglas se detectan automáticamente?
¿Cuántos MNT_UUID se asignan sin intervención?
¿Cuántos dominios se clasifican solos?

Éxito: > 80% de cobertura sin trabajo manual
```

### Métrica 2 — Replicabilidad del Gap A↔D (ADR-022)
```
Gap A↔D Montecristi = 17.71% IOC (Excel canónico)

¿El segundo GAD muestra un patrón similar?
¿O es un caso excepcional de Montecristi?

Si persiste: ADR-022 SUPPORTED → CONFIRMED
Si no persiste: ADR-022 permanece SUPPORTED → aprendizaje
```

### Métrica 3 — ICPI explicable en segundo GAD
```
¿Se puede responder "¿Por qué ICPI = X%?"
usando el mismo pipeline?

python -X utf8 scripts/analysis/explainability_report.py --icpi

Si funciona: ADR-023 deja de ser local.
```

---

## El pipeline que debe replicarse

```
1. ingest_holding.py     → corpus C+D del nuevo GAD
2. ingest_lotaip.py      → cédulas LOTAIP mensuales
3. tag_mnt_uuid.py       → SIGLA → MNT_UUID (adaptar SIGLA_MAP)
4. tag_domains.py        → Dom01-D12 (mismo mapeo)
5. explainability_report → ICPI explicable
6. metrics_mcr.py        → leer Gold Master del nuevo GAD
```

Nota: cada nuevo GAD necesitará su propio Gold Master o una extensión
del existente para sus 25 metas PDOT propias.

---

## Criterio de éxito de Gate 7

```
Si Gate 7 pasa:
  ADR-022 → CONFIRMED
  ADR-023 → principio general, no solo Montecristi
  QUIRA   → solución para 221 GAD del Ecuador

Si Gate 7 falla en algo:
  Hallazgo de qué es específico de Montecristi
  Aprendizaje para ADR-024 (por definir)
  Sistema más robusto para siguiente municipio
```

No hay fracaso posible. O el modelo escala, o aprendemos por qué no.

---

*GATE-007 · QUIRA Gov · Dylus Lab © 2026*  
*Decisión pendiente: Javo (fundador) elige el municipio*  
*Cronograma: a definir en próxima sesión*
