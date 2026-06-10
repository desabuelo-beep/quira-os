# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy loading: carga el detalle SOLO del área que vas a tocar. No leas todo "por si acaso".
> Mantener bajo 500 tokens. Actualizar `## AHORA` al cierre de cada sesión.

## QUÉ ES
> **"El Gold Master ya sabe medir la gestión pública; QUIRA está aprendiendo a
> demostrar documentalmente por qué cada métrica del Gold Master es verdadera o falsa."**
>
> Gate 6.6 no agrega datos. Agrega significado.
> Objetivo: **sistema de auditoría explicable del modelo ICPI.**

**3 niveles** (ADR-023 — inmutable):
- **Nivel 1 Motor**: Gold Master SIAP-ICPI v5.5 — calcula ICPI/TGI/SAT/MMP. Leer via `app/connectors/gold_master.py`. NUNCA recalcular fuera del Excel.
- **Nivel 2 SO**: QUIRA — ingesta + trazabilidad (MNT_UUID) + evidencia documental
- **Nivel 3 UI**: Dashboards + GeoTwin — solo visualizan, no calculan

**MATRIZ_CANONICA** del Excel = ADN compartido. Sin ella: dos mundos. Con ella: un sistema.

## AHORA (actualizar al cierre)
- **Sprint A ✅ COMPLETO** (2026-06-04) · **ADR-026 v1.3 ✅ MODELO OPERATIVO** (2026-06-09)
- **FASE 0 — Arqueología funcional ✅ COMPLETA** (2026-06-09):
    9 excavaciones: D02 · D03 · D04 · D06 · D07 · D08 · D09 · D10 · D12
    Taxonomía 5 capas: Tipo D (corpus) · A (7 generadores) · B (sintetizador) · C (protocolo) · A² (consecuencia)
    → ADR-026 v1.3: `docs/adr/ADR-026_Topologia_Funcional_QUIRA.md`
    → MAPA_FUNCIONAL_QUIRA_v1: `docs/architecture/MAPA_FUNCIONAL_QUIRA_v1.md`
    → QUIRA_DATA_REGISTRY_v1: `docs/architecture/QUIRA_DATA_REGISTRY_v1.md`
- **FASE 1 Operaciones — EN CURSO D02** — último commit `1879d84` (2026-06-09):
    ✅ Bloomberg Firewall `2571e23`: p7_brecha · p10_inversion · p15_transparencia (deprecated) · m3_municipal · p_cadena
    ✅ D03 routing `205af2a`: mod=metas → p8_metas.py (IFE-A 72.73% ahora accesible)
    ✅ QUIRA_DATA_REGISTRY_v1 `2f8a98f`: ~32 LIVE · 10 MISSING · 2 HARDCODED · 1 PENDIENTE
    ✅ D02 Migración 002 `1879d84`: 5 tablas Supabase + 21 requisitos + 21 emisores ancla
       fondos_emisores · fondos_convocatorias · fondos_requisitos · fondos_conv_requisitos · fondos_elegibilidad
- **D02 MOTOR DE ELEGIBILIDAD — 5/5 PASOS COMPLETOS** (último commit `55c701a` p18 + D.2 pendiente):
    ✅ A.0 Schema 5 tablas Supabase (aplicado y verificado)
    ✅ A.1 Semilla: 21 requisitos (4 familias) + 21 emisores ancla + 5 convocatorias test
    ✅ B. `app/engines/fondos_matcher.py` — MCR-001: elegible=2·brecha=1·no_elegible=2·USD 1.3M
    ✅ C. `app/engines/fondos_simulator.py` — PSG→30%: ONU Mujeres USD 300K / ISP→65%: BDE USD 5M
    ✅ D.1 `quira_pages/p18_cooperacion.py` — rewrite COMPLETO como lector puro Supabase (commit `55c701a`)
    ✅ D.2 skill `/fondos-radar` — pipeline completo Adapter→Normalizer→Staging→Validator→Insert→Matcher
       - Migración 003: fondos_fuentes (salud) + fondos_historial (auditoría inmutable)
       - `app/fetchers/`: base_adapter · fondos_normalizer (Haiku) · fondos_radar_runner
       - 3 adaptadores MVP: PNUD · BID · AECID (demo+live, fallback heurístico)
       - `.claude/skills/fondos-radar/SKILL.md` — ciclo 15 días operativo
       - Test end-to-end: 6 fondos insertados · Matcher recalculado · fondos_fuentes OK
    ⚠️  NOTA: Gold Master almacena ISP/PSG como fracción decimal (0.028 = 2.8% ≠ 14.58%)
       Renderer usa demo_data.INDICES para display (escala % correcta). Matcher usa Gold Master (correcto).
    ⚠️  NOTA conv_requisitos: nuevas convocatorias del Fetcher necesitan requisitos manuales en Supabase
       antes de que el Matcher las evalúe. Ver skill /fondos-radar §"Nota importante sobre conv_requisitos".
