---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [13]
  type: ARQUITECTONICA
---

# QUIRA · HOJA DE RUTA MAESTRA
**Dylus Lab © 2026 · consolidada 2026-06-12 · el mapa completo, nada al garete**

> Este documento existe para que NINGUNA pieza vuelva a quedar de lado.
> Integra: los 3 productos, las 3 capas, los principios de diseño, GeoTwin 3D,
> QUIRA Ciudadana (Terra), QUIRA IA, el refactor L2 y el calendario CAF.
> BOOT.md §AHORA apunta aquí para la ruta; los detalles vivos siguen en BOOT.

---

## 0. LA TESIS — qué es QUIRA realmente (Javo · grabado 2026-06-12)

> **QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no
> cliente** (ADR-024, ratificado). Vender licencias es *complementario*, no el fin.

**QUIRA es una INFRAESTRUCTURA DE CONOCIMIENTO VERIFICABLE para la gestión
pública territorial.** El **Observatorio Nacional de Integridad Territorial** es
**una de sus interfaces** (Const. Art. 14 · DEC-0012), y a través de él el fin es el
barrido progresivo de los 222 GADs del Ecuador. Montecristi no es el cliente #1
— es el **MOLDE**: se valida y se pule una vez, y luego se replica nacionalmente
con **TRES MOTORES DE ADQUISICIÓN** (= los 3 productos de Fase 1; cada producto
alimenta el observatorio desde su ángulo). Ningún GAD se escapa, coopere o no:

```
MOTOR 1 · QUIRA OPERACIONES (Dylus + QUIRA IA)
  QUIRA IA barre Transparencia LOTAIP · SERCOP · CPCCS  +  equipo extrae PDOT
  → monitoreo progresivo cantón por cantón → Índice de Opacidad Nacional
  (se mide por AUSENCIA: el GAD que oculta, se delata; no requiere su cooperación)

MOTOR 2 · QUIRA CIUDADANA (la gente — cobertura nacional con la población)
  ciudadano activa la IA (busca Transparencia/SERCOP/CPCCS)
  + aporta (presupuesto participativo · PDOT · Plan CNE · orgánico)
  + si no los tiene → CASCADA LEGAL: solicitud de acceso → GAD entrega
    Excel/CSV por correo CON FIRMA DIGITAL → QUIRA valida info oficial real
  + silencio 15 días → vía judicial + procedimiento paso a paso → ciudadano ejecuta

MOTOR 3 · QUIRA INSTITUCIONAL / GESTIÓN (el GAD mismo — datos ORO)
  el GAD usuario entrega sus datos operativos directos ("su espejo privado")
  → GAD predictivo/preventivo · máxima calidad de dato (voluntario, firmado)
  → donde el GAD coopera: dato ORO; donde no: Motores 1+2 lo cubren igual
```

**EL DIFERENCIADOR LETAL (coyuntural):** cruce de **Plan CNE** (promesas de
campaña) **+ NLP del discurso del alcalde en RDC** + todos los índices = la
"fricción narrativa" / demagogia expuesta matemáticamente.
**VENTANA: elecciones de alcaldes NOVIEMBRE 2026** — máxima atención ciudadana,
promesas frescas. Es la ventana de posicionamiento y adopción nacional.

**Negocio central = complementario** (cooperación internacional · certificación
de integridad · datos · estándar de referencia regional · CAF) — NO licencias GAD.

**Implicación de secuencia (no negociable):** primero MOLDE (Montecristi
mostrable: refactor L2 + caso demostrable), DESPUÉS barrido nacional. No al revés.
Esta tesis manda sobre TODO lo que sigue — si algo no sirve al observatorio
nacional o al molde que lo habilita, no es prioridad.

---

## 0.1 LA VISIÓN (norte de largo plazo · grabada 2026-06-12 · = apertura del White Paper)

> **QUIRA es la infraestructura de conocimiento e inteligencia pública de
> América Latina y el Caribe — la que USA los mejores LLMs del momento, sin
> ser uno de ellos.**
>
> No es un modelo de lenguaje: es el CEREBRO DE DOMINIO que se monta sobre
> ellos (corpus verificado + ontología gestión pública LAC + motor de
> indicadores + grafo territorial). Los LLMs son commodities que se reemplazan
> cada año; **QUIRA es lo que permanece.**
>
> *"No quieras ser lo que se reemplaza cada año. Sé lo que permanece."*

