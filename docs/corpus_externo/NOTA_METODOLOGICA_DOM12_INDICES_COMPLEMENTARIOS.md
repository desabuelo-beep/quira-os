# NOTA METODOLÓGICA — DOM12 — Índices Complementarios de Impacto Territorial

**Estado**: POSTERGADO A BETA  
**Fecha descubrimiento**: 2026-05-31  
**Sesión**: Alpha 0.9 — P2 Patronato  
**Registrado por**: QUIRA Operaciones · Dylus Lab

---

## Hallazgo

El indicador `Ti` (tasa de ejecución presupuestaria, grupos G7+G8) mide **cumplimiento financiero del proceso**.

No mide necesariamente:
- Cobertura efectiva de servicios
- Intensidad de atención por beneficiario
- Continuidad de atención (servicios de alta dependencia: diálisis, psicología, gerontología)
- Impacto territorial real en la población objetivo

En servicios sociales intensivos en capital humano — diálisis, atención psicológica, trabajo social, atención gerontológica, nutrición, educación inicial — **pueden coexistir simultáneamente**:

```
Ti financiero ROJO  +  Impacto territorial VERDE
(Patronato ejecutó 50% del presupuesto PERO la clínica de diálisis atendió al 100% de sus pacientes)

— o —

Ti financiero VERDE  +  Impacto territorial ROJO
(El Patronato ejecutó el presupuesto PERO los programas alcanzaron solo el 20% de la población objetivo)
```

QUIRA necesita poder convivir con estas tres verdades simultáneamente:
- **Financieramente 🔴** (Ti < 70%)
- **Operativamente 🟢** (servicio continuo)
- **Territorialmente 🟢 o 🔴** (cobertura real)

El indicador `Ti` es válido para el Piso 1 (compliance presupuestario). Los índices complementarios son necesarios para el Piso 2 (impacto territorial).

---

## Lo que está en Alpha (válido, no cambia)

```
Ti_Patronato_2025 = 50.00%  →  🔴 ROJO  — CONFIRMADO
Ratio_COOTAD_249 = 20.84%   →  🟢 VERDE — pendiente_validacion

Estos datos son correctos. Solo afecta su INTERPRETACIÓN avanzada.
```

---

## Fuente para recuperación en Beta

**Carpeta**: `C:\Users\DELL\Desktop\Javo\Dylus Lab\Refactorización\varios\metodologicos antiguos\`

**Documentos relevantes**:
- `Metodologia SIAP-ICPI Final.md` — descripción metodológica de índices
- `SIAP-ICPI_VERSION_CON_METODOLOGIA.xlsx` — instrumento original con pesos
- `Instrumento SIAP-ICPI TESIS.xlsx` — versión tesis
- `TESIS DE LICENCIATURA EN CIENCIAS POLÍTICAS menos punitiva.docx` — marco teórico
- `INSUMOS METODOLOGIA.md` — insumos del proceso metodológico

Los índices complementarios de impacto territorial que medían `outputs`, `outcomes` e `impactos` — no solo ejecución presupuestaria — están en estos documentos.

---

## Tarea Beta (no ahora)

```
Sprint: Dom12-Beta — Recuperación Índices Complementarios
Pre-requisito: Neo4j Alpha operativo + primera consulta causal ejecutada
Acción: leer Metodologia SIAP-ICPI Final.md + TESIS + recuperar índices
         → incorporar como C8 de Piso 2 en los QTMP Dom12
         → distinguir Ti (Piso 1) de Índice Complementario (Piso 2) en UI
```

---

## Por qué no ahora

> Alpha tiene una misión clara. Los índices complementarios fortalecen Beta. Neo4j fortalece Alpha.
> 
> *— Colega, 2026-05-31*

**No afecta la validez de los datos Alpha. Solo afecta su interpretación avanzada.**

---

*NOTA METODOLÓGICA DOM12 — registrada 2026-05-31 · Dylus Lab — DOCUMENTO INTERNO*
