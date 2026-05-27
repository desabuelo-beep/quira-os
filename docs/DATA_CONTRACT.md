# Data Contract — QUIRA Intelligence
## Sprint D.2 · Estabilización Operacional

> **Propósito**: Define formalmente qué produce el Gold Master, qué consume la vista,
> qué calcula TOP en runtime, y qué vive en cada capa del sistema.  
> Antes de este documento, el flujo de datos era implícito. Ahora es explícito.

**Versión**: 1.0  
**Fecha**: 2026-05-27  
**Autoridad**: Dylus Lab  
**Fuente canónica de datos**: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx`

---

## 1. Capas del Sistema (flujo de datos)

```
Excel Gold Master (OFFLINE — nunca en repo)
        │
        ▼  pipeline (scripts/)
  data/gm_snapshot.json  ← puente Streamlit ← único artefacto Git de datos
        │
        ▼  utils/cache_quira.py → cargar_gm_snapshot()
  dict Python en memoria
        │
        ▼  quira_pages/*.py (render)
  HTML generado → Streamlit st.markdown()
        │
        ▼  Supabase (escritura)
  historical snapshots ← solo el pipeline escribe, NUNCA la vista
```

**Regla cardinal**: el pipeline NUNCA escribe en el Gold Master. La vista NUNCA escribe en Supabase. El Excel NUNCA va al repo.

---

## 2. Gold Master → gm_snapshot.json

### 2.1 Keys de primer nivel (contrato de salida del pipeline)

| Key | Tipo | Fuente Excel | Descripción |
|---|---|---|---|
| `tgi` | `dict` | H73_TGI_SCORE | Índice de Gobernanza Territorial Integral |
| `icpi` | `dict` | H74_ICPI | Índice de Coherencia del Plan Institucional |
| `sat_gm` | `dict` | SAT_ACTIVAS | Alertas del Sistema de Alerta Temprana |
| `financiero` | `dict` | H90_PRESUPUESTO | Ejecución presupuestaria consolidada |
| `psg` | `dict` | PSG_FIDELIDAD | Plan de Seguimiento y Gestión |
| `gad` | `dict` | METADATOS_GAD | Promesas CNE, metas PDOT |
| `territorial` | `dict` | PDOT_PARROQUIAS | Datos por parroquia |

### 2.2 Schema `tgi`

```python
{
  "score": float,            # 0–100 · TGI Global
  "clasificacion": str,      # "Transición con Riesgos" | "Ruptura" | ...
  "color_hex": str,          # "#FFB800" | "#EF4444" | "#22C55E"
  "d1": {"valor": float},    # Legalidad y normativa
  "d2": {"valor": float},    # Planificación y PDOT
  "d3": {"valor": float},    # Ejecución de inversión
  "d4": {"valor": float},    # Equidad territorial
  "d5": {"valor": float},    # Capacidad institucional
  "irs": {
    "valor": float,          # Índice de Regresividad del Gasto (0–100)
    "clasificacion": str,    # "Muy Regresivo" | "Regresivo" | "Neutro" | ...
  },
  "ied_global": {"valor": float},      # Eficiencia Directiva
  "brecha_rural_usd": float,           # Brecha de inversión rural ($)
}
```

### 2.3 Schema `icpi`

```python
{
  "global_pct": float,       # 0–100 · velocidad de ejecución
  "clasificacion": str,      # "Ruptura Sistémica" | "En Riesgo" | ...
}
```

### 2.4 Schema `sat_gm`

```python
{
  "clasif_riesgo": str,      # "BAJO" | "MEDIO" | "ALTO" | "CRÍTICO"
  "activas_count": int,      # N alertas activas
  "sat_activas_detalle": {
    "SAT-III": {"peso": float, "descripcion": str},
    "SAT-IV":  {"peso": float, "descripcion": str},
    "SAT-V":   {"peso": float, "descripcion": str},
    # ... solo SATs activas
  }
}
```

### 2.5 Schema `financiero`

```python
{
  "ti_2026_raw_pct": float,                         # Ti inversión GAD (G71-78)
  "presupuesto_codificado_grupos78_2026": float,    # $ codificado GAD inversión
  "devengado_q1_2026": float,                       # $ devengado GAD Q1
  "fondos_bloqueados_est": float,                   # $ fondos no activados
  "fondos_bloqueados_detalle": str,                 # descripción textual
  "h90_consolidado": {
    "gad_ti_q1_pct": float,                         # Ti GAD todos grupos H90
    "patronato_codificado": float,
    "patronato_devengado_q1": float,
    "patronato_ti_q1_pct": float,
    "ep_aseo_codificado": float,
    "ep_aseo_devengado_q1": float,
    "ep_aseo_ti_q1_pct": float,
    "bomberos_codificado": float,
    "bomberos_devengado_q1": float,
    "bomberos_ti_q1_pct": float,
    "holding_ti_q1_pct": float,
    "holding_total_codificado": float,
    "holding_total_devengado_q1": float,
  }
}
```

### 2.6 Schema `territorial`

```python
{
  "parroquias": [
    {
      "nombre": str,
      "tipo": str,              # "Urbana" | "Rural"
      "nbi_pct": float,         # Necesidades Básicas Insatisfechas %
      "iet_local_pct": float,   # Índice de Equidad Territorial %
      "inv_percapita_q1": float, # Inversión per cápita $
      "alerta": str | None,     # descripción si hay alerta específica
    },
    ...
  ],
  "nbi_rural_promedio": float,
}
```

---

## 3. Runtime — computado en cada render

Estos valores NO viven en el snapshot. Se calculan en Python en cada llamada a `render()`.

### 3.1 Ecosistema Municipal — `_compute_ecosistema(data)`

**Input**: `data` dict (del snapshot)  
**Output**: `list[dict]` — 4 elementos, índice 0 = GAD siempre

```python
# Por cada entidad:
{
  # Desde utils/top.py → top_entidad():
  "entidad": str,           # nombre canónico
  "ti_pct": float,          # Ti usado para el cálculo
  "top": float,             # TOP = Ti_acum / W_Q
  "top_display": float | None,  # None si sobre_ritmo == True
  "categoria": str,         # "ruptura" | "alerta" | "sostenible"
  "color": str,             # hex según categoría
  "icono": str,             # emoji según categoría
  "label": str,             # texto label del badge
  "diagnostico": str,       # frase diagnóstica
  "sobre_ritmo": bool,      # True si TOP > 100
  # Agregados en _compute_ecosistema():
  "nombre": str,            # alias de "entidad" para compatibilidad HTML
  "emoji": str,             # emoji institucional (🏛 💚 ♻ 🚒)
  "nota_ti": str,           # descripción del tipo de Ti usado
  "codificado": float,      # $ codificado
  "devengado": float,       # $ devengado Q1
}
```

**Orden fijo** (nunca reordenar):
```
eco[0] = GAD Municipal       → Ti inversión G71-78 (D3 estricto)
eco[1] = Patronato Municipal  → Ti H90 todos grupos
eco[2] = EP Aseo              → Ti H90 todos grupos
eco[3] = Cuerpo de Bomberos   → Ti H90 todos grupos
```

### 3.2 Narrativa IA — `_compose_quira_ia(data, eco)`

**Input**: `data` dict + `eco` list  
**Output**: `str` — texto ejecutivo, español institucional, ~3–5 oraciones

**Estructura interna**:
1. Brief GAD (de `narrativa_ia(eco[0])`)
2. Sobre-ritmo de otras entidades (si existen)
3. Entidades con atención requerida (si existen)
4. Palanca BDE (siempre presente)

### 3.3 Briefing ejecutivo — `_briefing_sentence(narrative)`

**Input**: `narrative` str  
**Output**: `str` — máximo 280 chars, 2 primeras oraciones de `narrative`

### 3.4 Timestamp render — `ts_render`

```python
from datetime import datetime
ts_render = datetime.now().strftime("%H:%M · %d/%m")
```

Calculado en `render()` una vez por renderización. No cacheado.

---

## 4. utils/top.py — Contrato de API

### 4.1 `top_entidad(ti_pct, corte, nombre)`

**Input**:
- `ti_pct: float` — tasa de inversión acumulada al corte (0–100)
- `corte: str` — "Q1-2026" | "Q2-2026" | etc.
- `nombre: str` — nombre de la entidad

**Output**: `dict` con keys: `entidad`, `ti_pct`, `top`, `top_display`, `categoria`, `color`, `icono`, `label`, `diagnostico`, `sobre_ritmo`

**W_Q calibrado eSIGEF**:
```python
W_Q = {"Q1": 0.13, "Q2": 0.35, "Q3": 0.60, "Q4": 1.00}
```

**TOP = `ti_pct / W_Q[trimestre]`**

**Gold assertions Q1-2026** (verificadas en 56 tests):
```
GAD Municipal:       Ti=1.05%  → TOP=8.1%   → RUPTURA
Patronato Municipal: Ti=19.56% → TOP=150.5% → SOBRE RITMO
EP Aseo:             Ti=18.17% → TOP=139.8% → SOBRE RITMO
Cuerpo de Bomberos:  Ti=19.43% → TOP=149.5% → SOBRE RITMO
```

### 4.2 `narrativa_ia(td)`

**Input**: `td: dict` — output de `top_entidad()`  
**Output**: `str` — frase ejecutiva en español institucional

---

## 5. Fallback — `_FALLBACK`

El fallback es el snapshot de Q1-2026 hardcodeado. Se usa cuando:
- `cargar_gm_snapshot()` falla
- El archivo `data/gm_snapshot.json` no existe
- Los datos del snapshot no tienen la key `tgi`

**El fallback NUNCA se usa en producción**. Si se activa, hay un problema de pipeline.

El fallback vive en `quira_pages/p_vista_ejecutiva.py` → `_FALLBACK` dict.  
Los valores del fallback son idénticos a las gold assertions Q1-2026.

---

## 6. Supabase — Contrato de escritura

| Tabla | Escritor | Frecuencia |
|---|---|---|
| `monthly_snapshots` | `sentinel/` pipeline | Mensual · corte de mes |
| `monthly_kpis` | `sentinel/` pipeline | Mensual |
| `alerts_history` | `sentinel/` pipeline | Por evento SAT |
| `budget_execution_lines` | `sentinel/` pipeline | Mensual · por línea presupuestal |
| `document_uploads` | Vista ciudadano (futuro) | Por subida |
| `municipality_snapshots` | Pipeline multi-GAD (futuro) | Por GAD por mes |

**Lectura**: la Vista Ejecutiva NO lee de Supabase directamente. Lee de `gm_snapshot.json`.

**RLS**: habilitado en todas las tablas. Las conexiones psycopg2 bypass RLS por ser conexiones directas PostgreSQL (rol superuser). La anon key REST no tiene acceso.

---

## 7. config.py — Constantes de runtime

```python
GAD_NOMBRE = str    # "GAD Municipal del Cantón Montecristi"
ALCALDE    = str    # "Nombre Apellido del Alcalde"
CORTE      = str    # "Q1-2026" — trimestre activo
```

Estas 3 constantes son el único punto de parametrización por GAD en el sistema actual. En multi-GAD, se convertirán en variables de sesión o parámetros de URL.

---

## 8. Invariantes del sistema

Estas propiedades nunca deben romperse:

1. `eco[0]` es siempre el GAD Municipal
2. `eco` siempre tiene exactamente 4 elementos
3. `gad_top = eco[0]` es la señal crítica Z1
4. Si `sobre_ritmo == True` → `top_display == None`
5. Si `top_display == None` → UI muestra "Sobre ritmo esperado"
6. El briefing se extrae de `_compose_quira_ia`, no se genera por separado
7. `ts_render` se computa fresh en cada `render()` — nunca se cachea
8. `_load()` tiene TTL=300 — los datos se refrescan máximo cada 5 minutos

---

## 9. Lo que NO existe todavía (deuda explícita)

| Componente | Estado | Sprint |
|---|---|---|
| Schema JSON validado del snapshot | Ausente — solo fallback como referencia | D.2+ |
| Tests de integración pipeline→snapshot | Ausente | Futuro |
| Lectura Supabase desde Vista Ejecutiva | Ausente por diseño — usar snapshot | D.4+ |
| Manejo de multi-GAD (CORTE como variable) | Ausente | Post Next.js |
| Versionado del gm_snapshot.json | Ausente — solo un archivo | Futuro |
| Schema Pydantic de `eco` | Ausente | D.4 |

---

*Dylus Lab · QUIRA Intelligence · Sprint D.2 Data Contract v1.0 · 2026-05-27*
