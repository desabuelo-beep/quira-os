---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-013 — Mapeo Canónico QTMP → 12 Dominios del Centro de Mando

**Estado:** Aceptado  
**Fecha:** 2026-05-31  
**Autores:** Dylus Lab — Director + Advisor  
**Vigencia:** Permanente — cambiar requiere nuevo ADR

---

## Contexto

Los tres circuitos QTMP cargados en Neo4j `quira-alpha` usan la nomenclatura
del framework TGI de 5 dimensiones (D1-D5: Legalidad, Planificación, Holding,
Equidad, Capacidad). Esa nomenclatura NO corresponde a los 12 dominios
canónicos del Centro de Mando (D01-D12 inmutables). Sin un mapeo explícito,
cada sesión de desarrollo podría asociar un circuito a un dominio distinto,
rompiendo la coherencia del panel estratégico.

## Decisión

Quedan congelados los siguientes mapeos:

| Circuito QTMP  | Dominio canónico | Nombre dominio                         | Módulo Streamlit  |
|----------------|------------------|----------------------------------------|-------------------|
| `GAP_10PCT`    | **Dom12**        | Protección Social & Grupos Prioritarios | `p19_genero.py`   |
| `AGUA_POTABLE` | **Dom10**        | Territorio & Cobertura                 | `p4_geotwin.py`   |
| `EQUIDAD`      | **Dom06**        | Salud Institucional                    | `m1_situacion.py` |

### Nodo de entrada canónico por circuito

| Circuito       | Norma base    | Artículo | Resultado confirmado      | Semáforo  |
|----------------|---------------|----------|---------------------------|-----------|
| `GAP_10PCT`    | COOTAD        | 249      | Ti_Patronato = 50 %       | 🔴 ROJO   |
| `AGUA_POTABLE` | Constitución  | 264      | Cobertura red = 34.9 %    | 🔴 ROJO   |
| `EQUIDAD`      | COOTAD        | 228      | IRS cantonal = 79.7 %     | 🟡 AMARILLO |

## Racional

**GAP_10PCT → Dom12:** El circuito mide la paradoja COOTAD Art. 249
(asignación formal 20.84% cumple el piso legal; ejecución Patronato 50% no
llega al territorio). Dom12 es el dominio de Protección Social — exactamente
la audiencia que recibe o no recibe esa inversión no ejecutada.

**AGUA_POTABLE → Dom10:** La cobertura de agua potable (34.9 %) y la
continuidad del servicio (0 % de zonas con agua 24/7) son indicadores
territoriales directos. Dom10 es Territorio & Cobertura.

**EQUIDAD → Dom06:** La distribución territorial de la inversión municipal
(IRS 79.7 %, brecha NBI 32 pp) refleja la salud institucional del GAD en
relación a sus obligaciones de equidad. Dom06 es el dominio de Salud
Institucional — la capacidad del municipio de cumplir sus obligaciones
distributivas de forma sostenida.

## Consecuencias

1. El conector `app/connectors/neo4j_qtmp.py` implementa esta tabla como
   constante `CIRCUIT_DOMAIN_MAP` — es la única fuente de verdad en código.

2. En Sprint 3 Panel Estratégico solo se conectan a Neo4j los módulos
   `p19_genero.py` (Dom12), `p4_geotwin.py` (Dom10) y `m1_situacion.py` (Dom06).
   Los otros 9 cajones muestran estado "En Modelado" hasta que exista QTMP.

3. El `dominio_tgi` en los nodos Neo4j (`Dom04`, `Dom02`, etc.) corresponde
   al framework TGI de 5 dimensiones — NO a los 12 dominios canónicos.
   La conversión canónica es este ADR. Los scripts de carga NO se modifican.

4. El campo `fuente_neo4j: bool` en la respuesta del conector indica si el
   dato viene del grafo (True) o del fallback embebido (False). La UI no
   muestra este campo al usuario.

## Prohibiciones derivadas

- NUNCA exponer en la UI los IDs internos: `GAP_10PCT`, `AGUA_POTABLE`,
  `EQUIDAD`, `SP_G10P_MCR`, `RES_G10P_04_MCR`, `IND_AGPT_01_MCR`, etc.
- NUNCA mostrar la nomenclatura TGI D1-D5 al usuario final.
- NUNCA modificar el mapeo sin crear un nuevo ADR.

---

## Corrigendum — 2026-06-01 (Sprint 3)

Dos correcciones aplicadas al código durante Sprint 3. El mapeo de dominio no cambia — solo los nombres de módulo Streamlit y la adición de un cuarto circuito:

**1. AGUA_POTABLE módulo corregido:**
- Versión original: `p4_geotwin.py` (error tipográfico de sesión anterior)
- Versión correcta: `p10_territorio.py` (implementado y verificado en Sprint 3)

**2. TRANSPARENCIA añadido:**
El cuarto circuito QTMP fue materializado en Sprint 3 y registrado en `CIRCUIT_DOMAIN_MAP`:

| Circuito QTMP | Dominio | Nombre dominio | Módulo Streamlit |
|---------------|---------|----------------|------------------|
| `TRANSPARENCIA` | Dom07 | Transparencia | placeholder `municipal` hasta Sprint 4 |

La tabla completa y vigente de `CIRCUIT_DOMAIN_MAP` está en `app/connectors/neo4j_qtmp.py`. Este ADR es el registro jurídico-arquitectónico; el código es la fuente de verdad operativa.

La decisión de cuándo y en qué orden se cierran los dominios pendientes está en **ADR-014**.

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"La pantalla sigue al grafo. Nunca al revés."*
