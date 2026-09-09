---
id: UNIVERSO-BUSQUEDA-D-015
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 9]
  type: REGISTRO
estado: CERRADO — universo agotado y declarado
fecha: 2026-09-09
---

# Universo de búsqueda · `D-015` — procedencia de `SITA 2025`

> **Este registro existe para que una conclusión de ausencia sea auditable.** Sin él, «no
> aparece» y «no existe» se confunden — que es exactamente el error que esta sesión cometió dos
> veces.

## Por qué se escribió

Javo, 2026-09-09:

> *«Siempre nos pasa: no se revisa, y hay documentación en todas partes y procesos creados, y no
> se lee todo. Debe revisarse todo —no importan los tokens— y no asumir nada de memoria ni
> suponer.»*

Y el registro de lo ocurrido, que es la prueba de la necesidad:

| # | conclusión emitida | universo que faltaba |
|---|---|---|
| 1 | «la capacidad documental no existe» | `worktrees`, y buscar por nombre del trabajo y no por número de dominio |
| 2 | «`0,4448` es un valor huérfano» | la **historia de git** — `git log -S` la resolvía en un comando |
| 3 | «búsqueda exhaustiva» | `_historico` y Obsidian seguían sin mirar |
| 4 | la propia prueba dio un **falso positivo** | su universo de acreditación eran sólo corridas y `PCD-D07` |

Las cuatro son la misma falla: **interpretar antes de agotar la evidencia.**

## 1 · Qué se buscaba

La procedencia de las cuatro cifras que circulan como `SITA 2025`, y en particular si existe
**algún artefacto posterior al 2026-08-20 que reproduzca `0,4448`**, el valor vigente.

## 2 · Rutas y fuentes inspeccionadas

| # | universo | método | resultado |
|---|---|---|---|
| U1 | `quira-os/` completo, **incluidos `worktrees`** | `grep -rn`, sin exclusiones de ruta | sólo las ocurrencias ya conocidas |
| U2 | **historia de git** (`--all`) | `git log -S` por cada cifra | ★ **la genealogía completa** |
| U3 | `_historico/` · 898 archivos | `grep` + OOXML + PDF | 0 |
| U4 | `ProyecT/` | `grep` + OOXML + PDF | 0 |
| U5 | `documentos_proyecto/` | `grep` + OOXML + PDF | 0 |
| U6 | `governance/` (externo al repo) | `grep` + OOXML | 0 |
| U7 | `quira-harvester/` | `grep` | 0 |
| U8 | `quiraintelligence-web/` | `grep` | 0 |
| U9 | `tesis historicas/` | `grep` + OOXML + PDF | 0 |
| U10 | `metodologia_beta_Dctos/` | `grep` + OOXML + PDF | 0 |
| U11 | Obsidian — `data/vault_backup_p2/`, `docs/corpus_obsidian/`, `vault_registry.json` | `grep` | 0 |
| U12 | **372 archivos OOXML** (`.xlsx`/`.xlsm`/`.docx`/`.pptx`) | descomprimidos como ZIP, XML interno | 0 decimales |
| U13 | **129 PDF** | `pypdf`, texto extraído íntegro | 0 |

## 3 · Términos y variantes

```
0,4646 · 0.4646 · 4646          0,4448 · 0.4448 · 4448
0,4630 · 0.4630 · 4630          0,9719 · 0.9719 · 9719
SITA (palabra completa)          RUN-D07-*
vara_sha e5f753f7…               fechas 2026-08-2* · 2026-09-*
```

En OOXML se buscó además el patrón decimal con cola (`0.44480000001`), porque Excel almacena el
valor y no su formato.

## 4 · Filtros aplicados, y su efecto

- **`SITA` como subcadena descartada.** «neceSITA», «viSITA», «depoSITA» producían 70 falsos
  positivos sólo en `_historico`. Se exigió palabra completa.
- **Enteros sueltos descartados.** `4646`/`4448` sin parte decimal aparecen 1.530 veces en los
  OOXML de `TERRA_ECIAP` — son celdas, montos e identificadores del motor histórico, no valores
  `SITA`. Sólo cuenta el patrón decimal.
- **Base64 descartado.** Las primeras coincidencias en `_historico` eran logotipos embebidos.

## 5 · Períodos cubiertos

Toda la historia del repositorio hasta `13baa49` (2026-09-09), sin corte inferior. Los artefactos
externos se inspeccionaron por contenido, sin filtrar por fecha.

## 6 · ⚠️ Qué quedó FUERA del universo, y por qué

| artefacto | motivo |
|---|---|
| **21 PDF sin capa de texto** (de 129) | actas de audiencia **escaneadas**; requieren OCR. Son las mismas que `app/agents/d08/fuentes.py` declara. **No se afirma nada sobre su contenido** |
| `~$TERRA…xlsx` · `~$SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx` | ficheros temporales de bloqueo de Excel (prefijo `~$`), no documentos |
| `Tecnic_SOLO_CONTIENE_API_KEY_GEMINI/` | **excluido deliberadamente**: contiene credenciales y no se inspecciona |
| Supabase · Neo4j | almacenes remotos; no se consultaron en este barrido |

Que un artefacto quede fuera **no autoriza a afirmar que no contiene lo buscado**. Estos cuatro
grupos son el margen declarado de esta búsqueda.

## 7 · Resultado

**No existe ningún artefacto —en ninguno de los trece universos inspeccionados— posterior al
2026-08-20 que reproduzca `0,4448`.** Tampoco aparece ninguna corrida que produzca `0,4646` fuera
de las citas de `PCD-D07` y de la propia historia de git.

La única fuente que acredita el valor vigente es **la genealogía del repositorio**: el commit
`76ca5de` (2026-08-20), que documenta la transformación `0,4646 → 0,4448` al acreditar `enlaces`
e `inventario`, con el movimiento de `CI` (0,4792 → 0,4000) y su razón — *«la medición anterior
contaba como bueno lo que nunca se había mirado»*.

## 8 · Conclusión autorizada

> `0,4448` es el valor **vigente** de `SITA 2025`, con **procedencia documental y de cambio
> demostrada**, y **sin reproducción computacional preservada**. Las corridas de
> `data/d07/corridas/` son todas del 2026-08-18 y nunca se regeneraron tras la acreditación del
> 20-ago.

Lo que **no** se concluye, por no estar demostrado:

- que `0,4646` carezca de corrida propia — pudo existir y no conservarse
- que los 21 PDF escaneados no contengan nada pertinente
- que `0,4630` sea equivalente a `0,4646`: son cifras distintas y su diferencia sigue sin
  explicarse

## 9 · Lo que habilita

La condición que la dirección fijó —*«si no aparece un artefacto posterior al 20-08 que reproduzca
`0,4448`, entonces sí regenerar»*— **se cumple**. Queda habilitada, a la espera de autorización
explícita:

```
regenerar corrida 2025 → preservar JSON → SHA → registrar run
                       → comprobar reproducción → cerrar D-015
```

Y la cadena que eso dejaría, que es la que faltaba:

> **cambio acreditado → ejecución reproducible → artefacto sellado → valor reproducible**

⛔ `PCD-D07` **no se edita** para ponerlo al día. Se registra que quedó desfasado respecto de
`76ca5de` y su tratamiento lo decide la gobernanza documental. Está bajo preservación
(`REARQ-001`).

---
*Registro de universo de búsqueda · `D-015` · 13 universos · 372 OOXML · 129 PDF · 4 grupos
declarados fuera · Dylus Lab © 2026*
