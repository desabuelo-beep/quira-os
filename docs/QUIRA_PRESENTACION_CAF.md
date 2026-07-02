# QUIRA — Sistema Operativo de Inteligencia Territorial
### Documento de presentación · Diplomado CAF · GovTech Ecuador

> *Guía para presentar QUIRA a un equipo técnico y a la tutoría.* Sigue el orden de la imagen adjunta.
> **Regla de oro para presentar: primero el problema, después la tecnología.**

---

## 0 · Abre con el problema (el gancho para CAF)

> *"Hoy un municipio produce **miles de datos** —presupuestos, contratos, planes, rendiciones—,
> pero nadie puede responder una pregunta sencilla: **¿cumplió realmente lo que prometió?**
> QUIRA nace para responder esa pregunta con **evidencia verificable.**"*

Recién después de esa frase, muestra la imagen. La tecnología deja de ser el protagonista y pasa a ser
el **medio**.

---

## 1 · ¿Qué es QUIRA? (en una frase)

**QUIRA convierte datos públicos dispersos en inteligencia verificable para la toma de decisiones.**

Para hacerlo, **observa integralmente a los gobiernos locales**: mide la **congruencia** de toda la
cadena —**PROMESA → PLAN → PRESUPUESTO → EJECUCIÓN → RESULTADO → TERRITORIO**— y encuentra las
**brechas** entre lo prometido y lo realmente ejecutado.

El GAD (gobierno municipal) es el **sujeto observado, no el cliente**. Empezamos por **Montecristi
(Municipio 001)** como el "molde", con vocación de cubrir los **221 GAD del Ecuador**.

**La diferencia clave:** QUIRA no *calcula* opiniones, **las demuestra documentalmente**. Cada número
tiene detrás una evidencia verificable (una norma con firma digital, una cédula presupuestaria, un
acta). Si un dato no está verificado, no existe.

---

## 2 · La metáfora: un Sistema Operativo

No es una aplicación. Es un **Sistema Operativo**. Así como **Windows administra computadoras, QUIRA
administra conocimiento público**. Y como todo sistema operativo, hace cuatro cosas:

1. **Organiza** la información (el canon).
2. **Ejecuta** motores (la inteligencia).
3. **Conecta** componentes (el cableado).
4. **Ofrece experiencias** al usuario (las pantallas y la conversación).

Esas cuatro funciones son las **cuatro capas** de la imagen.

---

## 3 · La arquitectura en 4 capas (recorriendo la imagen)

### ① EL CANON — la fuente de verdad
Aquí vive la verdad; **todo lo demás deriva de aquí.** Tres piezas:

| Pieza | Tecnología | Qué es |
|---|---|---|
| **Gold Master** | (motor en Excel, pero **no es "un Excel"**) | **Motor metodológico · 123 hojas · canon operativo · la fuente de verdad.** Calcula todos los índices; su fórmula central es **INMUTABLE**. |
| **Corpus** | **Supabase** (PostgreSQL + pgvector) | Los **documentos** verificados: normativa, informes de rendición, PDOT — cada uno con firma digital **SHA-256**. |
| **Grafo** | **Neo4j** | Las **relaciones**: qué proyecto se vincula a qué meta, qué proceso a qué partida. Lo que las tablas no cruzan solas. |

### ② EL SISTEMA OPERATIVO — organiza y conecta
Corre en **Python + Claude** (los modelos de Anthropic: Haiku para volumen, Opus para razonamiento).
**Ingiere** evidencia, **la traza** (huella SHA-256) y **la explica**. Regla: *la IA razona, pero nunca
produce la verdad.*

Aquí vive su capacidad más singular — la **Curación del Conocimiento** (esto es **ingeniería del
conocimiento**, no un dashboard):

> **Estado → Audita → Corrige → Normaliza → Relaciona → Explica → Visualiza**

Y las **7 capacidades ("cables")** con que cada dominio se conecta a la evidencia: Matemático · Datos
vivos · Normativo · Relacional · Documental · IA · Visual.

