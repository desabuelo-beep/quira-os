# Storyboard de Experiencia — El Viaje del Alcalde (Sprint D · Producto)

**2026-06-20 · fase DISEÑO (antes de dashboards) · mesa (colega + académico + Javo) · Director: Ronald**

> **Qué es:** el mapa de la **experiencia**, no del conocimiento. El conocimiento ya vive sellado en el
> `DICCIONARIO_CONCEPTUAL_QUIRA.md` (13 ADN · 11 campos). Este doc **NO lo repite — lo pone en movimiento.**
> Añade solo lo que el Diccionario no tiene: el **viaje**, los **dashboards** que necesita cada dominio, y el
> **criterio** que la IA dictamina. *(Regla #6: si una verdad ya tiene rector, aquí se referencia, no se redefine.)*

## 0 · Por qué este doc (y por qué NO es el "Doc 2" del colega)

El colega pidió "los 13 dominios como experiencia: **por qué existe · qué pregunta · qué evidencia · qué decisión**".
Esos cuatro **ya son el ADN sellado** (campos 5·6·9·10). Reescribirlos sería reconstruir el canon por 3ª vez —
la misma amnesia que reinventó ADR-030. Aquí tomamos el ADN como **dado** y diseñamos lo único que falta:
**dashboards + criterio IA + viaje.** Lo demás se lee del Diccionario.

## 1 · El Viaje del Alcalde (la experiencia, en 6 momentos)

1. **Entra.** No ve KPIs sueltos: entra al **puente de mando** de un sistema operativo estatal. Sobrio,
   denso, soberano. La primera impresión NO es "lindo dashboard" — es *"esto me conoce el cantón entero".*
2. **Mira arriba.** Cuatro **Dominios de Exploración** (§2) le abren su territorio, su gobierno, su proyecto
   político y su evidencia. Separan de entrada **lo técnico de lo político** (regla de Javo).
3. **Hace click en un cajón.** La card asimétrica no le da un número: le da una **definición que construye
   criterio** (concepto, izq) + el **dato duro** (der) + la **pregunta** que ese dominio responde (al pie).
   El click es en toda la tarjeta — entra sin fricción.
4. **Abre el dashboard.** Regla **50/50**: mitad visualización, mitad interpretación. No es un gráfico con
   leyenda — es media pantalla de evidencia y media pantalla de **juicio metodológico**.
5. **Pregunta a QUIRA.** El copiloto no describe la barra del gráfico (eso lo hace cualquier software barato).
   Dictamina el **criterio** — la distancia entre lo que se declaró, lo que se certificó y lo que se observó (§3).
6. **Sale convencido.** No porque vio algo bonito, sino porque vio la **distancia entre la narrativa pública y
   la evidencia institucional** — y eso no se lo da nadie más.

## 2 · Los 4 Dominios de Exploración (menú superior · navegación de producto · QUIRA Institucional)

Lo único que el canon **no tenía**: los 4 de arriba dejan de ser KPIs repetidos y se vuelven el **menú de
identidad** del producto. Separan las dos líneas que hoy se mezclan (regla de Javo · "no juntar lo político y
lo técnico"):

| # | Dominio de Exploración | Línea | Entra a (de los 13) |
|---|---|---|---|
| ① | **Territorio** | el *dónde* | d10 Cobertura · d13 Ambiental · GeoTwin |
| ② | **Gobierno** | lo **técnico-administrativo** | d06 Salud · d01 Planificación · d02 Presupuesto · d04 Alertas · d05 Holding · d07 Transparencia |
| ③ | **Proyecto Político (Plan CNE)** | lo **político-democrático** | d03 Gobernanza del Mandato · d08 Participación · d09 Rendición |
| ④ | **Evidencia Documental** | el *sustento probatorio* | corpus · informes · links LOTAIP (transversal) |

> **La separación clave (Javo):** el **plan de campaña (CNE)** vive en ③ Proyecto Político; el **PDOT técnico**
> vive en ② Gobierno. El cajón **d03** es el puente que *mide la distancia entre ambos* — por eso es político,
> no técnico. Así nunca se confunde la promesa con la programación. *(Operaciones y Ciudadana definirán sus
> propios 4 — estos son los de Institucional.)*

## 3 · El criterio de QUIRA = los 3 mundos (el patrón universal del 50% interpretación)

QUIRA no describe gráficos. En cada dominio mide la **distancia entre tres relatos del mismo hecho**:

```
        QUIRA observó            CPCCS certificó           ALCALDE declaró
     (Gold Master · motor)   (informe oficial · control)  (discurso público · NLP)
            └───────────────── la DISTANCIA entre los tres ─────────────────┘
                          eso es el criterio. eso es QUIRA.
```

Su forma más pura es **d09 Rendición de Cuentas** (los tres mundos explícitos). Pero el patrón aplica a todos:
QUIRA siempre contrasta **lo declarado vs. lo evidenciado** y dictamina dónde divergen. *Ej. d09:* "el informe
refleja el 91% de la gestión; el discurso sobrerrepresenta seguridad y omite ejecución social — 3 divergencias."

## 4 · Tabla de Experiencia — los 13 (concepto público · dashboard · criterio IA)

**Concepto público** = el texto de la card (condensa el campo-4 del ADN a lenguaje de administración pública;
firewall). **Dashboard** = lo que necesita (cosecha · `PLANO_DE_CAJONES`). **Criterio QUIRA** = el juicio, no la
descripción. *(pregunta·evidencia·exclusiones·indicador → se leen del Diccionario, no se repiten aquí.)*

| # | Dominio | Concepto público (= card · construye criterio) | Dashboard(s) que necesita | Qué dictamina QUIRA (criterio) |
|---|---|---|---|---|
| d01 | Planificación Estratégica | La consistencia entre lo que el municipio planificó a largo plazo y los hitos que de verdad cumple — el rumbo, no el discurso. | Tablero de Metas (4 ejes · avance físico) | Si el rumbo plurianual se sostiene o qué ejes se desviaron del plan. |
| d02 | Presupuesto & Financiamiento | La capacidad de captar, mover y ejecutar recursos a tiempo — y de apalancar capital externo sin caer en subejecución. | Tablero Financiero + Radar de Elegibilidad de fondos | Si la ejecución sigue el ritmo del compromiso o hay riesgo de subejecución / capital ocioso. |
| d03 | Gobernanza del Mandato | La correspondencia entre lo prometido en campaña y lo que el plan de gobierno realmente ejecuta — la palabra empeñada, medida. | Matriz Promesa↔Plan + NLP de campaña | La distancia entre la promesa electoral y el plan ejecutado: qué se cumplió, qué se diluyó. |
| d04 | Alertas Institucionales | La vigilancia preventiva: las desviaciones y riesgos detectados antes de que se vuelvan crisis. | Monitor de Alertas (cola · semáforo) | Cuáles alertas exigen intervención HOY — prioridad causal, no una lista plana. |
| d05 | Holding e Integración Municipal | El desempeño coordinado de las **entidades** del municipio (empresas públicas y adscritas) — quién articula y quién arrastra al conjunto. | Comparativo de Entidades (misma vara) | Qué entidad arrastra al conjunto y por qué — no el promedio. |
| d06 | Salud Institucional | El estado de fondo del aparato público: su capacidad de sostener el cumplimiento de sus funciones en el tiempo, no solo cumplir hoy. | Diagnóstico Institucional + mapa de causalidad a otros dominios | Dónde se concentra el deterioro estructural — causa, no síntoma. |
| d07 | Transparencia | La relación entre la obligación legal de publicar y la capacidad real de sostener una gestión auditable por la ciudadanía. | Tablero LOTAIP (21/21 · evidencias + links verificables) | Si la apertura es verificable o solo formal: publicado ≠ auditable. |
| d08 | Participación Ciudadana | La incidencia real de la ciudadanía en las decisiones — no cuántos talleres hubo, sino cuánto cambiaron lo que se decidió. | Tablero de Incidencia (mecanismo → ¿cambió la decisión?) | Si la participación incidió o fue decorativa — cambió una decisión, sí o no. |
| d09 | Rendición de Cuentas | La validación pública de la gestión: si la narrativa que el municipio declara coincide con la evidencia que el sistema observó. | Tablero de Congruencia 3-mundos (declaró/certificó/observó) + NLP del discurso | La distancia exacta entre lo declarado, lo certificado por el control y lo observado en el presupuesto. |
| d10 | Cobertura de Servicios e Infraestructura | El acceso real a los servicios básicos visto desde el territorio: dónde llegan las redes y dónde está el déficit estructural. | Tablero de Cobertura & Brecha (parroquial) + GeoTwin | Dónde está el déficit estructural y a quién golpea — no el promedio cantonal. |
| d11 | Desarrollo Económico Territorial | La vitalidad económica del territorio: su capacidad de sostener producción, empleo y cadenas de valor. | *(bloqueado · esqueleto — campo verde)* | *(en construcción · NO inventar indicador madre)* |
| d12 | Inclusión, Equidad y Género | La capacidad de cerrar las brechas de los grupos de atención prioritaria, sobre todo donde la vulnerabilidad se concentra en el territorio. | Tablero de Equidad (presupuesto + brecha territorial) | Si el presupuesto de equidad es real o nominal, y dónde se concentra la brecha. |
| d13 | Sostenibilidad y Resiliencia Ambiental | El equilibrio entre las presiones sobre el ambiente y la capacidad del municipio de conservar sus recursos y adaptar el territorio al riesgo climático. | Tablero Ambiental (riesgo biofísico × asentamientos) + ODS ambientales | Si la gestión mitiga la vulnerabilidad ambiental o solo la declara. |

## 5 · Rulings de Javo — registrados (revisan la Auditoría)

- **Holding SÍ es dominio (d05), re-scope.** No es comodín: analiza **solo las entidades satélite** del GAD
  (empresas públicas, adscritas — Aseo, Bomberos, Patronato), **NO el GAD-núcleo** (eso es d06 Salud
  Institucional). Tiene frontera → es dominio legítimo. *Revierte el "adelgazar d05" de la Auditoría; lo que SÍ
  se mueve es el contenido de RdC (→d09) y Participación (→d08) que estaba mal ubicado.*
- **CNE arriba.** Una de las 4 etiquetas superiores = **Proyecto Político (Plan CNE)** (§2 ③), para separar la
  línea política de la técnica. Ya estaba en ADR-030 §2 — confirmado y operacionalizado aquí.

## 6 · Orden de construcción (cuando se aprueben los conceptos)

1. **Subir los 13 conceptos** (esta tabla, col. 3) a las cards — el upgrade semántico (deriva campo-4). *Visible, chico, "bien y bonito".*
2. **4 Dominios de Exploración** arriba (§2) — reemplazan los KPIs repetidos.
3. **Dashboards por ola** (cada uno con su razón de existir, ya definida arriba):
   **Ola 1** d06 · d02 · d10 (núcleo ejecutivo · CAF) → **Ola 2** d09 (3-mundos, la joya) · d03 · d13 → **Ola 3** el resto.
4. Cada dashboard: 50/50 + criterio IA del patrón 3-mundos. Verificación en deploy por cajón.

---
*Storyboard de Experiencia v1 · Sprint D · Dylus Lab © 2026 · "QUIRA no vende pantallas: vende la distancia entre lo que se dijo y lo que se hizo. El ADN dice qué es cada dominio; este doc dice cómo se vive."*
