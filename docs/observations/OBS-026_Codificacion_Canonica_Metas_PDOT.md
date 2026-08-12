---
id: OBS-026
authority:
  parent: ADR-047
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-12
dominio: d01 · d06 · motor
estado: VERIFICADA
---

# OBS-026 · El PDOT no tiene llave primaria — y sin ella nadie puede auditar su propio plan

> **Hallazgo de Javo (2026-08-12):** *«el GAD no crea codificación real para la trazabilidad que
> permita monitorear y evaluar su propio PDOT»*. Registrado para d01.

## El problema, y por qué no es un detalle técnico

Los PDOT presentan sus metas como **texto narrativo en tablas informativas, sin identificador
estable**. Los correlativos locales —`M001`, `M002`— son orden de escritura, no llaves: no dicen
a qué sistema pertenece la meta, y no son comparables entre municipios.

Consecuencias, todas verificadas en este proyecto:

1. **Ningún cruce intersistémico es posible sin inferencia.** Para unir una meta del PDOT con una
   actividad del POA, una partida de la cédula y un proceso del SERCOP hace falta emparejar
   **texto**. El 2026-08-11 el director lo intentó: el mejor emparejamiento automático dio
   **puntajes de una a dos palabras comunes** —«gestión del riesgo» empataba con «mantener
   porcentualmente la gestión de…»— y hubo que descartarlo por no ser evidencia.
2. **El texto es mutable.** Una coma, un redondeo o un truncamiento en una hoja de cálculo rompen
   la correspondencia. De las 66 metas, **8 no coincidían literalmente** entre el Excel de
   contraste y el PDOT: mismas metas, cifras distintas.
3. **Una reforma del plan destruye el histórico.** Si el municipio reordena o renumera, los
   correlativos pierden sentido y la serie de auditoría se corta.

> **Sin llave primaria, un municipio no puede evaluar su propio plan de forma reproducible.** No
> es que no quiera: es que el instrumento no lo permite.

## La codificación canónica QUIRA

Diseñada por Javo (2026-08-12). Formato:

```
M-[COMPONENTE]-O[OBJETIVO]-[SECUENCIA]
```

| Parte | Qué es |
|---|---|
| `M` | prefijo inalterable — el registro es una meta oficial de planificación territorial |
| `COMP` | sistema territorial del PDOT, 3 letras |
| `O#` | objetivo estratégico del componente al que tributa |
| `##` | ordinal de dos dígitos dentro de ese objetivo |

### Los seis componentes — literales, no glosables

**Son los sistemas del PDOT que fija la norma. No se abrevian por su parecido fonético.**

| Código | Componente | Comprende |
|---|---|---|
| **BIO** | **Biofísico y Ambiental** | recursos naturales, cambio climático, taludes, fauna |
| **ASE** | **Asentamientos Humanos y Servicios Públicos** | agua potable, alcantarillado, desechos, infraestructura sanitaria, vivienda |
| **MOV** | **Movilidad, Energía y Conectividad** | vías, señalización, tránsito, redes pluviales |
| **SOC** | **Sociocultural y Derechos** | salud, educación, cultura, patrimonio, grupos de atención prioritaria |
| **ECO** | **Económico y Productivo** | fomento productivo, turismo, comercio |
| **POL** | **Político-Institucional y Gobernanza** | transparencia, TIC, capacidad institucional, finanzas, participación |

> ⛔ **Lectura errónea detectada y corregida (Javo · 2026-08-12):** glosar `BIO` como «biológico»,
> `ASE` como «asesoramiento» y `MOV` como «movimiento». **Rompe la correspondencia con los
> sistemas del PDOT**, que son los que la norma fija. Los códigos son abreviaturas de los
> sistemas, no palabras sueltas.

**Ejemplo:** `M-ASE-O1-04` — Asentamientos Humanos y Servicios Públicos, objetivo 1, meta 04
(*«Aumentar del 39,25 % al 42,38 % la cobertura de agua potable…»*).

## Verificación de la codificación

| Comprobación | Resultado |
|---|---|
| 66 códigos canónicos únicos | ✅ |
| `M001`–`M066` sin huecos ni repetidos | ✅ |
| Formato `M-COMP-O#-##` bien formado en las 66 | ✅ |
| Suma por componente | ✅ BIO 6 · ASE 16 · MOV 13 · SOC 13 · ECO 5 · POL 13 = 66 |
| Ejecutores | ✅ 54 GAD · 6 empresa pública · 6 adscrita — coincide con el registro maestro |
| Puente Motor ↔ PDOT, 25 filas | ✅ |
| `PI-I-G-01` declarado *sin correlato* | ✅ declarado, no forzado |

## El caso `M009` — resuelto con evidencia, no con interpretación

Dos códigos del motor apuntan a la misma meta del PDOT:

```
M009 «Contar con capacidad para disposición final de desechos sólidos…»
   ← AH-I-N-01   Gestión desechos sólidos
   ← FA-DIS-01   Disposición final desechos
```

**La pregunta decisiva no es si son dos competencias distintas** —eso es interpretación—, sino si
**se alimentan del mismo dato**. Verificado en H13:

| | `V_SERCOP` | `V_eSIGEF` | `V_LOTAIP` | `V_CPCCS` | `Vi` |
|---|---|---|---|---|---|
| `AH-I-N-01` | 1 | 1 | 0 | 0 | 0,5 |
| `FA-DIS-01` | 0 | 0 | 1 | 1 | 0 |

**Exactamente complementarios. Ningún verificador compartido.** Una acredita por contratación y
devengado; la otra por publicación y rendición. Si fuera la misma meta duplicada, las filas serían
idénticas — y no coinciden en ninguna de las cuatro columnas.

**No hay doble contabilidad.** Y un detalle lo confirma: `FA-DIS-01` aporta **cero** al numerador
(`Vi = 0`, sin núcleo financiero no hay puntuación). Quien duplicara una meta para inflar el
índice no dejaría la copia en cero.

### Regla que queda fijada

> **`M009` es una meta de enunciado único con evidencia disjunta.** Tributa a `AH-I-N-01` por la
> operación del servicio y a `FA-DIS-01` por la disposición final, **con verificadores
> independientes**. Peso acumulado `Pi = 0,0422`. No se fusionan: fusionarlas eliminaría una
> dimensión que hoy se verifica por separado.

Por eso el puente tiene **23 IDs distintos para 24 correlatos**, y es correcto.

## Lo que este hallazgo aporta más allá de Montecristi

La codificación no resuelve un problema de un municipio: resuelve **una carencia estructural del
instrumento**. Cualquier GAD que quiera medir su propio PDOT enfrenta lo mismo — y hoy la
alternativa es emparejar texto, que no es reproducible.

Es replicable a los 222 sin cambiar nada: los seis sistemas territoriales son los que fija la
norma, y la numeración se deriva del propio plan.

---
*OBS-026 · Dylus Lab © 2026 · codificación de Javo · verificada contra el motor y el registro maestro.*
