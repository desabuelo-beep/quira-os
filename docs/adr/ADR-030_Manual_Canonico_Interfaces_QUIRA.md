---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-030 · Canon de Expresión de Interfaz QUIRA

**Estado:** RATIFICADO · 2026-06-21 (Javo) · reescrito estrecho para NO duplicar el Diccionario
**Alcance estricto:** SOLO la **expresión visual**. El **contenido** (qué es cada cajón, su pregunta,
exclusiones, indicador madre) lo gobierna `docs/sprint-c/DICCIONARIO_CONCEPTUAL_QUIRA.md` (13 ADN ·
11 campos · SELLADO 2026-06-14) — **fuente única**. Este ADR **no redefine dominios.**
**Relacionado:** DICCIONARIO_CONCEPTUAL (contenido) · PLANO_DE_CAJONES (método cosecha) · CONSTITUCION_ONTOLOGICA · ADR-027 (firewall) · ADR-028.

---

## Por qué existe (y por qué NO duplica)

El Diccionario ya define **QUÉ es cada cajón** (13 ADN anclados al motor). No define **CÓMO se renderiza.**
Este ADR cubre solo la forma, y **deriva todo su contenido del Diccionario.**

> **Regla anti-duplicación:** ADR-030 no contiene definiciones de dominio — contiene reglas de render.
> El texto de la UI se LEE del ADN, jamás se reescribe aquí. Si la UI contradice el Diccionario, gana el Diccionario.

*(Nota de memoria: la versión previa de este ADR y la mesa de 2026-06-21 re-derivaron una anatomía de
"4 preguntas" sin recordar el ADN de 11 campos ya sellado — la "pérdida de narrativa" que el colega advirtió.
Javo lo cazó. Esta versión lo corrige: el ADN manda.)*

## §1 · La card del cajón = RENDER del ADN (Variante A)

La card renderiza campos del ADN — no inventa texto:

| Elemento visual (card) | Campo del ADN (Diccionario · fuente) |
|---|---|
| Nombre | Campo 2 · Dominio Canónico (Nomenclátor) |
| Concepto / significado | Campo 4 · Definición conceptual (en lenguaje público · firewall ADR-027) |
| Métrica + estado | Campo 10 · Indicador madre + operativos (leído del motor · Regla 1, nunca recalcular) |
| Pregunta | Campo 6 · Pregunta estratégica |

**Layout Variante A:** nombre arriba · concepto (izq) | métrica+estado (der) · pregunta al pie · ↗ esquina.
**Mecánica A1:** card 100% clicable vía `st.button` transparente superpuesto (nativo · sin iframe · navega en
deploy). Sin botón "abrir". Grilla · color por temperatura · d04 dinámico · cajón deshabilitado seguro.

## §2 · Los 4 Dominios de Exploración (menú superior · GENUINAMENTE NUEVO)

Lo único que el canon no tenía (Javo + mesa · 2026-06-21): los 4 de arriba dejan de ser KPIs redundantes
y se vuelven el **menú de identidad de cada producto**. **QUIRA Institucional:**
① Territorio · ② Gobierno · ③ Proyecto Político (Plan CNE) · ④ Evidencia Documental.
*(NO son los 13 dominios de gestión — son navegación de producto. Operaciones/Ciudadana definirán los suyos.)*

## §3 · El dashboard interno = Regla 50/50

Cada dashboard = 50% visualización + 50% interpretación (el criterio de QUIRA IA, §4 — no leyendas).
Se construye por **cosecha** (`PLANO_DE_CAJONES`): se recicla lo valioso de las ~40 pantallas-cantera; se
crea solo lo que falte. **Ningún dashboard nace de una pantalla; nace del ADN** (Regla QUIRA).

## §4 · QUIRA IA en la interfaz = produce CRITERIO

La IA responde la **Pregunta estratégica** del ADN (campo 6) con juicio metodológico, no describe gráficos.
Ej.: *"el informe refleja el 91% de la gestión; el discurso sobrerrepresenta seguridad y omite ejecución
social · 3 divergencias."* Frontera Regla 1 intacta (lee la verdad sellada, no la recalcula).

## §5 · La frontera "qué NO es" se respeta en el render

El **campo 8 del ADN (Exclusiones)** gobierna dónde vive cada widget. Caso vivo: **Holding (d05)** acumuló
contenido de RdC (→d09) y Participación (→d08) en `p2_holding.py`, violando las Exclusiones de su propio ADN.
Render correcto = reubicar a sus cajones. **No es decisión nueva: es cumplir el canon** (confirmado · Javo).

## Consecuencias

- ADR-030 = contrato de **render**. Diccionario = contrato de **contenido**. Cero competencia, cero duplicación.
- **Trabajo real (Sprint D · VÍA PRODUCTO):** sincronizar el Centro de Mando vivo con el canon. Hoy:
  `p_command_center_v2.py` tiene **12 cajones con nombres viejos**; el canon tiene **13 ADN** con Nomenclátor
  (falta **d13 Sostenibilidad y Resiliencia Ambiental**; renombrar d03→"Gobernanza del Mandato",
  d10→"Cobertura de Servicios e Infraestructura", d12→"Inclusión, Equidad y Género").
- **Orden:** sincronizar nombres + 13 cajones → A1 card (Variante A) → 4 Dominios de Exploración →
  dashboards por ola (cosecha) → verificación en deploy. Es **implementar el canon**, no re-conceptualizar.

---
*ADR-030 · Canon de Expresión de Interfaz QUIRA · Dylus Lab © 2026 · "El Diccionario dice qué es cada cajón; este canon dice cómo se ve. El contenido se lee del ADN — jamás se reinventa en la UI."*
