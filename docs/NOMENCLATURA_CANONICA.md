# QUIRA Intelligence — Nomenclatura Canónica
**FREEZE TOTAL — Última revisión 2026-05-27 · Dylus Lab**

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

---

## 7. Ecosistema Municipal

> **Corrección arquitectónica v2 — 2026-05-27**
> QUIRA no modela "el municipio" = GAD. QUIRA modela el **ecosistema institucional municipal**.
> El GAD es el núcleo dominante. Las entidades son la capa periférica de gobernanza del alcalde.

### Término canónico

| Término | Usar | Razón |
|---|---|---|
| `Ecosistema Municipal` | ✅ SIEMPRE | Comunica sistema vivo. El alcalde piensa en su sistema, no en su holding. |
| `Holding Municipal` | ⚠ Solo internamente | Correcto técnicamente, frío cognitivamente. Nunca en UI. |
| `Adscritas` | ❌ Nunca en UI | Incompleto — no incluye EPs ni Bomberos. |
| `Dependencias` | ❌ Nunca | Errado institucionalmente. |
| `Entidades` | ⚠ Neutral | Aceptable en contexto técnico, no en interfaz. |

### Catálogo canónico de entidades — Montecristi

| Key interno | Nombre display | Tipo | Prioridad visual | Estado datos |
|---|---|---|---|---|
| `gad` | GAD Municipal | Núcleo / Matriz | 🔴 Dominante | ✅ Gold Master completo |
| `patronato` | Patronato Municipal | Adscrita social | 🟡 Secundaria | ✅ 12 meses 2025 |
| `ep_aseo` | EP Aseo Municipal | Empresa pública | 🟡 Secundaria | ✅ 12 meses 2025 |
| `bomberos` | Cuerpo de Bomberos | Adscrita operacional | 🟡 Secundaria | ✅ 12 meses 2025 |

**Reglas de keys internos:**
- Minúsculas, sin tildes, sin espacios, sin guiones dobles
- `gad` = siempre el GAD matriz (no el municipio en general)
- Entidades futuras siguen el patrón: `ep_agua`, `ep_movilidad`, `fundacion_x`

### Jerarquía de visibilidad en Vista Ejecutiva v2

```
Header    → GAD (nombre) · TGI · SAT activas · Alcalde
Zona 1    → Pulso Institucional GAD (TGI · D1-D5 · ICPI)
Zona 2    → Lo Urgente — SAT sistémicas GAD
Zona 3    → Compromisos GAD (RDC · PDOT · IFE)
Zona 4    → Territorio (parroquias · IRS · brecha)
Zona 5    → Ecosistema Municipal (Patronato · EP Aseo · Bomberos)
Zona 6    → Oportunidades + QUIRA IA
```

### Indicadores canónicos mínimos por entidad del ecosistema

| Indicador | Obligatorio | Descripción |
|---|---|---|
| Estado semafórico | ✅ | 🟢 Estable / 🟡 Atención / 🔴 Riesgo |
| Ti (ejecución) | ✅ | % devengado sobre codificado |
| Señal operativa | ✅ | El dato más relevante del tipo de entidad |
| Acción recomendada | Si riesgo | Qué debe hacer el alcalde |

**Señal operativa por tipo:**

| Tipo entidad | Señal operativa canónica |
|---|---|
| Adscrita social (Patronato) | Cobertura de beneficiarios · calidad evidencia IMN |
| Empresa pública (EP Aseo) | Cobertura territorial de servicio |
| Adscrita operacional (Bomberos) | Capacidad operativa · tiempos de respuesta |

### Jerarquía SAT en el ecosistema

| Nivel SAT | Nombre | Origen | Vista |
|---|---|---|---|
| SAT sistémica (I-VIII+) | SAT del municipio | GAD | Zona 2 — Lo Urgente · afecta ICPI |
| SAT operativa sectorial | SAT de entidad | Patronato / EP / Bomberos | Zona 5 — Ecosistema · no contamina ICPI |

**Regla:** Las SAT sistémicas del GAD NUNCA se mezclan visualmente con las señales del ecosistema.
Son cualitativamente distintas. Una SAT sistémica activa implica riesgo legal municipal.
Una señal de ecosistema implica deterioro operativo periférico que el alcalde debe monitorear.

### Prohibiciones del Ecosistema

- ❌ Mostrar el GAD y las entidades del ecosistema como si fueran iguales en peso visual
- ❌ Llamar "Holding" a la Zona 5 en la UI
- ❌ Inventar datos de entidades — si no hay dato, mostrar "Sin datos Q1"
- ❌ Activar SAT sistémicas desde datos de entidades adscritas (solo el GAD activa SAT sistémicas)
- ❌ Mostrar una zona Ecosistema sin al menos estado semafórico y Ti de cada entidad

---

## 7.2 TOP — Trayectoria Operativa Proyectada

