# GEOTWIN 3D — ESPECIFICACIÓN DE DIRECTOR
**QUIRA OS · 2026-06-12 · eleva `GEOTWIN_3D_origen_Javo.md` a spec ejecutable**

## DEFINICIÓN CANÓNICA (Javo — inmutable)
> **GEOTWIN NO ES UN DOMINIO. Es una CAPA COMPLETA de QUIRA**: lleva todos los
> dominios y sus dashboards y los conecta con el territorio real. Es donde
> aterrizan las políticas públicas, planes, programas y proyectos; donde se ven
> las asimetrías e inequidades territoriales con barrios, sectores, parroquias
> y densidad poblacional.

Principio rector: **el 3D en gestión pública no es estética, es evidencia.**

## LO QUE YA EXISTE (no reconstruir)
- Motor narrativo validado (`app/engines/geotwin_narrativo.py`): explicar_parroquia()
  + 3 casos en runtime — **los 3 casos = las 3 vistas narrativas del 3D**:
  | Vista 3D (doc origen) | Caso del motor YA validado |
  |---|---|
  | La Brecha Territorial (prismas per cápita) | Caso 1 Isabel Muentes + Caso 3 urbano-rural |
  | Anatomía del Riesgo (pendientes + asentamientos) | Caso 2 Riesgo (82.28% masa · 48,399 ha incendios) |
  | Materialización El Aromo (estado real vs anuncios) | G-27 estado de materialización |
- Mapa Folium 2D operativo (p4_geotwin) + geojson 7 parroquias + clic→explicación (F1 ✅)
- pdot_indicadores: 2,004 (27 PUGS polígonos + 408 riesgos territorializados)

## DECISIONES TÉCNICAS (director)
1. **Stack v1 = PyDeck** ($0, nativo Streamlit, extrusión por atributo). Mapbox GL
   (fly-tos cinematográficos) = fase 2 cuando haya demo CAF/inversores.
2. **DEM gratuito**: NASA SRTM 30m o ALOS PALSAR 12.5m → recorte cantonal → simplify.
3. **Regla Thumbnail (blindaje rendimiento)**: la pantalla principal JAMÁS carga el
   motor 3D — SVG estático; el 3D despierta solo al entrar a la capa.
4. **PostGIS en Supabase** para geometrías (tier free alcanza para v1).
5. **Extrusión**: PUGS edificabilidad/uso (los polígonos finos requieren el PUGS
   narrativo = 1,254 chunks pendientes de créditos API — mientras: extrusión por
   indicadores ya cargados: agua/saneamiento/NBI/inversión per cápita).

## ROADMAP G3D (incorporado a HOJA_RUTA_2026)
- **G3D.1** Datos: DEM descarga + recorte + polígonos parroquiales con atributos
  desde pdot_indicadores → PostGIS. ($0)
- **G3D.2** PyDeck v1: vista "La Brecha Territorial" (prismas inversión/agua por
  parroquia sobre relieve) emb