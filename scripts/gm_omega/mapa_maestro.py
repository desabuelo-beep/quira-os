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
    ("QNEXT", "Rearquitectura integral · fondo y forma",
     "¿cómo evoluciona el ecosistema entero sin dañar lo que es válido?",
     "011-C4 para EJECUTAR", "Q0 ✅ · Q1 sí · Q3 espera al dictamen"),
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
    ("GM-Ω", "008-R", "Reconciliación meta a meta 66 ↔ 25", _CURSO,
     "PARCIAL · caso N:1 demostrado · correspondencia exhaustiva sin reconciliar"),
    ("GM-Ω", "v2", "Universo completo del PDOT (66) — decisión de Javo", _BLOQ,
     "011 · 008-R · exige ADR propio y recalibración (ADR-036 §4)"),
    ("GM-Ω", "009", "¿Se puede optimizar el índice sin mejorar la realidad?",
     _HECHO, "★ superficie de incentivo DINÁMICA: la ventaja material domina mientras hay margen y puede invertirse al cierre"),
    ("GM-Ω", "010", "Transferibilidad LATAM · arquitectura vs contingencia",
     _HECHO,
     "★ 24 componentes: 7 núcleo · 10 adaptador · 2 sedimentación · 5 "
     "contingentes · el núcleo es METODOLÓGICO, no métrico — y la "
     "multiplicatividad está en `D`, no en `A`"),
    ("GM-Ω", "007-B0", "Genealogía del constructo · unidad `i` · factores",
     _HECHO, "★ reescrito con toda la evidencia · CERRADO como reconstrucción, NO como validación"),
    ("GM-Ω", "011-A", "Unidad de análisis · ¿qué es `i`?", _CURSO,
     "★ genealogía RESUELTA: era PROMESA CNE → META PDOT «pues era mandato» (Javo) · falta DECLARARLA en el canon"),
    ("GM-Ω", "011-B", "Regla de correspondencia PDOT → ICPI (1:1·N:1·1:N·N:N)",
     _BLOQ, "011-A"),
    ("GM-Ω", "011-C1", "Genealogía algebraica · P·R·V·T → +E → +C · escalas",
     _ABIERTO, "★ 007-B0 la dejó reconstruida"),
    ("GM-Ω", "011-C2", "Genealogía semántica · qué significó cada factor",
     _HECHO, "★ C_i mide LEGALIDAD del proceso, no entrega · E_i y C_i "
             "comparten escala sin ser la misma · 4 divergencias latentes"),
    ("GM-Ω", "011-C3", "Justificación de cada transformación · qué·por qué·quién·cuándo",
     _HECHO, "★ el 27-abr C_i no ENTRÓ: cambió de mecanismo (imputabilidad → "
             "calidad de proceso) · E_i↔C_i justificada · 3 de 9 NO "
             "DETERMINABLE porque la razón nunca se escribió"),
    ("GM-Ω", "011-C4", "¿Es la multiplicatividad NECESARIA al constructo, o una "
     "arquitectura elegida y conservada?", _CURSO,
     "★ DESBLOQUEADA: C2·C3·C3R·010 cerrados. Faltan A2 y B (no bloquean el "
     "núcleo del dictamen) · 5 decisiones contingentes enumeradas · 2 "
     "paramétricas sin fundamento cuantitativo"),

    ("TF", "T1", "Inventario de nombres propios", _HECHO, ""),
    ("TF", "T2", "Clasificación ontológica + capa de presentación", _HECHO, ""),
    ("TF", "T3", "Contrato índice → dominio → rol → pregunta → capa", _CURSO,
     "se llena con la curación de cada dominio"),
    ("TF", "T4", "Rol de cada indicador", _CURSO, "sin inventar: sólo con fuente"),
    ("TF", "T5", "Presentación dentro de su dominio", _BLOQ, "T3 · T4"),
    ("TF", "T6", "Acción: conservar / renombrar / deprecar / eliminar", _BLOQ,
     "011 · T5"),

    ("QNEXT", "Q0", "Carta de rearquitectura v2 · el plan del refactor integral",
     _HECHO, "★ 4 bases medulares · 5 categorías · 10 ejes · 4 inventarios "
             "separados · DOC-029 regla maestra · NO ejecuta"),
    ("QNEXT", "BM-01", "Corpus normativo · vigencia, clase y separación "
                       "norma↔instrumento", _ABIERTO,
     "🔴 13.147 chunks SIN columna de vigencia · document_class vacía en 81 % "
     "· norma e instrumentos de gestión en la misma tabla"),
    ("QNEXT", "BM-05", "Memoria histórica de diseño · 898 archivos + 71 "
                       "versiones únicas del motor", _HECHO,
     "★ inventariada · la serie fechó el cambio de `C_i` · pendiente el resto "
     "del corpus (121 .md · 80 .txt de fórmulas)"),
    ("GM-Ω", "011-C3R", "Serie temporal del motor + Fase 3 documental · "
                        "sensibilidad de las conclusiones de C3", _HECHO,
     "★ CERRADO · 25→29-abr en UN acto · `E-CRIT-04` declara el PORQUÉ del "
     "constructo · parámetros sin fundamento cuantitativo = 3 decisiones "
     "ABIERTAS para C4"),
    ("GM-Ω", "011-P6", "Grafo de correspondencia de versiones · identidad de "
                       "artefactos", _ABIERTO,
     "3 esquemas sin reconciliar · NO bloquea a C4 · no cabe en 010: es "
     "identidad, no transferibilidad"),
    ("QNEXT", "Q1", "Matriz de clasificación · candidato → ratificado",
     _ABIERTO, "no espera al dictamen: clasificar no es cambiar · primer test "
               "= migración semántica de «auditoría»"),
    ("QNEXT", "Q2", "Dashboards y narrativa por dominio · visual→analítica→"
                    "explicación", _BLOQ, "R0 — no 011: depende de saber qué "
                                          "pregunta cada dominio"),
    ("QNEXT", "Q3", "Ejecución del refactor · fondo y forma", _BLOQ,
     "011-C4 · Q1 · R0/R1"),

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

    A("## Qué está corrigiendo este refactor · RESTAURAR vs. CREAR")
    A("")
    A("Javo: *«tenemos la tesis, y todo el constructo metodológico allí claro "
      "[…] eso es lo que estamos corrigiendo con este refactor»*. Es cierto en "
      "lo esencial, **y hay un matiz operativo**: no todo lo que el refactor "
      "toca estaba en la tesis.")
    A("")
    A("### 🔵 RESTAURAR — la tesis tenía la respuesta y la implementación la perdió")
    A("")
    A("| | La tesis decía | El motor hizo |")
    A("|---|---|---|")
    A("| `P_i` | antídoto anti-gaming, explicado | correcto — la auditoría lo "
      "dudó y la tesis la corrigió |")
    A("| `E_i` | regla con `COOTAD 54 · NCI 200-04` | valores que no la siguen |")
    A("| AVEP | «Baremo de **Interpretación**» | fórmula `IF` copiada en 11 hojas |")
    A("| universo | «muestra **estratégica**» | rotulado `Total_Metas_PDOT` |")
    A("| nombre | `SIAP` integridad ⊃ `ICPI` congruencia | se perdió la jerarquía |")
    A("| `V_i` | regla de tres niveles con núcleo | documentada, **no implementada** |")
    A("")
    A("### 🟠 CREAR — la tesis NO tiene la respuesta, y hay que decidirla")
    A("")
    A("| | Por qué no está en la tesis |")
    A("|---|---|")
    A("| Criterio de selección de las 25 | lo declaró Javo en 2026-09-03, no el documento |")
    A("| **Qué es `i`** (`011-A`) | la tesis habla de metas; no resuelve la unidad documental que contiene tres |")
    A("| Umbrales de AVEP | ni la tesis ni ninguna norma los fundamenta |")
    A("| Transferibilidad LATAM (`010`) | no era pregunta de una tesis sobre Montecristi |")
    A("| Capas de presentación (`DOC-014`) | no existía el producto cuando se escribió |")
    A("| Arquitectura de dominios (`T3-R`) | posterior a la tesis |")
    A("")
    A("⚠️ **La distinción es operativa, no filosófica.** Buscar en la tesis una "
      "respuesta que no está lleva a inventarla; decidir por cuenta propia algo "
      "que la tesis ya resolvió rompe la genealogía. Esta auditoría cometió los "
      "dos errores —dudó de `P_i`, que la tesis explicaba; y declaró "
      "`UNTRACEABLE` a `E_i`, cuya regla la tesis define—.")
    A("")
    A("> **Antes de decidir cualquier punto del refactor: ¿esto lo resuelve la "
      "tesis?** Si sí, se restaura y se cita. Si no, se decide **y se declara "
      "que es una decisión nueva**, no un hallazgo.")
    A("")

    A(f"## Los {len(_FRENTES)} frentes")
    A("")
    A("| Frente | Qué pregunta responde | Depende de | ¿Puede avanzar ahora? |")
    A("|---|---|---|---|")
    for fid, nombre, preg, dep, par in _FRENTES:
        A(f"| **{fid}** · {nombre} | {preg} | {dep} | {par} |")
    A("")

    A("## ★ Para qué sirve todo esto — el encuadre, fijado el 2026-09-05")
    A("")
    A("Javo:")
    A("")
    A("> *«Lo histórico no es la verdad absoluta o una camisa de fuerza que se "
      "deba continuar.»*")
    A("")
    A("**Tiene razón, y el canon ya lo decía.** `DOC-013`: QUIRA no conserva "
      "conceptos por herencia, sólo los que cumplen una función verificable. "
      "Lo que ocurrió es que `GM-Ω` reconstruyó tanta genealogía que empezó a "
      "producir un **sesgo conservador de hecho**, aunque de derecho el canon "
      "dijera lo contrario.")
    A("")
    A("### La corrección de encuadre")
    A("")
    A("```")
    A("  reconstruir la historia   →   NO obliga a repetirla")
    A("                            →   habilita a decidir SABIENDO qué se cambia")
    A("```")
    A("")
    A("Y de ahí sale la regla operativa (`DOC-027`):")
    A("")
    A("> ### Un `NO DETERMINABLE` genealógico es un GRADO DE LIBERTAD, no una laguna")
    A(">")
    A("> Donde no hay razón documentada, **no hay nada que respetar**.")
    A("")
    A("Aplicado a lo que `011-C2` y `C3` acaban de producir, el balance se "
      "invierte: no son hallazgos para conservar, son **permisos para "
      "cambiar**.")
    A("")
    A("| Hallazgo | Lo que habilita |")
    A("|---|---|")
    A("| Dos generaciones de `C_i` conviven y el instrumento no declara cuál "
      "rige | **hay que elegir una** — no elegir también es una decisión, y "
      "hoy está tomada por omisión |")
    A("| La razón de la sustitución, los pesos y el piso: `NO DETERMINABLE` | "
      "**tres decisiones libres**, sin contradecir a nadie |")
    A("| La residencia del ICPI en `d06` se apoya en «Cumplimiento "
      "Institucional», nombre que el canon **ya retiró** | **la residencia "
      "está abierta**, y hay instrumento: la prueba de exportabilidad |")
    A("")
    A("### ⚠️ La única camisa de fuerza real, y no es histórica")
    A("")
    A("Hay una parte del constructo que **no puede rediseñarse libremente**, y "
      "conviene no confundirla con herencia:")
    A("")
    A("| | Naturaleza | ¿Se puede cambiar? |")
    A("|---|---|---|")
    A("| `R_i` ↔ COOTAD 54-55 · Constitución 12, 14 | **anclaje normativo** | "
      "🔴 sólo si cambia la norma |")
    A("| `V_i` ↔ LOTAIP 7 · LOSNCP 22 · NCI 410-11 | **anclaje normativo** | "
      "🔴 sólo si cambia la norma |")
    A("| `T_i` ↔ COPFP 115-117 · Acuerdo 067 MEF | **anclaje normativo** | 🔴 "
      "sólo si cambia la norma |")
    A("| `P_i` ↔ COPFP 54 | **anclaje normativo** | 🔴 ídem |")
    A("| pesos de deducción · piso `0,50` · qué constructo de `C_i` rige | "
      "**decisión de diseño** | ✅ **libre** |")
    A("| residencia de cada índice en su dominio | **decisión de diseño** | ✅ "
      "**libre** |")
    A("| nombres de presentación | **decisión de diseño** | ✅ libre, con "
      "basónimo (`DOC-015`) |")
    A("")
    A("> **Herencia histórica ≠ anclaje normativo.** Lo primero se revisa; lo "
      "segundo se acata. Confundirlos en cualquiera de las dos direcciones es "
      "el error: congelar por costumbre lo que se puede mejorar, o rediseñar "
      "por gusto lo que la ley fija.")
    A("")
    A("### Qué NO cambia este encuadre")
    A("")
    A("- **El Gold Master sigue congelado** hasta `011-C4`. Ampliar el alcance "
      "de lo que se puede decidir **no adelanta el momento de intervenir**.")
    A("- **La genealogía no se descarta**: es lo que permite distinguir "
      "herencia de anclaje. Sin `C2`/`C3` no sabríamos cuál de las dos "
      "generaciones de `C_i` estamos eligiendo.")
    A("- **`DOC-011` sigue vigente**: un vacío se clasifica por su naturaleza. "
      "Que un `NO DETERMINABLE` habilite a decidir no autoriza a **inventar** "
      "la razón que faltaba y presentarla como hallazgo.")
    A("")

    A("## El orden, y qué se puede hacer en paralelo")
    A("")
    A("```")
    A("  LA RUTA AL DICTAMEN — acordada 2026-09-05, saneamiento ontológico primero")
    A("")
    A("  011-C2  ✅ semántica de los factores      qué mide cada letra")
    A("     ↓")
    A("  011-C3  ✅ justificación                  por qué cambió · quién · cuándo")
    A("     ↓")
    A("  010        transferibilidad LATAM        qué parte del constructo es local")
    A("     ↓")
    A("  011-C4     DICTAMEN                      ¿es NECESARIA la multiplicatividad?")
    A("")
    A("  EN PARALELO — nada de esto se bloquea entre sí")
    A("  ├── GM-Ω 008-R resolver las 40 ambiguas · 66↔25  ← desbloquea v2")
    A("  ├── GM-Ω 011-A2 declarar la unidad `i` en el canon")
    A("  ├── QNEXT BM-01 corpus normativo: vigencia · clase · norma↔instrumento")
    A("  ├── QNEXT Q1   matriz de clasificación · candidato → ratificado")
    A("  ├── T3-R R0    diagnóstico de los 13 dominios  ← desbloquea Q2")
    A("  ├── T3-R R1    modelos A · B · C de arquitectura de dominios")
    A("  ├── 2ING d07   curación de Transparencia")
    A("  └── DEUDA      D-008 · D-009 · D-011 · D-012 · D-013 · D-014")
    A("")
    A("           ↓ y sólo tras el dictamen")
    A("")
    A("  ├── T3-R R2    residencia y ámbito de los índices")
    A("  ├── TF   T5    presentación dentro del dominio")
    A("  ├── TF   T6    conservar / renombrar / deprecar / eliminar")
    A("  └── QNEXT Q3   ejecución del refactor integral · fondo y forma")
    A("```")
    A("")
    A("⚠️ **El refactor integral (`QNEXT`) no es un frente que se abra después "
      "de `GM-Ω`: es el destino que le da sentido.** Su plan —la carta `Q0`— "
      "ya está, y `Q1` puede correr hoy porque **clasificar no es cambiar**. "
      "Lo que espera al dictamen es la EJECUCIÓN. Detalle: "
      "`QUIRA-NEXT_CARTA_REARQUITECTURA.md`.")
    A("")
    A("⚠️ **Por qué `010` va DESPUÉS de `C3` y no antes.** Esta dirección "
      "proponía adelantarla —la transferibilidad también alimenta al "
      "dictamen—. El criterio que prevaleció es el del colega y es mejor: "
      "**mientras no se sepa qué significan `E_i` y `C_i`, todo análisis se "
      "hace sobre variables cuya ontología seguimos reconstruyendo**. `011-C2` "
      "lo demostró en el acto: la semántica que se daba por buena era falsa.")
    A("")
    A("⚠️ **`011-A2` y `011-B` siguen abiertas y la ruta acordada las "
      "pospone.** No es un olvido: `A` tiene su genealogía resuelta y sólo "
      "falta declararla en el canon, y `B` —la correspondencia documental ↔ "
      "operacional— depende de `008-R`. Ninguna bloquea a `C3`. Pero **`C4` "
      "sigue necesitándolas**, así que no desaparecen del camino.")
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
