# MAPA DE NAVEGACIÓN — Dashboards QUIRA (qué está vivo, muerto y duplicado)
**Sprint C · 2026-06-12 · construido navegando el grafo de código (codegraph + imports)**

> Hallazgo madre: los "40+ dashboards" NO son 40 pantallas a refactorizar.
> Son una JERARQUÍA de módulos-contenedor + páginas-hoja, con CÓDIGO MUERTO
> conviviendo con el vivo. El "shampoo" es en buena parte huérfanos y duplicados.
> Refactorizar sin este mapa = refactorizar pantallas que nadie ve.

---

## ⚰️ CÓDIGO MUERTO — archivar primero (limpieza barata que reduce el shampoo)

Verificado por grafo de imports: nadie los rutea para render.

| Archivo | Estado | Reemplazado por | Acción |
|---|---|---|---|
| **p_vista_ejecutiva.py** (1520 líneas) | HUÉRFANO — solo se auto-referencia | el Centro de Mando v2 + m1_situacion | archivar |
| **p0_inicio.py** | HUÉRFANO post-v2 (solo en comentarios) | p_command_center_v2 | archivar |
| **p_congruencia.py** | HUÉRFANO (duplicado) | p3_congruencias (vivo) | archivar |
| **p15_transparencia.py** | DEPRECATED (lo dice su propio código) | p07_transparencia (vivo) | archivar |
| **p_command_center.py** (v1) | semi-vivo: solo fallback + `_load_data` | p_command_center_v2 | conservar SOLO como fallback; migrar `_load_data` a v2 luego |

**⚠️ Corrección a la auditoría Bloomberg previa:** medía violaciones SIN saber si
la página estaba viva. p_vista_ejecutiva (32) y p0_inicio (11) eran las "peores"
— y están muertas. La auditoría se re-corre SOLO sobre los vivos.

---

## ✅ LO VIVO — entorno GOV (lo que ve el alcalde/técnico)

Jerarquía real: **módulos-contenedor (M)** que agrupan y rutean a **páginas-hoja (P)**.

### Sección Ejecutiva (todos los roles GOV)
| Cajón / módulo | Archivo | Páginas-hoja que rutea |
|---|---|---|
| INICIO (Centro de Mando) | `p_command_center_v2` ✅ ya nativo | — |
| Situación Institucional | `m1_situacion` | p_ejecutivo · p6_pulso · p7_brecha |
| Metas PDOT (D03) | `p8_metas` | (hoja) |
| Alertas | `m2_alertas` | p9_sat |
| Gestión Municipal | `m3_municipal` | p2_holding · p16_gobernanza · p07_transparencia · p10_inversion |
| ODS | `p11_ods` | (hoja) |
| Confianza Ciudadana | `p16_confianza` | (hoja) |
| Rendición de Cuentas | `p17_rdc` | (hoja · ya tiene C-RDC live) |
| Cooperación | `p18_cooperacion` | (hoja · ya lector Supabase) |
| Género y Ambiente | `p19_genero` | (hoja) |
| Cadena Institucional | `p_cadena_institucional` | p16_gobernanza · p8_metas · p12_cadena · p16_confianza · p17_rdc · p07_transparencia |
| Territorio | `p10_territorio` | (hoja) |
| Transparencia | `p07_transparencia` | (hoja · compartida) |

### Sección Técnica (Técnico/Operador/Admin)
| Módulo | Archivo | Páginas-hoja |
|---|---|---|
| Análisis Estratégico | `m4_analisis` | p1_dashboard · p14_eficiencia · p8_metas · p12_cadena · p5_operacion |
| GeoTwin | `p4_geotwin` ✅ F1 cableado | (hoja) |
| Congruencias | `p3_congruencias` | (hoja) |
| Simulador | `p13_simulador` | (hoja) |
| Centro de Control | `m5_control` | p_sentinel_hub · p_carga · p_ingesta · p_historico · p_alertas · p_seguimiento · p_reportes · p_gestion |
| Concejo | `p_concejo` | (hoja) |

