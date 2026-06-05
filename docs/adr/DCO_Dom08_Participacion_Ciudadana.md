# DCO · Dom08 — Participación Ciudadana & Control Democrático

**Estado:** PROPUESTO v1.0  
**Fecha:** 2026-06-02  
**Autores:** Dylus Lab (Javo + Claude)  
**Derivado de:** ADR-016 (template DCO) · ADR-017 (C01 — Dom08 es INTERMEDIARIO) · ADR-018 (CE_95 es NRC)  
**Relacionado:** DCO Dom07 (origen C01) · DCO Dom09 (pendiente — cierra Triángulo P-02)

---

## Por qué Dom08 es el segundo DCO

Dom08 es el nodo **INTERMEDIARIO** de C01 (Transparencia → **Participación** → Planificación).  
Sin Dom08 operacional, C01 es un circuito con origen fuerte (Dom07) y destino aislado (Dom04).  
Con Dom08, la cadena constitucional completa `CE_226 → CE_95 → Dom08 → C01` queda computable.

Adicionalmente, Dom08 es el primer test empírico de ADR-018:  
CE_95 es NRC porque su remoción rompe Dom08 (participación) **y** Dom09 (rendición de cuentas) **y** Dom04 (planificación participativa) — tres dominios independientes.  
Cuando Dom08 esté activo en Neo4j, `CE_95.betweenness_centrality` comenzará a ser medible.

---

## Los 8 Componentes DCO

