# CIRUGÍA DEL GOLD MASTER — Sprint D.2A

**2026-06-15 · sobre COPIA · Excel nativo (preserva malla) + verificación determinista · `B33` JAMÁS tocada**

> Sincerar el motor sin romper la fórmula canónica. Las 3 correcciones son **INPUTS/semáforo**
> (sancionado por `METODOLOGIA_GOLD_MASTER.md`), nunca la fórmula `H12!B33`.

## Resultado
**ICPI 2026 (corte abril): 17.45% → 27.46%**
- `17.45 → 17.76` (+0.32 pp): homologación adscritas (Ti=0 → cédula SERCOP)
- `17.76 → 27.46` (+9.70 pp): FactorTemporal lineal → curva de pacing real 2025

El 27.46% es la proyección HONESTA: el GAD va a ~30% anual proyectado, **por debajo** de su 2025 (~60-73%) —
su inversión 2026 va rezagada (obras G8 devengado=0 en abril). No es maquillaje; es la realidad leída bien.

## Las 3 correcciones (celda a celda)

### 1 · Adscritas Ti=0 → cédula oficial SERCOP
- `H07b!D19` (Bomberos Ti_raw): `0` → **`0.1943`**. El motor leía eSIGEF (vacío); el dato existe en `H90!D7`
  (cédula SERCOP Q1). Jerarquía del propio Excel (`H90` línea 80): **"Cédula oficial > eSIGEF > POA"**.
- `H12!F26:F29` (4 metas `GAD_SIN_ESIGEF`): `0` literal → **`=H07b!B20`** (heredan el Ti del GAD, como las
  otras ~17 metas GAD; era hueco de dato, no cero real).

### 2 · Semáforo `H12!B34` — bug de escala + consciente del corte
- **Escala:** `>=90/70/40/20` → `>=0.90/0.70/0.40/0.20`. `B33` se guarda en fracción (0.27), los umbrales AVEP
  canónicos son fracción → el bug hacía que **SIEMPRE** diera "Ruptura", incluso con ejecución perfecta.
- **Corte:** `=IF(H07_S5!B22>=12, [AVEP fracción], "Corte parcial - lectura preliminar (no comparable con umbral anual)")`.
  No se aplica veredicto anual sobre un corte Q1; la clasificación AVEP solo opera al cierre (mes 12).

### 3 · FactorTemporal — lineal → curva de pacing REAL de Montecristi
- `H07_S5!B23`: `B22/12` (lineal, 0.333 en abril) → **`=IFERROR(CHOOSE(B22, curva), 0.3333)`**.
- Curva (% del anual ejecutado al mes M · inversión · dev acumulado/anual):

  | Mes | 1 | 2 | 3 | **4** | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|
  | pacing % | 1.1 | 11.0 | 12.8 | **21.2** | 26.6 | 36.0 | 44.2 | 51.6 | 76.6 | 88.3 | 92.5 | 100 |
  | lineal % | 8.3 | 16.7 | 25.0 | **33.3** | 41.7 | 50.0 | 58.3 | 66.7 | 75.0 | 83.3 | 91.7 | 100 |

- **Fuente:** `monthly_kpis` (Supabase) · promedio simple de las 3 adscritas con cobertura 2025
  (BOMBEROS 12m · EMAI-EP 11m · PATRONATO 12m) · dev_inv acumulado/anual. Scripts: `scripts/dev/gm_2025_curve.py`.
- **Efecto:** GAD Ti_norm 19.3% → 30.3%. El back-loading es real (gran salto sep-oct: 76%→88%, clásica obra pública).

## Limitaciones DECLARADAS (inexpugnabilidad = honestidad, no fabricar)
1. El **GAD** (dominante, 19/25 metas) NO tiene serie intra-anual 2025 (solo Oct-Dic) → la curva usa las 3 adscritas
   como **proxy**. Promedio **SIMPLE** (no ponderado) porque el GAD es obras-pesado (G8 dev=0 en abril → el más
   back-loaded, como Bomberos); el ponderado lo dominaría EMAI (el más rápido), menos representativo del GAD.
2. Datos 2025 con ruido (duplicados, EMAI mes 7 no-monótono) → curva forzada monótona + normalizada por anual.
3. **Revisar al cerrar 2026** — será la primera curva intra-anual real del propio GAD.
4. **NO se fabricó hipótesis nacional** — todo es dato propio de Montecristi (corrección del colega al académico).

## Verificación (Excel nativo, determinista)
- `B33 = =B31/B32` **INTACTA** · `B31=SUM(J6:J30)` · `B32=SUM(K6:K30)` · denominador B32 idéntico antes/después.
- `B40 = ✅ AXIOMA VERIFICADO: ICPI = 69.9309%` — el guardián de integridad del propio motor PASA.
- **Errores añadidos por la cirugía: 0.** 5 preexistentes idénticos en prístina y aplicada:
  `H00!B155 · H36c!C8 · H36c!C13 · H98!B36 · H99!B45` (peatonales/TGI · fuera del motor ICPI · **pendientes aparte**).

## Estado
- **Copia corregida:** `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260615_D2A_APLICADO.xlsx`
- **Vivo** (`..._TGI.xlsx`): **INTACTO** (mtime 2026-05-30). Promoción a vivo = decisión de Javo (respaldo→freeze primero).

---
*Cirugía Gold Master D.2A · Dylus Lab © 2026 · la fórmula canónica es INMUTABLE · correcciones solo en inputs/semáforo, sobre copia, con evidencia verificada.*
