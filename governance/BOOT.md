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

## 🎯 LA TESIS (lo que NUNCA se debe olvidar — Javo lo ha dicho muchas veces)
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente** (ADR-024).
QUIRA = **OBSERVATORIO NACIONAL DE INTEGRIDAD TERRITORIAL** (221 GADs). Montecristi = el MOLDE.
Cobertura nacional con **3 MOTORES = los 3 productos de Fase 1**: **Operaciones** (Dylus/QUIRA IA
barre Transparencia/SERCOP/CPCCS + extrae PDOT) · **Ciudadana** (la gente + cascada legal con firma
digital) · **Institucional/Gestión** (el GAD aporta dato ORO directo · GAD predictivo). Fase 2
(después, vistas de explotación): **Cooperación · Impact · Economic** (6 productos total · ADR-024).
Diferenciador: Plan CNE + NLP discurso RDC = demagogia expuesta. Ventana: **elecciones alcaldes
NOV-2026**. Negocio central = complementario (cooperación/certificación/estándar), no licencias.
Detalle completo: `HOJA_DE_RUTA_MAESTRA.md §0`.

## 📜 CONSTITUCIÓN ONTOLÓGICA → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md`
**Define QUÉ ES QUIRA (capa 0 Doctrina + 4 macroejes + 12 dominios).** QUIRA mide la
CONGRUENCIA de la cadena PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO y
encuentra las BRECHAS. Los 12 dominios cambian; la Doctrina permanece. Esto, no los
dashboards, es lo que se define UNA vez. Sprint C: ontología antes que ingeniería.

## 🗺️ HOJA DE RUTA COMPLETA → `governance/HOJA_DE_RUTA_MAESTRA.md`
**Para la RUTA (qué sigue, sprints, productos, GeoTwin 3D, Ciudadana, CAF): leer ese archivo.**
BOOT.md §AHORA = detalle vivo del paso actual. Hoja de Ruta = el mapa completo que no se mueve.

## AHORA (actualizar al cierre)
- **✅ CIRUGÍA GOLD MASTER D.2A — COMPLETA Y VERIFICADA INEXPUGNABLE (2026-06-15 · sobre COPIA · Excel nativo + dump):**
    Registro celda-a-celda → `docs/architecture/CIRUGIA_GOLD_MASTER_D2A.md`. **ICPI 17.45% → 27.46%** (corte abril · proyección
    HONESTA: el GAD va rezagado vs su 2025 ~60-73%, obras G8 dev=0). 3 correcciones, TODAS input/semáforo, **B33 JAMÁS tocada**:
    (1) Adscritas Ti=0: `H07b!D19` Bomberos `0→0.1943` (cédula SERCOP `H90` · jerarquía del propio Excel "Cédula>eSIGEF") +
    `H12!F26:F29` GAD_SIN_ESIGEF `0→=H07b!B20`. (2) Semáforo `H12!B34`: bug de escala (umbrales %→fracción · daba SIEMPRE Ruptura) +
    consciente del corte (mes<12 → "lectura preliminar", no veredicto anual). (3) FactorTemporal `H07_S5!B23`: lineal `mes/12` →
    **curva pacing REAL de Montecristi** (CHOOSE 12m · abril 0.333→0.212 · GAD Ti_norm 19.3%→30.3%) desde `monthly_kpis` Supabase
    (prom 3 adscritas con cobertura 2025 · GAD sin serie intra-anual → proxy DECLARADO · NO hipótesis nacional). Scripts: `scripts/dev/gm_2025_{probe,curve}.py`.
    VERIFICADO determinista: `B33==B31/B32` INTACTA · `B40 ✅ AXIOMA 69.9309%` · **0 errores añadidos** (5 preexistentes idénticos).
    COPIA: `ProyecT\...WORK_20260615_D2A_APLICADO.xlsx` · **VIVO INTACTO** (mtime 05-30).
    ✅ **PROMOVIDO A VIVO (2026-06-15 16:22)** · slot `...v5.5_TGI.xlsx` conserva nombre (= contrato del código, conector intacto) ·
    vivo lee **27.46%** · `B33==B31/B32` verificada. Respaldos: `..._FREEZE_20260615_pre-D2A` (rollback 17.45%) + `..._v6.0_FREEZE_20260615`
    (sello oficial). Conector documentado (`app/connectors/gold_master.py` docstring). Pendientes aparte: revisar curva al cerrar 2026 ·
    5 errores preexistentes (`H98!B36`·`H99!B45` = TGI, fuera del motor ICPI).
    ✅ **MAPA DEL HILO CONDUCTOR documentado** → `docs/architecture/MAPA_HILO_CONDUCTOR.md` (5 capas Raíz→Motor→Puente→Soporte→Cerebro ·
    Regla de Oro · 3 datos del académico corregidos: 2025 ingesta PARCIAL no completa · claves REALES H73 no inventadas · el Puente ORQUESTA no solo exporta).
    🛡️ **REGLA DE DISCIPLINA adoptada (colega):** ningún debate metodológico nuevo salvo que una pantalla/cosecha REAL lo obligue (no re-filosofar ICPI · no rediseñar congruencias · no tocar ontología).
    ▶ **Sprint D.1 · d06 EN VIVO** (cableado, NO teoría · 2 carriles que NO se mezclan: A=QUIRA UI · B=metodología freezer):
    ✅ **PASO 1 VERIFICADO (2026-06-15):** contrato `H73` + pipeline entregan **27.46% + semáforo de corte END-TO-END** ·
    GM corregido **PASA governance** (30 reglas · 0 err · 0 alertas) · ciclo dry-run OK 10.4s **sin tocar Supabase** ·
    claves REALES del snapshot (anidadas): `icpi.global_pct`·`icpi.clasificacion`·`tgi.score`·`tgi.d1..d5`·`financiero.*`·`sat_engine.*` (+`_raw_h73` 64 claves). Tool: `scripts/dev/gm_contract_check.py`.
    Nota: dry-run NO persistió el JSON (guardado=skipped); persistir `gm_snapshot.json` = escritura producción (Supabase+JSON) → paso consciente antes del cableado (Paso 3).
    ✅ **PASO 2 (2026-06-15):** matriz `docs/architecture/d06_MAPPING_MATRIX.md`. Hallazgo: `p_ejecutivo` Q1 YA cablea snapshot (`icpi.global_pct`·`tgi.score`·`sat.*` ✅) ·
    `p6_pulso`+`p7_brecha` = `demo_data`+hardcode. HUECOS reales (el académico decía 'ninguno'): 🟥 4 congruencias→C3/QUIRA IA (no en snapshot) · 🟥 FactorTemporal/Ti_raw/adscritas = celdas INTERNAS no exportadas a H73 (Carril B) · 🟡 texto hardcoded.
    ▶ **PASO 3 INICIADO (2026-06-15 · arquitectura del colega ADOPTADA):** titular = **ICPI 27.46%** (cimiento · Regla 1) · TGI 66.79% = explicador · congruencias = tensión ·
    **cablear ANTES de persistir** (3A cablear→deploy→auditoría visual · 3B Supabase DESPUÉS, no antes).
    ✅ **2 BLOQUEOS RESUELTOS (2026-06-15 22:05 · arteria restablecida):**
    (a) builder `scripts/_update_snapshot.py` **RECREADO** — refresca valores canónicos desde `fetch_gold_master_data()` (H73), **preserva lo curado** (7 parroquias, 5 series longitudinales, gad, notas), respalda el JSON previo. Idempotente, solo lectura del Excel + escritura JSON local.
    (b) `data/gm_snapshot.json` **REFRESCADO**: `icpi.global_pct` **53.56 → 27.46** · clasif "Corte parcial - lectura preliminar" · TGI 66.79 (D1-D5 = 83.2/69.93/59.85/44.79/100) · `version_excel=v6.0_D2A_20260615` · **SIN tocar Supabase** · curado intacto.
    ▶ **PASO 3A EN CURSO (2026-06-16):**
    🚨 **DESCUBIERTO:** `cargar_snapshot`/`load_snapshot` lee **Supabase PRIMERO** y Supabase tiene **17.45% STALE** (pre-cirugía) → el app por su ruta normal mostraba 17.45%, NO el 27.46%. La dispersión era real y activa (3 valores: Supabase 17.45 · JSON viejo 53.56 · JSON nuevo 27.46).
    ✅ `p_ejecutivo` Q1 **RECABLEADO** → `cargar_gm_snapshot()` (JSON LOCAL = 27.46% · sin Supabase) + **ICPI TITULAR** (cimiento · Regla 1) · TGI 66.79 explicador subordinado · SAT del `sat_gm`. Data-verificado + compila OK. Footer v5.5→v6.0.
    🛡️ **FRONTERA DE LENGUAJE (Regla 2 · Javo lo cachó · skill `quira-language-guard`):** `p_ejecutivo` corregido — etiquetas VISIBLES en lenguaje de gobernanza, NO canónico.
    Mapa: ICPI→"Cumplimiento institucional" · TGI→"Gobernanza territorial" · SAT/SAT-III→"Alertas" (nombre+ley, sin código) · "Gold Master/version/Supabase"→"QUIRA Intelligence · Dylus Lab" · ISP→Salud presup. · IED→Eficiencia directiva · IGP→Participación · IOC→Opacidad informativa · IET→Equidad territorial · PSG→Presup. con enfoque de género.
    Claves internas (`icpi.global_pct`…), comentarios y docstrings se CONSERVAN (capa interna permitida).
    ✅ **d06 COMPLETO — CERO demo_data (2026-06-16):** las 3 pestañas (`p_ejecutivo` · `p6_pulso` · `p7_brecha`) leen el snapshot LOCAL (`cargar_gm_snapshot`) ·
    lenguaje de gobernanza (frontera limpia · verificado) · 4 coherencias→"Pendiente análisis contextual" (C3) · 6 vectores reales (isp 3.22·ied 24.94·igp 48.33·ioc 17.71·iet 44.8·psg 2.83) ·
    holding real (GAD 11.2·Pat 19.56·Aseo 18.17·Bom 19.43) · parroquia crítica real (Isabel Muentes $40 vs $217) · SIN narrativa de "caída" (corte parcial ≠ cierre anual).
    Builder extendido (bloque `vectores` en `_update_snapshot.py`). Acid test `grep demo_data` d06 = **0** · las 3 compilan.
    ▶ SIGUIENTE: **auditoría visual** (`streamlit run` → abrir d06 → ¿pantalla muestra 27.46% en gobernanza? = EL HITO · la vive Javo) · luego **3B persistir Supabase** (mata el 17.45% stale). Matriz-spec: `docs/architecture/d06_MAPPING_MATRIX.md`.
    Las 2 anclas (ontología Sprint C + motor inexpugnable) firmes. Cadena cerrada: TESIS→GOLD MASTER→H73→ONTOLOGÍA→DOMINIOS→CONGRUENCIAS→DASHBOARDS.
