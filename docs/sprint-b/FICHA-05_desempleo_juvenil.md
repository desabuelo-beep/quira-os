# FICHA DE EXPLICABILIDAD QUIRA — 05
**Caso: Desempleo Juvenil · Cantón Montecristi · 2026**
*Sprint B.1 Diagnóstico · 2026-06-09 · pronóstico 🔴 — caso de frontera deliberado*

---

## Caso

Empleo juvenil en Montecristi: ¿puede el sistema explicar la situación
laboral de los jóvenes del cantón con la información disponible?

---

## ¿Qué pasa?

**Lo que el sistema sabe (mejor de lo pronosticado):**
- **Tasa de desempleo cantonal: 4.35 %** (2022), con meta del plan de
  desarrollo de reducirla a **3.73 %** — vinculada a ODS 1 y ODS 8.
- **Estructura del empleo formal** (Registro Estadístico de Empresas,
  INEC 2022): las empresas grandes generan el **65 % del empleo** (10,239
  plazas); microempresas 13 % (2,023); pequeña empresa 10 % (1,260);
  medianas 12 % (1,285). Total formal registrado: ~14,800 plazas.
- Montecristi es el **3er aportante de plazas de empleo de Manabí**.
- Señal educativa relevante: entre 2001 y 2022 la matrícula creció 107 % en
  inicial y 97 % en bachillerato, pero solo **44 % en nivel universitario**
  — el embudo se estrecha justo donde se forma el empleo calificado.

**Lo que el sistema NO sabe (el caso de la ficha):**
- La **tasa de desempleo JUVENIL no existe** — ni en el plan de desarrollo
  ni en el corpus. La tasa 4.35 % es general; la juvenil suele duplicarla o
  triplicarla (patrón nacional), pero **afirmarlo sería estimar sin fuente**
  — el sistema no estima (regla de gobernanza).
- Tampoco existe desagregación parroquial de empleo ni de población joven
  ocupada.

**Semáforo: ⚪ NO MEDIBLE con datos propios — frontera del sistema confirmada.**

## ¿Por qué pasa?

Lo demostrable con el corpus:
1. **Dependencia de pocas empresas grandes:** 2 de cada 3 empleos formales
   dependen de empresas grandes — el FODA del plan registra "no cuenta con
   suficiente especialización económica de la población" como debilidad.
2. **El embudo educativo:** el crecimiento universitario (44 %) es la mitad
   del de bachillerato (97 %) — los jóvenes terminan el colegio y el
   territorio no ofrece el siguiente escalón.
3. **El tejido microempresarial es pequeño** (13 % del empleo) para absorber
   a quienes no entran a la empresa grande.

*(Cadena causal construida con datos cantonales generales — sin el dato
juvenil específico, es contexto, no diagnóstico juvenil.)*

## ¿Dónde pasa?

**Sin respuesta territorial.** No existe empleo por parroquia en ninguna
fuente del sistema. Único proxy: la demografía por unidad territorial del
diagnóstico (estructura de edades) — insuficiente para localizar desempleo.

## ¿Cuánto cuesta no resolverlo?

**Sin cuantificación posible hoy.** No hay tasa juvenil, no hay costo de
inacción calculable. La meta del plan (4.35 → 3.73) implica ~?? plazas — ni
siquiera eso es computable sin la PEA del cantón en el corpus (Gap G-19).

## ¿Qué recursos existen?

**Vacío del radar confirmado (segunda instancia de G-15):** la base de
fondos no tiene ninguna convocatoria con tema empleo, juventud o desarrollo
productivo. Las 11 convocatorias actuales cubren: agua (3), gobernanza/
transparencia (5), género (2), democracia (1). **Empleo juvenil: 0.**

Emisores ancla con líneas relevantes existen (BID: desarrollo local;
cooperación española: formación profesional) — el radar aún no los barre
con esos términos.

---

## Evidencia

1. PDOT Bicentenario 2023 — META-MNT-ECO-001 (desempleo 4.35 → 3.73, ODS 1/8,
   p. 385-387) · estructura REEM (p. 320) · FODA económico (tabla 173, p. 338)
2. INEC — Registro Estadístico de Empresas 2022, serie educativa 2001-2022
3. Base de fondos D02 — barrido de cobertura temática (0 matches empleo)

## Nivel de confianza

| Pregunta | Confianza | Razón |
|---|---|---|
| ¿Qué pasa? | **Media** (contexto) / **Nula** (juvenil) | Tasa general sólida con meta; tasa juvenil inexistente |
| ¿Por qué? | **Media** | Cadena estructural demostrable, pero no específica de jóvenes |
| ¿Dónde? | **Nula** | Sin desagregación territorial de empleo |
| ¿Cuánto? | **Nula** | Sin PEA en corpus, sin tasa juvenil |
| ¿Recursos? | **Media** | Vacío del radar verificado — fondos existen afuera |

**Resultado del caso: 2/5 parciales + 3 sin respuesta. El pronóstico 🔴 se
confirma — y eso era el propósito: esta ficha ES el mapa de la frontera.**

## Gaps detectados

| ID | Tipo | Descripción | Dónde debería vivir | Esfuerzo |
|---|---|---|---|---|
| G-18 | Dato (estructural) | Tasa de desempleo juvenil (15-29) no existe en ninguna fuente del sistema — fuente natural: ENEMDU/INEC (dato cantonal puede requerir solicitud específica) | Fuente externa INEC → corpus | Alto |
| G-19 | Dato | PEA cantonal no está en el corpus (impide convertir metas % en plazas) | Corpus PDOT (verificar) o INEC Censo 2022 | Bajo |
| G-20 | Radar | Términos empleo/juventud/desarrollo productivo ausentes del fetcher D02 (segunda instancia del patrón G-15) | `app/fetchers/` términos radar | Medio |
| G-21 | Dato | Empleo por parroquia inexistente — candidato a explotación del censo INEC 2022 (ocupación por parroquia existe en censo) | Fuente externa INEC | Medio |

## Acción propuesta (ejecutar en B.2 — no ahora)

1. **G-19 primero** (barato): verificar PEA en el resto del corpus; si no
   está, es un dato público INEC inmediato.
2. **G-20 con G-15** en un solo lote: ampliar términos del radar (movilidad +
   empleo + juventud) — una sola intervención al fetcher.
3. **G-18/G-21**: paquete INEC (ENEMDU cantonal + censo ocupación parroquial)
   — vía pública o D12-003 al descongelar. Mismo paquete que G-09 género.

**Patrón consolidado para B.2:** los gaps externos convergen en UN paquete
INEC (género G-09 + empleo G-18/G-21 + PEA G-19) y UNA intervención al radar
(G-15 + G-20). Dos acciones cierran siete gaps.

---

*Referencia interna (omitir en versión demo): PDOT_MONTECRISTI_KB_a59cd286.md
L1984-1985 (META-MNT-ECO-001/TUR-004: 4.35→3.73) · L1045-1054 (REEM p.320) ·
L1108/L3832 (3er lugar, FODA tabla 173) · chunk PDOT-MONTECRISTI #10 (serie
educativa 107/97/44%) · fondos_convocatorias 11 filas 0 empleo ·
B1A: juventud 67 chunks/13 parroquiales (demografía solamente).*
*Ficha 5/6 · Sprint B.1 · QUIRA OS · Dylus Lab © 2026*
