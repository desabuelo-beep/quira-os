# ADR-038 · La BRN — capa de conocimiento normativo del ecosistema (opera sobre CNO, no artículos)

> **Definición canónica (colega · 2026-07-17):** *La BRN no es una biblioteca de reglas ni un
> motor de cálculo. Es la **capa de conocimiento normativo** del ecosistema QUIRA. Su función es
> transformar el ordenamiento jurídico vigente en **reglas operativas únicas, trazables y
> reutilizables** por las SAT, los DOM y QUIRA IA, manteniendo un **único punto de verdad
> normativa**.*

**Estado:** PROPUESTO · 2026-07-17 (Javo decide · director técnico redacta · síntesis del colega) · **pendiente de ratificación**
**Contexto de origen:** el error del "65% = COOTAD Art. 192". La BRN v1 (ADR-035) catalogaba
**artículos aislados**; el error demostró que ese diseño es insuficiente. Javo: *"la BRN debe
trabajar con TODA la norma nacional… crear las condiciones lógicas con las cadenas de artículos
para operativizar la gestión pública"*. El colega converge: *"el Derecho no funciona por
artículos aislados; la regla emerge de una cadena normativa"*.
**Relacionado:** ADR-035 (BRN · esta es su v2) · ADR-032 (objeto canónico compartido) · ADR-023
(Regla 1/4 · el Gold Master es el único motor) · ADR-005 (corpus Supabase · SHA256) · Regla 3
(sin norma verificada, no hay dato) · Regla 9 (nace en el canon).

---

## Contexto — por qué v1 falló

La BRN v1 preguntaba *"¿qué dice el artículo X?"*. Pero un artículo, por sí solo, **rara vez
expresa una regla jurídica completa**. La regla del 65% de asignación mínima prioritaria no vive
en ningún artículo: **emerge de una cadena**:
```
CE Art. 271  →  COOTAD Art. 192 (reformado por COOTAD-2026 Art. 3)
             →  Art. 198.1 (regla · COOTAD-2026 Art. 4)  →  198.2 (gasto computable)
             →  198.6 (incumplimiento → Contraloría · COOTAD-2026 Art. 7)
             →  Disposición Transitoria Primera  →  umbral 65% (desde 1-dic-2026)
```
El director citó solo el Art. 192 y concluyó que el 65% era falso. **El error no fue de lectura:
fue de diseño.** Preguntar por artículos aislados invita a tomar porciones. La BRN debe hacer
imposible tomar una porción.

## Decisión

### 0. La BRN es una CAPA, no un módulo (precisión del colega — la pieza que faltaba)
Prueba: *¿puede existir QUIRA sin BRN?* No. Un módulo puede desaparecer; la BRN no. Por tanto
**no es un cajón**: es una **capa transversal bajo todo el ecosistema** — todo pasa por ella.
```
QUIRA IA
  DOM
    SAT
════════ BRN — capa de conocimiento normativo (único punto de verdad normativa) ════════
  Gold Master · Corpus · Canon
```
Su **cajón** (4ª lente del frame · ADR-037) es solo su **cara de auditoría** para el humano —
`📖 Base de Reglas Normativas`: lista las CNO, su estado, vigencia, SHA, normas involucradas y
las SAT/DOM que las consumen. **No calcula, no decide: permite auditar el cerebro.**

**Consecuencia en QUIRA IA:** consulta **la BRN primero**; solo si la BRN no tiene la regla,
baja al Corpus. Como un abogado: primero la doctrina consolidada, después abre la ley. **Con una
salvaguarda (Regla 3 · Principio Rector):** la BRN no "sabe" — la respuesta de toda CNO **apunta
siempre al Corpus con el SHA de cada eslabón**. El Corpus prueba; la BRN organiza el camino.
Ninguna CNO responde sin traza al texto verificado, o sería una IA interpretando Derecho.

### 1. El nodo de la BRN es la REGLA, no el artículo — la Cadena Normativa Operativa (CNO)
La BRN deja de almacenar artículos. Almacena **Reglas de Negocio Públicas**, cada una como una
**CNO**: una unidad viva que consolida toda la cadena que la sostiene. Los artículos pasan a ser
**evidencia** de la CNO, no su objeto.
```
CNO-IV-001 · Regla de Asignación Mínima Prioritaria
  ├── fundamento constitucional : CE Art. 271
  ├── fundamento legal          : COOTAD Art. 192 · 198.1 · 198.2 · 198.6
  ├── reforma                   : COOTAD-2026 (Arts. 3, 4, 7)
  ├── disposición               : Transitoria Primera
  ├── metodología / procedimiento: (Min. Finanzas · seguimiento anual)   ← si está en el canon
  ├── variable(s)               : Pct_Gasto_No_Permanente
  ├── umbral                    : 65 %  (desde 1-dic-2026)
  ├── dominios que la consumen  : d02
  ├── señal que la materializa  : Alerta fiscal (Gold Master · H24_SAT-IV)
  ├── estado                    : propuesta | vigente | derogada
  └── SHA256                    : de CADA eslabón de la cadena
```
**Consultar una CNO obliga a recorrer toda su cadena.** Ninguna IA —ni ningún humano— podrá citar
un artículo aislado creyendo que entendió la regla.

