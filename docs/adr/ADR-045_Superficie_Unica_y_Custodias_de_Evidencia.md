---
id: ADR-045
authority:
  parent: ADR-043
  constitution_articles: [1, 2, 4, 5]
  type: ARQUITECTONICA
status: APROBADO — sellado por Javo 2026-08-08 (ADR-035 §5)
fecha: 2026-08-08
supersedes:
  - ADR-043 §2 (fila «Adquisición de evidencia»)
---

# ADR-045 · Una superficie de observación · tres custodias de evidencia

> **Supersede `ADR-043 §2`, únicamente en la fila de Adquisición.** El método de ADR-043 no se
> discute: se le aplica a un caso al que no se lo habíamos aplicado, y devuelve un resultado
> distinto del que quedó escrito.

## 1 · Qué de ADR-043 §2 no se sostiene

La tabla lista **Observatorio** y **QUIRA Ciudadana** como dos entradas paralelas. El propio
ADR-043 §3 fija el criterio: si dos cosas comparten usuario y salida, son una vista, no dos
productos. Aplicado:

| | Observatorio | Ciudadana |
|---|---|---|
| Pregunta | ¿qué puede comprobarse del territorio? | ¿qué puede comprobarse del territorio? |
| Usuario | cualquiera | cualquiera |
| Entrega | conocimiento territorial verificable | conocimiento territorial verificable |

**Idénticas en las tres.** Son una superficie con dos modos de participación, no dos puertas.

La duplicación tuvo costo real: se publicaron dos accesos donde solo uno existía, y el código
nunca llegó a tener un ambiente `ciudadana` — el router solo conoce «Confianza Ciudadana», que
es el módulo del dominio d07, otra cosa.

## 2 · La superficie se llama Observatorio

**«Centro de Inteligencia Territorial» deja de ser nombre público.** Sigue existiendo como capa
del núcleo; lo que termina es su presencia en la UI.

Tres razones, en orden de peso:

1. **ADR-024 §Capa A ya lo decía**: el núcleo es «Invisible. Interno.» El Centro es núcleo. Que
   su nombre encabezara pantallas es el núcleo filtrándose al producto — la misma clase de error
   que el Firewall (Regla 2) existe para impedir.
2. **Registro.** «Centro de Inteligencia» suena, ante un ministro o un director de CAF, a
   servicios de inteligencia. Para un sistema cuya tesis es transparencia y control social, el
   registro juega en contra. «Observatorio» es español de administración pública, que es lo que
   la Regla 2 exige afuera.
3. **El sistema ya lo sabía.** La etiqueta de acceso en producción decía, en una sola cadena:
   `"Entrar al Observatorio\n\nCentro de Inteligencia Territorial · equipo Dylus Lab"`. Cuando
   hace falta un segundo nombre para decir una cosa, sobra uno de los dos.

## 3 · Tres custodias, no dos

Lo que **no** puede fusionarse no es el producto: es la custodia. Si evidencia que QUIRA no
presenció entrara al corpus indistinguible de la que capturó, QUIRA estaría certificando lo que
no vio — y eso contradice el Principio Rector, no una convención de nombres.

| | Origen | ¿Reproducible? | Techo de verificabilidad |
|---|---|---|---|
| **Captura directa** | QUIRA toma de fuente pública abierta | sí, repitiendo el procedimiento | independiente |
| **Adquisición asistida** | la entidad responde y **firma** un oficio que QUIRA redactó | sí — cualquiera puede presentar el mismo oficio | institucional |
| **Aporte directo** | el ciudadano entrega lo que ya tenía (factura, foto, acta) | no hay procedimiento que repetir | parcial, hasta corroborar |

La segunda fila corrige un error de este documento en su primer borrador, que la daba por no
reproducible (corrección de Javo · 2026-08-08). El fundamento no es que «QUIRA ayude»: es la
**firma electrónica**. El oficio exige respuesta por correo precisamente para forzarla, de modo
que lo que llega es un documento institucional firmado. **El origen es la entidad; el ciudadano
fue el vehículo.** Por eso alcanza techo institucional y no parcial.

### 3.1 · Custodia y verificabilidad son dos ejes, no uno

La columna de la derecha dice **techo**, no nivel, y la distinción es operativa:

| | Pregunta que responde | Instrumento |
|---|---|---|
| **Custodia** | ¿de dónde vino y qué presenció QUIRA de su adquisición? | las tres filas de arriba |
| **Verificabilidad** | ¿cuánto podemos afirmar sobre esta evidencia? | la escala de 5 niveles |

La custodia **fija el máximo alcanzable; no asigna el nivel**. Una evidencia de captura directa
no es «independiente» por serlo: puede quedar en *contradicción* si choca con otra, o en
*parcial* si está incompleta. Leer la tabla como asignación automática convertiría la
procedencia en un certificado, que es exactamente lo que QUIRA no hace.

## 4 · El circuito de adquisición asistida

Norma verificada en corpus (Regla 3):

