# UX Contract — QUIRA Intelligence
## Sprint D.1 · Estabilización Operacional

> **Propósito**: Este documento es el blueprint visual y conductual de QUIRA.  
> Cualquier implementación futura (React, Next.js, móvil) debe cumplirlo.  
> Las decisiones aquí son definitivas hasta que una nueva versión del contrato las reemplace.

**Versión**: 1.0  
**Fecha**: 2026-05-27  
**Autoridad**: Dylus Lab  
**Fuente viva**: `quira_pages/p_vista_ejecutiva.py` + `quira_pages/p_concejo.py`

---

## 1. Identidad Visual

### 1.1 Paleta canónica

| Token | Hex | Uso |
|---|---|---|
| `--accent` | `#00D4FF` | Identidad QUIRA, links, chips IA, ecosistema |
| `--ruptura` | `#EF4444` | TOP en ruptura, SAT-III, alertas críticas |
| `--sostenib` | `#22C55E` | TOP sobre ritmo, D5 capacidad, SISTEMA VIVO |
| `--amber` | `#F59E0B` | SAT-IV, Concejo ALTO, compromisos urgentes |
| `--warning` | `#F97316` | SAT activas, cierre Q2, naranja intermedio |
| `--purple` | `#7C5CFC` | Fondos bloqueados, reencuadre político |
| `--bg` | `#050A12` | Background global — negro institucional |
| `--surface` | `rgba(255,255,255,.025)` | Cards, zonas — superficie con profundidad |
| `--border` | `rgba(255,255,255,.07)` | Bordes base — sutil, no intrusivo |
| `--text` | `#E2E8F0` | Texto principal — blanco frío |
| `--muted` | `rgba(255,255,255,.35)` | Texto secundario |
| `--ultra-muted` | `rgba(255,255,255,.18)` | Metadata, labels de zona |

**Semáforo TGI estándar** (función `_sem(valor)`):

| Rango | Color | Significado |
|---|---|---|
| ≥ 70 | `#22C55E` | Sostenible |
| 50–69 | `#FFB700` | Transición |
| 30–49 | `#F97316` | Atención requerida |
| < 30 | `#EF4444` | Ruptura |

**Semáforo TOP** (colores definidos en `utils/top.py`):

| Categoría | Color | Umbral |
|---|---|---|
| `ruptura` | `#EF4444` 🔴 | TOP < 60% |
| `alerta` | `#F97316` 🟠 | TOP 60–79% |
| `sostenible` | `#22C55E` 🟢 | TOP ≥ 80% |
| `sobre_ritmo` | `#22C55E` 🟢 | TOP > 100% (display: "Sobre ritmo esperado") |

### 1.2 Tipografía

| Rol | Familia | Peso | Tamaño |
|---|---|---|---|
| Headings institucionales | `Inter` | 900 | `clamp(2.4rem, 7vw, 4rem)` |
| Métricas dominantes (TOP, TGI) | `Inter` | 900 | `3rem` / `2.8rem` |
| Métricas secundarias | `Inter` | 900 | `1.5rem–1.6rem` |
| Cuerpo ejecutivo | `Inter` | 400 | `11px/1.7` |
| Labels zona / chips | `Inter` | 700–800 | `7px–9px`, `letter-spacing: .07–.1em`, `UPPERCASE` |
| Metadata / fuentes | `JetBrains Mono` | 400 | `8px–9px` |
| Alertas / acciones | `Inter` | 600–700 | `10px–11px` |

**Regla tipográfica principal**: los números grandes hablan primero. El texto describe, nunca compite con el número.

---

## 2. Arquitectura de Atención (Modelo Cognitivo)

Esta es la doctrina central de UX de QUIRA. Todo elemento de la interfaz tiene una **capa de atención asignada**. No se puede poner contenido de capa 3 antes del de capa 1.

```
TIEMPO   CAPA          ELEMENTO                     SEÑAL
0–3s     DOMINANTE     TOP % en rojo grande         Crisis sistémica
3–8s     CONTEXTO      TGI + D1–D5 barras           Marco institucional
8–15s    ACCIÓN        Briefing strip + SAT          Qué hacer hoy
15–30s   SOPORTE       Ecosistema + IA + Fondos      Profundidad analítica
```

