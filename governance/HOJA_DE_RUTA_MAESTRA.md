# QUIRA · HOJA DE RUTA MAESTRA
**Dylus Lab © 2026 · consolidada 2026-06-12 · el mapa completo, nada al garete**

> Este documento existe para que NINGUNA pieza vuelva a quedar de lado.
> Integra: los 3 productos, las 3 capas, los principios de diseño, GeoTwin 3D,
> QUIRA Ciudadana (Terra), QUIRA IA, el refactor L2 y el calendario CAF.
> BOOT.md §AHORA apunta aquí para la ruta; los detalles vivos siguen en BOOT.

---

## 1. EL ECOSISTEMA (qué estamos construyendo)

**Dylus Lab** (empresa · `dyluslab.com`) construye **QUIRA** (producto ·
`quiraintelligence.com`): un ecosistema de inteligencia territorial. NO un
dashboard — un sistema operativo territorial. Tres productos, un solo motor:

| Producto | Usuario | Qué resuelve | Línea CAF |
|---|---|---|---|
| **QUIRA Operaciones** | Alcaldía, directores, analistas | Datos dispersos → decisiones operativas | 3 (Transición digital) |
| **QUIRA Institucional** | GAD, control, cooperación | Gobernanza preventiva, trazabilidad PDOT-PAI-Presupuesto | 3 + 8 |
| **QUIRA Ciudadana** | Ciudadanía, OSC, academia | La gente no entiende la planificación pública | 8 (Gobernanza participativa) |

El motor (Gold Master + corpus + 2,004 indicadores + motor narrativo + radar
D02 + GeoTwin) es el activo irreemplazable. Los 3 productos son vistas.

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

### SPRINT E — Escalamiento nacional (post-validación Montecristi)
- Índice de Opacidad Nacional (221 GADs · se mide por ausencia · sin Gold Master por cantón).
- Replicación: PDOT → extractor → base → GeoTwin (mismo pipeline, otro cantón).
- Testers UEB + diplomado CAF como fuerza de ingesta distribuida.
- quiraintelligence.com como portal radar nacional (⚠️ requiere hosting ≠ Streamlit Cloud).

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
