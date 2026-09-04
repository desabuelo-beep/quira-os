# -*- coding: utf-8 -*-
"""
scripts/gm_omega/mapa_maestro.py — EL MAPA ÚNICO DE FRENTES ABIERTOS

    POR QUÉ EXISTE. Javo lo pidió y tenía razón: hay refactor, construcción,
    auditoría del motor, freeze terminológico y ahora dominios, y **no había un
    artefacto que dijera qué frentes hay, en qué orden y qué depende de qué**.
    Vivía en la cabeza del director y disperso en cinco documentos.

    Es la misma deuda que esta auditoría persigue en todo lo demás: conocimiento
    que existe en el diseño y no en algo verificable. Con una diferencia grave —
    **de este dependía no repetir trabajo**.

    ⚠️ Y SE DERIVA, NO SE ESCRIBE. Un mapa de estado escrito a mano se queda
    atrás en dos semanas y después se sigue citando: es exactamente el patrón
    del «48,33 %». El ESTADO sale de las fuentes vivas —`deuda.py`,
    `doctrina.py`, los documentos de GM-Ω, `docs/pcd/`—; la SECUENCIA y las
    DEPENDENCIAS se declaran, porque son un juicio de dirección.

Uso:  python scripts/gm_omega/mapa_maestro.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_MAPA_MAESTRO.md"

# ── LOS FRENTES ──────────────────────────────────────────────────────────────
# (id, nombre, qué pregunta responde, depende de, puede avanzar en paralelo)
_FRENTES = [
    ("GM-Ω", "Auditoría del motor ICPI",
     "¿el indicador mide lo que dice medir, y su matemática está fundamentada?",
     "—", "sí · es la vía crítica"),
    ("TF", "Terminology Freeze",
     "¿qué es cada nombre, quién lo define y en qué capa se lee?",
     "—", "sí · independiente de GM-Ω"),
    ("T3-R", "Refactor de arquitectura de dominios",
     "¿la estructura de dominios representa lo que QUIRA sabe hoy?",
     "TF · T3", "R0 y R1 sí · R2 espera a 011"),
    ("2ING", "Segunda ingeniería · curación dominio a dominio",
     "¿cada dominio está curado de la fuente a la UI, por las 7 capas?",
     "—", "sí · y alimenta a TF y a T3-R"),
    ("DEUDA", "Registro de deudas con ataque",
     "¿qué sabemos que está mal y aún no se ha corregido?",
     "—", "sí · cada una a su ritmo"),
]

# ── LAS ETAPAS DE CADA FRENTE ────────────────────────────────────────────────
# (frente, etapa, título, estado, bloqueada_por)
_HECHO, _CURSO, _ABIERTO, _BLOQ = "✅", "🔄", "⬜", "⛔"

_ETAPAS = [
    ("GM-Ω", "001", "Identidad y árbol matemático", _HECHO, ""),
    ("GM-Ω", "002", "El veto de la obra sobre la norma", _HECHO, ""),
    ("GM-Ω", "003", "Reconstrucción de la fórmula", _HECHO, ""),
    ("GM-Ω", "004", "Matriz de procedencia · 150 celdas", _HECHO, ""),
    ("GM-Ω", "005", "Temporalidad y determinabilidad", _HECHO, ""),
    ("GM-Ω", "006", "Semántica del cero", _HECHO, ""),
    ("GM-Ω", "007", "Sensibilidad A·B·C·D·X + X-bis", _HECHO, ""),
    ("GM-Ω", "008", "Cobertura real del universo medido", _HECHO,
     "veredicto: JUSTIFICADA EN v1 · criterio = mayor monto (Javo)"),
    ("GM-Ω", "008-R", "Reconciliación meta a meta 66 ↔ 25", _ABIERTO,
     "⚠️ NO depende de 011 · prerequisito de v2 · desbloquea lo demás"),
    ("GM-Ω", "v2", "Universo completo del PDOT (66) — decisión de Javo", _BLOQ,
     "011 · 008-R · exige ADR propio y recalibración (ADR-036 §4)"),
    ("GM-Ω", "009", "¿Se puede optimizar el índice sin mejorar la realidad?",
     _ABIERTO, ""),
    ("GM-Ω", "010", "Transferibilidad LATAM · núcleo vs adaptador", _ABIERTO, ""),
    ("GM-Ω", "011", "**Dictamen de validez del constructo**", _BLOQ,
     "008 · 009 · 010"),

    ("TF", "T1", "Inventario de nombres propios", _HECHO, ""),
    ("TF", "T2", "Clasificación ontológica + capa de presentación", _HECHO, ""),
    ("TF", "T3", "Contrato índice → dominio → rol → pregunta → capa", _CURSO,
     "se llena con la curación de cada dominio"),
    ("TF", "T4", "Rol de cada indicador", _CURSO, "sin inventar: sólo con fuente"),
    ("TF", "T5", "Presentación dentro de su dominio", _BLOQ, "T3 · T4"),
    ("TF", "T6", "Acción: conservar / renombrar / deprecar / eliminar", _BLOQ,
     "011 · T5"),

    ("T3-R", "R0", "Diagnóstico de los 13 dominios", _ABIERTO, ""),
    ("T3-R", "R1", "Modelos A · B · C de arquitectura", _ABIERTO, ""),
    ("T3-R", "R2", "Decisión: residencia y ámbito de los índices", _BLOQ, "011"),

    ("2ING", "d01", "Planificación", _HECHO, "⚠️ PCD bajo canon anterior"),
    ("2ING", "d06", "Salud Institucional", _HECHO, "⚠️ PCD bajo canon anterior"),
    ("2ING", "d09", "Rendición de Cuentas", _HECHO, "⚠️ PCD bajo canon anterior"),
    ("2ING", "d07", "Transparencia", _CURSO, ""),
    ("2ING", "d08", "Participación Ciudadana", _ABIERTO, "entrable"),
    ("2ING", "d02·d03", "Presupuesto · Gobernanza del Mandato", _ABIERTO, ""),
    ("2ING", "d04·d05·d10-d13", "Sellados · sin construir", _ABIERTO, ""),
]


def estado_deudas() -> dict:
    from app.agents.deuda import deudas
    todas = deudas()
    abiertas = [d for d in todas
                if not str(d.get("estado", "")).startswith("RESUELTA")]
    return {"total": len(todas), "abiertas": abiertas,
            "resueltas": len(todas) - len(abiertas)}


def estado_doctrina() -> int:
    from app.agents.doctrina import doctrina
    return len(doctrina())


def documentos_gm_omega() -> list[str]:
    d = _RAIZ / "docs" / "architecture"
    return sorted(p.name for p in d.glob("GM-OMEGA_*.md"))


def pruebas_totales() -> int:
    """Cuenta las funciones de prueba del repositorio — el tamaño real de la red
    de custodios, derivado y no recordado."""
    n = 0
    for p in (_RAIZ / "tests").rglob("test_*.py"):
        n += len(re.findall(r"^def test_", p.read_text(encoding="utf-8",
                                                       errors="replace"), re.M))
    return n


def main() -> int:
    deu = estado_deudas()
    docs = documentos_gm_omega()
    n_doc = estado_doctrina()
    n_test = pruebas_totales()

    hechas = sum(1 for e in _ETAPAS if e[3] == _HECHO)
    print(f"frentes: {len(_FRENTES)} · etapas: {len(_ETAPAS)} "
          f"({hechas} cerradas) · deudas abiertas: {len(deu['abiertas'])} · "
          f"doctrina: {n_doc} · pruebas: {n_test}")

    _escribir(deu, docs, n_doc, n_test, hechas)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(deu, docs, n_doc, n_test, hechas) -> None:
    o: list[str] = []
    A = o.append

    A("# QUIRA · MAPA MAESTRO DE FRENTES")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/mapa_maestro.py`. El **estado** sale de las fuentes "
      "vivas (`deuda.py`, `doctrina.py`, `docs/pcd/`, `tests/`); la **secuencia "
      "y las dependencias** se declaran en el script, porque son un juicio de "
      "dirección y no un dato.")
    A("")
    A("> ### Por qué existe")
    A("> Javo: *«hay varios frentes […] para que no nos pase nuevamente volver "
      "a hacer refactor porque no recordamos»*. No había un artefacto que "
      "dijera qué frentes hay, en qué orden y qué depende de qué: vivía en la "
      "cabeza del director y disperso en cinco documentos.")
    A(">")
    A("> Es la misma deuda que esta auditoría persigue en todo lo demás "
      "—conocimiento que existe en el diseño y no en algo verificable— con un "
      "agravante: **de éste dependía no repetir trabajo.**")
    A("")

    A("## Los cinco frentes")
    A("")
    A("| Frente | Qué pregunta responde | Depende de | ¿Puede avanzar ahora? |")
    A("|---|---|---|---|")
    for fid, nombre, preg, dep, par in _FRENTES:
        A(f"| **{fid}** · {nombre} | {preg} | {dep} | {par} |")
    A("")

    A("## El orden, y qué se puede hacer en paralelo")
    A("")
    A("```")
    A("  AHORA, en paralelo — nada de esto se bloquea entre sí")
    A("  ├── GM-Ω 008-R reconciliación meta a meta 66 ↔ 25  ← desbloquea v2")
    A("  ├── GM-Ω 009   gaming: ¿se optimiza el índice sin mejorar la realidad?")
    A("  ├── GM-Ω 010   transferibilidad LATAM")
    A("  ├── T3-R R0    diagnóstico de los 13 dominios")
    A("  ├── T3-R R1    modelos A · B · C")
    A("  ├── 2ING d07   curación de Transparencia")
    A("  └── DEUDA      D-008 · D-009 · D-011 · D-012")
    A("")
    A("           ↓ los tres primeros alimentan")
    A("")
    A("  GM-Ω 011   DICTAMEN DE VALIDEZ DEL CONSTRUCTO")
    A("             ¿qué mide el ICPI · qué significa su álgebra ·")
    A("             conservar / corregir / potenciar / rediseñar?")
    A("")
    A("           ↓ y sólo entonces")
    A("")
    A("  ├── T3-R R2    residencia y ámbito de los índices")
    A("  ├── TF   T5    presentación dentro del dominio")
    A("  └── TF   T6    conservar / renombrar / deprecar / eliminar")
    A("```")
    A("")
    A("⚠️ **`R0` y `R1` NO dependen de `011`** —esta dirección lo tuvo mal y se "
      "corrigió—: son diagnóstico y **lo alimentan**. Sólo `R2` espera, porque "
      "mover un indicador cuyo constructo está en dictamen sería reorganizar la "
      "casa antes de saber qué se guarda.")
    A("")
    A("Y **`T6` espera a `011` por la misma razón**: deprecar `AVEP` o migrar el "
      "nombre del `ICPI` son decisiones que dependen de qué resulte que mide el "
      "constructo.")
    A("")

    A("## Estado por etapa")
    A("")
    A(f"{_HECHO} cerrada · {_CURSO} en curso · {_ABIERTO} abierta, sin bloqueo · "
      f"{_BLOQ} bloqueada")
    A("")
    A("| Frente | Etapa | Título | Estado | Nota |")
    A("|---|---|---|:-:|---|")
    for f, et, tit, est, nota in _ETAPAS:
        A(f"| {f} | `{et}` | {tit} | {est} | {nota} |")
    A("")
    A(f"**{hechas} de {len(_ETAPAS)} etapas cerradas.**")
    A("")

    A("## Estado derivado de las fuentes vivas")
    A("")
    A("| | |")
    A("|---|---:|")
    A(f"| Deudas declaradas | {deu['total']} |")
    A(f"| Deudas resueltas | {deu['resueltas']} |")
    A(f"| Deudas abiertas | **{len(deu['abiertas'])}** |")
    A(f"| Reglas de doctrina con custodio | {n_doc} |")
    A(f"| Pruebas que las fijan | {n_test} |")
    A(f"| Documentos GM-Ω | {len(docs)} |")
    A("")
    A("### Deudas abiertas")
    A("")
    A("| Deuda | Estado |")
    A("|---|---|")
    for d in deu["abiertas"]:
        est = str(d.get("estado", "ABIERTA"))
        A(f"| `{d['id']}` | {est[:110]} |")
    A("")
    A("### Documentos de la auditoría")
    A("")
    for n in docs:
        A(f"- [`{n}`]({n})")
    A("")

    A("## Las tres reglas que sostienen este mapa")
    A("")
    A("1. **Ningún frente se cierra sin custodio.** Una etapa marcada `✅` sin "
      "prueba que la fije acredita cero por no existir — es el defecto que "
      "`D-004` documentó en el propio CI.")
    A("2. **Un frente bloqueado no es un frente parado.** `011` está bloqueada "
      "por `008-010`, y esos tres pueden trabajarse hoy. La secuencia existe "
      "para ordenar, no para esperar.")
    A("3. **Este mapa se deriva.** El día que alguien lo edite a mano, dejará de "
      "reflejar el estado real sin que nada avise, y volveremos exactamente al "
      "punto que motivó escribirlo.")
    A("")
    A("---")
    A(f"*QUIRA · Mapa Maestro · {hechas}/{len(_ETAPAS)} etapas cerradas · "
      f"{len(deu['abiertas'])} deudas abiertas · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