```yaml
# ══════════════════════════════════════════════════════════════════
# DCO · Dom08 — Participación Ciudadana & Control Democrático
# Versión 1.0 · 2026-06-02 · Dylus Lab
# ══════════════════════════════════════════════════════════════════

dominio_id: Dom08
nombre_canonico: "Participación Ciudadana & Control Democrático"
version: "1.0"
estado: PROPUESTO
fecha_cierre: 2026-06-02
autores: [Dylus Lab]

definicion_operacional: >
  El GAD garantiza el ejercicio protagónico de la ciudadanía en las
  decisiones públicas, habilitando formalmente el sistema de participación
  (Dom08-A) y ejecutando el presupuesto participativo como mecanismo
  vinculante de gestión fiscal democrática (Dom08-B).

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 2 — NORMA FUNDANTE
# ══════════════════════════════════════════════════════════════════

norma_fundante:
  ack_id: CE_95
  norma: "Constitución del Ecuador"
  articulo: "Art. 95"
  texto_clave: >
    "Las ciudadanas y ciudadanos participarán de manera protagónica en la
    toma de decisiones, planificación y gestión de los asuntos públicos,
    y en el control popular de las instituciones del Estado."
  jerarquia: 0
  vigente: "2008-10-20"

# DECISIÓN CURATORIAL: Por qué CE_95 y no CE_61
# CE_61 establece derechos políticos (voto, iniciativa popular, fiscalización).
# CE_95 crea el mandato de PARTICIPACIÓN PROTAGÓNICA en la gestión pública —
# incluyendo planificación, toma de decisiones y control. Es más amplio y
# directamente vinculado a la obligación del GAD de garantizar esa participación.
# CE_61 aplica al ciudadano como sujeto electoral; CE_95 aplica al GAD como
# obligado a habilitar la participación en su gestión cotidiana.
# Esta es una decisión humana, no algorítmica. El DCO la congela.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 3 — CADENA NORMATIVA
# ══════════════════════════════════════════════════════════════════

cadena_normativa:

  C1_constitucional:
    - ack_id: CE_95
      articulo: "Art. 95"
      rol: fundante                  # crea el mandato de participación protagónica
    - ack_id: CE_100
      articulo: "Art. 100"
      rol: habilitante               # obliga a conformar instancias de participación
    - ack_id: CE_61
      articulo: "Art. 61"
      rol: complementario            # derechos políticos ciudadanos (dim. electoral)
    - ack_id: CE_18
      articulo: "Art. 18"
      rol: habilitante               # participación informada requiere CE_18 (Dom07)

  C2_organica:
    - ack_id: COOTAD_302
      articulo: "Art. 302"
      rol: operativo                 # participación ciudadana en GADs — obligación formal
    - ack_id: COOTAD_303
      articulo: "Art. 303"
      rol: procedimental             # derecho a la participación — mecanismos
    - ack_id: COOTAD_304
      articulo: "Art. 304"
      rol: procedimental             # sistema de participación ciudadana — arquitectura
    - ack_id: LOPC_72
      articulo: "Art. 72"
      rol: operativo                 # mecanismos participación en GADs (cabildos, RDC, PP)

  C3_reglamentaria: []               # No hay reglamento específico LOPC para GAD Municipal

  C4_observacion:
    - ack_id: CPCCS_METODOLOGIA
      articulo: "Metodología veedurías"
      rol: verificacion              # CPCCS verifica ejercicio democrático en GADs

# NOTA ARQUITECTÓNICA:
# La LOPC (Ley Orgánica de Participación Ciudadana) opera en C2 para Dom08,
# NO en C4. A diferencia de LOTAIP en Dom07 (que es ventana de observación),
# la LOPC CREA mecanismos de participación — es norma de obligación, no de medición.
# Esto invierte el patrón Dom07 y es una diferencia doctrinal crítica.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 4 — SUBDOMINIOS
# ══════════════════════════════════════════════════════════════════

subdominios:

  - id: Dom08-A
    nombre: "Participación Protagónica en Decisiones"
    descripcion: >
      El GAD HABILITA los espacios formales donde la ciudadanía participa
      en la planificación, toma de decisiones y control de la gestión pública.
      Obligación de crear y mantener el sistema de participación (CE_100 + COOTAD_304).
      Incluye: asamblea cantonal, silla vacía, cabildos populares, consultas.
    norma_fundante: CE_95
    obligacion_tipo: dialogica
    criterio_distincion: >
      Si la obligación recae en el GAD de CREAR o MANTENER espacios donde
      la ciudadanía incide en decisiones públicas (planificación, presupuesto,
      control), es Dom08-A.

  - id: Dom08-B
    nombre: "Presupuesto Participativo"
    descripcion: >
      El GAD EJECUTA el presupuesto participativo como mecanismo vinculante
      que incorpora prioridades ciudadanas en la inversión pública.
      Obligación fiscal-democrática: no solo consultar, sino incorporar
      formalmente las demandas ciudadanas en el POA y presupuesto.
    norma_fundante: COOTAD_303
    obligacion_tipo: procedimental
    criterio_distincion: >
      Si la obligación involucra la dimensión FISCAL de la participación
      (ciudadanía define prioridades de inversión), es Dom08-B.
      Dom08-B es la intersección Dom08 ∩ Dom02 (presupuesto).

# Por qué solo dos subdominios y no tres:
# Se consideró Dom08-C (Control Social / Rendición de Cuentas) pero ese
# dominio ya está parcialmente capturado en Dom09 (Rendición de Cuentas).
# Duplicar aquí rompe la separación de dominios. Dom08-B captura la
# dimensión activa de la participación en el ciclo presupuestario.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 5 — ACTORES
# ══════════════════════════════════════════════════════════════════

actores:
  obligado:
    - GAD Municipal
    - Alcalde (garante del sistema de participación)
    - Concejo Municipal (aprueba presupuesto participativo)
    - Responsable de Participación Ciudadana (operativo)

  beneficiario:
    - Ciudadanía en general
    - Organizaciones sociales y barriales
    - Comunas y comunidades del cantón
    - Grupos de atención prioritaria (con énfasis especial CE_95 párr. 2)

  articulador:
    - CPCCS (Consejo de Participación Ciudadana y Control Social)
    - SNP (Secretaría Nacional de Planificación — orientación metodológica)
    - CNP (Consejo Nacional de Planificación — articulación PDOT)

  controlador:
    - CPCCS (veedurías ciudadanas — principal controlador Dom08)
    - DPE (Defensoría — reclamos por vulneración participación)
    - CGE (auditorías de cumplimiento LOPC en GADs)
    - Judicatura (acción constitucional si se niega participación)

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 6 — VARIABLES OPERACIONALES
# ══════════════════════════════════════════════════════════════════

variables:

  Dom08-A:
    instancias_formales:
      - nombre: sistema_participacion_activo
        descripcion: "Sistema de participación ciudadana conformado y activo (COOTAD_304)"
        evidencia: "Resolución o acto normativo de creación + actas de sesiones"
        frecuencia: anual
        rango_esperado: "Activo / Inactivo"

      - nombre: cabildos_realizados
        descripcion: "Número de cabildos populares realizados en el período (CE_100.3)"
        evidencia: "Actas Concejo Municipal"
        frecuencia: anual
        rango_esperado: "Mínimo 2 por año"

      - nombre: asambleas_cantonales
        descripcion: "Asambleas cantonales o instancias ciudadanas convocadas"
        evidencia: "Actas de asamblea + convocatorias"
        frecuencia: anual

      - nombre: silla_vacia_ejercida
        descripcion: "Veces que se ejerció la silla vacía en sesiones de Concejo"
        evidencia: "Actas sesiones Concejo con silla vacía activada"
        frecuencia: anual

    control_social:
      - nombre: veedurias_habilitadas
        descripcion: "Veedurías ciudadanas habilitadas formalmente por CPCCS"
        evidencia: "Registro CPCCS + resoluciones habilitación"
        frecuencia: anual

  Dom08-B:
    presupuesto_participativo:
      - nombre: pp_realizado
        descripcion: "Presupuesto participativo ejecutado en el período"
        evidencia: "Resolución Concejo aprobando presupuesto participativo + POA"
        frecuencia: anual
        rango_esperado: "Sí / No"

      - nombre: porcentaje_pp
        descripcion: "Porcentaje del presupuesto de inversión definido participativamente"
        evidencia: "Presupuesto aprobado + metodología PP documentada"
        frecuencia: anual
        formula: "(inversion_pp / inversion_total) * 100"

      - nombre: participantes_pp
        descripcion: "Número de ciudadanos participantes en el proceso de PP"
        evidencia: "Listas de asistencia o registros del proceso PP"
        frecuencia: anual

# NOTA: Variables son observables jurídicos — no nombrar aquí indicadores
# internos del sistema. H-series, ICPI, TGI permanecen en el Excel Canónico.

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 7 — CIRCUITOS CONSTITUCIONALES
# ══════════════════════════════════════════════════════════════════

circuitos:
  - id: C01
    nombre: "Transparencia_Participacion_Planificacion"
    rol_en_circuito: INTERMEDIARIO
    peso_chs: 1.0
    descripcion_rol: >
      Dom08 es el nodo INTERMEDIARIO de C01. Recibe información de Dom07
      (transparencia activa) y la convierte en participación ciudadana
      con base informada. A su vez, la participación es el insumo
      constitucional de Dom04 (planificación territorial — PDOT).
    condicion_ruptura: >
      Ausencia de cabildos por más de 6 meses, O
      sistema de participación inactivo (sin sesiones documentadas), O
      presupuesto participativo no ejecutado por 2+ años consecutivos.
    mecanismo_entrada: "CE_18 → CE_95 (Dom07 informa a Dom08)"
    mecanismo_salida: "CE_95 → CE_264.1 (Dom08 habilita Dom04)"

  - id: C04
    nombre: "Participacion_RendicionCuentas_Control" # pendiente ADR-017
    rol_en_circuito: ORIGEN
    descripcion_rol: >
      Dom08 será ORIGEN del Circuito C04 (pendiente de formalización).
      La participación ciudadana activa la rendición de cuentas (Dom09)
      y el control social (CPCCS).
    estado: PENDIENTE_ADR017

# ══════════════════════════════════════════════════════════════════
# COMPONENTE 8 — CORPUS Y OBSIDIAN
# ══════════════════════════════════════════════════════════════════

corpus:
  milestone_primario: F0.1          # CE (norma fundante CE_95)
  milestones_complementarios:
    - F0.3                           # COOTAD (Arts. 302-304)
    - F0.2                           # LOPC (pendiente ingesta completa)

  acks_clave:
    - ack_id: CE_95
      relevancia: fundante (NRC)
    - ack_id: CE_100
      relevancia: habilitante instancias
    - ack_id: COOTAD_302
      relevancia: operativo participación GAD
    - ack_id: COOTAD_303
      relevancia: procedimental derecho participación
    - ack_id: COOTAD_304
      relevancia: procedimental sistema formal
    - ack_id: LOPC_72
      relevancia: mecanismos participación (corpus gap pendiente)

  queries_canonicas:
    Dom08-A:
      - "¿Qué artículo constitucional obliga al Estado a garantizar la participación protagónica ciudadana en la gestión pública?"
      - "¿Qué norma obliga al GAD Municipal a conformar un sistema de participación ciudadana?"
      - "¿Qué instancias de participación deben existir en todos los niveles de gobierno según la Constitución?"
      - "¿Qué es la silla vacía y cuándo se activa en el Concejo Municipal?"
    Dom08-B:
      - "¿Qué norma del COOTAD regula el presupuesto participativo en los GADs?"
      - "¿Qué mecanismos de participación ciudadana deben implementar los gobiernos autónomos descentralizados?"

obsidian:
  nota_dominio: "Dom08_Participacion.md"
  nivel: 1
  notas_instrumento:
    - "LOPC_Participacion_GAD.md"
    - "COOTAD_Participacion_Territorial.md"
    - "CE_Principios_Participacion.md"
  notas_ack:
    - CE_95.md
    - CE_100.md
    - COOTAD_302.md
    - COOTAD_303.md
    - COOTAD_304.md
    - LOPC_72.md
```

