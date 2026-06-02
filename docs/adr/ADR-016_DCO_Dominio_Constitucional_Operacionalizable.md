# ADR-016 — Dominio Constitucional Operacionalizable (DCO)

**Estado:** CONGELADO v1.0 — Dom07 caso de referencia activo  
**Fecha:** 2026-06-01  
**Autores:** Dylus Lab (Javo + Claude)  
**Derivado de:** Sprint 4 (Corpus Normativo F0.1-F0.2) · Dom07 caso de referencia  
**Relacionado:** ADR-013 (CIRCUIT_DOMAIN_MAP) · ADR-017 (Circuitos Constitucionales) · ADR-018 (NRC) · QLEP v1.0

---

## Contexto — El problema que resuelve

Durante Sprints 1-4 surgieron tres fallas de diseño que este ADR congela para siempre:

### Falla 1: Dominio ≠ Indicador
"Dom07 Transparencia" fue tratado como un indicador simple. Terminó siendo tres naturalezas distintas (administrativa, democrática, territorial). Sin plantilla DCO, cada dominio se construye ad hoc y se vuelve inconsistente.

### Falla 2: Corpus ≠ Doctrina
La validación F0.1 demostró que el corpus semántico devuelve Art.19 para la consulta de "transparencia activa", cuando la norma rectora es Art.18. El corpus mide similitud. La doctrina establece autoridad. Sin DCO, no existe un artefacto formal que diga cuál norma *gobierna* un dominio.

### Falla 3: Dominio ≠ Circuito
Un dominio es un área de obligación institucional. Un circuito es una cadena causal que atraviesa múltiples dominios. Sin DCO, los dos se confunden y los QTMP no saben a qué dominio pertenecen.

---

## Decisión — El Template DCO

El DCO (Dominio Constitucional Operacionalizable) es la **unidad canónica de dominio en QUIRA**. Cada uno de los 12 dominios tiene exactamente un DCO. Es el artefacto que integra los tres cerebros (ver `docs/architecture/TRES_CEREBROS_QUIRA.md`).

Un DCO NO es:
- Una nota Obsidian (el DCO genera una nota Obsidian, no es la nota)
- Un ACK (el DCO organiza ACKs, no es un ACK)
- Un indicador (el DCO define variables, no las mide)
- Un módulo Python (el DCO inspira módulos, no los implementa)

Un DCO ES:
- El contrato canónico entre el ordenamiento jurídico y la plataforma QUIRA
- La fuente de verdad sobre qué norma gobierna cada dominio
- El artefacto de integración entre Cerebro 1, 2 y 3

---

## Los 8 Componentes del Template DCO