### 2.1 Jerarquía de Zonas

| Zona | Nombre | Grid | Peso visual | Capa |
|---|---|---|---|---|
| Z1 | Pulso del Municipio | Col 1 · Rows 1–2 | 🔴 MÁXIMO | 1 |
| Z2 | Lo Urgente (SAT) | Col 2 · Row 1 | 🔴 ALTO | 1 |
| Z34 | Compromisos + Territorio | Col 2 · Row 2 | 🟡 MEDIO | 2 |
| Z5 | Ecosistema Municipal | Full-width | 🟢 SOPORTE | 3 |
| Z6 | QUIRA IA + Oportunidades | Full-width | 🟢 SOPORTE | 3 |

**Grid CSS canónico**:
```css
.ve-grid {
  display: grid;
  grid-template-columns: 1.45fr 1fr;   /* Z1 domina */
  grid-template-rows: auto auto;
  gap: 14px;
}
.ve-z1  { grid-column: 1; grid-row: 1 / 3; }  /* DOMINANTE */
.ve-z2  { grid-column: 2; grid-row: 1; }
.ve-z34 { grid-column: 2; grid-row: 2; }
.ve-z5, .ve-z6 { grid-column: 1 / -1; }       /* Full width */
```

**Breakpoints**:
- `≤ 900px` → stack vertical, 1 columna, Z34 visible completo
- `≤ 480px` → ecosistema a 2 cols (luego 1 col)

---

## 3. Tokens de Spacing

| Token | Valor | Uso |
|---|---|---|
| `gap-grid` | `14px` | Gap entre zonas principales |
| `gap-card` | `12px` | Gap entre entity cards (ecosistema) |
| `gap-inner` | `8–10px` | Gap interno dentro de zona |
| `pad-zone` | `20px` | Padding zona estándar |
| `pad-zone-compact` | `14px 16px` | Padding Z34 (compacta) |
| `pad-card` | `14px 12px` | Padding entity card |
| `pad-header` | `11px 18px` | Padding header institucional |
| `pad-briefing` | `12px 18px` | Padding briefing strip |
| `gap-label` | `8px` | Gap ícono → texto en rows |
| `margin-section` | `16px 0` | Separación entre secciones dentro de zona |

**Regla de spacing**: los gaps son siempre múltiplos de 2. Nada de 3px, 5px, 7px. Excepciones documentadas aquí.

---

## 4. Animaciones — Sprint C.3 Observabilidad Viva

Doctrina: **"el sistema respira — pulsos mínimos, no ruido"**. Cada animación tiene un propósito semiótico específico.

| Nombre | Propiedad | Timing | Propósito |
|---|---|---|---|
| `ve-ruptura-glow` | `box-shadow` 0→5px+22px | 2.8s ease-in-out | Señal crítica TOP ruptura en Z1 |
| `ve-live-beat` | `opacity` 1→0.28 + `scale` 1→0.58 | 1.8s ease-in-out | Heartbeat "SISTEMA VIVO" en header |
| `ve-briefing-glow` | `border-left-color` 60%→100% | 3.2s ease-in-out | Urgencia en briefing strip (solo ruptura) |

**Timings distintos intencionalmente**: 1.8s / 2.8s / 3.2s crean sensación orgánica — ningún elemento pulsa al unísono.

**Clases CSS**:
```css
.ve-ruptura-pulse  → TOP RUPTURA box en Z1
.ve-live-dot       → heartbeat dot (6×6px, verde)
.ve-briefing-live  → briefing strip (solo cuando GAD = ruptura)
```

**Regla de animaciones**: solo se animan elementos que comunican **estado sistémico crítico**. Nunca decorativas. El sobre-ritmo no se anima (es positivo, no urgente).

---

## 5. Componentes Canónicos

### 5.1 Header Institucional

```
[🏛 GAD Nombre]  [Subtítulo corte]       [TGI chip] [SAT chip] [Ejecutivo chip] [● SISTEMA VIVO]
```