---

## Relación Dom08 con la Prueba NRC de ADR-018

El propósito arquitectónico de este DCO, más allá de formalizar Dom08, es activar el test empírico de ADR-018.

Una vez que Dom08 esté activo en Neo4j, la consulta:

```cypher
MATCH p=(:ACK {ack_id:'CE_226'})-[:HABILITA*0..3]->(:ACK {ack_id:'CE_95'})
-[:FUNDA]->(:Dominio {id:'Dom08'})-[:ALIMENTA]->(:Circuito {id:'C01'})
RETURN p
```

debe retornar resultado, demostrando que la segunda rama del NRC CE_95 está activa:

```
CE_226 → CE_95 → Dom08 → C01   ← segunda cadena constitucional computable
CE_226 → CE_18 → Dom07 → C01   ← primera (ya verificada)
```

Cuando ambas coexisten, C01 pasa de circuito mono-dominio fuerte a circuito **multi-dominio constitucional**.

---

## Diferencia arquitectónica crítica con Dom07

| Dimensión | Dom07 | Dom08 |
|---|---|---|
| Norma fundante | CE_18 (derecho información) | CE_95 (derecho participación) |
| Naturaleza obligación | GAD publica activamente | GAD habilita espacios de decisión |
| LOPC en cadena | C4 (observación) | C2 (obligación directa) |
| Relación con COOTAD | C4 Art.302 (complementario) | C2 Arts.302-304 (operativo) |
| Rol en C01 | ORIGEN (peso 1.5) | INTERMEDIARIO (peso 1.0) |
| Test NRC | CE_18 → Dom07 ✅ | CE_95 → Dom08 (este DCO) |

---

## Próximos pasos post-Dom08

1. **Dom09 DCO** — Rendición de Cuentas (cierra Triángulo P-02: Dom07↔Dom08↔Dom09)
2. **C04 Formalizar** — Participación → Rendición → Control Social (ADR-017 extensión)
3. **Centralidad NRC** — Con Dom08+Dom09 activos, correr betweenness_centrality en Neo4j

---

*DCO Dom08 · QUIRA Gov · Dylus Lab © 2026*  
*Siguiente: DCO Dom09 — Rendición de Cuentas & Control Ciudadano*
