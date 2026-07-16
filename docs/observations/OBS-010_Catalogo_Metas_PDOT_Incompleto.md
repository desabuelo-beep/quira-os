# OBS-010 · El catálogo de metas del canon está incompleto (25 de 66)

**Estado:** ABIERTO · 2026-07-15 · **bloquea la vinculación de d03**
**Origen:** Javo pide un "último filtro" antes de promover d03 y aporta el **Plan Plurianual
PDOT 2023-2027 GAD Montecristi** (`Holding_Municipal_Montecristi` · SHA256 `09a2aacc…`).
Ese filtro destapa el hallazgo. **Javo dictamina: el canon quedó incompleto** (no es un
subconjunto deliberado).
**Relacionado:** ADR-023 (Regla 1 · fórmula canónica INMUTABLE) · ADR-035 §5 (IA propone,
humano valida) · d01 Planificación · d03 Gobernanza del Mandato.

---

## El hecho

La matriz plurianual estructura cada sistema en columnas (`Sistema · Objetivo de Desarrollo ·
Objetivo Estratégico · Objetivo de Gestión · Política · Indicadores · **Meta** · Línea Base
2023 · anualización 2024-2027 · Programa · Proyectos · PND · ODS · Unidad Responsable`).
Contando la columna **Meta** de cada hoja:

| Sistema (hoja) | Metas |
|---|---|
| Físico-Ambiental (`1. FIS AM`) | 9 |
| Asentamientos (`2. ASEN`) | 26 |
| Socio-Cultural (`3.SOC`) | 13 |
| Económico (`4. EC`) | 5 |
| Institucional (`5. INST`) | 13 |
| **TOTAL PDOT** | **66** |
| **Gold Master** (`H04_S2_PLANIFICACIÓN_PDOT`) | **25** |
| **BRECHA** | **41 metas ausentes** |

> **Nota de método:** un primer conteo por patrón de texto dio ~92; era ruido (capturaba metas
> del PND, indicadores y objetivos). El conteo válido es **por estructura** (columna `Meta`):
> **66**. Se registra el error para que nadie reutilice la cifra equivocada.

**Verificación complementaria:** las **25 del canon SÍ existen todas en el PDOT** — ninguna
inventada, y los sistemas cuadran (Agua→ASEN · Salud→SOC · Turismo→EC · Riesgo→FIS AM). El
canon **no fabricó metas: tomó un subconjunto de 25 y dejó fuera 41**.

**El caso que lo destapó:** la promesa *"Gestionar la instalación de Infocentro"* (SC-017).
El director la vinculó como **Parcial** contra `AH-C-X-02` (información territorial),
forzándola porque no hallaba nada mejor entre las 25. Javo corrigió: es **Directa** contra una
meta social real —*"Incrementar el número de beneficiarios que acceden a puntos digitales de
19.265 (2023) a 23.265 (2027)"*, programa **Educa e Innova**, hoja `3.SOC` fila 7, con serie
anual completa (19265→20265→21265→22265→23265)—. **Esa meta no está en H04.** No faltaba la
nomenclatura: faltaba la meta.

## Por qué importa (afecta a dos dominios)

1. **d03 · el denominador es incompleto.** El índice de fidelidad pregunta *"¿la promesa llegó
   al plan?"* y lo responde contra 25 metas cuando el plan tiene 66. Una promesa **realmente
   incorporada** al PDOT puede aparecer como *sin correspondencia* solo porque su meta no está
   en el canon → **el índice subestima la fidelidad del mandato por construcción**.
2. **d03 · las 76 vinculaciones quedan comprometidas.** Se propusieron contra un catálogo
   parcial. Varias "forzadas" (Infocentro, albergue animal, marca ciudad) probablemente tienen
   su meta exacta esperando entre las 41 ausentes — SC-017 ya lo demostró.
3. **d01 · publica "25 metas · cobertura 96%".** Si el PDOT tiene 66, ese dominio mide
   cobertura sobre un universo recortado. **El hallazgo no es de d03: es del canon.**

## La tensión que NO se resuelve sin decisión de Javo

```
H12!B31 = SUM(J6:J30)      ← 25 filas
H12!B32 = SUM(K6:K30)      ← 25 filas
H12!B33 = B31/B32          ← ICPI · FÓRMULA CANÓNICA
```
**El ICPI se calcula sobre esas 25 metas.** Ampliar H04 obliga a ampliar ese rango — y eso es
**tocar la fórmula canónica que la Regla 1 declara INMUTABLE**. No hay salida trivial:

- **Ampliar** → se modifica el motor (prohibido sin decisión explícita de Javo) y el ICPI
  histórico deja de ser comparable: 2025 y 2026 medirían universos distintos (25 vs 66 metas).
- **No ampliar** → d01 y d03 siguen midiendo contra 25 de 66, y hay que **declararlo** en la
  UI: *"se mide contra las 25 metas estratégicas del modelo, no contra el PDOT completo"*.

## Estado

- **d03 CONGELADO.** La copia `_TRABAJO_d03_promesas.xlsx` conserva las **76 promesas reales**
  + la propuesta marcada. **No se promueve al canon.**
- **Correcciones de Javo aplicadas:** AM-008 **eliminada** (derogar un decreto nacional no es
  competencia municipal → no vinculable en POA ni presupuesto; su exclusión evita penalizar al
  GAD en el denominador) · IN-007 **Parcial** ✔ · SC-009 **Parcial** ✔ · SC-017 **Directa** ✔
  (con su meta señalada como ausente del canon).
- **El Gold Master NO fue tocado.** Íntegro: IFE 72.73% · centinela ✅ · ICPI 0.27458226534062735.

## Siguiente paso (requiere a Javo)

Decidir si H04 se amplía a las 66 metas —con lo que implica para el rango del ICPI y la
comparabilidad histórica— o si las 25 se declaran públicamente como el subconjunto estratégico
que el modelo mide. **Hasta esa decisión, vincular promesas es construir sobre arena.**

---
*OBS-010 · Dylus Lab © 2026 · "El último filtro que pidió Javo encontró lo que ni el canon ni la máquina veían: no faltaba una nomenclatura, faltaban 41 metas."*
