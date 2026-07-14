# ADR-034 · Orquestación de Operaciones — encender la Capa B (el ciclo mensual de dominio)

**Estado:** RATIFICADO · 2026-07-13 (Javo + director técnico · a partir de una propuesta del colega)
**Contexto de origen:** Javo pregunta cómo QUIRA **opera mensualmente** para 221 GAD (y luego LAC). El
colega lo formaliza como "catálogo de *Skills* / QCL". Se adopta la **intuición** (correcta y potente) y se
**rechaza la envoltura** (renombra lo que ya existe · Regla 7).
**Relacionado:** ADR-024 (4 capas · **Capa B Operaciones = capacidad, NO producto**) · ADR-031 (5 motores
tipados · el MCD) · ADR-023 (Regla 1/4 · no recalcular el motor) · ADR-033 (dos verdades) · Regla 7 anti-inflación.

---

## Contexto

La pregunta de Javo: *¿cómo se opera QUIRA, mes a mes, a escala (221 GAD → LAC)?* La respuesta **no** es "más
pantallas" ni un humano "abriendo el dominio": es **pipelines programados**, por GAD y por período. El colega
propuso una capa nueva ("Skills/QCL"); el canon la atrapa: eso **renombra** los motores (ADR-031) y describe
la **Capa A** que ya existe. Lo válido de la propuesta es el **cuándo y el cómo se ejecuta**, no una ontología nueva.

## Decisión

### 1. El salto NO es una capa nueva — es ENCENDER la Capa B (Operaciones)
ADR-024 ya declara la **Capa B · QUIRA Operaciones = una CAPACIDAD interna** (*"Operaciones es una capacidad,
no un producto"* — corrección del colega, 2026-06-04). Hoy la ejercen humanos (*"Javo + Claude + Colega SON
QUIRA Operaciones"*). El salto de escala es **automatizarla**.

### 2. El Orquestador — la capacidad genuinamente nueva (pasa Regla 7)
Encadena, por GAD y por período, la maquinaria que **ya existe**:
```
conectores (ingesta: PDOT · POA · PAC · SERCOP · Presupuesto · Rendición)
   → motores tipados (ADR-031: Matemático · Grafos · Causal · Descubrimiento · Prospectivo)
   → snapshot (Regla 1)
   → DOM / cajón (proveniencia 🟢🔵🟣 · ADR-033)
   → alertas
```
Lo nuevo **no** es ninguna pieza (todas existen): es la **orquestación programada + calendarizada** de todas.
Eso es exactamente lo que faltaba para operar a escala.

### 3. LÍMITE DURO (Regla 1 + Regla 4 + Prohibición)
El Orquestador **orquesta la LECTURA del Gold Master; JAMÁS recalcula.** Un paso "calcula ICPI" sería el
**motor de cálculo paralelo prohibido**. El ciclo **lee** los índices ya calculados (MCM) y los **traza**; no
los produce. La verdad analítica nace en el Excel; el Orquestador solo la mueve, la explica y la actualiza.

### 4. Rechazo explícito (Regla 7 · anti-inflación del canon)
- **"Skill" NO entra** como primitiva: renombra los **motores** (prueba en el propio diagrama del colega:
  *Biografía* aparece como **Motor** y como **Skill** a la vez), o los **conectores**, o el **snapshot**. Si
  solo cambia el nombre, no entra.
- **"QCL / Capability Library" NO entra** como capa: es la **Capa A** que ya existe, nombrada en inglés.
  Convención canónica: **español** (Motor de Biografía, no `BIOGRAPHY_ENGINE` · Firewall).
- **"QUIRA Operaciones / Alcalde / Contraloría" NO son productos:** Operaciones es **capacidad** (ADR-024);
  la taxonomía de productos es **Institucional · Ciudadana · Impact · Economic · Cooperación**. No se mintan productos.

### 5. Lo que SÍ se conserva del aporte
- La **metadata de ejecución** (Entradas · Salidas · Dependencias · Periodicidad · Motor · DOM · Proveniencia):
  útil, pero como **manifiesto del Orquestador** (un DAG la necesita), en español, no como "librería" nueva.
- La **visión "Sistema Operativo de Administración Pública"**: se conserva como **norte** — de hecho ya está
  en el nombre, **QUIRA OS**. Capa B = el *planificador de procesos*; los motores = las *llamadas al sistema*;
  los DOM = las *áreas funcionales*. Todo eso ya existe: se **enciende y se programa**, no se re-bautiza.

## Consecuencia práctica
El trabajo de **curar cada DOM** (sus dos verdades · ADR-033) **no cambia**. Lo que se añade: una vez curado,
cada dominio expone un **ciclo mensual** ejecutable. **Primero se curan los DOM; después el Orquestador los
corre solos**, por GAD, cada mes. Ese es el camino real a 221 GAD → LAC — sin un humano por pantalla.

---
*ADR-034 · Orquestación de Operaciones · Dylus Lab © 2026 · "No se opera el sistema: se ejecutan ciclos programados. El Orquestador enciende la Capa B; los motores ya saben trabajar — ahora trabajan solos, cada mes, para cientos de gobiernos."*
