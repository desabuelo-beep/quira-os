---
id: PCD-D06
authority:
  parent: PROTOCOLO_CURACION_DOMINIO
  constitution_articles: [1, 2, 3, 4]
  type: EXPEDIENTE
status: CERRADO con hueco declarado — silo S6 abierto
fecha: 2026-08-10
---

# PCD-D06 · Salud Institucional (QINV-006)

> **Pregunta canónica del dominio:** *¿tiene esta institución capacidad para sostener el
> gobierno?* (Diccionario d06 · campo 6). Ancla en **ICPI** — cumplimiento sostenible de
> funciones (`MAPA_ANCLAJE_MOTOR`).

## Estado inicial

d06 llegó a esta curación **funcionalmente vivo**, no a medio construir. Conviene decirlo así
desde el principio porque el diagnóstico contrario estaba a mano y era falso.

- **UI**: `m1_situacion` (QINV-006 sobre el kernel UMI) con tres cuerpos de evidencia —
  `p_ejecutivo` · `p6_pulso` · `p7_brecha`.
- **Datos**: leídos del snapshot, sin `demo_data`, y **contrastados contra el motor v5.6** el
  2026-08-05 (`_meta.verificacion_2026_08_05`).
- **Documentación previa**: `d06_MAPPING_MATRIX.md` (2026-06-15), con un plan de cableado.

**El documento de junio quedó desactualizado, y en la dirección buena:** describe los widgets
leyendo `_raw_h73.*`, una interfaz que ya no se usa. El código fue re-cableado a la estructura
del snapshot (`vectores`, `territorial`, `sat_gm`, `icpi`, `tgi`). La matriz envejeció porque el
dominio avanzó.

## Hallazgos de la auditoría de 7 capas

| Capa | Resultado |
|---|---|
| **1 · Gold Master** | ✅ ICPI 27,46 · TGI 66,79 (d1…d5 83,20/69,93/59,85/44,79/100,00) · IGP 48,33 — coinciden con el motor |
| **2 · Metodológica** | ✅ pregunta y ancla canónicas · ⚠️ `CHK-08` pendiente (ICPI 2026 = T_i_2026) |
| **3 · Matemática** | ✅ los 6 vectores causales tienen clave real · 🔴 **falta ICM** (silo S6) |
| **4 · Semántica** | ✅ `vectores._nota` ya separa clave interna de `label` público — Firewall previsto en el dato |
| **5 · Cableado** | ✅ Excel → snapshot → módulo, sin pérdidas · matriz de junio desactualizada |
| **6 · Visual** | 🔴 **el kernel tenía paleta propia con verde de «bien»** |
| **7 · Narrativa** | 🟡 la ausencia se declaraba, pero no era accionable |

### H-1 · El kernel de expedientes tenía una segunda verdad visual

`quira_pages/umi.py` definía su propia paleta —`#FF4D4D`, `#FFB020`, `#00D4FF`, **`#22C55E`**—
al margen de `utils/css_tokens`. **No es un rincón: ese módulo renderiza todos los expedientes
QINV**, así que el desvío alcanzaba a cada dominio curado.

Lo de fondo es el verde. El sistema visual **no tiene color de «bien»** porque QUIRA mide
verificabilidad y no bondad: pintar de verde a un municipio es un juicio de valor que este
sistema no puede emitir. Con ICPI en 27,46 % la rama nunca se activaba en Montecristi —
**el defecto estaba latente, esperando al primer municipio que puntuara alto.**

### H-2 · Un fallo técnico era indistinguible de una ausencia de evidencia

`_cargar()` capturaba toda excepción y devolvía `{}`. Un error de lectura y un corte sin datos
producían **la misma pantalla**. Son cosas distintas: una se arregla, la otra se consigue.

### H-3 · La ausencia se declaraba, pero no se podía hacer nada con ella

La rama sin evidencia decía «cargue el corte» — una instrucción de operador, dirigida a quien no
está mirando esa pantalla. ADR-046 §2.4 exige decir **qué falta, por qué falta y cómo se
consigue**.

### H-4 · El hueco mayor: el silo S6 no tiene quien lo cure

`MATRIZ_CABLEADO_CANONICO` lo registra sin adornos: *«d00, d05 y d06 no existen en
`app/agents/`. Tres silos del motor no tienen dominio que los cure — S1 electoral, S6 SIGAD y
S9 ODS. Eso es un hallazgo, no un error de la matriz.»*

