# PLANO DE CAJONES — Conceptualización + Cosecha (Capa 2)
**Sprint C · 2026-06-13 · PROPUESTA para co-crear cajón por cajón**

## EL MÉTODO DE COSECHA (Javo 2026-06-13)

> Las ~40 pantallas existentes NO son "vivas vs muertas para descartar".
> Son una **CANTERA de piezas reutilizables**. El refactor NO es pantalla por
> pantalla — es **por CAJÓN**:
>
> 1. **NOMBRE** (Tabla de Equivalencias) + **CONCEPTO robusto** (qué ES el
>    dominio · potente · que incite a abrir) + **DATA CENTRAL** (el indicador madre).
> 2. Eso DEFINE qué dashboard(s) necesita el cajón (1 o N · según su naturaleza).
> 3. **PLANO DE COSECHA**: qué piezas de entre las 40 pantallas alimentan cada dashboard.
> 4. Ensamblar reciclando + aplicar Tabla de Equivalencias + datos vivos (Excel/MMP/Supabase).
>
> El concepto del cajón es el IMÁN que atrae las piezas. Sin concepto definido,
> no se sabe qué cosechar. Por eso: conceptualizar PRIMERO, cosechar DESPUÉS.
> (Por esto los muertos se archivan, no se borran: son cantera.)

## REGLA QUIRA (colega + Javo · 2026-06-13 · arquitectónica, permanente)

> **Ningún dashboard nace desde una pantalla existente. Todo dashboard nace
> desde un dominio conceptual. Las pantallas existentes son ÚNICAMENTE fuente
> de cosecha.**

Evita el envejecimiento clásico (pantalla vieja → parche → pantalla nueva →
parche → 80 pantallas). El conocimiento de una pantalla importa aunque la
pantalla esté archivada; lo que NO se hace es "partir de la pantalla".

## PRINCIPIO DE FRONTERAS Y CONEXIÓN (Javo · 2026-06-13)

> Fronteras claras ARRIBA, conexión profunda ABAJO. Como los órganos del cuerpo.

- **ARRIBA (UX) — FRONTERAS CLARAS:** cada cajón es autónomo en su gestión —
  propósito, pregunta, decisión y data central propios. El usuario nunca
  confunde un cajón con otro. Cada ADN incluye un campo "qué NO es" para
  marcar la frontera.
- **ABAJO (motor) — CONEXIÓN:** todos los cajones son vistas de UN motor único
  (Gold Master + grafo + 2.004 indicadores). La conexión real vive aquí.
- **TRANSVERSAL (GeoTwin) — CONVERGENCIA:** todas las brechas de todos los
  cajones aterrizan en el mapa territorial. GeoTwin es la superficie común.

Respuesta a la duda de Javo ("¿a partir de GeoTwin o antes?"): AMBOS — la
conexión se teje en el motor (abajo) y se expresa en GeoTwin (transversal).

---

## LOS 12 CAJONES — plano maestro

*Data central = objetiva (del sistema, ya conocida). Cosecha = pantallas que
aportan piezas (incluye archivadas = cantera). **Concepto = a CO-CREAR con Javo**
— debe ser potente/contundente, no lo invento solo.*

| # | Cajón (nombre público) | Data central (indicador madre) | Cosecha candidata (de las 40) | Dashboards est. |
|---|---|---|---|---|
| 01 | Planificación Estratégica | Avance de metas PDOT (4 ejes) | p11_ods · p8_metas · m4_analisis | 1-2 |
| 02 | Presupuesto & Financiamiento | $ en juego + elegibilidad (radar D02) | p18_cooperacion · radar fondos | 1-2 |
| 03 | Metas PDOT · Mandato | Cumplimiento del plan de campaña (IFE-A) | p8_metas · p_concejo (promesas CNE) | 1 |
| 04 | Alertas Institucionales | Alertas activas (Sistema de Alerta Temprana) | m2_alertas · p9_sat · p_alertas | 1 |
| 05 | Holding / Ecosistema Municipal | Promedio 4 entidades | m3_municipal · p2_holding | 1 |
| 06 | Salud Institucional | Cumplimiento Institucional (índice madre) | m1_situacion · p6_pulso · p1_dashboard · p14_eficiencia · ⚰️p_ejecutivo · ⚰️p0_inicio | 1-2 |
| 07 | Transparencia | Transparencia activa (LOTAIP 21/21) | p07_transparencia · ⚰️p15_transparencia | 1 |
| 08 | Participación Ciudadana | Participación / gobernanza participativa | p16_confianza · p16_gobernanza | 1 |
| 09 | Rendición de Cuentas | Días + estado circuito rendición (C-RDC live) | p17_rdc | 1 |
| 10 | Territorio & Cobertura | Cobertura de servicios por parroquia + GeoTwin | p10_territorio · p4_geotwin · p7_brecha · p10_inversion | 2 (tabla + mapa) |
| 11 | Ecosistema Productivo Territorial | (en construcción) | cantera económica del PDOT extraído (139 ind.) | — |
| 12 | Protección Social & Género | Presupuesto con enfoque de género (PSG) | p19_genero | 1 |

