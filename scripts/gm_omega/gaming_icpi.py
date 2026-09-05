# -*- coding: utf-8 -*-
"""
scripts/gm_omega/gaming_icpi.py — GM-Ω-ICPI-009 · GAMING

    ¿Puede un actor mejorar el ICPI **sin mejorar la realidad** que el ICPI
    pretende medir?

    LA PREGUNTA, formulada por el colega y sin la hipótesis de 008 dentro:

        ¿Podría un actor mejorar artificialmente el ICPI seleccionando,
        controlando o favoreciendo aquellas unidades, metas o evidencias cuya
        trazabilidad y ejecución resultan más fáciles de demostrar, sin que
        exista una mejora equivalente del fenómeno medido?

    ⚠️ NO se asume que las 25 se eligieran por disponibilidad de evidencia —eso
    quedó `NO DETERMINABLE` en 008 y el criterio declarado fue el monto. 009 no
    audita el pasado: mide el **incentivo que la fórmula produce hoy**.

    EL MÉTODO. Cada factor se mueve a su máximo, una meta cada vez, y se mide
    cuánto sube el ICPI. Después se separan las palancas por **naturaleza del
    esfuerzo**:

        DOCUMENTAL  se mejora aportando evidencia  → V_i
        MATERIAL    exige ejecutar de verdad        → T_i
        ESTRUCTURAL depende del organigrama         → E_i
        PENDIENTE   semántica sin cerrar            → C_i
        FIJA        no la mueve el gestor           → P_i · R_i

    ⚠️ Y LA COMPARACIÓN NO ES UN VEREDICTO. «Documentar rinde más que ejecutar»
    NO equivale a «hay gaming»: documentar lo realmente hecho es una obligación
    legal y forma parte del fenómeno que el ICPI mide. El gaming sería otra
    cosa — que el índice suba SIN que el fenómeno mejore — y eso 009 no puede
    observarlo desde la fórmula.

    LECTURA PURA · no toca el Gold Master · no recalcula el baseline oficial.
    Todo escenario es CONTRAFACTUAL y NO AUTORIZADO PARA PUBLICACIÓN (`DOC-010`).

Uso:  python scripts/gm_omega/gaming_icpi.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_GAMING_009.md"
_BASELINE = 0.27458226534062735

# Naturaleza del esfuerzo que exige mover cada factor. Es la clasificación que
# convierte una tabla de sensibilidad en una tabla de INCENTIVOS.
# ⚠️ `C_i` ESTUVO CLASIFICADO AQUÍ COMO DOCUMENTAL y era un error de esta
# dirección. Javo lo corrigió describiendo qué captura de verdad:
#
#   «Si T_i = 1,0 (dinero entregado) pero la obra no tiene acta de
#    entrega-recepción ni impacto verificado (C_i → 0), el producto lógico
#    penaliza la meta, anulando el maquillaje contable de fin de año.»
#
# Es decir: `C_i` mide ATRIBUCIÓN Y ENTREGA MATERIAL, no papeleo. Clasificarlo
# como documental inflaba artificialmente el techo de la vía documental — y ése
# era justamente el resultado que 009 mide.
#
# Se deja como PENDIENTE y NO se suma a ninguna vía: su semántica exacta es lo
# que `011-C2/C3` tiene que cerrar, y prejuzgarla aquí sería que un análisis de
# incentivos dictamine sobre el constructo que lo audita.
_NATURALEZA = {
    "V": ("DOCUMENTAL", "aportar evidencia en los cuatro silos"),
    "T": ("MATERIAL", "devengar presupuesto — exige ejecutar"),
    "C": ("PENDIENTE", "⚠️ atribución y entrega material verificada (acta, "
                       "impacto) — su semántica la cierra 011-C2/C3"),
    "E": ("ESTRUCTURAL", "modalidad de ejecución / control del director"),
    "P": ("FIJA", "peso presupuestario — no lo mueve el gestor"),
    "R": ("FIJA", "relevancia jurídica — la fija la norma"),
}


def _icpi(metas: list[dict]) -> float:
    sj = sum(m["P"] * m["R"] * m["V"] * m["E"] * m["T"] * m["C"] for m in metas)
    sk = sum(m["P"] * m["R"] for m in metas)
    return sj / sk if sk else 0.0


def palancas(metas: list[dict]) -> list[dict]:
    """Para cada meta y cada factor movible: ¿cuánto sube el ICPI si ese factor
    pasa a su máximo, dejando TODO lo demás igual?

    Es el «precio» de cada punto de ICPI, y con él se puede ordenar qué es lo
    más rentable de mover — que es exactamente lo que haría alguien que quisiera
    subir el número sin mejorar el fenómeno."""
    base = _icpi(metas)
    out = []
    for i, m in enumerate(metas):
        for f in ("V", "E", "T", "C"):
            if m[f] >= 1.0:
                continue                      # ya está al máximo: no hay palanca
            copia = [dict(x) for x in metas]
            copia[i][f] = 1.0
            nat, coste = _NATURALEZA[f]
            out.append({"meta": m["id"], "factor": f, "de": m[f],
                        "delta": (_icpi(copia) - base) * 100,
                        "naturaleza": nat, "coste": coste})
    out.sort(key=lambda x: -x["delta"])
    return out


def por_naturaleza(pal: list[dict], metas: list[dict]) -> dict:
    """El resultado que decide 009: ¿qué rinde más, documentar o ejecutar?

    Se compara el techo alcanzable moviendo TODOS los factores de una naturaleza
    a la vez — no la suma de palancas individuales, que sobreestima por ignorar
    la interacción multiplicativa."""
    base = _icpi(metas)
    techos = {}
    for nat in ("DOCUMENTAL", "MATERIAL", "ESTRUCTURAL", "PENDIENTE"):
        factores = [f for f, (n, _) in _NATURALEZA.items() if n == nat]
        copia = [dict(x) for x in metas]
        for m in copia:
            for f in factores:
                m[f] = 1.0
        techos[nat] = {"icpi": _icpi(copia),
                       "delta": (_icpi(copia) - base) * 100,
                       "factores": factores}
    return techos


def main() -> int:
    from scripts.gm_omega.sensibilidad_icpi import leer_motor
    d = leer_motor()
    if not d:
        print("[no determinable] Gold Master no resuelto.")
        return 2
    metas = d["metas"]

    base = _icpi(metas)
    if abs(base - _BASELINE) > 1e-9:
        print(f"[hallazgo] el laboratorio no reproduce el baseline: "
              f"{base * 100:.6f} % vs {_BASELINE * 100:.6f} %")
        return 1

    pal = palancas(metas)
    techos = por_naturaleza(pal, metas)

    doc, mat = techos["DOCUMENTAL"]["delta"], techos["MATERIAL"]["delta"]
    print(f"baseline {base * 100:.4f} % · palancas {len(pal)}")
    print(f"techo DOCUMENTAL {doc:+.2f} pp · MATERIAL {mat:+.2f} pp · "
          f"ESTRUCTURAL {techos['ESTRUCTURAL']['delta']:+.2f} pp")
    print(f"las 5 palancas mayores suman "
          f"{sum(p['delta'] for p in pal[:5]):.2f} pp")

    _escribir(metas, pal, techos, base)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(metas, pal, techos, base) -> None:
    o: list[str] = []
    A = o.append
    doc, mat = techos["DOCUMENTAL"]["delta"], techos["MATERIAL"]["delta"]

    A("# GM-Ω · ICPI — GAMING  `009`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/gaming_icpi.py`.")
    A("")
    A("> ### Las tres etiquetas")
    A("> Cada cifra de este documento es **MATEMÁTICAMENTE REPRODUCIBLE** · "
      "**METODOLÓGICAMENTE CONTRAFACTUAL** · **NO AUTORIZADA PARA PUBLICACIÓN** "
      "(`DOC-010`). El único ICPI publicable sigue siendo **27,4582 %**.")
    A("")
    A("## La pregunta")
    A("")
    A("> ¿Podría un actor **mejorar artificialmente el ICPI** seleccionando, "
      "controlando o favoreciendo aquellas unidades, metas o evidencias cuya "
      "trazabilidad resulta más fácil de demostrar, **sin que exista una mejora "
      "equivalente del fenómeno medido**?")
    A("")
    A("⚠️ **009 no audita el pasado.** No asume que las 25 se eligieran por "
      "disponibilidad de evidencia —el criterio declarado fue el monto, y lo "
      "demás quedó `NO DETERMINABLE` en `008`—. Mide **el incentivo que la "
      "fórmula produce hoy**, que es una pregunta independiente.")
    A("")

    A("## El método · naturaleza del esfuerzo")
    A("")
    A("Cada factor se clasifica por **qué hay que hacer realmente** para subirlo:")
    A("")
    A("| Factor | Naturaleza | Qué exige |")
    A("|---|---|---|")
    for f, (nat, coste) in _NATURALEZA.items():
        A(f"| `{f}_i` | **{nat}** | {coste} |")
    A("")
    A("⚠️ **Y la comparación entre las dos primeras NO es un veredicto.** Decir "
      "«si documentar rinde más que ejecutar, el incentivo está torcido» sería "
      "una **hipótesis normativa**, no una conclusión matemática — y puede ser "
      "falsa: si el ICPI mide congruencia, **documentar correctamente lo "
      "ejecutado forma parte del fenómeno**, no es una manipulación.")
    A("")
    A("El gaming es algo más estrecho:")
    A("")
    A("```")
    A("   sube V  →  sube el ICPI  →  pero el fenómeno real NO mejora")
    A("```")
    A("")
    A("Es decir: **optimización del indicador sin mejora equivalente del "
      "constructo**. Y eso **009 no puede observarlo desde la fórmula** — sólo "
      "puede medir dónde está el margen.")
    A("")

    A("## ★ El resultado")
    A("")
    A("Techo alcanzable llevando **todos** los factores de cada naturaleza a su "
      "máximo — no la suma de palancas sueltas, que sobreestimaría al ignorar la "
      "interacción multiplicativa:")
    A("")
    A("| Vía | Factores | ICPI alcanzable | Δ |")
    A("|---|---|---:|---:|")
    for nat in ("DOCUMENTAL", "MATERIAL", "ESTRUCTURAL", "PENDIENTE"):
        t = techos[nat]
        fs = " · ".join(f"`{x}_i`" for x in t["factores"])
        A(f"| **{nat}** | {fs} | {t['icpi'] * 100:.4f} % | {t['delta']:+.2f} pp |")
    A("")
    if doc > mat:
        A(f"> ### 🔴 DOCUMENTAR RINDE MÁS QUE EJECUTAR")
        A(f"> **{doc:+.2f} pp** frente a **{mat:+.2f} pp** — una diferencia de "
          f"**{doc - mat:.2f} puntos**.")
        A("")
        A("Un actor que quisiera subir el número **sin ejecutar una obra más** "
          "obtendría más recorrido aportando evidencia documental que "
          "devengando presupuesto. **El incentivo apunta al papel.**")
    else:
        A(f"> ### 🟢 EJECUTAR RINDE MÁS QUE DOCUMENTAR")
        A(f"> **{mat:+.2f} pp** frente a **{doc:+.2f} pp**.")
        A("")
        A("La vía más rentable para subir el índice **exige ejecución real**. El "
          "incentivo apunta al hecho, no al papel — que es lo que un indicador "
          "de integridad debe producir.")
    A("")

    A("## ⚠️ ¿Es un resultado de la FÓRMULA o del ESTADO?")
    A("")
    A("Las tres palancas mayores son `T_i` **desde 0,30** — el valor del GAD "
      "central en el corte de abril. Cabe que la ventaja material venga de que "
      "**hoy queda mucho margen en `T` y poco en `V`**, no de la arquitectura. "
      "Es una objeción legítima y se puede medir: se repite el análisis "
      "simulando **fin de año**, con la ejecución material ya alta.")
    A("")
    A("| Escenario | DOCUMENTAL | MATERIAL | ¿Qué rinde más? |")
    A("|---|---:|---:|---|")
    A(f"| **Corte abril** (estado real) | {doc:+.2f} pp | {mat:+.2f} pp | "
      f"{'MATERIAL' if mat > doc else 'DOCUMENTAL'} |")
    for etiqueta, tval in (("T = 0,75 · ejecución alta", 0.75),
                           ("T = 0,90 · cierre de año", 0.90)):
        sim = [dict(m) for m in metas]
        for m in sim:
            m["T"] = max(m["T"], tval)
        b2 = _icpi(sim)
        d2 = m2 = 0.0
        for nat, factores in (("DOCUMENTAL", ("V",)), ("MATERIAL", ("T",))):
            cop = [dict(x) for x in sim]
            for m in cop:
                for f in factores:
                    m[f] = 1.0
            delta = (_icpi(cop) - b2) * 100
            if nat == "DOCUMENTAL":
                d2 = delta
            else:
                m2 = delta
        A(f"| {etiqueta} | {d2:+.2f} pp | {m2:+.2f} pp | "
          f"{'MATERIAL' if m2 > d2 else '**DOCUMENTAL**'} |")
    A("")
    A("> ### ★ LA SUPERFICIE DE INCENTIVO ES DINÁMICA")
    A("")
    A("**Y ésta es la respuesta real de 009**, más interesante que un sí o un "
      "no. La objeción era correcta: el resultado **no es una propiedad "
      "atemporal de la fórmula**, sino del estado de ejecución —")
    A("")
    A("```")
    A("  ENERO-ABRIL     ejecutar rinde 6,6× más que documentar")
    A("        ↓         (queda mucho margen material)")
    A("  MITAD DE AÑO    ejecutar sigue rindiendo más, pero por poco")
    A("        ↓")
    A("  CIERRE          documentar rinde el DOBLE que ejecutar   ⚠️")
    A("```")
    A("")
    A("Y la mecánica es clara: cuando `T` se acerca a 1 **el margen material se "
      "agota**, mientras que las metas con `V = 0` siguen valiendo mucho —"
      "porque `V=0` anula la meta entera y recuperarla devuelve todo su peso—. "
      "El último tramo del año es exactamente donde **ejecutar ya no rinde y "
      "documentar sí**.")
    A("")
    A("### La formulación exacta")
    A("")
    A("⚠️ Una versión anterior escribió «la ventana de gaming tiene fecha». Es "
      "retóricamente potente y **epistemológicamente demasiado fuerte**: 009 no "
      "ha identificado el momento real de inversión, sólo la diferencia entre "
      "tres escenarios discretos. La formulación correcta es:")
    A("")
    A("> **La ventaja relativa entre las palancas documental y material depende "
      "del estado temporal del sistema y puede invertirse hacia el cierre del "
      "ejercicio.**")
    A("")
    A("⚠️ Y sobre los instrumentos existentes —`SAT-II Reforma Tardía`, el patrón "
      "`Q4_PUSH`— sólo puede decirse que **son compatibles con la vigilancia de "
      "este patrón**. Afirmar que fueron diseñados como respuesta a este "
      "fenómeno sería reconstruir la intención desde el resultado, que es lo "
      "que `DOC-009` prohíbe. Si aparece un documento que lo diga, se eleva.")
    A("")
    A("⚠️ Salvedad de método: al subir `T` sube también el baseline y los deltas "
      "se comprimen; la simulación mueve `T` de golpe para todas las metas, que "
      "no es como ocurre en la realidad. **La inversión del signo es robusta; "
      "el mes exacto en que ocurre, no está medido.**")
    A("")

    A("## Las palancas individuales")
    A("")
    A("Cuánto sube el ICPI moviendo **un solo factor de una sola meta** a su "
      "máximo, con todo lo demás igual:")
    A("")
    A("| # | Meta | Factor | De | Δ ICPI | Naturaleza |")
    A("|---|---|---|---:|---:|---|")
    for i, p in enumerate(pal[:12], 1):
        A(f"| {i} | `{p['meta']}` | `{p['factor']}_i` | {p['de']:.2f} | "
          f"{p['delta']:+.4f} pp | {p['naturaleza']} |")
    A("")
    top5 = sum(p["delta"] for p in pal[:5])
    A(f"**Las cinco palancas mayores suman {top5:.2f} pp** — de un baseline de "
      f"{base * 100:.2f} %. Y la primera sola vale {pal[0]['delta']:.2f} pp.")
    A("")
    A("⚠️ «Palanca mayor» significa **mayor capacidad de incremento del ICPI bajo "
      "la simulación contrafactual** — no «más rentable» en sentido económico. "
      "Llevar `T` de 0,30 a 1,00 no es comparable con llevar `V` de 0 a 1 sin "
      "saber cuánto cuesta materialmente producir cada incremento, y **eso no "
      "está medido**.")
    A("")
    docs_top = sum(1 for p in pal[:10] if p["naturaleza"] == "DOCUMENTAL")
    A(f"De las **10 palancas más rentables, {docs_top} son DOCUMENTALES**.")
    A("")

    A("## ★ El fenómeno institucional que hay detrás")
    A("")
    A("La inversión que 009 mide **no es una curiosidad matemática**: corresponde "
      "a una dinámica real y conocida del sector público ecuatoriano, que Javo "
      "describe así —")
    A("")
    A("> Los primeros meses se dedican a **planificación, regularización "
      "institucional y procesos precontractuales**; la ejecución fuerte del "
      "gasto se concentra en el **segundo semestre**.")
    A("")
    A("Y de ahí salen cuatro distorsiones que afectan a cualquier evaluación de "
      "PDOT — con la particularidad de que **el ICPI tiene una respuesta para "
      "cada una**:")
    A("")
    A("| Distorsión | Qué pasa | Cómo responde el motor |")
    A("|---|---|---|")
    A("| **Falso negativo semestral** | al primer corte el avance es ~0 y se "
      "lee como incumplimiento, cuando el proyecto está en fase precontractual "
      "| `V_i` captura la **existencia documental** del proceso: distingue la "
      "inactividad de la maduración precontractual |")
    A("| **Disociación financiero ↔ físico** | anticipo transferido en noviembre "
      "= gasto alto, obra sin empezar | `T_i` mide ejecución presupuestaria, "
      "pero `C_i` exige **atribución y entrega**: `T=1` con `C→0` penaliza la "
      "meta y anula el maquillaje contable |")
    A("| **Reforma tardía** | se desvían fondos de infraestructura a gasto "
      "corriente rápido de contratar | dispara `SAT-II` / `SAT-IV`: la mutación "
      "de metas activa alertas de sustitución y fragmentación |")
    A("| **Calidad del gasto** | programas de 8 meses comprimidos en campañas "
      "de 60 días | los indicadores de impacto se vuelven frágiles — y esto el "
      "motor **no lo captura hoy** |")
    A("")
    A("⚠️ **Esto reencuadra el hallazgo de 009.** La inversión del incentivo al "
      "cierre no describe un motor mal diseñado: describe **el momento del año "
      "en que la realidad institucional ecuatoriana concentra su presión**. Que "
      "el índice cambie de comportamiento justo ahí es coherente con el "
      "fenómeno, y por eso `011-C4` no puede juzgarlo sólo como propiedad "
      "algebraica.")
    A("")
    A("### Y una consecuencia que apunta a `v2`")
    A("")
    A("> Las metas del PDOT no pueden evaluarse como un valor binario a fin de "
      "año. Requieren **descomposición por hitos** —viabilidad técnica, "
      "adjudicación, entrega— y una lógica **plurianual** que asuma que las "
      "obras grandes ocupan dos ejercicios.")
    A("")
    A("Eso conecta directamente con `008-R`: si una unidad operacional puede "
      "corresponder a varias metas documentales, **también puede corresponder a "
      "varios hitos temporales de la misma meta**. `011-B` heredaba una "
      "pregunta de correspondencia entre universos; ahora hereda también una de "
      "**correspondencia temporal**.")
    A("")

    A("## ⚠️ Lo que este análisis NO demuestra")
    A("")
    A("- **No demuestra que nadie haya hecho esto.** Mide un incentivo "
      "estructural, no una conducta. Confundirlos sería una acusación sin "
      "evidencia — exactamente lo que el canon prohíbe.")
    A("- **No demuestra que documentar sea ilegítimo.** Aportar evidencia a "
      "LOTAIP o al CPCCS **es una obligación legal**, y que el índice la premie "
      "es correcto. El problema aparecería sólo si documentar rindiera MÁS que "
      "ejecutar, porque entonces el índice premiaría más el cumplimiento formal "
      "que el material.")
    A("- **No mide el coste real de cada palanca.** Se asume que documentar es "
      "más barato que ejecutar, lo cual es plausible y **no está medido**.")
    A("")

    A("## Lo que 009 entrega a `011-C4`")
    A("")
    A("La pregunta de `011-C4` es si la **arquitectura multiplicativa** está "
      "justificada. `007-D` midió que es la decisión más consecuente del motor "
      "(51,26 pp). `009` añade la otra mitad:")
    A("")
    A("> **El incentivo que produce la arquitectura multiplicativa NO ES "
      "CONSTANTE: cambia de signo a lo largo del ejercicio.** Durante la mayor "
      "parte del año premia la ejecución material —lo que un indicador de "
      "integridad debe hacer— y en el tramo final premia la documental.")
    A("")
    A("Eso da a `011-C4` un argumento matizado y utilizable:")
    A("")
    A("- **A favor de conservarla**: durante la ventana operativa relevante, la "
      "vía rentable exige ejecutar. La multiplicatividad **no premia el papel** "
      "mientras quede margen material.")
    A("- **A vigilar**: la inversión de fin de año es una propiedad estructural "
      "de la fórmula, no un defecto de datos. Cualquier rediseño debe "
      "conservar o corregir ese comportamiento **a sabiendas**.")
    A("")
    A("Y una pregunta que `009` entrega y no responde: **¿debería el índice "
      "tener un incentivo constante?** Un indicador cuyo estímulo cambia con el "
      "calendario puede ser exactamente lo correcto —al final del año lo que "
      "queda por hacer ES documentar lo ejecutado— o una debilidad. Eso es "
      "constructo, y lo juzga `011`.")
    A("")
    A("## Dictamen de 009 · por grado de certeza")
    A("")
    A("| Afirmación | Estado |")
    A("|---|---|")
    A("| Existe sensibilidad del ICPI a gaming contrafactual | **DEMOSTRADO** |")
    A("| `T` tiene mayor techo que la vía documental en el corte de abril | **DEMOSTRADO** |")
    A("| Esa ventaja disminuye al acercarse `T` a 1 | **DEMOSTRADO** |")
    A("| Puede producirse inversión documental ↔ material | **DEMOSTRADO en escenarios simulados** |")
    A("| La superficie de incentivo cambia con `T` | **DEMOSTRADO** |")
    A("| Existe un mes exacto de inversión | **NO DETERMINABLE** |")
    A("| Algún GAD ha manipulado efectivamente el ICPI | **NO DETERMINABLE** |")
    A("| Documentar constituye gaming | **NO DEMOSTRADO** |")
    A("| Ejecutar es la única mejora legítima | **NO DEMOSTRADO** |")
    A("| `C_i` es un factor documental | **PENDIENTE** · `011-C2/C3` |")
    A("| El gaming es propiedad permanente del índice | **REFUTADO** |")
    A("| La multiplicatividad debe conservarse por este resultado | **NO DETERMINABLE** · `011-C4` |")
    A("")
    A("> ### GM-Ω-009 — CERRADO COMO DIAGNÓSTICO CONTRAFACTUAL DE GAMEABILIDAD")
    A(">")
    A("> La capacidad de incremento contrafactual del ICPI mediante las distintas "
      "palancas **no es constante durante el ejercicio**. En los escenarios "
      "examinados la vía material domina mientras existe margen de ejecución, y "
      "su ventaja disminuye conforme `T_i` se aproxima a su máximo, pudiendo ser "
      "superada por la recuperación documental.")
    A(">")
    A("> **No demuestra** que haya ocurrido gaming real, ni que documentar sea "
      "conducta indebida, ni el instante de inversión, ni el coste relativo de "
      "cada acción.")
    A(">")
    A("> **Transferible a `011-C4`:** la arquitectura multiplicativa debe "
      "evaluarse no sólo por su sensibilidad estática (`007-D`: 51,26 pp) sino "
      "por los **incentivos marginales que produce a lo largo del ciclo "
      "temporal**.")
    A("")
    A("Y la pregunta que ninguno de los dos responde, y que es la de `011-C4`:")
    A("")
    A("> **¿Es la multiplicatividad una propiedad NECESARIA del constructo de "
      "congruencia intersistémica, o una arquitectura matemática elegida durante "
      "el desarrollo y conservada después?**")
    A("")
    A("---")
    A(f"*GM-Ω-ICPI-009 · {len(pal)} palancas medidas · baseline "
      "27,4582 % congelado · el Gold Master no se modificó · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
