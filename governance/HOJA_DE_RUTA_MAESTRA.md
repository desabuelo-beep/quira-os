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

**QUIRA es un OBSERVATORIO NACIONAL DE INTEGRIDAD TERRITORIAL.** El fin es el
barrido progresivo de los 221 GADs del Ecuador. Montecristi no es el cliente #1
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
| **QUIRA Institucional / Gestión** | GAD, control | GAD predictivo/preventivo · MOTOR 3 (el GAD aporta dato ORO) | 3 + 8 |
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

## 2. LAS 3 CAPAS DE LA UI (arquitectura de navegación)

```
L1  CENTRO DE MANDO   → 12 cajones (el v2 nativo ya navega · 2026-06-11)
        ↓ clic ABRIR
L2  DASHBOARDS        → N dashboards por cajón · "cada cajón abre su universo"
        ↓ territorializa
L3  GEOTWIN           → CAPA TRANSVERSAL (no es un dominio) · aterriza TODO en
                        el territorio real · 2D hoy → 3D (PyDeck) en ruta
```

**Regla GeoTwin (Javo · canónica):** GeoTwin NO ES UN DOMINIO. Es la capa
completa que lleva todos los dominios y sus dashboards y los conecta con el
territorio real — donde se ven las asimetrías por barrio/sector/parroquia.
Es donde aterrizan políticas, planes, programas y proyectos.

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

## 4. DÓNDE ESTAMOS (2026-06-12)

```
Sprint A ✅  Base metodológica
Sprint B ✅  Territorio comprendido (2,004 indicadores · GeoTwin narrativo validado)
Sprint C 🔄  Operacionalización — EN CURSO
    ✅ Centro de Mando v2 nativo (cajones navegan en deploy)
    ✅ GeoTwin F1 (clic parroquia → explica · motor cableado)
    🔄 Refactor L2 dashboards — PROPUESTA en mesa (docs/sprint-c/PROPUESTA_REFACTOR_L2.md)
```

---

## 5. LA RUTA COMPLETA (todo lo pendiente, integrado y ordenado)

### SPRINT C — Operacionalización (en curso)
**Objetivo: "que una persona abra QUIRA y entienda Montecristi sin leer el PDOT".**

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

### SPRINT D — QUIRA Ciudadana (producto 3 · la fuerza del equipo CAF)
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

### SPRINT E — ACTIVACIÓN DE LA TESIS: barrido nacional (NO es una fase tardía — es el FIN)
Se activa cuando el MOLDE Montecristi está mostrable (no antes). Es el corazón del §0.
**Motor 1 · Operaciones:**
- Fetchers a construir: Transparencia LOTAIP · SERCOP · CPCCS (patrón de `app/fetchers/`
  ya existe para fondos — replicar). Dependencia: créditos API.
- Extractor PDOT por cantón → base → GeoTwin: **YA CONSTRUIDO** (`pdot_extractor.py` +
  `kb_loader.py`). Una pieza del barrido ya está lista — replica a cualquier cantón.
- Índice de Opacidad Nacional (221 GADs · se mide por ausencia · sin Gold Master por cantón).
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
