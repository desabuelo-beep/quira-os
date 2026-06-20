# ADR-028 · Compilador de Lenguaje Institucional + Ciclo de Inteligencia Determinista (CID)

**Estado:** RATIFICADO · 2026-06-20 (Javo + mesa: colega asesor + académico · reframe post-Blitz)
**Contexto de origen:** Sprint D.2A — Firewall Blitz COMPLETO (deuda Familia 119 → 0).
**Relacionado:** ADR-027 (3 capas de soberanía) · Regla 1 (Excel=Estado) · `scripts/dev/firewall_audit.py` · `docs/architecture/QUIRA_IA_BUCLES_AGENTICOS.md`

---

## Contexto — qué construimos sin nombrarlo

El Firewall Blitz no fue una limpieza de acrónimos. Al llevar la deuda Familia de 119 a 0,
calibramos un instrumento que **traduce determinísticamente** la nomenclatura canónica interna
(ICPI·TGI·SAT·H73·Gold Master) a lenguaje de administración pública. Eso tiene un nombre en
ingeniería: **un compilador.** Y el método con que lo ejecutamos —escanear → verificar capa →
editar → compilar → re-escanear → commit → siguiente— es **un bucle agéntico**. Lo corrimos a
mano. Es reproducible y automatizable.

## Decisión 1 — El Compilador de Lenguaje Institucional (CLI-Q)

`firewall_audit.py` **ya es el front-end de un compilador** — no es aspiración, está construido:

| Fase de compilador | Qué hace hoy el escáner | Estado |
|---|---|---|
| Lexer/Parser | AST walk → tokeniza strings VISIBLES (excluye docstrings/comentarios = "no fuente") | ✅ |
| Tabla de símbolos | `PROHIBITED`: cada regla mapea `término canónico → alternativa pública` (el `alt` YA existe) | ✅ |
| Análisis de alcance | clasificación de capa DYLUS/QUIRA_IA/FAMILIA (ADR-027) = qué se compila y qué no | ✅ |
| **Transform / code-gen** | aplicar el `alt` y reescribir el string | ⛏️ hoy lo hace el humano |

**Insight clave:** la columna `alt` de `PROHIBITED` (ICPI→"Cumplimiento", SAT→"Alerta"…) **es la tabla
de traducción**. El compilador no hay que inventarlo: hay que **cerrar el último paso** (el transform).

### Multi-backend — un motor, N idiomas
"Público" es un solo *target*. El mismo source canónico compila a otros cambiando la columna `alt`:

```
            ┌─→ alt_publico    → Familia QUIRA (GAD)
 CANON  ────┼─→ alt_academico  → tesis / papers
 (Dylus)    ├─→ alt_juridico   → cascada legal / SHA-256
            ├─→ alt_financiero → PNUD / BID / GEF
            └─→ alt_ciudadano  → la gente
```
Un compilador con backends intercambiables. **Esto es propiedad intelectual vendible** (metodología GovTech).

## Decisión 2 — El Ciclo de Inteligencia Determinista (CID)

El transform automatizado es un **bucle agéntico de memoria estructurada** (no conversacional):

```
 estado.json ─→ LLM (Haiku) propone 1 acción ─→ aplicar parche ─→ re-escanear EL ARCHIVO
      ▲                                                                    │
      └──────────────── actualizar estado (leaks, alt, paso) ◄────────────┘   hasta ALTO=0
```

**Tres reglas que vuelven el CID barato y determinista** (corrigen la "bola de nieve" de tokens):
1. **Memoria estructurada, no conversacional.** El ciclo lee SOLO `estado.json` + el archivo objetivo.
   Cero historial de chat acumulado → costo plano por vuelta.
2. **El escáner provee el target.** `estado.json` lleva `{term, alt, línea}` desde el escáner — el LLM
   no *adivina* la traducción, la *aplica*. Determinismo guiado.
3. **Escaneo por-archivo, no por-repo.** *(Mejora sobre el blueprint del académico.)* Cada vuelta
   re-escanea SOLO el archivo objetivo vía `scan_file(path)`, no `quira_pages/` completo → **O(1) por
   iteración, no O(n)**. *Prerrequisito:* que el CLI del escáner acepte un archivo (hoy solo carpeta).

Modelo escudo: **Haiku 4.5** + caché + `task_budget`. Bucle acotado (≤N pasos) = centavos.

## Decisión 3 — Dónde vive el CID (disciplina inviolable)

| Capa | ¿Bucles? | Por qué |
|---|---|---|
| **Familia QUIRA (cliente GAD)** | ❌ NUNCA | El alcalde necesita respuestas DETERMINISTAS. `Excel → Motor → Respuesta`. Cero costo API oculto, cero improvisación (Regla 1). |
| **QUIRA IA (infra)** | 🔁 acotados | Razonamiento causal sobre el grafo · Sentinel · `task_budget`. |
| **Dylus Lab (laboratorio)** | 🔁 largos | CID Auditor (= el Blitz) · CID Ontológico · CID ADR · CID Excel · CID Sentinel. Aquí viven los agentes autónomos. |

**El CID jamás toca el producto del cliente.** Es la cadena de montaje del laboratorio, no la máquina vendida.

## Consecuencias

- El Firewall Blitz se reconceptualiza: fue el **primer pase manual del CID Auditor.** Reproducible.
- Roadmap natural de `firewall_audit.py`: (a) CLI acepta un archivo · (b) modo `--suggest` (emite el `alt`) ·
  (c) modo `--fix` (transform) · (d) envolverlo en el CID con `estado.json`.
- Capa Familia QUIRA: **0 bucles, 100% determinista** — sellado como diferenciador comercial (con ADR-027).
- Pendiente (post-convergencia · decisión de Javo, NO ahora): construir el primer CID autónomo en Dylus
  Lab sobre el Gold Master validado, en las capas Analista/Laboratorio — nunca en la pública.

---
*ADR-028 · Compilador de Lenguaje Institucional + CID · Dylus Lab © 2026 · "El Firewall dejó de ser una restricción: es un compilador. El motor produce la verdad; el CID produce N idiomas de esa verdad — sin tocar jamás la respuesta determinista que ve el GAD."*
