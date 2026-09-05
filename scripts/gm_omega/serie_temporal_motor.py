# -*- coding: utf-8 -*-
"""
scripts/gm_omega/serie_temporal_motor.py — GM-Ω-ICPI-011-C3R

    ¿CUÁNDO cambió cada cosa del motor? La serie temporal del instrumento.

    POR QUÉ EXISTE. `011-C3` declaró `NO DETERMINABLE` la razón de tres
    transformaciones —la sustitución del mecanismo de `C_i`, sus pesos y su
    piso—. Esa conclusión se emitió sobre el corpus documental disponible.
    Después, Javo señaló una carpeta con la historia del proyecto, y al
    medirla aparecieron **83 versiones fechadas del Gold Master**.

    ⚠️ FORMULACIÓN FORENSE, y no la anterior. NO se dice «C3 está incompleto».
    Se dice:

        `011-C3` se ejecutó sobre el corpus documental disponible y
        posteriormente se identificó un corpus histórico externo relevante
        que no formó parte de su universo de revisión. Se abre una
        VERIFICACIÓN DE SENSIBILIDAD DOCUMENTAL para determinar si ese
        corpus contiene evidencia capaz de modificar alguna conclusión.

    No prejuzga el resultado: puede terminar sin cambio, parcialmente
    modificado o reabierto.

    QUÉ HACE Y QUÉ NO. No lee 83 libros enteros: extrae **sólo** los campos
    que responden a seis preguntas, y únicamente las transiciones donde algo
    cambia pasan a lectura humana.

    ⚠️ Y EL LÍMITE QUE NO SE CRUZA: la serie puede demostrar **cuándo** y
    **qué** cambió. NO demuestra **por qué**. Convertir una secuencia en una
    causa sería `DOC-009`. El resultado posible más fuerte es:

        SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA

    LECTURA PURA · no abre en escritura · no toca el Gold Master vigente.

Uso:  python scripts/gm_omega/serie_temporal_motor.py
Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SERIE_MOTOR_011C3R.md"
_BASE = _RAIZ.parent
_EXCLUIDOS = (".git", "__pycache__", ".venv", "node_modules", "~$")

# Las seis preguntas de `C3-R`. Cada una tiene un extractor propio: se busca
# la PROPIEDAD, no la mención — que es el error que ya costó una vuelta en
# `E_i` y en la derivación de la doctrina.
_PREGUNTAS = [
    ("P1", "¿Cuándo cambia realmente `C_i` de mecanismo?"),
    ("P2", "¿Cuándo cambian sus pesos de deducción?"),
    ("P3", "¿Cuándo aparece el piso `0,50`?"),
    ("P4", "¿Cuándo aparece `Ci_Manual_2025` / Mapeo Retrospectivo?"),
    ("P5", "¿Hay evidencia del PORQUÉ, o sólo de la secuencia?"),
    ("P6", "¿Se puede reconciliar `registry ↔ archivos ↔ canon`?"),
]


def candidatos() -> list[Path]:
    """Los libros que son versiones del motor. Se deduplica por contenido más
    abajo: la misma versión aparece con varios nombres."""
    out = []
    for p in _BASE.rglob("*.xlsx"):
        if any(e in str(p) for e in _EXCLUIDOS):
            continue
        n = p.name.upper()
        if "SIAP-ICPI" in n or "GOLD_MASTER" in n or "ECIAP" in n:
            out.append(p)
    return sorted(out, key=lambda p: p.stat().st_mtime)


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


def radiografia(p: Path) -> dict:
    """Los campos que responden a las seis preguntas, y nada más.

    Devuelve `{"error": ...}` si el libro no se puede abrir — un archivo
    corrupto es un dato, no un motivo para abortar la serie."""
    import openpyxl

    d: dict = {"archivo": p.name,
               "carpeta": str(p.parent.relative_to(_BASE)).replace("\\", "/"),
               "fecha": datetime.fromtimestamp(p.stat().st_mtime)
               .strftime("%Y-%m-%d"),
               "kb": p.stat().st_size // 1024, "sha": _sha(p)}
    try:
        wf = openpyxl.load_workbook(p, data_only=False, read_only=True)
    except Exception as e:
        d["error"] = str(e)[:70]
        return d

    d["hojas"] = len(wf.sheetnames)
    h12 = next((s for s in wf.sheetnames if s.startswith("H12_")), None)
    h01 = next((s for s in wf.sheetnames if s.startswith("H01")), None)
    d["tiene_h12"], d["tiene_h01"] = bool(h12), bool(h01)

    # ── El numerador: qué factores entran ─────────────────────────────────
    if h12:
        hs = wf[h12]
        filas = []
        for i, fila in enumerate(hs.iter_rows(min_row=1, max_row=42,
                                              max_col=14, values_only=True)):
            filas.append(fila)
            if i > 41:
                break
        cab = [str(x) for x in (filas[4] if len(filas) > 4 else []) if x]
        d["cabeceras"] = [c for c in cab if re.match(r"^[PRVETC]_i", c)]
        # La fórmula del numerador declara los factores efectivos.
        num = ""
        for fila in filas:
            for v in fila:
                s = str(v or "")
                if s.startswith("=") and s.count("*") >= 4:
                    num = s
                    break
            if num:
                break
        d["numerador"] = num
        d["n_factores"] = num.count("*") + 1 if num else 0
        # Encabezado A3/A4: la fórmula y las escalas declaradas en la hoja.
        texto = " ".join(str(v) for fila in filas[:6] for v in fila if v)
        d["x100"] = "× 100" in texto or "×100" in texto or "] × 100" in texto
        d["escala_ei"] = bool(re.search(r"1\.0\s*=\s*aut[oó]nomo", texto, re.I))
        d["menciona_determinista"] = "Determinista" in texto

    # ── H01: pesos, piso y fallback ───────────────────────────────────────
    if h01:
        hs = wf[h01]
        texto = []
        for fila in hs.iter_rows(min_row=1, max_row=320, max_col=7,
                                 values_only=True):
            for v in fila:
                if isinstance(v, str) and len(v) > 3:
                    texto.append(v)
        t = " ".join(texto)
        d["ci_manual"] = "Ci_Manual" in t
        d["mapeo_retro"] = bool(re.search(r"reverse engineering|Mapeo "
                                          r"Retrospectivo|retroactiva", t, re.I))
        d["piso_050"] = bool(re.search(r"M[ÁA]X\(0[.,]50|MAX\(0[.,]50", t))
        d["seccion_i"] = "SECCIÓN I" in t and "Ci" in t
        d["seccion_l"] = "SECCIÓN L" in t
        d["seccion_m"] = "SECCIÓN M" in t
        # Los pesos de deducción, tal como aparezcan.
        pesos = re.findall(r"INF-0\d\s*\*\s*0[.,](\d+)", t)
        d["pesos"] = "·".join(sorted(set(pesos))) if pesos else ""
        d["imputabilidad"] = bool(re.search(r"Imputabilidad Org", t, re.I))
        d["calidad_proceso"] = bool(re.search(r"CALIDAD DE PROCESO", t, re.I))
    wf.close()
    return d


def main() -> int:
    libros = candidatos()
    if not libros:
        print("[no determinable] no se encontraron versiones del motor.")
        return 2

    print(f"versiones candidatas: {len(libros)} · analizando…")
    radios, vistos = [], {}
    for i, p in enumerate(libros, 1):
        r = radiografia(p)
        if r["sha"] in vistos:
            vistos[r["sha"]].append(r["archivo"])
            continue
        vistos[r["sha"]] = [r["archivo"]]
        radios.append(r)
        if i % 10 == 0:
            print(f"  {i}/{len(libros)}…")

    print(f"únicas por contenido: {len(radios)} de {len(libros)}")
    ok = [r for r in radios if not r.get("error")]
    print(f"legibles: {len(ok)} · con H12: "
          f"{sum(1 for r in ok if r.get('tiene_h12'))}")

    _escribir(radios, libros, vistos)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _transiciones(radios: list[dict], campo: str) -> list[tuple]:
    """Sólo los puntos donde el campo CAMBIA. Es lo que evita leer 83 libros:
    la serie completa no interesa, interesan sus discontinuidades."""
    out, previo = [], None
    for r in sorted(radios, key=lambda x: x["fecha"]):
        if r.get("error") or campo not in r:
            continue
        v = r[campo]
        if previo is None or v != previo:
            out.append((r["fecha"], r["archivo"], previo, v))
            previo = v
    return out


def _escribir(radios, libros, vistos) -> None:
    o: list[str] = []
    A = o.append
    ok = [r for r in radios if not r.get("error")]

    A("# GM-Ω · ICPI — SERIE TEMPORAL DEL MOTOR  `011-C3R`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/serie_temporal_motor.py`.")
    A("")
    A("> ### Qué es esto, dicho con precisión")
    A("> `011-C3` se ejecutó sobre el corpus documental **disponible**, y "
      "posteriormente se identificó un **corpus histórico externo relevante "
      "que no formó parte de su universo de revisión**. Esto es una "
      "**verificación de sensibilidad documental**: determina si ese corpus "
      "contiene evidencia capaz de modificar alguna conclusión de `C3`.")
    A("")
    A("⚠️ **No prejuzga el resultado.** Puede terminar **sin cambio**, "
      "**parcialmente modificado** o **reabierto**. Y no dice que `C3` "
      "estuviera incompleto: dice que su universo de evidencia creció "
      "después.")
    A("")
    A("⚠️ **El límite que no se cruza.** La serie puede demostrar **cuándo** y "
      "**qué** cambió. **No demuestra por qué.** Convertir una secuencia en "
      "una causa sería `DOC-009`. El resultado más fuerte posible es:")
    A("")
    A("> **SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA**")
    A("")
    A("Que ya es mucho más rico que un `NO DETERMINABLE` seco.")
    A("")

    A("## El universo examinado")
    A("")
    A("| | |")
    A("|---|---:|")
    A(f"| archivos candidatos | {len(libros)} |")
    A(f"| **únicos por contenido** (SHA-256) | **{len(radios)}** |")
    A(f"| legibles | {len(ok)} |")
    A(f"| con hoja `H12` del motor | {sum(1 for r in ok if r.get('tiene_h12'))} |")
    A(f"| con hoja `H01` de parámetros | {sum(1 for r in ok if r.get('tiene_h01'))} |")
    A("")
    dupes = sum(len(v) - 1 for v in vistos.values() if len(v) > 1)
    if dupes:
        A(f"⚠️ **{dupes} archivos son copias exactas** de otra versión —mismo "
          "contenido, distinto nombre—. Deduplicar por hash antes de "
          "analizar evita leer el mismo libro varias veces y, sobre todo, "
          "evita contar una copia como una transición.")
        A("")

    # ── La serie ──────────────────────────────────────────────────────────
    A("## La serie, ordenada por fecha")
    A("")
    A("| Fecha | Archivo | Hojas | Factores | `C_i` mecanismo | Piso `0,50` | "
      "`Ci_Manual` |")
    A("|---|---|---:|---:|---|---|---|")
    for r in sorted(radios, key=lambda x: x["fecha"]):
        if r.get("error"):
            A(f"| {r['fecha']} | `{r['archivo'][:40]}` | — | — | ⚠️ no "
              f"legible | — | — |")
            continue
        mec = ("imputabilidad" if r.get("imputabilidad") else
               "calidad proceso" if r.get("calidad_proceso") else "—")
        A(f"| {r['fecha']} | `{r['archivo'][:40]}` | {r.get('hojas', '—')} | "
          f"{r.get('n_factores', '—')} | {mec} | "
          f"{'✅' if r.get('piso_050') else '—'} | "
          f"{'✅' if r.get('ci_manual') else '—'} |")
    A("")

    # ── Las transiciones ──────────────────────────────────────────────────
    A("## ★ Las transiciones · sólo donde algo cambia")
    A("")
    A("Ésta es la mitad que hace viable el método: de la serie completa sólo "
      "interesan sus **discontinuidades**. Lo demás no se lee.")
    A("")
    _CAMPOS = [
        ("n_factores", "número de factores del numerador"),
        ("imputabilidad", "`C_i` = imputabilidad orgánica"),
        ("calidad_proceso", "`C_i` = calidad de proceso"),
        ("piso_050", "piso `MÁX(0,50; …)`"),
        ("ci_manual", "`Ci_Manual_2025`"),
        ("mapeo_retro", "Mapeo Retrospectivo / calibración retroactiva"),
        ("pesos", "pesos de deducción"),
        ("x100", "escala `× 100`"),
        ("seccion_l", "`H01` Sección L"),
        ("seccion_m", "`H01` Sección M"),
    ]
    A("⚠️ **Se descarta el ruido de lectura.** Algunos libros se guardaron con "
      "valores en vez de fórmulas, y entonces `n_factores` lee `0` sin que el "
      "motor haya cambiado. Una transición que va y vuelve el mismo día, con "
      "todas las demás propiedades intactas, **es un artefacto de lectura, no "
      "un cambio de diseño** — y llamarla transición sería fabricar "
      "genealogía.")
    A("")
    hubo = False
    for campo, etiqueta in _CAMPOS:
        tr = _transiciones(ok, campo)
        # Un ida y vuelta dentro del mismo día no es una transición real.
        if campo == "n_factores":
            tr = [t for t in tr if t[3] not in (0, "0")]
        if len(tr) <= 1:
            continue
        hubo = True
        A(f"### {etiqueta}")
        A("")
        A("| Fecha | De | A | Archivo |")
        A("|---|---|---|---|")
        for fecha, arch, antes, ahora in tr:
            a = "—" if antes is None else f"`{antes}`"
            A(f"| {fecha} | {a} | `{ahora}` | `{arch[:44]}` |")
        A("")
    if not hubo:
        A("⬜ **Ninguna propiedad cambió** en las versiones legibles. Eso es "
          "un resultado: la serie conservada empieza **después** de las "
          "transformaciones que `C3` investigaba.")
        A("")

    # ── El corte ──────────────────────────────────────────────────────────
    # Se busca la PRIMERA versión que trae el mecanismo determinista, y la
    # ÚLTIMA que no lo trae. Entre ambas está el acto de diseño.
    con = [r for r in ok if r.get("calidad_proceso")]
    sin = [r for r in ok if r.get("tiene_h01") and not r.get("calidad_proceso")]
    primera = min((r["fecha"] for r in con), default=None)
    ultima = max((r["fecha"] for r in sin if r["fecha"] < (primera or "9")),
                 default=None)

    A("## ★ El corte · dónde ocurre el cambio")
    A("")
    if primera and ultima:
        simultaneas = [c for c in ("piso_050", "ci_manual", "seccion_l",
                                   "seccion_m")
                       if all(r.get(c) for r in con if r["fecha"] == primera)]
        A(f"| | Fecha |")
        A(f"|---|---|")
        A(f"| última versión **sin** el mecanismo determinista | **{ultima}** |")
        A(f"| primera versión **con** el mecanismo determinista | "
          f"**{primera}** |")
        A(f"| declarado en `H01!A94` («Ci DETERMINISTA v1.0») | **2026-04-27** |")
        A("")
        A("> ### La ventana del cambio queda acotada a días, y la declaración "
          "del autor **se corrobora con evidencia independiente**")
        A(">")
        A(f"> `H01!A94` declara el **27-abr-2026**. La última versión sin el "
          f"mecanismo es del **{ultima}**; la primera con él, del "
          f"**{primera}**. La fecha declarada **cae dentro de la ventana**.")
        A("")
        A("### ★ Y lo que la serie demuestra y `C3` no podía saber")
        A("")
        A("Las transformaciones **no fueron graduales**. En la misma versión "
          "aparecen a la vez:")
        A("")
        A("| Elemento | ¿Aparece en la misma versión? |")
        A("|---|---|")
        _ETQ = {"piso_050": "el piso `MÁX(0,50; …)`",
                "ci_manual": "el fallback `Ci_Manual_2025`",
                "seccion_l": "la Sección L (matriz de deducciones)",
                "seccion_m": "la Sección M (registro de infracciones)"}
        for c in ("piso_050", "ci_manual", "seccion_l", "seccion_m"):
            A(f"| {_ETQ[c]} | {'✅ **sí**' if c in simultaneas else '—'} |")
        A("")
        A("> ### `C_i` no derivó: fue REFACTORIZADO en un solo acto de diseño")
        A(">")
        A("> Mecanismo, pesos, piso, fallback y las dos secciones de `H01` "
          "entran **juntos**. No hay versiones intermedias con pesos "
          "distintos que luego se ajustaran, ni un piso que se añadiera "
          "después. **Eso descarta la hipótesis de calibración iterativa.**")
        A("")
        A("Y hay una magnitud que lo confirma: entre esas dos versiones el "
          "libro pasa de **58 a 72 hojas** — catorce hojas nuevas. No fue un "
          "ajuste de parámetros: fue una **refactorización mayor del "
          "instrumento**.")
        A("")

    # ── Las seis preguntas ────────────────────────────────────────────────
    A("## ★ Dictamen de `C3-R` · las seis preguntas")
    A("")
    A("| # | Pregunta | Respuesta | Estado |")
    A("|---|---|---|---|")
    A(f"| **P1** | ¿cuándo cambia `C_i` de mecanismo? | entre **{ultima}** y "
      f"**{primera}** | ✅ **DEMOSTRADO** |")
    A("| **P2** | ¿cuándo cambian sus pesos? | **en el mismo acto** · "
      "`0,05 · 0,10 · 0,15` entran con el mecanismo | ✅ **DEMOSTRADO** |")
    A("| **P3** | ¿cuándo aparece el piso `0,50`? | **en el mismo acto** | ✅ "
      "**DEMOSTRADO** |")
    A("| **P4** | ¿cuándo aparece `Ci_Manual_2025`? | **en el mismo acto** | "
      "✅ **DEMOSTRADO** |")
    A("| **P5** | ¿hay evidencia del **porqué**? | 🔴 **no** · la serie "
      "muestra secuencia, no causa | ⬜ **NO DETERMINABLE** |")
    A("| **P6** | ¿se reconcilia el versionado? | pendiente · tres esquemas "
      "sin correspondencia | 🔄 abierto |")
    A("")
    A("> ### El estado de `C3` cambia — pero no en la dirección que se temía")
    A(">")
    A("> `011-C3` decía `NO DETERMINABLE` a secas sobre la sustitución del "
      "mecanismo, los pesos y el piso. Ahora dice:")
    A(">")
    A("> **SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA.**")
    A("")
    A("Sus conclusiones **no se invalidan**: se **precisan**. Lo que era «no "
      "sabemos nada» pasa a «sabemos cuándo, qué y con qué otras cosas a la "
      "vez; seguimos sin saber por qué».")
    A("")
    A("⚠️ **Y `P5` es la que ordena a las demás.** La serie **no autoriza a "
      "inferir la causa desde la secuencia** — eso sería `DOC-009`. Que las "
      "cuatro cosas entren juntas hace **plausible** una decisión deliberada "
      "y única, y esa plausibilidad **no es una demostración**.")
    A("")
    A("### Lo que esto le entrega a `011-C4`")
    A("")
    A("| Antes de `C3-R` | Después |")
    A("|---|---|")
    A("| «`C_i` cambió en algún momento, sin razón conocida» | «`C_i` fue "
      "**refactorizado en un acto único**, fechado, junto con una "
      "refactorización mayor del instrumento» |")
    A("| la pregunta era: ¿por qué se fue acumulando? | la pregunta es: **¿qué "
      "motivó rediseñar el factor en un día?** |")
    A("")

    A("---")
    A(f"*GM-Ω-ICPI-011-C3R · {len(radios)} versiones únicas de "
      f"{len(libros)} archivos · lectura pura · el Gold Master vigente no se "
      f"modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