```yaml
# ══════════════════════════════════════════════════════════════════
# COMPONENTE 1 — IDENTIDAD
# ══════════════════════════════════════════════════════════════════

dominio_id: DomXX
nombre_canonico: "[Nombre completo del dominio]"
version: "1.0"
estado: PROPUESTO | ACTIVO | CONGELADO | REVISANDO
fecha_cierre: YYYY-MM-DD
autores: [Dylus Lab]

definicion_operacional: >
  [Una oración precisa. Qué HACE el GAD en este dominio. No qué
  reporta o mide — qué HACE. Usar verbos de acción institucional:
  gestiona, garantiza, planifica, ejecuta, rinde. Máximo 3 líneas.]

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 2 — NORMA FUNDANTE
# (La norma que CREA la obligación — no la que la mide ni la sanciona)
# ══════════════════════════════════════════════════════════════════

norma_fundante:
  ack_id: [SIGLA_ARTICULO]       # ej: CE_18
  norma: [nombre oficial]
  articulo: "[número]"
  texto_clave: >
    [Las palabras exactas que crean la obligación — máx 40 palabras]
  jerarquia: 0                   # 0=CE, 1=LO, 2=Reglamento, 3=Plan, 4=Local
  vigente: YYYY-MM-DD

# Nota: si el dominio tiene subdominios, cada uno tiene su norma fundante.
# Ver Componente 4 (SUBDOMINIOS) para el caso multinatural.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 3 — CADENA NORMATIVA
# (La jerarquía completa que desarrolla la obligación)
# ══════════════════════════════════════════════════════════════════

cadena_normativa:

  C1_constitucional:             # jerarquia=0 — normas CE que aplican
    - ack_id: CE_XX
      articulo: "Art. XX"
      rol: "[fundante | complementario | habilitante]"

  C2_organica:                   # jerarquia=1 — leyes orgánicas
    - ack_id: LOTAIP_XX
      articulo: "Art. XX"
      rol: "[operativo | procedimental | definitorio]"

  C3_reglamentaria:              # jerarquia=2 — reglamentos
    - ack_id: RLOTAIP_XX
      articulo: "Art. XX"
      rol: "[procedimental]"

  C4_observacion:                # jerarquia=3-5 — planes, guías, ordenanzas
    # CRÍTICO: C4 es para instrumentos de OBSERVACIÓN del cumplimiento,
    # NO para normas de obligación. LOTAIP está en C4 para Dom07 (observación),
    # no en C2 (aunque es LO), porque mide cumplimiento, no crea obligación.
    # Ver principio arquitectónico: OBLIGACIÓN ≠ VENTANA DE OBSERVACIÓN
    - ack_id: GUIA_LOTAIP_MEC_XX
      articulo: "Sección XX"
      rol: "[metodologico | verificacion]"

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 4 — SUBDOMINIOS
# (Si el dominio tiene múltiples naturalezas, se modelan aquí)
# ══════════════════════════════════════════════════════════════════

subdominios:
  - id: DomXX-A
    nombre: "[Nombre subdominio A]"
    descripcion: >
      [Qué hace diferente de DomXX-B. Máx 2 líneas.]
    norma_fundante: CE_XX          # puede diferir del dominio padre
    obligacion_tipo: "[activa | pasiva | dialógica | procedimental]"

  - id: DomXX-B
    nombre: "[Nombre subdominio B]"
    descripcion: >
      [...]
    norma_fundante: CE_YY
    obligacion_tipo: "[...]"

# Regla: Si un dominio tiene solo una naturaleza, subdominios = vacío.
# Si tiene más de dos, revisar si en realidad son dos dominios distintos.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 5 — ACTORES
# ══════════════════════════════════════════════════════════════════

actores:
  obligado:
    - "[GAD Municipal | Alcalde | Concejo | Director | Empresa Pública]"
    # El actor que DEBE cumplir — responsable primario

  beneficiario:
    - "[Ciudadanía | Grupo prioritario | Institución superior]"
    # El actor que RECIBE el cumplimiento o el derecho

  articulador:
    - "[CPCCS | CNE | SENPLADES | etc.]"
    # El actor que HABILITA o COORDINA (no sanciona)

  controlador:
    - "[CGE | DPE | PGE | CPCCS | Judicatura]"
    # El actor que SANCIONA el incumplimiento

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 6 — VARIABLES OPERACIONALES
# (Qué se puede observar o medir — por subdominio)
# ══════════════════════════════════════════════════════════════════

variables:
  DomXX-A:                       # Por subdominio
    administrativas:
      - nombre: "[Var_AA]"
        descripcion: "[Qué se observa]"
        evidencia: "[Portal LOTAIP | RDC | POA | PAC | Acta]"
        frecuencia: "[mensual | trimestral | anual]"

    cuantitativas:
      - nombre: "[Var_AB]"
        descripcion: "[...]"
        formula: "[si aplica]"

  DomXX-B:
    democraticas:
      - nombre: "[Var_BA]"
        [...]

# NOTA: Variables ≠ Indicadores plataforma.
# Variables son observables jurídicos. Los indicadores de plataforma
# (H-series) derivan de variables + metodología Excel Canónico.
# NUNCA nombrar H-series en un DCO público.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 7 — CIRCUITOS CONSTITUCIONALES
# (A qué circuitos ADR-017 pertenece este dominio)
# ══════════════════════════════════════════════════════════════════

circuitos:
  - id: C01
    nombre: "[Nombre del circuito]"
    rol_en_circuito: "[origen | nodo | destino]"
    # Cuándo un incumplimiento de ESTE dominio rompe el circuito C01

  - id: C02
    [...]

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 8 — CORPUS Y OBSIDIAN
# (Interface con Cerebro 1 y Cerebro 3)
# ══════════════════════════════════════════════════════════════════

corpus:
  milestone_primario: F0.X        # Milestone que cubre la norma fundante
  milestones_complementarios:
    - F0.Y

  acks_clave:                     # ACKs que anclan este dominio en QLEP
    - ack_id: CE_XX
      relevancia: fundante
    - ack_id: LOTAIP_XX
      relevancia: operativo

  queries_canonicas:
    # Estas queries, ejecutadas en Cerebro 1, deben devolver los
    # chunks más relevantes para cada subdominio.
    # Son decisiones curatoriales — no lo que el embedding cree, sino
    # lo que el jurista dice que es la pregunta correcta.
    DomXX-A:
      - "[Query literal para buscar en normativa_corpus sobre DomXX-A]"
    DomXX-B:
      - "[Query literal para buscar en normativa_corpus sobre DomXX-B]"

obsidian:
  nota_dominio: "Dom07_Transparencia.md"           # Nivel 1
  notas_instrumento:
    - "LOTAIP_Transparencia_GAD.md"                # Nivel 2 (ya existe)
    - "CE_Principios_Estado_GAD.md"                # Nivel 2 (ya existe)
  notas_ack:                                       # Nivel 3 (a crear via QLEP)
    - CE_18.md
    - LOTAIP_7.md
```

