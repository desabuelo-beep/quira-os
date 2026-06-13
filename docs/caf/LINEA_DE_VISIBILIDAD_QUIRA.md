# LÍNEA DE VISIBILIDAD QUIRA — qué se muestra y qué se protege
**Dylus Lab © 2026 · consolidada 2026-06-12 (consulta Javo)**

> Unifica las TRES capas de visibilidad que antes estaban dispersas (Bloomberg
> Firewall en código · estrategia IP en docs/caf · Open Core en Hoja de Ruta).
> **Regla de oro:** se muestra QUÉ hace y QUÉ sale (lenguaje de gobernanza);
> se oculta CÓMO lo calcula. Aplica a CAF, equipos, prensa, competidores.

---

| Capa | ✅ VISIBLE (mostrable / público) | 🔒 CAJA NEGRA (propietario) |
|---|---|---|
| **Metodología** | Marco conceptual · dominios canónicos · principios de diseño · QUÉ mide | Fórmulas de ponderación · ACK profundo · ontología operativa |
| **Motor** | Que existe un "motor de indicadores" + sus salidas en lenguaje de gobernanza | Gold Master (Excel) · SIAP-ICPI · H-codes · motor narrativo · algoritmo de matching |
| **Producto / UI** | Las pantallas finales · los 6 productos · el caso Montecristi | Nomenclatura interna (ICPI · TGI · SAT · Dom07 · CE_xxx) = **Bloomberg Firewall** |
| **Datos** | Resultados · fichas · GeoTwin · narrativas (Bloomberg-safe) | Credenciales · node IDs · MNT_UUID · estructura interna de la BD |
| **Código** | *(futuro)* metodología/taxonomía como estándar abierto — **DIFERIDO a tracción** | repo `quira-os` · fetchers · conectores · motor de inferencia |

---

## Las tres capas, explicadas

1. **Visibilidad de PRODUCTO (Bloomberg Firewall — ya operativo en código):**
   qué términos aparecen en la UI. Nunca: ICPI, TGI, SAT, QTMP, H01-H99, Gold
   Master, node IDs. Solo lenguaje de gobernanza pública.

2. **Visibilidad de IP / NEGOCIO (ante CAF, equipos, terceros):**
   ante el diplomado y cualquier tercero se muestra arquitectura conceptual,
   pantallas y caso Montecristi. Se oculta: Excel, fórmulas, repo, credenciales,
   instancia Neo4j. El motor es una "caja negra": ven qué entra (PDOT) y qué
   sale (Centro de Mando), no las entrañas. (Fuente: `CAF_proyecto_equipos_IP.md`.)

3. **Visibilidad de ESTÁNDAR (Open Core — estrategia futura):**
   se ABRE la metodología (White Paper, taxonomía) para posicionar como estándar
   regional. Se mantiene CERRADO el motor (ACK, Gold Master, narrativo, matching,
   radar). La apertura formal del código está DIFERIDA hasta tener tracción
   (varios cantones). Abrir antes regala la ventaja sin cobrar el efecto de red.

---

## La frase para recordar

> **Mostramos QUÉ hace y QUÉ revela. Ocultamos CÓMO lo calcula.**
> El conocimiento (corpus, metodología, grafo) puede ser visible y hasta abierto.
> El motor de cálculo (Gold Master, fórmulas, ACK profundo) nunca sale de Dylus.

---

*Línea de Visibilidad QUIRA · Dylus Lab © 2026 · referenciada por White Paper, Hoja de Ruta y estrategia CAF.*
