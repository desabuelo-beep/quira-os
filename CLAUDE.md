# QUIRA OS — Guía Canónica para Claude
## Dylus Lab · Sistema Operativo de Coherencia Institucional

> Leer este archivo PRIMERO antes de tocar cualquier código.
> Toda construcción sigue las reglas aquí. Sin excepción.

---

## PROTOCOLO DE ARRANQUE DE SESIÓN

Antes de cualquier trabajo, leer en orden:
1. Este archivo (`CLAUDE.md`) — reglas de construcción
2. `governance/QUIRA_STATE.md` — qué está abierto, cerrado, en qué sprint
3. Verificar que el módulo a tocar existe en env_gov.py

---

## ARQUITECTURA CANÓNICA

### Stack
```
Streamlit (UI) + Python (backend) + Claude Haiku (AI) + Neo4j (grafo causal) + Supabase (longitudinal)
```

### 3 Capas UI — NUNCA mezclar responsabilidades

```
Layer 1 → p_command_center.py     → Centro de Mando: 12 cajones HTML canvas
           Full-screen, sin sidebar, navegación via postMessage bridge
           COMPLETO — no modificar estructura

Layer 2 → p11-p19, m1-m5, p_*    → Dashboard por dominio (drill-in desde Layer 1)
           Una pantalla por dominio. Narrativa causal. Fuentes públicas.
           CONSTRUIR cajón por cajón en Sprint 3

Layer 3 → p4_geotwin.py           → GeoTwin mapa territorial Folium
           Solo rol Técnico. Parroquias, NBI, cobertura.
```

### Router — env_gov.py

```
REGLA: env_gov.py ES UN ROUTER PURO. Zero contenido, zero lógica de negocio.
MÓDULOS: un archivo = un módulo.
AGREGAR: nueva feature → nuevo archivo + UNA LÍNEA en _GOV_MODULES
```

### 12 Dominios Canónicos — INMUTABLES

| ID | Nombre | Módulo destino | Archivo | Rol acceso |
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

**D12 tiene QTMP GAP_10PCT completo en Neo4j — es el único con cadena causal verificable.**

---

## FRONTERA DE LENGUAJE — BLOOMBERG MODEL

> El mundo ve el espejo. La metodología es del laboratorio.
> Esta regla es ley. Viola → bloquea el PR.

### PROHIBIDO en UI / API / reportes externos / comentarios visibles al usuario

```
Gold Master  →  cualquier nombre, versión o referencia al Excel canónico
H-series     →  H01, H07b, H12, H41, H73, H75, H85, H90 (nombres de hojas)
Índices      →  ICPI, TGI, IFE, IED, ITAM, IGP, IPE, PSG, ISP, IOC, IET
Fórmulas     →  Ti, Vi, Pi, Ri, Ei (en contexto de variables de fórmula)
QTMP IDs     →  SP_G10P_MCR, RES_G10P_01_MCR, IND_G10P_04_MCR
Protocolos   →  QTMP, ACK, QLEP, QNKC-002, QNKC
```

### CORRECTO en UI (lenguaje de gobernanza pública)

```python
# MAL  ❌
"Ti_Patronato_2025 = 50% (H07b fila 18)"
"Gold Master v5.5_TGI · Corte Q1-2026"
"ICPI: 17.4% — Ruptura Sistémica"

# BIEN ✓
"Ejecución presupuestaria del Patronato Municipal: 50% — 3 años consecutivos bajo umbral"
"Fuente: Sistema Integrado de Gestión Financiera · noviembre 2025"
"Cumplimiento institucional: 17.4% — 47.6 puntos bajo umbral · umbral 65%"
```

### Checklist antes de commit con código de UI

- [ ] ¿Contiene "Gold Master"? → ELIMINAR
- [ ] ¿Contiene H00-H73 como nombres? → ELIMINAR
- [ ] ¿Contiene ICPI, IOC, IGP, IET, IED, IFE, PSG, ISP, ITAM? → ELIMINAR
- [ ] ¿Contiene Ti=, Vi=, Pi= en texto visible? → ELIMINAR
- [ ] ¿El texto puede entenderse sin conocer la metodología? → APROBADO

---

## ROLES Y ACCESO

```
Ejecutivo    → Centro de Mando (sin sidebar, sin sección técnica)
Directivo    → Sidebar + 9 módulos ejecutivos
Técnico      → Sidebar + 14 módulos (incluye: geotwin, cadena, simulador, control)
Administrador → Todo
```

Verificar con `utils/session.py`:
```python
is_ejecutivo()    # solo el Ejecutivo (alcalde/concejales)
is_tecnico()      # Técnico, Operador, Administrador
is_admin()        # solo Administrador
get_rol()         # string: "Ejecutivo" / "Directivo" / "Técnico" / "Administrador"
```

