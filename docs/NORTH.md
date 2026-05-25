# QUIRA OS — Norte y Hoja de Ruta Definitiva
**CANON OFICIAL — No modificar sin validación del equipo**
*Última actualización: 2026-05-25 — Sprint 1 Ejecutado*

---

## 1. Identidad Estratégica

**QUIRA** es una **infraestructura operativa de inteligencia institucional** para Gobiernos Autónomos Descentralizados del Ecuador.

Su función NO es "automatizar gobiernos". Es aumentar:
- **observabilidad** institucional
- **coherencia** entre planificación, contratación y ejecución
- **trazabilidad** documental y normativa
- **memoria longitudinal** territorial
- **validación** explicable y auditable

**Flujo doctrinal permanente:**
```
OBSERVAR → ENTENDER → VALIDAR → MEMORIZAR → PROYECCIÓN CONTEXTUAL LIMITADA
```

---

## 2. Principios No Negociables

1. **Doctrina antes que herramientas** — D1-D5, SAT, TGI son permanentes. Streamlit, Supabase, pgvector son reemplazables.
2. **Determinismo y explicabilidad** antes que IA opaca.
3. **Replicabilidad territorial** antes que sofisticación.
4. **Complejidad gradual y validada** — no inflar el techo conceptual.
5. **Transparencia y auditabilidad total** — cada alerta SAT tiene base legal y base doctrinal.

---

## 3. Lo Permanente vs Lo Reemplazable

| Permanente (Doctrina) | Reemplazable (Tecnología) |
|---|---|
| D1–D5 | Streamlit |
| TGI Territorial | Supabase / pgvector |
| SAT (Sistema de Alertas y Trazabilidad) | LangChain / RAG frameworks |
| ICPI | Embeddings concretos |
| RC-M (Fase 4) | UI frameworks |
| Longitudinal Engine | Librerías de visualización |
| Validación intersistémica | Cualquier LLM específico |
| Trust Score | Proveedor de cloud |

---

## 4. Arquitectura por Capas

| Capa | Nombre | Función | Fase |
|---|---|---|---|
| Q1 | Observación | Captura y estructuración | **Sprint 1** |
| Q2 | Comprensión | Recuperación semántica (RAG) | Fase 2 |
| Q3 | Validación | Coherencia, SAT, riesgos | Fase 2-3 |
| Q4 | Memoria | Longitudinalidad histórica | Fase 4 |
| Q5 | Proyección Contextual | Escenarios acotados y explicables | Fase 5 |
| Q6 | Infraestructura | Operación multi-GAD | Fase 6 |

**Sprint 1 opera exclusivamente en Q1 (Observación).**

---

## 5. TGI vs QUIRA — Relación Canónica

```
TGI = doctrina de evaluación institucional
QUIRA = infraestructura operativa que ejecuta y escala esa doctrina
```

| TGI (Qué mide) | QUIRA (Cómo opera) |
|---|---|
| D1 Legalidad | Q2 Comprensión + Q3 Validación |
| D2 Planificación | Q1 Observación + Q3 Validación |
| D3 Ejecución | Q1 Observación |
| D4 Equidad Territorial | Q3 Validación + Q4 Memoria |
| D5 Capacidad Institucional | Q6 Infraestructura |

---

## 6. SAT — Sistema de Alertas y Trazabilidad

**SAT no es metodología paralela a la ley. SAT es capa de validación doctrinal SOBRE la ley.**

Cada alerta tiene triple anclaje:
| Capa | Ejemplo |
|---|---|
| Legal | Art. 113 COPFP — obligación evaluación presupuestaria |
| Operativa | Ejecución observada = 59.85% |
| Doctrinal QUIRA | Riesgo SAT-D3 crítico por persistencia longitudinal |

**Catálogo SAT será hoja complementaria `SAT_Catalogo` en Gold Master.**
El Gold Master (motor matemático TGI/ICPI/D1-D5) NO se modifica.

---

## 7. Hoja de Ruta Operativa

### FASE 0 — Contención Estratégica ✅ COMPLETA
- Detener expansión conceptual innecesaria
- Congelar doctrinas experimentales
- QUIRA dejó de "mutar" cada semana

### FASE 1 — Consolidación del Núcleo (Jun–Ago 2026) 🔄 EN PROGRESO
**Sprint 1 — Consolidación Base (semanas 1-2):**
- [x] `municipality_registry.json` — registro canónico 17 municipios
- [x] `scripts/registry.py` — CRUD module
- [x] `app/connectors/dpe.py` — conector DPE API
- [x] `app/connectors/sercop.py` — conector SERCOP OCDS
- [x] `app/connectors/cpccs.py` — conector CPCCS RdC
- [x] `app/pipelines/snapshot_pipeline.py` — **orquestador principal**
- [x] `config.py` — configuración centralizada Sprint 1
- [x] `scripts/run_pipeline.py` — entry-point CLI
- [ ] Ejecutar snapshot real Montecristi — verificar pipeline end-to-end
- [ ] Guardar primeros snapshots históricos en `data/snapshots/130801/`

