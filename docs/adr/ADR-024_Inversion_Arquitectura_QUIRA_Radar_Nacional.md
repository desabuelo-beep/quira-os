---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-024 — Inversión de Arquitectura: QUIRA como Radar Nacional

**Estado**: RATIFICADO — 2026-06-04 · Consenso equipo Dylus Lab (Javo + Claude + Colega)
**Fecha**: 2026-06-04
**Proyecto**: QUIRA Gov · Dylus Lab
**Origen**: Javo (fundador) + síntesis Colega + criterio Claude (director técnico)
**Supersede parcialmente**: la jerarquía implícita "Institucional = raíz"

---

## PREGUNTA CENTRAL A RATIFICAR (sesión de arquitectura)

> **¿QUIRA es un software municipal, o un radar nacional independiente
> de inteligencia pública?**

Si la respuesta es la segunda (y los tres convergemos en que lo es), entonces
quiraintelligence.com es el producto principal y quiraholding.streamlit.app es
el laboratorio operativo. Este ADR documenta la propuesta; la sesión la ratifica.

Diferencia que está en juego:
- **Software municipal** → el municipio es el CLIENTE
- **Radar nacional** → el municipio es el SUJETO OBSERVADO

Cambia narrativa, mercado, posicionamiento, gobernanza del dato y crecimiento.

---

## Contexto

Hasta hoy operábamos con una jerarquía implícita:

```
QUIRA Institucional (raíz)
  → Ciudadana · Impact · Economic · Cooperación · Operaciones (derivados)
```

Javo planteó una inversión: quiraintelligence.com no es la vitrina de Montecristi
ni el demo de Institucional. Es el **radar vivo e independiente de los 221 GAD
del Ecuador**. Y lo que llevamos meses construyendo no es un dashboard municipal —
es la infraestructura de un sistema operativo de inteligencia pública.

## Decisión

Se adopta una arquitectura de **4 capas**:

### Capa A — NÚCLEO (motor de cálculo + conocimiento)
Invisible. Interno. Ya construido en gran parte.
- Gold Master SIAP-ICPI v5.5 (cálculo canónico — ADR-023 Nivel 1)
- QLEP → Neo4j (corpus normativo: 136 ACK atoms)
- Graphify → grafo de construcción del proyecto (memoria histórica)
- GeoTwin engine (territorial)
- Conectores: DPE, SERCOP, CPCCS, Gold Master
- NLP (discurso público: RDC + redes + entrevistas)
- Índices: ICPI · TGI · IOC · PSG · IED · ITAM · SAT · TOP

### Capa B — QUIRA OPERACIONES (capacidad interna, NO producto)
**Corrección del Colega (2026-06-04): Operaciones es una CAPACIDAD, no un producto.**
Es la función interna de Dylus Lab que alimenta el núcleo.
- HOY: Javo + Claude + Colega SON QUIRA Operaciones
- MAÑANA: analistas de Dylus Lab
- DESPUÉS: módulo derivado para técnicos municipales (sólo con contrato GAD)
- Hace: ingesta · scraping DPE/SERCOP · monitoreo mensual · validación SHA-256 · curación
- NO se vende como UI. Es el motor humano detrás del radar.

### Capa C — PRODUCTOS (interfaces sobre el mismo motor)
- **QUIRA Institucional** → alcaldes y directivos (la médula del sistema)
- **QUIRA Ciudadana** → ciudadanía, academia, OSC
- **QUIRA Impact** → BID, CAF, PNUD, Banco Mundial
- **QUIRA Economic** → inversión y desarrollo económico local
- **QUIRA Cooperación** → elegibilidad y financiamiento internacional

### Capa D — PORTAL NACIONAL (el PRODUCTO PRINCIPAL)
**Corrección del Colega: quiraintelligence.com NO es landing ni demo. Es el producto.**
- **quiraintelligence.com** = Radar Nacional de Gobernanza Explicable
- El visitante NO entra a ver Montecristi. Entra a ver ECUADOR:
  221 GAD monitoreados · 24 provincias · semáforo nacional · ranking de coherencia
  mapa Ecuador · alertas críticas · ejecución · transparencia · contratación · cooperación
- Luego puede entrar a un GAD: Montecristi · Manta · Cuenca · Quito...
- Referencia: Bloomberg Government · FiscalNote · OpenGov — pero ecuatoriano
- **quiraholding.streamlit.app** = el LABORATORIO operativo donde validamos el motor
  antes de escalarlo al Ecuador completo. NO es el producto final.

## El cambio de modelo de negocio (lo más importante)

```
ANTES: vender software (SaaS) a municipios → depende de buena voluntad política
AHORA: monitoreo INDEPENDIENTE de los 221 GAD desde fuentes públicas
       → el municipio es OBJETO de análisis, no cliente
       → se monetiza a cooperantes, academia, inversores, prensa
       → el GAD viene después (licencia Institucional = su espejo privado)
```

Coherente con el Bloomberg Firewall: el dato se produce independientemente,
el GAD no lo controla. Primera línea de mercado de Dylus Lab.

## Montecristi redefinido

Montecristi deja de ser el destino. Pasa a ser **Municipio 001** — el laboratorio
donde se valida que el motor despierta. Si funciona en 001, escala a los 221.

## Lo que NO cambia

- **El roadmap de ejecución es idéntico**: Sprint A→B→C→D→E→F → Montecristi v1.0
- ADR-023 sigue vigente (3 niveles de cálculo: Motor/SO/UI)
- Bloomberg Firewall intacto
- Esto es marco mental + destino final, NO scope creep

## Consecuencias

**Positivas:**
- Modelo de negocio independiente de la voluntad política del GAD
- quiraintelligence.com tiene un norte claro: radar nacional, no demo
- Los 5 productos comparten un solo motor → eficiencia de construcción
- La valoración futura de Dylus Lab cambia: no es una app, es infraestructura nacional

**Riesgos:**
- Scope creep si se intenta construir el radar antes de validar Montecristi
- Mitigación: Montecristi v1.0 es prerequisito duro antes de cualquier capa D

## Relación con otros ADRs
- ADR-023 (3 niveles de cálculo) → se mantiene, opera DENTRO de la Capa A
- ADR-011 (tres productos motor IA) → ampliado a 5 productos sobre un núcleo
- GATE-007 (Manta) → sigue congelado; ahora se entiende como "Municipio 002"

---
*ADR-024 · QUIRA Gov · Dylus Lab © 2026*
*Decisión arquitectónica de primer orden — registrada en grafo (regla canónica)*