- **🔎 AUDITORÍA INTEGRAL DEL GOLD MASTER — COMPLETA (2026-06-15 · chat separado · 100% determinista · solo lectura):**
    Entregable único y durable → `docs/architecture/GM_REGISTRO_INTEGRAL.md` (las 123 hojas vectorizadas: ficha · grupo ·
    inputs/outputs · estado · rol ICPI/TGI · gaps). Herramientas reusables: `scripts/dev/gm_full_audit.py` (123 volcados +
    grafo de dependencias por fórmula → `docs/architecture/gm_dumps/`), `gm_probe.py` (valores cacheados), `gm_freeze_diff.py`.
    **TODO sale de la celda, NADA de memoria.** Hallazgos mayores (resumen §0 del registro):
    (1) Motor LIMPIO de errores de fórmula — la cadena H12/H07b/H98/H99/H73 sin `#REF!`/`#DIV`; 3 tokens hallados = 1 falso
    positivo (`H01!A28` texto) + 2 reales periféricos (`H36c!C13`, `H71!B8` enmascarado por IFERROR→0). (2) ICPI=17.45%
    confirmado (`H12!B33=0.174489`; `=B31/B32*100` INTACTA · `H85!CHK-11 ✅`). (3) **5/25 metas con Ti=0** colapsan numerador:
    `H12!F18` Bomberos + `F26:F29` GAD_SIN_ESIGEF. (4) Bomberos SÍ existe en `H90!D7=19.43%` (SERCOP) — es ruteo de fuente, no
    falta de dato. (5) Discrepancia eSIGEF vs SERCOP en los 4 entes (norm infla: Patronato 41.7 vs 19.56 · EP Aseo 72.5 vs 18.17).
    (6) Motor Ci íntegro hoy (`H39!D25/D26/D27 ✅` · 0 hilos rotos) pero `H39!D28 ERROR` (Ci 1pp) + S-04 (Pi hardcodeados en H12,
    no fórmulas a H14). (7) `H73!MMP_AVANCE_PCT` única `VALIDACION_OK=NO`. (8) Brecha rural inconsistente INTERNA (`H73/H99=1.37M`
    vs `H97!V-14=7.47M`). (9) FREEZE diff: 79/123 hojas difieren pero ~70 solo por sello de fecha; sustantivo = H06 +9057 celdas
    SERCOP + reclasificación territorial Rural↔Urbana (H99/CAPA/SCHEMA_TERR/H43). **B33 jamás se tocó.**
    SIGUIENTE: con Javo, decidir sobre copia freezer (INPUT no B33): fuente canónica adscritas (eSIGEF vs SERCOP H90) + curva
    FactorTemporal real + semáforo consciente del corte parcial. El registro es la base para cablear/recablear.
    ⚠️ DIRECTOR (corrige el "copia freezer"): el FREEZE (05-26) es MÁS VIEJO que el vivo (05-30 · sin H06 SERCOP +9057 ni la
    reclasif. territorial) → la cirugía va sobre **COPIA DEL VIVO** (decidir: ¿terminar la reclasif. a medias del vivo, o partir del
    freeze más limpio?). La homologación SERCOP es **BIDIRECCIONAL** (sube Bomberos 0→19.43 · BAJA Patronato 41.7→19.56 y EP Aseo
    72.5→18.17) → homologar los 4 a UNA fuente honesta (recomiendo SERCOP/H90), efecto neto al ICPI se calcula en copia.
