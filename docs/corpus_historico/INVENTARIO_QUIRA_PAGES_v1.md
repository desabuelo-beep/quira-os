# Inventario quira_pages — v1
> Generado: 2026-06-05 | Fuente: lectura primeras 35 líneas de cada archivo
> Total archivos: 48 (incluye __init__.py, html_engine.py y archivos env_*)

## Tabla principal

| Archivo | Función | Dominio | Estado |
|---|---|---|---|
| `p0_inicio.py` | Ficha cantonal identidad institucional — alcalde, período, presupuesto, parroquias, SAT descriptores; Bloomberg Firewall activo (sin ICPI/TGI) | Portada / Sprint A | Activo |
| `p1_dashboard.py` | Entry point MVC — delega render al DashboardController | Infraestructura / Router | Activo |
| `p2_holding.py` | Holding Municipal Cajón 1 — Contratación Pública SERCOP; 5 entidades (GAD, Patronato, Bomberos, EMAI, EP Hábitat); datos reales SERCOP API 2023-2026 | Holding Municipal | Activo |
| `p3_congruencias.py` | 4 Congruencias HPT-M (Política / Operativa / Territorial / Ecosistémica) — cards con scores, barras de progreso, preguntas Sentinel | Congruencias | Activo |
| `p4_geotwin.py` | GeoTwin Territorio — mapa Folium/Leaflet + tabla parroquias + Gov Twin; carga GeoJSON parroquias | Territorial / D10 | Activo |
| `p5_operacion.py` | Operación Técnica Backoffice — orquesta P-17 Ingesta, P-18 Validador, P-19 HITL como sub-páginas; visible solo técnico | Infraestructura Técnica | Activo |
| `p6_pulso.py` | Pulso Ejecutivo — KPIs críticos (ICGI-T, congruencias, SAT, PSG, IET) en un vistazo; fiel a DEMO.html P-00 | Ejecutivo | Activo |
| `p7_brecha.py` | Causas de la Brecha — vectores causales (ISP -8.2, IED -6.8, etc.) que explican caída ICGI-T | Análisis / D01-D12 | Activo |
| `p8_metas.py` | Metas PDOT — trazabilidad Promesa→Meta→Ejecución; metas M-01 a M-25; datos PDOT+Gold Master | Planificación PDOT | Activo |
| `p9_sat.py` | Alertas SAT Preventivas — matriz de riesgo institucional (Fiscal / Contractual / Transparencia); 9 tipos SAT-0 a SAT-VIII | Alertas / SAT | Activo |
| `p10_inversion.py` | Inversión per Cápita — equidad territorial $/hab por parroquia; 8 ejes sectoriales; meta $80/hab | Territorial / D10 | Activo |
| `p10_territorio.py` | Dom10 Agua Potable y Cobertura Territorial — Layer 2 canónico; Bloomberg Model; ADR-013; semáforo + narrativa causal | D10 Agua/Territorio | Activo |
| `p11_ods.py` | ODS Tracker Agenda 2030 — 17 ODS con estado Montecristi; vinculación PDOT↔ODS; ICODS 87.5%; 4 scores del Gold Master | ODS / D11 | Activo |
| `p12_cadena.py` | Cadena POA·PAC·SERCOP·eSIGEF — trazabilidad operativa; 4 metas sin contrato PAC (SAT-0) | Planificación / D12 | Activo |
| `p13_simulador.py` | Simulador de Escenarios — ¿Qué ICGI-T logramos si mejoramos X?; modelo simplificado vectores; Tab 2 sensibilidad IRS | Análisis / Técnico | Activo |
| `p14_eficiencia.py` | Eficiencia por Dirección — IED 33.99%; ranking 12 Direcciones GAD; SAT por dirección; SIAP-ICPI Q1-2026 | D14 Eficiencia Institucional | Activo |
| `p15_transparencia.py` | Transparencia LOTAIP — ITAM 56%; IOC 17.71%; estado de 21 artículos LOTAIP; portal municipal | D15 Transparencia | Activo |
| `p16_confianza.py` | Confianza Ciudadana — IGP 27.98%; 6 mecanismos participación (Asambleas, PP, UT, RDC, Veedurías, Portal) | D16 Confianza | Activo |
| `p16_gobernanza.py` | Gobernanza Participativa — Tab1: PP 2024/2025/2026, parroquias, IGP; Tab2: Control Social, RDC CPCCS, IFE, ICM vs ICPI, aportes ciudadanos | D16 Gobernanza | Activo |
| `p17_rdc.py` | Rendición de Cuentas 2026 — checklist CPCCS 30 ítems por categoría (Normativa/Financiero/PDOT/Participación/Transparencia/Género) | D17 RDC | Activo |
| `p18_cooperacion.py` | Cooperación Internacional — portafolio fondos BID/CAF/PNUD/ONU Mujeres/GEF; elegibilidad y deadlines | D18 Cooperación | Activo |
| `p19_genero.py` | Género y Equidad + Ambiente — Tab1: PSG 12.83%, ODS 5, Gender Bond, IGM 6 sub-indicadores; Tab2: metas FA PDOT, PP 2026, RDC aportes ambientales | D19 Género/Ambiente | Activo |
| `p07_transparencia.py` | Dom07 Transparencia e Información Pública — Layer 2; dualidad epistémica QNKC-P01 (C4×C5a×C5b×C5c); ADR-013+ADR-014; fuente canónica DPE | D07 Transparencia | Activo |
| `p_historico.py` | Inteligencia Histórica Holding Municipal — Sprint 2.5B; evolución Ti por entidad; ranking ejecución inversión; semáforo alertas automático; usa Plotly | Holding / Sentinel | Activo |
| `p_congruencia.py` | Estado de Congruencia Institucional — Sprint 2.5C; parity_engine + integrity_engine; visible analista/director/alcalde | Congruencias / Sentinel | Activo |
| `p_ingesta.py` | Centro de Ingesta Mensual — Sprint 2.5A; upload cédula presupuestaria xlsx; parser valida G1-G5; calcula Ti mensual; SHA256; Supabase | Infraestructura Técnica / Sentinel | Activo |
| `p_seguimiento.py` | Seguimiento Institucional — Sprint 2.6.2; aging de alertas; reincidencia por entidad; ranking riesgo institucional; alertas sin resolver | Sentinel / Gobernanza | Activo |
| `p_reportes.py` | Reportes Institucionales Mensuales — Sprint 2.6.3; genera PDF ejecutivo corte mensual Holding; para alcalde/concejales/Contraloría/LOTAIP | Sentinel / Reporting | Activo |
| `p_aprendizaje.py` | Aprendizaje Institucional Trazable — Sprint 2.8A; cómo el sistema aprende de resoluciones humanas; categorías, frecuencias, tiempos, ejemplos auditables | Sentinel / IA | Activo |
| `p_gestion.py` | Ruta de Atención Institucional — Sprint 2.9A; gobernanza operativa; estados formales, ownership, escalamiento, bitácora inmutable por alerta | Sentinel / Gobernanza | Activo |
| `p_sentinel_hub.py` | Centro de Inteligencia Territorial — Pantalla 0; datos del gm_snapshot.json + SENTINEL API localhost:8100; TGI/financiero/territorial/parroquias | Sentinel / Centro de Control | Activo |
| `p_alertas.py` | Centro de Alertas de Cumplimiento — Sprint 2.6; alertas ejecución Ti + cobertura; export XLSX; SLA badge; learning engine sugerencias resolución | Sentinel / Alertas | Activo |
| `p_ejecutivo.py` | Vista Ejecutiva Alcalde/Directivos RC-1 — semáforos sin tablas; ¿Cómo está el municipio? ¿Qué requiere atención? SAT + SLA | Ejecutivo | Activo |
| `p_carga.py` | Panel de Carga Mensual RC-CARGA — upload gm_snapshot.json por técnico; valida y guarda en Supabase; acceso solo Técnico | Infraestructura Técnica | Activo |
| `p_cadena_institucional.py` | Cadena Institucional Sprint E.1 — vista técnica del analista; orquesta CNE→PDOT→POA→PAC→Presupuesto→PP→RdC→LOTAIP; recicla p8/p12/p15/p16/p17 como tabs | Planificación / Técnico | Activo |
| `p_vista_ejecutiva.py` | Vista Ejecutiva Sprint C.3 — jerarquía de atención 3 capas; TGI + SAT sistémicas; grid Z1-Z6; motor TOP desde utils/top.py; 3s de lectura crítica | Ejecutivo | Activo |
| `p_concejo.py` | Panel Estratégico Sprint C.2 — preparación política datos reales Gold Master v5.5; 6 vectores de ataque oposición + respuestas; argumentario | Ejecutivo / Político | Activo |
| `p_command_center.py` | Centro de Mando Sprint D.3.2 — teatro operacional full-screen; cards 12 dominios D01-D12; TGI+Holding; cargar desde gm_snapshot.json | Infraestructura / L1 Centro Mando | Activo |
| `m1_situacion.py` | Módulo M1 Situación — consolida Vista Ejecutiva + Pulso + Causas de Brecha en tabs | Router / Módulo | Activo |
| `m2_alertas.py` | Módulo M2 Alertas — consolida SAT Activas + Evolución Longitudinal RC-M en tabs; Sprint 3 Longitudinal Engine | Router / Módulo | Activo |
| `m3_municipal.py` | Módulo M3 Municipal — consolida Holding + Gobernanza + Transparencia + Inversión en tabs | Router / Módulo | Activo |
| `m4_analisis.py` | Módulo M4 Análisis — consolida Tablero Técnico + Eficiencia + Metas + Cadena + Operación; tabs extra para técnico | Router / Módulo | Activo |
| `m5_control.py` | Módulo M5 Control (solo Técnico) — 9 tabs: Centro Control, Carga, Ingesta, Historial, Monitor Alertas, Seguimiento, Reportes, Gestión, Sentinel IA | Router / Módulo | Activo |
| `env_gov.py` | Router GOV v4 Sprint A+ — mapea 26 rutas hacia m1-m5 y p0-p19; 2 secciones (Ejecutiva / Técnica); puro, sin lógica de negocio | Infraestructura / Router | Activo |
| `env_civic.py` | QUIRA Civic — placeholder vista pública participativa ciudadanía; estado FUTURO (roadmap cuando GOV estable) | Futuro / Placeholder | Legacy/Placeholder |
| `env_impact.py` | QUIRA Impact — placeholder outputs estratégicos para cooperación internacional (BID/PNUD/CAF); estado FUTURO | Futuro / Placeholder | Legacy/Placeholder |
| `env_ops.py` | Ambiente Ops — infraestructura interna equipo QUIRA; 5 tabs: Pipeline, Snapshots, Reliability, Gold Master, Configuración; acceso Operator/Admin | Infraestructura / Ops | Activo |
| `html_engine.py` | Shim de compatibilidad — re-exporta desde views/html_engine.py; mantiene imports existentes sin cambios | Infraestructura / Shim | Activo |
| `__init__.py` | Vacío (1 línea) | Infraestructura | Activo |

## Resumen estadístico

| Categoría | Cantidad |
|---|---|
| Total archivos | 48 |
| Páginas de contenido (p0–p19, p_*) | 36 |
| Módulos router (m1–m5) | 5 |
| Ambientes (env_*) | 4 |
| Infraestructura (html_engine, __init__) | 2 |
| Placeholders futuros | 2 (env_civic, env_impact) |
| Activos | 46 |
| Legacy/Placeholder | 2 |

## Mapa de capas UI según env_gov.py

```
EJECUTIVA (todos los roles):
  inicio → p0_inicio | situacion → m1 | alertas → m2 | municipal → m3
  ods → p11 | confianza → p16_confianza | rdc → p17 | cooperacion → p18
  genero → p19 | territorio → p10_territorio | transparencia → p07

TÉCNICA (solo Técnico/Operador/Admin):
  analisis → m4 | geotwin → p4 | congruencias → p3
  simulador → p13 | control → m5
```

---
*Corpus Histórico QUIRA — Dylus Lab © 2026*
