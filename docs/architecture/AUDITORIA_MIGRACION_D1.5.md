# AUDITORÍA DE MIGRACIÓN — Sprint D.1.5

**2026-06-16 · barrido determinista · "¿dónde siguen viviendo las mentiras?"** (KPI del colega)

> Pregunta: ¿cuánto de QUIRA respira YA el motor vivo (snapshot local 27.46%) vs demo/hardcode/stale?

## 🎯 KPI BRUTAL: MIGRACIÓN ≈ 8% (1 de 12 cajones)
Solo **d06 (Salud Institucional)** lee 100% el snapshot local — sus 3 pestañas (`p_ejecutivo`·`p6_pulso`·`p7_brecha`), tras el cableado de hoy. Los otros 11 cajones siguen en demo/hardcode.

## 🔴 EL ENEMIGO: verdades simultáneas en lugares distintos
El L1 Centro de Mando muestra hardcodes que **contradicen el motor**:

| Métrica | Motor vivo (real) | L1 muestra (hardcode) | ¿Contradice? |
|---|---|---|---|
| ICPI (d06) | **27.46%** | 27.5% | ✅ alineado (fix de hoy) |
| Holding (d05) | ~17% (H90) | **68.7%** | 🔴 SÍ |
| Participación·IGP (d08) | 48.33% | **27.98%** | 🔴 SÍ |
| Género·PSG (d12) | 2.83% | **12.83%** | 🔴 SÍ |

## Mapa cajón → pantalla → fuente
| Cajón | Pantalla detalle (`mod`) | Fuente | Estado |
|---|---|---|---|
| d01 Planificación | `p11_ods` | `load_all` | 🔴 demo |
| d02 Presupuesto | `p18_cooperacion` | `demo_data` | 🔴 demo |
| d03 Metas PDOT | `p8_metas` | `load_all` | 🔴 demo |
| d04 Alertas | `p9_sat` | `load_all` | 🔴 demo |
| d05 Holding | `p2_holding` | verificar | 🟡 |
| **d06 Salud** | **`m1_situacion` (3 tabs)** | **`cargar_gm_snapshot`** | **✅ REAL** |
| d07 Transparencia | `p07_transparencia` | verificar | 🟡 |
| d08 Participación | `p16_confianza` | `load_all` | 🔴 demo |
| d09 RDC | `p17_rdc` | `load_all` | 🔴 demo |
| d10 Territorio | `p10_territorio` | verificar (¿QTMP/Neo4j?) | 🟡 |
| d11 Ecosistema | — | deshabilitado | ⬜ en construcción |
| d12 Protección Social | `p19_genero` | `load_all` | 🔴 demo |

## L1 Centro de Mando — métricas de tarjeta (`_DOMAINS_12`)
- ✅ **Dinámicas (3):** d04 `n_alertas` · **d06 `icpi_pct` (27.46 real)** · d09 `dias_rdc`.
- 🔴 **Hardcodeadas (8):** d01 "56/56" · d02 "$3.66M" · d03 "94.6%" · d05 "68.7%" · d07 "21/21" · d08 "27.98%" · d10 "34.9%" · d12 "12.83%". **3 contradicen el motor (d05·d08·d12).**

## Contaminación demo (pantallas activas que importan `load_all`/`demo_data`)
~14: `p3_congruencias` · `p4_geotwin` · `p8_metas` · `p9_sat` · `p10_inversion` · `p11_ods` · `p12_cadena` · `p13_simulador` · `p14_eficiencia` · `p16_confianza` · `p16_gobernanza` · `p17_rdc` · `p18_cooperacion` · `p19_genero`.
*(Reales: las 3 de d06 · `p_command_center` L1 parcial · `p_cadena_institucional` · `p_concejo` · `env_ops`.)*

## Conclusión
El patrón **`Gold Master → snapshot → pantalla` está PROBADO** (d06, en producción). Falta **REPLICARLO** a los otros 11 cajones + matar los 8 hardcodes del L1. El "17.45 / 27.46 / 53.56 / 68.7 / 27.98 / 12.83" coexistiendo es el enemigo. El motor (d06) está blindado; el resto es cantera por cosechar.

## ▶ Próximo: Sprint D.2 — replicación
Replicar el patrón d06 a d01-d12 (tu arquitectura de cantera: cosechar partes → forma nueva de cajón), eliminando `load_all`/demo/hardcode, con frontera de lenguaje + el builder de snapshot extendido por cajón. Prioridad alta: los 3 hardcodes del L1 que contradicen el motor (d05·d08·d12).

---
*Auditoría de Migración · Sprint D.1.5 · Dylus Lab © 2026 · una sola fuente de verdad.*