- **🏁 SPRINT C CERRADO · SPRINT D ABIERTO (2026-06-14 · 17 commits · jornada de fundación):**
    **Sprint C = Fundación Ontológica → ✅ CERRADO** (13 dominios anclados · Tabla Equivalencias v2 · ESG ·
    Protocolo de Expansión · piloto de falsación d10 PASÓ). **Sprint D = EVIDENCIA OPERATIVA → ✅ ABIERTO**
    (plan completo en `HOJA_DE_RUTA_MAESTRA §5`).
    **▶ PRIMER ACTO próxima sesión = SPRINT D.1: traducir a CÓDIGO el blueprint del MVP demostrador d06** (↓ diseñado ·
    con harness de verificación visual · "60-Second Causality Test"). Contexto d06 (✅ cosechado · el corazón epistemológico:
    ICPI / ICGI-T / 6 vectores ISP·IED·IGP·IOC·IET·PSG · recibe `p7_brecha` · 32 términos Bloomberg).
    🔎 Head-start (cosecha asomada 2026-06-14): `m1_situacion` = el WRAPPER de d06 — 3 tabs → `p_ejecutivo`
    (Vista Ejecutiva) · `p6_pulso` (Pulso) · `p7_brecha` (Causas/6 vectores · ya cosechada). Otras d06: `p1_dashboard` ·
    `p14_eficiencia` (IED) + cantera `_deprecated/p_vista_ejecutiva` (32 Bloomberg) · `_deprecated/p0_inicio`.
    Arranque concreto: leer `p_ejecutivo` + `p6_pulso` → mapear componentes → test de falsación (Tipo A/B/C).
    ✅ COSECHA d06 EJECUTADA (2026-06-14 · plano en Diccionario): la TEORÍA se sostuvo. 🅰️ ICPI núcleo desde
    SNAPSHOT vivo (cache_quira/sentinel/GM v5.5). 🅲 HALLAZGO MAYOR: **d06 = SÍNTESIS** (cross-domain por naturaleza ·
    el ICPI es el CIMIENTO y los índices relacionales se posan ENCIMA — NUNCA lo promedian (Regla 1 · corrección Javo); los vectores cruzan d02/d07/d08/d10/d12 · su dashboard = mapa de causalidad que enlaza,
    no pantalla aislada · CONFIRMA ADR-026 Sintetizador). 🅱️ 2 rutas de datos a unificar (p_ejecutivo snapshot vs
    p6_pulso data.loader) + 6 vectores hardcoded en p7_brecha. ✅ "4 congruencias" (pol/oper/terr/ecosist) = **CAPA DE CONGRUENCIA** sobre el cimiento ICPI
    (lectura relacional que opera la Doctrina · sellada en Constitución · NO es dominio · no dispara Protocolo).
    MODELO B (mesa · adoptado): las congruencias leen los DOMINIOS en las uniones de la Cadena Madre — Política←d01·d03 ·
    Operativa←d02·d04·d05·d06 · Territorial←d10·d11 · Ecosistémica←d12·d13. ELEVACIÓN (colega): es la operacionalización
    COMPLETA de la Doctrina (Capa 0) — el mecanismo que explica POR QUÉ un municipio funciona · transversal · pertenece
    a QUIRA; **d06 = su LAUNCHPAD**, no dueño. UX = TENSIONES (no %). CONTRATO d06 v2.0 PRE-APROBADO (mesa): ① ancla base
    "Cumplimiento Institucional" · ② 4 barras de TENSIÓN · ③ grilla bento relacional (enlaces d02/d07/d08/d10/d12/d13) ·
    ④ filtro exclusión SAT→d04 · Holding→d05.
    ✅ SPRINT D.0 — MATRIZ DE CONGRUENCIAS sellada (Diccionario · recomendación colega): bindeo VERIFICADO
    congruencia→eslabón→dominios→indicador madre→ancla. Director filtró 3ª deriva del académico (d03 IFE-A → H73+corpus,
    NO H26/H31). Estados: Política ✅ · Operativa ⏳(eSIGEF 2026) · Territorial ✅ · Ecosistémica 🟡(IGM/ODS5 MISSING ·
    ICODS-amb a precisar). d07·d08·d09 = capa de verificación que audita cada unión.
    ✅ SPRINT D.1 — BLUEPRINT MVP DEMOSTRADOR d06 (mesa colega+académico · DISEÑADO hoy, NO codificado · "60-Second
    Causality Test"): propósito = probar que las TENSIONES explican el estado institucional (validar la TEORÍA, no el
    código · observador externo 60s · SÍ→Modelo B validado · NO→refinar · ambas salidas buenas). 5 elementos, brutalmente
    simple (SIN GeoTwin/PyDeck/animaciones):
      ① CIMIENTO — KPI central "Cumplimiento Institucional" ~53.56% (snapshot vivo Q1 2026).
      ② 4 BARRAS DE TENSIÓN (Modelo B · muestran ± fortaleza/presión, NO %): Política→IFE-A · Operativa→ISP/IED+SAT ·
         Territorial→IET+INEC · Ecosistémica→PSG+biofísico.
      ⚠️ PRERREQUISITO DEL MVP (de-risk 2026-06-14 · leído data/loader + demo_data.py): las 4 congruencias HOY están
         HARDCODEADAS en demo_data.py (NO salen del Gold Master). 3/4 alinean con Modelo B (política=IFE-A 72.73 ·
         operativa=cadena 47.20 · territorial=IET 44.80) PERO la 4ª DIVERGE: la "ecosistemica" del demo = HOLDING/4
         entidades (d05), NO sostenibilidad d12/d13. → El MVP DEBE: (a) redefinir Ecosistémica = PSG+biofísico (Modelo B,
         no holding) · (b) etiquetar las 4 como "ilustrativo · en calibración Q1 2026" (Regla 3, son demo) · (c) ❓PREGUNTA
         A JAVO (Regla 4): ¿las 4 congruencias del Modelo B existen en el Gold Master como capas relacionales, o son una
         lectura a definir? Si existen → cablear; si NO → su fórmula se define EN EL EXCEL, nunca en Python (no motor paralelo).
      ✅ RESPUESTA JAVO (2026-06-14): las 4 congruencias son el ESPÍRITU de las tesis QUIRA anteriores · NUNCA formalizadas
         en el Excel canónico (sin aterrizaje matemático/metodológico). HOY = capa CONCEPTUAL/narrativa, NO cálculo del motor.
         Corregido en Constitución + Matriz (marco válido, pendiente formalización). Hogar a explorar: QUIRA IA (C3), no el Excel.
         → MVP las muestra como MARCO etiquetado "metodología en formalización", NUNCA como dato calculado (Regla 3/4).
   - **PMV vs MVP (aclaración Javo):** el PMV = QUIRA COMPLETO modelado sobre Montecristi (el molde · el producto real).
     El "MVP demostrador d06" NO es otro producto ni versión chica aparte — es la **1ª TAJADA VERTICAL del PMV**: d06 real
     (el primer cajón/corazón), mínimo→completo, validado con el test 60s, antes de seguir al siguiente. PMV completo construido
     cajón por cajón (vertical), no los 13 de golpe ni un juguete desechable.
   - 🔭 REFLEXIONES JAVO a no perder: (1) **Obsidian/KB** — verificar conexión (solo se cargó `vault_fondos`, el resto del KB ¿conectado?).
     (2) **QUIRA IA (C3 Razonamiento · la capa FINAL del proyecto)** aún NO incorporada — posible hogar de las congruencias narrativas.

