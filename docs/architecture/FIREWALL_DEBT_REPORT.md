# FIREWALL DEBT REPORT — Sprint D.2A

**2026-06-17 · barrido determinista AST · "no estimar, MEDIR"**
Generador: [`scripts/dev/firewall_audit.py`](../../scripts/dev/firewall_audit.py) · data cruda: `firewall_debt.json`

> ¿Cuántas pantallas activas filtran nomenclatura canónica/interna en **capa visible**?
> El segundo enemigo (después de `demo_data`): **metodología expuesta** (Regla 2 · Bloomberg).

## 🎯 KPI MEDIDO: 190 fugas VISIBLES en 25 archivos
- **ALTO (190)** = término embebido en texto/HTML renderizado (fuga real al usuario).
- **BAJO (63)** = el string ES la clave bare (`.get("IGP")`) → acceso a dato interno, no se renderiza.
- El escáner usa **AST**: excluye docstrings y comentarios (capa interna permitida); distingue strings visibles de claves. NO marca términos PÚBLICOS legítimos (SIGEF/eSIGEF/SERCOP/CPCCS/LOTAIP/COOTAD/PDOT/ODS/NBI/CNE/RDC).

## ✅ Validación: las pantallas convergidas están LIMPIAS
`p_ejecutivo.py` (d06) y `p16_confianza.py` (d08) salen **0 ALTO** (solo clave interna). **El patrón de convergencia deja el firewall impecable** — lo que purgamos, queda purgado.

## 📊 Matriz de deuda — por archivo (ranked) + exposición

| Pantalla | ALTO | Términos visibles | Exposición |
|---|---:|---|---|
| **p19_genero.py** (d12) | **22** | PSG · H73 · Gold Master · Neo4j · SAT · H10c | 🌐 PÚBLICO ← **prioridad** |
| p_cadena_institucional.py | 14 | Gold Master · H90 · IFE · IGP · IOC · ITAM · SAT-0 | 🌐 PÚBLICO |
| p16_gobernanza.py | 13 | ICPI · IGP · H20b · H10c · IFE · SAT | 🌐 PÚBLICO |
| env_ops.py | 12 | Gold Master · ICPI · TGI · Supabase · gm_snapshot · v5.5 | 🔧 INTERNO-OPS |
| p_concejo.py | 11 | Gold Master · H90 · IET · TGI · SAT-III | 🌐 PÚBLICO |
| p_sentinel_hub.py | 11 | Gold Master · ICPI · TGI · IET · SIAP-ICPI | 🔬 VERIFICAR |
| p14_eficiencia.py | 11 | ICPI · IGP · ISP · IED · SAT · SIAP-ICPI | 🌐 PÚBLICO |
| m2_alertas.py | 11 | ICPI · SAT · SAT-III | 🔬 VERIFICAR (¿técnico?) |
| p12_cadena.py | 10 | ICPI · IGP · IED · SAT-0 · SIAP-ICPI | 🌐 PÚBLICO |
| p13_simulador.py | 9 | Gold Master · ICPI · IED · IET · ISP · SAT-0 | 🌐 PÚBLICO |
| p_carga.py | 9 | Gold Master · Supabase · TGI · gm_snapshot | 🔧 INTERNO-OPS |
| p11_ods.py | 9 | H73 · H99 · IGP · ISP · IET · PSG | 🌐 PÚBLICO |
| p8_metas.py | 8 | ICPI · IFE · ITAM · PSG · SAT-0 · SIAP-ICPI | 🌐 PÚBLICO |
| p9_sat.py | 7 | IGP · IOC · ISP · SAT-0 | 🌐 PÚBLICO |
| p17_rdc.py | 7 | IFE · IOC · ISP · Neo4j · PSG · SAT-0 | 🌐 PÚBLICO |
| p3_congruencias.py | 6 | ICPI · IFE · H16 · H99 · SAT-0 · SIAP-ICPI | 🌐 PÚBLICO |
| p5_operacion.py | 4 | ICPI · H05 · SAT-0 · SIAP-ICPI | 🌐 PÚBLICO |
| p10_inversion.py | 4 | ICPI · IET · PSG · H99 | 🌐 PÚBLICO |
| p4_geotwin.py | 3 | ICPI · IET · PSG · H24 | 🌐 PÚBLICO |
| env_gov.py | 3 | IFE · SAT | 🔧 router (spots aislados) |
| p07_transparencia.py | 2 | Neo4j | 🌐 PÚBLICO |
| p18_cooperacion.py | 1 | Supabase | 🌐 PÚBLICO |
| p2_holding.py | 1 | Supabase (nota técnica · `show_tech`) | 🔬 gated |
| p10_territorio.py | 1 | Neo4j | 🌐 PÚBLICO |
| p_command_center.py | 1 | IFE | 🔧 V1 fallback (dormido) |

**Reparto:** ~150 ALTO en capa **pública** (deuda real) · ~22 en **interno-ops** (términos legítimos: consolas Dylus Lab de ingesta/carga) · ~23 a **verificar** (¿gated por `is_tecnico`?).

## 🟢 Tabla de sustitución canónica (para la purga)
| Interno | Público (gobernanza) |
|---|---|
| ICPI | Cumplimiento institucional |
| TGI | Gobernanza territorial |
| IGP | Participación ciudadana |
| PSG | Presupuesto con enfoque de género |
| ISP / IED / IOC / IET | Salud presupuestaria / Eficiencia directiva / Opacidad informativa / Equidad territorial |
| SAT · SAT-III | Alerta de reincidencia |
| H##·OUTPUT_API·Gold Master·SIAP-ICPI·v5.5 | Fuente pública (SIGEF/SERCOP/CPCCS) · "motor" |
| Supabase · Neo4j · gm_snapshot · demo_data | registros institucionales (o quitar) |

## ▶ Recomendación
1. **d12 (`p19_genero`) PRIMERO** — es el peor ofensor (22) **y** el último de los 3 hardcodes críticos (PSG 12.83→2.83). Un solo frente mata dos enemigos: hardcode + firewall.
2. Luego barrer las pantallas 🌐 públicas por orden de deuda (p_cadena, p16_gobernanza, p14, p12, p11…).
3. **Verificar** si `m2_alertas`/`p_sentinel_hub` están gated por `is_tecnico` (si sí → capa técnica, prioridad menor).
4. **Interno-ops** (`env_ops`, `p_carga`): términos canónicos son legítimos ahí (consola del operador Dylus Lab) — NO purgar, solo dejar constancia.
5. Re-correr el barrido tras cada purga → la deuda baja MEDIDA hacia 0.

---
*Firewall Debt Report · Sprint D.2A · Dylus Lab © 2026 · el espejo afuera, la metodología en el laboratorio.*
