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

## QUÉ ES → `identity/CONSTITUCION_INSTITUCIONAL.md` (CONSTITUCION-001 · raíz `parent:null`)
> **QUIRA = plataforma de inteligencia pública · infraestructura de conocimiento verificable**
> (Plataforma · Método · Patrimonio Cognitivo) para gobiernos, ciudadanía, academia, cooperación.
> ⛔ **NO es "auditoría" ni "observatorio"** — función menor y producto (Javo 2026-08-05).
> Escala: SIAP-ICPI **mide** · QUADRUM **detecta** · **QUIRA EXPLICA la causalidad**.

**3 niveles** (ADR-023 — inmutable): **1 Motor** = Gold Master v5.5 (calcula ICPI/TGI/SAT/MMP · leer vía
`app/connectors/gold_master.py` · NUNCA recalcular fuera del Excel) · **2 SO** = QUIRA (ingesta +
trazabilidad MNT_UUID + evidencia) · **3 UI** = Dashboards + GeoTwin (solo visualizan).
**MATRIZ_CANONICA** del Excel = ADN compartido: sin ella, dos mundos.

## 🎯 LA TESIS — no olvidar
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente.**
El **Observatorio de Integridad Territorial** es UN PRODUCTO, no la identidad: lleva QUIRA a los 222 GAD. Montecristi = el MOLDE.
Fase 1 = 3 motores/productos: **Operaciones · Ciudadana · Institucional**. Fase 2: Cooperación ·
Impact · Economic. Diferenciador: Plan CNE + NLP discurso RDC. Ventana: **elecciones NOV-2026**.
Negocio = complementario, no licencias. **Detalle: `HOJA_DE_RUTA_MAESTRA.md §0` · ADR-024.**

## 📜 ONTOLÓGICA → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `HOJA_DE_RUTA_MAESTRA.md`
Define el OBJETO observado, **no a QUIRA** (CAPA 0 + 4 macroejes + 12 dominios): CONGRUENCIA
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO → BRECHAS. 3ª pieza: `GOVERNANCE_CHARTER.md`.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
🧭 **ADR-031** cajón=MCD·GM=MCM·**MCIP=5 motores** · **ADR-035/037** Ley→BRN→GM→QUIRA, IA propone/humano valida · **ADR-038** BRN v2: **Corpus→CNO→RO→SAT**.
✅ **PCD: d01·d02·d03·d09** · **d08 ENTRABLE** (**Asamblea AUTÓNOMA** · CNO-VIII(8) · **OBS-012..017**).
🩺 **Canon curado por DOM (R.8), ICPI intacto. Gate `check_health.py`: NO adivinar.**
🏛️ **GOBERNANZA v1.0:** `identity/`→`governance/`→`marco_teorico/`→Canon→`registry/`. ⚠️ Derivación **solo en lo catalogado**.
🖥️ **d08 EN WEB** (tarjeta 191→162→**15%**, NO el 48,33): **2 CAUSAS**: **66 inverificable-instrumento** · **96 sin-tema**. MRSPP v4 26·8·**0**·9 · **T0**.
🩹 Gate **`smoke_cajones.py`** (AppTest 8×2 roles · **HUELLA**: sin ella daba falsos OK).
🎚️ Gate **`check_epistemico.py`**: 4 de 10 checks léxicos; 6 de juicio = lectura. **d01·d08·landing = 0**.
🎨 **Landing v7 · identidad v1.1**: marca = **asset, NO se redibuja** · 1 acento coral · **plano afuera/volcánico adentro** · **acceso único: Observatorio** · fail-open cerrado → docstring `login_view.py`.
🔌 **CABLEADO** (`MATRIZ_CABLEADO_CANONICO.md`): **GM→SILOS→DOM→QUIRA**. **S1·S6·S9 sin DOM.**
🧨 **OBS-023 · brecha ICM↔ICPI NO citable:** bug escala `B36` + **DESCALCE PDOT** (1º comparable = **ICM 2025**, ~may-26). **`SAT-I`=S6 SIGAD**. ⛔ NO redefinir (R.1).
🚨 **OBS-022: SAT sin BRN, deuda 90%→60%.** PCD → **`cerrado con deuda declarada`** (R.8). Gate `check_sat_brn.py`. ⛔ `SAT-IX`(d08) ≠ `SAT-IX-001`(=SAT-V).
🏛️ **R-C..R-H → `PROTOCOLO_CURACION_DOMINIO.md` §3** (D **se mide, no se parcha** · **E LEY**: solo MCR · **H no comparar horizontes**).
🔬 **d01 §05** (CVI · OBS-020): POA **100% QUÉ · 1,1% DÓNDE · 3,5% QUIÉN · 1 de 1027 ambas**. **148 a 1** con financiador externo (hipótesis, n=12). `inverificable` ≠ `no atendido`.
⚖️ **3 CAPAS**: jurídica (**Guía LOTAIP=LEY**) · operativa (**d07**) · analítica (**no tramita**). 🧪 **H-ARQ-01** HIPÓTESIS ⛔R-E.
🧠 **DESCUBRIMIENTO NORMATIVO**: NO es motor nuevo — 4º de los **5 MCIP**. Vacío → `C10-{n}` → sella Javo. **Laboratorio, NO runtime**. ⛔R-E.
⏭️ **JAVO: (1)** 2ª validación v4 (¿retirar `complementaria`?) **(2)** promover `_CANDIDATO_v5.7`→`v5.7_TGI` **(3)** Haiku ~$60/18 meses.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (§LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 222 GAD).

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
| Retomar d07 | `CATALOGO_CANONICO_CD_D07.md` + `app/agents/d07/` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
