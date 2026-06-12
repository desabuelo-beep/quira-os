# PROPUESTA — PROGRAMA DE REFACTORIZACIÓN L2 (dashboards internos)
**QUIRA OS · Sprint C · 2026-06-12 · para consenso de mesa (Javo + Colega + Director)**
*Estado: PROPUESTA — nada se ejecuta sin aprobación. Principio de Javo:
"uno por uno, con base y fundamento, no una cuestión al garete".*

---

## El diagnóstico con números (auditoría 2026-06-12)

Con los cajones L1 por fin navegando, lo que se abre detrás son las pantallas
de la era Terra, sin reestructurar y con **nomenclatura canónica prohibida
visible** (Regla de Oro 2 — Bloomberg Firewall) en producción.

Auditoría automática de términos prohibidos en strings renderizables
(`scripts/dev/audit_bloomberg_l2.py`):

| Severidad | Página | Violaciones | Nota |
|---|---|---|---|
| 🔴 | p_vista_ejecutiva | 32 | La pantalla del alcalde — la peor |
| 🔴 | p07_transparencia | 31 | Mayoría en metadatos internos de dicts — confirmar qué se renderiza |
| 🟠 | m2_alertas | 17 | ICPI×10 + SAT×7 visibles |
| 🟠 | p0_inicio | 11 | Posiblemente huérfana tras el v2 — verificar y archivar |
| 🟡 | 11 páginas más | 1-7 c/u | p17/p18/p07 ya parcialmente modernizadas este sprint |
| 🟢 | m1, m3, m4 | 0 | ⚠️ Son WRAPPERS de ~40-50 líneas — sus hijos internos se auditan al refactorizar cada cajón |

**Dos matices honestos:** (a) la cifra es cota superior — el conteo incluye
strings internas de dicts que podrían no renderizarse; el refactor por página
confirma. (b) Los wrappers m1/m3/m4 delegan en sub-páginas Terra que esta
pasada no ve — el inventario real crece al abrir cada cajón.

---

## El método propuesto: "Un dashboard a la vez"

### PASO 0 — Consenso de lenguaje (sin código · 1 sesión de mesa)
**Tabla de Equivalencias Canónica**: cada término interno → su nombre público
de gobernanza, decidido UNA vez y aplicado en todos los refactors.
Ejemplos a consensuar (el Centro de Mando v2 ya sentó precedente):

| Interno (prohibido en UI) | Público (propuesta) |
|---|---|
| ICPI | Cumplimiento Institucional |
| SAT | Alertas Institucionales / Sistema de Alerta Temprana |
| TGI | Gestión Territorial (a definir en mesa) |
| Gold Master / H73 | Motor de indicadores institucional (nunca visible) |
| Dom07 / C01 / CE_xxx | — jamás visibles; solo lenguaje del dominio |

### Plantilla canónica por dashboard (hereda Fichas v2 + Cajones v2)
1. **CONCEPTO arriba** — qué es este dominio, en 1-2 líneas humanas
2. **Lenguaje 100 % gobernanza** — cero nomenclatura interna (tabla del Paso 0)
3. **Número duro + interpretación** — el patrón Indicador | Dato | Lectura
4. **Datos VIVOS** — Gold Master vía connector · Supabase · pdot_indicadores; cero hardcode Terra
5. **Decisión/acción sugerida** cuando exista (curada, jamás generada)
6. **Límites declarados** — lo que el sistema aún no sabe, dicho en pantalla

### Gate de cierre por dashboard (sin esto, no se declara terminado)
- [ ] Auditoría Bloomberg de la página = 0 visibles
- [ ] Verificación VISUAL con harness local + Playwright (regla 2026-06-11)
- [ ] Verificado EN DEPLOY (build stamp + mirada de Javo)
- [ ] Datos vivos confirmados (sin residuos Terra)

### Cadencia por dashboard (1 por sesión enfocada)
```
1. Director: MAQUETA EN TEXTO (qué dirá la pantalla, sección por sección)
2. Mesa: Javo + Colega ajustan y aprueban la maqueta
3. Director: ejecución + gate completo
4. Javo: mirada final en deploy → cerrado → siguiente
```

---

## Orden propuesto (criterio: lo que el Ejecutivo toca primero × severidad × valor demo)

| # | Cajón → página(s) | Por qué primero |
|---|---|---|
| 1 | **06 Salud Institucional** → m1 + p_vista_ejecutiva | La pantalla del alcalde · la más violada (32) · primera impresión del sistema |
| 2 | **10 Territorio** → p10 | Conecta con GeoTwin/F1 ya validado · demo natural |
| 3 | **09 Rendición de Cuentas** → p17 | Ya tiene el circuito en vivo · casi limpia (2) — cierre rápido |
| 4 | **02 Cooperación** → p18 | Ya es lector Supabase · sumar taxonomía SIMULADA/VALIDADA visible |
| 5+ | resto por ranking de auditoría | m2_alertas (17) · p0_inicio (¿archivar?) · … |

**En paralelo, sin código:** sesión de contenido de los CAJONES L1 — iterar
los 12 conceptos/ganchos en texto con Javo hasta que digan lo que él quiere.

**QUIRA IA (Pregúntale a QUIRA):** hoy abre el Sentinel-Terra. Su reemplazo
(conversacional, consciente de rol, alimentado por motor narrativo + 2,004
indicadores) entra al programa como pieza propia — **dependencia: créditos
API**. Hasta entonces, propuesta mínima: pantalla puente digna ("QUIRA IA en
preparación" + las explicaciones del motor narrativo como respuestas estáticas).

---

## Lo que pido a la mesa

1. ¿Se aprueba el método (Paso 0 + plantilla + gate + cadencia)?
2. ¿Se aprueba el orden (Salud Institucional primero)?
3. Tabla de equivalencias: ¿la armamos en la próxima sesión de mesa?

*Propuesta del Director Técnico · QUIRA OS · Dylus Lab © 2026*