- **SEGURIDAD** (commit pendiente · 2026-06-09): Migración 004 — RLS habilitado en 23/23 tablas Supabase.
    Correo Supabase 08-Jun detectó `rls_disabled_in_public`. Resuelto: 0 tablas expuestas.
    App no afectado (conexión directa postgres bypasea RLS por diseño).
- **PD-GEN-01 — PRINCIPIO DE DISEÑO GÉNERO** (directorio: ADR-026 §Género · 2026-06-09):
    Descubrimiento: el eje Género de QUIRA se estructura primariamente sobre brechas TERRITORIALES.
    Los indicadores institucionales (PSG, IGM-A, IGM-B) son indicadores de CAPACIDAD (20%).
    Los indicadores territoriales (violencia, cuidados, empleo, movilidad, seguridad) son RESULTADOS (80%).
    Fuente territorial: PDOT vigente (PDOT Bicentenario 2023 ya en corpus) agrega INEC/DINASED/Banco Central.
    D12 Territorial ≠ nueva campaña de levantamiento = extracción estructurada del PDOT (ya ingresado).
    PDOT → GeoTwin: la Capa B de género territorial se territorializa espacialmente en el GeoTwin del cantón.
    Narrativa que cambia: "PSG=12.83%" → "capacidad institucional insuficiente → brechas territoriales persisten
    → $300K ONU Mujeres bloqueados → programas territoriales no ejecutados"
    Sprint B: extraer variables Capa B del corpus PDOT (violencia · jefatura femenina · cuidados · empleo).
- **PD-GEO-01 — PRINCIPIO DE DISEÑO TERRITORIAL** (ADR-026 §Geografía · 2026-06-09):
    PDOT vigente = Gemelo Digital Territorial canónico de QUIRA. No es un documento — es un modelo territorial.
    El PDOT agrega INEC · DINASED · MSP · BCE · MIES · SENPLADES · catastros · equipamientos.
    Por tanto: PDOT ≡ GeoTwin (definición formal, no metáfora).
    Toda brecha territorial debe representarse simultáneamente como:
      1. Indicador (tabla/Gold Master)   2. Narrativa (texto gobernanza)   3. Entidad geoespacial (capa GeoTwin)
    Pregunta que cambia: "¿Cuántos casos?" → "¿DÓNDE ocurren?" — la pregunta que necesita un alcalde.
    Cadena completa QUIRA: PDOT/GeoTwin (DÓNDE) → QUIRA (CAPACIDAD) → D02 (FINANCIAMIENTO) → GeoTwin (DÓNDE INTERVENIR)
    Ejemplo operativo: "$300K ONU Mujeres para intervenir parroquias X/Y/Z donde GeoTwin muestra
    mayor concentración de vulnerabilidad de género" — esto es gobernanza territorial inteligente.
    Relación PD-GEN-01→PD-GEO-01: Violencia · Cuidados · Movilidad · Empleo femenino = capas nativas GeoTwin.
    Completa ADR-026: Norma→Observación→Interpretación→Validación→Consecuencia→**DÓNDE ocurre la consecuencia**.
- **PD-CIU-01 — PROPUESTA Javo (pendiente revisión Colega · 2026-06-09): pipeline de adquisición ciudadana**:
    QUIRA Ciudadana = cascada: N0 sistema busca solo (LOTAIP·SERCOP·CPCCS·web GAD) →
    N1 ciudadano sube (PDOT·plan trabajo·orgánico·presup. participativo) → N2 sistema genera
    solicitud acceso info pública → N3 día 15 sin respuesta: email acción judicial + paso a paso.
    Invierte D12: el ciudadano exige con derecho propio (presión que un oficio Dylus no tiene).
    Ciudadano = sensor del radar nacional · coyuntura electoral = máxima motivación.
    Testers UEB/CAF usan la misma cascada con SU cantón (o ven demo Montecristi en portal).
    ⚠️ Plantillas legales SOLO con texto vigente verificado SHA256 (LOTAIP reformada 2023 + LOGJCC).
    ✅ Capa de autenticidad RESUELTA (Javo): N2 siempre pide remisión al correo → fuerza respuesta
    electrónica del GAD con firma digital → oficio firmado = respaldo probatorio de QUIRA.
    Firma electrónica > SHA256: hash + identidad firmante + sello de tiempo + GAD comprometido.
    Niveles confianza corpus: 🥇ORO oficio GAD firmado (verif. criptográfica PAdES) ·
    🥈PLATA fuente oficial pública (URL+SHA256+fecha) · 🥉BRONCE upload ciudadano (referencia, NO evidencia).
    Secuencia: es material Sprint C/D — Sprint B (validación motor) no se detiene.
    **MODELO 3 VÍAS de adquisición** (Javo · 2026-06-09): V1 Dylus/Operaciones = barrido activo
    LOTAIP·SERCOP·CPCCS·web GADs → **ÍNDICE DE OPACIDAD NACIONAL** (221 GADs · post-validación;
    opacidad se mide por AUSENCIA → no requiere cooperación GAD ni Gold Master por cantón) ·
    V2 Ciudadana = cascada N0-N3 (corre por parte del ciudadano, independiente) ·
    V3 Testers UEB/CAF = ingesta documental de SU cantón como experiencia.
    Las 3 convergen al corpus con niveles 🥇ORO/🥈PLATA/🥉BRONCE. OSINT = capa futura posterior.
    ❓Mesa pendiente: ¿Índice Opacidad = conteo documental QUIRA o métrica Excel? (zona gris ADR-023)
    **TRIÁNGULO EN CONSTRUCCIÓN** (Javo · 2026-06-09): Operaciones (expone: radar/opacidad) →
    Ciudadana (presiona: cascada) → **Institucional/Gestión (válvula de salida: espejo privado
    del GAD, donde responde y mejora — el ingreso de Dylus)**. Institucional = VÍA 4 adquisición:
    GAD cliente entrega datos operativos directos (calidad ORO+). Flywheel: más datos → mejor radar
    → más presión → más GADs a Institucional → más datos. Alcaldes entrantes 2027 = clientes naturales.
