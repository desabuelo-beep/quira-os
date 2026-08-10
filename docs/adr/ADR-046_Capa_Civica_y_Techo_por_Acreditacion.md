---
id: ADR-046
authority:
  parent: ADR-045
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: APROBADO — sellado por Javo 2026-08-10 (ADR-035 §5)
fecha: 2026-08-10
supersedes:
  - ADR-045 §3 (columna «techo de verificabilidad»)
  - ADR-045 §10 (la cláusula sobre el nombre de la capa cívica)
---

# ADR-046 · El techo lo fija el documento · y la capa cívica tiene lugar propio

> **Supersede dos partes de `ADR-045`.** Ninguna de las dos toca su decisión central —una
> superficie, no dos— que queda intacta y confirmada.

## 1 · El error: la vía de llegada no fija el techo

ADR-045 §3 dio a cada custodia un techo de verificabilidad, y puso **«aporte directo → parcial»**.
Eso trata la vía por la que llegó un documento como si determinara qué acredita.

**No lo determina.** Corrección de Javo (2026-08-10):

> «Si el GAD responde, sea físico o digital, es información oficial. Basta la firma digital o
> física escaneada para que sea un documento legal, legítimo desde la institucionalidad.»

Y el canon lo respalda. **COA Art. 94** · `SHA256 d306997e39a46321`, cuyo encabezado remite a la
*Ley de Comercio Electrónico, Firmas y Mensajes de Datos, Art. 44*:

> «Firma electrónica y certificados digitales. La actividad de la administración será emitida
> mediante certificados digitales de firma electrónica. Las personas podrán utilizar certificados
> de firma electrónica en sus relaciones con las administraciones públicas.»

Las **NCI-CGE** añaden el requisito operativo · `SHA256 37f338e2dca3c714`: verificar que el
archivo firmado use «un certificado emitido por una entidad de certificación de información
**acreditada en el país**».

Eso resuelve la cuestión de raíz: **lo que se verifica es el certificado, no el portador.** Un
acto de la administración no deja de serlo porque lo entregue un vecino en vez de un scraper.

### 1.1 · Los dos ejes, ahora bien separados

| | Qué responde | Qué determina |
|---|---|---|
| **Custodia** | ¿qué presenció QUIRA de la adquisición? | la trazabilidad del ingreso |
| **Acreditación** | ¿qué acredita el documento en sí mismo? | **el techo de verificabilidad** |

Las tres custodias de ADR-045 §3 **siguen vigentes tal cual** —captura directa, adquisición
asistida, aporte directo— porque registran algo real y distinto. Lo que cambia es que ya no
cargan el techo: solo dicen por dónde entró la evidencia.

El techo pasa a esta tabla:

| Qué es el documento | Techo |
|---|---|
| Acto de la administración con **firma electrónica certificada** por entidad acreditada | **institucional** |
| Acto de la administración con **firma física y sello**, digitalizado | **institucional** |
| Comunicación desde **dominio institucional sin firma** (correo oficial) | **institucional**, con reserva declarada — LCEFEMD |
| Evidencia propia del aportante: fotografía, factura de un tercero, testimonio | **parcial**, hasta corroborar |

Y ADR-045 §3.1 se mantiene entero: **el techo es máximo alcanzable, no nivel asignado.** Un
documento institucional puede quedar en *contradicción* si choca con otro.

**Pendiente de corpus:** la LCEFEMD completa no está ingerida —solo la concordancia del COA 94—.
Hasta que entre, la fila del correo sin firma se sostiene en concordancia, no en texto verificado.
Se suma a LOGJCC y LOPDP en la lista de ingesta (ADR-045 §9).

## 2 · La capa cívica no es negociable, y por eso necesita lugar

Javo (2026-08-10):

> «No es negociable dejar el lado cívico. Nacimos con ese propósito y no es loable ni ético
> abandonarlo.»

**Qué se retiró realmente el 2026-08-08:** 44 líneas de HTML con el cartel «PRÓXIMAMENTE — EN
ROADMAP». No había ninguna capacidad ciudadana ahí: ni un formulario, ni un dato, ni una acción.
Y ADR-045 §3 **subió** el aporte ciudadano de página inexistente a vía canónica de adquisición.

**Pero la objeción es correcta**, y apunta a `ADR-045 §10`. Aquel párrafo dejó la formulación de
proyectos «fuera, pendiente de su propio ADR» y añadió que no se llamaría «QUIRA Ciudadana». Una
capacidad sin fecha, sin lugar y sin nombre **es abandono con otro nombre**, aunque la intención
fuera de prudencia. Esa cláusula era mía y era preventiva; no estructural.

### 2.1 · El test, aplicado a la capa cívica real

ADR-045 §1 aplicó el test de ADR-043 §3 a «Ciudadana como portal de consulta» y salió idéntica al
Observatorio. Correcto — **para eso**. Aplicado a lo que Terra describía de verdad, no sale igual:

| | Consultar el Observatorio | Capa cívica |
|---|---|---|
| Pregunta | ¿qué puede comprobarse del territorio? | ¿cómo ejerzo control social **con** esa evidencia? |
| Usuario | cualquiera | ciudadanía organizada · barrios · OSC · academia |
| Entrega | conocimiento consultable | oficios, expedientes, dossiers, guías, proyectos |

Distinta pregunta y distinta entrega. **Tiene identidad propia** — lo que nunca tuvo es
superficie propia, y esa distinción es toda la arquitectura de ADR-045.

### 2.2 · Decisión

