# QUIRA — Sistema Operativo de Inteligencia Territorial
### Documento de presentación · Diplomado CAF · GovTech Ecuador

> *Guía para explicar la arquitectura de QUIRA a un equipo técnico y a la tutoría.*
> Léelo de arriba abajo: sigue exactamente el orden de la imagen adjunta.

---

## 1 · ¿Qué es QUIRA? (en una frase)

**QUIRA no vende software a los municipios. QUIRA los OBSERVA.**

Es un **Observatorio Nacional de Integridad Territorial**: un sistema que mide la **congruencia**
de toda la cadena del gobierno local —**PROMESA → PLAN → PRESUPUESTO → EJECUCIÓN → RESULTADO →
TERRITORIO**— y encuentra las **brechas** entre lo que se prometió y lo que realmente pasó.

El gobierno municipal (GAD) es el **sujeto observado**, no el cliente. Empezamos por **Montecristi
(Municipio 001)** como el "molde", con vocación de cubrir los **221 GAD del Ecuador**.

**La diferencia clave:** QUIRA no *calcula* opiniones. **Las demuestra documentalmente.** Cada número
tiene detrás una evidencia verificable (una norma con su firma digital, una cédula presupuestaria, un
acta). Si un dato no está verificado, no existe.

---

## 2 · La idea central: "una verdad, un rector"

El corazón filosófico de QUIRA es que **existe una sola fuente de verdad**, y todo lo demás **deriva**
de ella. Nunca hay dos verdades (una en el Excel y otra en el código). Esto se resume en dos reglas:

- **El canon manda.** El flujo es siempre `Canon → Sistema → Pantalla`, **nunca al revés**.
- **Ningún cambio nace en el código.** Todo concepto (una métrica, una fórmula) nace en el canon;
  el software solo lo *implementa o deriva*.

Y una regla de método: **"no diseñamos, leemos y ruteamos"** — antes de construir algo nuevo,
verificamos si ya existe en el canon. No inventamos; enrutamos lo que ya está.

---

## 3 · La arquitectura en 3 capas (recorriendo la imagen)

### ① EL CANON — la fuente de verdad (la base de la imagen)
Aquí vive la verdad. Tres piezas:

| Tecnología | Qué es | Rol |
|---|---|---|
| **Excel — "Gold Master"** | Un libro Excel de 123 hojas (SIAP-ICPI v5.5) | **El MOTOR de cálculo.** Calcula todos los índices (ICPI, alertas, etc.). Su fórmula central es **INMUTABLE**: jamás se toca. Es el "núcleo epistemológico" del sistema. |
| **Supabase** (PostgreSQL + pgvector) | Base de datos en la nube con búsqueda semántica | **El corpus documental.** Guarda la normativa (leyes, códigos), los informes de rendición, el PDOT — cada documento **verificado con firma digital SHA-256**. |
| **Neo4j** | Base de datos de grafos | **Las relaciones.** Conecta lo que las tablas no cruzan solas: qué proyecto se vincula a qué meta, qué proceso a qué partida. Hace visible la trama. |

> **Por qué Excel:** porque el conocimiento metodológico ya vivía ahí, validado durante años. En vez
> de reimplementarlo en código (y arriesgar dos verdades), lo tratamos como el motor canónico. El
> software lo **lee**, no lo reemplaza.

### ② QUIRA SO — el Sistema Operativo (el centro de la imagen)
Es el cerebro que conecta el canon con las pantallas. Corre en **Python + Claude** (los modelos de IA
de Anthropic — Haiku para volumen, Opus para razonamiento). Hace tres cosas: **ingiere** evidencia,
**la traza** (cada dato con su huella SHA-256), y **la explica**. Regla de oro: *la IA razona, pero
nunca produce la verdad* — la verdad viene del canon.

Se organiza en tres niveles de abstracción:
- **7 Cables (capacidades):** Matemático · Datos vivos · Normativo · Relacional · Documental · IA · Visual.
  Son las "tomas" con que cada dominio se conecta a la evidencia.
