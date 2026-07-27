---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-027 · Tres Capas de Soberanía de Lenguaje

**Estado:** RATIFICADO · 2026-06-17 (Javo + mesa: colega asesor + académico)
**Contexto de origen:** Sprint D.2A — Firewall Blitz. Observación fundacional de Javo.
**Relacionado:** Regla 2 (Bloomberg Firewall · CLAUDE.md) · ADR-024 (Radar Nacional) · `quira-language-guard`

---

## Contexto

El Firewall Blitz operaba con una premisa implícita **falsa**:
> "Todo lo que está en QUIRA debe hablar lenguaje de gobernanza."

Javo identificó la confusión arquitectónica: **el centro técnico vive en Dylus Lab, no en QUIRA.**
La nomenclatura canónica (ICPI·TGI·SAT·H73·Gold Master·QTMP) **es legítima y nativa en el laboratorio** —
es el lenguaje con el que Dylus Lab audita y calibra los algoritmos. No es deuda; es la cocina.

La pregunta correcta no es *"¿hay nomenclatura canónica?"* sino:
> **"¿Esta pantalla pertenece a la Familia QUIRA (producto vendible) o a Dylus Lab (laboratorio)?"**

## Decisión — tres capas de soberanía

```
┌─ CAPA 1 · DYLUS LAB (el laboratorio) ──────────────────────────────┐
│  Canon PURO legítimo: ICPI·TGI·SAT-III·H73·H90·Gold Master·QTMP    │
│  Consolas internas: ingesta, validación, calibración, monitoreo    │
│  nacional. Equivale a Bloomberg Methodology Center / DeepMind Res.  │
│  → NO se purga. El canon es el lenguaje nativo del fabricante.      │
└───────────────────────────────┬────────────────────────────────────┘
                                ▼
┌─ CAPA 2 · QUIRA IA (la infraestructura) ───────────────────────────┐
│  Motor transversal invisible: grafos, Neo4j, QTMP, razonamiento     │
│  causal, Sentinel. Variables internas que el usuario JAMÁS ve.      │
│  → NO se purga. Es infraestructura detrás del telón.                │
└───────────────────────────────┬────────────────────────────────────┘
                                ▼
┌─ CAPA 3 · FAMILIA QUIRA (los productos vendibles al GAD) ──────────┐
│  Institucional · Ciudadana · OPERACIONES · Cooperación · Impact ·   │
│  Economic. El alcalde/director del GAD los usa y/o los compra.      │
│  ⚠️ FIREWALL OBLIGATORIO: lenguaje de administración pública.        │
│  ICPI→Cumplimiento institucional · SAT→Alerta · H73→Fuente validada │
│  → SÍ se purga. El firewall aquí es un ESCUDO COMERCIAL.            │
└─────────────────────────────────────────────────────────────────────┘
```

### El hallazgo mayor: QUIRA Operaciones es VENDIBLE
La mesa trataba "Operaciones" como consola técnica interna. **Es un producto vendible al GAD.**
Si un cantón compra QUIRA Operaciones para su gestión diaria, su director **no debe ver `SAT-III` ni `H73`** —
necesita alertas, desvíos, flujos y eficiencia en lenguaje de administración pública. Ahí el firewall
deja de ser una restricción y se vuelve un **diferenciador comercial impenetrable.**

## Clasificación operativa (extensible · fuente: `scripts/dev/firewall_audit.py`)

| Capa | Archivos | Canon visible | Escáner |
|---|---|---|---|
| **Dylus Lab** | `env_ops` `p_carga` `p_ingesta` `p_reportes` `p_sentinel_hub` | ✅ legítimo | `DYLUS_LAB` (excluido de deuda) |
| **QUIRA IA** | `env_gov` (router/infra) | ✅ invisible | `QUIRA_IA` (excluido de deuda) |
| **Familia QUIRA** | el resto de `quira_pages/*` (dashboards de dominio, Centro de Mando, GeoTwin) | ❌ prohibido | cuenta como deuda |

**Criterio de clasificación (regla de decisión):**
1. ¿La gateé `is_ops()` (Operador/Admin = solo Dylus)? → **Dylus Lab.**
2. ¿Es router/motor invisible (el usuario nunca ve la variable)? → **QUIRA IA.**
3. ¿La alcanza un rol del GAD (`is_ejecutivo` o `is_tecnico`=Directivo) como producto? → **Familia QUIRA → purgar.**
   - Caso MIXTO: el *motor* (Sentinel/SAT engine) = QUIRA IA; la *vista* que ve el GAD (ej. cajón d04 `m2_alertas`) = Familia → purgar.

## Consecuencias

- **La deuda de firewall MEDIDA pasa de 154 a 119** (los 35 restantes son canon legítimo Dylus/IA, no deuda).
- El escáner `firewall_audit.py` separa `DEUDA FAMILIA QUIRA` de `canon legítimo Dylus/IA`.
- El Firewall Blitz **solo opera sobre Familia QUIRA** — purgar consolas Dylus sería trabajo perdido (migrarán al universo privado de Dylus Lab).
- Pendiente producto (decisión de Javo, no técnica): si una pantalla migra físicamente a la web/repo de Dylus Lab, sale de `quira_pages/`.

---
*ADR-027 · Tres Capas de Soberanía · Dylus Lab © 2026 · "La Familia QUIRA habla gobernanza. Dylus Lab habla metodología. QUIRA IA es la capa invisible que conecta ambos mundos."*
