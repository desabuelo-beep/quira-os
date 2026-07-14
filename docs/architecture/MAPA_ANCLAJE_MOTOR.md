# MAPA DE ANCLAJE DEL MOTOR — la ontología atada al Gold Master

**Sprint C · 2026-06-14 · "ancla mínima + consolidar" (decisión de mesa)**

> El puente que pidió Javo: cada **operativo** de cada **cajón** amarrado a la **hoja
> real del Gold Master** que lo produce, con su **estado** operativo. Convierte la
> ontología en el *reflejo operativo* del motor — y sirve igual a las 3 QUIRAs
> (un motor → una ontología anclada → tres lenguajes de la Tabla de Equivalencias).

## Alcance y honestidad (lo que ESTE mapa es y NO es)

- **ES:** inventario de superficie + completitud + conexión. Determinista, reproducible
  (`scripts/dev/gm_surface_map.py` → `GM_SURFACE_DUMP.md`), $0, sin leer celdas por LLM.
- **NO ES:** auditoría de corrección de fórmulas (¿el ICPI/TGI están bien calculados?).
  Esa es la **auditoría B**, que sigue **DIFERIDA** hasta su disparador.
- **LLENA = poblada** (hay valor cacheado en la hoja), **no** verificada-correcta.
- Fuentes consolidadas: `GM_SURFACE_DUMP.md` (superficie viva v5.5) + `QUIRA_DATA_REGISTRY_v1.md`
  (operativo→código+estado, jun-9) + `GOLD_MASTER_v6_SCHEMA.md` (grupos G1-G7) +
  contrato `_KEYS_OF_INTEREST` de `app/connectors/gold_master.py` (H73_OUTPUT_API).

**Leyenda de estado:** ✅ LIVE (poblado y legible vía conector) · ⏳ PENDIENTE (diseñado,
hueco de dato — típicamente columna 2026) · ❌ MISSING (fuente externa no conectada) ·
⚠️ HARDCODED (funcional con dato estático, falta snapshot).

## El mapa (12 cajones → operativo → hoja del motor → estado)

| Cajón (canónico) | Indicador madre (concepto) | Operativo REAL | Ancla en el motor | Estado |
|---|---|---|---|---|
| **d01** Planificación Estratégica | Cumplimiento de la planificación | Avance físico metas PDOT (4 ejes) | `H11b_MONITOR_POLITICAS` (41/47) · `H12c_ICPI_HISTÓRICO` · corpus METAS_PDOT (Supabase) | ✅ LIVE *(conexión TGI D1/D2 = auditoría B)* |
| | | Pertinencia estratégica del gasto (IPE) | `H16b_IPE` — Cobertura metas-POA **96%** ✅ · IPE-$ ejecutado ⏳ (camino A · objetivo+meta) | ⏳ PARCIAL |
| **d02** Presupuesto & Financiamiento | Captación y eficiencia del gasto | Sostenibilidad presupuestaria (ISP) | `H73_OUTPUT_API` → `ISP_SALUD_PRESUP` (hoja `H19_ICS_ISP`) | ✅ LIVE |
| | | Eficiencia de gestión (IED) | `H73_OUTPUT_API` (vector ICPI) | ✅ LIVE |
| | | Ejecución presupuestaria (devengado) | `H07_S5_FINANCIERO_eSIGEF` (37/88 · zona 2026 cruda) | ⏳ PENDIENTE 2026 (CHK-08) |
| | | Elegibilidad / fondos en riesgo | radar D02 · Supabase `fondos_*` *(no es Gold Master)* | ✅ LIVE |
| **d03** Gobernanza del Mandato | Congruencia promesa↔plan | Cumplimiento del plan de campaña (IFE-A) | `H73_OUTPUT_API` (48/66 promesas CNE→PDOT) | ✅ LIVE |
| | | Fidelidad de ejecución (IFE-E) | eSIGEF (POA→PAC→eSIGEF) | ⏳ PENDIENTE Q2-2026 |
| **d04** Alertas Institucionales | Riesgo operativo y legal activo | Cola del Sistema de Alerta Temprana | `H75_SAT_ENGINE` (14/14) · `H24_SAT-IV` (15/20) | ✅ LIVE |
| | | Matriz de riesgo (4 categorías) | demo_data → conectar a `H75` snapshot | ⚠️ HARDCODED |
| **d05** Holding e Integración Municipal | Desempeño del ecosistema | Promedio de entidades | `H12d_ICPI_POR_ENTIDAD` (19/24) | ✅ LIVE |
| **d06** Salud Institucional | Cumplimiento sostenible de funciones | Cumplimiento Institucional (ICPI) | `H73_OUTPUT_API` → `ICPI_GLOBAL` · `H12_MOTOR_ICPI` (hist. 23-25) | ✅ LIVE *(ICPI 2026 = T_i_2026, CHK-08 ⏳)* |
| **d07** Transparencia | Apertura verificable | Transparencia activa (LOTAIP 21/21) | QTMP (Neo4j) · `H73_OUTPUT_API` (IOC) | ✅ LIVE |
| **d08** Participación Ciudadana | Incidencia ciudadana | Gobernanza participativa (IGP) | `H73_OUTPUT_API` · CPCCS `H31_REPORTE_CPCCS` (58/65) · aportes `H10c` | ✅ LIVE |
| **d09** Rendición de Cuentas | Validación pública de la gestión | Estado del circuito de rendición (RDC) | `H73_OUTPUT_API` → `RDC_SCORE` · `H10c_RDC_APORTES` (132/134) | ✅ LIVE |
| **d10** Cobertura de Servicios e Infraestructura | Acceso territorial a bienes públicos | Cobertura agua/saneamiento/recolección (INEC) · NBI | QTMP AGUA_POTABLE (Neo4j) · data.loader · corpus PDOT | ✅ LIVE |
| | | Equidad Territorial | `H73_OUTPUT_API` (IET · 7 parroquias) | ✅ LIVE |
| | | Inversión per cápita | `H07b_Ti_INVERSIÓN_eSIGEF` (27/30) | ✅ LIVE |
| **d11** Desarrollo Económico Territorial | Capacidad productiva y de empleo | PEA / cadenas de valor | corpus PDOT económico (139 ind. · Supabase) | ✅ LIVE *(sin hoja GM dedicada — campo en construcción)* |
| **d12** Inclusión, Equidad y Género | Protección de grupos prioritarios | Presupuesto con enfoque de género (PSG) | `H73_OUTPUT_API` → `PSG_EJECUCION` | ✅ LIVE |
| **d13** Sostenibilidad y Resiliencia Ambiental | Integridad ecológica y resiliencia | ODS ambientales (ICODS) · riesgo biofísico · conservación | corpus biofísico (Supabase · 362 ind) · capa riesgo (KB_RIESGOS) · ICODS → `H73_OUTPUT_API` (sub-eje ambiental a precisar) | ✅ LIVE (corpus/riesgo) · ⚠️ ICODS-ambiental a confirmar |
| | | IGM-A/B/C/F · ODS 5.x | RRHH/DAF · CNE · PNUD/INEC (externos) | ❌ MISSING |