> **Principio doctrinal central (QUIRA_DOCTRINE_v1.3):**
> QUIRA no mide ejecución acumulada. QUIRA vectoriza la trayectoria institucional.
> El semáforo representa hacia dónde va la institución — no dónde está.

### Nombre canónico

**TOP — Trayectoria Operativa Proyectada**

| Término | Usar | Razón |
|---|---|---|
| `TOP` | ✅ SIEMPRE | Nombre oficial. Vector + trayectoria + proyección. |
| `RIP` | ❌ NUNCA | Semántica fúnebre en español. |
| `VIP` | ❌ NUNCA | Sonido comercial superficial, pierde rigor público. |
| "ejecución acumulada" | ❌ No como semáforo | Describe el pasado, no la trayectoria. |

### Fórmula canónica

```
TOP = Ti_acumulado / W_Q
```

Donde `W_Q` es la fracción histórica esperada del presupuesto anual devengado al cierre de ese trimestre, según la curva real del eSIGEF ecuatoriano.

### Constantes W_Q (curva eSIGEF — GADs Ecuador tamaño intermedio)

| Quarter | W_Q | Comportamiento institucional |
|---|---|---|
| Q1 | 0.13 | Letargo administrativo — liquidación año anterior, reformas, SERCOP |
| Q2 | 0.35 | Contratos activados — primera ola de obra pública |
| Q3 | 0.60 | Avance de obras — devengados parciales acumulados |
| Q4 | 1.00 | Explosión final — ~40% del presupuesto en los últimos 45 días |

**Calibración:** Valores actuales son la curva nacional. Se calibrarán con serie histórica real de Montecristi a partir del año 2 del Gold Master.

### Umbrales canónicos del semáforo TOP

| TOP proyectado | Color | Hex | Diagnóstico doctrinal |
|---|---|---|---|
| ≥ 75% | 🟢 Sostenible | `#22C55E` | Gobernanza por Mandato — cumplimiento PDOT garantizado |
| ≥ 55% | 🟡 Atención | `#F59E0B` | Desaceleración leve — monitorear Q siguiente |
| ≥ 35% | 🟠 Alerta Institucional | `#F97316` | Intervención requerida — reforma presupuestaria |
| < 35% | 🔴 Ruptura de Trayectoria | `#EF4444` | Riesgo Contraloría — acción ejecutiva urgente |

### Regla de display — cap de TOP

| TOP matemático | Mostrar en UI | Razón |
|---|---|---|
| > 100% | Label narrativo: "Sobre ritmo esperado" | Numéricamente exacto pero políticamente confuso |
| ≤ 100% | Porcentaje: "78%" | Cognitivamente directo |

**NUNCA mostrar "150%" en UI.** El valor matemático se preserva internamente para QUIRA IA y cálculos.

### Scope de TOP — indicadores tiempo-dependientes

TOP aplica a TODO indicador que tenga ciclo anual y corte temporal:

| Indicador | Aplicación TOP | Estado |
|---|---|---|
| Ti presupuestario (GAD + Ecosistema) | `top_entidad()` en `utils/top.py` | ✅ Sprint B |
| Cobertura de servicios (EP Aseo, etc.) | TOP de avance vs. meta anual | 📅 Sprint C |
| Velocidad de respuesta SAT | TOP del tiempo de resolución | 📅 Sprint C |
| IFE — fidelidad electoral | TOP de promesas con proceso contractual | 📅 Sprint D |
| IMN Score por dirección | TOP de calidad de reporte acumulada | 📅 Sprint C |

### Implementación

```
utils/top.py
├── WQ                            constantes estacionales
├── calcular_top(ti, quarter)     función pura determinista
├── calcular_top_desde_corte()    conveniencia con corte canónico
├── clasificar_top(top)           ficha institucional completa para UI + IA
├── top_entidad(ti, corte, nombre) conveniencia para Ecosistema Municipal
└── narrativa_ia(entidad_dict)    brief institucional ejecutivo para QUIRA IA
```

### Prohibiciones del TOP

- ❌ Usar semáforo de valor absoluto acumulado (19% ≠ rojo en Q1)
- ❌ Proyectar linealmente sin W_Q estacional
- ❌ Mostrar valores TOP > 100% como números en UI
- ❌ Activar SAT sistémica solo por TOP bajo de una entidad del ecosistema
- ❌ Calcular TOP sin dato de Ti verificado en Gold Master

| Archivo | Responsabilidad |
|---|---|
| `config.py` | Parámetros del GAD: nombre, período, alcalde, corte |
| `models/auth.py` | Keys, hashes, validación, roles meta |
| `utils/session.py` | Helpers de sesión y rol |
| `app.py` → `ENVIRONMENTS` | Catálogo de ambientes y acceso por rol |
| `env_gov.py` → `_GOV_MODULES` | Módulos GOV y visibilidad por rol |

---

*Dylus Lab © 2026 — QUIRA Intelligence · Este documento es ley.*
