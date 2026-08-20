---
id: OBS-031
authority:
  parent: ADR-042
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-19
dominio: método · verificación
estado: VERIFICADA
---

# OBS-031 · El Gold Master estaba sano; lo roto era el aparato que decía verificarlo

> Durante casi tres meses, nueve pruebas del contrato del Gold Master fallaron sin interrupción.
> La lectura inmediata era **«el Excel tiene 14 claves ausentes»**. El Excel no tenía nada. El
> verificador había migrado al canon v5.5 y **las pruebas seguían hablando v6.0**.

## La cadena de inferencia, y dónde se torcía

| Lo que decía la salida | Lo que se concluía | Lo que era |
|---|---|---|
| `Clave ausente en H73_OUTPUT_API: TGI_SCORE` ×14 | el Gold Master perdió su contrato | el **mock** sólo respondía a `G6.1_OUTPUT_API` |
| `assert 'hoja_requerida:G3.3_D3_EJECUCION_GAD'` falla | falta una hoja | esa hoja es del template v6.0, **no del canónico** |
| «v5.5 debe dar ALERTA por no ser v6» | el archivo está desactualizado | **v5.5 ES el canónico activo**; la prueba defendía una premisa derogada |

El validador (`app/services/gold_master_governance.py`) ya nombraba `H73_OUTPUT_API` y
`H82_CONFIG_PARAMS`. Las pruebas se quedaron en la nomenclatura anterior. El mock devolvía una
hoja vacía, las catorce claves salían «ausentes», y el fallo se leía como un defecto del Estado.

## La comprobación que deshizo el error

Antes de tocar nada se corrió el validador contra el **archivo real**:

```
SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx → 30 reglas · 30 OK · 0 errores · 0 alertas
```

La corrección se hizo en el aparato de prueba obsoleto. **El Estado no se tocó.**

## La regla que este caso demuestra — y que NO vive aquí

La regla quedó en el nivel normativo, **`ADR-042 §6-bis`**, y no dentro de esta observación. La
distinción la pidió el colega y es correcta:

    REGLA CANÓNICA (ADR-042 §6-bis)
          │
          └── OBS-030 y OBS-031 demuestran por qué existe

Una regla encerrada en una observación obliga a redactar doctrina nueva cada vez que el fenómeno
reaparece en otro verificador. En el ADR se aplica sola al Gold Master, al CNE, al CPCCS, al
SERCOP o a cualquier instrumento futuro:

> **Antes de atribuir un fallo al objeto observado, debe falsarse el mecanismo que produjo la
> afirmación sobre ese objeto.**

Este caso es OBS-030 aplicada un nivel más adentro. Allí el instrumento acusaba a un portal del Estado que
funcionaba; aquí el aparato de prueba acusaba al artefacto canónico que estaba intacto. **Mismo
fenómeno, distinto sujeto:** el observador se equivocaba y la culpa viajaba hacia afuera.

Protege directamente la **Regla de Oro 1** (*Excel = Estado*): sin esta regla, el camino natural
ante nueve fallos rojos es «corrijamos el Excel» — y se habría modificado un artefacto sano para
satisfacer una prueba obsoleta.

## La segunda lección, y no es menor

**Una prueba que falla siempre no protege nada.** Durante ese tiempo el contrato del Gold Master
no estaba verificado por nadie: el fallo constante se leía como ruido de fondo. Un rojo permanente
es funcionalmente idéntico a no tener prueba, con el agravante de que aparenta cobertura.

## Consecuencias

- Las 9 pruebas se realinearon al canon activo (v5.5) conservando el camino de compatibilidad v6.0,
  que el validador acepta y que también debe quedar cubierto.
- `test_version_no_v6_da_alerta` se reescribió como `test_version_fuera_del_canon_da_alerta`:
  exigía que **v5.5 alertara**, cuando v5.5 es el canónico. Defendía una premisa derogada.
- Suite completa: **433 pruebas verdes**, 1 omitida por diseño (prueba de origen · ADR-051 §7).

---
*OBS-031 · Dylus Lab © 2026 · el día que el termómetro acusó al paciente.*
