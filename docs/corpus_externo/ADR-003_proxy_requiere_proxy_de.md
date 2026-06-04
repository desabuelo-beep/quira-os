# ADR-003 — Todo valor proxy requiere declarar proxy_de

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

Varios indicadores de QUIRA no tienen datos primarios disponibles (microdatos INEC parroquiales, cédulas específicas, etc.). Durante Alpha, se usaron proxies: valores zonales donde se necesitaban parroquiales, estimaciones donde se necesitaban mediciones directas.

El riesgo es que un proxy sin documentación de origen se convierta en "dato" por inercia. En 6 meses, nadie recuerda que era una estimación.

## Decisión

**Ningún valor proxy puede existir en QUIRA sin el campo `proxy_de` declarado.**

En QTMP schema v1.1:
```yaml
proxy_de:
  fuente_original: [nombre del dato que se está aproximando]
  metodo: [cómo se calculó el proxy]
  precision_estimada: [alta / media / baja]
  validez: [provisional / permanente]
  notas: [contexto adicional]
```

El estado `proxy_aprobado` en `estado_dato` es válido, pero solo cuando `proxy_de` está completo.

Un dato con `estado_dato: proxy_aprobado` y sin `proxy_de` es un error de schema.

## Consecuencias

- Los proxies NBI parroquiales de Montecristi están documentados como `pendiente_microdato` (BETA-TERRITORIO-001)
- El PMV no puede mostrar un proxy como dato confirmado sin advertencia visible
- La Red Académica puede validar los proxies convirtiéndolos de `proxy_aprobado` a `validado_academico`

## Principio subyacente

> La certeza no es requisito para operar. La honestidad sobre la incertidumbre sí lo es.
> — QUIRA Data Governance v1.0, Principio 4
