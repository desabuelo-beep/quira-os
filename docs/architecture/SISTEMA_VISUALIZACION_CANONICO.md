# 🎨 SISTEMA DE VISUALIZACIÓN CANÓNICO DE QUIRA
**Dylus Lab © 2026 · el lenguaje visual de QUIRA — nace con el mismo rigor que la Constitución Ontológica**

> El primer cajón no es una pantalla: es el **nacimiento del Sistema de Visualización Canónico** (asesor).
> Regla 9: esto **nace en el canon**, no en Python. Este documento es la doctrina; el código la implementa.

---

## 0 · El principio

No construimos gráficos: construimos **el lenguaje visual de QUIRA**, y ese lenguaje tiene una **gramática**.
Un mismo patrón sirve para todos los cajones (Verificabilidad · ICPI · PAC · POA · CPCCS · Cobertura ·
Presupuesto…). Por eso **no se diseña un cajón: se diseña el patrón de todos los cajones.**

**Cada cajón responde UNA sola pregunta** (asesor). Ej.: *¿Qué dijo? · ¿Cómo se verificó? · ¿Qué documento
lo respalda? · ¿Qué nivel de evidencia tiene? · ¿Qué regla aplicó?* Esa disciplina hace el dashboard claro.

---

## 1 · La arquitectura — separación `analytics` / `render` (decisión arquitectónica mayor)

```
Motor (Narrativo · ICPI · …)
        │  produce resultados crudos
        ▼
app/viz/analytics.py   →  transforma a OBJETO CANÓNICO
        │
        ▼
NarrativeEvidence (el Modelo de Datos Canónico)   ← TODOS los renderers consumen ESTO
        │
        ▼
app/viz/render/
        ├── matplotlib   (PDF · informes oficiales)   ⭐ control total, reproducible, Firewall
        ├── svg / web    (dashboard interactivo)
        └── plotly       (interactivo · futuro)
```

**El motor NUNCA sabe que existe Matplotlib.** Es la filosofía de QUIRA aplicada a los gráficos:
**canon → datos → presentación**, nunca al revés (Regla 1). El `analytics/` devuelve **solo datos**; el
`render/` decide cómo dibujar. Mañana se cambia el renderer sin tocar el motor.

**Por qué Matplotlib en el producto (asesor + director):** reproducibilidad exacta de informes oficiales,
control de la identidad visual (tipografía, colores de gobernanza, export PDF/SVG) y **coherencia con el
Bloomberg Firewall** — el renderer fija el lenguaje una sola vez, sin defaults que puedan filtrar lo interno.
Seaborn queda para la **fase científica** (calibración, matriz de confusión), nunca para el producto.

---

## 2 · El objeto canónico — `NarrativeEvidence`

Toda visualización del Motor Narrativo consume **este** objeto (no el motor). Un renglón = una afirmación.

| Atributo | Significado |
|---|---|
| `id` | identificador de la afirmación (ej. `MN2024-058`) |
| `entidad` | GAD / EP / Patronato… (quién habla) |
| `afirmacion` | el texto dicho por la autoridad |
| `tipo` | clasificación narrativa (Familia A): gestión · proceso · meta |
| `estado` | veredicto legible (Verificado · En contratación · Declarado · Sin evidencia · Contradicción) |
| `nivel_evidencia` | Familia B: independiente · institucional · parcial · sin_evidencia_publica · contradiccion |
| `fuente` | el documento/sistema que respalda (POA · PAC/SERCOP · cédula · Literal D · informe) o vacío |
| `regla` | regla de jurisprudencia aplicada (R1…R8 / familia) |
| `explicacion` | la evidencia, en **lenguaje de gobernanza** (no acusatorio) |
| `periodo` | ventana temporal (ej. `2024`, `sep–dic 2024`) — jamás se extrapola |
| `confianza` | score del cruce (0–1) |

---

## 3 · La gramática de color — EJE DE EVIDENCIA (decisión del director · 2026-07-08)

Distinta del **semáforo de cumplimiento** del Gold Master (¿se cumplió?). Esta mide **verificabilidad
pública** (¿qué respaldo tiene?). Coexisten: son ejes distintos, hermanos coherentes (verde/rojo alineados).

| Nivel de evidencia | Color | Nombre | Significa |
|---|---|---|---|
| independiente | 🟢 `#1E8E3E` | verde | Verificado en registro externo del Estado |
| institucional | 🔵 `#1A73E8` | azul | Declarado solo en el documento de la propia entidad |
| parcial | 🟡 `#F9AB00` | ámbar | Hay evidencia, con ventana temporal limitada |
| sin_evidencia_publica | ⚪ `#9AA0A6` | gris | **No existe evidencia pública** (ausencia ≠ "malo") |
| contradiccion | 🔴 `#D93025` | rojo | La evidencia pública contradice lo afirmado |

**El gris es deliberado:** "sin evidencia" es un **resultado de auditoría**, no una acusación (principio
rector). Nunca rojo por ausencia. Regla de convivencia: cada gramática se muestra **etiquetada por su eje**,
nunca como un punto de color a secas que pueda confundirse con el otro semáforo.

---

## 4 · Orden de trabajo (asesor)

1. **Definir el objeto canónico** `NarrativeEvidence` → `app/viz/evidence.py`. ✅
2. **Construir la arquitectura** `analytics/` → `render/` → `app/viz/`. ✅ (analytics + interfaz render)
3. **Implementar el primer cajón** "Verificabilidad Pública del Discurso" (render Matplotlib/SVG). ← siguiente
4. **Reutilizar el patrón** en todos los módulos (ICPI, PAC, POA, CPCCS, Cobertura, Presupuesto).

---
*Sistema de Visualización Canónico · Dylus Lab © 2026 · el motor nunca conoce al renderer · CAF ve algo que un alcalde entiende en 10 segundos.*