- **C-RDC FORMALIZACIÓN — COMPLETA** (commit `96a98c9` · 2026-06-09):
    ✅ `scripts/cypher/001_crdc_circuit.cypher` — topología convergente + 6 nodos + EvaluacionCircuito MCR-001
    ✅ `scripts/cypher/apply_cypher.py` — runner AuraDB (requiere reanudar instancia 6c134c35)
    ✅ `app/connectors/neo4j_crdc.py` — get_crdc_state() + simulate_crdc_mejora() + fallback MCR-001
    ✅ `quira_pages/p17_rdc.py` — bloque C-RDC live wired (6 nodos · semáforos · impacto D02 $5.3M)
    ✅ AuraDB reanudado + Cypher 29/29 aplicado · Fuente Neo4j: True · live en p17_rdc.py
    Verificado CLI: BLOQUEADO · 2/6 nodos · $5.3M · PSG→20% sube nodo pero circuito sigue bloqueado
    (ITAM 56%<80% + ISP 14.58%<25% = 2 críticos que impiden desbloqueo total)
- **SPRINT B — ABIERTO** (2026-06-09 · consenso Javo+Colega+Director):
    Objetivo: **Montecristi = primer territorio completamente explicable por QUIRA.**
    NO construir — validar. Matriz 5 casos × 5 preguntas (qué·por qué·dónde·cuánto·recursos).
    Estructura: B.1 Diagnóstico (NO reparar) → B.2 Cierre gaps críticos → B.3 Re-validación.
    Casos (6): Transparencia ✅PASA · Agua+Alcantarillado ✅PASA · Violencia género ✅4/5+frontera ·
    Movilidad 🔴 · Desempleo juv. 🔴 · Residuos sólidos 🟡 (caso 06 — cadena distinta a agua)
    FICHA-03 resultado: pronóstico Colega EXACTO — 4 responden, "¿dónde?" en frontera.
    **G-09 CRÍTICO confirmado**: 0 indicadores género desagregados por parroquia en PDOT (verificado
    por script). Asimetría hallada: sistema conoce OFERTA territorial (liderazgo 2/7 parroquias,
    Isabel Muentes y Aníbal SA sin cobertura) pero no DEMANDA (dónde duele la brecha). Femicidios
    1.14/100K (meta 0.8) · jefatura fem. 36.1% · VIF y embarazo adolescente SIN TASA ni cantonal
    (G-11/G-12). G-10: brechas PSG inconsistentes (-7.17 C-RDC vs -19.97 matcher, escala decimal).
    Hipótesis Colega (correlación capacidad↔brechas territoriales) registrada — verificable post-G-09.
    **B.1A AUDITORÍA PDOT ✅** (2026-06-09 · `docs/sprint-b/B1A_AUDITORIA_PDOT.md` + script reproducible):
    Corpus narrativo 1,587 chunks PDOT auditado por tema. VEREDICTOS: Ambiente 211/65×parroquia y
    Movilidad 211/49 = gaps de EXTRACCIÓN (riqueza sin explotar, NO faltan datos) · Género 18/0 =
    GAP REAL doble fuente (KB+narrativo) · Residuos 158 (caso 06 asegurado) · Juventud 67/13 parcial.
    HALLAZGO NUEVO: Junta Cantonal Protección Derechos — casos Mujer 120→198 (+65% en 1 año) ·
    morbilidad 66.25% femenina → enriquecen FICHA-03 "qué pasa" (extraer en B.2).
    Pronósticos revisados: Movilidad 🔴→🟡 · Residuos 🟡→🟢.
    **FICHA-04 Movilidad ✅** (3/5 + 2 frontera): tabla vial parroquial p.136 extraída — Colorado
    8.92% tratada/35.56% sin tratamiento/110km red mayor · pluvial 0% en 4 parroquias · ANT 95.8%
    siniestros rurales. HALLAZGOS COLATERALES: G-05 RESUELTO (discrepancia agua = núcleo CUP vs
    parroquia completa, tabla corregida p.115 con flags [EST]) · G-06 RECLASIFICADO (saneamiento
    parroquial SÍ existe p.115: Isabel Muentes 0% · EA 12.4%). Gaps nuevos: G-13 unidades km/m ·
    G-14 La Pila+IM sin datos viales · G-15 radar sin tema movilidad (vacío fetcher, CAF presta) ·
    G-16 transporte público sin datos operativos · G-17 indicador ANT ambiguo.
    **B.1 DIAGNÓSTICO COMPLETO ✅ (2026-06-09) — 6/6 FICHAS:**
    FICHA-05 Desempleo juvenil (2/5, frontera mapeada): tasa cantonal 4.35%→meta 3.73 SÍ existe ·
    tasa JUVENIL no existe (G-18) · empleo 65% en empresas grandes · embudo universitario 44% vs 97%.
    FICHA-06 Residuos (3/5+2): recolección 96% FUERTE con tabla parroquial+recintos (Isabel Muentes
    70% otra vez al fondo) · disposición final = CELDA EMERGENTE desde 2019 (no relleno técnico) ·
    recuperación reciclables ≈1.3% · Montecristi-EP cadena completa desde 2017.
    BALANCE B.1: 25 gaps (G-01…G-25) · 2 resueltos en camino (G-05/G-06) · 0 reparaciones prematuras.
    PATRONES TRANSVERSALES: (1) Isabel Muentes al fondo de TODO (agua 1.02% · saneamiento 0% ·
    inversión $40pc · recolección 70%) — la parroquia-síntoma del cantón. (2) Radar D02 con 3 vacíos
    temáticos (movilidad·empleo·residuos) = 1 sola intervención al fetcher. (3) Gaps externos
    convergen en 1 paquete INEC (G-09 género + G-18/21 empleo + G-19 PEA).
    **B.2 REDEFINIDA = OPERACIÓN MINERA DEL PDOT** (Colega post-B.1 · 2026-06-09):
    "Extraer primero todo lo que ya existe adentro" — hallazgo central B.1: Corpus ≠ KB estructurado.
    Lotes: 1.Género · 2.Ambiente · 3.Movilidad · 4.Juventud · 5.Empleo (campo verde — Javo: el
    componente Económico Productivo NUNCA fue excavado). Luego B.3: re-correr FICHAS 03-06 sin
    tocar el motor y MEDIR: ¿cuánto de los 25 gaps era no-extraído vs vacío real? Esa razón decide
    el próximo sprint (expansión corpus vs cirugía GM). Gold Master NO se toca hasta esa medición
    (Fase 3 = auditorías dirigidas GM-GEN-01·GM-AMB-01·GM-COOP-01·GM-BONOS-01 con evidencia B.1/B.2).
    **LOTE-01 GÉNERO v1 ✅** (`docs/sprint-b/mineria/LOTE-01_genero.md` · commit d315852):
    11 indicadores extraídos formato KB. HALLAZGO MAYOR: violencia letal cambió de régimen —
    homicidios 6/año (2014-21) → 25 (2022) → 47 (2023), +683% vs línea base (Tabla 121 p.242).
    Femicidios serie 10 años: total 5, bajo y estable (Tabla 122 p.243). Junta Cantonal Mujer
    120→198. G-11 confirmado por el PROPIO PDOT ("no se registran cifras para este nivel territorial").
    Pendiente lote 1 v2: cuidados T.100-101 · CDBV · fecundidad. Lotes 2-5: ambiente · movilidad ·
    juventud · empleo (campo verde).
    **EXTRACCIÓN TOTAL PDOT APROBADA POR MESA Y EN CURSO** (2026-06-10 · commit `0d40ab2`):
    Migración 005 aplicada (pdot_indicadores + pdot_extract_log · RLS día 1).
    `scripts/sprint_b/pdot_extractor.py` — Haiku + ventana vecinos + dedup + reanudable.
    PUGS confirmado DENTRO del PDOT (Javo: 2ª parte de 800+ pp · 370 chunks con contenido suelo).
    Corrida total 1,587 chunks lanzada en background. Validación dirigida post-corrida en:
    Género (A) · Ambiente (B) · Economía Productiva (C) — prioridades del Colega.
    El extractor = PROTOTIPO del módulo de ingesta Sprint C (misma arquitectura para 221 cantones:
    PDOT → Extractor → Base estructurada → GeoTwin → Operaciones).
    **ESTADO CORRIDA + PLAN SIN CRÉDITOS API** (2026-06-10):
    Corrida Haiku murió al 22.1% (350/1,587 chunks · 372 indicadores) por créditos API agotados.
    PAI completo · PDOT-MCR parcial · PLAN-BICENTENARIO 0 (ahí está el PUGS).
    VÍA $0 ACTIVADA: `kb_loader.py` (commit aaddfc6) parsea el KB estructurado (producto /graphify
    del Excel KB) determinísticamente → 1,610 indicadores confianza ALTA (carga en curso).
    Doble vía conviven: KB determinístico ($0) + narrativo Haiku (reanudable al recargar créditos:
    `python scripts/sprint_b/pdot_extractor.py` simplemente continúa donde quedó).
    **DIRECTIVAS COLEGA post-corrida**: validar SOLO 3 cortes — Género (vs Lote 1 manual) ·
    Ambiente (el más rico esperado) · Económico Productivo (apuesta estratégica → QUIRA Economic).
    MÉTRICA DECISIVA: ¿cuántos de los 25 gaps desaparecen? (quedan 20=problema modelo ·
    quedan 5=era extracción · quedan ~12=responsabilidad compartida GM+corpus).
    Gold Master: NI UNA LÍNEA hasta el informe de cosecha.
    **COSECHA v1 COMPLETA** (2026-06-10): **1,959 indicadores** en pdot_indicadores
    (KB determinístico 1,587 confianza alta + Haiku 372). **1,617 TERRITORIALIZADOS (82.5%)**
    en ~103 territorios (parroquias+recintos+urbano/rural). Por sistema: SOCIOCULTURAL 658 ·
    ASENTAMIENTOS 643 · BIOFISICO 362 · ECONOMICO_PRODUCTIVO 139 (campo verde poblado) ·
    POLITICO_INST 104 · MOVILIDAD 46 · PUGS 4 (espera créditos — narrativo Plan Bicentenario).
    Corte género VALIDADO vs Lote 1: converge (Junta Cantonal 120→198 idéntico en ambas vías)
    Y SUPERA: jefatura femenina serie 2001-2022 (18.7→25.4→36.1 = casi se duplicó en 20 años) ·
    analfabetismo digital mujeres 34.8→7.8. Limpieza pendiente: normalizar territorios
    (Montecristi/Cantón Montecristi/Montecristi (Cantón)) + dedup semántico de indicadores.
    SIGUIENTE: validar cortes 2-3 (Ambiente · Económico Productivo) → B.3 re-validación fichas
    → MEDICIÓN: ¿cuántos de los 25 gaps caen? → informe de cosecha a la mesa.
    **OBSERVACIÓN JAVO VALIDADA CON COSECHA** (2026-06-10): brecha urbano/rural ENORME confirmada —
    pobreza rural 42.2% vs urbana 18.4% · pobreza EXTREMA rural 23.7% vs urbana 3.3% (7×) ·
    multidimensional rural 67.9% vs urbana 23% (3×) · NBI rural 53.3 vs urbano 21.3 (+32pp).
    Las "comunidades históricamente olvidadas" SÍ están (agregadas): fila "Demás áreas sin
    parroquia" = agua 19.3% · saneamiento 15.53% · pluvial 0% — peor que cualquier parroquia
    nombrada. Isabel Muentes (1.02% agua) es parroquia URBANA → la precariedad es DENTRO del CUP.
    → **G-26 NUEVO**: inventario sub-parroquial de comunidades/recintos con/sin sistema de agua
    no existe como capa nombrada (promedio parroquial invisibiliza). Fuente: GAD/PDOT anexos.
    **CORTE 2 AMBIENTE ✅** (directiva Colega · 2026-06-10): BIOFISICO 362 = riqueza confirmada.
    Temas: ecosistemas 54 · residuos 45 · clima 25 · riesgo/amenaza 18 · suelo 13.
    SORPRESA (como predijo Colega): capa de riesgo COMPLETA y cuantificada —
    **82.28% del territorio con susceptibilidad a movimientos de masa** · 13.51% riesgo
    inundación · sismo tsunamigénico min 7.0 (ref. 7.8 Pedernales 2016) · índice riesgo
    cantonal 41.98→meta 59.22 (2025). Conecta Operaciones+Cooperación+Impact: fondos
    adaptación climática (BID/CAF/GEF) — y el radar D02 NO tiene términos clima/resiliencia
    (4ª instancia patrón G-15). Hipótesis Colega actualizada: 25 gaps → probablemente 10-15 reales.
    **CORTE 3 ECONÓMICO PRODUCTIVO ✅ + CORRECCIÓN JAVO** (2026-06-10):
    el campo verde escondía MEGA-PROYECTOS — pero son **PROYECTOS FALLIDOS/ESTANCADOS de
    gobiernos nacionales anteriores, NUNCA CONSTRUIDOS** (corrección del fundador):
    (1) Central Fotovoltaica El Aromo: 200 MW · ~USD 145M — contrato firmado mar-2023,
    obra JAMÁS INICIADA (estancado). (2) Refinería del Pacífico/ZEDE 200 MBPD — abandonado.
    El PDOT los documenta como capacidad; la realidad territorial es que no existen físicamente.
    → **G-27 NUEVO (arquitectura · descubierto por corrección Javo)**: el sistema NO distingue
    **estado de materialización** (anunciado/contratado/en construcción/operativo/estancado/
    abandonado). Sin esa dimensión, QUIRA repetiría el error del PDOT: presentar promesas como
    activos. La brecha PLANIFICADO vs MATERIALIZADO ES auditoría de gestión pública pura —
    El Aromo es el caso de estudio perfecto. Candidata a dimensión obligatoria del schema.
    Hallazgos VÁLIDOS del corte: relevo generacional agro roto (79.3% productores 45+ ·
    solo 6.2% <35 — conecta FICHA-05) · minería no metálica activa · riego Río Bravo 38 familias ·
    tenencia 83.8% propia · 43% montubio.
    **3/3 CORTES COMPLETOS** → siguiente: B.3 re-validación FICHAS 03-06 + MEDICIÓN de gaps.
    **B.3 MEDICIÓN ✅** (2026-06-10 · `docs/sprint-b/B3_MEDICION_GAPS.md`):
    **27 gaps → 14 A (reales) · 4 B (extracción) · 9 C (arquitectura)**. 48% se resuelve sin
    fuentes externas ni tocar el GM. **Los 14 reales son TODOS fuentes externas (INEC·DINASED·
    MSP·ANT·GAD) — CERO fórmulas faltantes del motor.** Hipótesis Colega direccionalmente correcta.
    7 decisiones de QUIRA cambiaron (FICHA-03 qué pasa Media→Alta · saneamiento IM 0% · prioridad
    territorial + "Demás áreas" · relevo agro · capa riesgo operativa · Economic con G-27 · radar 4 temas).
    VEREDICTO PRELIMINAR GM: NO es el problema principal. Auditoría futura = 3 dimensiones
    quirúrgicas con evidencia: (1) estado de materialización G-27 · (2) riesgo/vulnerabilidad
    territorial · (3) brecha urbano/rural transversal. NO bloques enteros género/ambiente/bonos.
    SIGUIENTE: B.3 fase 2 (fichas v2) · B.2-cierre C (lote arquitectura sin API: G-01/02/08/10 +
    radar 4 temas) · mesa GM cuando Javo+Colega dispongan.
    **G-27 RECLASIFICADO (aclaración Javo · 2026-06-10)**: el GM YA disciplina materialización de
    obras MUNICIPALES (variable con verificación SERCOP — confirmado en QUIRA_DATA_GOVERNANCE_v1.0 +
    tabla sercop_contratos 772 filas). El Aromo/Refinería = obras NACIONALES (fuera del ámbito GAD
    por diseño). G-27 queda como mejora de capa territorial: campos competencia + materialización
    en pdot_indicadores. Auditoría GM futura baja a 2 dimensiones (riesgo territorial · urbano/rural).
    **B.2-CIERRE ARQUITECTURA EJECUTADO** (voto Colega · 2026-06-10):
    ✅ G-10 escala: fondos_matcher normaliza PSG/ISP del GM (fracción→%) — brecha -19.97 era falsa.
       ⚠️ G-10b pendiente MESA: psg_ejecucion (GM 2.8%) vs PSG display (12.83%) = variables distintas
       — decidir contra cuál se evalúan requisitos de fondos ANTES de re-correr matcher.
    ✅ G-15/20/23+clima: radar amplió vocabulario — 8 temas nuevos (movilidad·empleo·juventud·
       residuos·economia_circular·clima·resiliencia·riesgo_desastres) en normalizer+prompt.
    ✅ G-02: dedup semántico en runner (nombre normalizado+emisor) + duplicada PNUD id=6 eliminada.
    📋 G-01/G-08: plantilla `scripts/seed/003_conv_requisitos_TEMPLATE.sql` — 5 convocatorias con
       URL listas para verificar bases reales y cargar requisitos (NO se inventan — Regla 3).
    **VOTO DE MESA EJECUTADO** (Colega+Javo · 2026-06-10):
    ✅ G-10b RESUELTO: PSG ejecutado = principal de elegibilidad (capacidad real) · PSG codificado =
       contextual (alineación). AMBOS conservados en matcher. Matcher RE-CORRIDO con GM live
       (64 métricas Excel): brechas corregidas ONU PSG -19.97→-17.17 · BDE ISP -64.97→-61.78.
       Veredictos estables: 2 elegibles ($900K) · 1 brecha (AECID ITAM -9) · 2 no elegibles.
    🛑 G-01 RECLASIFICADO (hallazgo verificado): las 5 convocatorias "sin veredicto" son DATOS
       DEMO de los adaptadores (URLs hardcodeadas en adapter_pnud/bid). NO existen bases que leer.
       Marcadas en DB (es_real=false). El G-01 real = ciclo LIVE del fetcher (requiere créditos
       API) → convocatorias reales → bases reales → requisitos. El radar ampliado (8 temas) ya
       está listo para ese ciclo. ❓Mesa: ¿las 5 del seed original (BDE/ONU/PNUD/AECID/FORD con
       elegibilidad calculada) son convocatorias verificadas o plantillas realistas de test?
    SIGUIENTE (orden Colega): Fichas v2 (productización) → GeoTwin (consolidación) → auditoría GM.
    **TAXONOMÍA ORIGEN_OPORTUNIDAD IMPLEMENTADA** (mesa · 2026-06-10):
    Migración 006 aplicada: SIMULADA(gris)/VALIDADA(azul)/VIGENTE(verde)/CERRADA(rojo).
    10/10 convocatorias actuales = SIMULADA (seed test + fetcher demo — hipótesis Colega confirmada:
    plantillas realistas para validar matching, NO radar vivo). Runner propaga origen: live→VALIDADA ·
    demo→SIMULADA. Regla: SOLO VIGENTE se presenta como oportunidad operativa; SIMULADA = "caso de
    validación del motor". Ciclo radar 15 días → **SEMANAL** (decisión Javo · proxima_revision +7).
    ⏳ OBSIDIAN: los 15-20 fondos revisados NO están en repo/corpus (viven en vault local de Javo).
    Pedido a Javo: ruta o export de esa nota → primera carga VALIDADA real del radar.
    ⏳ UI p18: badge de origen (gris/azul/verde/rojo) pendiente — material Fichas v2/UI.
    **REVISIÓN GOLD MASTER pendiente (pedido Javo)**: género/ambiente/bonos/cooperación flojos en Excel.
    B.1A produce el insumo: Ambiente=extraer del PDOT→proponer indicadores · Género=fuentes externas ·
    Cooperación/bonos=D02 ya es la fuente, afinar reglas. Decisión de mesa Javo+Director post-B.1.
    FICHA-02 resultado: PASA 5/5 · respuesta territorial por parroquia (Isabel Muentes 1.02% agua ·
    NBI 61.2% · $40 pc vs cabecera 95%/$217) · serie 20 años +2.2pp · meta PDOT 2027 inalcanzable
    sin BDE $5M (bloqueado por fiscal) · 4 gaps: G-05 semántica agua parroquial/cantonal ·
    G-06 alcantarillado parroquial no existe · G-07 costo social sin cuantificar · G-08 BID sin requisitos
    **DECISIÓN ESTRATÉGICA UEB/CAF (Javo · 2026-06-09): NO demo — QUIRA operando sobre X cantones,**
    **testers operativizan ingesta completa como experiencia.** Fichas = QA del motor pre-réplica.
    Horizonte propuesto: B validar → C industrializar ingesta (operable no-ingenieros) → D replicar
    X cantones (testers como operadores). Diplomado CAF = fuerza de ingesta distribuida.
    ⚠️ Cuello de botella identificado: Gold Master es POR CANTÓN (Excel MCR) — réplica requiere
    decisión arquitectónica (X Excels vs capa documental sin motor para cantones nuevos).
    → `docs/sprint-b/README.md` (definición+plantilla) · `FICHA-01_transparencia.md` ✅
    FICHA-01 resultado: PASA 5/5 preguntas · 4 gaps (G-01 conv_requisitos · G-02 dedup PNUD ·
    G-03 convención institucional ✅resuelto · G-04 trazabilidad ITAM→corpus)
    Hallazgo clave: AECID $400K bloqueado por brecha exacta ITAM −9 · $900K elegible HOY gobernanza.
    Las 5 fichas = material demo UEB/CAF (cuerpo Bloomberg-safe, pie técnico omitible).