### ③ LA INTELIGENCIA — ejecuta los motores
- **5 Motores Analíticos:** Matemático · Grafos · Causal · Descubrimiento · Prospectivo.
- **13 Dominios** (un "cajón" o Modelo Canónico de Dominio por área: Planificación, Presupuesto,
  Rendición de Cuentas, Participación, Salud Institucional, Territorio…). **Cada dominio se construye
  cableando las mismas capacidades** — por eso el sistema crece por *repetición*, no por excepción.
- Al evaluarse, cada dominio **produce estado**: índices y **alertas preventivas**.

### ④ LAS EXPERIENCIAS — lo que se ofrece al usuario (**Streamlit**)
Cuatro, al mismo nivel:
- **Centro de Inteligencia Territorial** — el tablero de mando.
- **Dashboards de dominio** — un tablero detallado por dominio.
- **GeoTwin 3D** — el territorio en mapa.
- **QUIRA IA (conversacional)** — la capa de conversación del sistema. **No es ChatGPT ni Claude a
  secas:** conversa con **TODO** el conocimiento de QUIRA (Gold Master, corpus, grafo, motores,
  dominios, resultados, relaciones, auditorías, evidencias). Responde: *¿por qué bajó este índice?
  ¿qué artículo del COOTAD respalda esta alerta? ¿qué dijo el alcalde sobre esta obra? compárame el
  PDOT con el presupuesto.*

### Transversales
- **GitHub** — repositorio **privado** que **versiona y da trazabilidad** a todo (código, documentos,
  decisiones). Cada cambio queda registrado y es reversible.
- **🛡 Firewall** — la frontera ética: en la pantalla pública nunca aparece la "cocina" interna, solo
  lenguaje de gobernanza. Y sobre todo: **QUIRA informa, no actúa.** Expone la evidencia; la decisión
  es de las personas.

---

## 4 · La idea más potente: **Segunda Ingeniería Pública**

> **Los sistemas públicos producen datos. QUIRA produce coherencia.**

Eso no lo hace ningún otro sistema. No "mantenemos" ni "arreglamos pantallas": **auditamos, curamos y
potenciamos** el conocimiento público, dominio por dominio, siempre desde el canon hasta la pantalla.

---

## 5 · ¿Cómo evoluciona QUIRA? (CAF seguramente lo preguntará)

QUIRA crece por **repetición industrial**: cada dominio recorre **exactamente el mismo protocolo**, lo
que garantiza una arquitectura uniforme en vez de acumular excepciones:

> **Canon (Excel) → Curación → Modelo Canónico de Dominio → Motores → Pantalla → Auditoría (7 capas) →
> Patrón → Repetición**

Cada dominio cierra con un **expediente de trazabilidad (PCD)**, para que dentro de un año cualquiera
pueda responder *"¿por qué este dominio quedó exactamente así?"*. **Ese flujo es la innovación
metodológica** — no una tecnología, sino un marco para convertir información pública en inteligencia
verificable.

---

## 6 · El diferenciador (lo que nadie más hace)

QUIRA cruza el **discurso oficial** (lo que la autoridad DICE en su rendición, extraído por IA del
video) con la **evidencia verificada** (lo que los sistemas del Estado registran). Cuando el discurso y
el hecho no coinciden, **la brecha queda a la vista, con la prueba al lado** — demagogia expuesta con
evidencia, no con opinión.

Sumado al cruce **plan de campaña (CNE) ↔ PDOT ↔ ejecución**, responde la pregunta que hoy nadie
responde de forma verificable. **Ventana estratégica: elecciones de alcaldes, noviembre 2026.**

---

## 7 · La familia QUIRA — 6 productos

Un solo motor, seis vistas: **Operaciones · Ciudadana · Institucional · Impact · Cooperación ·
Economic.**

---

## Cierre (para la tutoría)

QUIRA ya no es una aplicación que se documenta: es un **marco metodológico para convertir información
pública en inteligencia verificable**. Ese es el cambio de escala.

*QUIRA · Dylus Lab © 2026 · Montecristi = Municipio 001 · GovTech Ecuador.*