- **LOTAIP Art. 34** · `SHA256 7e6fb9b6d0e86908` — «deberá ser respondida en el plazo de diez (10)
  días, que puede prorrogarse por cinco (5) días más, **por causas debidamente justificadas e
  informadas a la persona solicitante**».
- **LOTAIP Art. 40** · `SHA256 f3bf5fc59611db3e` — gestión oficiosa ante respuesta ambigua o de
  mala calidad; 10 días para corregir; si no, interviene la Defensoría del Pueblo.
- **LOTAIP Art. 41** · `SHA256 b883e5dd1d61d420` — se presenta ante la DPE dentro de 30 días
  desde el vencimiento; informe con correctivos de aplicación obligatoria y plazo perentorio.

| Día | Qué ocurre |
|---|---|
| 0 | se presenta la solicitud |
| **10** | vence — **salvo** prórroga notificada y justificada |
| **15** | vence la prórroga máxima |
| **15 → 45** | ventana para gestión oficiosa ante la DPE |
| después | Acción de Acceso a la Información Pública — *fundamento pendiente de verificar* |

Dos precisiones que el archivo histórico no tenía:

- **La prórroga no es automática.** Requiere notificación justificada. Si la entidad calla, el
  plazo venció el día 10 — y no haber notificado la prórroga es, en sí mismo, un dato de opacidad.
- **Existe un escalón administrativo antes del judicial** (arts. 40-41), más rápido y barato, y
  va a la misma Defensoría cuyo portal de transparencia el Observatorio ya monitorea. El circuito
  se cierra sobre una entidad con la que QUIRA ya trabaja.

**Lo que QUIRA hace:** redacta el oficio con su fundamento normativo, corre el cronómetro, avisa
al vencimiento, prepara el documento del siguiente escalón.
**Lo que QUIRA NO hace:** comparecer, representar ni patrocinar. Eso requiere abogado y no se
promete. La vía judicial queda descrita, no ofrecida, hasta que la **LOGJCC entre al corpus** —
hoy no está, y sin norma verificada no hay dato.

**La reproducibilidad no depende de la identidad, la permanencia ni la participación posterior
del ciudadano que activó el procedimiento.** Lo que se repite es el procedimiento —el mismo
oficio, a la misma entidad, con el mismo fundamento—, no la persona que lo presentó. Si el
ciudadano abandona el trámite a mitad de camino, la respuesta firmada que ya llegó **sigue siendo
evidencia institucional válida**: su validez nunca dependió de que él siguiera ahí.

De ahí una restricción de diseño, más estricta que cualquier obligación legal:

- El **contacto del ciudadano es opcional**. Sirve para avisarle del vencimiento; no es condición
  para generar el oficio, ni para que la respuesta entre al corpus.
- **QUIRA guarda el mínimo indispensable y por el tiempo del trámite.** Quien exige información a
  su municipio queda expuesto por el hecho de exigirla: un registro de solicitantes sería una
  lista de quiénes fiscalizan a quién. Ese registro no debe existir.
- **La evidencia se incorpora sin la identidad de quien la gatilló.** El oficio y la respuesta
  firmada son públicos por naturaleza; el solicitante no.

*La LOPDP no está en el corpus — esto es decisión de diseño de QUIRA, no lectura de la ley.*

## 5 · El silencio es dato

Los oficios ignorados alimentan el **Índice de Opacidad Cantonal (IOC)**, que ya figura entre los
índices del motor en ADR-024 §Capa A y tiene datos en `gm_snapshot.json`. La ausencia de respuesta
no interrumpe el circuito: lo alimenta. Es la aplicación operativa del Principio Rector — la
ausencia de evidencia es un **resultado**, y aquí además es un resultado medido y publicable.

## 6 · «Observatorio»: denominación funcional, no figura jurídica

**LOPC Art. 79** · `SHA256 87b587756d87ef0e`:

> «Los observatorios se constituyen por grupos de personas u organizaciones ciudadanas **que no
> tengan conflicto de intereses con el objeto observado**. Tendrán como objetivo elaborar
> diagnósticos, informes y reportes con independencia y criterios técnicos…»

**No reserva la denominación.** Describe cómo se constituye la figura, no quién puede usar la
palabra. El contraste con el artículo anterior lo confirma: el **78**, de veedurías, remite a un
*Reglamento General de Veedurías*; el 79 no remite a nada — sin reglamento, sin registro, sin
sanción.

**Y no otorga ninguna facultad.** No da derecho de acceso ni canal privilegiado. Todo lo que QUIRA
hace ya lo puede hacer cualquier persona sin ser observatorio del 79. La figura daría legitimidad
institucional, no capacidad.

**Lo que sí costaría reclamarla:** la cláusula de conflicto de intereses. QUIRA Institucional le
vende al GAD, y el GAD es el objeto observado.

**Decisión: se usa la palabra, no se reclama la figura.** En concreto, se evita «**Observatorio
Ciudadano**», que es el término técnico de la ley y del instructivo del CPCCS. Esto no cierra la
otra puerta: si algún día conviene constituirlo, la salida es separar las personas jurídicas —
Dylus Lab pone la infraestructura, un observatorio constituido aparte firma los diagnósticos. Lo
único que la cerraría es reclamar el 79 ahora, mientras se le vende al observado.