⚰️ = pantalla archivada en `_deprecated/` que aporta como CANTERA (su contenido
se recicla aunque el archivo esté fuera de ruteo).

---

## LO QUE FALTA PARA EJECUTAR (co-creación uno por uno)

Por cada cajón, en mesa: definir el **CONCEPTO robusto** (1 párrafo potente que
defina el dominio y que incite a abrir — el que hoy "no dice nada") y validar la
**cosecha** (revisar qué piezas exactas de cada pantalla candidata sirven).

**Decisión de Javo:** ¿con cuál cajón co-creamos el primer concepto + cosecha
detallada (piloto del método)?
- Candidato del Director: **10 Territorio & Cobertura** — cosecha múltiple (4
  pantallas) demuestra bien el método · conecta Capa 2 ↔ Capa 3 (GeoTwin) ·
  historia ya validada (Isabel Muentes) · alto valor demo CAF.
- Alternativa: **09 RDC** (acotado, ya tiene C-RDC) o **02 Cooperación** (ya Supabase).

---

---

## 🧬 ADN CONCEPTUAL — PILOTO · CAJÓN 10 · TERRITORIO & COBERTURA
*Borrador del Director para AFINAR con Javo + Colega. Prueba el método de cosecha.*

| Elemento | Definición |
|---|---|
| **Propósito** | Convertir el promedio cantonal en el mapa real de la desigualdad territorial, para focalizar la acción donde más duele. |
| **Pregunta que responde** | ¿Dónde están las peores brechas del cantón y quién las sufre? |
| **Decisión que habilita** | ¿Dónde focalizar la próxima inversión/intervención? (ej. Isabel Muentes primero). |
| **Data central** | Cobertura de servicios por parroquia (agua·saneamiento·recolección) + brecha urbano-rural (pobreza extrema 7× · NBI) + riesgos territoriales (movimientos de masa · inundación · incendios) + inversión per cápita ($217 cabecera vs $40 Isabel Muentes) + GeoTwin. |
| **Frontera — qué NO es** | NO mide la institución (eso es Salud Institucional) · NO gestiona el dinero (eso es Presupuesto) · NO evalúa transparencia (eso es Transparencia). Territorio es el ESPACIO y sus desigualdades — el "DÓNDE". |
| **Pantallas cantera** | p10_territorio (cobertura/parroquias) · p4_geotwin (mapa Folium + GeoTwin narrativo F1) · p7_brecha (brecha) · p10_inversion (per cápita) · demo_data.PARROQUIAS · pdot_indicadores (servicios/riesgos parroquiales) |
| **Dashboards finales** | **2** — (1) Tablero de Cobertura & Brecha (tabla parroquial viva) · (2) GeoTwin (mapa, clic parroquia → explica · F1 ya cableado) |

**Concepto robusto (borrador a afinar — debe incitar a abrir):**

> *Territorio es donde la gestión municipal deja de ser un número promedio y se
> vuelve geografía concreta: el mapa de quién tiene agua y quién carga baldes,
> qué parroquia recibe $217 por habitante y cuál $40, dónde el riesgo de deslave
> amenaza a los asentamientos, y cómo la inversión llega —o no— a donde más
> duele. Convierte el "34.9% de cobertura cantonal" en la única pregunta que un
> alcalde necesita responder: ¿dónde intervengo primero?*

**Conexión (abajo + GeoTwin):** la data parroquial viene del motor (pdot_indicadores
+ Gold Master); las brechas de ESTE cajón aterrizan en GeoTwin (capa 3) junto con
las de género (12), residuos, etc. — convergencia territorial.

**Si este ADN captura la visión → el método queda probado para los otros 11.**

---

*Plano de Cajones v1 · Sprint C · Dylus Lab © 2026 · propuesta · concepto a co-crear.*