- **PENDIENTES (no bloqueantes — Sprint B corre en paralelo)**:
    ✅ D02 completo — 5/5 pasos (Motor de Elegibilidad Financiera operacional)
    ✅ C-RDC Neo4j — COMPLETO Y LIVE. AuraDB activo. Fuente Neo4j: True.
    ✅ Supabase RLS — 23/23 tablas protegidas. Vulnerabilidad Supabase resuelta.
    🔴 IFE-E (D03): trazabilidad POA→PAC→eSIGEF → Dirección Financiera GAD
    🧊 D12 → BACKLOG ESTRATÉGICO (no bloqueante · no ejecutar ahora)
       Oficios redactados y listos. NO enviar hasta que QUIRA demuestre valor.
       Realidad: municipios tardan 3+ meses en responder. UEB/CAF no puede esperar.
       Estrategia invertida: Modelo→Demo→Validación→Luego oficios.
    🟡 C02 + C03: specs parciales ADR-017 → completar
    ⬜ Verificar UI Sprint A: `streamlit run app.py` (Tarea A3)
    ⬜ Graphify update: `/graphify . --update` (artefactos nuevos: ADR-026 v1.3 · MAPA · REGISTRY · C-RDC)
- **Histórico** `fb78876` (2026-06-08): `historico-construccion-quira.md` + `ultima-conversacion-director-claude.md`
- **Gate 6.6 ✅ · Corpus**: ~13,509 chunks · Neo4j: 38/58
- **Connector LISTO**: `app/connectors/gold_master.py` → H73_OUTPUT_API + fallback TGI
- **GATE-007 🧊 CONGELADO** — Manta = Municipio 002 · retomar post-Montecristi v1.0
- **Roadmap revisado**: A✅→[Operaciones ✅]→**B ABIERTO**→C→D→E→F
    Siguiente: **Sprint B ABIERTO** — modelo demuestra valor con datos que ya tiene. D12 no bloquea.
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED · ADR-023 ACTIVO · ADR-024 RATIFICADO · ADR-026 v1.3 RATIFICADO**

