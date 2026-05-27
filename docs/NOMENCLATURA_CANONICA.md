# QUIRA Intelligence — Nomenclatura Canónica
**FREEZE TOTAL — Aprobado 2026-05-27 · Dylus Lab**

> Un cambio de nombre en este documento rompe decenas de archivos.
> Cualquier modificación requiere revisión formal del equipo Dylus Lab.
> No negociable. No experimental. No provisional.

---

## 1. Roles del Sistema

### Tabla maestra

| Key interno | Display UI | Emoji | Audiencia | Plataforma principal |
|---|---|---|---|---|
| `ejecutivo` | Ejecutivo | 🏛 | Alcalde, concejales (COOTAD: función ejecutiva) | GOV (vista ejecutiva) |
| `tecnico` | Técnico | 📐 | Técnico de planificación, analista municipal | GOV (vista técnica) |
| `operador` | Operador | ⚙️ | Equipo Dylus Lab — operación del sistema | OPS |
| `administrador` | Administrador | 🔑 | Equipo Dylus Lab — acceso total | OPS + GOV (verificación) |

### Reglas de roles

- `ejecutivo` y `tecnico` son **usuarios del producto GOV** (municipio).
- `operador` y `administrador` son **operadores del sistema OPS** (Dylus Lab).
- `administrador` puede acceder a GOV para verificación cruzada, pero **entra por OPS**.
- Los keys internos son en minúsculas, sin tildes, sin espacios.
- Los nombres de display tienen mayúscula inicial solamente.
- Los emojis son decorativos — solo en UI, nunca en lógica.

### Secrets en Streamlit Cloud

```toml
[auth]
ejecutivo_hash     = "<PBKDF2-SHA256 del password>"
tecnico_hash       = "<PBKDF2-SHA256 del password>"
operador_hash      = "<PBKDF2-SHA256 del password>"
administrador_hash = "<PBKDF2-SHA256 del password>"
```

### Helpers de sesión (utils/session.py)

| Función | True cuando el rol es... |
|---|---|
| `is_ejecutivo()` | `ejecutivo` |
| `is_tecnico()` | `tecnico`, `operador`, `administrador` |
| `is_operador()` | `operador`, `administrador` |
| `is_admin()` | `administrador` |
| `is_gov_user()` | `ejecutivo`, `tecnico`, `administrador` |
| `is_ops_user()` | `operador`, `administrador` |

---

## 2. Ambientes del Sistema

### Tabla maestra

| Key interno | Label sidebar | Nombre público | Audiencia | Estado |
|---|---|---|---|---|
| `gov` | GOV | QUIRA Institucional | Ejecutivo, Técnico (+ Admin para verificación) | ✅ Activo |
| `civic` | Civic | QUIRA Ciudadano | Ciudadanía, academia, ONGs | 🔄 Fase 3 |
| `impact` | Impact | QUIRA Cooperación | Cooperación internacional, investigadores | ⏳ Placeholder |
| `ops` | OPS | Operaciones | Equipo Dylus Lab | ✅ Activo |

### Reglas de ambientes

- Los keys internos son en minúsculas: `gov`, `civic`, `impact`, `ops`.
- Los labels del sidebar son los códigos cortos: `GOV`, `Civic`, `Impact`, `OPS`.
- Los nombres públicos (landing page) son los nombres de producto.
- **Nunca** usar un nombre público en lógica de código — solo el key interno.
- **OPS no es una plataforma pública**. No aparece como tarjeta en la landing.

---

## 3. Módulos GOV (navegación interna)

### Sección Ejecutiva — visible para todos los roles GOV

| Key módulo | Label sidebar | Módulo |
|---|---|---|
| `inicio` | 🏠 Inicio | `p0_inicio.py` |
| `situacion` | 📊 Situación Institucional | `m1_situacion.py` |
| `alertas` | 🚨 Alertas y Riesgos SAT | `m2_alertas.py` |
| `municipal` | 🏛 Gestión Municipal | `m3_municipal.py` |
| `ods` | 🌐 ODS y Metas PDOT | `p11_ods.py` |
| `confianza` | 🤝 Confianza Ciudadana | `p16_confianza.py` |
| `rdc` | 📋 Rendición de Cuentas | `p17_rdc.py` |
| `cooperacion` | 🌍 Cooperación Internacional | `p18_cooperacion.py` |
| `genero` | 💜 Género y Ambiente | `p19_genero.py` |

