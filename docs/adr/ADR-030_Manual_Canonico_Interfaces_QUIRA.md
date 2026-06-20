# ADR-030 · Manual Canónico de Interfaces QUIRA

**Estado:** EN REVISIÓN (Javo) · 2026-06-21 · canon de Experiencia Metodológica
**Contexto de origen:** rediseño del Centro de Mando. Mesa (colega + académico): *"no diseñes un dashboard bonito; diseña un instrumento de gobierno."*
**Relacionado:** ADR-027 (firewall · lenguaje público) · ADR-028 (compilador) · `p_command_center_v2.py` · `firewall_dictionary.json`

---

## Principio rector

QUIRA **no vende gráficos: vende comprensión.** El Centro de Mando no es un *menú* (lanzador de
pantallas) — es el **puente de mando** de un sistema operativo de inteligencia pública. Toda interfaz
obedece dos leyes:
1. **Instrumento de gobierno, no aplicación bonita.** Cada elemento enseña o decide; nada es decorativo.
2. **Regla 50/50** — 50% visualización · 50% interpretación. Un gráfico sin criterio no pasa.

Este manual define la **anatomía** una sola vez; los 13 cajones DERIVAN de él y nunca vuelven a divergir.

## §1 · Anatomía del CAJÓN — las 4 preguntas (obligatorias, sin excepción)

Ninguna card muestra datos sueltos. Cada cajón responde, en este orden:

| # | Pregunta | Elemento | Regla |
|---|---|---|---|
| 1 | ¿Qué dominio? | **Nombre** del dominio | nº + nombre |
| 2 | ¿Qué significa? | **Significado canónico** | definición metodológica, **NO eslogan** · lenguaje público (firewall) |
| 3 | ¿Cómo está? | **Estado** | el número del motor + badge de estado |
| 4 | ¿Por qué me importa? | **Pregunta marco-causal** | la invitación que da sentido al dato |

**Mecánica (A1 · locked):** card 100% clicable vía `st.button` transparente superpuesto (nativo, sin
iframe → navega en deploy). Sin botón "abrir". Layout **Variante A**: concepto (izq) | métrica grande +
estado (der) · pregunta al pie · ↗ en la esquina · hover aclara el borde. Grilla 4×3 · color por temperatura.

## §2 · Los 4 Dominios de Exploración (menú superior · identidad de cada QUIRA)

Los 4 de arriba **NO son KPIs ni atajos** (eran redundantes con los 12). Son **Dominios de Exploración**:
le dan cerebro propio a cada producto de la Suite. No solo cambian dashboards — cambian la identidad.

**QUIRA Institucional** (confirmado · Javo 2026-06-21):
```
①  Territorio          realidad dura: INEC · NBI · PDOT · cobertura · demografía
②  Gobierno            concejo · alcalde · dependencias · organigrama · competencias
③  Proyecto Político   Plan de Trabajo CNE · promesas · visión · agenda
④  Evidencia Documental ordenanzas · contratos · planes · informes (el búnker probatorio)
```
*(QUIRA Operaciones y Ciudadana definirán sus 4 Dominios cuando se construyan — mismo patrón, distinto cerebro.)*

## §3 · Anatomía del DASHBOARD interno (Regla 50/50)

Cada dashboard = dos mitades de igual peso:
```
┌─────────────────────────┬─────────────────────────┐
│  VISUALIZACIÓN (50%)     │  INTERPRETACIÓN (50%)    │
│  gráficos · tablas ·     │  el CRITERIO de QUIRA    │
│  mapas · series          │  (§4) — no leyendas      │
└─────────────────────────┴─────────────────────────┘
```
Se conserva solo lo valioso del dashboard heredado; lo demás se reconstruye bajo esta regla.
*(Todo dashboard heredado es un prototipo exploratorio, no canon.)*

## §4 · Anatomía de QUIRA IA — produce CRITERIO, no describe gráficos

La IA **no explica el dashboard** (eso ya existe en todo sistema). **Responde la pregunta marco-causal
del cajón (§1.4) y produce juicio metodológico.** Ejemplo canónico (RdC):
> *"El informe presentado al CPCCS refleja el 91% de la gestión observada. Sin embargo, el discurso
> público sobrerrepresenta la inversión en seguridad y omite parcialmente la ejecución social. Se
> detectan tres divergencias relevantes."*

No describe barras: dictamina. Frontera Regla 1 intacta — razona sobre la verdad sellada, no la recalcula.

## §5 · Caso canónico — Rendición de Cuentas (destruir y reconstruir)

El cajón 09 actual es invento; se reconstruye entero. RdC = **congruencia de tres relatos**:
```
RENDICIÓN DE CUENTAS · Congruencia entre:
   Gestión (lo que el sistema midió)  →  Informe CPCCS (lo reportado)  →  Discurso público (lo comunicado)

            ┌─────────────────────┐
            │   89% CONGRUENCIA    │   ← indicador gigante
            └─────────────────────┘
   ┌──────────────┬──────────────┬──────────────┐
   │ Lo ejecutado │ Lo reportado │ Lo comunicado│   ← 3 columnas
   └──────────────┴──────────────┴──────────────┘
   NLP del discurso (link de redes)  ← abajo, evidencia
   Criterio QUIRA (§4): las divergencias dictaminadas
```
Fuentes reales: informe oficial CPCCS + link del evento público de RdC (discurso) → NLP. Conecta con el
diferenciador del §0 de la Hoja de Ruta (Plan CNE + NLP discurso = demagogia expuesta).

## §6 · Holding — resolución de arquitectura de información

Holding se volvió **cajón comodín** (acumuló contenido ajeno). Misión canónica (confirmada · Javo):
**consolidación ponderada de las 4 entidades** (GAD · EP Aseo · Bomberos · Patronato) medidas con la
misma vara. **Adelgaza:** el contenido de Rendición de Cuentas → cajón 09 · el de Participación → cajón 08.
Cada widget vive donde pertenece; Holding deja de ser comodín.

## §7 · Los átomos (definidos una vez)

- **Métrica:** el número que dictamina el motor (Gold Master). Nunca se recalcula en la UI.
- **Concepto / significado canónico:** definición metodológica en lenguaje público (firewall · ADR-027) — jamás eslogan, jamás acrónimo interno.
- **Evidencia:** todo dato visible debe rastrearse a soporte verificable (SHA-256 / norma · Regla 3).

## Consecuencias

- Los 13 cajones y sus dashboards **derivan de este manual** → cero divergencia futura.
- Orden de construcción: A1 (card · §1) → A2 (Dominios · §2) → dashboards (§3-4) por ola → RdC (§5) → Holding (§6).
- Es **VÍA PRODUCTO** (Sprint D · CAF): mejora el molde Montecristi mostrable.
- **Verificación en deploy obligatoria** antes de declarar hecho cualquier cajón (regla del proyecto).

---
*ADR-030 · Manual Canónico de Interfaces QUIRA · Dylus Lab © 2026 · "Cada cajón enseña. Cada dashboard interpreta. La IA dictamina. La interfaz dejó de ser una app bonita: habla el Canon."*