- **🔬 SPRINT D.2 — SINCERAR EL EXCEL · ARRANCADO (2026-06-14 · decisión Javo: el paréntesis ya NO se posterga):**
    `scripts/dev/gm_h73_dump.py` → `docs/architecture/GM_H73_DUMP.md`: volcado del contrato REAL del motor
    (H73_OUTPUT_API · 65 claves con celda fuente). 🔴 HALLAZGO BOMBA: el motor dice **ICPI_GLOBAL = 17.45% "Ruptura
    Sistémica"** — pero las pantallas (demo_data) muestran **53.56%. EL PROYECTO ESTÁ DESINCRONIZADO DEL EXCEL.**
    Más desyncs: ISP demo 14.58% vs motor 3.22% · PSG demo 12.83% vs motor 2.83% (el motor guarda FRACCIÓN DECIMAL ·
    unidades a normalizar decimal↔%). El contrato TIENE todo: ICPI · TGI(D1-D5)=66.79 · 6 vectores · ICODS=87.5 (d13) ·
    IEF · IRS · SAT · presupuesto (devengado Q1 $5.14M) · NBI · fondos. Las 4 congruencias NO están en H73 (confirma Javo).
    ⚠️ EL MVP NO debe mostrar 53.56% — el dato real es 17.45%. (Blueprint a corregir.)
    SIGUIENTE (Sprint D.2 · fresco): reconciliar lecturas del proyecto → cablear a las 65 claves de H73 (vía gold_master.py) ·
    reemplazar demo_data · normalizar unidades. RECIÉN entonces el MVP de d06 se construye sobre DATO VIVO, no fachada.
    ✅ MATRIZ DE RECONCILIACIÓN TOTAL construida (`docs/architecture/MATRIZ_RECONCILIACION_TOTAL.md` · 4 inventarios · mesa):
    Inv1 Pantallas→Motor (deuda: p6_pulso·p7_brecha·p10_inversion = demo DESYNC · p_ejecutivo/p10_territorio = semi-live).
    Inv2 Ontología→Motor: **9/13 ✅ respaldo total** · 3 🟡 (d01·d05·d11) · 1 🔴 d09 (sin clave H73 directa). d13 ICODS=87.5 ✅ dorada.
    Inv3 H73→hojas (genealogía del dump: ICPI←H12!B33 · ISP←H19 · PSG←H16c · TGI←H98 · ICODS←H20 · MMP_AVANCE = única NO validada).
    Inv4 Congruencias→datos: solo MARCO Modelo B (insumos), SIN fórmula · pendiente formalizar (Javo/Excel) o reubicar en QUIRA IA.
    Director filtró cifras del académico (IET≠TGI 66.79 · ISP←H19 no H07_S5 · coords B4/B12 inventadas → fuentes reales del dump).
    ✅ DECISIONES JAVO (2026-06-15): (1) las 4 CONGRUENCIAS viven en **QUIRA IA (C3)** — juicios, no aritmética · la cadena
    intersistémica ya está en pantallas ejecutivo/técnico en refactor · NO se calculan en el Excel. Sellado en Constitución/Diccionario/Matriz.
    (2) ⚠️ CORRECCIÓN del 17.45%: NO es "Ruptura Sistémica" — es el ICPI ACUMULADO ANUAL leído en Q1 (mes 4-5), bajo por PARCIAL.
    Anualizado ≈52% ≈ el 53.56% demo (mismo estado, 2 lentes temporales). "Ruptura" = misread (umbral anual sobre valor parcial).
    Sincerar el Excel = definir la LECTURA PROPORCIONAL al tiempo de gestión (metodología Javo/motor), NO cablear el crudo. (Over-celebración del Director corregida.)
    🔬 DIAGNÓSTICO H12 (auditoría 2026-06-15 · `scripts/dev/gm_sheet_dump.py` → `docs/architecture/GM_SHEET_H12_MOTOR_ICPI.md`):
    ICPI = Σ(Pi·Ri·Vi·Ei·**Ti**·Ci)/Σ(Pi·Ri)×100 (H12!B33 · "FUENTE ÚNICA · NUNCA recalcular · NO modificar la lógica").
    **Ti = ejecución eSIGEF (devengado/codificado) = 0.2375 GAD en Q1** → Ti es MULTIPLICATIVO y a mitad de año va ~24% →
    arrastra el ICPI a 17.45%. NO es error de fórmula (el motor funciona): el error es la CLASIFICACIÓN AVEP (B34) que aplica
    umbrales ANUALES (<20%=Ruptura) a un valor PARCIAL → falsa "Ruptura".
    ✅ FIX RECOMENDADO (respeta "no cambiar lo canónico"): NO tocar el Excel (B33 axioma blindado · riesgo de corromper la malla
    de 123 hojas con openpyxl). QUIRA LEE el ICPI crudo + aplica la lectura PROPORCIONAL al periodo en PRESENTACIÓN (mensualizado).
    Errores de FONDO a revisar CON Javo (su metodología · con backup, NO yo solo): (1) "Motor Ci pendiente" (TBL_CALIBRACION_Ci sin
    construir · H01 §M · B40 lo marca) · (2) metas con Ti=0 (GAD_SIN_ESIGEF) que multiplican por cero. SIGUIENTE: decisión de Javo
    sobre la fórmula de normalización mensual + si toca los errores de fondo en el Excel (él, en Excel, con backup).
    🔬 AUDITORÍA H07b (2026-06-15 · `docs/architecture/GM_SHEET_H07B.md`): **¡el % proporcional EXISTE!** (Javo recordaba bien).
    `Ti_norm_2026` (H07b!B20) = `MIN(1, Ti_raw / FactorTemporal(mes/12))` — "avance proporcional al corte mensual". Y el ICPI
    YA lo lee (H12 F=H07b!B20). → NO hay que crear el proporcional. El 17.45% bajo viene de TRES causas (decisión de metodología Javo):
    (a) FactorTemporal LINEAL (mes/12) penaliza meses tempranos — el gasto público es BACK-LOADED (Q3-Q4) → refinar a curva real ·
    (b) metas con Ti=0 (GAD_SIN_ESIGEF) que arrastran el numerador (hueco de realidad: la tesis lo construyó, no subió al Excel) ·
    (c) ejecución 2026 genuinamente baja (devengado 1.95M / codificado 30.27M = 6.4% a abril · ciclo recién arranca).
    EJECUCIÓN SEGURA: trabajar la COPIA FREEZER de Javo (no el canon vivo) · Javo dirige metodología · Claude ejecuta mecánico +
    verifica con dumps · el freezer = rollback. Es metodología profunda = sesión fresca, NO a 30 commits / medianoche.
    ✅ PRINCIPIO INVIOLABLE ESTAMPADO (Javo · 2026-06-15): la **fórmula canónica `H12!B33` es INMUTABLE** · correcciones SOLO
    en inputs/semáforo/presentación · sobre COPIA · con evidencia · verificadas. Estampado en CLAUDE.md (Regla 1 + Prohibición) +
    `docs/architecture/METODOLOGIA_GOLD_MASTER.md` (NUEVO · registro canónico · "para nunca más perder la metodología en tesis archivadas").
    AUDITORÍA FASE 1 (colega): AVEP (config.py · H01) ≥.90 Excelencia · .70-.89 Mandato · .40-.69 Transición · .20-.39 Ocurrencia · <.20
    Ruptura → umbrales calibrados para valor ANUAL · el 17.45% parcial cae en Ruptura porque el SEMÁFORO no sabe que es corte parcial.
    DATOS para la curva: solo 2023-25 anual + 2026 mensual (NO hay 2021-22 ni trimestral pre-2026) → curva con evidencia parcial.
    PLAN CIRUGÍA (colega · bajo inmutabilidad · sobre copia freezer): F1 auditar semáforo/umbrales/Ti_norm/Ti=0 · F2 curva histórica
    Montecristi + mini-Ti por adscrita (NO factor 1.0 = regalar puntos) · F3 aplicar en copia → comparar ICPI actual vs corregido → validar. **NUNCA tocar B33.**
    ⚠️ VERIFICACIÓN DETERMINISTA (2026-06-15 · re-corrida `gm_h73_dump`): el ICPI ES **17.45% 🔴 Ruptura** (timestamp 2026-05-26 · SIN
    cambios). El académico AFIRMÓ 53.56% con números FABRICADOS (codificado 39.3M vs real 45.98M · devengado 11.47M vs real 5.14M ·
    Ti_norm GAD 0.70 vs real ~0.24). El colega reconstruyó el plan sobre esa fabricación, de buena fe. LECCIÓN (refuerza la metodología
    canónica): **ningún número se acepta de memoria/afirmación — SOLO del dump determinista (el árbitro es la celda, nunca la cabeza).**
    RESPUESTA a Javo: SÍ, construir la metodología completa (tesis+motor) es NECESARIO — pero INCREMENTAL (módulo×módulo · reconciliar
    intención-tesis vs realidad-motor · SIEMPRE verificado por dump). El real: ICPI 17% = FactorTemporal sub-normaliza (Ti_norm ~0.24) + Bomberos Ti=0.
    🧱 SPRINT D.2A — HOMOLOGACIÓN ADSCRITAS · FUENTE ENCONTRADA (2026-06-15 · dump `H90_PRESUPUESTO_CONSOLIDADO`):
    **el dato de Bomberos SÍ EXISTE.** H90 tiene los 4 entes con cédula SERCOP Q1-2026: GAD Ti=11.20% · Patronato 19.56% ·
    EP Aseo 18.17% · **Bomberos 19.43%** (cod 1.485M / dev 288.6K). El agujero NO es falta de dato — es que H07b lee el Ti
    desde eSIGEF (H07_S5, vacío para Bomberos=0) en vez de H90 (SERCOP, completo). FIX (sobre copia · INPUT, no B33): homologar
    el Ti de adscritas a H90 (SERCOP) — Bomberos 0→19.43% con dato REAL, NO factor 1.0. ⚠️ H90 difiere de H07b en Patronato
    (19.56 vs 13.9) y EP Aseo (18.17 vs 24.16) → DECIDIR con Javo la fuente canónica (eSIGEF vs SERCOP). Al subir Bomberos, el ICPI sube (deja de ×0).
      ③ REJILLA BENTO — 5 enlaces planos: Ver d02 Presupuesto · d03 Mandato · d10 Cobertura · d12 Género · d13 Ambiente
         (se posan sobre el cimiento, NO lo promedian).
      ④ EVIDENCIA — corte "Q1 2026 · datos en carga" + firma del snapshot del pipeline.
      ⑤ BLOOMBERG — "Cumplimiento Institucional" (nunca ICPI) · "motor de indicadores" (nunca Gold Master).
    SIGUIENTE (arranque EN FRÍO): traducción MECÁNICA de este blueprint a código + harness de verificación visual + deploy. Desguace: p_ejecutivo = {d06 + d04 SAT + d05 Holding}.
    SIGUIENTE d06: decidir las 4 congruencias (mesa) → contrato del dashboard d06 (síntesis con enlaces) → implementación.
    Regla (colega): d10 validó el MÉTODO; **d06 valida la TEORÍA** — sesión propia, en frío. Pregunta de apertura:
    ¿d06 se alimenta de pantallas reales sin reinterpretación? Pase o falle, las dos salidas son buenas.
    Detalle de arranque (loop · olas · doctrina interfaz · Mapa CNE) ↓ en los bloques de esta misma fecha.

