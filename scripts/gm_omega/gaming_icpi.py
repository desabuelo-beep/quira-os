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
        PENDIENTE   semántica sin cerrar            → C_i   (011-C2/C3)
        FIJA        no la mueve el gestor           → P_i · R_i

    ⚠️ `C_i` NO SE CLASIFICA. Hubo dos intentos —documental, luego material— y
    los dos eran prematuros: `011-C2/C3` existe para determinar qué significa
    históricamente cada factor. Si 009 fija esa semántica, un análisis de
    incentivos habrá resuelto la pregunta ontológica que debía auditarlo.

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
#
# ⚠️ `C_i` PASÓ POR DOS ESTADOS ERRÓNEOS Y ÉSTE ES EL TERCERO.
#
#   1. DOCUMENTAL — error de esta dirección. Inflaba el techo de la vía
#      documental, que es justamente el resultado que 009 mide.
#   2. MATERIAL — corregido por Javo: «si T_i = 1,0 (dinero entregado) pero la
#      obra no tiene acta de entrega-recepción ni impacto verificado (C_i → 0),
#      el producto lógico penaliza la meta, anulando el maquillaje contable de
#      fin de año». Plausible, institucionalmente coherente… y **todavía una
#      hipótesis del autor**, no una semántica demostrada del canon.
#   3. PENDIENTE — el estado correcto. Lo señaló el colega: `011-C2/C3` existe
#      precisamente para determinar qué significa históricamente cada factor.
#      Si 009 fija la semántica de `C_i`, entonces un análisis de incentivos
#      habrá resuelto la pregunta ontológica que debía auditarlo a él.
#
# ⚠️ Y ESPERAR TUVO PREMIO. `011-C2` leyó el instrumento y REFUTÓ la hipótesis:
# `C_i` es «Calidad de Proceso Orgánico» —descuentos por infracciones
# normativas verificadas (LOSNCP · CGE/NCI · COPFP · CPCCS)—, no entrega
# material. Si 009 la hubiera dado por buena, habría publicado como respuesta
# del motor una defensa que el motor NO implementa.
#
# SIGUE EN `PENDIENTE`, ahora por una razón mejor documentada: la naturaleza
# del ESFUERZO todavía no se puede fijar, porque depende de qué regla esté
# vigente —lo resuelve `011-C3`—:
#
#   si opera el mecanismo determinista  → JURÍDICA (exige no infringir)
#   si rige el fallback Ci_Manual_2025  → FIJA (ninguna acción del gestor
#                                         la mueve, como P_i y R_i)
#
# NO se suma a ninguna vía.
_NATURALEZA = {
    "V": ("DOCUMENTAL", "aportar evidencia en los cuatro silos"),
    "T": ("MATERIAL", "devengar presupuesto — exige ejecutar"),
    "C": ("PENDIENTE", "**calidad jurídica del proceso** (`011-C2`) — pero la "
                       "naturaleza del esfuerzo sigue abierta: ver nota"),
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
    A("### La nota de `C_i` · por qué sigue sin clasificar")
    A("")
    A("`011-C2` **sí** resolvió qué mide: **calidad jurídica del proceso "
      "orgánico** —descuentos por infracciones normativas verificadas—, y "
      "**refutó** la hipótesis de la entrega material. Pero 009 no clasifica "
      "por lo que un factor mide, sino por **qué hay que hacer para subirlo**, "
      "y eso todavía se bifurca:")
    A("")
    A("| Si `011-C3` determina que rige… | …la naturaleza del esfuerzo es |")
    A("|---|---|")
    A("| el mecanismo determinista (deducción por infracciones) | **JURÍDICA** "
      "· exige no incurrir en infracciones |")
    A("| el fallback `Ci_Manual_2025` | **FIJA** · ninguna acción del gestor la "
      "mueve, como `P_i` y `R_i` |")
    A("")
    A("Son incentivos opuestos —uno accionable, el otro inerte—, así que "
      "`C_i` **no se suma a ninguna vía** y no altera el resultado.")
    A("")
    A("⚠️ **Y esperar tuvo premio.** Si `009` hubiera dado por buena la "
      "hipótesis, habría publicado como respuesta del motor una defensa contra "
      "el maquillaje contable que **el motor no implementa**.")
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
    razon = (mat / doc) if doc else float("inf")
    A(f"> ### En el escenario de abril, el techo de `T_i` es {razon:.2f}× el de `V_i`")
    A(f"> **{mat:+.2f} pp** frente a **{doc:+.2f} pp**.")
    A("")
    A("**Ésta es la única formulación canónica del resultado**, y está "
      "deliberadamente escrita en términos de factores y no de conductas:")
    A("")
    A(f"> En el escenario contrafactual de abril, la capacidad de incremento "
      f"del ICPI atribuida a la modificación de `T_i` fue aproximadamente "
      f"**{razon:.2f} veces** la atribuida a la modificación de `V_i`, "
      f"**manteniendo las demás condiciones del escenario**.")
    A("")
    A("⚠️ **Se retiró el marco «ejecución vs documentación».** Era cómodo y "
      "engañoso por dos motivos: sugiere una teoría del coste y del "
      "comportamiento del gestor que `009` **no tiene** —un techo "
      "contrafactual no dice qué es más barato ni más probable—, y presupone "
      "que cada factor equivale a una conducta. `011-C2` mostró que esa "
      "equivalencia no se sostiene: `C_i` no era lo que la lectura intuitiva "
      "decía, y nada garantiza que `V_i` y `T_i` sí lo sean.")
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
    sims: dict[float, tuple[float, float]] = {}
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
        sims[tval] = (d2, m2)
        A(f"| {etiqueta} | {d2:+.2f} pp | {m2:+.2f} pp | "
          f"{'MATERIAL' if m2 > d2 else '**DOCUMENTAL**'} |")
    A("")
    A("> ### ★ LA SUPERFICIE DE INCENTIVO ES DINÁMICA")
    A("")
    A("**Y ésta es la respuesta real de 009**, más interesante que un sí o un "
      "no. La objeción era correcta: el resultado **no es una propiedad "
      "atemporal de la fórmula**, sino del estado de ejecución —")
    A("")
    d75, m75 = sims[0.75]
    d90, m90 = sims[0.90]
    A("```")
    A(f"  T = 0,30   techo material ≈ {mat / doc:.1f}× el documental")
    A("      ↓      (queda mucho margen material)")
    A(f"  T = 0,75   sigue dominando el material, ≈ {m75 / d75:.1f}×")
    A("      ↓")
    A(f"  T = 0,90   se invierte: el documental ≈ {d90 / m90:.1f}× el material")
    A("```")
    A("")
    A("⚠️ El eje es `T`, **no el calendario**. Rotularlo «enero-abril / cierre» "
      "sería atribuir a la simulación una escala temporal que no tiene: 009 "
      "movió `T` de golpe para todas las metas, y eso no es cómo avanza un "
      "ejercicio presupuestario real.")
    A("")
    A("Y la mecánica es transparente: cuando `T` se acerca a 1 **el margen "
      "material se agota**, mientras que las metas con `V = 0` siguen valiendo "
      "mucho —porque `V=0` anula la meta entera y recuperarla devuelve todo su "
      "peso—. Es decir, **la inversión no viene de una fecha sino del "
      "agotamiento del recorrido de un factor acotado en [0,1]**.")
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
      "= gasto alto, obra sin empezar | 🔴 **NO LO CAPTURA** · `011-C2` "
      "demostró que `C_i` mide **legalidad del proceso**, no entrega: sólo "
      "baja ante una infracción registrada, y hoy no hay ninguna |")
    A("| **Reforma tardía** | se desvían fondos de infraestructura a gasto "
      "corriente rápido de contratar | dispara `SAT-II` / `SAT-IV`: la mutación "
      "de metas activa alertas de sustitución y fragmentación |")
    A("| **Calidad del gasto** | programas de 8 meses comprimidos en campañas "
      "de 60 días | los indicadores de impacto se vuelven frágiles — y esto el "
      "motor **no lo captura hoy** |")
    A("")
    A("### 📜 CORRECCIÓN POSTERIOR — aportada por `011-C2`")
    A("")
    A("⚠️ **REGLA EDITORIAL DE ESTE EXPEDIENTE.** `009` **no se reescribe** "
      "para adoptar las conclusiones de `011-C2`. Conserva su naturaleza "
      "histórica y **anexa** la corrección, porque lo que GM-Ω necesita poder "
      "demostrar es la secuencia entera:")
    A("")
    A("```")
    A("  qué pensábamos  →  qué evidencia apareció  →  qué hubo que corregir")
    A("```")
    A("")
    A("Un expediente al que se le retocan las hipótesis para que todo parezca "
      "coherente en retrospectiva vale mucho menos que uno que muestra dónde "
      "se equivocó y con qué se corrigió.")
    A("")
    A("**Lo que 009 afirmó:** que el motor responde a la disociación "
      "financiero ↔ físico, porque «`C_i` exige atribución y entrega: `T=1` "
      "con `C→0` penaliza la meta».")
    A("")
    A("**Lo que `011-C2` encontró en el instrumento:**")
    A("")
    A("> `C_i` es **«Calidad de Proceso Orgánico»**. Nace en 1,00 por "
      "presunción de legalidad y se deduce por **infracciones normativas "
      "verificadas** (LOSNCP · CGE/NCI · COPFP · CPCCS). **Ninguna de las "
      "cuatro mide entrega material**, y hoy las cuatro están en cero para las "
      "25 metas.")
    A("")
    A("**Cómo queda la afirmación:** la hipótesis de que `C_i` mide o verifica "
      "la entrega material **no encuentra respaldo en la especificación ni en "
      "el mecanismo actualmente implementado**; la evidencia la contradice "
      "**como descripción del mecanismo vigente**. Lo que se quiso hacer "
      "originalmente es otra pregunta, y es `NO DETERMINABLE` hasta `011-C3`.")
    A("")
    A("**Consecuencia:** **dos distorsiones quedan sin cubrir, no una**.")
    A("")
    A("### ⚠️ Y aquí 009 tuvo que retirar una frase")
    A("")
    A("La versión anterior cerraba así:")
    A("")
    A("> ~~«La inversión del incentivo al cierre **no describe un motor mal "
      "diseñado**: describe el momento del año en que la realidad institucional "
      "ecuatoriana concentra su presión.»~~")
    A("")
    A("Suena bien y es **una absolución**. «No describe un motor mal diseñado» "
      "es un juicio de validez sobre la arquitectura, y `009` no tiene "
      "competencia para emitirlo — ni para condenar ni para absolver. La "
      "formulación forense es:")
    A("")
    A("> La inversión observada en los escenarios simulados **puede ser "
      "compatible** con la dinámica temporal de la gestión pública descrita, "
      "pero esa compatibilidad **no determina por sí misma que la arquitectura "
      "sea adecuada ni inadecuada**. La valoración corresponde a `011-C4`.")
    A("")
    A("### La triangulación que esto abre para `011-C2/C3`")
    A("")
    A("El marco institucional separa tres cosas que el motor **podría** estar "
      "midiendo por separado — y saber si lo hace es exactamente la pregunta de "
      "`011-C2`:")
    A("")
    A("| # | Dimensión | Pregunta | Fuente |")
    A("|---|---|---|---|")
    A("| 1 | Ejecución financiera · `T_i` | ¿cuánto presupuesto se ha devengado? "
      "| eSIGEF / Presupuesto |")
    A("| 2 | Evidencia de trazabilidad · `V_i` | ¿existe respaldo documental del "
      "proceso? | LOTAIP / SERCOP |")
    A("| 3 | Calidad jurídica del proceso · `C_i` | ¿hay infracciones "
      "normativas verificadas? | `H01` Secciones L/M — **resuelto por "
      "`011-C2`** |")
    A("| 4 | Entrega o resultado material | ¿lo pagado y respaldado produjo el "
      "bien o servicio? | 🔴 **NINGUNA VARIABLE LO MIDE** |")
    A("")
    A("```")
    A("  PRESUPUESTO")
    A("       │")
    A("       ▼")
    A("     T = 1")
    A("       ├──────────────┬──────────────┐")
    A("       ▼              ▼              ▼")
    A("  ¿se ejecutó?  ¿fue legal?     ¿se entregó?")
    A("      T_i           C_i               ⬜")
    A("                                  NADIE LO MIDE")
    A("```")
    A("")
    A("⚠️ **La hipótesis se contrastó y no se sostuvo.** `011-C2` leyó el "
      "instrumento: `C_i` mide **calidad jurídica del proceso** —descuentos "
      "por infracciones verificadas—, no entrega del producto. La defensa "
      "contra el maquillaje contable de fin de ejercicio **no está "
      "implementada**; la rama derecha del diagrama está vacía.")
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
      "es coherente con un constructo de congruencia. Que la vía documental "
      "tenga más techo que la material en un escenario dado **no basta** para "
      "concluir que el incentivo esté torcido: eso exigiría demostrar que el "
      "incremento documental ocurre sin mejora del fenómeno, que es "
      "precisamente lo que 009 no puede observar.")
    A("- **No mide el coste real de cada palanca.** Se asume que documentar es "
      "más barato que ejecutar, lo cual es plausible y **no está medido**.")
    A("- **No resuelve qué es `C_i`.** La hipótesis de entrega material es del "
      "autor, no del expediente. `011-C2/C3`.")
    A("")

    A("## Lo que 009 entrega a `011-C4`")
    A("")
    A("La pregunta de `011-C4` es si la **arquitectura multiplicativa** está "
      "justificada. `007-D` midió que es la decisión más consecuente del motor "
      "(51,26 pp). `009` añade la otra mitad:")
    A("")
    A("> **El techo contrafactual que produce la arquitectura multiplicativa NO "
      "ES CONSTANTE: depende del estado de `T`.** Mientras queda margen "
      "material, la vía material domina; conforme `T` se agota, la documental "
      "puede superarla.")
    A("")
    A("Eso da a `011-C4` **dos entradas de signo opuesto**, y ninguna es un "
      "veredicto:")
    A("")
    A("- La multiplicatividad produce, en el estado observado, un techo mayor "
      "por la vía que exige ejecución material.")
    A("- Ese ordenamiento **no se conserva** en todo el rango de `T`. Cualquier "
      "rediseño —o la decisión de no rediseñar— debe tomarse **a sabiendas** de "
      "que el comportamiento se invierte.")
    A("")
    A("Y una pregunta que `009` entrega y no responde: **¿debería el índice "
      "tener un incentivo constante?** Un indicador cuyo estímulo cambia con el "
      "estado de ejecución puede ser exactamente lo correcto —cuando ya no "
      "queda nada que ejecutar, lo que queda por hacer ES documentar lo "
      "ejecutado— o una debilidad. Eso es constructo, y lo juzga `011`.")
    A("")
    A("### La pregunta que 009 le hereda a `011-C4`")
    A("")
    A("Más fina que «¿hay gaming?», y la formuló el colega:")
    A("")
    A("> **¿El ICPI está diseñado para evaluar el ESTADO de una meta en un "
      "momento del ciclo fiscal, o para evaluar RETROSPECTIVAMENTE la "
      "integridad de todo su proceso de materialización?**")
    A("")
    A("Porque son cosas distintas, y la misma tupla se lee al revés según cuál "
      "sea:")
    A("")
    A("| Estado | Lectura A · «estado en el ciclo» | Lectura B · «integridad retrospectiva» |")
    A("|---|---|---|")
    A("| `T` bajo · `V` alto | correctamente en fase precontractual | incumplimiento |")
    A("| `T` alto · `V` alto | ejecutó y documentó | ejecutó y documentó |")
    A("| `T` alto · `V` alto · resultado material bajo | ✅ el índice no lo ve | ⚠️ gastó y documentó sin producir |")
    A("")
    A("La tercera fila es donde `C_i` sería decisivo **si** su semántica resulta "
      "ser la que Javo propone. Otra razón para no cerrarla aquí.")
    A("")
    A("### Cadena de entradas al dictamen")
    A("")
    A("```")
    A("  007-D  arquitectura multiplicativa        Δ estructural ≈ 51,26 pp")
    A("     │")
    A("  009    superficie de incentivo dinámica   depende de T")
    A("     │")
    A("  008    universo y unidad real             25 de 66 · N:1 no probado")
    A("     │")
    A("  010    transferibilidad LATAM             ¿qué parte es local?")
    A("     │")
    A("     ▼")
    A("  011-C4 ¿es la multiplicatividad NECESARIA para el constructo?")
    A("```")
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
    A("| `C_i` es un factor documental | **REFUTADO** por el propio autor |")
    A("| `C_i` mide **atribución** | ✅ **CONFIRMADO** por `011-C2` · Sección I |")
    A("| `C_i` mide o verifica **entrega material** | 🔴 **SIN RESPALDO EN EL "
      "MECANISMO VIGENTE** (`011-C2`) · mide infracciones normativas. La "
      "INTENCIÓN original queda `NO DETERMINABLE` hasta `011-C3` |")
    A("| El gaming es propiedad permanente del índice | **REFUTADO** |")
    A("| La arquitectura es adecuada / inadecuada | **FUERA DEL ALCANCE de 009** · `011-C4` |")
    A("| La multiplicatividad debe conservarse por este resultado | **NO DETERMINABLE** · `011-C4` |")
    A("")
    A("> ### GM-Ω-009 — CERRADO")
    A(">")
    A("> QUIRA identificó una **superficie de incentivo temporalmente variable** "
      "y delimitó las condiciones bajo las cuales la recuperación documental "
      "puede superar a la ejecución material. El análisis **no demuestra "
      "conducta de gaming ni resuelve la semántica de `C_i`**; ambas cuestiones "
      "quedan **fuera del alcance de 009**.")
    A(">")
    A("> Tampoco absuelve ni condena la arquitectura: la compatibilidad entre "
      "la inversión simulada y la dinámica real de la gestión pública **no "
      "determina que el diseño sea adecuado ni inadecuado**. Esa valoración es "
      "de `011-C4`.")
    A(">")
    A("> **Transferible a `011-C4`:** la arquitectura multiplicativa debe "
      "evaluarse no sólo por su sensibilidad estática (`007-D`: 51,26 pp) sino "
      "por los **incentivos marginales que produce a lo largo del rango de "
      "ejecución**.")
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