### Sección Técnica — solo Técnico, Operador, Administrador

| Key módulo | Label sidebar | Módulo |
|---|---|---|
| `analisis` | 📈 Análisis Estratégico | `m4_analisis.py` |
| `geotwin` | 🗺 GeoTwin Territorio | `p4_geotwin.py` |
| `congruencias` | 🔗 Congruencias PDOT | `p3_congruencias.py` |
| `simulador` | 🎮 Simulador de Escenarios | `p13_simulador.py` |
| `control` | ⚙ Centro de Control | `m5_control.py` |

### Regla de módulos

> **env_gov.py es un router, nunca un dashboard.**
> El contenido vive en m1-m5 y p0-p19. env_gov.py solo decide qué mostrar.
> Módulos nuevos = archivo nuevo + una línea en env_gov.py.
> Nunca agregar contenido directamente en env_gov.py.

---

## 4. Política de Colores (sistema semáforo)

| Color | Hex | Uso | Contexto |
|---|---|---|---|
| Verde | `#22C55E` | Estable / OK / Bien | ICPI ≥70%, D3 ≥70%, riesgo BAJO |
| Lima | `#84CC16` | Saludable | ICPI 70-80% |
| Amarillo | `#F59E0B` | Atención / En Construcción | ICPI 50-70%, D3 50-70%, riesgo MEDIO |
| Naranja | `#F97316` | Alerta | riesgo ALTO, SAT preventiva |
| Rojo | `#EF4444` | Crítico | ICPI <50%, SAT crítica, riesgo CRÍTICO |
| Rojo oscuro | `#DC2626` | Legal / Breach | SAT con base legal activada |
| Azul QUIRA | `#00D4FF` | Contextual / Info / Acento | Datos informativos, acento de marca |
| Violeta | `#7C5CFC` | Secundario | Cooperación, elementos secundarios |
| Gris | `#64748B` | Sin datos / Deshabilitado | Cuando no hay información |

**Regla:** Un indicador solo tiene UN color según su estado. No mezclar colores en el mismo badge.

---

## 5. Prohibiciones Formales

### Nomenclatura
- ❌ `Directivo` / `directivo` — RENOMBRADO A `ejecutivo`. Nunca volver a usar.
- ❌ `Viewer`, `Analyst`, `Operator`, `Admin` — ELIMINADOS. Nunca volver a usar.
- ❌ `Alcalde`, `Concejal`, `Técnico Municipal` — modelo SaaS v1, descartado.
- ❌ `is_directivo()` — RENOMBRADO A `is_ejecutivo()`. Nunca volver a usar.
- ❌ `Sentinel` como nombre de módulo de IA — usar `QUIRA IA`.
- ❌ `H73_OUTPUT_API` en código nuevo — usar `G6.1_OUTPUT_API` o la capa canónica.
- ❌ Mezclar key interno con display en lógica de negocio.

### Arquitectura
- ❌ Sección PLATAFORMA en el sidebar — ELIMINADA. No reintroducir.
- ❌ Agregar un 5to ambiente al router principal.
- ❌ Agregar contenido directamente en `env_gov.py` (debe ser router puro).
- ❌ `env_civic.py` leyendo datos del núcleo soberano (Gold Master, snapshots operacionales).
- ❌ `app.py` superando 500 líneas — refactorizar si crece.

### Semáforo
- ❌ Usar colores fuera de la paleta de 9 colores definida arriba.
- ❌ Usar colores distintos para el mismo tipo de alerta en distintos módulos.

---

## 6. Nodos de Configuración

| Archivo | Responsabilidad |
|---|---|
| `config.py` | Parámetros del GAD: nombre, período, alcalde, corte |
| `models/auth.py` | Keys, hashes, validación, roles meta |
| `utils/session.py` | Helpers de sesión y rol |
| `app.py` → `ENVIRONMENTS` | Catálogo de ambientes y acceso por rol |
| `env_gov.py` → `_GOV_MODULES` | Módulos GOV y visibilidad por rol |

---

*Dylus Lab © 2026 — QUIRA Intelligence · Este documento es ley.*
