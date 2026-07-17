# PROTOCOLO · Curación del Corpus Jurídico → BRN (Javo · 2026-07-17)

**Estado:** vigente · procedimiento operativo · complementa ADR-038 (BRN) y ADR-005 (corpus).
**Fin:** poblar y mantener el **Corpus Jurídico Nacional** (Nivel 0) con la norma que genera
obligación operativa para los GAD, como fuente verificable (SHA256) de las CNO de la BRN.

---

## El canon legal ya existe (decisión de Javo · 2026-07-17)

**La normativa más importante inherente a los GAD YA está en el canon.** No se depende de ningún
proveedor externo. Dos fuentes reales, ambas de Javo:
- **Supabase** · `normativa_corpus` — 12.992 chunks vectorizados con SHA256 (la fuente viva que
  consulta el sistema).
- **`ProyecT/Normativa_Word/`** · 43 documentos `.docx` — el respaldo documental íntegro: COOTAD
  (+ reforma 2026), COPFP, Constitución, Código de la Democracia, LOPC, LOTAIP (+ reglamentos),
  COA, LOSEP, LOTUGS, Ley de la Contraloría, PDOT Montecristi, Plan Nacional 2025-2029, etc.

**La ampliación es de 2ª fase**, cuando arranque el Municipio 002 con QUIRA Operaciones. Para
Montecristi (Municipio 001), el corpus está **completo para operar**.

## El proceso NO depende de una fuente (precisión del colega)

La BRN depende del **Corpus**; el Corpus depende del **proceso de curación** — no de un proveedor.
El **puente no es una persona ni una herramienta: es el proceso.** Hoy es manual (Javo cura),
mañana parcialmente automatizable. Si cualquier fuente desaparece, QUIRA sigue igual.

```
FUENTE (Word oficial · Registro Oficial · portales SRI/Finanzas/Contraloría/SERCOP/CNE …)
   → Extracción → Verificación → CURACIÓN (Javo) → CORPUS (Supabase · SHA256) → BRN (CNO + RO)
```

## El flujo de ampliación (cuando falte una norma)

```
[ Claude ]                    [ Javo ]                         [ Claude ]
 MAPEA qué norma falta   ➔    la consigue y la convierte  ➔    ingesta al corpus (SHA),
 para una regla o dominio     a .docx en Normativa_Word/       propone la CNO + RO
```

1. **Claude MAPEA** — al construir una CNO, detecta qué eslabón normativo no está en el corpus y
   nombra exactamente la norma/artículo que falta (no "busca en internet": señala el hueco).
2. **Javo consigue y convierte** — obtiene el texto oficial y lo deja como `.docx` en
   `ProyecT/Normativa_Word/`. Esa es la única puerta de entrada al canon.
3. **Claude ingesta y propone** — vectoriza el `.docx` al corpus con su SHA (infraestructura
   existente: `scripts/normativa/ingest.py` · `chunker.py` · `manifest.py`), y con la cadena ya
   completa **propone** la CNO (Nivel 1) y la Regla Operativa (Nivel 2), en estado `propuesta`.
4. **Javo valida** → la CNO/RO pasa a `vigente` (ADR-035 §5 · ADR-038). Ninguna entra sin su firma.

## Líneas rojas (heredadas del canon)
- **La verdad es el SHA del Corpus.** Todo eslabón vive en Supabase con su huella; nada "queda
  fuera". Si no está en el corpus verificado, no sostiene una CNO (Regla 3).
- **La fuente aporta EVIDENCIA (texto); QUIRA construye la CADENA** — es decisión metodológica del
  proyecto, no del proveedor (soberanía metodológica · colega 2026-07-17).
- **La IA propone, Javo valida** (ADR-035 §5). Ninguna regla se declara vigente sin su firma.
- **Se cura por eje jurídico, no por volumen.** Se empieza por **Finanzas Públicas Municipales**
  (el eje del 65%), que ya está en el corpus.

---
*Protocolo de Curación del Corpus · Dylus Lab © 2026 · "El canon no depende de ninguna fuente: depende del proceso de curación. La fuente da texto; QUIRA da la cadena; Javo da la firma. Cámbiese la fuente y QUIRA no se entera."*