- Height: `auto`, padding `11px 18px`
- Background: `rgba(255,255,255,.02)`
- Border: `1px solid rgba(255,255,255,.07)`, `border-radius: 12px`
- KPI chips: `background: {color}12`, `border: 1px solid {color}30`, `border-radius: 8px`
- SISTEMA VIVO chip: verde, dot animado, timestamp `HH:MM · DD/MM`

### 5.2 Briefing Strip

```
[◆ BRIEFING EJECUTIVO]  |  [2 oraciones ejecutivas · máximo 280 chars]
[QUIRA IA · Corte]      |
```

- Siempre antes del grid, full-width
- `border-left: 3px solid {color_gad}` — color dinámico según TOP del GAD
- Animado (`ve-briefing-live`) solo cuando GAD está en ruptura
- Texto: máximo 280 chars, 2 oraciones, extraídas de `narrativa_ia()`

### 5.3 TOP Señal Crítica (Z1)

```
[⚡ Inversión GAD · Señal Crítica]      [🔴 RUPTURA]
[8.1%]  ← dominante visual, 3rem, rojo
[TOP · Trayectoria Operativa Proyectada · Q1-2026]
[diagnóstico]
```

- `border-left: 4px solid {color}`
- Animado (`ve-ruptura-pulse`) cuando categoría == RUPTURA
- El número es lo primero que ve el ojo: `font-size: 3rem`, weight 900

### 5.4 Mini Bar (TGI D1–D5)

```
[Label 9px bold] [sub 8px muted]        [valor%]
[──────────────────────────█████]  3px height, color semafórico
```

- `height: 3px`, `border-radius: 2px`
- Color del bar = `_sem(valor)` — semáforo estándar
- Margen bottom `9px` entre barras

### 5.5 Alerta Card (SAT)

```
[SAT-III badge]  [Título de la alerta]
[Causa detallada — 2 líneas max]
[⏱ Tiempo]      [COPFP Art. 113]
[→ Acción concreta]
```

- `border-left: 3px solid {color}`
- Background: `{color}07`
- Acción siempre en `color` del SAT (nunca blanco)

### 5.6 Entity Card (Ecosistema)

```
[emoji] [Nombre entidad]
[Ti Q1: X.XX%  (nota)]
[TOP badge: {valor o "Sobre ritmo"}]
[Codificado $K]  [Devengado Q1 $K]
```

- `border-top: 3px solid {color}` — semáforo por categoría
- `border-color: {color}33` lateral — translúcido del mismo color
- TOP display: si `top_display = None` → texto "Sobre ritmo esperado"

### 5.7 Compromiso Row

```
[icon 14px]  [Título  VALOR_COLOR]
             [descripción 9px muted]
             [⏱ urgencia] (si existe)
[── border-bottom ──────────────────]
```

- Gap: `10px`
- Bottom border: `1px solid rgba(255,255,255,.05)`
- Urgencia siempre en color propio (default amber)

---

## 6. Modo Concejo — Sala de Mando

Activado desde `env_gov.py` cuando `ejecutivo_modo == "concejo"`.

### 6.1 Paleta diferenciada

| Elemento | Color |
|---|---|
| Header accent | `#F59E0B` (amber — político, no institucional) |
| Ataque CRÍTICO borde | `#EF4444` |
| Ataque ALTO borde | `#F97316` |
| Ataque MEDIO borde | `#F59E0B` |
| Datos QUIRA | `#00D4FF` |
| Respuesta | `#E2E8F0` |
| Reencuadre | `#C084FC` (púrpura) |
| Ley | `rgba(255,255,255,.3)` |
| Argumentario ofensivo | `#22C55E` / `#00D4FF` / `#C084FC` / `#F59E0B` |

### 6.2 Anatomía de un Ataque Card

```
[NIVEL badge]  [Número ataque]
["Cita del concejal opositor"]      ← rojo o amber según nivel
[Datos QUIRA que sustentan]         ← cyan
[Respuesta del ejecutivo]           ← blanco
[Reencuadre político]               ← púrpura
[Base legal]                        ← muted
```

**Regla de Concejo**: los datos siempre preceden a la respuesta. El ejecutivo no argumenta desde la emoción — argumenta desde los números.

---

## 7. Semántica Institucional

