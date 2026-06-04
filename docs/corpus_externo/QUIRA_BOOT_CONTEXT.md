# QUIRA BOOT CONTEXT
## Documento Operacional de Orientación para IAs
**Versión**: 1.0 · Fecha: 2026-06-02 · Custodio: Dylus Lab  
**Uso**: Leer ANTES de abrir cualquier ADR, ACK, DCO o código.  
**Límite**: 5 páginas. No es un resumen narrativo — es la autoridad operacional mínima.

---

## 0. QUÉ ES QUIRA

QUIRA es un **Sistema Operativo de Coherencia Institucional Municipal** — no un dashboard, no un ERP, no un RAG clásico. Es infraestructura de gobernanza preventiva que transforma la operación mensual de un GAD en gobernanza pública verificable, causal y acumulativa.

**Frase canónica**: *"QUIRA evita que el municipio improvise institucionalmente."*

**Equipo**: Javo (fundador · 15 años sector público Ecuador) · Colega asesor (arquitecto externo senior) · Claude (director técnico · arquitecto/ejecutor)

**Escala objetivo**: 221 municipios Ecuador → 6,000 municipios LAC

---

## 1. ARTEFACTOS QUE GOBIERNAN (autoridad descendente)

```
1. Constitución Ecuador / COOTAD / LOPC / LOTAIP  → norma superior
2. Corpus normativo (Supabase · 7,740 chunks · 41 docs)
3. ACK Registry    data/ack_registry.json v0.5 (34 ACKs)
4. ADRs aprobados  docs/adr/ADR-016 a ADR-020
5. Neo4j + centrality_results.json               → evidencia computacional
6. Snapshots       docs/snapshots/               → estado verificable
7. Conversaciones / notas                        → contexto, no autoridad
```

**Regla**: Si una afirmación no puede rastrearse a los niveles 1-6, es hipótesis. Marcarla explícitamente.

**Regla corpus vs DCO**: Cuando el corpus semántico contradice el DCO, el DCO gana. (Caso canónico: corpus devuelve Art.19 para "transparencia" → DCO dice CE_18. El DCO gana.)

---

## 2. ARQUITECTURA EN UNA PANTALLA

```
Cerebro 1: Supabase pgvector  → corpus semántico (similitud, NO autoridad)
Cerebro 2: Neo4j              → grafo causal (autoridad normativa y circuitos)
Cerebro 3: Obsidian           → conocimiento humano estructurado

Flujo canónico:
  NRC (apex constitucional)
    ↓ CONSTITUYE / HABILITA
  ACK normal (operacionalización normativa)
    ↓ ancla a
  DCO (dominio como sistema de razonamiento)
    ↓ sus nodos son
  Circuito (cadena causal multi-dominio)
    ↓ produce
  Diagnóstico (CHS · estado · alerta)

Stack: Streamlit + Python + Neo4j AuraDB + Supabase pgvector + Claude Haiku
```

**Los 5 NRCs del sistema** (Community 0 Louvain — verificado):

| NRC | Tipo | Alcance |
|---|---|---|
| CE_1 | constituyente · soberanía popular | apex ontológico — CASCADE=39 |
| CE_226 | principio · legalidad | todos los dominios — CASCADE=34 |
| CE_95 | derecho · participación | Dom08, Dom09, Dom07 — CASCADE=22 |
| CE_18 | derecho · información | Dom07, Dom08, Dom09 — CASCADE=19 |
| CE_264 | competencia · GAD Municipal | Dom04, Dom10 — CASCADE=17 |

---

## 3. DOMINIOS Y CIRCUITOS ACTIVOS

**12 dominios canónicos** (Dom01–Dom12) — INMUTABLES sin nuevo ADR.

**DCOs activos** con cobertura normativa cargada en Neo4j:
```
Dom07 · Transparencia Activa          → LOTAIP + LOPC · ORIGEN C01
Dom08 · Participación Ciudadana       → 15 ACKs LOPC · INTERMEDIARIO C01
Dom09 · Rendición de Cuentas (seed)   → 4 ACKs · DESTINO C01 · INCOMPLETO
```

**Circuito C01** (activo): Dom07 → Dom08 → Dom04

**Par constitucional** (STRONGLY_SUPPORTED): Dom08 ↔ Dom09 vía GENERA+RETROALIMENTA

---

## 4. ESTADO DE HIPÓTESIS

