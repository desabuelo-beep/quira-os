# BRIDGE: Corpus Holding → Motor ICPI (Excel Canon)
**Documento de arquitectura fundamental — Dylus Lab © 2026**
**Gate 6.6 — La conexión que une todo**

> El Excel Canónico ES el secreto de la empresa.
> Su metodología (Pi, Ri, Vi, Ti, Ci) es propietaria.
> Nadie la ve — solo ven los resultados.
> QUIRA automatiza la alimentación del Excel con datos verificados.
> El Excel sigue calculando. QUIRA entrega los datos y muestra los resultados.

---

## La fórmula maestra (permanece en el Excel)

```
ICPI = [Σ(Pi × Ri × Vi × Ei × Ti × Ci) / Σ(Pi × Ri)] × 100

Donde por cada una de las 25 metas PDOT:
  Pi = Peso financiero normalizado (del POA)
  Ri = Relevancia normativa de competencia (COOTAD exclusiva/compartida)
  Vi = Producto lógico de 4 verificadores (ver abajo)
  Ei = Ejecutividad (1.0 autónomo / 0.9 compartido / 0.75 difuso)
  Ti = Índice de inversión (Devengado / Codificado, de eSIGEF)
  Ci = Modificador de circuito
```

### La lógica Vi — el corazón de la verificación

```
Vi = 0.0  si V_eSIGEF=0 O V_SERCOP=0  (sin ejecución financiera o contratación)
Vi = 0.5  si V_eSIGEF=1 Y V_SERCOP=1 Y V_LOTAIP=0 Y V_CPCCS=0
Vi = 1.0  si V_eSIGEF=1 Y V_SERCOP=1 Y (V_LOTAIP=1 O V_CPCCS=1)
```

**Esta lógica ya está en el Excel. QUIRA NO la recalcula.**

---

## Los 9 Silos: qué necesitan y qué tenemos

| Silo | Hoja Excel | Necesita | ¿Tenemos en corpus? | Estado |
|------|-----------|---------|---------------------|--------|
| S1 CNE | H03 | 66 promesas electorales | PLAN-BICENTENARIO-MCR, RC | ✅ |
| S2 PDOT | H04 | 25 metas PDOT 2023-2027 | PAI-GAD-2023/2025/2026 | ✅ |
| S3 POA | H05 | POA 2026 con montos por dirección | POA-GAD-2026-v2 | ✅ |
| S3b PAC | H05b | PAC 2026 con procesos | PAC-GAD-2026 | ✅ |
| S4 SERCOP | H06 | Procesos adjudicados SERCOP | PAC docs + SERCOP script | ⚠️ parcial |
| **S5 eSIGEF** | **H07** | **Cédulas devengado/codificado** | **LOTAIP mensual 48 archivos** | **✅ LISTO** |
| S6 SIGAD | H08 | ICM por meta 25 metas | SIGAD-GAD-2023/2024-DOC | ✅ (2023-2024) |
| **S7 LOTAIP** | **H09** | **Score LOTAIP por meta (URL pública)** | **LOTAIP mensual 48 archivos** | **✅ LISTO** |
| **S8 CPCCS** | **H10** | **V_CPCCS: meta mencionada en RC** | **RC-GAD-2023/2024** | **✅ LISTO** |
| S8b PP | H10b | PP 2026 fichas y montos | PP-2024/2025/2026 | ✅ |

**3 silos listos para actualización desde el corpus: S5, S7, S8.**

---

## Flujo completo del sistema

```
MUNDO REAL
  Cédulas LOTAIP, RC, POA, PAC, SIGAD, PP
       ↓
GATE 6.5 (completado)
  Corpus Holding → normativa_corpus + holding_structured_data
  13,509 chunks texto + 65 tablas estructuradas
       ↓
GATE 6.6 (siguiente)
  scripts/analysis/update_silos.py
  Lee corpus → formatea → actualiza zonas crudas del Excel
       ↓
EXCEL CANÓNICO (motor propietario permanente)
  H07 → Ti = Devengado/Codificado
  H09 → V_LOTAIP score por meta
  H10 → V_CPCCS por meta
  H12 → ICPI recalcula automáticamente
  H73 → OUTPUT_API exporta resultados
       ↓
app/connectors/gold_master.py (ya existe, lee H73)
       ↓
UI QUIRA
  Dom01-D12 (vista general) → click → Dashboard Excel
       ↓
QUIRA IA
  Causalidad + conversación sobre los resultados
       ↓
GeoTwin
  Aterriza resultados en el territorio
```

