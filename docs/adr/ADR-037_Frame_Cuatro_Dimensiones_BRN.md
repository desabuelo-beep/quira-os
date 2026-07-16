# ADR-037 · El frame de las 4 dimensiones — la BRN entra donde estaba Convergencia

**Estado:** PROPUESTO · 2026-07-16 (Javo decide · director técnico redacta) · **pendiente de ratificación**
**Contexto de origen:** revisión del Centro de Inteligencia Territorial. Javo: *"Territorio es el
punto de encuentro entre las QUIRA's en el territorio. Inteligencia debería ser QUIRA IA.
Convergencia debería salir para colocar aquí a la BRN."*
**Relacionado:** frame canónico (Javo · 2026-06-21) · ADR-024 (6 productos · las 6 QUIRAs) ·
ADR-035 (BRN) · Regla 9 (ningún cambio nace en Python).

---

## Contexto

El Centro de Inteligencia Territorial abre con un **frame de 4 dimensiones**, declarado canónico
el **2026-06-21** y **universal a las 6 QUIRAs** (el contenido cambia; el frame no):

```
¿Qué?       → Gobierno       · la institución y sus investigaciones
¿Dónde?     → Territorio     · el cantón en el mapa
¿Por qué?   → Inteligencia   · QUIRA lee y anticipa
¿Con quién? → Convergencia   · el encuentro entre las QUIRAs
```
Con una frontera explícita: *la ACCIÓN (¿y ahora qué?) la cierra el GOBIERNO, fuera de QUIRA:
QUIRA informa y conecta, no actúa.*

**El problema:** Javo precisa que **Territorio ES el punto de encuentro entre las QUIRAs en el
territorio**. Si eso es así, **Convergencia queda redundante**: el "¿con quién?" ya vive en el
"¿dónde?". Y al mismo tiempo, la **BRN** (ADR-035) no tiene lugar propio: hoy no es un dominio
—no observa una capacidad del Estado— pero es la **fuente de la lógica normativa** de todo el
sistema.

## Decisión

### 1. El frame pasa a: Gobierno · Territorio · Inteligencia · **Norma (BRN)**
```
¿Qué?         → Gobierno      · la institución, el mandato y sus investigaciones
¿Dónde?       → Territorio    · el cantón en el mapa · Y el encuentro entre las QUIRAs (GEO IA)
¿Por qué?     → Inteligencia  · QUIRA IA conversacional: lee, explica y anticipa
¿Bajo qué norma? → BRN        · Biblioteca de Reglas Normativas: de qué ley nace cada verificación
```
**El frame sigue siendo universal a las 6 QUIRAs**: las cuatro preguntas aplican a cualquiera
—toda QUIRA observa algo, en algún territorio, lo explica, y lo verifica **contra una norma**—.
La frontera se conserva intacta: **QUIRA informa y conecta; no actúa.**

### 2. Por qué la BRN es una dimensión legítima y no un parche
Es la pregunta que **sostiene a las otras tres**: sin norma verificada no hay dato (Regla 3), y
QUIRA no certifica verdad sino **verificabilidad** (Principio Rector). Los dominios ya la
ejercen —d02 y d03 muestran la cadena *Norma → Regla → Indicador → Señal*—, pero la biblioteca
que la alimenta no tenía lugar visible. **"¿Bajo qué norma?" es tan estructural como "¿qué?",
"¿dónde?" y "¿por qué?".**

### 3. Convergencia no se pierde: se absorbe
El encuentro entre las QUIRAs **pasa a Territorio** (donde ocurre de verdad: en el mapa, entre
cantones). No se elimina una capacidad: **se ubica donde corresponde** y se libera el cuarto
espacio, que estaba reservado a algo aún "— próximamente —".

### 4. Consecuencias en la interfaz (implementación, no doctrina)
- **Gobierno** muestra el mandato: alcalde, movimiento, inicio y fin de gestión, cuenta regresiva
  y nómina del concejo. **Solo lo verificado** (§5).
- **Inteligencia** absorbe el botón *"Preguntar a QUIRA"*: si Inteligencia **es** QUIRA IA, un
  botón aparte lo duplica. Se elimina también el chip **"Ejecutivo"**.
- La **BRN sale de la franja de dominios** (nunca fue un dominio) y ocupa la 4ª dimensión.
- La franja superior recibe **subtítulo propio**, como *ÁREAS DE GESTIÓN* lo tiene abajo.

### 5. LÍMITE DURO — solo se publica lo verificado (Regla 3)
Al construir Gobierno se auditó el canon:

| Dato | Estado |
|---|---|
| Alcalde · movimiento · **posesión 2023-05-14** | ✅ verificado (SCHEMA_CNE) |
| **Inicio 14-05-2023 · fin 13-05-2027** | ✅ **dictado por Javo (2026-07-16)** → debe cargarse en el canon (SCHEMA_CNE), no en el código |
| Vice-Alcalde, 3 Concejales Urbanos, 2 Rurales, Pdte. Junta La Pila | ❌ **7 de 8 sin dato** |

**La nómina del concejo NO se publica hasta que exista en el canon.** Se muestran los cargos con
su **ausencia declarada** — que es un resultado de auditoría, no un hueco a rellenar. El
contador se alimenta de las fechas **del canon**; si no están, no hay contador.

## Consecuencia práctica

El Centro de Mando deja de ofrecer una dimensión "próximamente" y pasa a exhibir **la columna
vertebral epistemológica de QUIRA**: qué observa, dónde, por qué lo afirma y **bajo qué norma lo
verifica**. La BRN deja de ser un frente interno y se vuelve **visible como lo que es: la fuente
de autoridad de todo el sistema**.

---
*ADR-037 · El frame de las 4 dimensiones · Dylus Lab © 2026 · "Convergencia no se elimina: se muda al territorio, que es donde las QUIRAs se encuentran de verdad. Y en su lugar entra la pregunta que sostiene a las otras tres: ¿bajo qué norma?"*
