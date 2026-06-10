# OPERACIÓN MINERA DEL PDOT — LOTE 01: GÉNERO Y PROTECCIÓN
**Sprint B.2 · QUIRA OS · 2026-06-09 · v1 (núcleo extraído)**
*Fuente: corpus narrativo Supabase (59 chunks tema género/protección filtrados a 43 con datos)*
*Método: `scripts/sprint_b/b1a_auditoria_pdot.py` + excavación dirigida*

---

## Indicadores extraídos (formato KB canónico)

| # | Indicador | Unidad | Valor | Año | Territorio | Fuente original | Pág. PDOT |
|---|---|---|---|---|---|---|---|
| 1 | Femicidios — serie anual | casos | 0·1·0·0·1·0·2·0·0·1 (2014→2023) · **total 5** | 2014-2023 | cantonal | INEC — Comisión Estadística de Seguridad Ciudadana y Justicia | 243 (T.122) |
| 2 | Posición provincial femicidios acumulados | lugar | 4º-5º (empate Chone) — tras Manta 13 · Portoviejo 8 · El Carmen 6 | 2014-2023 | provincial comparado | ídem | 243 (T.122) |
| 3 | Homicidios intencionales — serie anual | casos | 1·7·6·6·5·7·9·6·**25**·**47** (2014→2023) · total 119 | 2014-2023 | cantonal | ídem | 242 (T.121) |
| 4 | Variación homicidios 2022 / 2023 | % | **+317 % (2022) · +88 % (2023)** | 2022-2023 | cantonal | ídem (cálculo del propio PDOT) | 242 |
| 5 | Casos Junta Cantonal Protección — Mujer | casos | 120 → **198 (+65 %)** | 2022→2023 | cantonal | Junta Cantonal de Protección de Derechos | ~240 |
| 6 | Casos Junta Cantonal — Niñez y adolescencia | casos | 160 → 190 | 2022→2023 | cantonal | ídem | ~240 |
| 7 | Casos Junta Cantonal — Adulto Mayor / Bono | casos | 9 → 17 · Bono Mil 8 → 52 | 2022→2023 | cantonal | ídem | ~240 |
| 8 | Morbilidad — proporción femenina | % | 66.25 | 2023 | cantonal | MSP-HOSVITAL vía PDOT | 214 |
| 9 | Jefatura de hogar femenina | % | 36.1 | 2022 | cantonal | INEC Censo 2022 | 189 |
| 10 | Tasa de femicidios (indicador con meta) | tasa/100k mujeres | 1.14 → meta 0.8 | 2023 → 2027 | cantonal | PDOT Sistema Sociocultural (META-MNT-SEG-003) | 382 |
| 11 | Educación superior terciaria (meta PND ref.) | % | 51.75 (2022) → meta 61.20 (2025) | 2022 | referencia nacional/cantonal | PDOT vía PND | (chunk #395) |

## Hallazgo mayor del lote

**La violencia letal del cantón cambió de régimen en 2022-2023:** homicidios
estables ~6/año durante 8 años → 25 en 2022 → 47 en 2023 (+683 % vs línea
base). El femicidio tipificado se mantiene bajo (0-2/año), pero el contexto
de violencia general se multiplicó por ocho. Para el eje de género esto
significa: **el riesgo territorial para las mujeres no se mide solo en
femicidios tipificados — la curva de contexto está en la peor posición de
la década.** La FICHA-03 v1 no veía esta curva; la re-validación (B.3) debe
incorporarla.

## Gaps CONFIRMADOS como reales por el propio PDOT (no extraíbles)

| Gap | Evidencia textual |
|---|---|
| G-11 embarazo adolescente cantonal | El PDOT declara: *"no se registran cifras para este nivel territorial"* (los datos de salud materna son provinciales) — chunk #80, p. ~211 |
| G-09 desagregación parroquial | 0 cruces género×parroquia en 59 chunks — consistente con B.1A |
| G-12 tasa VIF cantonal | Sin tasa en el corpus; la demanda de protección (Junta Cantonal, #5) es el mejor proxy disponible |

## Segunda pasada pendiente (v2 del lote)

- Tablas 100-101 (cobertura Desarrollo Infantil Integral — eje cuidados)
- Chunks #91-92 (atenciones CDBV por tipo — verificar desagregación por sexo)
- Chunk #144/#278 (Sistema de Protección de Derechos — ordenanza 2014, institucionalidad)
- Chunk #29 (Consejo Cantonal de Protección de Derechos — estructura)
- Tabla 95-96 completas (nacidos vivos 2013-2022 — fecundidad)

## Destino de los datos

1. **Inmediato:** FICHA-03 re-validación (B.3) — series 1, 3, 5 y hallazgo mayor.
2. **GeoTwin:** ninguno de estos indicadores es territorializable aún (todos
   cantonales) — consistente con G-09.
3. **Candidatos a indicador formal** (mesa revisión motor): demanda de
   protección Junta Cantonal (serie) · contexto de violencia letal (serie).

---

*Lote 1/5 · Operación Minera B.2 · QUIRA OS · Dylus Lab © 2026*
*Raw de excavación: `scripts/sprint_b/_lote1_genero_raw.txt` (59 chunks, no commiteado)*
