# Release Checklist · BRN v2.1 — criterio de salida hacia testers

> **Qué es.** El criterio **oficial y verificable** para declarar que los dominios construidos están
> listos para pruebas con usuarios (propuesta del colega · 2026-07-20). No es una impresión: cada
> línea tiene evidencia reproducible. Se re-ejecuta antes de cada liberación.
>
> **Regla de Javo (2026-07-20):** la construcción debe estar **completa** antes de los testers. Las
> versiones siguientes nacen de **las observaciones de los testers**, no de cosas que dejamos a medias.

**Fecha de verificación:** 2026-07-20 · **Alcance:** d01 · d02 · d03 · d09 (los 4 DOM construidos)

## Checklist

| # | Verificación | Estado | Evidencia |
|---|---|---|---|
| 1 | Suite arquitectónica + semántica | ✅ **12/12** | `python scripts/test_brn_arquitectura.py` |
| 2 | Infrastructure diff = 0 | ✅ | check 12 contra `brn-v2.1` |
| 3 | Todos los SHA verificados contra el corpus | ✅ **4 CNO íntegras** (9+6+10+9 eslabones) | `python scripts/brn_cno.py` |
| 4 | Estados de gobernanza coherentes | ✅ **9/9 vigentes** con `validada_por: Javo` y fecha | inspección de `docs/brn/*.yaml` |
| 5 | Ninguna inferencia no sustentada | ✅ **1 hallazgo corregido** | ver §Hallazgos |
| 6 | Terminología consistente (Bloomberg Firewall) | ✅ **0 leaks en UI** | barrido de jerga en los 4 renders |
| 7 | Lenguaje no acusatorio | ✅ limpio | barrido `incumplió/violó/ilegal/irregular` |
| 8 | Documentación sincronizada | ✅ | matriz, plano maestro, molde y BOOT al día |
| 9 | Deudas conocidas registradas | ✅ | ver §Deudas |
| 10 | Cambios pendientes identificados para v3 | ✅ | matriz §Evolución prevista |

## Hallazgos del repaso de cierre (y su corrección)
| DOM | Hallazgo | Acción |
|---|---|---|
| **d09** | `LOPC Art. 88` citado en la UI **no existe en el corpus** (3 ocurrencias) — violaba la Regla 3 | Corregido a **LOPC Art. 89** (Definición de rendición de cuentas · SHA `d3e1686814de`), que es el fundamento real y ya está en CNO-IX-001 |
| d01·d02·d03 | citas de artículo revisadas contra las cadenas verificadas | Sin hallazgos — COOTAD 215/233, LOSNCP 22, COPLAFIP 41/42, COD 97 coinciden con sus CNO |
| todos | jerga interna en UI | Sin leaks: las 3 coincidencias eran docstrings de código, no texto de producto |
| d09 | afirmaciones categóricas (el patrón que produjo la inferencia de d02) | Sin hallazgos |

*Nota: d09 no había sido auditado en la revisión del 2026-07-18; este repaso lo cubre.*

## Deudas conocidas — **limitaciones de diseño, no defectos funcionales**
Distinción del colega (2026-07-20), que se mantiene explícita ante los testers:
> **Bug:** el sistema calcula mal. · **Limitación:** el modelo aún no representa algo con toda la
> riqueza conceptual deseable. **Son categorías distintas.**

| Deuda | Naturaleza | Por qué no se resuelve antes de testers |
|---|---|---|
| `metrica.tipo` (porcentaje/booleana/ordinal/cardinal) | **Limitación de diseño** | Está documentada; no rompe el contrato; **no produce resultados incorrectos**; solo limita expresividad. Resolverla exige tocar contrato, adaptador y compilador → BRN v3 con ADR. Hacerlo ahora sería evolución *preventiva*; hacerlo después será evolución *respaldada por evidencia de uso*. |
| ROAdapter → parser formal | Mejora de diagnóstico | No afecta resultados; mejora la expresividad de los errores. Candidato v2.2/v3. |

## Secuencia acordada
```
Promoción formal d01 ✅ → repaso transversal de los 4 DOM ✅ → checklist de liberación ✅
   → congelamiento → TESTERS → recoger evidencia → decidir si `metrica.tipo` justifica BRN v3
```
Este orden minimiza retrabajo: cualquier evolución posterior queda respaldada por **evidencia de uso
real**, no por anticipación de necesidades.

---
*Release Checklist BRN v2.1 · Dylus Lab © 2026 · "Listo para testers no es una impresión: es un checklist que se vuelve a correr y da verde."*