**Sprint 2 — Estabilización (semanas 3-4):**
- [x] `SAT_Catalogo` en Gold Master — hoja puente Q1→SAT_ENGINE (SAT-0 a SAT-VIII, triple ancla)
- [x] `app/connectors/gold_master.py` — conector H73_OUTPUT_API (51 métricas, reliability=0.99)
- [x] `app/services/sat_evaluator.py` — evaluador SAT con triple ancla legal+operativa+doctrinal
- [x] Pipeline ampliado a 11 pasos — ICPI=53.56%, SAT RIESGO=ALTO, 3 alertas activas
- [x] Supabase: snapshot guardado sin errores de validación (fix tgi.score Q1)
- [ ] Logging y manejo de errores centralizado
- [ ] Tests básicos de pipeline
- [ ] Dashboard ejecutivo: ICPI + SAT + D5 + longitudinalidad

### FASE 2 — Recuperación Semántica (Sep–Dic 2026)
- RAG sobre PDOT, POA, PAC, contratos, SERCOP, CPCCS
- Embeddings + pgvector
- Comprensión documental del territorio

### FASE 3 — Validación Multi-Territorial (2027)
- Manta (130901) + Jipijapa (130601) + Montecristi
- Demostrar replicabilidad doctrinal

### FASE 4 — Memoria Institucional
- RC-M, reincidencia, deterioro, recuperación longitudinal

### FASE 5 — Proyección Contextual Limitada
- Escenarios acotados, explicables, causales (NO simulación total)
- Ejemplo: "Si D3 < 60% por 3 trimestres → riesgo pérdida cooperación"

### FASE 6 — Infraestructura Territorial (Año 3+)
- Multi-GAD completo, observatorio regional

---

## 8. Stack Técnico Oficial

| Componente | Tecnología | Estado |
|---|---|---|
| UI | Streamlit | Activo |
| Core | Python 3.11+ | Activo |
| Base de datos | Supabase/Postgres + pgvector | Activo |
| Semántica | LangChain / LlamaIndex | Fase 2 |
| Visualización | Plotly + ECharts | Activo |
| Analítica | Pandas + motores doctrinales | Activo |

**Postergado estratégicamente:** CrewAI, AutoGen, Kubernetes, microservicios, deep learning opaco, multiagentes complejos.

---

## 9. Territorio Canónico

```
Municipio primario: Montecristi (código 130801)
Todo se valida primero allí.
```

**Expansión aprobada (Sprint 3 - Fase 3):**
1. Manta (130901) — mayor GAD costero Manabí
2. Jipijapa (130601) — perfil comparable para benchmarking

---

## 10. Arquitectura de Código Sprint 1

```
quira-os/
├── app/
│   ├── connectors/          ← Puentes institucionales (DPE, SERCOP, CPCCS)
│   │   ├── dpe.py           ✅
│   │   ├── sercop.py        ✅
│   │   └── cpccs.py         ✅
│   ├── pipelines/
│   │   └── snapshot_pipeline.py  ✅ CORAZÓN OPERACIONAL
│   ├── services/
│   ├── models/
│   ├── views/
│   └── utils/
├── data/
│   ├── municipality_registry.json  ✅
│   ├── doctrinal/           ← Gold Master (lectura)
│   ├── snapshots/           ← longitudinalidad por municipio/año
│   │   └── 130801/          ← Montecristi namespace canónico
│   └── raw/                 ← CSVs DPE sin procesar
├── scripts/
│   ├── registry.py          ✅
│   ├── run_pipeline.py      ✅ ENTRY POINT
│   ├── fetch_sercop.py      ✅
│   ├── fetch_rdc_cpccs.py   ✅
│   └── _generate_snapshot_dpe.py  ✅
├── utils/
│   └── snapshot_io.py       ✅
├── config.py                ✅
└── docs/
    └── NORTH.md             ✅ ESTE DOCUMENTO
```

---

## 11. Lo Que NO Debe Ocurrir

> "El riesgo más grande ahora no es técnico. Es volver a inflar el techo conceptual y dejar de ejecutar."

**Prohibido temporalmente:**
- CrewAI / AutoGen / LangGraph / multiagentes
- Kubernetes / microservicios / arquitectura distribuida pesada
- Institutional Digital Twin completo (prematuro)
- Simulación institucional fuerte (Fase 5)
- Debate filosófico grande (ya está resuelto)
- Nuevos frameworks experimentales

**El cuello de botella hoy es: estabilidad operacional, no IA.**

---

## 12. El Verdadero Diferencial

El valor de QUIRA no será "tener más IA".

Será demostrar:
- **coherencia longitudinal** entre planificación ↔ contratación ↔ ejecución
- **validación intersistémica** (DPE + SERCOP + CPCCS + redes)
- **trazabilidad** normativa explicable (base legal + base doctrinal)
- **replicabilidad territorial** real en municipios ecuatorianos

Convertir normativa pública dispersa en un sistema operativo observable y longitudinal.

**Eso es muchísimo más difícil que hacer un chatbot. Y ya están muy cerca.**