### 2. La relación cambia: `Ley → BRN → SAT` (antes `Ley → SAT`)
Hoy la SAT lleva su fundamento jurídico escrito adentro (y por eso hereda lecturas parciales).
En v2, **la SAT ya no conoce la ley**: lleva **solo el ID de la CNO** que consume.
```
antes:  SAT-IV  →  "Art. 192"                (frágil · lectura parcial)
v2:     SAT-IV  →  CNO-IV-001                 (la CNO conoce toda la cadena)
```
La **BRN conoce el Derecho; la SAT consume una regla ya curada.** Es el **objeto canónico
compartido** (ADR-032) llevado al plano normativo: la regla nace UNA vez, y todo dominio o señal
que la necesite la **referencia**, no la recopia.

### 3. LÍMITE DURO — la BRN DESTILA, no calcula (Regla 1 + Regla 4)
El colega la llama "Motor de Operativización Normativa": es un motor de **conocimiento**, no de
cálculo. La CNO provee la **regla, la variable y el umbral**; el **Gold Master** (único motor)
**computa** la señal con ese umbral. Una BRN que calculara métricas sería el motor de cálculo
paralelo prohibido. *La BRN dice cuál es la regla vigente; el Gold Master mide si se cumple.*

### 4. Dos capas separadas (arquitectura del colega)
- **Capa 1 · Corpus Jurídico Nacional** (Supabase · SHA256, ya existe con 12.992 chunks): el
  **texto oficial íntegro**. No se sube "solo normas": se sube **todo lo que genera obligación
  operativa** (regla del colega) — Constitución, leyes, **reglamentos, reformas, resoluciones,
  acuerdos, manuales, metodologías, procedimientos, instructivos, normas técnicas y dictámenes
  vinculantes**. El 65% no nació de una ley sola: nació de una reforma + una transitoria; el
  próximo puede nacer de una metodología del Ministerio de Finanzas. **Falta subir el resto.**
- **Capa 2 · BRN** (las CNO): el puente que traduce el Derecho en reglas operativas. Contiene la
  regla, su cadena completa, variables, indicadores, dominios que la consumen, vigencia, evidencia
  y SHA. **No recopia texto: referencia el corpus.**

### 5. La BRN trabaja por DOMINIOS NORMATIVOS, no artículo por artículo
No se cataloga el corpus linealmente. Se destila por **dominio normativo**:
```
Finanzas Públicas Municipales  →  N normas · M artículos · K metodologías  →  CNO-IV-*
Participación Ciudadana        →  …                                        →  CNO-PC-*
Talento Humano                 →  …                                        →  CNO-TH-*
```
Cada dominio normativo produce sus CNO reutilizables por todas las SAT del ecosistema.

### 6. Regla constitucional — validación humana, reforzada (ADR-035 §5)
Cadenas más complejas ⇒ **más** necesidad de validación humana, no menos.
`Norma → Extracción de la cadena → PROPUESTA de CNO → VALIDACIÓN HUMANA → BRN → Gold Master → SAT`.
Toda CNO nace `propuesta`. **Solo Javo la promueve a `vigente`.** Ninguna IA deriva ni declara
vigente una CNO por su cuenta — el error del 65% es la prueba de por qué.

### 7. Nueva unidad documental — el archivo CNO (propuesta del colega)
Junto a ADR/OBS/PCD/BOOT nace la **CNO** como unidad viva del canon: cada regla operativa con su
cadena, versionada y auditable. *(Formato y ubicación se definen al construir el piloto.)*

## Consecuencia práctica

**Las SAT ya canonizadas son el germen, no el conflicto** (Javo). No se fusionan ni se reemplazan:
sueltan su fundamento jurídico disperso, ese fundamento se **consolida en una CNO**, y la SAT pasa
a **referenciarla**. Las 3 SAT financieras de d02 y la cadena del mandato de d03 son las primeras
candidatas a migrar. **El error del 65% queda estructuralmente imposible**: la CNO-IV-001 obliga a
recorrer `CE 271 → COOTAD 192/198.1-6 → Transitoria`, y el 65% aparece con toda su cadena o no
aparece. La v1 (catálogo de artículos · commit `e003a7d`) queda **superada**.

**Orden de trabajo (corregido por el colega — el MOLDE antes que el piloto):**
1. Ratificar este ADR.
2. **Definir el MOLDE de una CNO** (identificador · nombre · estado · vigencia · cadena normativa ·
   variables · procedimientos · metodologías · SAT consumidoras · DOM consumidores · evidencias ·
   SHA). *Esa estructura no debe cambiar nunca:* si el molde cambia tras migrar 80 CNO, se
   reconstruye todo. Es el error del catálogo de artículos, otra vez, pero peor.
3. Inventariar la norma nacional en el corpus y subir lo que falta (todo lo que genera obligación
   operativa · §4).
4. Migrar la **CNO-IV-001** (asignación mínima prioritaria) como piloto — la misma regla que rompió
   la v1, ahora sobre el molde definitivo.
5. Reconstruir `brn_catalogo.py` como catálogo de CNO · enlazar SAT → CNO.

---
*ADR-038 · BRN sobre Cadenas Normativas Operativas · Dylus Lab © 2026 · "El error del 65% no fue leer mal un artículo: fue creer que un artículo era una regla. La BRN no almacena Derecho: lo destila en reglas operativas verificables. La ley manda, la BRN la consolida, el Gold Master la mide, QUIRA la explica — y nadie vuelve a tomar una porción."*
