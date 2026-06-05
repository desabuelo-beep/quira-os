# QUIRA Gov v1.1 DEMO — Resumen Histórico
> Archivo fuente: `QUIRA_Gov_v1.1_DEMO.html` (raíz del repo)
> Fecha de análisis: 2026-06-05 | Corpus Histórico Dylus Lab

## 1. Descripción general
HTML single-page application (SPA) puro — sin framework, sin servidor.
Paleta idéntica a la actual: navy-deep/navy-mid, cyan #00D4FF, red #FF4D6D, amber #FFB800, green #00E096, purple #7C5CFC.
Splash screen animado, modal para API key de IA, toggle de roles (Alcalde/Concejal/Técnico) en el header.
Score global visible en header: **53.56% · Transición Crítica** (ICGI-T Q1-2026).

## 2. Módulos y pantallas del DEMO

### Sidebar — 7 secciones, 19 pantallas

| Sección | Código | Pantalla |
|---|---|---|
| ① Executive Pulse | P-00 | Pulso Ejecutivo |
| ① Executive Pulse | P-01 | Gobernanza · ICGI-T |
| ① Executive Pulse | P-02 | Causas de la Brecha |
| ② Fidelidad Política | P-03 | Metas PDOT |
| ② Fidelidad Política | P-05 | 4 Congruencias · HPT-M |
| ③ Inteligencia Operativa | P-06 | Eficiencia por Dirección |
| ③ Inteligencia Operativa | P-08 | Cadena POA·PAC·Presupuesto |
| ③ Inteligencia Operativa | P-09 | Alertas SAT Preventivas |
| ④ Equidad Territorial | P-04 | GeoTwin · 7 Parroquias |
| ④ Equidad Territorial | P-10 | Inversión per Cápita |
| ⑤ Holding Municipal | P-07 | Holding Sandbox |
| ⑤ Holding Municipal | P-12 | ODS · Fondos Externos |
| ⑤ Holding Municipal | P-13 | Escenarios 2027 |
| ⑥ Sentinel Action Center | P-11 | Simulador de Decisiones |
| ⑥ Sentinel Action Center | P-14 | Confianza · Trazabilidad |
| ⑥ Sentinel Action Center | P-15 | Evidencia Documental |
| ⑥ Sentinel Action Center | P-16 | SENTINEL · IA |
| ⑦ Operación Técnica | P-17 | Ingesta de Cumplimiento |
| ⑦ Operación Técnica | P-18 | Validador Cruzado |
| ⑦ Operación Técnica | P-19 | Auditor HITL |

## 3. Datos mostrados en P-00 (pantalla principal)

- **4 metas PDOT sin ruta de ejecución** (M-03 agua, M-07 fiscal, M-11 género, M-18 participación)
- **Inversión per cápita Isabel Muentes: $40/hab** vs. cabecera $113/hab; TPS 77.94 (máxima urgencia)
- **Ejecución género: 1%** de $438K asignados; bloquea $95K BID Lab Gender Bond
- **4 Congruencias semáforo**: Política 58.4% 🟠, Operativa 47.2% 🔴, Territorial 44.8% 🔴, Ecosistémica 61.1% 🟠
- **Proyección riesgo sin corrección Q2**: ICGI-T cae a 47.8%, $2.4M PNUD bloqueados
- **Oportunidad con corrección Q2**: ICGI-T sube a 64.2%, $2.58M desbloqueados (PNUD+GEF), BID Lab activado

## 4. Decisiones de diseño rescatables

| Decisión | Valor para versión actual |
|---|---|
| Paleta completa ya definida en CSS variables | Idéntica a la actual — continuidad confirmada |
| Numeración P-00 a P-19 con sección sidebar agrupada | La versión actual usa m1-m5 como agrupadores; el DEMO usó secciones textuales (① a ⑦) — más legible en sidebar |
| Score ICGI-T en el header siempre visible | La versión actual mueve el score al p0_inicio; el DEMO lo ponía en badge permanente — decisión de Sprint A |
| Toggle de roles en el header | Reemplazado por login/roles en Supabase — más robusto pero menos inmediato para demo |
| Modal API key para activar IA | Reemplazado por integración directa Claude Haiku via connector — correcto |
| Splash screen animado con barra de carga | No implementado en Streamlit (limitación técnica) |
| Navigation JavaScript puro (nav() function) | Reemplazado por routing Streamlit — obligatorio para el stack actual |
| DOP-01 (Dirección Obras Públicas) con IED pendiente H30 | Dato vivo en versión actual via Gold Master |
| Riesgo/Oportunidad en formato dual card (rojo/verde) | Rescatable para p_vista_ejecutiva.py zona 2 |
| Sección ⑦ Operación Técnica separada visualmente | Implementado como m5_control.py solo-técnico — mantiene la separación |

## 5. Qué fue superado por la versión actual

| Aspecto DEMO v1.1 | Versión actual (Sprint A+) |
|---|---|
| Datos hardcodeados en HTML con JS | Datos reales desde Gold Master + Supabase via connectors |
| Sin autenticación real | Roles reales (Alcalde/Técnico/Operador/Admin) via Supabase |
| IA opcional via modal API key | Claude Haiku integrado como conector permanente |
| 19 pantallas planas (P-00 a P-19) | 48 módulos organizados en capas L1/L2/L3 + módulos m1-m5 |
| Scoring ICGI-T estático Q1-2026 | TGI dinámico via Gold Master connector; lectura Excel real |
| Sin Sentinel / sin alertas automáticas | Sentinel completo: alert_engine, learning_engine, sla_db, governance_engine |
| Sin ingesta documental real | p_ingesta.py: parser cédula presupuestaria, SHA256, Supabase |
| Sin histórico longitudinal | p_historico.py: curvas Ti por entidad, Plotly, Supabase |
| Bloomberg Firewall no documentado | ADR-023 ratificado: 3 niveles de exposición, inmutable |
| Holding como "Sandbox" P-07 | p2_holding.py: datos reales SERCOP API 5 entidades |
| P-12 "ODS · Fondos Externos" combinado | p11_ods.py + p18_cooperacion.py separados con datos verificados |
| P-14 "Confianza · Trazabilidad" genérico | p16_confianza.py + p16_gobernanza.py con fuentes Gold Master H31/H63/H10c |

## 6. Números clave del DEMO que siguen vigentes (continuidad histórica)

- ICGI-T base: **53.56%** (Q1-2026) — mismo corte en versión actual
- ISP: **14.58%** (bajo umbral COOTAD 65%)
- IET: **$40/hab** parroquia más crítica (Isabel Muentes)
- IGP: **27.98%**
- PSG: **12.83%** (ejecución género)
- IOC: **17.71%** (opacidad)
- 4 metas sin PAC — SAT-0 activa
- 24 procesos sin SHA-256 — "Gasto Ciego C4"
- Umbral cooperación PNUD: **≥55%** ICGI-T (brecha: 1.44 pts en demo)

---
*Corpus Histórico QUIRA — Dylus Lab © 2026*