## REGLA CANÓNICA NUEVA (2026-06-03)
**Todo artefacto construido entra al grafo.** Docs, decisiones, specs, planes, versiones históricas.
La memoria histórica es la base de QUIRA dialéctica / autorregenerativa.
Comando: `/graphify . --update` al cierre de cada sesión con nuevos artefactos.

## ARQUITECTURA DE 4 CAPAS (ADR-024 — RATIFICADO 2026-06-04)
**Pregunta central a ratificar: ¿QUIRA es software municipal o radar nacional?**
Los 3 convergemos en: RADAR NACIONAL independiente. (GAD = sujeto observado, no cliente)
- **Capa A NÚCLEO**: Gold Master · QLEP · Graphify · GeoTwin · conectores · NLP · índices (ya construido)
- **Capa B OPERACIONES**: CAPACIDAD interna Dylus Lab (NO producto). Hoy = Javo+Claude+Colega
- **Capa C PRODUCTOS**: Institucional · Ciudadana · Impact · Economic · Cooperación (5 UIs, 1 motor)
- **Capa D PORTAL** = **PRODUCTO PRINCIPAL**: quiraintelligence.com = radar vivo 221 GAD
    quiraholding.streamlit.app = LABORATORIO donde validamos el motor (no es el producto final)
- **Montecristi = Municipio 001** (laboratorio). NO cambia sprints; SÍ cambia interpretación.
- ADR-024 RATIFICADO. Capa D disponible post-Montecristi v1.0.