- **🧬 SESIÓN 2026-06-14 — LAUNCH PAD DE LOS 12 ADN ARMADO (mesa Javo+colega+académico):**
    Fundación lista para REDACTAR los ADN. Todo sellado en `docs/sprint-c/DICCIONARIO_CONCEPTUAL_QUIRA.md`:
    ✅ NOMENCLÁTOR CANÓNICO — 12 nombres oficiales + alias histórico/backend (FUENTE ÚNICA de nombres).
       Renombrados: d03 Gobernanza del Mandato · d05 Holding e Integración Municipal · d12 Inclusión,
       Equidad y Género. ✅ PROPAGADO a Constitución (Capa 0.5 + macroejes + índice) + PLANO_DE_CAJONES
       (check 2.5 OK · Hoja sin tabla de dominios · snapshot UI viejo lo corrige el refactor L2).
    ✅ PLANTILLA MADRE elevada 9→11 CAMPOS (Capacidad 0.5 → Dominio → … → Expresión GeoTwin).
       Cajón 10 re-sellado como molde definitivo. CONVENCIÓN SELLADA (fallo Javo): indicador madre =
       CONCEPTO puro, NUNCA "Índice de…" (Regla Oro 3 · evitó el 4º índice inventado del académico).
    ✅ MATRIZ MAESTRA (idea colega) = índice de la ontología: Capacidad↕Dominio↕Madre↕Operativos↕GeoTwin.
    ✅ d01 Planificación Estratégica = primer ADN completo bajo la nueva arquitectura (revisado por mesa).
    SIGUIENTE: redactar d02→d09 → d11 → d12 (10 ADN restantes), uno por uno, propuesta→mesa→siguiente.
       Después: propagar Nomenclátor a Constitución/Hoja · Tabla de Equivalencias definitiva · cosecha.
    Método mesa confirmado: "revise, mejore, supere, ejecute" · indicadores SIEMPRE reales · Javo decide.

- **🔩 ANCLAJE AL MOTOR — "ancla mínima" ejecutada (2026-06-14):** la ontología atada al Gold Master.
    DECISIÓN mesa: anclar AHORA (no cajones-ciegos + merge) · auditoría de fórmulas (B) sigue DIFERIDA.
    ✅ `scripts/dev/gm_surface_map.py` (determinista · $0 · sin LLM) → `docs/architecture/GM_SURFACE_DUMP.md`:
       Excel v5.5 vivo = 123 hojas · 119 LLENAS · 0 muertas · 4 incompletas (H65/66/67 Ciudadano IN + H34b narrativa).
    ✅ `docs/architecture/MAPA_ANCLAJE_MOTOR.md` = cajón→operativo→hoja motor→estado (LIVE/PENDIENTE/MISSING).
    HALLAZGO: motor ~97% poblado · auditoría may-26 quedó STALE (H26 18→43 · H31 33→58 · H11b poblada 41/47).
       Único hueco que toca cajones = cédula eSIGEF 2026 (H07_S5) → destraba d02/d03/d06 2026 a la vez (CHK-08).
       MISSING reales = externos d12 (IGM RRHH/CNE · ODS5 PNUD). LLENA=poblada, NO verificada-correcta (=auditoría B).
    ✅ 4 ADN ANCLADOS sellados en Diccionario: d01 · d02 · d03 (el SELLO QUIRA · eslabón PROMESA↔PLAN) · d10.
       Director filtró 3 derivas del académico: d01 sin "Vector IED" (IED es d02/d06) · d03 ancla a
       H73+corpus promesas (NO H26/H31) · d03 "NLP del discurso" bajado a capa futura Sprint E (no operativo hoy).
       Plantilla campo 10 ahora incluye "ancla motor (código·estado)" · Matriz Maestra apunta a MAPA_ANCLAJE_MOTOR.
    ✅ TANDA 1 sellada (2026-06-14): d04·d05·d06·d07·d08·d09 anclados — todos ✅ LIVE
       (d04 riesgo-matrix ⚠️HARDCODED · d06 ICPI 2026 ⏳ T_i_2026/eSIGEF · d08/d09 H31+H10c LIVE).
       **10/12 ADN completos y anclados.** Cadencia: 2 tandas temáticas (cada tanda = lote revisable de mesa).
    ✅ TANDA 2 sellada — **12/12 ADN COMPLETOS Y ANCLADOS** · fundación ontológica del Diccionario CERRADA.
       d11 corpus PDOT (campo verde · sin hoja GM · NO se inventó madre del motor) · d12 PSG H73 LIVE + IGM/ODS5 MISSING.
    ✅ TABLA DE EQUIVALENCIAS v2.0 DEFINITIVA (`TABLA_EQUIVALENCIAS_v1.md`): puente UNA verdad → 3 QUIRAs
       (Operaciones / Institucional / Ciudadana) · 12 dominios + indicadores + B/C · = auditoría de lenguaje de los ADN.
       Hallazgos a ratificar: d05 "Holding"→"Empresas y Entidades" · "equidad" en 2 sentidos (IET d10 vs d12 género) ·
       IOC nunca "opacidad" · CERRADO: ICPI(índice)="Cumplimiento Institucional" vs d06(dominio)="Salud Institucional".
    ✅ 5 hallazgos de lenguaje RATIFICADOS (mesa) · d03 Institucional = "Cumplimiento del Mandato Democrático".
- **🌍 d13 SOSTENIBILIDAD Y RESILIENCIA AMBIENTAL creado (2026-06-14 · commit aa5e289 · 1er ejercicio de Mutabilidad):**
    Radar del fundador: ambiente estaba descolado (gemelo de género para el Banco Verde CAF). Mesa partida
    (académico=d13 dominio · colega=capa ESG); Director sintetizó: **d13 + vista ESG + gate**.
    Justificación: el dato biofísico estaba HUÉRFANO (362 ind Sprint B sin cajón) + "Resiliencia" pasa exportabilidad.
    GATE sellado (cierra slippery-slope): un dominio entra solo si pasa exportabilidad + tiene data huérfana propia.
    Propagado: Constitución (Capa 0.5/Macroeje 4/índice 13/nota Mutabilidad+ESG) · Diccionario (Matriz + ADN d13) ·
    CLAUDE.md (prohibición "D01-D12 inmutables" reconciliada al gate) · MAPA_ANCLAJE (d13) · Tabla v2.0 (+ESG).
    Ancla d13: ICODS (ODS · sub-eje a precisar) + corpus biofísico (Supabase 362) + riesgo (KB_RIESGOS) → LIVE corpus.
    **13/13 ADN.** ✅ PROTOCOLO DE EXPANSIÓN ONTOLÓGICA sellado (6 condiciones · ley del gate · Constitución):
       capacidad universal+exportable · data huérfana · no solapamiento · ancla real (Regla 3) · obligación de
       propagación+check · consenso de mesa. Cierra el slippery-slope; d13 es el precedente.
    SIGUIENTE FASE: **COSECHA ATÓMICA** (ontología→ingeniería · el freeze de código se levanta — fundación cerrada).
       SECUENCIA DISCIPLINADA (NO saltar a código, lección del refactor L2 atascado): (1) inventario REAL de la
       pantalla cantera (leyéndola, no adivinando) → matriz [pantalla·componente·indicador·dominio·capacidad·
       estado(Mapa)·dashboard] · (2) contrato del dashboard (maqueta texto) → consenso mesa · (3) código ·
       (4) gate Bloomberg 0 + verificación VISUAL en deploy. Cruza MAPA_NAVEGACION × MAPA_ANCLAJE.
       PILOTO: d10 Cobertura (plano sembrado en Diccionario + conecta GeoTwin).
       ⚠️ ANCLAS — verificar c/u contra el Mapa (el académico deriva): cobertura agua/saneamiento d10 = INEC/corpus/
       loader (NO H73) · H73 solo IET. Estilo "Bloomberg" = fase UI, no cosecha. Dashboards se nombran por dominio.
       **PRUEBA DE REALIDAD del piloto d10 (criterio de falsación — el 1er test empírico de la fundación):**
       ✅ PASA si cada componente real de la pantalla mapea a UN dominio + un ancla REAL del Mapa, sin huérfanos ni forzar.
       🔴 FALLA si: un componente no cabe en ningún dominio (=hueco ontológico) · su indicador no está en el Mapa
       (=dato fantasma) · cabe en DOS dominios (=problema de frontera). Cada fallo NO se fuerza: es hallazgo que corrige
       la ontología (como d13 nació de un hueco). Pregunta del test: ¿se alimenta de pantallas reales SIN reinterpretación?
       ✅ PILOTO d10 — INVENTARIO EJECUTADO (2026-06-14 · leyendo pantallas reales): la ontología SOBREVIVIÓ.
       Tipo A (núcleo encaja): agua → QTMP AGUA_POTABLE (Neo4j) · inversión p.c./IET/brecha → data.loader.
       Test cazó: 🅲 p7_brecha MAL asignada al plano (es d06 ICGI-T 6 vectores, NO d10) → cosechar en d06 ·
       🅲 saneamiento/recolección SIN pantalla cantera (huecos) · 🅱️ EJES_INVERSION = material d02 + HARDCODED.
       Plano d10 corregido en Diccionario. FALTA: implementación (código) = próxima sesión CON harness de verificación.
       🧊 REGLA SPRINT D (mesa · inviolable): ontología CONGELADA — cero cambios de dominio/capacidad/ADN/Tabla salvo que
       una cosecha descubra un Tipo C ESTRUCTURAL (nuevo "biofísico huérfano") → solo entonces, Protocolo de Expansión.
       ORDEN SPRINT D = EVIDENCIA: (1) cosecha pantallas restantes · (2) contratos de dashboard (maqueta texto) ·
       (3) implementación Tipo A (Supabase/PyDeck) · (4) verificación visual (gate Bloomberg 0 en deploy caliente).
       PLAN SPRINT D sellado en `HOJA_DE_RUTA_MAESTRA §5` (objetivo FUSIONADO: trazabilidad=medio, entender el cantón
       sin PDOT=fin · pregunta científica colega: ¿la ontología describe o deforma? · 4-step loop · 3 olas).
       Reconciliación: insertado Sprint D Evidencia (no renombrado) → E=Ciudadana · F=Barrido. Ola 1 (orden colega):
       **d06 Salud Inst → d02 Presupuesto → d10 Cobertura**. DOCTRINA INTERFAZ (Javo): cero menús/sidebars, los 13
       cajones SON el command center (no hay "pantalla del alcalde"). CAPA 1 "Efecto Mapa CNE": Ecuador→cantón→13
       cajones (shell Montecristi ahora · nacional en Sprint F · eleva la Caja 0). Arrancar: cosecha d06 ∥ implementación d10.
       Auditoría de fórmulas (B) diferida · ICODS-ambiental a precisar.

