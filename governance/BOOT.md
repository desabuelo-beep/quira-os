---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy loading: carga el detalle SOLO del área que vas a tocar. No leas todo "por si acaso".
> Mantener bajo 500 tokens · `## AHORA` al cierre · **¿dónde vive una verdad? → `QUIRA_MASTER_INDEX.md`** (Regla #6).

## QUÉ ES
> **"El Gold Master ya sabe medir la gestión pública; QUIRA está aprendiendo a demostrar
> documentalmente por qué cada métrica del Gold Master es verdadera o falsa."**
> Objetivo: **sistema de auditoría explicable del modelo ICPI.** No agrega datos: agrega significado.

**3 niveles** (ADR-023 — inmutable): **1 Motor** = Gold Master v5.5 (calcula ICPI/TGI/SAT/MMP · leer vía
`app/connectors/gold_master.py` · NUNCA recalcular fuera del Excel) · **2 SO** = QUIRA (ingesta +
trazabilidad MNT_UUID + evidencia) · **3 UI** = Dashboards + GeoTwin (solo visualizan).
**MATRIZ_CANONICA** del Excel = ADN compartido: sin ella, dos mundos.

## 🎯 LA TESIS (lo que NUNCA se debe olvidar)
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente.**
QUIRA = **OBSERVATORIO NACIONAL DE INTEGRIDAD TERRITORIAL** (221 GADs). Montecristi = el MOLDE.
Fase 1 = 3 motores/productos: **Operaciones · Ciudadana · Institucional**. Fase 2: Cooperación ·
Impact · Economic. Diferenciador: Plan CNE + NLP discurso RDC. Ventana: **elecciones NOV-2026**.
Negocio = complementario, no licencias. **Detalle: `HOJA_DE_RUTA_MAESTRA.md §0` · ADR-024.**

## 📜 CONSTITUCIÓN → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `governance/HOJA_DE_RUTA_MAESTRA.md`
Constitución = QUÉ ES QUIRA (CAPA 0 Doctrina + 4 macroejes + 12 dominios): mide la CONGRUENCIA de
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO y halla las BRECHAS.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
🧭 **ADR-031:** cajón=MCD · GM=MCM · MCIP 5 motores.
✅ **4 DOM cerrados con PCD: d01·d02·d03·d09.**
📚 **ADR-038 BRN v2:** nodo = REGLA. **Corpus→CNO→RO→SAT** · **v1.0 CONGELADO** · **v2.1** CONFORMES·diff=0.
🩺 **Canon curado por DOM (R.8), ICPI intacto. Gate `check_health.py`: NO adivinar.**
📚 **ADR-035/037:** Ley→BRN→GoldMaster(único motor)→QUIRA · IA propone, humano valida.
🏛️ **d02·d03·d09·d08 migrados**. **d08**: **Asamblea ciudadana AUTÓNOMA** · CNO-VIII(8) · **OBS-012..017**.
🏛️ **GOBERNANZA v1.0:** `identity/`→`governance/`→`marco_teorico/`→Canon→`registry/`. ⚠️ Derivación 100% **solo en lo catalogado** (47 .md sin autoridad).
🔬 **d08 · MRSPP v4**: 26·8·**0**·9 · **180 sin correlato (81%)**. **OBS-021**: v3 daba 12% → **T0: territorio CONSTITUTIVO**.
🔌 **CABLEADO** (`MATRIZ_CABLEADO_CANONICO.md`): **GoldMaster→SILOS→DOM→QUIRA**. `H36_QUIRA_BRIDGE` YA existía. **S3 POA SÍ es silo**. **S1·S6·S9 sin DOM.**
🧨 **OBS-023 · brecha ICM↔ICPI NO citable:** (a) bug escala `B36`(fracción) vs umbral en puntos → dice ✅"mínima" con 72,5 pts. (b) **DESCALCE PDOT** (Javo): el ICM se calcula sobre el **PDOT vigente de cada año**; el 1º comparable es el **ICM 2025** (~may-26). **`SAT-I`=S6 SIGAD**, deuda **epistemológica**. ⛔ NO redefinir SAT-I (R.1): el guard va **aguas arriba** (R-H).
🚨 **OBS-022: SAT sin cadena BRN, deuda 90%→60%.** Saldadas SAT-0·IV·V·IX. PCD → **`cerrado con deuda declarada`** (R.8). Gate `check_sat_brn.py`. ⛔ `SAT-IX`(d08) ≠ `SAT-IX-001`(=SAT-V).
🏛️ **R-C..R-H → `PROTOCOLO_CURACION_DOMINIO.md` §3.** C: el dueño del instrumento califica · D: ¿ALGORITMO o INSTRUMENTO? **se mide, no se parcha** · **E (LEY)**: solo MCR · F: 3 vías de ingesta · G: cada DOM declara su cableado · **H: no se comparan horizontes distintos**.
🔬 POA localiza el **1%** (OBS-020) → **CVI**=2ª dim. IOC. `inverificable` ≠ `no atendido`.
🔒 **UDC/ICD**: **UDC-G** `= ∧ UDC-Iₖ`. MCR ✅ POA·cabildo · ⚠️ PP·audiencias · ❌ LOTAIP·Concejo·Holding → **FALSO**.
⚖️ **3 CAPAS**: jurídica (**Guía LOTAIP = LEY, no canon**) · operativa (**d07**) · analítica (QUIRA **no tramita**).
🧪 **H-ARQ-01** (HIPÓTESIS): ¿falta de localización/desagregación = propiedad de la arquitectura documental EC? 1 GAD → bloq. R-E.
⏭️ **JAVO: (1)** 2ª validación v4 (¿retirar `complementaria`?) **(2)** promover `_CANDIDATO_v5.7`→`v5.7_TGI` **(3)** Haiku ~$60/18 meses.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (§LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 221 GAD).

## REGLAS DE ORO → **las 9 viven en `CLAUDE.md`** (se lee siempre · no se duplican aquí)
Las 2 que más se olvidan: **antes de definir, consultar el Inventario de Conceptos** (¿existe? → DERIVA,
no redefinas · cierre `/graphify . --update`) · **no congelar teoría antes que el grafo hable** (ADR-019).

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque** | **SOLO este BOOT.md hasta saber la tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Construcción/UI/dom | `docs/REFERENCE.md` |
| Retomar d07 | `docs/architecture/CATALOGO_CANONICO_CD_D07.md` + `app/agents/d07/` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