---

## Caso de Referencia — Dom07 Transparencia & Apertura Informativa

Este es el primer DCO completo. Define el estándar para los 11 dominios restantes.

```yaml
# ══════════════════════════════════════════════════════════════════
# ADR-016 · DCO · Dom07 — Transparencia & Apertura Informativa
# Versión 1.0 · 2026-06-01 · Dylus Lab
# ══════════════════════════════════════════════════════════════════

dominio_id: Dom07
nombre_canonico: "Transparencia & Apertura Informativa"
version: "1.0"
estado: PROPUESTO
fecha_cierre: 2026-06-01

definicion_operacional: >
  El GAD garantiza el acceso irrestricto a información pública, publicando
  activamente los datos de gestión institucional (Dom07-A) y habilitando
  los mecanismos de participación y deliberación ciudadana que sustentan la
  democracia local (Dom07-B).

# ── COMPONENTE 2: NORMA FUNDANTE ────────────────────────────────

norma_fundante:
  ack_id: CE_18
  norma: "Constitución del Ecuador"
  articulo: "Art. 18"
  texto_clave: >
    "Todas las personas, en forma individual o colectiva, tienen derecho a
    buscar, recibir, intercambiar, producir y difundir información veraz,
    verificada, oportuna, contextualizada, plural, sin censura previa..."
  jerarquia: 0
  vigente: "2008-10-20"

# DECISIÓN CURATORIAL: Por qué Art.18 y no Art.19
# El corpus semántico (F0.1) devolvió Art.19 como primer resultado para
# "transparencia activa". Art.19 trata de medios de comunicación, no del
# derecho ciudadano de acceso. Art.18 crea el derecho fundamental.
# Esta es una decisión humana, no algorítmica. El DCO la congela.

# ── COMPONENTE 3: CADENA NORMATIVA ──────────────────────────────

cadena_normativa:

  C1_constitucional:
    - ack_id: CE_18
      articulo: "Art. 18"
      rol: fundante                        # crea el derecho fundamental
    - ack_id: CE_91
      articulo: "Art. 91"
      rol: complementario                  # acción de acceso a información
    - ack_id: CE_61
      articulo: "Art. 61"
      rol: habilitante                     # derechos de participación (Dom07-B)
    - ack_id: CE_95
      articulo: "Art. 95"
      rol: habilitante                     # participación en asuntos públicos (Dom07-B)
    - ack_id: CE_100
      articulo: "Art. 100"
      rol: habilitante                     # instancias de participación (Dom07-B)

  C2_organica:
    - ack_id: LOTAIP_7
      articulo: "Art. 7"
      rol: operativo                       # obligaciones de transparencia activa
    - ack_id: LOTAIP_34
      articulo: "Art. 34"
      rol: procedimental                   # plazo 10 días hábiles respuesta
    - ack_id: LOTAIP_47
      articulo: "Art. 47"
      rol: sancionador                     # sanciones por incumplimiento
    - ack_id: LOPC_72
      articulo: "Art. 72"
      rol: operativo                       # rendición de cuentas (Dom07-B)
    - ack_id: COD_1
      articulo: "Art. 1-ss"
      rol: definitorio                     # democracia representativa y participativa

  C3_reglamentaria:
    - ack_id: RLOTAIP_1
      articulo: "Art. 1-ss"
      rol: procedimental                   # Reglamento LOTAIP — procedimientos

  C4_observacion:
    - ack_id: GUIA_LOTAIP_MEC_Sec1
      articulo: "Sección 1"
      rol: metodologico                    # Guía MEC — cómo medir cumplimiento
    - ack_id: GUIA_LOTAIP_ENT_Sec1
      articulo: "Sección 1"
      rol: verificacion                    # Guía DPE/CPCCS — verificación
    - ack_id: COOTAD_302
      articulo: "Art. 302"
      rol: complementario                  # competencia GAD para transparencia local
    # NOTA: LOTAIP como instrumento de observación está en C4, no en C2,
    # aunque es LO. Es la ventana de observación, no la norma de obligación.

# ── COMPONENTE 4: SUBDOMINIOS ────────────────────────────────────

subdominios:

  - id: Dom07-A
    nombre: "Transparencia Administrativa"
    descripcion: >
      El GAD PUBLICA activamente su gestión institucional (portales, informes,
      presupuesto, contratos, nóminas, actas) sin esperar solicitudes ciudadanas.
      Obligación de hacer, no de responder.
    norma_fundante: CE_18
    obligacion_tipo: activa
    criterio_distincion: >
      Si la obligación recae en el GAD de publicar por iniciativa propia
      (sin necesidad de solicitud), es Dom07-A.

  - id: Dom07-B
    nombre: "Transparencia Democrática"
    descripcion: >
      El GAD HABILITA los mecanismos por los cuales la ciudadanía puede
      deliberar, consultar y participar en las decisiones públicas.
      Obligación de facilitar el diálogo democrático, no solo de publicar.
    norma_fundante: CE_61
    obligacion_tipo: dialogica
    criterio_distincion: >
      Si la obligación recae en el GAD de CREAR o MANTENER espacios donde
      la ciudadanía ejerce derechos políticos, es Dom07-B.

# Por qué no Dom07-C (Transparencia Territorial)?
# La proyección territorial del acceso a información es una función de
# Dom07-A aplicada al territorio, no una naturaleza distinta.
# Se captura en las variables territoriales de Dom07-A.

# ── COMPONENTE 5: ACTORES ────────────────────────────────────────

actores:
  obligado:
    - GAD Municipal
    - Alcalde (responsable de política de transparencia)
    - Director de Comunicación (operativo)
    - Responsable LOTAIP (operativo - Art. 12 LOTAIP)

  beneficiario:
    - Ciudadanía en general
    - Organizaciones de control social
    - Medios de comunicación
    - Personas naturales o jurídicas que soliciten información

  articulador:
    - CPCCS (promueve participación y control social)
    - SNAP (política de transparencia sector público)
    - DPE (Defensoría del Pueblo — reclamos acceso info)

  controlador:
    - DPE (Defensoría del Pueblo — acción de acceso a info)
    - CPCCS (veedurías ciudadanas)
    - CGE (auditorías de cumplimiento LOTAIP)
    - Judicatura (acción constitucional)

# ── COMPONENTE 6: VARIABLES OPERACIONALES ────────────────────────

variables:

  Dom07-A:
    publicacion_activa:
      - nombre: literales_publicados
        descripcion: "Número de literales LOTAIP Art.7 publicados en portal"
        evidencia: "Portal web GAD / reporte LOTAIP"
        frecuencia: trimestral
        rango_esperado: "0–25 literales"

      - nombre: actualizacion_portal
        descripcion: "Fecha de última actualización del portal de transparencia"
        evidencia: "Metadata portal LOTAIP"
        frecuencia: mensual

      - nombre: solicitudes_respondidas
        descripcion: "% solicitudes de acceso a información respondidas en plazo (10 días hábiles)"
        evidencia: "Registro interno unidad LOTAIP"
        frecuencia: trimestral
        formula: "(solicitudes_en_plazo / solicitudes_totales) * 100"

    completitud_documental:
      - nombre: contratos_publicados
        descripcion: "Contratos del PAC publicados en portal transparencia"
        evidencia: "SERCOP + portal GAD"
        frecuencia: mensual

      - nombre: presupuesto_publicado
        descripcion: "Presupuesto aprobado y reformas publicadas"
        evidencia: "Portal GAD + eSIGEF"
        frecuencia: mensual

  Dom07-B:
    participacion_democratica:
      - nombre: cabildos_realizados
        descripcion: "Número de cabildos populares realizados (Art.100.3 CE)"
        evidencia: "Actas Concejo Municipal"
        frecuencia: anual

      - nombre: mecanismos_activos
        descripcion: "Instancias de participación ciudadana habilitadas y activas"
        evidencia: "RDC + resoluciones internas"
        frecuencia: anual

      - nombre: consultas_previas
        descripcion: "Consultas realizadas a comunas, comunidades o pueblos"
        evidencia: "Actas de consulta"
        frecuencia: anual

# NOTA: Variables son observables jurídicos. No nombrar aquí ningún
# identificador interno del sistema (H-series, ICPI, TGI, etc.)

# ── COMPONENTE 7: CIRCUITOS CONSTITUCIONALES ─────────────────────

circuitos:
  - id: C01
    nombre: "Transparencia_Participacion_Planificacion"
    rol_en_circuito: origen
    descripcion_rol: >
      Dom07 es el origen del Circuito C01. Si la transparencia falla,
      la participación ciudadana no tiene información para ejercerse,
      y la planificación pierde su base de legitimidad democrática.
    condicion_ruptura: >
      Portal LOTAIP sin actualizar por más de 90 días, O
      solicitudes de acceso a información sin respuesta sistemática, O
      ausencia de cabildos por más de 6 meses.

  - id: C02
    nombre: "Presupuesto_Contratacion_Transparencia"
    rol_en_circuito: destino
    descripcion_rol: >
      Dom07 es el destino de C02: la ejecución presupuestaria y
      la contratación deben publicarse (cerrando el ciclo de control).
    condicion_ruptura: >
      PAC o contratos no publicados en portal LOTAIP dentro del plazo legal.

# ── COMPONENTE 8: CORPUS Y OBSIDIAN ──────────────────────────────

corpus:
  milestone_primario: F0.2        # LOTAIP+LOPC+COD+Guías
  milestones_complementarios:
    - F0.1                         # CE (norma fundante)
    - F0.3                         # COOTAD Art.302 (competencia territorial)

  acks_clave:
    - ack_id: CE_18
      relevancia: fundante
    - ack_id: CE_61
      relevancia: fundante Dom07-B
    - ack_id: CE_95
      relevancia: habilitante
    - ack_id: LOTAIP_7
      relevancia: operativo central
    - ack_id: LOTAIP_34
      relevancia: procedimental plazo
    - ack_id: LOTAIP_47
      relevancia: sancionador
    - ack_id: LOPC_72
      relevancia: rendicion cuentas

  queries_canonicas:
    Dom07-A:
      - "¿Qué norma obliga al GAD a publicar información pública de manera activa sin esperar solicitudes?"
      - "¿Qué artículo establece los literales de transparencia activa que debe publicar toda entidad pública?"
      - "¿Cuál es el plazo máximo para responder solicitudes de acceso a información?"
    Dom07-B:
      - "¿Qué artículo constitucional fundamenta el derecho de participación ciudadana en decisiones del Estado?"
      - "¿Qué norma obliga al GAD a crear instancias de participación ciudadana?"
      - "¿Qué ley regula la rendición de cuentas del GAD ante la ciudadanía?"

obsidian:
  nota_dominio: "Dom07_Transparencia.md"
  nivel: 1
  notas_instrumento:
    - "LOTAIP_Transparencia_GAD.md"      # ya existe en vault backup
    - "CE_Principios_Estado_GAD.md"      # ya existe en vault backup
    - "LOPC_Participacion_RDC.md"        # ya existe en vault backup
  notas_ack:
    - CE_18.md
    - CE_61.md
    - CE_95.md
    - LOTAIP_7.md
    - LOTAIP_34.md
    - LOTAIP_47.md
    - LOPC_72.md
```