- **🔚 CIERRE DE SESIÓN 2026-06-13 (se acabó contexto · nuevo chat):**
    Pivote mayor: dejamos de diseñar dashboards y construimos LA TEORÍA DE QUIRA.
    "Primero la ontología, después la ingeniería" (mesa Javo+colega+académico).
    **FUNDACIÓN ONTOLÓGICA en curso** → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md`:
    ✅ Capa 0 Doctrina (cadena PROMESA→...→TERRITORIO · congruencia · brechas · genealogía
       SIAP-ICPI mide→QUADRUM detecta→QUIRA explica · raíces CONGELADAS recuperadas del corpus)
    ✅ Capa 0.5 Capacidades del Estado (12 capacidades universales → 12 dominios · pasó prueba
       de exportabilidad Ministerio de Salud → teoría LAC, no sistema municipal)
    ✅ 4 macroejes · GeoTwin capa transversal epistemológica (base PDOT 6 componentes + gestión
       12 dominios) · mutabilidad de dominios · ADN Cajón 10 plantilla madre.
    Docs Sprint C: CONSTITUCION · DICCIONARIO_CONCEPTUAL (d10 hecho) · PLANO_DE_CAJONES (cosecha
       atómica) · TABLA_EQUIVALENCIAS (TGI=Territorial Governance Intelligence · ICPI=Calidad
       Pública Institucional · AVEP interno · MMP externo) · MAPA_NAVEGACION (4 muertos archivados
       en _deprecated/) · audit_bloomberg_l2 (p07=31 la peor real).
    SIGUIENTE: completar 12 ADN bajo marco de CAPACIDAD (integrar d01-04 del colega, corregir
       indicador inventado de d02) → Tabla Equivalencias definitiva → cosecha → dashboards.
    **PROMPT del nuevo Claude** → `governance/PROMPT_ARRANQUE_PROXIMA_SESION.md` (actualizado).
    REGLAS reforzadas: indicadores SIEMPRE reales (frenado 3 veces a asesores que inventaban) ·
    conceptos abstractos nivel CAF/BID · navegar el grafo, no leer docs enteros (ahorrar tokens).

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
    ✅ OBSIDIAN LOCALIZADO Y CARGADO (ruta Javo: C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi):
    Módulo 06_Fuentes_Financiamiento = 18 notas de fondo + CATASTRO 40 fuentes + dashboard.
    `vault_fondos_loader.py` (determinístico, $0): **18 líneas VALIDADA + 7 emisores nuevos**
    (BEI·CELEC·COSUDE·GIZ·GCF·NED·OSF·Embajadas). Distribución: 18 VALIDADA · 10 SIMULADA.
    **HALLAZGO MAYOR del vault**: el cantón tiene financiamiento ACTIVO EN EJECUCIÓN que las
    fichas v1 no veían — CAF acueducto agua cruda (80/20) · BEI/PROGAPSA alcantarillado Eloy
    Alfaro (mixto, 15% no reemb.) · BDE alcantarillado La Sequita-Pepa de Huso · BDE Premio
    Verde Manglar (Fase 1 ejecutada) · CELEC compensación estudios. + PAI pipeline USD 366.7M ·
    48 articulaciones PDyOT. FICHA-02 v2 DEBE incorporar esto (la v1 decía "ninguno accesible").
    El vault además ya tenía score_quira por fondo calculado por GM v5.4 (módulo fondos del Excel).
    **FICHA-03 v2 GÉNERO ✅** (2026-06-10 · `docs/sprint-b/v2/FICHA-03_v2_genero.md`):
    Primera ficha formato PRODUCTO (filosofía Colega): Situación→Evidencia→Causalidad→Territorios→
    Costo→Oportunidades→UNA Próxima Decisión. Narrativa nueva: "el hogar cambió; la política no" ·
    "la pregunta no es si existen fondos — es por qué género no está entre las 48 articulaciones".
    Decisión única: generar evidencia territorial (censo INEC jefatura parroquial + DINASED)
    ANTES de gestionar el siguiente fondo. Honestidad: SIMULADA presentada como mecánica, no como
    oportunidad; oportunidades citadas = VALIDADA del vault (Ford·USAID·CFLI·PNUD).
    → FORMATO APROBADO POR MESA (Colega: "APROBADA con ajustes menores · plantilla base").
    **FICHAS v2 COMPLETAS 4/4** (2026-06-10 · `docs/sprint-b/v2/`):
    3 ajustes Colega aplicados a la plantilla: evidencia/interpretación separadas por columna ·
    sección CAPACIDAD INSTALADA · oportunidades divididas gestión vs financiamiento.
    FICHA-02 v2 Agua: "el cantón ejecuta crédito HOY — ¿llega donde la brecha es mayor?" ·
    decisión: siguiente proyecto del banco municipal = Isabel Muentes.
    FICHA-06 v2 Residuos: decisión = ventana CELEC activa → estudio cierre técnico de la celda.
    FICHA-05 v2 Empleo: la ficha de la frontera honesta ("no se puede medir") · decisión =
    obtener tasa juvenil INEC antes de diseñar programas. Megaproyectos marcados no-materializados.
    Regla metodológica permanente adoptada: UNA ficha = UNA decisión.
    Las 4 fichas v2 = primer producto de inteligencia pública de QUIRA (lenguaje para
    alcaldes/CAF/UEB/ciudadanía · Bloomberg-safe · límites declarados · pie técnico omitible).
    **VEREDICTO DE MESA FINAL** (Colega · 2026-06-10): Fichas v2 APROBADAS · GeoTwin SIGUIENTE ·
    Gold Master ESPERAR ("el territorio todavía sigue hablando").
    **HALLAZGO CONCEPTUAL — FAMILIAS A/B** (patrón emergente de las 4 decisiones):
    Familia A = problemas que requieren EVIDENCIA antes de actuar (género·empleo: "medir primero").
    Familia B = problemas donde la evidencia existe y falta GESTIÓN (agua·residuos: "focalizar lo activo").
    Capa analítica nueva para clasificar problemas públicos — candidata a principio de diseño.
    Conclusión Colega del sprint: "casi la mitad de los vacíos atribuidos al modelo eran conocimiento
    territorial que ya existía sin estructurar" — justifica la Operación Minera ANTES que cirugía GM.
    **CONSULTA API RESUELTA (Javo · 2026-06-10): NO recargar para GeoTwin v1.**
    El KB estructurado ya tiene la capa GeoTwin esencial vía determinística ($0):
    POLÍGONOS CUP (13 polígonos · áreas ha · barrios listados · CUP total 3,952.2 ha) +
    KB_RIESGOS georreferenciado por sitio (Playa San José·La Pila·Los Ceibos · inundación 10,032 ha).
    kb_loader F4+F5 CARGADO: censo final **2,004 indicadores** (PUGS 27 · BIOFISICO 408 con riesgos
    territoriales). Limpieza: 443 duplicados por anio NULL eliminados + clave normalizada s/f.
    La recarga API queda como COMPLEMENTO
    (PUGS normativo fino del narrativo + resto Plan Bicentenario, 1,254 chunks reanudables) —
    no como bloqueo. GeoTwin v1 arranca con lo que hay.
    **GEOTWIN NARRATIVO v1 ✅ VALIDADO** (2026-06-10 · `app/engines/geotwin_narrativo.py`):
    Mandato Colega ejecutado: GeoTwin nace EXPLICANDO, no visualizando. 3 casos generados EN
    RUNTIME desde pdot_indicadores (no documentos estáticos — si el dato cambia, la narrativa cambia):
    CASO 1 Isabel Muentes: el motor COMPUTÓ la convergencia — peor del cantón en 4/5 dimensiones
    + hallazgo nuevo del motor: es el polígono urbano MÁS EXTENSO (777 ha) con los menores servicios.
    CASO 2 Riesgo: hallazgos nuevos en runtime — incendios forestales 48,399 ha (el riesgo MAYOR
    del cantón, invisible hasta hoy) · deslizamientos 4,547 ha · 40 riesgos con nombre de lugar ·
    "depósitos clandestinos de basura en quebradas" en Colorado/Isabel Muentes (residuos↔riesgo↔IM).
    CASO 3 Brecha urbano-rural: ratios computados 7.2×/2.3×/3.0× + serie NBI + comunidades dispersas.
    CRITERIO COLEGA CUMPLIDO: el motor explica los 3 casos con los 2,004 indicadores — y encontró
    señales que su constructor no conocía. GeoTwin = validado conceptualmente. CLI:
    `python -m app.engines.geotwin_narrativo [--caso N]`. Siguiente: capa visual cuando mesa ordene.
    **CIERRE SPRINT B — DIRECTIVA SIGUIENTE ETAPA** (Colega asesor · 2026-06-10):
    Hipótesis arquitectónica VALIDADA: "el territorio puede explicarse a sí mismo si se estructura
    correctamente la evidencia". El sistema produce CONOCIMIENTO NUEVO (inferencia territorial).
    🧊 CONGELAMIENTO de ciclo corto: Gold Master · nuevas métricas · nuevos módulos. NO abrir
    frentes nuevos ("cuando algo empieza a funcionar, conviene entenderlo antes de expandirlo").
    📋 SIGUIENTE ETAPA (en orden): (1) VALIDACIÓN EXTERNA de los 3 casos GeoTwin — protocolo y
    material listos en `docs/sprint-b/GEOTWIN_VALIDACION_EXTERNA.md` (entrevistas 15-20 min a
    técnico municipal/director planificación/conocedor del cantón · pregunta central: "¿esto
    explica mejor el territorio que un informe tradicional?" · SÍ → GeoTwin = producto → capa
    visual · NO → las razones = backlog del motor). (2) Refinar motor narrativo. (3) Capa visual.
    ⏳ API: no recargar — 1,254 chunks = valor incremental, no crítico.
    Conclusión de mesa: "La siguiente etapa ya no es descubrir datos; es demostrar que la
    explicación territorial genera valor para usuarios reales."
    ~~ACCIÓN JAVO: agendar 1-3 entrevistas de validación~~ → **VALIDACIÓN CERRADA INTERNAMENTE**
    (Javo · 2026-06-10): "yo valido, soy técnico, conozco Montecristi, armé el modelo y el Excel".
    Colega concuerda: la validación funcional ocurrió DURANTE el sprint (el motor encontró relaciones
    no explícitas · contradicciones · convergencias multisistema · corrigió hipótesis · cambió
    decisiones). El protocolo queda como activo reutilizable para Municipio 002+.
- **SPRINT C — OPERACIONALIZACIÓN · ABIERTO** (mesa Javo+Colega+Director · 2026-06-10):
    **Objetivo único: "Que una persona pueda abrir GeoTwin y entender Montecristi sin leer el PDOT."**
    Cambio de modo: DESCUBRIR→ESTRUCTURAR→EXPLICAR ✅ → **OPERAR**.
    🧊 NO abrir: auditoría GM · nuevas métricas · nuevas dimensiones · más extracción PDOT.
    Riesgo declarado: "parálisis por riqueza de información" — el cuello es convertir conocimiento
    en herramienta que alguien use.
    FRENTES (orden Colega):
    F1 (prioridad máxima) GeoTwin Visual v1 — mapa→clic parroquia→GeoTwin explica. EXPERIENCIA, no dashboard.
       ✅ RECONOCIMIENTO: el mapa YA EXISTE (p4_geotwin.py 327 líneas Folium + 
       data/parroquias_montecristi.geojson 7 features) + motor narrativo listo + base 2,004.
       F1 = CABLEAR motor al mapa existente (no construir de cero). Nota: reconciliar tipos
       urbana/rural del geojson vs CUP del PDOT.
    F2 Fichas automáticas — indicadores→motor→ficha v2 generada (patrón geotwin_narrativo → formato ficha).
    F3 Radar vivo — promover ~10 fondos del vault VALIDADA→VIGENTE con verificación web real.
    F4 CASO DEMOSTRADOR: Isabel Muentes — GeoTwin+Ficha+Radar+Financiamiento sobre UN caso.
       Estrategia Director: F1 arranca CON IM como primer contenido (F1+F4 juntos).
    Roadmap actualizado: A✅ → B✅ CUMPLIDO → **C OPERAR** → D...
    **F1 GEOTWIN VISUAL — CABLEADO COMPLETO ✅** (2026-06-10):
    Flujo del Colega implementado: Mapa → Clic → Narrativa → Indicadores soporte → Decisión sugerida.
    `geotwin_narrativo.py` + `explicar_parroquia(nombre)` (generalización del Caso 1 — primer paso
    hacia explicar_territorio(objeto)) + `render_panel_html()` Bloomberg-safe + fallback snapshot IM.
    `p4_geotwin.py`: st_folium captura clic (last_object_clicked_tooltip) → panel "GEOTWIN EXPLICA"
    full-width con cache 1h. Decisiones CURADAS de las Fichas v2 (no se inventan en runtime — solo
    IM la tiene). Verificado funcional: IM live 5/5 peor del cantón · polígono mayor · decisión ✓ ·
    Colorado degrada elegante (1/5, sin decisión) · fallback OK.
    Criterio F1 (Colega): "clic en IM → entender en <30s" — panel: resumen 1 línea + 5 dimensiones
    + paradoja 777ha + decisión = ~25s de lectura.
    **C2 ✅ LAS 7 PARROQUIAS** (commit e4ccae8): 6/7 con 5 dimensiones completas (La Pila 1 = G-14
    real). Alias toponímicos agregados + fix [EST] (LIKE prefijo). IM 5/5 peor; ninguna otra >1.
    ❓JAVO confirmar toponimia: geojson/demo_data dicen "Leónidas Plaza" · PDOT dice "Leonidas Proaño".
    **🚀 DEPLOY DESBLOQUEADO** (2026-06-10): el repo estaba **135 commits adelante de GitHub** —
    por eso quiraholding.streamlit.app no mostraba cambios (el deploy se alimenta del push).
    PUSH ejecutado (d2bcd64→e4ccae8): TODO Sprint B+C va al deploy. Streamlit Cloud redespliega
    automáticamente en minutos. El motor narrativo en cloud usa secrets del dashboard (database ya
    configurada — p18 la usa) y si falla → fallback snapshot IM por diseño.
    **VERIFICACIÓN VISUAL C1 — guion 60s para JAVO** (post-redeploy):
    1. Abrir quiraholding.streamlit.app (esperar redeploy ~5 min tras el push)
    2. Login → módulo ④ GeoTwin · Territorio
    3. Clic en el círculo de Isabel Muentes en el mapa
    4. Confirmar: aparece panel "🧠 GEOTWIN EXPLICA · ISABEL MUENTES" con 5 dimensiones,
       paradoja 777 ha y decisión sugerida — ¿se entiende en <30 segundos? → F1 TERMINADO (veredicto Colega).
    **🔧 FIX CAJONES L1 — CAUSA RAÍZ RESUELTA** (commit 3c20ffa · 2026-06-11):
    Síntoma Javo (deploy): "no se abre ningún cajón, no hay dashboards, no hay conexión GeoTwin".
    CAUSA: bug de diseño del bridge postMessage — cards envían a window.parent pero el listener
    se registraba en el iframe del script (los message events solo llegan a la ventana destino)
    → el listener JAMÁS recibió nada → L1→L2 nunca funcionó (ni local ni cloud).
    FIX: listener en window.parent (same-origin srcdoc) + selector 'button' robusto a versiones.
    La cadena completa ya existía: 12 cards qNav() → botones ocultos __QNAV_x__ → gov_module →
    env_gov rutea (incl. geotwin→p4 con F1). PUSHEADO → redeploy ~5 min → Javo re-prueba:
    refresh + relogin (el reboot mata sesión) + clic en cualquier cajón → dashboard L2 ·
    cajón Territorio/acceso GeoTwin → mapa → clic Isabel Muentes → panel F1.
    + Toponimia corregida en mismo commit (geojson Leónidas Proaño + tipos: solo La Pila rural).
    Lo que SIGUE crudo (inventario UX Colega + Sprint D): L2/L3 de entornos Ciudadana ·
    Institucional fino · Operaciones ("en construcción") — la arquitectura L1→L2→L3 del entorno
    Ejecutivo queda operativa con este fix.
    **⚠️ RE-PRUEBA JAVO NEGATIVA (2026-06-11): cajones siguen muertos en deploy.**
    LECCIÓN REGISTRADA (patrón señalado por Javo): "Claude siempre decía está conectado todo
    pero nunca se pudo pasar de los cajones" → REGLA NUEVA: ningún cableado UI se declara
    funcionando sin verificación VISUAL en el deploy (no basta sintaxis+lógica).
    Causa probable residual: iframe sandbox cross-origin en Streamlit Cloud bloquea el acceso
    a window.parent (el fix postMessage funciona local, puede no en cloud) — O la prueba fue
    pre-redeploy. **EXPERIMENTO BINARIO pusheado (c6e7ccd): footer ahora muestra
    "UI v1.1-cajones · 2026-06-11"** → si Javo ve v1.1 y cajones muertos = sandbox confirmado →
    **DECISIÓN: matar el bridge — reescribir cajones L1 como nativos st.button estilizados**
    (1 sesión enfocada). Si funcionan = era timing del redeploy.
    **✅ CENTRO DE MANDO v2 NATIVO CONSTRUIDO Y PUSHEADO** (commit e006702 · 2026-06-11):
    Experimento v1.1 confirmó sandbox → bridge MUERTO. `p_command_center_v2.py`: st.container +
    st.button REALES (DOM Streamlit, cero iframes de navegación — no puede fallar). 12 cajones
    con specs Javo (CONCEPTO+número+GANCHO 12/12) · KPI band clicable · estética via CSS
    st-key-* (temperaturas conservadas) · botón QUIRA IA nativo→control · stamp UI v2.0-nativo.
    env_gov._render_inicio → v2 con fallback v1.
    **🎯 CAUSA RAÍZ DEFINITIVA HALLADA Y CORREGIDA (commit bb71144 · 2026-06-11):**
    env_gov tenía DOS rutas al Centro de Mando: _render_inicio (Directivo/Admin — ya cambiada)
    y la Landing Ejecutivo L569 (LA PUERTA DE JAVO) que seguía importando v1 → por eso veía
    v1.1 con el v2 desplegado y sano. Ambas rutas ahora → v2.
    **VERIFICACIÓN CON OJOS (regla nueva en acción):** harness `scripts/dev/preview_cc2.py`
    (sesión simulada SIN tocar auth) + Playwright localhost: v2 renderiza completo (stamp v2.0 ·
    11 ABRIR · conceptos 12/12 · KPIs vivos GM 17.4%) y CLIC VERIFICADO: "NAVEGACIÓN DISPARADA
    → gov_module='ods'". Build stamp pre-auth verificado en deploy por Playwright (pipeline
    GitHub→Cloud ~1-2 min OK). Episodio "ventana --no-sandbox": Javo miraba el navegador de
    pruebas de Playwright con sesión vieja — cerrado.
    **🎉 CAJONES ABREN (Javo 2026-06-12): "Ahora sí entramos, se da click y aparecen las pantallas."**
    El muro de semanas cayó. NUEVO DIAGNÓSTICO al entrar: los dashboards L2 son las pantallas
    de la era TERRA sin reestructurar, con NOMENCLATURA CANÓNICA PROHIBIDA VISIBLE (violación
    Regla de Oro 2 en producción) — incl. "Pregúntale a QUIRA" → Sentinel-Terra tal cual.
    Directiva Javo: REFACTORIZAR TODOS los dashboards — uno por uno, con base, consensuado,
    propuesta antes de ejecutar. Las pantallas viejas sirven como insumo, no como resultado.
    **AUDITORÍA BLOOMBERG L2 ✅** (`scripts/dev/audit_bloomberg_l2.py` · strings renderizables):
    🔴 p_vista_ejecutiva 32 · p07_transparencia 31 (mayoría metadatos internos — confirmar) ·
    🟠 m2_alertas 17 · p0_inicio 11 (¿huérfana post-v2?) · 🟡 11 páginas 1-7 c/u ·
    ⚠️ m1/m3/m4 "limpios" son WRAPPERS — hijos Terra se auditan por cajón.
    **PROPUESTA EN MESA** (`docs/sprint-c/PROPUESTA_REFACTOR_L2.md` — pendiente consenso):
    Paso 0 tabla de equivalencias de lenguaje → plantilla canónica (concepto·gobernanza·dato
    vivo·decisión curada·límites) → gate por dashboard (Bloomberg 0 + verificación visual
    harness + deploy) → cadencia maqueta-texto→consenso→ejecución→mirada Javo.
    Orden propuesto: 1º Salud Institucional (pantalla del alcalde, la peor) · 2º Territorio
    (conecta F1) · 3º RDC · 4º Cooperación. Paralelo sin código: contenido cajones L1 con Javo.
    QUIRA IA: reemplazo del Sentinel-Terra en el programa — dependencia créditos API.
    RE-PRUEBA JAVO (la definitiva): SU Chrome → Ctrl+Shift+R → login → cards con concepto +
    botón ABRIR → → clic → dashboard L2. Footer: UI v2.0-nativo.
    **SPECS JAVO PARA CAJONES v2** (registradas · 2026-06-11):
    cada cajón = (a) CONCEPTO: qué ES este dominio en lenguaje humano (definir/conceptualizar),
    (b) número duro representativo, (c) GANCHO que invite a entrar al dashboard.
    "Su info no me dice nada, es solo un número frío" → aplicar el patrón del motor narrativo a L1.
    **QUIRA IA — TESIS JAVO VALIDADA**: la IA junta todo (resultado final del ecosistema) —
    enseña/explica/educa/guía a CADA rol (alcalde·técnico·ciudadano·operaciones). ES C3
    Razonamiento (arquitectura ya definida) + Sentinel existente en m5_control. El botón
    "Preguntar a QUIRA" era DECORATIVO (onclick=void(0)) → cableado a 'control' (c6e7ccd).
    Ubicación correcta: header transversal (siempre visible). Implementación plena = Sprint C/D
    con dependencia de créditos API (Haiku conversacional).
    **UX/UI — PREGUNTA DE MESA ABIERTA** (Javo · 2026-06-10): cajones/tarjetas/dashboards sin tocar
    hace semanas + dominios comprados (dyluslab · quiraintelligence) sin destino definido.
    POSICIÓN DEL DIRECTOR para la mesa: Sprint D = PRODUCTO & EXPERIENCIA, después de cerrar C
    (C3 comparador + F3 radar). Alcance D: (1) UX refresh del laboratorio (cajones/tarjetas/
    dashboards), (2) decisión dominios: quiraintelligence.com = portal radar nacional (YA definido
    en ADR-024 Capa D como PRODUCTO PRINCIPAL) · dyluslab.com = corporativo, (3) GeoTwin visual
    pulido como pieza central demo UEB/CAF. ⚠️ Nota técnica: Streamlit Community Cloud NO soporta
    dominios custom → quiraintelligence.com requiere decisión de hosting (costo) — decisión de mesa.
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