---

## Estado actual de cada Silo (lo que encontramos leyendo el Excel)

| Silo | Variable clave | Valor actual | Calidad |
|------|---------------|-------------|---------|
| S5 eSIGEF 2026 | Ti_Global_2026 | 6.43% (solo Q1) | ✅ REAL (cédula abr-2026) |
| S5 histórico | Ti_2023, Ti_2024 | 68.04%, 79.61% | ✅ REAL (H36b inmutable) |
| S6 SIGAD | ICM por meta | 1.0 (25/25) | ⚠️ SIMULADO (extrapolado 2023/2024) |
| S7 LOTAIP | V_LOTAIP 2025 | ~82.29% ITAM | ✅ REAL (DPE verificado) |
| S7 LOTAIP 2026 | V_LOTAIP 2026 | ~84% proyectado | ⚠️ proyección |
| S8 CPCCS | V_CPCCS | 0.5 (parcial) | ⚠️ SIMULADO (patrón RDC 2024) |

**El corpus tiene los documentos para reemplazar los valores SIMULADOS con verificados.**

---

## Qué hace Gate 6.6 concretamente

### Tarea 1 — update_silos.py

Lee de `holding_structured_data` (LOTAIP mensual) y actualiza H07:
- Lee cédulas LOTAIP del GAD 2025/2026
- Calcula Ti = Devengado_Total / Codificado_Total por grupo (G7+G8)
- Escribe en H07 zona cruda (filas 46+)
- Excel recalcula ICPI automáticamente

### Tarea 2 — Verificar V_CPCCS desde RC corpus

Lee de `normativa_corpus` las RC 2023 y 2024:
- Busca menciones de cada una de las 25 metas PDOT
- Si meta SC-I-N-01 (agua potable) aparece citada con evidencia → V_CPCCS = 1
- Si aparece sin evidencia → V_CPCCS = 0.5
- Actualiza H10 con valores verificados en lugar de simulados

### Tarea 3 — Tagging Dom01-D12 en corpus

Para cada chunk en normativa_corpus donde canton_id='MCR':
- Identifica a qué meta PDOT corresponde (SC-I-N-01, AH-I-N-01, etc.)
- Asigna el dominio canónico (Dom01-D12)
- Asigna el circuito (C01, C02, C03)
- Actualiza campo `dominios_quira`

---

## Por qué el Excel es el secreto de la empresa

Los inversores y auditores ven:
```
Montecristi 2025:
  ICPI = 69.93%  (Transición Crítica)
  TGI  = 66.79%
  D3 Ejecución = 59.85%  ← donde está el trabajo
  D4 Equidad   = 44.79%  ← gap crítico
```

Nadie ve Pi/Ri weights, la lógica Vi, los 25 IDs de meta, la escala
AVEP, los SATs, los MMP, los IEDs por dirección.

**Eso es propiedad intelectual de Dylus Lab.**
**QUIRA es el sistema que la hace operable a escala.**

---

## Próximos pasos Gate 6.6

```
1. update_silos.py        → alimentar H07 con cédulas reales
2. verify_cpccs.py        → verificar V_CPCCS desde corpus RC
3. tag_domains.py         → tagging Dom01-D12 en Holding corpus
4. metrics_mcr.py         → ya lee de H73 (completado)
5. UI bridge              → Dom01-D12 → click → dashboard Excel
```

---

*BRIDGE_EXCEL_CORPUS.md · QUIRA Gov · Dylus Lab © 2026*
*Commit: Gate 6.6 — puente Corpus → Motor ICPI*
