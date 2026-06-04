# ADR-007 — Gold Master es la única fuente canónica de cálculo

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

El proyecto acumuló 15+ versiones del archivo de cálculo (v4.1 a v5.5). Existía confusión sobre cuál versión era la activa. En al menos una ocasión, datos del PMV divergieron del Gold Master porque se actualizó uno sin el otro.

## Decisión

**`ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` es la única fuente canónica de cálculo.**

Reglas:
1. **Nunca actualizar el PMV sin pasar primero por el Gold Master**
2. Cualquier dato que aparezca en Supabase, QTMP, o PMV proviene del Gold Master — nunca al revés
3. La versión canónica es `v5.5_TGI` sin fecha (fecha fija = versión congelada)
4. Snapshots con fecha (`_FREEZE_YYYYMMDD`) son solo lectura — registros históricos
5. El historial de versiones existe en `ProyecT\historial_gold_master\` — nunca reemplaza la canónica

## Jerarquía de autoridad

```
SIGEF (cédulas oficiales)
        ↓
Gold Master v5.5_TGI     ← único punto de entrada para cálculo
        ↓ deriva simultáneamente a:
  Supabase (métricas H73 + provenance)
  QTMP (circuitos yaml)
  PMV Streamlit (visualización)
  Vault Obsidian (navegación)
```

## Consecuencias

- Si hay discrepancia entre PMV y Gold Master: corregir el PMV, no el Gold Master
- Si hay discrepancia entre Gold Master y SIGEF: corregir el Gold Master, documentar en provenance
- El Gold Master tiene nombre interno sin sufijo fecha — es la versión viva, no un snapshot
- Provenance engine (CHK-08) garantiza trazabilidad hacia atrás desde cada métrica

## Versión activa

```
Archivo: SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx
Ruta: ProyecT\
Freeze: SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260526.xlsx (solo lectura)
H73 confirmadas: 58/63 = 92.1%
```