El silo de d06 es **S6 · `H08_S6_AUTOREPORTE_SIGAD`**, y lo que produce es la **brecha
`ICM − ICPI`**: la distancia entre lo que el GAD declara de sí mismo al reportarse al SIGAD y lo
que la evidencia sostiene. Con ella se enciende **SAT-I**, cuyo umbral —corregido por Javo en
OBS-023— es `ICM_Global ≥ 80 % AND pct_metas_reportadas ≤ 10 %`: **calificarse 80 sobre 100
habiendo reportado una de cada diez metas.** No mide fragmentación de contratos; mide
fragmentación del reporte (COPFP Art. 54).

Hoy la alerta **existe en el código y está apagada**: `sat_evaluator.py:297` — *«ICM / cobertura
metas no disponible (requiere SIGAD)»*. La materia prima ya está en el corpus:
`SIGAD-GAD-2023` (16 fragmentos) y `SIGAD-GAD-2024` (3).

## Cambios

**Visual (H-1).** `umi.py` pasa a consumir `utils/css_tokens`. El mapeo de fondo:
`verde → C.SIN_SENAL` — *no hay nada que señalar aquí*, que es lo que ese estado significa de
verdad. El gate del sistema visual se amplía para cubrir el kernel: vigilaba los ambientes y
dejaba fuera el módulo que pinta cada dominio, es decir **protegía el marco y no el cuadro**.

**Gate (efecto secundario).** Al documentar en un comentario el color retirado, el propio gate
lo volvió a encontrar. Se corrigió el gate, no el comentario: ahora tokeniza y descarta los
comentarios de Python —que no llegan al navegador, a diferencia de los de CSS, motivo por el que
el gate de la portada trata ese caso al revés—. Verificado con prueba negativa: inyectado
`#22C55E` en código real, el gate sigue fallando.

**Cableado (H-2).** `_cargar()` devuelve `(datos, motivo)` y distingue `error_tecnico` de
`sin_datos`.

**Narrativa (H-3).** d06 es **el primer dominio que aplica ADR-046 §2.4**. Sin evidencia, la
pantalla nombra lo que falta (cédula presupuestaria y reportes de ejecución del período), dice
que puede pedirse por solicitud de acceso o aportarse, y añade la salvaguarda de §2.5: que la
evidencia llegue por esa vía **enciende la lectura del territorio y deja constancia igual de que
no estaba publicada**. En la rama de fallo técnico dice explícitamente que **no es ausencia
documental y no corresponde al municipio.**

## Cambios en el canon

**Ninguno.** No se tocó el Gold Master, ninguna fórmula, ningún valor del snapshot. Todo lo
corregido está en la capa de presentación y en los gates. `H12!B33` intacta.

## Validación

| | |
|---|---|
| `check_sistema_visual` | verde · 5 ambientes, ningún verde de «bien» |
| Prueba negativa del gate | inyectado `#22C55E` en código → falla (exit 1) |
| `smoke_cajones` | 20/20 (10 destinos × 2 roles) |
| `check_errores_silenciosos` | verde |
| `check_health` · `check_consistencia` | verde |
| Excel ↔ Python | ICPI 27,4582 · TGI 66,787 · IGP 48,33 — coinciden |

## Estado final

**d06 queda cerrado como sintetizador, con su silo de entrada declarado abierto.** La distinción
importa y conviene dejarla escrita:

> **d06 no es un extractor: es el dominio que sintetiza evidencia producida por otros.** No debe
> convertirse en un agente que genere su propia verdad. Que no exista `app/agents/d06` no es una
> carencia del dominio — es coherente con su naturaleza. Lo que sí falta es el **insumo S6**.

Por eso la formulación correcta no es «d06 está incompleto», sino:

> d06 está funcionalmente vivo como sintetizador; permanece abierta la incorporación del silo S6
> de autorreporte SIGAD, cuya ausencia impide calcular el ICM y la brecha `ICM − ICPI` con el
> mismo nivel de evidencia que los demás vectores.

**Lo que queda abierto**, ya dimensionado y sin maquillar:

| # | Qué | Efecto de no tenerlo |
|---|---|---|
| 1 | Silo S6 → ICM → brecha `ICM − ICPI` | **SAT-I apagada** — no se mide la fragmentación del reporte |
| 2 | `CHK-08` · ICPI 2026 = T_i_2026 | validación metodológica del corte vigente |
| 3 | Las 4 congruencias del Pulso | requieren juicio de C3; hoy no tienen clave real |
| 4 | `d06_MAPPING_MATRIX` desactualizada | describe `_raw_h73`, retirado — se mantiene como registro de época |

**La pregunta técnica de la siguiente etapa queda limpia y aislada:** si la extracción del ICM
desde los documentos SIGAD puede hacerse de forma determinista o necesita modelo. Esa decisión
pertenece a la construcción de S6 y **no contamina este cierre**.

---
*PCD-D06 · Dylus Lab © 2026 · auditoría de 7 capas · canon sin cirugía · silo S6 declarado abierto.*