---

## FUENTE DE VERDAD — JERARQUÍA

```
1. Constitución / COOTAD / COPLAFIP   → norma superior (no modificar)
2. SIGEF (cédulas presupuestarias)    → dato oficial (fuente pública)
3. Gold Master (interno — SECRETO)    → cálculo canónico
4. QTMP yaml (circuitos)              → observación QUIRA estructurada
5. gm_snapshot.json / Supabase        → derivados para runtime Streamlit
```

**Si hay conflicto: la fuente más alta gana. Siempre.**

---

## PATRONES DE CÓDIGO CANÓNICOS

### Cargar datos (siempre con cache)
```python
from utils.cache_quira import cargar_snapshot, cargar_gm_snapshot

snap, _meta = cargar_snapshot()   # 5 min cache
gm          = cargar_gm_snapshot()  # 15 min cache
```

### Semáforo de color
```python
from utils.css_tokens import C

color = C.sem(valor_pct)  # "#22C55E" / "#F97316" / "#EF4444"
```

### Verificar rol antes de mostrar contenido técnico
```python
from utils.session import is_tecnico, is_ejecutivo

if is_tecnico():
    st.write("Vista técnica")
else:
    st.write("Vista ejecutiva simplificada")
```

### Template Layer 2 (cada cajón debe seguir esta estructura)
```python
def render() -> None:
    # 1. KPI contextual del dominio (lenguaje gobernanza)
    # 2. Narrativa causal (sin nomenclatura interna)
    # 3. Indicadores con semáforo + fuente pública
    # 4. Mini-viz (chart o progress bar)
    # 5. Banda inferior: fuente pública + fecha corte
    # NO: Gold Master, ICPI, Ti, IDs de nodos
```

---

## PROHIBICIONES ABSOLUTAS

```
NUNCA hardcodear datos sin referencia a snapshot/Gold Master
NUNCA agregar nuevos items al sidebar del Ejecutivo
NUNCA modificar governance/* — documentos congelados
NUNCA modificar .github/workflows/* sin aprobación
NUNCA inventar artículos de ley sin fuente verificada
NUNCA usar lenguaje acusatorio ("incumplió", "violó", "ilegal")
NUNCA agregar un nuevo dominio (D01-D12 son inmutables)
NUNCA exponer QTMP IDs, ACK IDs o nombres de circuitos en la UI
```

---

## SKILL ROUTING — CUÁNDO USAR CADA SKILL

| Si el trabajo es... | Usar skill |
|---|---|
| Construir Layer 2 de un cajón | `/grill-with-docs` primero (valida contra docs canónicos) |
| Bug complejo o regresión | `/diagnose` |
| Convertir conversación en spec | `/to-prd` |
| Code review antes de merge | `/engineering:code-review` |
| Test-driven development | `/tdd` |
| Pasar contexto entre sesiones | `/handoff` |
| Auditar arquitectura actual | `/improve-codebase-architecture` |
| Atomizar normativa COOTAD/LOTAIP | `/qlep` |
| Construir circuito QTMP | `/qtmp` |
| Crear/editar Excel canónico | `/anthropic-skills:xlsx` |
| Crear Word/informe | `/anthropic-skills:docx` |

---

## CONVENCIÓN DE COMMITS

```
[área]: descripción corta en español

Ejemplos:
  d12: enriquecer Layer 2 con cadena causal en lenguaje gobernanza
  fix: corregir routing D10 para rol Ejecutivo en Centro de Mando
  layer2: crear template canónico de dominio dashboard
  chore: actualizar CLAUDE.md con reglas Sprint 3
  neo4j: cargar circuito agua_potable en QTMP
```

---

## DOCTRINA FINAL

> QUIRA informa — la autoridad pública decide.
> El mundo ve el espejo. La metodología es del laboratorio.
> Montecristi no es un piloto — es donde QUIRA aprende qué es un municipio.
> Cuando QUIRA pueda representar un municipio completo, los otros cantones son escala.

---

## Graphify (CodeGraph local)

Si existe `graphify-out/graph.json`:
- Para preguntas estructurales: `graphify query "<pregunta>"`
- Para relaciones entre archivos: `graphify path "<A>" "<B>"`
- Para explorar un concepto: `graphify explain "<concepto>"`
- Después de editar código: `graphify update .`

---

*CLAUDE.md v2.0 — Sprint 3 Panel Estratégico — Dylus Lab © 2026*
*Actualizar cuando cambie la arquitectura o se agreguen dominios nuevos*
