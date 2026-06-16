# MAPA DEL HILO CONDUCTOR — la anatomía de QUIRA

**2026-06-15 · estructura canónica del proyecto · el hilo que teje las piezas**

> Las piezas dejaron de estar sueltas. Todo el proyecto fluye por **UN pipeline**, organizado por los
> **13 dominios** de la ontología y amarrado por **MNT_UUID**. Esto es la BASE estructural — se actualiza
> solo si cambia la arquitectura (vía ADR), no la implementación del día a día.

## El pipeline único (5 capas)

```
 [1 · RAÍZ]            [2 · MOTOR]           [3 · PUENTE]            [4 · SOPORTE]          [5 · CEREBRO]
 Obsidian / cédulas →  Gold Master Excel  →  snapshot_pipeline   →  Supabase + Neo4j   →  QUIRA UI
 eSIGEF·SERCOP·LOTAIP  (H73_OUTPUT_API)      → gm_snapshot.json      histórico + grafo     (Streamlit)
 EVIDENCIA pura        CÁLCULO canónico      CONTRATO único         MEMORIA longitudinal  LEE, no calcula
 (atestigua)           (B33 inmutable)       + validación SAT       + relaciones impacto  pinta widgets
       └──────────────────────── amarre: 13 DOMINIOS (ontología) · MNT_UUID (celda↔pixel) ────────────────┘
```

## Las 5 capas (con estado HONESTO)

### 1 · La Raíz — evidencia pura (atestigua, no calcula)
- Obsidian (tesis · corpus · PDOT) · cédulas eSIGEF/SERCOP/LOTAIP · corpus normativo en Supabase.
- **Estado: 2025 ingestado PARCIAL** (≠ "completo"): BOMBEROS 12/12 · EMAI-EP 11/12 · PATRONATO 9/12 ·
  **GAD 3/12 (solo Oct-Dic)**. 2026 Ene-Abr vivo. *(El hueco del GAD intra-anual es por qué la curva de pacing usa proxy de adscritas.)*

### 2 · El Motor — Gold Master Excel (cálculo soberano)
- `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` (slot vivo) — **contenido v6.0 corregido** (cirugía D.2A).
- Única sede de la fórmula **`H12!B33` (inmutable)** + el **Axioma de Invarianza**. Procesa el ICPI real (**27.46%**). NO dibuja pantallas.
- **Estado: CERRADO Y SELLADO 🔒** (inexpugnable · `..._v6.0_FREEZE_20260615` archivado · rollback `..._pre-D2A`).

### 3 · El Puente — `snapshot_pipeline.py` (el hilo conductor REAL)
- **NO es "solo exportar el Excel".** ORQUESTA: `fetch` (Gold Master + DPE + SERCOP + RDC) → `normalize` →
  `validate` (SAT triple ancla legal+operativa+doctrinal) → `build` `gm_snapshot.json` → `save` (Supabase + JSON) → `emit_provenance` (MNT_UUID).
- Flujo doctrinal: **OBSERVAR → ENTENDER → VALIDAR → MEMORIZAR.** El Gold Master es la fuente canónica/fallback del ensamble.
- Salida = el **CONTRATO ÚNICO DE DATOS**. Las claves son las REALES de `H73_OUTPUT_API` (ver `GM_H73_DUMP.md`, 65 claves:
  `ICPI_GLOBAL` · `ICPI_CLASIFICACION` · `TGI_SCORE` · `TGI_D1..D5` · `ISP_*` · `PSG_*` · `IFE_*` · `SAT_*`…). **NO claves inventadas.**
- **Estado: existe** (`app/pipelines/snapshot_pipeline.py` + `data/gm_snapshot.json`) · **siguiente: regenerar sobre el vivo corregido.**

### 4 · El Soporte — Supabase + Neo4j
- **Supabase:** histórico longitudinal (`monthly_kpis` · `budget_execution_lines` · `document_uploads`…) + persistencia del snapshot. Tablas ✅ listas.
- **Neo4j:** grafo causal (QTMP · relaciones de impacto entre dependencias). Estado: estructurado (QTMP yaml + scripts) · **operacionalización por verificar.**

### 5 · El Cerebro — QUIRA UI (lee, no calcula)
- Streamlit/Python. Lee el snapshot (contrato) y pinta widgets con fidelidad absoluta. **No calcula NADA.**
- **Estado: diseño ~90% · aún lee `demo_data` en varias pantallas** ← justo la deuda que teje Sprint D.1.

## 🔑 La Regla de Oro del tejido
> Cambia un dato en el **Motor** → se corre el **Puente** → se actualiza `gm_snapshot.json` →
> lo reflejan Supabase, Neo4j y la pantalla de QUIRA. **Una sola fuente de verdad. Cero dispersión.**

## 🛡️ La Regla de Disciplina (adoptada — recomendación del colega)
> **Ningún debate metodológico nuevo se abre salvo que una pantalla real o una cosecha real lo obligue.**
> NO re-filosofar el ICPI · NO rediseñar congruencias · NO tocar ontología. La ontología ya sobrevivió;
> ahora toca DEMOSTRAR que opera. **Cada pixel con su celda; cada celda con su tesis.**

## 🎯 Próximo objetivo — Sprint D.1: d06 en vivo (ingeniería de cableado, NO teoría)
Que el dashboard **d06 (Integridad Institucional)** deje de leer `demo_data` y lea el motor real vía el Puente.
1. **Puente fiel:** regenerar `gm_snapshot.json` sobre el vivo corregido (B33=27.46% + vectores 13 dominios desde H73).
2. **Mapeo widget↔clave:** auditoría estricta — cada widget de d06 → su clave REAL del snapshot (verificada, no inventada).
3. **Cableado quirúrgico:** sustituir `demo_data` por la lectura del snapshot en d06 · push limpio a Streamlit (SIN tocar la estética ya construida).
4. **Prueba de la verdad (auditoría visual):** QUIRA en pantalla vs Excel — ¿coincide exacto (27.46% · semáforo · vectores GAD+adscritas)?
   **Sí → QUIRA deja de ser teoría y es Sistema Operativo vivo.**

## La cadena — por primera vez CERRADA
```
TESIS → GOLD MASTER → H73_OUTPUT_API → ONTOLOGÍA → DOMINIOS → CONGRUENCIAS → DASHBOARDS
```
Eso es arquitectura. Y por primera vez está cerrada de punta a punta.

---
*Mapa del Hilo Conductor · Dylus Lab © 2026 · estructura canónica del proyecto · actualizar SOLO vía ADR si cambia la arquitectura.*
