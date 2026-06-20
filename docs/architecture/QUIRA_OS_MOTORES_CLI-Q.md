# QUIRA OS · Inventario de Motores + Hoja de Ruta CLI-Q (Sprint E)

**2026-06-20 · captura de mesa (Javo + colega + académico) · post-Firewall Blitz (deuda 119→0)**
**Relacionado:** ADR-028 (Compilador + CID) · ADR-027 (3 capas) · ADR-023 (3 niveles) · `scripts/dev/firewall_dictionary.json`

> **El reframe:** QUIRA dejó de ser "el Excel". El Excel es un **origen** del conocimiento, no el
> sistema. QUIRA OS = la **orquestación** de varios motores, cada uno dueño de UNA verdad.

## Los motores y su frontera de verdad (qué hace cada uno · qué NO hace)

| Motor | Tecnología | Frontera de verdad (lo único que dictamina) | NO hace |
|---|---|---|---|
| **Analítico** | Gold Master (Excel SIAP-ICPI v6.0) | la **causalidad administrativa** — el número (ICPI/TGI/SAT/holding). H12!B33 inmutable. | no ingiere, no explica, no expone |
| **Operacional** | Supabase / PostgreSQL | el **hecho observado** — evidencia cruda del territorio (SERCOP, NBI/PUGS/INEC, snapshots) | no calcula índices |
| **Causal** | Neo4j (capa QUIRA IA) | la **doctrina** — la cadena Promesa→…→Territorio y las 4 congruencias (dónde se corta el eslabón) | no promedia |
| **Semántico** | Graphify (AST + comunidades) | la **estructura** — dependencias, ADRs, axiomas de diseño (auditor de IP) | no opera sobre datos vivos |
| **Inferencial** | CLI-Q / LLM en CID (Dylus Lab) | la **exposición** — traduce canon→idioma de salida (público/académico/…) | jamás inventa el dato (Regla 1) |
| **Visual** | Streamlit / GeoTwin | la **presentación** — sólo visualiza, no calcula (ADR-023 Nivel 3) | no es fuente de verdad |

**El orden de dependencia (arquitectura de compilador):**
```
Gold Master (causalidad)  →  Motor canónico  →  Compilador CLI-Q (firewall)
                                                        │
                                       ┌────────────────┼────────────────┐
                                       ▼                ▼                ▼
                                   Público          Académico        Financiero  …
                              (el motor nunca cambia; cambia sólo el backend de salida)
```

## Hoja de Ruta — Sprint E: Industrialización del CID (CLI-Q Compiler)

La cacería manual de strings **terminó** (superficie pública al 100% limpia). El próximo vuelo NO abre
módulos nuevos: construye el compilador que vuelve el Blitz un comando reproducible.

- **Fase 1 — Diccionario Soberano** ✅ `scripts/dev/firewall_dictionary.json` (este commit).
  20 índices + motor + infra + node-IDs, extraídos de la tabla `PROHIBITED` (fuente única). Estructura
  multi-backend (`publico` hoy; `academico/juridico/financiero` mañana = claves paralelas).
- **Fase 2 — Bucle Determinista (CID)** ⛏️ Agente Python: `scan → leer diccionario → patch → verificar AST → git commit`.
  Memoria estructurada (`estado.json`, no conversacional) · escaneo por-archivo O(1) · Haiku + `task_budget`.
  *Prerrequisitos:* (a) `firewall_audit.py` acepta un archivo; (b) modo `--suggest` (emite el `alt`); (c) modo `--fix` (transform).
  **Vive SÓLO en Dylus Lab** — nunca en el cliente (ADR-028).
- **Fase 3 — Multi-backend de salida** ⛏️ `quira firewall --backend <publico|academico|financiero|…>`. Un motor, N idiomas.

## Pendiente antes de escalar (prioridad del colega)
**Inventario de capacidades a nivel código**, no de archivos: ¿qué consulta hoy el LLM y qué no? ¿qué es
fuente de verdad vs sólo visualización? Verificar cada motor contra su frontera declarada arriba.
*(Candidato: correr graphify sobre `app/connectors/` para mapear el cableado real entre motores.)*

---
*QUIRA OS · Inventario de Motores · Dylus Lab © 2026 · "Ya no limpiamos código; compilamos lenguajes institucionales. El motor produce la verdad; el compilador la traduce a N idiomas sin tocarla."*