## REGLAS DE ORO (inviolables — el resto en CLAUDE.md)
1. **Excel = Estado.** Gold Master es fuente de verdad. Excel→Python→Supabase→UI, nunca al revés.
2. **Bloomberg Firewall.** NUNCA en UI/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226).
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos/cifras.
4. **No congelar teoría antes que el grafo hable.** ADR-019 a propósito en SUPPORTED.
5. **Commits**: `[area]: desc en español` + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque normal** | **SOLO este BOOT.md. No leas nada más hasta saber tu tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Gate 6.6 / tagging / bridge Excel | `docs/architecture/BRIDGE_EXCEL_CORPUS.md` |
| Gate 7 (segundo municipio) | `docs/adr/GATE-007_Validacion_Externa_Municipio2.md` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Reglas de construcción/UI/dominios | `docs/REFERENCE.md` |
| Ingesta corpus/Holding | `scripts/holding/manifest_holding.py` (docstring) |
| Tocar el grafo Neo4j | `docs/adr/ADR-017` + `ADR-018` |
| Clasificar documentos | `docs/adr/ADR-021` + `docs/architecture/CANONICAL_CHUNK_SCHEMA.md` |
| Hallazgos territoriales | `docs/observations/OBS-005/006/008/009` |
| Estado histórico completo (snapshot) | `governance/historico/QUIRA_STATE_2026-06-03.md` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB Free instancia `6c134c35` (user=DB=instance ID · patrón MATCH+MERGE) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
