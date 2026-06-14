# GEOTWIN — PLAN DE IMPLEMENTACIÓN Y EVOLUCIÓN
**Dylus Lab © 2026 · consolidado 2026-06-13 · capa territorial transversal**

> Reframe del Director (corrección Javo + colega 2026-06-13): GeoTwin 3D NO es
> "futuro/fantasía". Es una **capacidad DISEÑADA y DOCUMENTADA, con arquitectura
> de costo ~$0, cuya implementación está DIFERIDA** hasta consolidar la Fundación
> Ontológica y reconstruir los dominios. No es promesa de marketing — es una fase
> posterior de ejecución, ya planificada.

## LA EVOLUCIÓN DE GEOTWIN (3 versiones · hoja de ruta propia)

```
GeoTwin v1 · TERRITORIALIZA   "¿dónde ocurre?"   ← parcial HOY
  Folium 2D · GeoJSON centroides · motor narrativo F1 (clic parroquia → explica)
  Pendiente v1-completo: botón "Ver en Territorio" por cajón + mapa que muta por dominio
  Costo: ~$0

GeoTwin v2 · VISUALIZA 3D      "el relieve real"  ← DIFERIDO (diseñado)
  DEM NASA SRTM · polígonos PUGS · PostGIS · extrusión PyDeck · prismas
  Costo: ~$0 (stack abierto)

GeoTwin v3 · PREDICE           "¿qué ocurrirá?"   ← DIFERIDO (visión, con tracción)
  Series temporales + infraestructura + presupuesto + riesgo climático + IA
  El verdadero gemelo digital predictivo
```

Secuencia: **primero territorializa, después visualiza en 3D, finalmente predice.**

---

## STACK DE COSTO CERO ($0 licencias e infraestructura)

| Fase | Herramienta | Licencia | Propósito |
|---|---|---|---|
| 1. Captura DEM | NASA Earthdata / USGS (SRTM 30m / ALOS 12.5m) | datos públicos | relieve real del Cerro de Montecristi |
| 2. Procesamiento | QGIS + Python (geopandas) | Open Source GPL | recorte + simplificación de polígonos PUGS |
| 3. Almacenamiento | Supabase + extensión PostGIS | free tier | base espacial + índices GIST (microsegundos) |
| 4. Conectividad IA | Claude Code + Postgres MCP (+ QGIS MCP) | open protocol | consultas espaciales en lenguaje natural |
| 5. Renderizado 3D | Streamlit + PyDeck (WebGL) | Open Source Apache | extrusión volumétrica en navegador |

**Elimina el argumento de venta de ArcGIS Enterprise / Mapbox Premium / Cesium
comercial.** La narrativa pasa de "necesitamos presupuesto" a "necesitamos
madurez institucional para desplegarlo".

## PASO A PASO TÉCNICO (para cuando se active v2)

1. **DEM gratis:** descargar GeoTIFF de NASA SRTM / ALOS PALSAR del cuadrante Montecristi.
2. **Regla anti-lag (Python):** cruzar PUGS × elevación + simplificación radical:
   `gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.0005, preserve_topology=True)`
   (reduce nodos ~80% manteniendo precisión visual).
3. **PostGIS en Supabase:** activar extensión `postgis` (free tier) + índices `GIST`
   → colisión geográfica (ej. vulnerabilidad ∩ Isabel Muentes) en <5 ms.
4. **Puente IA (MCP):** Claude vía Postgres MCP escribe/ejecuta `ST_Intersects`,
   `ST_AsGeoJSON` directo en las tablas — el equipo no escribe queries espaciales a mano.
   (QGIS MCP para que el Director manipule capas geoespacialmente.)
5. **PyDeck in-place:** mapa base CartoDB Dark Matter (sin token Mapbox). El mapa
   se alimenta del indicador real (Cumplimiento Institucional). Dominio en rojo →
   gradiente translúcido `#EF4444` sobre los polígonos afectados.

## REGLA DE RENDIMIENTO (ya canónica)
La pantalla principal NO carga el motor 3D. Thumbnail SVG estático en la tarjeta;
PyDeck despierta solo al clic in-place (cero scroll, latencia mínima).

---

## DEPENDENCIAS PARA ACTIVAR v2 (lo que falta, honesto)
- PUGS de Montecristi en polígonos (hoy: dentro del PDOT como texto · 370 chunks ·
  + GeoJSON de centroides, no polígonos). Falta digitalizar/obtener shapefiles.
- DEM descargado (NASA — gratis, no hecho aún).
- Extensión PostGIS activada en Supabase + tablas espaciales.
- Disparador: tras consolidar Fundación Ontológica + reconstruir dominios.

---

*GeoTwin Plan de Implementación · Dylus Lab © 2026 · capacidad diseñada, diferida — no fantasía.*