**Una superficie —el Observatorio— y dentro, la capa cívica con nombre y lugar propios.** No es
una puerta: es una sala con letrero. Se conserva el nombre **QUIRA Ciudadana** para designarla.

Queda derogada la cláusula de ADR-045 §10 que prohibía el nombre. Lo que **no** se deroga y sigue
mandando: no hay segunda superficie, ni segundo cuerpo de conocimiento, ni segundo acceso.

### 2.3 · Las cuatro capacidades

Heredadas del archivo Terra y admitidas al canon —insumo que sirve, según ADR-045 §7:

| Capacidad | Qué hace | Estado |
|---|---|---|
| **Evidencia territorial** | documentos, actas, fotografías y geolocalización se vuelven evidencia estructurada y trazable | canon · ADR-045 §3 |
| **Exigibilidad asistida** | redacta el oficio, corre el cronómetro, prepara el escalón siguiente | canon · ADR-045 §4 |
| **Inteligencia cívica** | los 12 dominios legibles en varios niveles, sin jerga | canon · ADR-023 |
| **Acción territorial** | incidencia, control social y formulación de proyectos | **admitida, sin construir** |

La cuarta entra al canon como capacidad reconocida. Su **diseño** —relación con QUIRA
Cooperación, alcance, idiomas— sigue abierto: sirve a quien **pide** financiamiento, mientras
Cooperación sirve a quien lo **da**, y por el test de ADR-043 §3 esa diferencia todavía debe
resolverse. Lo que este ADR cierra es que **no se abandona**.

### 2.4 · Por qué aporta la ciudadanía: para ver su propio territorio

Javo (2026-08-10):

> «El fin de que la gente suba su información municipal es para poder **visualizar los resultados
> en los dominios**.»

Esto responde la pregunta que casi ninguna plataforma de aporte ciudadano responde: **¿por qué se
tomaría alguien el trabajo?** La respuesta no es altruismo ni «ayudar al sistema». Es reciprocidad
directa y verificable:

> **QUIRA observa 222 GAD, pero solo calcula sobre lo que existe. Un municipio que no publica
> tiene sus doce dominios vacíos. Quien aporta la evidencia de su municipio enciende la lectura
> de su propio territorio.**

Tres consecuencias, y las tres son de diseño, no de discurso:

**1 · La cobertura nacional deja de depender solo de Dylus Lab.** La captura directa alcanza hasta
donde llega la publicación oficial. Más allá de ese límite, **la ciudadanía puede activar su
cantón** — que es la única vía realista de llegar a 222 sin depender de la voluntad de 222
alcaldías.

**2 · Se enlaza con el IOC.** Un municipio opaco tiene índice de opacidad alto y dominios vacíos.
Su ciudadanía tiene la vía para llenarlos, y cada oficio ignorado en el intento **alimenta el
propio índice**. La opacidad se vuelve costosa por partida doble.

**3 · Obligación para la UI: la ausencia se muestra, y se muestra accionable.** Un dominio sin
evidencia no puede quedar en blanco ni en error. Debe decir **qué falta, por qué falta y cómo se
consigue**. La infraestructura ya existe —los ocho estados de captura de ADR-042 §6 y el nivel
`sin_evidencia` de la escala— y hasta ahora solo se usaba para informar. Aquí pasa a convocar:
un dominio vacío es un diagnóstico y una invitación, no una pantalla rota.

### 2.5 · Y una salvaguarda que esto obliga a fijar

**Que la ciudadanía llene el hueco no absuelve al GAD de haberlo dejado.** La transparencia activa
es obligación de la entidad (LOTAIP), no de sus habitantes.

Por tanto: cuando una evidencia entra por aporte ciudadano supliendo una publicación ausente, el
**IOC sigue registrando que el GAD no publicó**. El dominio se enciende; el incumplimiento no se
borra. Sin esta regla el sistema premiaría la opacidad —bastaría con no publicar y esperar a que
alguien lo haga por uno—, y convertiría el trabajo ciudadano en un servicio gratuito al
incumplidor.

## 3 · Lo que no cambia

Una sola superficie · un solo cuerpo de conocimiento · el Centro sigue siendo núcleo sin cartel ·
las tres custodias · el cronómetro LOTAIP · el IOC · «Observatorio» como denominación funcional
sin reclamar el art. 79. ADR-041, ADR-042, ADR-043 y ADR-044, intactos.

## 4 · Consecuencias

| # | Qué | Estado |
|---|---|---|
| 1 | `ADR-045 §3` columna de techo → tabla de acreditación | ⏳ al sellar |
| 2 | `ADR-045 §10` cláusula del nombre → derogada | ⏳ al sellar |
| 3 | La portada nombra la capa cívica y sus cuatro capacidades | ⛔ pendiente |
| 4 | Verificación de certificado contra entidad acreditada (NCI-CGE) | ⛔ pendiente |
| 5 | LCEFEMD al corpus, con LOGJCC y LOPDP | ⛔ pendiente |
| 6 | Pines territoriales (rojo · morado · verde) de Terra | ⛔ no decidido — no se publican hasta tener ADR |
| 7 | Dominio sin evidencia: mostrar qué falta y cómo conseguirlo (§2.4) | ⛔ pendiente |
| 8 | El IOC no se limpia porque la ciudadanía supla la publicación (§2.5) | ⛔ pendiente en el motor |

---
*ADR-046 · Dylus Lab © 2026 · supersede ADR-045 §3 y §10 · deriva de ADR-045.*