---

## Reglas de creación de nuevos DCOs

1. **Un DCO por dominio, exactamente.** No se crean DCOs para subdominios.
2. **La norma fundante es decisión curatorial.** No se infiere del corpus — se decide.
3. **C4 es observación, no obligación.** Un instrumento de medición no es fuente de obligación aunque sea ley orgánica.
4. **Subdominios solo si hay naturalezas distintas.** Si la diferencia es solo operativa, es una variable, no un subdominio.
5. **Las queries canónicas se escriben antes de ejecutarlas.** El jurista decide qué preguntar; el corpus responde.
6. **El DCO no nombra indicadores internos.** Las H-series, ICPI, TGI y toda metodología interna son del Excel Canónico, nunca del DCO.
7. **El DCO se congela cuando Dom07 está activo.** Para revisar un DCO activo, crear ADR de revisión y justificar.

---

## Consecuencias

### Inmediatas
- Dom07 tiene su DCO de referencia — puede comenzar Layer 2 completo (módulo Python, nota Obsidian, circuito Neo4j)
- Los 11 dominios restantes esperan su DCO antes de avanzar a Layer 2

### Arquitectónicas
- El corpus (Cerebro 1) ahora tiene queries canónicas por dominio — no depende del usuario para saber qué preguntar
- Obsidian (Cerebro 3) tiene una estructura de nota dominio especificada — los ACKs se generan vía QLEP y la nota dominio se escribe después de los ACKs, nunca antes
- Neo4j (Cerebro 2) tiene su CIRCUIT_DOMAIN_MAP validado por ADR-016 — los circuitos ADR-017 pueden formalizarse con este DCO como base

### Epistemológicas
- QUIRA ahora distingue formalmente: corpus (similitud) vs. doctrina (autoridad)
- La frase "¿Está en el DCO?" se convierte en la pregunta que precede toda decisión sobre qué norma gobierna un dominio

---

## Próximos DCOs (orden recomendado)

| Dominio | Prioridad | Razón |
|---|---|---|
| Dom08 — Participación | 1 | Parte del Triángulo de Gobernanza con Dom07 |
| Dom09 — Rendición de Cuentas | 2 | Cierra el Triángulo P-02 |
| Dom10 — Servicios & Infraestructura | 3 | AGUA_POTABLE circuit activo |
| Dom12 — Protección Social | 4 | GAP_10PCT circuit activo |
| Dom02 — Presupuesto & Financiamiento | 5 | Presupuesto circuit |

---

*ADR-016 · QUIRA Gov · Dylus Lab © 2026*  
*Siguiente: ADR-017 — Circuitos Constitucionales (C01: Transparencia → Participación → Planificación)*