## Instrumentos transversales (Motores Analíticos QUIRA — NO son cajón)

Ratificado 2026-07-01 (detalle: `CIRUGIA_GOLD_MASTER_20260701_IPE_COBERTURA.md`). Estas hojas
NO pertenecen a un cajón: son lentes analíticos que **varias** investigaciones invocan —
por eso quedan simétricas con el plan sin duplicarse (Regla #6/#7).

| Hoja | Qué es | Consumidores | Nota |
|---|---|---|---|
| `H37_SENSIBILIDAD_ESTRATÉGICA` | Simulación de escenarios sobre el ICPI (Pi/Ri/Ti) | d01 · Simulador (`p13`) | ⚠️ Firewall: expone ICPI/Pi/Ri/Ti crudos — motor interno, NO se renderiza |
| `H38_ALCANCE_PREVENTIVO` | Matriz SAT-0…VI → acción preventiva por señal | d04 Alertas · cada cajón lee su fila (d01 = SAT-0) | Lenguaje 100% preventivo |

**Ruteo de las 5 hojas (2026-07-01):** `H11b`/`H16b` → d01 · `H19` → d02 · `H37`/`H38` transversales.

**Consumo cruzado (objeto canónico compartido · ADR-032 · 2026-07-13):** `H11b` (mapa estratégico PDOT↔PND) **nace en d01**; **consumido por d02 Presupuesto y Cooperación** como elegibilidad de financiamiento — se **referencia, no se mueve** (zanja la duda de Javo sobre moverlo a Presupuesto).

## Hallazgos del anclaje (lo que el mapa revela)

1. **El motor está ~97% poblado** (119/123 LLENAS). La auditoría de may-26 quedó stale:
   `H26` 18→43 · `H31` 33→58 · `H11b` poblada (41/47). El analista llenó el motor.
2. **Los únicos huecos que tocan cajones son de DATO 2026, no de hoja faltante:**
   `H07_S5 eSIGEF 2026` crudo → d02 ejecución + d03 IFE-E + d06 ICPI 2026 = ⏳ (CHK-08).
   Es UN hueco (la cédula eSIGEF 2026) que destraba 3 operativos a la vez.
3. **Las 4 incompletas NO son del núcleo:** `H65/H66/H67_CIUDADANO_IN_*` = inputs de
   QUIRA Ciudadana (vacíos pre-lanzamiento, esperado) · `H34b` narrativa.
4. **MISSING reales = externos de d12** (IGM RRHH/CNE, ODS5 PNUD) — ya en el Data Registry
   como gestión de cooperación, no son falla del motor.
5. **Para las 3 QUIRAs:** todo operativo ✅ LIVE se lee de la MISMA celda; las 3 QUIRAs
   solo cambian el idioma (Tabla de Equivalencias), nunca el número. El ancla lo garantiza.

## Conexión a la auditoría B (diferida)

Lo que este mapa **NO** resuelve y queda para la auditoría de fórmulas, cuando se dispare:
- `H98_TGI_FRAMEWORK`: los pesos documentados (20/20/25/25/10) no reproducen el TGI — pesos reales sin documentar.
- `H11b`: poblada, pero su **conexión** real al TGI D1/D2 (¿cadena viva o cacheada?) es de fórmula.
- ICPI 2026 vivo: depende de cargar la cédula eSIGEF 2026 (`H07_S5` zona cruda).

---

*Mapa de Anclaje del Motor · QUIRA OS · Dylus Lab © 2026 · ancla mínima (superficie/conexión) · corrección de fórmulas = diferida · regenerar superficie: `python scripts/dev/gm_surface_map.py`*
