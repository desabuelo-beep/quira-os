---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5]
  type: OPERATIVA
---

# PROMPT DE ARRANQUE — PRÓXIMA SESIÓN (copiar/pegar en chat nuevo)

> Lean a propósito: **BOOT.md §AHORA es la fuente VIVA** (al día). Este prompt solo orienta.
> Última jornada (2026-06-16): d06 cableado y VIVO en la nube · auditoría de migración hecha. Frontera = Sprint D.2.

```
Retomamos QUIRA OS (Dylus Lab). Eres el Director Técnico. Lee SOLO `governance/BOOT.md` §AHORA — está al día.
NO leas docs enteros (Javo financia cada token). Navega con los dumps (`scripts/dev/gm_*`), la matriz
`docs/architecture/d06_MAPPING_MATRIX.md` y la auditoría `docs/architecture/AUDITORIA_MIGRACION_D1.5.md`.

DÓNDE ESTAMOS (resumen · detalle en BOOT §AHORA):
- Motor Gold Master v6.0 BLINDADO y VIVO (cirugía D.2A · ICPI 27.46% · B33 intacta · pasa governance 30 reglas).
- Snapshot local `data/gm_snapshot.json` a 27.46% (builder `scripts/_update_snapshot.py` · incluye bloque `vectores`).
- **d06 (Salud Institucional) COMPLETO y VIVO EN LA NUBE** (quiraholding.streamlit.app): 3 pestañas
  (`p_ejecutivo`·`p6_pulso`·`p7_brecha`) + L1 Centro de Mando (`p_command_center`) leen el snapshot local (27.46%) ·
  lenguaje de gobernanza (frontera Regla 2) · cero demo_data · firewall-limpio · botones con `key` único.
- Hilo conductor documentado (`MAPA_HILO_CONDUCTOR.md`). Seguridad: token GitHub limpio (ya no existe · GCM OAuth).

▶ FRONTERA = Sprint D.2 — REPLICAR el patrón d06 a los 11 cajones (ingeniería de cableado, NO teoría):
  Migración actual ~8% (solo d06 real · ver auditoría D.1.5). Faltan d01-d05, d07-d12 (~14 pantallas leen `demo_data`).
  🔴 PRIORIDAD: los 3 hardcodes del L1 que CONTRADICEN el motor → d05 Holding (68.7 vs ~17) · d08 Participación
     (27.98 vs 48.33) · d12 Género (12.83 vs 2.83). Eso es "el enemigo" (verdades simultáneas).
  PATRÓN PROBADO (d06): `load_all()`→`cargar_gm_snapshot()` · etiquetas a gobernanza · `key=` único en botones ·
     si falta el dato en el snapshot, extender `_update_snapshot.py` (como el bloque `vectores`).
  ⚠️ MATIZ DE JAVO: las pantallas viejas son CANTERA — cosechar sus PARTES y rearmar en la FORMA NUEVA de cada
     cajón (no cablear la pantalla vieja entera, como se hizo en d06 a modo interino). Mapa cajón→pantalla→fuente: en la auditoría D.1.5.

REGLAS DEL VUELO (grabadas):
- 🛡️ Disciplina: ningún debate metodológico nuevo salvo que una pantalla/cosecha REAL lo obligue.
- 2 CARRILES que NO se mezclan: A = cableado QUIRA (UI) · B = metodología Gold Master (freezer · FactorTemporal/Ti/Ci).
- Cablear ANTES de persistir Supabase (3B pendiente · `cargar_snapshot` aún trae 17.45% stale). NUNCA B33. Claves REALES (no inventar · lección del académico).
- 🧬 Inteligencia relacional (Neo4j·QTMP·SAT·congruencias·Gephi) = capacidad de QUIRA IA (C3), consumida por TODA la familia.
  Gephi = QUIRA LAB futuro (post-Neo4j operativo · NO ahora). Las 4 congruencias = juicios de C3 ("Pendiente análisis contextual" en UI).
- Frontera de lenguaje (Regla 2): público ve gobernanza, nunca ICPI/TGI/SAT/Gold Master/H## (skill `quira-language-guard`).
- Cada pixel con su celda; cada celda con su tesis.

Confirma que leíste BOOT §AHORA + la auditoría D.1.5, da 5 líneas del estado, y pregunta a Javo por dónde arrancamos. NO ejecutes nada aún.
```