Estos términos tienen significado técnico preciso. No son intercambiables:

| Término | Definición | Nunca confundir con |
|---|---|---|
| **TOP** | Trayectoria Operativa Proyectada = `Ti_acum / W_Q` | Porcentaje de ejecución simple |
| **TGI** | Índice de Gobernanza Territorial Integral (5 dims) | Rating general o nota |
| **SAT** | Sistema de Alerta Temprana institucional | "Alerta" genérica |
| **ICPI** | Índice de Coherencia del Plan Institucional | Avance de ejecución |
| **Ti** | Tasa de inversión acumulada al corte | Gasto total |
| **W_Q** | Peso trimestral calibrado eSIGEF | Factor arbitrario |
| **IRS** | Índice de Regresividad del Gasto | Gini o distribución simple |
| **IET** | Índice de Equidad Territorial parroquial | Cobertura geográfica |
| **IED** | Índice de Eficiencia Directiva | Performance individual |
| **RDC** | Rendición de Cuentas (CPCCS) | Reporte interno |

---

## 8. Reglas de Comportamiento Ejecutivo

Estas reglas gobiernan CÓMO QUIRA presenta información. Son inviolables.

1. **Los números grandes hablan primero**. Nunca poner texto antes del número dominante en Z1.
2. **Un color por semántica**. Rojo = ruptura. Verde = saludable. Amarillo = transición. Nunca invertir.
3. **La acción siempre termina la tarjeta**. Después del diagnóstico, siempre hay `→ acción concreta`.
4. **El briefing son 2 oraciones máximo**. No más. No un párrafo. No un resumen completo.
5. **QUIRA no es chatbot**. El tono es ejecutivo institucional. Sin "puede que", "quizás", "podría".
6. **Las fuentes siempre visibles**. Cada métrica tiene su fuente (Gold Master v5.5_TGI, COPFP Art. X).
7. **El ecosistema siempre muestra las 4 entidades**. GAD · Patronato · EP Aseo · Bomberos. Sin excepciones.
8. **TOP > 100 nunca muestra número**. Display: "Sobre ritmo esperado". El número puede generar confusión.
9. **Animaciones solo en estados críticos**. Ruptura pulsa. Sostenible no pulsa.
10. **El concejo tiene paleta propia**. Amber, no cyan. Cambia el tono emocional del dashboard.

---

## 9. Anti-patrones (NO hacer)

| Anti-patrón | Razón |
|---|---|
| Mostrar datos sin fuente | Pierde autoridad institucional |
| Poner TGI antes de TOP ruptura | Viola jerarquía cognitiva (3s regla) |
| Texto descriptivo antes del número grande | El ojo busca el número primero |
| Usar `border-radius > 14px` en zonas | Pierde carácter institucional |
| Color rojo en cosas no críticas | Desensibiliza la señal de ruptura |
| Más de 3 animaciones simultáneas | Ruido visual, pierde atención |
| Número negativo sin contexto | Confunde sin el W_Q o la comparación |
| Cambiar colores entre Vista Ejecutiva y Concejo | El alcalde debe reconocer el mismo sistema |
| Truncar narrativa IA en menos de 1 párrafo | Pierde el valor analítico |
| Mostrar todos los datos de una parroquia | Solo IET · NBI · inv/hab — nada más |

---

## 10. Contrato de Migración React

Cuando QUIRA migre a React/Next.js, este contrato garantiza continuidad. La migración es válida solo si:

- [ ] Todos los tokens CSS de §1.1 están en un archivo `tokens.ts` o `design-tokens.json`
- [ ] El modelo cognitivo (§2) está implementado como layout invariante
- [ ] Los 3 keyframes de animación (§4) están en un módulo CSS global
- [ ] Los 7 componentes canónicos (§5) tienen su React component homónimo
- [ ] La semántica institucional (§7) está en un archivo de constantes, no hardcodeada
- [ ] Las reglas de comportamiento ejecutivo (§8) están documentadas como comentarios en cada componente
- [ ] La paleta Concejo (§6) es una variante de tema, no un archivo separado

---

*Dylus Lab · QUIRA Intelligence · Sprint D.1 UX Contract v1.0 · 2026-05-27*
