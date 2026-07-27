---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-036 · El universo operacional del modelo — 25 metas estratégicas (v1) y su evolución a 66 (v2)

**Estado:** RATIFICADO · 2026-07-15 (Javo + director técnico · propuesta del colega)
**Contexto de origen:** OBS-010. El "último filtro" de Javo (Plan Plurianual PDOT 2023-2027 ·
SHA256 `09a2aacc…`) revela que el PDOT tiene **66 metas** y el Gold Master opera con **25**.
La pregunta era si el canon estaba roto. **No lo está.**
**Relacionado:** ADR-023 (Regla 1 · fórmula canónica INMUTABLE) · ADR-024 (221 GAD · Capa B) ·
ADR-034 (el Orquestador) · OBS-010 (el hallazgo) · d01 Planificación · d03 Mandato.

---

## Contexto

Existen **dos niveles de realidad** que hasta hoy estaban implícitamente mezclados:

| Realidad **documental** | Realidad **operacional** |
|---|---|
| Plan CNE · PDOT completo (66 metas) · POA · Presupuesto · SIGAD | las estructuras que el motor **usa**: 25 metas · fórmulas · rangos |

No son lo mismo, y confundirlas fue lo que hizo parecer que el canon estaba mal. **El Gold
Master no está equivocado: opera sobre un universo estratégico que nunca se explicitó.** Lo
que cambió hoy no es el canon: es que ahora **sabemos exactamente qué representa**.

## Decisión

### 1. El universo operacional de v1 son las 25 metas estratégicas — y se DECLARA
> El Gold Master utiliza el **subconjunto estratégico de 25 metas del PDOT** como **universo
> operacional** para el cálculo del ICPI. No mide el PDOT completo (66 metas).

Deja de ser un supuesto tácito y pasa a ser una **decisión arquitectónica explícita**. Toda
publicación de d01/d03 debe declararlo: *"se mide contra las 25 metas estratégicas del modelo"*.
Verificado (OBS-010): **las 25 existen todas en el PDOT** — ninguna inventada. Es un
subconjunto legítimo, no un error de carga.

### 2. H12 y el ICPI se CONGELAN (no se amplían)
```
H12!B31 = SUM(J6:J30)   ← 25 filas · NO SE TOCA
H12!B33 = B31/B32       ← ICPI · FÓRMULA CANÓNICA · INMUTABLE (Regla 1)
```
Ampliar el rango de 25 a 66 **no sería una corrección**: cambiaría denominador, series
históricas, comparabilidad, hipótesis y resultados. Eso es una **nueva versión metodológica**,
y exige ADR propio, recalibración y nueva validación empírica. **No entra por la puerta de una
"cura".** H12 es hoy un motor empírico validado; se respeta como tal.

### 3. Montecristi es la VALIDACIÓN EMPÍRICA del molde (visión de Javo)
Montecristi = Municipio 001 = el **molde**. Se cierra con el universo estratégico de 25 metas,
que es lo que valida el modelo. **Al terminar Montecristi arranca QUIRA Operaciones** (Capa B ·
ADR-024/034) para incorporar progresivamente los **221 GAD** — y ese escalamiento se hace
**corrigiendo el universo total de metas por GAD** (Javo · 2026-07-15).

```
v1 · MONTECRISTI (validación empírica)      v2 · 221 GAD (escalamiento)
PDOT (66)                                    PDOT completo por GAD
   → 25 metas estratégicas                      → universo total de metas
   → ICPI validado          ─── evolución ───→  → ICPI recalibrado
   → CONGELADO                                  → nuevo producto, no reparación
```

### 4. La ampliación 25 → 66 es EVOLUCIÓN, no corrección — y tendrá su propio ADR
Cuando se aborde (al escalar a los 221), requerirá: **versión nueva del motor · recalibración ·
nueva validación empírica · ADR específico**. La serie histórica de v1 **se preserva intacta**:
2025 y 2026 seguirán siendo comparables entre sí porque miden el mismo universo. Un ICPI de v1
y uno de v2 **jamás se comparan directamente** — miden universos distintos.

### 5. Lo que SÍ se corrige ahora (sin tocar una sola fórmula)
- ✅ **Rótulos que inducen a error** — hecho hoy: `Promesas_Con_Meta_PDOT = 48` era en realidad
  la **suma de scores**; se renombró a `Suma_Score_Vinculación` y el conteo real (64) pasó a su
  propia celda. También: `Clasificación_IFE` dejó de ser texto estampado y ahora se calcula.
- ✅ **El estado de verificación** nació como dato en el canon (col `Estado_Verificación`), en
  vez de inferirse en Python (Regla 9).
- 🔜 **Completar H03** con las 77 promesas reales del Plan CNE y su trazabilidad, una vez Javo
  valide la propuesta de vinculación (76 tras excluir AM-008 · ADR-035 §5).
- 🔜 **Documentar qué significa el IFE** y contra qué universo se calcula (§1).

## Consecuencia práctica

**d03 se DESBLOQUEA** — pero declarando su alcance. El índice de fidelidad mide contra las **25
estratégicas**, no contra el PDOT completo, y eso se dice en la pantalla. Una promesa cuya meta
existe en el PDOT pero **fuera del universo operacional** (caso real: *Infocentro* → *"puntos
digitales 19.265→23.265"*, hoja `3.SOC`) no se marca como incumplimiento del GAD: se declara
como **fuera del alcance del modelo v1**. Es un hallazgo, no una falta.

**Lo más valioso de la sesión no fue encontrar las 77 promesas ni las 66 metas: fue descubrir
que el Gold Master operaba sobre un universo que nunca se había explicitado.** Documentarlo
convierte una posible debilidad en una **decisión arquitectónica transparente y defendible** —
exactamente lo que un banco de desarrollo, una contraloría o un GAD tienen derecho a exigir.

---
*ADR-036 · Universo Operacional del Modelo · Dylus Lab © 2026 · "El motor no estaba equivocado: estaba callado sobre su propio alcance. v1 valida el molde con 25 metas; v2 escala a 221 GAD con el universo completo. Ampliar no es curar: es evolucionar — y eso se hace con ADR, recalibración y evidencia nueva."*
