# Meta-Catálogo de Agentes — Organigrama Cognitivo de QUIRA IA

> **Estado:** vivo · 2026-07-22 (colega, Punto 7) · se amplía con cada DOM migrado
> **Qué es:** el mapa de quién hace qué en QUIRA IA. Distingue lo **agéntico** (juicio, LLM,
> cuesta API) de lo **determinístico** (aritmética fija, gratis). Regla rectora de la sesión:
> *cada DOM es mayoritariamente IA en extracción/interpretación; solo el cálculo final es
> determinístico.*

## Distinción fundamental

| Tipo | Qué es | Cuándo corre | Costo |
|---|---|---|---|
| **IA** | navega, extrae, interpreta, cruza, redacta — requiere juicio | Fase 4/5 | Haiku/Sonnet |
| **Determinístico** | aritmética/lectura fija sobre datos ya limpios | siempre | gratis |

## Catálogo

| Agente / Módulo | DOM | Entrada | Salida | Tipo | Estado | Reutilizable | Dependencias (lo usan) |
|---|---|---|---|---|---|---|---|
| **Portal Navigator** | d07 | Portal DPE (URL por CD) | página/archivo localizado | IA | ⬜ Fase 4 | ✅ genérico (cualquier portal) | d07 hoy; candidato d01/d02 web-GAD |
| **Evidence Collector** | d07 | página localizada | archivo descargado (PDF/CSV/HTML) | IA | ⬜ Fase 4 | ✅ genérico | d07 |
| **Evidence Interpreter** | d07 | archivo | ¿completo? ¿simulación? ¿enlace roto? | IA | ⬜ Fase 4 | ✅ genérico | d07 |
| **Compliance Evaluator** | d07 | evidencia juzgada | CTA/ETA/RP/CI (0-1) | **Determinístico** | ✅ `scoring.py` | parcial (reglas SITA son de d07) | d07 |
| **SITA Engine** | d07 | CTA/ETA/RP/CI | SITA = promedio/4 | **Determinístico** | ✅ `scoring.py` | ❌ específico LOTAIP | d07 |
| **Report Generator** | d07 | score + evidencia | narrativa (Regla Oro 2) | IA | ⬜ Fase 5 | ✅ genérico (cambia solo el prompt) | d07, candidato todos |
| **PDOT Agent** | d01 | web GAD | JSON PDOT (metas) | IA | ⬜ Fase 4 | ✅ genérico (Portal Navigator especializado) | d01 |
| **POA Agent** | d01 | web GAD | JSON POA (programación) | IA | ⬜ Fase 4 | ✅ genérico | d01 |
| **PAC Agent** | d01 | SERCOP / web GAD | JSON PAC | IA | ⬜ Fase 4 | ✅ genérico | d01 |
| **SERCOP Agent** | d01 | portal compras públicas | contratación real ejecutada | IA | ⬜ Fase 4 | ✅ genérico | d01, candidato d02 (compras) |
| **Budget Agent** | d01 | portal transparencia (=CD-06 d07) | cédula presupuestaria | IA | ⬜ Fase 4 · **reuso d07** | ✅ **YA compartido** | **d01 + d02 + d07 + d09** |
| **Alignment Agent** | d01 | PDOT+POA+PAC+SERCOP | hallazgos RO-I-001/002 | IA | ⬜ Fase 4 (`articulacion.py`) | ❌ específico (reglas RO de cada CNO) | d01 |
| **Motor IPE (lectura)** | d01 | Gold Master H16b | IPE, cobertura | **Determinístico** | ✅ `motor.py` (LEE, no calcula) | ❌ específico (celda propia) | d01 |
| **ICPI Engine** | Core | índices | ICPI (H12!B33) | **Determinístico** | ✅ Gold Master (INMUTABLE) | — (único, no se replica) | todos los DOM lo consumen |
| **Motor Capacidades (lectura)** | d02 | Gold Master (H19/H07/H20c/H11) | ISP·Ti·fondos·PND | **Determinístico** | ✅ `motor.py` envuelve `enrich_presupuesto.py` ya en producción | ❌ específico (4 celdas propias) | d02 |
| **Resultado Agent** | d02 | web GAD / transparencia | ¿existe medición de impacto? | IA | ⬜ Fase 4 (`fuentes.py`) | ✅ genérico (Portal Navigator) | d02, único hueco agéntico real del dominio |
| **eSIGEF (Fuente)** | d02 | Gold Master H07 | cédula ejecución | — | ✅ reuso confirmado | ✅ **YA compartido** | **d02 = d01 Presupuesto = d07 CD-06** (misma cédula) |
| **Motor Mandato (lectura)** | d03 | Gold Master H03/H16 | incorporación%, calidad_IFE%, centinela | **Determinístico** | ✅ `motor.py` envuelve `enrich_mandato.py` ya en producción | ❌ específico (2 métricas propias) | d03 |
| **Contraste Documental Agent** | d03 | Plan CNE original + SCHEMA_CNE | promesa verificada / autoridad actualizada | IA | ⬜ Fase 4 (`fuentes.py`) | ✅ genérico (Portal Navigator) | d03, único hueco agéntico real del dominio |
| *(d09)* | — | — | — | — | ⬜ pendiente de migrar | — | — |

## Lecturas del catálogo (lo que revela)

- **Solo 5 piezas son determinísticas** (Compliance Evaluator, SITA Engine, Motor IPE-lectura, Motor
  Mandato-lectura, ICPI Engine). Todo lo demás — la mayoría — es IA. Confirma la doctrina: QUIRA IA
  es un ecosistema de agentes, no un motor de scripts con un extractor aislado.
- **El ICPI Engine es el único intocable** (Regla 1). Todos los demás determinísticos LEEN o
  agregan; ninguno redefine el motor canónico.
- **Budget Agent se comparte** (d01 lo consume, d07 lo produce) — es la memoria operacional de
  Neo4j en acción: la cédula se extrae una vez (`MISMA_FUENTE_QUE`), no dos.
- **Patrón replicable**: cuando se migren d02/d03/d09, cada uno añade sus agentes de extracción
  (IA) + su lectura de motor (determinística) — misma forma, distinta sustancia.
- **Columnas Reutilizable/Dependencias (colega, 2026-07-23):** Navigator/Collector/Interpreter/
  Report Generator son **genéricos** — no leen la ley, leen el Catálogo del DOM que los invoca
  (`app/agents/d0X/catalogo.py`). Lo específico de cada DOM son sus reglas de scoring (SITA≠IPE)
  y su Alignment Agent. Esto es lo que hace viable el DOM_TEMPLATE (ver §DOM_TEMPLATE en
  `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md` o el módulo `app/agents/_template/`).

---
*Meta-Catálogo de Agentes · Dylus Lab © 2026 · "El organigrama cognitivo: quién razona, quién solo calcula."*