| Hipótesis | Estado | Evidencia | Pendiente |
|---|---|---|---|
| NRCs forman Comunidad 0 (Louvain) | **CONFIRMED** | centrality_results.json O-02 | — |
| Dom08 es hub de legitimación democrática | **CONFIRMED** | betweenness 4.59× Dom07 (M2) | — |
| CE_1 > CE_226 en cascade constitucional | **CONFIRMED** | CASCADE=39>34 (M6) | — |
| Dom08+Dom09 = "Sistema Democrático Constitucional" | **STRONGLY_SUPPORTED** | C1+C2+C4b PASS | C3: Dom09 completo + re-run |
| LOPC = ley de coordinación constitucional | **CANDIDATO** | LOPC_101=27 (supera CE_95=22) | ADR-021 pendiente · verificar con Dom09 |
| H1-H8 causalidad territorial | **HIPÓTESIS** | inferidas, no validadas | Red Académica (FLACSO/IAEN) |

**Por qué ADR-019 NO es CONFIRMED todavía**:
- C4b usa Cascade Score — métrica propia de QUIRA, no estándar de teoría de grafos
- C3 fue reformulado (diferentes comunidades = PASS) — el criterio original falló
- Dom09 es seed: Comunidad 3 (Dom09) tiene solo 4 ACKs; con Dom09 completo (~15 ACKs) la comunidad será más robusta
- CONFIRMED requiere: Dom09 completo + re-run con métricas estándar (betweenness, Louvain) corroborando Cascade Score

---

## 5. GATES Y ESTADO

```
Gate 0  QUIRA_STATE v2.0       ✅  2026-06-02
Gate 1  ACK Registry v0.5      ✅  commit c3c815c — 34 ACKs · Neo4j=JSON
Gate 2  Cascade Score M6       ✅  commit cfb6595 — reproducible en JSON
Gate 3  Dom09 completo         ⏳  COOTAD 266+ · LOPC 88-97 · Neo4j extension
Gate 4  Re-run analítico       ⏳  después de Gate 3 · snapshot estable
Gate 5  ADR-019 CONFIRMED      ⏳  después de Gate 4 · si evidencia sostiene
```

**Lo que NO hacer hasta Gate 5**: no abrir ADR-021 (LOPC candidato), no crear nuevos dominios, no cambiar taxonomía principal.

---

## 6. BLOOMBERG FIREWALL (CRÍTICO)

Nunca en UI / API / reportes externos / comentarios visibles al usuario:

```
Gold Master · ICPI · Ti · TGI · QTMP · H-series (H01-H99) · QNKC · PSG
IOC · IGP · IET · H41_IOC · SIAP · Sprint Canon · metodología interna
ACK IDs · DCO IDs · NRC IDs · nombres de circuitos internos
```

El mundo ve el espejo. La metodología es del laboratorio.

---

## 7. RUTAS CANÓNICAS

```
Repo principal:   C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\
Governance:       C:\Users\DELL\Desktop\Javo\Dylus Lab\governance\
ProyecT (local):  C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\
Gold Master:      ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx  [SECRETO]
Memoria Claude:   C:\Users\DELL\.claude\projects\C--Users-DELL-Desktop-Javo-Quadrum-Gov-Tech\memory\
Skills QUIRA:     C:\Users\DELL\.claude\skills\quira-orient\ (skill de arranque)
```

**Archivos críticos de arranque**:
1. `quira-os/CLAUDE.md` — reglas de construcción
2. `governance/QUIRA_STATE.md` v2.0 — estado completo del proyecto
3. `governance/QUIRA_BOOT_CONTEXT.md` (este) — orientación mínima

**Para sesión nueva**: leer este doc + QUIRA_STATE.md + ADR-018/019/020 + DCO Dom08/09. Con esos 7 artefactos tienes 90% del contexto.

---

## 8. ANTI-PATRONES CONOCIDOS

| Error | Por qué falla | Correcto |
|---|---|---|
| Mover hipótesis a CONFIRMED con una sola métrica | Una métrica propia no basta — se necesitan métricas estándar corroborando | STRONGLY_SUPPORTED hasta re-run con métricas estándar |
| Reformular criterio de hipótesis para hacer PASS | Eso no es evidencia, es ajuste | Documentar el fallo y esperar más datos |
| Art.19 = transparencia | Corpus devuelve similitud, no autoridad | DCO: CE_18 es norma fundante |
| "Terra en C:\Desa\" | Proyecto antiguo abandonado | IGNORAR COMPLETAMENTE |
| canton_id en ACK Registry | Viola principio de alcance nacional | Nunca. El código lo rechaza. |
| Crear ACK = crear ADR | ACKs son átomos normativos; ADRs son decisiones arquitectónicas | Distinción estricta |

---

*QUIRA_BOOT_CONTEXT v1.0 · Dylus Lab © 2026*  
*"QUIRA no impone una teoría de gobernanza — revela la que el ordenamiento jurídico ya diseñó."*  
*Actualizar al cerrar cada sprint significativo que cambie hipótesis o estado de gates.*
