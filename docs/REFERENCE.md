# QUIRA · REFERENCE — Detalle de Construcción

> Referencia consultable. NO se lee al arranque — solo cuando trabajas en el área específica.
> Movido desde CLAUDE.md (2026-06-03) para aligerar el contexto de arranque.

---

## ARQUITECTURA 3 CAPAS UI — nunca mezclar responsabilidades

```
Layer 1 → p_command_center.py  → Centro de Mando: 12 cajones HTML canvas
          Full-screen, sin sidebar, navegación postMessage. COMPLETO — no modificar estructura.
Layer 2 → p11-p19, m1-m5, p_*  → Dashboard por dominio (drill-in desde Layer 1)
          Una pantalla/dominio. Narrativa causal. Fuentes públicas. CONSTRUIR cajón por cajón.
Layer 3 → p4_geotwin.py        → GeoTwin mapa territorial Folium. Solo rol Técnico.
          GeoTwin NO es dominio — es la capa de proyección espacial (Layer 3).
```

## ROUTER — env_gov.py
```
REGLA: env_gov.py ES ROUTER PURO. Zero contenido, zero lógica de negocio.
Un archivo = un módulo. Nueva feature → nuevo archivo + UNA LÍNEA en _GOV_MODULES.
```

## 12 DOMINIOS CANÓNICOS — INMUTABLES
| ID | Nombre | Módulo | Archivo | Rol |
|---|---|---|---|---|
| D01 | Planificación Estratégica | ods | p11_ods.py | Todos |
| D02 | Presupuesto & Financiamiento | cooperacion | p18_cooperacion.py | Todos |
| D03 | Seguimiento de Metas | situacion | m1_situacion.py | Todos |
| D04 | Alertas Institucionales | alertas | m2_alertas.py | Todos |
| D05 | Holding Municipal | municipal | m3_municipal.py | Todos |
| D06 | Salud Institucional | situacion | m1_situacion.py | Todos |
| D07 | Transparencia | municipal | m3_municipal.py | Todos |
| D08 | Participación Ciudadana | confianza | p16_confianza.py | Todos |
| D09 | Rendición de Cuentas | rdc | p17_rdc.py | Todos |
| D10 | Territorio & Cobertura | geotwin | p4_geotwin.py | Técnico |
| D11 | Ecosistema Productivo Territorial | — | DISABLED | — |
| D12 | Protección Social & Grupos Prioritarios | genero | p19_genero.py | Todos |

D12 tiene QTMP GAP_10PCT completo en Neo4j. **NUNCA agregar nuevo dominio** (D01-D12 inmutables).

## BLOOMBERG FIREWALL — detalle completo
PROHIBIDO en UI/API/reportes/comentarios visibles:
```
Gold Master · H-series (H01-H99, H07b, H41, H73…) · ICPI·TGI·IFE·IED·ITAM·IGP·IPE·PSG·ISP·IOC·IET
Fórmulas Ti·Vi·Pi·Ri·Ei (como variables) · QTMP IDs (SP_G10P_MCR…) · ACK IDs · Protocolos QTMP·ACK·QLEP·QNKC
node IDs internos (Dom07·C01·CE_226)
```
```python
# MAL ❌  "Ti_Patronato_2025 = 50% (H07b fila 18)"
# BIEN ✓ "Ejecución presupuestaria del Patronato: 50% — 3 años bajo umbral"
# MAL ❌  "ICPI: 17.4% — Ruptura Sistémica"
# BIEN ✓ "Cumplimiento institucional: 17.4% — 47.6 puntos bajo umbral 65%"
```
Checklist pre-commit UI: ¿Gold Master? ¿H00-H99? ¿ICPI/IOC/IGP/IET/IED/IFE/PSG/ISP/ITAM? ¿Ti=/Vi=/Pi=? → ELIMINAR.
Test: ¿el texto se entiende sin conocer la metodología? → APROBADO.

## ROLES Y ACCESO
```
Ejecutivo    → Centro de Mando (sin sidebar, sin sección técnica)
Directivo    → Sidebar + 9 módulos ejecutivos
Técnico      → Sidebar + 14 módulos (geotwin, cadena, simulador, control)
Administrador → Todo
```
```python
from utils.session import is_ejecutivo, is_tecnico, is_admin, get_rol
# is_ejecutivo() solo alcalde/concejales · is_tecnico() Técnico/Operador/Admin
```
NUNCA agregar items al sidebar del Ejecutivo.

## FUENTE DE VERDAD — jerarquía (conflicto: la más alta gana)
```
1. Constitución/COOTAD/COPLAFIP  → norma superior (no modificar)
2. SIGEF (cédulas)               → dato oficial público
3. Gold Master (interno SECRETO) → cálculo canónico
4. QTMP yaml                     → observación QUIRA estructurada
5. gm_snapshot.json / Supabase   → derivados runtime
```

## PATRONES DE CÓDIGO
```python
from utils.cache_quira import cargar_snapshot, cargar_gm_snapshot
snap, _meta = cargar_snapshot()      # 5 min cache
gm          = cargar_gm_snapshot()   # 15 min cache
from utils.css_tokens import C
color = C.sem(valor_pct)             # "#22C55E"/"#F97316"/"#EF4444"
```
Template Layer 2 (cada cajón): 1) KPI dominio (lenguaje gobernanza) 2) narrativa causal 3) indicadores+semáforo+fuente 4) mini-viz 5) banda inferior fuente+fecha. NO: Gold Master, ICPI, Ti, node IDs.

## PROHIBICIONES ABSOLUTAS
```
NUNCA hardcodear datos sin snapshot/Gold Master · NUNCA agregar items sidebar Ejecutivo
NUNCA modificar governance/* congelados · NUNCA modificar .github/workflows/* sin aprobación
NUNCA inventar artículos sin fuente · NUNCA lenguaje acusatorio (incumplió/violó/ilegal)
NUNCA agregar dominio nuevo · NUNCA exponer QTMP/ACK IDs en UI
```

## SKILL ROUTING
| Trabajo | Skill |
|---|---|
| Construir Layer 2 cajón | `/grill-with-docs` primero |
| Bug/regresión | `/diagnose` |
| Conversación→spec | `/to-prd` |
| Code review pre-merge | `/engineering:code-review` |
| TDD | `/tdd` |
| Contexto entre sesiones | `/handoff` |
| Auditar arquitectura | `/improve-codebase-architecture` |
| Atomizar COOTAD/LOTAIP | `/qlep` |
| Construir circuito | `/qtmp` |
| Excel canónico | `/anthropic-skills:xlsx` |
| Word/informe | `/anthropic-skills:docx` |
| Ingesta corpus masiva | `/qlep-corpus` |

## CONVENCIÓN COMMITS
```
[área]: descripción corta en español
Ej: d12: enriquecer Layer 2 · fix: corregir routing D10 · layer2: template dominio
```

## SNP no SENPLADES
La entidad de planificación es **SNP** (Secretaría Nacional de Planificación). SENPLADES ya no existe.

## DOCTRINA FINAL
> QUIRA informa — la autoridad pública decide.
> El mundo ve el espejo. La metodología es del laboratorio.
> Montecristi no es un piloto — es donde QUIRA aprende qué es un municipio.
> QUIRA crece en circuitos, no solo en chunks.