- **5 Motores Analíticos:** Matemático · Grafos · Causal · Descubrimiento · Prospectivo.
  Son las técnicas de análisis (desde estadística hasta detección de patrones).
- **13 Dominios (un "cajón" o Modelo Canónico de Dominio por área):** Planificación, Presupuesto,
  Rendición de Cuentas, Participación, Salud Institucional, Territorio, etc. **Cada dominio se
  construye cableando las mismas 7 capacidades** — por eso el sistema crece por *repetición*, no por
  excepción.

### ③ LAS PANTALLAS — Streamlit (la cima de la imagen)
La interfaz que ve el usuario, construida en **Streamlit** (framework de Python para dashboards). Tres capas:
- **Centro de Inteligencia Territorial** — el tablero de mando con los 13 cajones.
- **Dashboards de dominio** — un tablero detallado por cada dominio.
- **GeoTwin 3D** — el territorio representado en mapa.

### Transversales
- **GitHub** — repositorio **privado** que versiona y da **trazabilidad** a todo el sistema (código,
  documentos, decisiones). Cada cambio queda registrado y es reversible.
- **🛡 El Firewall** — una frontera ética: en la pantalla pública nunca aparece la "cocina" interna
  (los códigos y fórmulas del motor), solo lenguaje de gobernanza. Y sobre todo: **QUIRA informa, no
  actúa.** Expone la evidencia; la decisión es de las personas.

---

## 4 · El stack tecnológico, de un vistazo

| Pieza | Tecnología | Para qué |
|---|---|---|
| Motor de cálculo | **Excel** (Gold Master) | La fuente de verdad de las métricas |
| Corpus documental | **Supabase** (pgvector) | Documentos verificados (SHA-256) |
| Relaciones | **Neo4j** | El grafo de vínculos |
| Cerebro / razonamiento | **Claude** (Haiku · Opus) | Ingesta, interpretación, explicación |
| Orquestación | **Python** | Une el canon con las pantallas |
| Interfaz | **Streamlit** | Los dashboards y el mando |
| Versionado / trazabilidad | **GitHub** | Historia y reversibilidad de todo |

---

## 5 · El diferenciador (lo que ningún otro sistema hace)

QUIRA cruza el **discurso oficial** (lo que la autoridad DICE en su rendición de cuentas, extraído por
IA del video) con la **evidencia verificada** (lo que los sistemas del Estado registran). Cuando el
discurso y el hecho no coinciden, **la brecha queda a la vista, con la prueba al lado.** Es la
demagogia expuesta con evidencia — no con opinión.

Sumado al cruce **Plan de campaña (CNE) ↔ PDOT ↔ ejecución**, QUIRA responde una pregunta que hoy
nadie responde de forma verificable: *¿el gobernante cumplió lo que prometió?*

**Ventana estratégica:** elecciones de alcaldes en **noviembre 2026**.

---

## 6 · Cómo trabajamos (por si preguntan por el método)

No hacemos mantenimiento ni "arreglamos pantallas". Hacemos **segunda ingeniería**: auditamos, curamos
y potenciamos **dominio por dominio**, siempre desde el canon hasta la pantalla, por una **auditoría de
7 capas** (Gold Master → metodológica → matemática → semántica → cableado → visual → narrativa). Cada
dominio cierra con un expediente de trazabilidad (**PCD**), para que dentro de un año cualquiera pueda
responder *"¿por qué este dominio quedó exactamente así?"*.

---

## 7 · La familia QUIRA — 6 productos

Un solo motor, seis vistas de explotación:
**Operaciones** (el barrido de datos) · **Ciudadana** (la gente + la cascada legal) ·
**Institucional** (el GAD aporta su dato) · **Impact** · **Cooperación** (fondos CAF/BID/PNUD) ·
**Economic**.

---

*QUIRA · Dylus Lab © 2026 · Montecristi = Municipio 001 · GovTech Ecuador.*
*"El Gold Master ya sabe medir la gestión pública; QUIRA está aprendiendo a demostrar documentalmente
por qué cada métrica es verdadera o falsa."*
