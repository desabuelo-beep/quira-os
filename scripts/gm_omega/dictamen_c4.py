# -*- coding: utf-8 -*-
"""
scripts/gm_omega/dictamen_c4.py — GM-Ω-ICPI-011-C4 · EL DICTAMEN

    ¿Merecen permanecer las decisiones de diseño del constructo?

    La cadena entera desemboca aquí, y cada etapa hizo una pregunta distinta:

        C3    ¿de dónde vino la decisión?
        010   ¿pertenece al núcleo o al contexto?
        C4    ¿merece permanecer?

    ⚠️ LA REGLA QUE ORDENA EL DICTAMEN, y que bloquea los dos errores
    simétricos:

        La historia explica. La transferibilidad clasifica.
        La metodología justifica. La evidencia decide.

        «es antiguo, luego se conserva»    → prohibido (DOC-013)
        «es contingente, luego se elimina» → prohibido (DOC-027)

    ⚠️ Y LA SEGUNDA REGLA, que gobierna `C4-4`:

        La ausencia de evidencia puede LIMITAR lo que el sistema puede
        afirmar; no demuestra por sí misma la ausencia del fenómeno.

    QUÉ NO HACE. No modifica el Gold Master. No recalibra. No renombra. Todo
    escenario es CONTRAFACTUAL y NO AUTORIZADO PARA PUBLICACIÓN (`DOC-010`):
    el único ICPI publicable sigue siendo **27,4582 %**.

Uso:  python scripts/gm_omega/dictamen_c4.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_DICTAMEN_011C4.md"
_BASELINE = 0.27458226534062735

# Las siete secciones del dictamen. El orden importa: no se puede juzgar el
# álgebra antes de saber qué fenómeno se mide, ni la escala antes de saber qué
# clasifica.
_SECCIONES = [
    ("C4-1", "Fenómeno", "¿qué pretende medir realmente el ICPI?"),
    ("C4-2", "Unidad", "¿qué representa cada `i`, y cómo se relacionan unidad "
                       "documental, operacional y estadística?"),
    ("C4-3", "Arquitectura algebraica", "¿la multiplicación representa la "
                                        "relación entre dimensiones, o "
                                        "introduce una restricción no "
                                        "demostrada?"),
    ("C4-4", "Evidencia", "¿`V_i` mide verificabilidad, ausencia de "
                          "evidencia, calidad documental — o algo más?"),
    ("C4-5", "Parametrización", "¿hay fundamento suficiente para "
                                "`0,15/0,10/0,05` y `0,50`?"),
    ("C4-6", "Interpretación", "¿qué afirmaciones permite el resultado, y "
                               "cuáles no?"),
    ("C4-7", "AVEP", "¿el baremo clasifica el fenómeno medido, o traduce el "
                     "resultado para comunicación institucional?"),
]


def medir() -> dict:
    """La evidencia del dictamen. `C4` no opina: mide qué hace hoy el motor.

    ⚠️ Todo lo que sale de aquí es CONTRAFACTUAL salvo el baseline."""
    from scripts.gm_omega.sensibilidad_icpi import leer_motor
    d = leer_motor()
    if not d:
        return {}
    metas = d["metas"]

    def icpi(ms: list[dict]) -> float:
        sj = sum(m["P"] * m["R"] * m["V"] * m["E"] * m["T"] * m["C"]
                 for m in ms)
        sk = sum(m["P"] * m["R"] for m in ms)
        return sj / sk if sk else 0.0

    base = icpi(metas)

    # ── ¿Cuántas metas anula cada factor, y cuánto peso arrastran? ─────────
    anuladas = {}
    for f in ("V", "E", "T", "C"):
        ceros = [m for m in metas if float(m[f]) == 0.0]
        peso = sum(m["P"] * m["R"] for m in ceros)
        anuladas[f] = {"n": len(ceros), "peso": peso,
                       "ids": [m["id"] for m in ceros]}
    denom = sum(m["P"] * m["R"] for m in metas)

    # ── `C4-4` · el contrafactual que separa las tres proposiciones ───────
    #
    # Si `V=0` significara «no acreditado» en vez de «no ocurrió», la meta no
    # se anularía: quedaría FUERA del universo medido —numerador y denominador
    # a la vez—. Es la diferencia entre penalizar y no poder afirmar.
    con_v = [m for m in metas if float(m["V"]) > 0.0]
    icpi_excl = icpi(con_v) if con_v else 0.0

    # Y el otro extremo: tratar `V=0` como si la meta cumpliera plenamente.
    # No es defendible; se mide para acotar el rango del efecto.
    sup = [dict(m) for m in metas]
    for m in sup:
        if float(m["V"]) == 0.0:
            m["V"] = 1.0
    icpi_sup = icpi(sup)

    # ── `C4-3` · ¿cuánto del resultado viene de anulación y cuánto de
    # degradación gradual? Es la pregunta empírica sobre la multiplicatividad.
    sin_ceros = [m for m in metas
                 if all(float(m[f]) > 0.0 for f in ("V", "E", "T", "C"))]
    return {"metas": metas, "base": base, "denom": denom,
            "anuladas": anuladas, "icpi_excl": icpi_excl,
            "icpi_sup": icpi_sup, "n_sin_ceros": len(sin_ceros),
            "n": len(metas)}


def main() -> int:
    m = medir()
    if not m:
        print("[no determinable] Gold Master no resuelto.")
        return 2
    if abs(m["base"] - _BASELINE) > 1e-9:
        print(f"[hallazgo] el laboratorio no reproduce el baseline: "
              f"{m['base'] * 100:.6f} %")
        return 1

    print(f"baseline {m['base'] * 100:.4f} % · metas {m['n']} · "
          f"sin ningún factor en cero: {m['n_sin_ceros']}")
    for f, d in m["anuladas"].items():
        if d["n"]:
            print(f"  {f}=0 en {d['n']} metas · {d['peso'] / m['denom'] * 100:.1f} % "
                  f"del peso")
    print(f"contrafactual `V=0` excluida: {m['icpi_excl'] * 100:.4f} % · "
          f"tratada como 1: {m['icpi_sup'] * 100:.4f} %")

    _escribir(m)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(m) -> None:
    o: list[str] = []
    A = o.append
    pct = lambda x: f"{x * 100:.4f} %"

    A("# GM-Ω · ICPI — DICTAMEN  `011-C4`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/dictamen_c4.py`.")
    A("")
    A("> ### Las tres etiquetas")
    A("> Toda cifra distinta del baseline es **MATEMÁTICAMENTE REPRODUCIBLE** "
      "· **METODOLÓGICAMENTE CONTRAFACTUAL** · **NO AUTORIZADA PARA "
      "PUBLICACIÓN** (`DOC-010`). El único ICPI publicable sigue siendo "
      "**27,4582 %**.")
    A("")
    A("⚠️ **`C4` no modifica nada.** No recalibra, no renombra, no mueve "
      "dominios. Emite un juicio metodológico sobre decisiones de diseño "
      "enumeradas.")
    A("")

    # ── Las dos reglas ────────────────────────────────────────────────────
    A("## Las dos reglas que ordenan el dictamen")
    A("")
    A("> ### La historia explica. La transferibilidad clasifica. La "
      "metodología justifica. La evidencia decide.")
    A("")
    A("| Error | Estado |")
    A("|---|---|")
    A("| «es antiguo, por tanto debe conservarse» | 🔴 prohibido · `DOC-013` |")
    A("| «es contingente, por tanto debe eliminarse» | 🔴 prohibido · "
      "`DOC-027` |")
    A("")
    A("Y la segunda, que gobierna `C4-4`:")
    A("")
    A("> ### La ausencia de evidencia puede LIMITAR lo que el sistema puede "
      "afirmar; no demuestra por sí misma la ausencia del fenómeno.")
    A("")
    A("⚠️ Y lo que `C4` **no** es: un juicio sobre si QUIRA está «bien» o "
      "«mal». Las cinco decisiones `D` de `010` llegan aquí como **decisiones "
      "sometidas a prueba, no como cargos contra el diseño**. `D` significa "
      "«no puede recibir presunción de necesidad» — no «incorrecto».")
    A("")

    A("## La estructura del dictamen")
    A("")
    A("| # | Sección | Pregunta |")
    A("|---|---|---|")
    for sid, nombre, pregunta in _SECCIONES:
        A(f"| `{sid}` | **{nombre}** | {pregunta} |")
    A("")
    A("El orden no es arbitrario: **no se puede juzgar el álgebra antes de "
      "saber qué fenómeno se mide, ni la escala antes de saber qué "
      "clasifica**.")
    A("")

    # ── C4-1 ──────────────────────────────────────────────────────────────
    A("## `C4-1` · Fenómeno")
    A("")
    A("> ¿Qué pretende medir realmente el ICPI?")
    A("")
    A("Lo que las etapas anteriores establecieron:")
    A("")
    A("| Fuente | Qué dice |")
    A("|---|---|")
    A("| `GM-Ω-001` | **Índice de Congruencia Programática e "
      "Intersistémica** |")
    A("| Constitución §CAPA 0.5 | «Cumplimiento Institucional (ICPI)» — "
      "⚠️ nombre que el propio canon retiró |")
    A("| `data/gm_snapshot.json` | «Índice Compuesto de Progreso "
      "Institucional», «mide velocidad de ejecución» — 🔴 `D-011` |")
    A("")
    A("> ### Tres nombres distintos para el mismo número, y dos de ellos "
      "afirman cosas que el motor no hace")
    A("")
    A("El ICPI **no mide cumplimiento** ni **velocidad**: mide si la cadena "
      "`programa → norma → verificación → ejecución → tiempo → trazabilidad` "
      "**se sostiene entera**. Es una propiedad de la cadena, no un grado de "
      "avance.")
    A("")
    A("| Dictamen | |")
    A("|---|---|")
    A("| El fenómeno está **definido** en el constructo | ✅ **DEMOSTRADO** "
      "(`001`) |")
    A("| La **capa de publicación** lo describe mal | 🔴 **DEMOSTRADO** · "
      "`D-011`, abierta |")
    A("| El nombre `ICPI` corresponde al fenómeno | 🟡 **parcial** · "
      "«congruencia» sí; el acrónimo circula con tres expansiones |")
    A("")

    # ── C4-2 ──────────────────────────────────────────────────────────────
    A("## `C4-2` · Unidad")
    A("")
    A("> ¿Qué representa cada `i`?")
    A("")
    A("| Etapa | Resultado |")
    A("|---|---|")
    A("| `007-B0` · `011-A` | la unidad **cambió**: `i` = promesa del Plan "
      "CNE → `i` = meta del PDOT |")
    A("| `DOC-023` | el cambio **no es deriva**: hay razón declarada, "
      "definición operacional y genealogía |")
    A("| `008` | el universo medido son **25 de 66** metas |")
    A("| `008-R` | la correspondencia documental↔operacional **no está "
      "reconciliada** |")
    A("| `011-A2` | la unidad vigente **no está declarada en el canon** |")
    A("")
    A("> ### El dictamen no puede cerrar `C4-2`, y eso es un hallazgo")
    A(">")
    A("> Mientras `011-A2` no declare la unidad en el canon y `011-B` no "
      "establezca la regla de correspondencia, **el ICPI se calcula sobre una "
      "unidad que el sistema no define formalmente**. El motor funciona; la "
      "definición vive en la práctica y no en el canon.")
    A("")
    A("| Dictamen | |")
    A("|---|---|")
    A("| La unidad operacional está **implementada y es consistente** | ✅ "
      "**DEMOSTRADO** · 25 identificadores estables |")
    A("| La unidad está **declarada en el canon** | 🔴 **no** · `011-A2` |")
    A("| La correspondencia con las 66 documentales | ⬜ **NO DETERMINABLE** "
      "· `011-B` |")
    A("")
    A("⚠️ **Esto no invalida el índice**: lo acota. El ICPI es válido "
      "**sobre su universo operacional declarado**, y `ADR-036` lo congela "
      "para `v1`. Lo que no puede hacerse es presentarlo como si midiera el "
      "PDOT completo.")
    A("")

    _secciones_medidas(m, o)


def _secciones_medidas(m, o) -> None:
    """Segunda mitad: las secciones que dependen de la medición. Recibe la
    lista y la completa; **el archivo se escribe una sola vez, al final**."""
    A = o.append
    pct = lambda x: f"{x * 100:.4f} %"
    an = m["anuladas"]
    denom = m["denom"]

    # ── C4-3 ──────────────────────────────────────────────────────────────
    A("## ★ `C4-3` · Arquitectura algebraica")
    A("")
    A("> ¿La multiplicación **representa** la relación entre dimensiones, o "
      "**introduce una restricción no demostrada**?")
    A("")
    A("Lo primero es medir qué hace hoy:")
    A("")
    A("| | |")
    A("|---|---:|")
    A(f"| metas del universo | {m['n']} |")
    A(f"| metas **sin ningún factor en cero** | {m['n_sin_ceros']} |")
    A(f"| metas **anuladas** por al menos un factor | "
      f"{m['n'] - m['n_sin_ceros']} |")
    A("")
    A("| Factor | Metas en cero | Peso `P·R` que arrastran |")
    A("|---|---:|---:|")
    for f in ("V", "E", "T", "C"):
        d = an[f]
        A(f"| `{f}_i` | {d['n']} | {d['peso'] / denom * 100:.2f} % |")
    A("")
    if an["V"]["n"] and not any(an[f]["n"] for f in ("E", "T", "C")):
        A("> ### La anulación multiplicativa opera hoy por **un solo "
          "factor**: `V_i`")
        A(">")
        A(f"> Ningún `E_i`, `T_i` ni `C_i` vale cero. Las "
          f"**{an['V']['n']} metas anuladas** lo están **exclusivamente por "
          f"falta de evidencia documental**, y arrastran el "
          f"**{an['V']['peso'] / denom * 100:.2f} %** del peso del "
          f"denominador.")
        A("")
        A("Eso reformula `D1`: la pregunta sobre la multiplicatividad **no es "
          "abstracta**. En el estado actual, *toda* la anulación proviene de "
          "`V_i`, así que `D1` y `D2` **son la misma pregunta en la "
          "práctica** — aunque sigan siendo distintas en teoría.")
        A("")
    A("| Dictamen | |")
    A("|---|---|")
    A("| La multiplicatividad **produce anulación total** ante un solo "
      "factor en cero | ✅ **DEMOSTRADO** · es su definición |")
    A(f"| Hoy esa anulación afecta a **{an['V']['n']} de {m['n']}** metas | "
      f"✅ **DEMOSTRADO** |")
    A("| Existe razón **teórica, normativa o empírica** que la funde | ⬜ "
      "**NO DETERMINABLE** · `C3-R` cerró: los parámetros están documentados, "
      "su fundamento no |")
    A("| La multiplicatividad es **necesaria** al constructo | 🔴 **NO "
      "DEMOSTRADO** |")
    A("| La multiplicatividad es **incorrecta** | 🔴 **NO DEMOSTRADO** |")
    A("")
    A("> ### Veredicto de `D1` · **DECISIÓN DE DISEÑO NO FUNDAMENTADA, "
      "CONSERVABLE BAJO DECLARACIÓN EXPLÍCITA**")
    A(">")
    A("> No se demuestra necesaria ni incorrecta. Puede conservarse **si el "
      "sistema declara que es una elección metodológica** y no una propiedad "
      "derivada del fenómeno. Lo que no puede hacerse es seguir "
      "presentándola como si estuviera fundada.")
    A("")
    A("Y hay un argumento **a favor** que sí es defendible, y conviene "
      "decirlo: una cadena de congruencia en la que **cualquier eslabón roto "
      "invalida el conjunto** es una lectura coherente del fenómeno. `007-D` "
      "midió que es la decisión más consecuente del motor (**51,26 pp**). Que "
      "sea coherente no la vuelve necesaria — hay agregaciones alternativas "
      "que también lo serían.")
    A("")

    # ── C4-4 ──────────────────────────────────────────────────────────────
    A("## ★★ `C4-4` · Evidencia — la sección decisiva")
    A("")
    A("> ¿`V_i` mide verificabilidad, ausencia de evidencia, calidad "
      "documental — o algo más?")
    A("")
    A("### Las tres proposiciones que no pueden confundirse")
    A("")
    A("| # | Proposición | Naturaleza |")
    A("|---|---|---|")
    A("| 1 | «el fenómeno **no ocurrió**» | afirmación sobre el **mundo** |")
    A("| 2 | «**no hay evidencia suficiente** para acreditarlo» | afirmación "
      "sobre el **estado del conocimiento** |")
    A("| 3 | «la unidad **no puede contribuir** al índice mientras carezca de "
      "evidencia» | **regla metodológica** |")
    A("")
    A("> ### La proposición 3 puede ser perfectamente defendible. Lo que NO "
      "puede es presentarse como **consecuencia lógica** de la 2.")
    A(">")
    A("> Y ése es exactamente el punto que `C4` debe resolver.")
    A("")
    A("### Qué hace el motor hoy")
    A("")
    A(f"`V_i = 0` en **{an['V']['n']} de {m['n']} metas**, y el producto las "
      f"anula: `J_i = 0`. Contribuyen `0` al numerador **y siguen pesando en "
      f"el denominador** — el {an['V']['peso'] / denom * 100:.2f} %.")
    A("")
    A("El contrafactual que separa la proposición 2 de la 3:")
    A("")
    A("| Tratamiento de `V=0` | ICPI | Δ |")
    A("|---|---:|---:|")
    A(f"| **vigente** · anula la meta, que sigue en el denominador | "
      f"**{pct(m['base'])}** | — |")
    A(f"| «no acreditado» · la meta **sale del universo medido** | "
      f"{pct(m['icpi_excl'])} | "
      f"{(m['icpi_excl'] - m['base']) * 100:+.2f} pp |")
    A(f"| «se presume cumplida» · `V=1` | {pct(m['icpi_sup'])} | "
      f"{(m['icpi_sup'] - m['base']) * 100:+.2f} pp |")
    A("")
    A("⚠️ **La tercera fila no es una alternativa defendible** —presumir "
      "cumplimiento sin evidencia contradice el principio rector—; se mide "
      "sólo para **acotar el rango** del efecto.")
    A("")
    A("> ### El hallazgo")
    A(">")
    A(f"> Tratar `V=0` como «no acreditado» en vez de «no cumplido» mueve el "
      f"índice **{(m['icpi_excl'] - m['base']) * 100:+.2f} pp**. No es un "
      f"matiz interpretativo: **es una decisión con efecto material medible** "
      f"sobre el resultado publicado.")
    A("")
    A("### El choque con el canon, dicho sin rodeos")
    A("")
    A("| Principio rector | *«La ausencia de evidencia es un RESULTADO de "
      "auditoría, nunca autorización para inferir hechos.»* |")
    A("|---|---|")
    A("")
    A("Si `V=0` anula la meta, el índice **resta** por no poder acreditar. "
      "Caben dos lecturas, y el sistema no declara cuál sostiene:")
    A("")
    A("| Lectura | Qué implicaría |")
    A("|---|---|")
    A("| **A** · el ICPI mide *congruencia acreditada* | anular es correcto: "
      "lo no acreditado **no cuenta como congruente**, y eso es un resultado, "
      "no una inferencia |")
    A("| **B** · el ICPI mide *congruencia real* | anular es una "
      "**inferencia**: se trata la falta de evidencia como falta de "
      "cumplimiento |")
    A("")
    A("> ### Veredicto de `D2` · **LA REGLA ES DEFENDIBLE BAJO LA LECTURA "
      "`A`, Y HOY EL SISTEMA NO DECLARA CUÁL SOSTIENE**")
    A(">")
    A("> Bajo `A` no hay contradicción con el principio rector: el índice "
      "mide lo acreditable y lo declara. Bajo `B` sí la hay. **La diferencia "
      "no está en la fórmula: está en lo que el sistema afirma que el número "
      "significa** — y eso es `C4-6`.")
    A("")
    A("⚠️ Y el índice mide entonces **dos cosas a la vez**: la gestión y la "
      "capacidad de documentarla. Puede ser intencional y legítimo en un "
      "índice de *congruencia intersistémica* —donde la trazabilidad **es** "
      "parte del fenómeno—, pero **debe declararse como elección "
      "metodológica**, no asumirse.")
    A("")
    A("### La formulación endurecida de `V_i = 0`")
    A("")
    A("> `V_i = 0` **no significa que el fenómeno no ocurrió**. Significa "
      "que, bajo la arquitectura actual, **la unidad no puede aportar "
      "congruencia acreditada al índice**.")
    A("")
    A("Y el salto `27,4582 % → 31,4883 %` **no vale porque `31,4883` sea "
      "mejor** —no lo es ni pretende serlo—. Vale porque demuestra que **una "
      "decisión semántica sobre el estado de la evidencia tiene efecto "
      "material sobre el resultado**. Eso convierte a `D2` en una cuestión de "
      "**diseño epistemológico**, no en un detalle de fórmula.")
    A("")
    A("### La pregunta que `D2` deja preparada — y que `C4` NO responde")
    A("")
    A("Si la trazabilidad forma parte del fenómeno observado, entonces `V_i` "
      "**no es un defecto accidental del índice**: puede ser una dimensión "
      "sustantiva. Pero entonces:")
    A("")
    A("> ¿Debe `V_i` estar **embebida multiplicativamente** dentro de un "
      "único ICPI, o debe existir **además** como una medida explícita e "
      "independiente de **acreditabilidad**?")
    A("")
    A("⚠️ **Esa pregunta pertenece a la arquitectura futura y no se responde "
      "retrospectivamente aquí.** Resolverla dentro de `C4` sería rediseñar "
      "desde un peritaje, que es precisamente lo que la `Regla Maestra` "
      "(`DOC-029`) prohíbe.")
    A("")

    # ── C4-5 ──────────────────────────────────────────────────────────────
    A("## `C4-5` · Parametrización")
    A("")
    A("> ¿Hay fundamento suficiente para `0,15 / 0,10 / 0,05` y `0,50`?")
    A("")
    A("`C3-R` ya cerró la genealogía: **no hay que rehacerla**. Los "
      "parámetros están documentados; su fundamento cuantitativo no está "
      "determinado. `C4` sólo pregunta si hay justificación **metodológica** "
      "para conservarlos.")
    A("")
    A("| Decisión | Estado | Efecto hoy |")
    A("|---|---|---|")
    A("| `D3` ponderación `0,15/0,10/0,05` | ⬜ sin fundamento cuantitativo | "
      "🔵 **ninguno** · no hay infracciones registradas |")
    A("| `D4` piso `C_i ≥ 0,50` | ⬜ sin fundamento cuantitativo | 🔵 "
      "**ninguno** · el piso no se alcanza |")
    A("")
    A("> ### Veredicto de `D3` y `D4` · **LATENTES · CONSERVABLES CON "
      "REVISIÓN OBLIGATORIA ANTES DE SU PRIMERA ACTIVACIÓN**")
    A(">")
    A("> Hoy no mueven el índice: ninguna infracción está registrada. Se "
      "activan **el día que se registre la primera** — y ése es exactamente "
      "el día en que tienen que estar bien. Conservarlos sin revisar sería "
      "aplazar la decisión hasta el momento en que ya no se pueda tomar con "
      "calma.")
    A("")
    A("Y `D4` merece una línea propia, porque **no es un parámetro técnico**:")
    A("")
    A("> El piso afirma que **incluso acumulando infracciones existe un "
      "mínimo de contribución institucional que debe preservarse**. Eso es "
      "una tesis sustantiva sobre la relación entre infracción y desempeño, y "
      "requiere fundamento propio.")
    A("")

    # ── C4-6 ──────────────────────────────────────────────────────────────
    A("## ★ `C4-6` · Interpretación")
    A("")
    A("> ¿Qué afirmaciones permite el resultado — y cuáles no?")
    A("")
    A("La sección que convierte al dictamen en algo operativo. Lo que "
      "**27,4582 %** autoriza a decir:")
    A("")
    A("| ✅ Se puede afirmar | 🔴 NO se puede afirmar |")
    A("|---|---|")
    A("| «la congruencia **acreditada** de las 25 metas del universo "
      "operacional es 27,4582 %» | «el GAD cumple el 27 % de su PDOT» |")
    A("| «al corte de abril, con `T_i` parcial» | «el desempeño anual es del "
      "27 %» |")
    A("| «`n` metas carecen de evidencia en al menos un silo» | «`n` metas "
      "**no se ejecutaron**» |")
    A("| «el índice mide la cadena completa» | «el índice mide velocidad de "
      "ejecución» (`D-011`) |")
    A("")
    A("> ### La columna derecha no es hipotética")
    A(">")
    A("> `D-011` documenta que la capa de publicación ya describe el ICPI "
      "como «progreso institucional» que «mide velocidad de ejecución». Esa "
      "afirmación **no la sostiene el motor**.")
    A("")

    # ── C4-7 ──────────────────────────────────────────────────────────────
    A("## `C4-7` · AVEP")
    A("")
    A("> ¿El baremo **clasifica el fenómeno medido**, o **traduce el "
      "resultado para comunicación institucional**?")
    A("")
    A("⚠️ **No se pregunta qué escala es correcta.** No se puede validar una "
      "escala antes de declarar el fenómeno que pretende clasificar "
      "(`DOC-012`).")
    A("")
    A("| Lo que consta | |")
    A("|---|---|")
    A("| `AVEP` es un **baremo propio**, no una norma externa | `007-X-bis` |")
    A("| Conviven **dos escalas divergentes** — 4 niveles con umbrales "
      "75/60/50 y 5 con 90/70/40/20 | 🔴 `D-012` |")
    A("| Para el mismo baseline, el motor dice «🟠 Gestión por Ocurrencia» y "
      "el canon «🔴 Nivel de Atención Alta» | 🔴 `D-012` |")
    A("| Qué fenómeno clasifica —integridad, cumplimiento, desempeño, "
      "evidencia o riesgo— | ⬜ **NO DECLARADO** |")
    A("")
    A("> ### Veredicto de `D5` · **NO EVALUABLE HASTA QUE SE DECLARE SU "
      "OBJETO**")
    A(">")
    A("> No es que la escala esté mal: es que **no se puede juzgar**. Y "
      "mientras dos versiones convivan sin que ninguna superficie declare "
      "cuál rige, el mismo número admite dos lecturas institucionales "
      "distintas.")
    A("")

    # ── Dictamen ──────────────────────────────────────────────────────────
    A("## ★ DICTAMEN CONSOLIDADO")
    A("")
    A("| | Decisión | Veredicto |")
    A("|---|---|---|")
    A("| `D1` | multiplicatividad | **no fundamentada · conservable bajo "
      "declaración explícita** |")
    A("| `D2` | `V_i` multiplicativo | **defendible bajo la lectura "
      "«congruencia acreditada» · el sistema debe declarar cuál sostiene** |")
    A("| `D3` | pesos `0,15/0,10/0,05` | **latente · revisión obligatoria "
      "antes de su primera activación** |")
    A("| `D4` | piso `0,50` | **latente · y afirma una tesis sustantiva que "
      "requiere fundamento propio** |")
    A("| `D5` | `AVEP` | **no evaluable hasta declarar su objeto** |")
    A("")
    A("### Lo que el dictamen NO dice")
    A("")
    A("- **No dice que el ICPI esté mal.** Ninguna decisión resultó "
      "incorrecta.")
    A("- **No autoriza a eliminar nada.** `D` era incertidumbre, no condena.")
    A("- **No recalibra.** El Gold Master sigue intacto y el baseline "
      "congelado.")
    A("")
    A("### ⚠️ Y la corrección de la frase de cierre")
    A("")
    A("Una versión anterior decía:")
    A("")
    A("> ~~«El constructo **funciona y es internamente coherente**.»~~")
    A("")
    A("Es **más amplia que lo demostrado**. `D1`-`D5` muestran justamente que "
      "**operatividad matemática ≠ coherencia sustantiva demostrada**. La "
      "formulación canónica es:")
    A("")
    A("> **La implementación actual del constructo es matemáticamente "
      "operativa y sus reglas producen un resultado reproducible; su "
      "coherencia sustantiva depende de decisiones metodológicas que `C4` ha "
      "identificado y cuya necesidad no está completamente fundamentada.**")
    A("")
    A("### ★ Las tres capas, que no pueden colapsarse")
    A("")
    A("| # | Capa | Estado |")
    A("|---|---|---|")
    A("| 1 | **Operatividad computacional** — la fórmula corre y produce "
      "`27,4582 %` de forma reproducible | ✅ **DEMOSTRADA** |")
    A("| 2 | **Consistencia formal** — las reglas se ejecutan juntas sin "
      "conflicto | 🟡 **PARCIAL** · hay decisiones semánticas sin declarar |")
    A("| 3 | **Validez sustantiva** — el índice mide el fenómeno que dice "
      "medir | ⬜ **NO DEMOSTRADA POR `C4`** |")
    A("")
    A("> La tercera capa es la que impide que «el motor funciona» se "
      "convierta inadvertidamente en «el índice es válido». **Las tres pueden "
      "ser ciertas a la vez sin contradicción.**")
    A("")
    A("### ⚠️ Y qué hace realmente `C4` con las decisiones `D`")
    A("")
    A("> **`C4` no las valida ni autoriza a conservarlas: cambia su ESTATUS "
      "EPISTEMOLÓGICO.** Pasan de ser reglas aplicadas sin declarar a ser "
      "decisiones identificadas, acotadas y con condición de revisión.")
    A("")
    A("Lo que le falta al constructo no son correcciones: es **declarar sus "
      "propias elecciones como elecciones**. Cinco decisiones sostienen el "
      "índice y ninguna está declarada como decisión — se presentan como si "
      "fueran propiedades del fenómeno.")
    A("")
    A("### Dictamen global")
    A("")
    A("> **No existe evidencia suficiente para declarar que las decisiones "
      "`D` sean incorrectas. Tampoco existe evidencia suficiente para "
      "tratarlas como propiedades necesarias del fenómeno.**")
    A("")
    A("Ése es el punto medio que `GM-Ω` tenía que alcanzar: ni "
      "conservadurismo ni revisionismo.")
    A("")
    A("### La acción que el dictamen autoriza · **cinco `ADR`, no cuatro**")
    A("")
    A("Son cinco decisiones y **no tienen el mismo tipo epistemológico**, así "
      "que cada una necesita su propia declaración:")
    A("")
    A("| `ADR` | Decisión | Función de la declaración |")
    A("|---|---|---|")
    A("| `ADR-D1` | multiplicatividad | declarar la elección algebraica y sus "
      "alternativas |")
    A("| `ADR-D2` | `V_i` multiplicativo | declarar el significado de la "
      "ausencia / no acreditación |")
    A("| `ADR-D3` | pesos `C_i` | declarar el estado de fundamentación y la "
      "condición de activación |")
    A("| `ADR-D4` | piso `C_i ≥ 0,50` | declarar la tesis sustantiva "
      "implícita y su revisión obligatoria |")
    A("| `ADR-D5` | `AVEP` | declarar el objeto **antes** de usar el "
      "baremo |")
    A("")
    A("Y cada `ADR` debe contener **los diez campos**, o se convierte en una "
      "justificación retrospectiva:")
    A("")
    A("```")
    A("   1. decisión vigente")
    A("   2. fenómeno que pretende representar")
    A("   3. unidad afectada")
    A("   4. evidencia que la sostiene")
    A("   5. alternativas consideradas")
    A("   6. qué está DEMOSTRADO")
    A("   7. qué es INFERENCIA")
    A("   8. qué permanece NO DETERMINABLE")
    A("   9. consecuencias de mantenerla")
    A("  10. condición objetiva para revisarla")
    A("```")
    A("")
    A("⚠️ **Los `ADR` primero; la implementación después.** El motor no se "
      "toca hasta que sus decisiones estén declaradas.")
    A("")
    A("| Después de los cinco `ADR` | |")
    A("|---|---|")
    A("| **Corregir la capa de publicación** | `D-011`, ya abierta |")
    A("| **Declarar el objeto de `AVEP`** | desbloquea `D5` y `D-012` |")
    A("| **Ontología FONDO / FORMA** | `REARQUITECTURA` |")
    A("")
    # ── La frontera ───────────────────────────────────────────────────────
    A("## ★ La frontera · dónde termina `GM-Ω` y empieza la construcción")
    A("")
    A("```")
    A("  C3            genealogía DEMOSTRADA")
    A("  010           dependencia y contexto CLASIFICADOS provisionalmente")
    A("  C4            suficiencia metodológica NO DEMOSTRADA")
    A("  Gold Master   CONGELADO")
    A("  baseline      27,4582 % CONGELADO")
    A("  REARQUITECTURA    autorizado para DISEÑO · no para ejecución todavía")
    A("```")
    A("")
    A("Y el orden de la construcción, que invierte el hábito de empezar por "
      "la fórmula:")
    A("")
    A("```")
    A("  1. qué queremos CONOCER")
    A("  2. qué EVIDENCIA hace falta para conocerlo")
    A("  3. cómo INFERIMOS")
    A("  4. …y sólo al final, qué FÓRMULA merece entrar al Gold Master")
    A("```")
    A("")
    A("> ### La regla que protege de los dos entusiasmos")
    A(">")
    A("> **No se rediseña un indicador porque tenga un problema matemático. "
      "Se rediseña cuando la relación entre fenómeno, unidad, evidencia, "
      "inferencia y resultado deja de estar suficientemente justificada.**")
    A("")
    A("Y las tres cosas que hoy son ciertas **a la vez**, sin contradicción:")
    A("")
    A("| | |")
    A("|---|---|")
    A("| el motor funciona | ✅ |")
    A("| el índice produce un resultado reproducible | ✅ |")
    A("| **no se ha demostrado que ese resultado represente adecuadamente el "
      "fenómeno que se quiere medir** | ⬜ |")
    A("")
    A("### El cambio de pregunta")
    A("")
    A("| Etapa | Pregunta |")
    A("|---|---|")
    A("| `GM-Ω` | ¿qué construimos, y cómo llegó a ser lo que es? |")
    A("| **`REARQUITECTURA`** | **¿qué debe ser QUIRA para responder "
      "correctamente a aquello que queremos conocer sobre la gestión "
      "pública?** |")
    A("")
    A("> **La historia ya hizo su trabajo. Ahora no debemos pedirle que "
      "diseñe el futuro de QUIRA.**")
    A("")
    A("---")
    A("*GM-Ω-ICPI-011-C4 · dictamen sobre 5 decisiones de diseño · el Gold "
      "Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © "
      "2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