**Corrección de director (consulta existencial Javo · 2026-06-12):** QUIRA NO
debe ser ni puede ser un LLM propio (cuesta cientos de millones, se obsoleta en
meses, no se necesita). El activo DEFENDIBLE no es el modelo — es la capa de
conocimiento: corpus público verificado (SHA256), metodología SIAP-ICPI,
ontología, grafo territorial y la red de adquisición ciudadana. Los gigantes
de IA trabajan PARA QUIRA (Claude/Haiku vía API), no contra ella.
**Si alguna vez regresa la tentación de "entrenar nuestro propio modelo": NO.**
Ese capital va a la infraestructura de conocimiento, que es lo irreemplazable.
Detalle: `docs/whitepaper/WHITE_PAPER_QUIRA_v1_outline.md`.

---

## 1. EL ECOSISTEMA (cómo se materializa la tesis)

**Dylus Lab** (empresa · `dyluslab.com`) construye **QUIRA** (producto ·
`quiraintelligence.com`): un ecosistema de inteligencia territorial. NO un
dashboard — un sistema operativo territorial. **6 productos, un solo motor**
(ADR-024), construidos en 2 fases:

**FASE 1 — los 3 que construimos HOY (= los 3 motores de adquisición):**

| Producto | Usuario | Qué resuelve · rol en el observatorio | Línea CAF |
|---|---|---|---|
| **QUIRA Operaciones** | Dylus Lab (ingesta nacional) | Datos dispersos → decisiones · MOTOR 1 (barrido activo) | 3 |
| **Observatorio / Gestión** | GAD, control | GAD predictivo/preventivo · MOTOR 3 (el GAD aporta dato ORO) | 3 + 8 |
| **QUIRA Ciudadana** | Ciudadanía, OSC | Participación y control social · MOTOR 2 (la gente exige+sube) | 8 |

**FASE 2 — los 3 posteriores (vistas de EXPLOTACIÓN, mientras se opera):**

| Producto | Usuario | Qué explota |
|---|---|---|
| **QUIRA Cooperación** | cooperación internacional | elegibilidad y financiamiento (radar D02) |
| **QUIRA Impact** | BID · CAF · PNUD · Banco Mundial | evidencia de impacto territorial |
| **QUIRA Economic** | inversión, desarrollo económico local | inteligencia económica del territorio |

El motor (Gold Master + corpus + 2,004 indicadores + motor narrativo + radar
D02 + GeoTwin) es el activo irreemplazable. Los 6 productos son vistas.
**Fase 1 = motores (adquieren datos) · Fase 2 = vistas (explotan datos ya adquiridos).**
Secuencia (Javo): consolidar las 3 de Fase 1 mientras se opera → luego construir las 3 de Fase 2.

---

## 2. LAS 3 CAPAS DE LA UI (arquitectura REDEFINIDA · Javo 2026-06-13)

Reordenamiento clave: el TERRITORIO aterriza PRIMERO. Antes de los cajones,
el usuario entiende DÓNDE está parado. Secuencia pedagógica: dónde estamos →
qué pasa → dónde ocurre.

```
CAPA 1 · EL CANTÓN            → primera pantalla. Aterriza al territorio real.
  (antes "Caja 0")              Perfil de Montecristi: datos territoriales +
                                administración municipal (alcalde, concejo,
                                período: días transcurridos / días restantes de
                                mandato — DINÁMICO, no estático), alimentado de
                                webs institucionales. "¿Dónde estamos parados?"
        ↓ entrar
CAPA 2 · CENTRO DE MANDO       → 12 cajones + los dashboards que abre cada cajón.
  (hoy p_command_center_v2)      "¿Qué pasa en la gestión?" · El v2 ya navega.
        ↓ territorializa
CAPA 3 · GEOTWIN               → mapa GIS del cantón. Territorializa PDOT
                                diagnóstico + PUGS + resultados anuales medidos
                                por QUIRA. "¿DÓNDE ocurre?" · 2D hoy → 3D (PyDeck).
```