**Esto no es todavía una posición jurídica.** El art. 79 entra a la lista de revisión de jurista
de `ACK_REGISTRY` antes de ser definitivo.

## 7 · El archivo histórico es insumo, no autoridad

Regla fijada por Javo (2026-08-08), tras verificar que el diseño de Ciudadana estaba completo
desde junio en `docs/ciudadana/TERRA_CIUDADANA_origen.md`:

> **Del archivo se toma lo que sirve. El canon vigente manda.**

Dos consecuencias, y las dos importan:

1. **Se consulta el archivo antes de reconstruir.** Este ADR existe porque el director y el colega
   pasaron dos intercambios rehaciendo a mano un diseño terminado hacía dos meses. De ahí salieron
   la firma electrónica, el cronómetro y el IOC.
2. **El archivo no supersede al canon.** En los documentos de TERRA, «Impact» nombraba el
   marketplace financiero y «Data» la capa de academia. **ADR-044 se mantiene sin cambios**:
   Impact es investigación y apertura, Cooperación es financiamiento. Un documento de época
   anterior no revierte una decisión vigente.

El archivo también envejeció donde el canon ya corrigió: describe al motor leyendo el **eSIGEF**,
que es exactamente lo que se rectificó de raíz el 2026-08-07. Se lee sabiendo dónde falla.

## 8 · Qué NO cambia

Motor Gold Master · corpus · grafo · MATRIZ_CANONICA · los 12 dominios · los 8 estados de captura
· conectores · registro de corridas · los 8 gates de CI · la escala de verificabilidad de 5
niveles · la cadena madre de seis eslabones · el sistema visual.

ADR-023, ADR-042 y ADR-044 quedan intactos. **ADR-041 §4 sobrevive entero**: Ciudadana sigue
siendo entrada de evidencia — este ADR la hace más precisa, no la desplaza. De ADR-043 solo cae
una fila; su método es el que produjo esta corrección.

## 9 · Consecuencias

| # | Qué | Estado |
|---|---|---|
| 1 | `ADR-043 §2`, fila de Adquisición, superada por este documento | ⏳ al sellar |
| 2 | «Centro de Inteligencia Territorial» sale de la UI — ~12 cadenas visibles, **a mano** | ⛔ pendiente |
| 3 | Portada: sección ecosistema + etiqueta de acceso | ⛔ pendiente |
| 4 | `login_view.py` «no es solo un observatorio» — se contradice con el nombre | ⛔ pendiente |
| 5 | Atajo superior de acceso: fija el estado pero no trae el formulario a la vista | ⛔ pendiente |
| 6 | LOGJCC y LOPDP al corpus — hoy no están (verificado 2026-08-08) | ⛔ pendiente |
| 7 | Art. 79 LOPC a la lista de revisión de jurista | ⛔ pendiente |
| 8 | Aviso de superación en ADR-024 puesto antes del sello de ADR-044 — se regulariza al sellar | ⛔ pendiente |

**El cambio de nombres se aplica sitio por sitio, nunca por reemplazo automático** (ADR-044 §4:
un reemplazo masivo produjo cuatro reversiones el 2026-08-07).

## 10 · Lo que este ADR NO decide

- **Cuándo se construye el circuito de adquisición asistida.** Fija qué es; no su calendario, que
  depende del presupuesto de API.
- **Si QUIRA constituye alguna vez un observatorio del art. 79.** Deja la puerta abierta y dice
  qué la cerraría.
- **El estatuto de la evidencia aportada** (ADR-041 §6), que sigue pendiente de decisión.
- **La formulación de proyectos para convocatorias** —marco lógico, teoría del cambio, salida en
  el idioma del financiador— que Javo planteó el 2026-08-08 y que el archivo TERRA ya describía
  en su Fase 6. **Queda deliberadamente fuera**, no por olvido: este ADR supersede la fila de
  *adquisición* de ADR-043 §2, y formular un proyecto no es adquirir evidencia — es usarla.
  Tiene su propio contrato de salida (OSC, ONG, fundaciones y organizaciones territoriales) y su
  propia pregunta abierta: si es un producto o una capacidad de la misma superficie. Esa pregunta
  choca con **QUIRA Cooperación**, que sirve a quien **da** el dinero mientras esto serviría a
  quien lo **pide** —distinto usuario y distinta entrega, que por el test de ADR-043 §3 es
  precisamente lo que separa un producto de una vista—. Se decide en su propio ADR, con el mismo
  test, y **no reabre ADR-044**. Lo único que este ADR sí fija por adelantado: **no se llamará
  «QUIRA Ciudadana»**, porque sería reinstalar la segunda puerta que acaba de cerrarse.

---
*ADR-045 · Dylus Lab © 2026 · supersede ADR-043 §2 · deriva de ADR-043 y ADR-044.*