## ✅ LO VIVO — entorno OPS (Dylus Lab)
`env_ops` → p_sentinel_hub · p_carga · p_ingesta · p_historico · p_seguimiento · p_reportes · p_aprendizaje · p_gestion · p_alertas

## ⏳ env_civic (Ciudadana) y env_impact (Cooperación)
NO rutean dashboards en el grafo → **placeholders.** Coherente: Ciudadana es
producto de Fase 1 aún por construir; Impact/Cooperación es Fase 2. (Nomenclatura
Canónica ya los marca "Fase 3" y "Placeholder".)

---

## DUPLICADOS — aclarar en el refactor (no todos son duplicados reales)

| Par | Veredicto |
|---|---|
| p07 vs p15 transparencia | p15 MUERTO → archivar |
| p3_congruencias vs p_congruencia | p_congruencia MUERTO → archivar |
| p16_confianza vs p16_gobernanza | AMBOS vivos — ¿confianza ciudadana ≠ gobernanza municipal? VERIFICAR en refactor |
| p12_cadena vs p_cadena_institucional | NO duplicado: uno es hoja, otro contenedor |
| m2_alertas vs p9_sat vs p_alertas | NO duplicado: GOV-contenedor / GOV-hoja / OPS — distintos contextos |

---

## IMPLICACIÓN PARA EL REFACTOR (el número real)

- **No son 40+ pantallas planas.** Son ~13 entradas ejecutivas GOV + ~6 técnicas,
  muchas compartiendo hojas reusadas (p8_metas, p07, p16 aparecen en varios).
- **Primero archivar los 5 muertos** → el shampoo baja de golpe, sin riesgo.
- **El refactor real de cara al alcalde** = las ~13 entradas de la Sección Ejecutiva GOV.
- **Cooperación (p18) y RDC (p17)** ya están medio modernizadas → mejores pilotos.
- **GeoTwin (p4)** ya tiene F1 cableado.

## MAPA DE CONOCIMIENTO (TGI/TOP/ICPI/AVEP/metodología)
NO se mapea todo de golpe (gasta tokens). Se navega **on-demand**: al refactorizar
cada dashboard, se consulta el grafo/Obsidian SOLO por el término que esa pantalla
usa. AVEP y MMP ya definidos por Javo (2026-06-12). TGI/TOP/ICPI → buscar en
Obsidian (`C:\Proyectos\QUIRA\knowledge_base`) + grafo cuando toque la pantalla.

---

---

## AUDITORÍA BLOOMBERG SOBRE VIVOS (re-corrida 2026-06-12, post-archivado)

Ranking real (ya sin las pantallas muertas que contaminaban):

| Sev | Página | Violaciones | Nota |
|---|---|---|---|
| 🔴 | p07_transparencia | 31 | la peor REAL (p_vista_ejecutiva ya archivada) |
| 🟠 | p_ejecutivo · p_concejo | 18 c/u | p_concejo: TGI×12 |
| 🟠 | m2_alertas | 17 | ICPI/SAT |
| 🟠 | p16_gobernanza · p12_cadena | 13 c/u | |
| 🟠 | p_cadena_institucional · p9_sat | 10 c/u | |
| 🟡 | 13 páginas | 1-7 c/u | p18(6) · p17(2) · p19(7) · p4(3) … |
| 🟢 | LIMPIAS | 0 | p_command_center_v2 ✅ · p2_holding (961 líneas, 0!) · m1/m3/m4 (wrappers) · p1_dashboard (stub) |

**Pilotos recomendados** (manejables + ya modernizados, para calibrar método):
p18_cooperacion (6 · lector Supabase) · p17_rdc (2 · C-RDC live). La joya
p07_transparencia (31) se ataca con el método YA rodado, no de primera.

*Mapa de Navegación · Sprint C · Dylus Lab © 2026 · read-only, ningún código de producto tocado.*