**Regla GeoTwin (Javo + colega · canónica · reforzada 2026-06-13):** GeoTwin NO
ES UN CAJÓN/DOMINIO. Es la CAPA TRANSVERSAL de territorialización. **Ningún cajón
es territorial por sí mismo; TODOS se territorializan vía GeoTwin.** Arquitectura:
**12 dominios de gestión + 1 capa territorial transversal.** Cada cajón tiene un
botón "🛰️ Ver en Territorio" que espacializa SU indicador madre — el mismo mapa
mutando según el dominio activo. (El Cajón 10 se purificó: "Cobertura de Servicios
e Infraestructura" — dejó de "ser el mapa".) Detalle + Matriz de Espacialización:
`docs/sprint-c/DICCIONARIO_CONCEPTUAL_QUIRA.md §GeoTwin`.
Evolución (diseñada y documentada · `docs/geotwin/GEOTWIN_PLAN_IMPLEMENTACION.md`):
v1 territorializa (2D Folium + F1 · parcial hoy) → v2 visualiza 3D (PyDeck+PostGIS+DEM ·
stack $0 · DISEÑADO, implementación DIFERIDA — no "futuro") → v3 predice (IA · con tracción).

**⚠️ DECISIÓN DE NAMING PENDIENTE (Javo 2026-06-13):** "Centro de Mando" es
nombre ejecutivo/militar — sirve para Operaciones e Institucional, NO para
Ciudadana. Necesita un nombre apropiado para los 3 productos, o un nombre por
producto. Opciones a decidir en mesa:
- Transversal: "Tablero Territorial" · "Panorama" · "Centro de Inteligencia Territorial"
- Por producto: Operaciones=Centro de Mando · Institucional=Tablero de Gestión ·
  Ciudadana=Mirador Ciudadano
La Capa 1 (el Cantón) sí es naturalmente transversal — el nombre del cantón
("Montecristi") funciona igual para los 3.

---

## 3. PRINCIPIOS DE DISEÑO REGISTRADOS (inviolables)

- **PD-GEN-01** — Género territorial 80% / institucional 20%. El Pin Morado.
- **PD-GEO-01** — PDOT ≡ GeoTwin. Toda brecha = indicador + narrativa + entidad geoespacial.
- **PD-CIU-01** — QUIRA Ciudadana = motor de adquisición (cascada N0-N3 + 6 fases Terra).
- **Bloomberg Firewall (Regla Oro 2)** — cero nomenclatura interna en UI.
- **Gate de verificación visual (2026-06-11)** — ningún cableado UI se declara
  funcionando sin verlo en el deploy. Herramientas: build stamp pre-auth +
  harness Playwright (`scripts/dev/preview_cc2.py`).

---

## 4. DÓNDE ESTAMOS (2026-06-21 · reconciliación de DOS VÍAS · Javo + mesa)

> **Reconciliación clave (resuelve la sensación de "salto"):** QUIRA creció en DOS vías paralelas.
> La numeración A-F es la **VÍA PRODUCTO**. La gobernanza/ingeniería de junio es la **VÍA SISTEMA**
> (Dylus Lab) — NO consume letras de producto. No fue desvío: fue construir la segunda vía, que ni
> siquiera estaba dibujada. Mapea a la decisión de Javo: *Operaciones opera el Estado · Dylus opera QUIRA.*

**VÍA PRODUCTO (QUIRA Operaciones · hacia afuera · la manda el CAF):**
```
Sprint A ✅  Base metodológica
Sprint B ✅  Territorio comprendido (2,004 indicadores · GeoTwin narrativo validado)
Sprint C ✅  Fundación Ontológica (13 dominios · Tabla Equivalencias v2 · ESG · Protocolo)
Sprint D 🔄  EVIDENCIA OPERATIVA — EN CURSO (13 cajones con dato real · gate Bloomberg 0 ✅ · GeoTwin pendiente)
Sprint E ⏳  QUIRA Ciudadana (6 fases Terra)   ·   Sprint F ⏳  Barrido Nacional
```

**VÍA SISTEMA (Dylus Lab · hacia adentro · ingeniería de la plataforma · NO es ruta de producto):**
```
S-1 ✅  Firewall Bloomberg + escáner calibrado (deuda Familia 119→0 · = el gate Bloomberg de Sprint D)
S-2 ✅  Soberanía + Lenguaje: ADR-027 (3 capas) · ADR-028 (Compilador CLI-Q + CID) · Diccionario Soberano
S-3 ✅  Cartografía: Architecture v1.0 · Dependency Atlas v1.0 · Inventario código · grafo maestro 1972
S-4 ⏳  Compilador CLI-Q/CID Fase 2 · Desexcelización (ADR-029) — se construye cuando el producto lo permita
```
*(Las etiquetas "Sprint D.2A / Sprint E" usadas en junio eran VÍA SISTEMA — re-ancladas aquí. El Sprint E de
producto sigue siendo QUIRA Ciudadana, intacto. La VÍA SISTEMA jamás roba prioridad a la VÍA PRODUCTO.)*

**Prioridad (CAF manda · §6):** la **VÍA PRODUCTO**. Próximo foco = **cerrar Sprint D** (demo Montecristi
mostrable: 13 cajones + GeoTwin), NO el compilador (Dylus-interno). El molde primero, siempre (§0).

---

## 5. LA RUTA COMPLETA (todo lo pendiente, integrado y ordenado)

### SPRINT C — FUNDACIÓN ONTOLÓGICA (✅ CERRADO 2026-06-14 · los dashboards C.1 pasaron a Sprint D)
**Objetivo cumplido: la teoría de QUIRA quedó en pie, anclada y defendible (13 ADN · Tabla · ESG · Protocolo).**
*(El detalle C.0-C.5 abajo es histórico: C.0 Tabla ✅ · C.1 dashboards → Sprint D · C.5 Caja 0 → Capa 1 "Mapa CNE".)*

- **C.0 — Tabla de Equivalencias QUIRA v1.0** (sin código · mesa) ← BLOQUEANTE
  El documento más importante: cada término interno → nombre público. Sin él,
  la nomenclatura prohibida reaparece en cada pantalla. Borrador: §Tabla abajo.
- **C.1 — Refactor L2 dashboards, uno por uno** (cadencia: maqueta texto →
  consenso mesa → ejecución → gate Bloomberg 0 + verificación visual + deploy).
  Orden (voto Colega): 1º Salud Institucional · 2º **Cooperación** (más cercana a
  producto: vault + taxonomía) · 3º Territorio (conecta GeoTwin) · 4º RDC · resto por auditoría.
  Insumo de diseño: `docs/ciudadana/TERRA_INSTITUCIONAL_v3_origen.md` (3,531 líneas spec PMV).
- **C.2 — Contenido de los 12 cajones L1** (sin código · mesa, en paralelo).
  Javo: "el concepto debe estar MUY bien explicado, 1-2 líneas no alcanzan".
  Iterar concepto+gancho de cada cajón hasta que digan lo que deben decir.
- **C.3 — Auditor de Comprensión** (propuesta Colega): segundo gate además de
  Bloomberg. Binario: ¿un alcalde/concejal/ciudadano/CAF entiende esta pantalla?
  Si no → no pasa, aunque tenga 0 Bloomberg.
- **C.4 — QUIRA IA ("Pregúntale a QUIRA")**: hoy abre el Sentinel-Terra crudo.
  Reemplazo: conversacional, consciente de rol, alimentado por motor narrativo +
  2,004 indicadores. **Dependencia: créditos API (Haiku).** Es el C3 Razonamiento
  de la arquitectura (el integrador final del ecosistema — tesis Javo validada).
- **C.5 — Caja 0 "Realidad Cantonal"** (NUEVO · pregunta Javo 2026-06-12):
  pantalla de entrada ANTES del Centro de Mando = perfil del cantón (población,
  7 parroquias, mapa, administración municipal, presupuesto global) como contexto
  para entender las realidades. **Postura Director: SÍ viable, NO es GeoTwin** —
  es la antesala estática ("quién es Montecristi"); GeoTwin es la capa dinámica
  transversal ("dónde ocurre todo"). Se nutre de datos que YA existen en las
  pantallas Terra que se refactorizan. Entra como dashboard de bienvenida.

### GEOTWIN 3D — entra al cerrar el refactor de Territorio (C.1 #3)
Fuente: `docs/geotwin/GEOTWIN_3D_origen_Javo.md`. Principio: "el 3D en gestión
pública no es estética, es evidencia".
- **Stack $0**: PyDeck (deck.gl, nativo Streamlit) + DEM gratis (NASA SRTM 30m /
  ALOS PALSAR 12.5m) + extrusión de polígonos PUGS + CartoDB (sin token Mapbox).
- **3 vistas narrativas**: Anatomía del Riesgo · La Brecha Territorial (columnas
  3D: cabecera gigante, Isabel Muentes plana 0%) · Materialización El Aromo.
- **Regla de rendimiento**: la pantalla principal NO carga el motor 3D — thumbnail
  SVG estático; PyDeck despierta solo al clic in-place (cero scroll, latencia mínima).
- **Costo**: $0 infra · ~40-60h desarrollo (lo hace Claude Code + PostGIS/Supabase).
- **Pendiente datos**: PUGS de Montecristi (está DENTRO del PDOT, 2ª parte 800+ pp —
  370 chunks ya detectados) + DEM descarga.

### SPRINT D — EVIDENCIA OPERATIVA (nuevo · insertado 2026-06-14 · el molde mostrable)
> Reconciliación (colega): la ejecución real INSERTÓ un sprint — no se renombró nada.
> Teoría C→D→E · Realidad C→D→E→F. Rastro histórico limpio para CAF/auditores.

**Objetivo FUSIONADO (Javo):** que cualquiera —CAF, concejal, ciudadano— abra QUIRA y entienda
EL CANTÓN entero (su radiografía) **sin abrir el PDOT**, viendo los 13 cajones vibrar con datos REALES
y trazables. La trazabilidad es el MEDIO; la comprensión inmediata del territorio es el FIN.

**Pregunta científica (colega):** Sprint D no "construye dashboards" — responde si la ontología
DESCRIBE la realidad o la DEFORMA. Mucho Tipo A = QUIRA funciona · mucho Tipo C = la ontología aprende
(activa el Protocolo si es estructural) · mucho Tipo B = la arquitectura aprende.

**Loop de 4 pasos POR cajón:** (1) cosecha (inventario real) → (2) contrato del dashboard (maqueta
texto) → consenso → (3) implementación (Tipo A + llenar Tipo C · con harness) → (4) verificación
visual (gate Bloomberg 0 + Auditor de Comprensión en deploy). Ontología CONGELADA salvo Tipo C estructural.

**Olas (orden colega — flujo de lectura ejecutiva):**
- 🌊 **Ola 1 · Núcleo Ejecutivo:** d06 Salud Institucional (*¿está sano el municipio?*) → d02 Presupuesto
  (*¿con qué recursos?*) → d10 Cobertura (*¿qué llega al territorio?*). Piloto d10 ya inventariado.
- 🌊 **Ola 2 · Diferenciadores CAF:** d13 Ambiente · d12 Inclusión y Género · d03 Gobernanza del Mandato.
- 🌊 **Ola 3 · Ecosistema completo:** d07 · d08 · d09 · d04 · d05 · d11 · d01.

**Doctrina de interfaz (Javo · canónica):** QUIRA es UNA pieza bento. **CERO menús, CERO sidebars.**
Los 13 cajones SON el Centro de Mando ejecutivo / de gestión / de control institucional, a la vez —
la interfaz refleja la ontología pura en la pantalla de inicio. NO hay "pantalla del alcalde": todas lo son.

**Capa 1 · "Efecto Mapa CNE" (Javo · el puente al barrido):** primera capa que aterriza de lo NACIONAL
al territorio — mapa de Ecuador → clic provincia → cantón → parroquia (estilo portal de resultados CNE).
Al hacer clic en un cantón: zoom dinámico + inyecta la retícula de los 13 cajones de ESE GAD + su
administración (alcalde, concejo, período dinámico). NO es demás: es el **pasaporte del Barrido Nacional**
y la antesala pedagógica (país → territorio → gestión). Eleva la antigua "Caja 0 · Realidad Cantonal" (C.5).
Scope: el *shell* que aterriza en Montecristi (único poblado hoy) entra en Sprint D; la forma nacional plena = Sprint F.

**Arranque:** cosecha d06 (recibe `p7_brecha`) ∥ implementación d10 (Tipo A listos). GeoTwin (Capa 3,
incl. 3D · ver arriba) se cablea al cerrar d10/Territorio.

### SPRINT E — QUIRA Ciudadana (antes Sprint D · producto 3 · la fuerza del equipo CAF)
Fuente canónica: `docs/ciudadana/TERRA_CIUDADANA_origen.md` (6 fases completas).
PD-CIU-01 era la Fase 1; Terra Ciudadana es el diseño completo:
- **Fase 1** Ingesta + Artillería Legal (cascada N0-N3 ya diseñada · oficios LOTAIP
  + cronómetro 15 días + acción judicial + Índice de Opacidad Cantonal).
- **Fase 2** Filtro Preventivo + Análisis (validación firma digital + SHA256 +
  human-in-the-loop pedagógico + 3 niveles de lenguaje).
- **Fase 3** Inventario Georreferenciado (Pin Rojo falla general · **Pin Morado**
  brecha de género — conecta PD-GEN-01 · **Pin Verde** acción climática dMRV).
- **Fase 4** Match Cívico C2C + Match Financiero (radar D02 + Gender Bonds + barrio↔OSC).
- **Fase 5** Incidencia y Poder (Silla Vacía digital · audiencias · denuncia algorítmica).
- **Fase 6** Autogestión (perfil de proyecto IA en idioma del financiador + trazabilidad ESG).
- **Estrategia equipo CAF**: el equipo trabaja la CAPA CIUDADANA (metodología, UX,
  participación) — NUNCA el núcleo. Background IP de Dylus declarado por escrito.

### SPRINT F — ACTIVACIÓN DE LA TESIS: barrido nacional (antes Sprint E · NO es una fase tardía — es el FIN)
Se activa cuando el MOLDE Montecristi está mostrable (no antes). Es el corazón del §0.
**Motor 1 · Operaciones:**
- Fetchers a construir: Transparencia LOTAIP · SERCOP · CPCCS (patrón de `app/fetchers/`
  ya existe para fondos — replicar). Dependencia: créditos API.
- Extractor PDOT por cantón → base → GeoTwin: **YA CONSTRUIDO** (`pdot_extractor.py` +
  `kb_loader.py`). Una pieza del barrido ya está lista — replica a cualquier cantón.
- Índice de Opacidad Nacional (222 GADs · se mide por ausencia · sin Gold Master por cantón).
**Motor 2 · Ciudadana:** las 6 fases de Terra (ver Sprint D) — la gente amplía la cobertura.
**Diferenciador electoral (construir para ventana NOV-2026):**
- Análisis Plan CNE (promesas de campaña) — semilla ya existe (dom03: 48/66 promesas CNE en PDOT).
- NLP del discurso del alcalde en RDC cruzado con índices ("fricción narrativa" — Terra Fase 2).
**Infra:** testers UEB + diplomado CAF = fuerza de ingesta distribuida ·
quiraintelligence.com como portal radar nacional (⚠️ requiere hosting ≠ Streamlit Cloud).
**Estrategia de institucionalización (consulta Javo 2026-06-12 · respuesta Director):**
- **White Paper QUIRA v1.0** (50-80 pp · síntesis de lo ya escrito) = ENTREGABLE Sprint D · oro CAF.
  Esqueleto + visión + mapeo de fuentes YA listos: `docs/whitepaper/WHITE_PAPER_QUIRA_v1_outline.md`.
  Abre con LA VISIÓN (§0.1). Redacción = ensamblaje del 80% ya escrito, caja negra del motor.
- Apertura: abrir la METODOLOGÍA ahora (White Paper, posicionamiento) ≠ abrir el CÓDIGO
  (Open Core formal) — esto último DIFERIDO hasta tener tracción (varios cantones). Abrir el
  estándar antes de tracción regala la ventaja sin cobrar el efecto de red. Framing "estándar
  territorial abierto + motor cerrado" para CAF = legitimidad sin riesgo (motor sigue caja negra).

### BACKLOG congelado (no abrir hasta su disparador)
- Auditoría Gold Master (2 dimensiones: riesgo territorial · urbano-rural) — tras refactor L2.
- D12 oficios institucionales — backlog estratégico (no bloqueante).
- SAT-0.1 / SAT-0.2 (fugas presupuestarias eSIGEF/SERCOP) — v3.0 del motor, post-financiamiento.
- OSINT — capa futura del Índice de Opacidad.

---

## 6. CALENDARIO CAF (deadline externo — manda sobre prioridades)

**Diplomado en Gobernabilidad e Innovación Pública (DGIP 5ta ed · CAF).**
Los mejores 20 proyectos de LATAM pasan a ronda con técnicos CAF.
- **Retos que dan vida a la propuesta**: **3** Transición digital en la admin
  pública (principal) · **8** Gobernanza participativa (complementaria) · **9**
  Ciudades digitales y verdes (GeoTwin + ambiente/economía circular).
- **Proyecto presentado**: "QUIRA by Dylus Lab — Ecosistema de Inteligencia
  Territorial" (3 productos, caso Montecristi). Texto en `docs/caf/CAF_proyecto_equipos_IP.md`.
- **Qué SÍ se muestra**: arquitectura conceptual, pantallas finales, caso Montecristi.
  **Qué NO**: Excel Gold Master, fórmulas, repo, credenciales (caja negra).
- **Implicación para la ruta**: el material demo CAF = Centro de Mando v2 +
  GeoTwin (idealmente 3D) + Fichas v2 + radar. Priorizar lo que se ve.

---

## 7. TABLA DE EQUIVALENCIAS QUIRA v1.0 — BORRADOR (a cerrar en mesa C.0)

*Inventario real de términos internos en strings de UI (auditoría 2026-06-12):*
SAT×94 · PSG×49 · ICPI×40 · Gold Master×39 · TGI×36 · IGP×35 · DomNN×30 · Hxx×26 ·
NBI×25 · IED×22 · ISP×21 · ITAM×20 · IET×19 · IOC×17 · TPS×16 · IFE-A×15 · etc.

| Interno (PROHIBIDO en UI) | Público propuesto (a consensuar) |
|---|---|
| ICPI | Cumplimiento Institucional |
| SAT | Sistema de Alerta Temprana / Alertas Institucionales |
| TGI | (definir — ¿Gestión Territorial Integral?) |
| PSG | Presupuesto con enfoque de género |
| ISP | Inversión en salud / saneamiento (según contexto) |
| ITAM | Transparencia activa municipal |
| IGP | Participación / gobernanza participativa |
| IOC | Opacidad institucional |
| IED | Eficiencia de direcciones |
| IET | Equidad territorial |
| NBI | Necesidades básicas insatisfechas (este SÍ es público estándar INEC — confirmar) |
| TPS | (definir) |
| Gold Master / Hxx / H73 | "Motor de indicadores" — NUNCA visible |
| DomNN / C01 / CE_xxx | jamás visibles — solo lenguaje del dominio |
| Gov Twin | GeoTwin |
| AVEP / MMP / QTMP / ACK / MNT_UUID | jamás visibles |

---

## 8. DEPENDENCIAS Y BLOQUEOS CONOCIDOS

- **Créditos API (Haiku)**: bloquea QUIRA IA conversacional + extracción narrativa
  PDOT pendiente (1,254 chunks) + ciclo live del radar. NO bloquea: refactor L2,
  GeoTwin, Caja 0, cajones (todo determinístico/datos ya en base).
- **PUGS de Montecristi**: dentro del PDOT (2ª parte) — extraer para GeoTwin 3D.
- **DEM**: descarga gratuita NASA/ALOS para relieve 3D.
- **Hosting quiraintelligence.com**: Streamlit Community Cloud NO soporta dominio
  propio — decisión de mesa (costo) para activar el portal.

---

*Hoja de Ruta Maestra · QUIRA OS · Dylus Lab © 2026 · actualizar cuando cambie la ruta, no el detalle (eso vive en BOOT.md §AHORA).*
