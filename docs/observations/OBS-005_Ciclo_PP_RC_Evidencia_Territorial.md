---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-005 — Ciclo PP→RC→PP: Tres Capas de Evidencia Convergentes

**Estado**: CONFIRMED  
**Fecha**: 2026-06-02  
**Actualizado**: 2026-06-03 (elevado de observacion a hallazgo fundante)  
**Origen**: Gate 6.5A · Semantic Mining Q01+Q02+Q07 + corpus RC+PP Montecristi  
**Circuitos**: C01 (Dom08↔Dom09), C02 (Dom08→Dom02→Dom04)  
**Candidato ADR**: Sí — revisar con colega asesor para apertura de ADR-022

> **Nota del colega asesor (2026-06-03):**
> *"OBS-005 cambia de categoría epistemológica. Ya no apoya el ciclo Dom08→Dom09→Dom08
> únicamente en norma, grafo o métricas. Ahora tiene evidencia documental territorial real.
> Ese es un cambio de madurez de hipótesis."*

---

## El Hallazgo Central

La hipótesis de ADR-019 (Dom08+Dom09 = par constitucional con ciclo democrático
bidireccional) tiene ahora respaldo en tres capas independientes y convergentes.

**Esta convergencia de tres capas transforma ADR-019 de hipótesis arquitectónica
a propiedad observable del sistema de gobernanza de Montecristi.**

---

## Capa 1 — Evidencia Normativa (Capa A)

| ACK | Texto canónico | Función en el ciclo |
|---|---|---|
| COOTAD_266 | "...prioridades de ejecución del siguiente año" | Cierre normativo RC→PP |
| LOPC_65 | Presupuesto Participativo obligatorio | Apertura normativa PP |
| LOPC_89/90/91 | Proceso de Rendición de Cuentas | Obligación RC |
| CE_95 | Participación ciudadana protagónica | Norma fundante |

OBS-003 (CONFIRMED, commit d66c2d3) estableció que COOTAD_266 positiviza
el ciclo en 65 palabras. La norma existe desde 2010.

---

## Capa 2 — Evidencia Computacional (Cerebro 2)

| Métrica | Valor | Fuente |
|---|---|---|
| Dom08 betweenness | 4.6× Dom07 | centrality_results.json |
| Dom09 Comunidad 3 | separada de C2 pero unida por GENERA+RETROALIMENTA | Louvain Gate 4 |
| CE_1 Cascade Score | 39 > CE_226 (34) | M6 ADR-020 |
| Dom08 ↔ Dom09 proxy | 427 vs Dom07: 207 (2.06×) | Gate 4 re-run |

ADR-019 STRONGLY_SUPPORTED (commit 3c98583) — espera Dom09 completo para CONFIRMED.

---

## Capa 3 — Evidencia Documental Territorial (Capa D) — NUEVA

**Lo que el corpus de Montecristi contiene** (Gate 6.5, commit 0ece5dd):

### PP (Dom08 observable)

Los informes PP-GAD-2024/2025/2026 contienen evidencia directa del ejercicio
democrático predicho por la norma:

- **Demandas ciudadanas con nombre + cédula + barrio + proyecto específico**
  (evidencia de participación real, verificable individualmente)
- **Montos asignados por programa**: infraestructura vial, sociocultural,
  económico-productivo, asentamientos humanos
- **URL del formulario digital** (LOPC_101 — Evidencia Digital Verificable)
- **Proceso de priorización**: asamblea territorial convocada formalmente

### RC (Dom09 observable)

Los informes RC-GAD+ASEO+BOMBEROS+PATRONATO-2023/2024 contienen:

- **Número de informe CPCCS** (N° 17649 GAD-2023, N° 13057 ASEO-2023)
- **Metas planificadas vs ejecutadas** con porcentaje de cumplimiento
- **Ejecución presupuestaria**: codificado / ejecutado / planificado en $
- **Preguntas de la asamblea ciudadana al GAD** (la retroalimentación funciona)
- **URLs de transparencia activa** (LOTAIP Art. 12 cumplido)

### Retroalimentación RC→PP (Dom09→Dom08 observable)

Los chunks de Q07 (sim=0.602) detectan menciones al "siguiente ejercicio" y
"prioridades del próximo año" en los RC — exactamente el lenguaje de COOTAD_266.

El ciclo que QUIRA modeló como `Dom09 -[RETROALIMENTA]-> Dom08` existe
como práctica institucional documentada en Montecristi.

---

## Convergencia — El Argumento Completo

```
La norma DICE (Capa A):
  COOTAD_266: "el ejecutivo convocará a la asamblea para informar sobre
  ejecución presupuestaria y prioridades del siguiente año"

El grafo REVELA (Capa 2):
  Dom08 betweenness 4.6× Dom07
  Dom08 ↔ Dom09 bidireccional (GENERA + RETROALIMENTA)
  CE_1 como nodo apex de soberanía popular

El territorio MUESTRA (Capa 3):
  PP-GAD-2024: 246 chunks de demandas ciudadanas reales
  RC-GAD-2023/2024: 25 chunks con datos de metas y presupuesto
  RC de las 4 entidades: cobertura 100% del Holding
  Retroalimentación: mencionada en los propios RC
```

**Tres fuentes independientes, una estructura observable.**

---

## Gap A≠D Detectado (señal Q08)

Los PP contienen demandas específicas por barrio y proyecto.
Los RC reportan ejecución presupuestaria en % y $.
**Gap actual**: QUIRA no puede todavía verificar si la demanda "Alcantarillado
en Ciudadela X" del PP-2024 aparece como ejecutada en el RC-2024.

Esto requiere POA + PAC (Gate 6.5 Fases 2-3) para cerrar la trazabilidad
Demanda PP → Presupuesto POA → Contratación PAC → Ejecución RC.

**Este gap A≠D es el objeto de Gate 7: Trazabilidad Territorial Completa.**

---

## Implicación para ADR-019

OBS-005 aporta la evidencia territorial que faltaba como tercer pilar.

```
ADR-019 STRONGLY_SUPPORTED tenía:
  ✅ C1: Dom08 betweenness > 1.3× Dom07 (4.6×)
  ✅ C2: Dom09 betweenness posición 2°
  ⏳ C3: Dom09 Comunidad 3 estable con Dom09 completo
  ✅ C4b: CE_1 Cascade Score > CE_226

OBS-005 añade ahora:
  ✅ C_D: Ciclo PP→RC→PP documentado con corpus de evidencia Montecristi
```

El criterio C3 sigue pendiente (Dom09 aún incompleto normativamente).
Pero C_D refuerza el argumento desde una dirección independiente.

---

## Candidatura a ADR-022

La convergencia de tres capas en torno al mismo objeto (ciclo PP→RC→PP) es
suficientemente robusta para considerar un ADR que formalice:

1. El ciclo como **propiedad emergente verificada** del sistema de gobernanza
2. El método de verificación multicapa (A + computacional + documental)
3. Los criterios para declarar una hipótesis ADR como "verificada territorialmente"

**Acción**: revisar con colega asesor si abrir ADR-022 tras Gate 6.5 Fase 2.

---

*OBS-005 v2.0 · QUIRA Gov · Dylus Lab · 2026-06-03*  
*"El ciclo que la norma mandó en 2010, el grafo reveló en 2026, y el territorio confirma ahora."*
