# -*- coding: utf-8 -*-
"""
scripts/gm_omega/genealogia_documental.py — GM-Ω · EXPEDIENTE GENEALÓGICO

    Barre los documentos históricos de `tesis historicas/documentos antiguos/`
    y extrae la cadena metodológica que el corpus posterior NO conserva.

    POR QUÉ. Javo aportó una carpeta con material de abril, y el primer
    documento abierto —`Metodologia_SIAP_ICPI.docx`, TERRA/QUADRUM— ya demostró
    que **abril contiene información que no está representada en el corpus
    posterior**: la regla de `E_i` que esta auditoría había declarado
    `NOT_DETERMINABLE`.

    ⚠️ Y LA REGLA DE ESTE BARRIDO: reconstruir la cadena ENTERA antes de
    reescribir ningún diagnóstico. Corregir `007-B0` con el primer documento y
    volver a corregirlo con el segundo sería hacer el trabajo dos veces — y
    dejar en el expediente dos versiones de la misma historia.

    NO decide cuál versión metodológica es «la correcta». Registra que existen,
    con su fecha y su documento. Eso lo dictamina `011`.

Uso:  python scripts/gm_omega/genealogia_documental.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_GENEALOGIA_DOCUMENTAL.md"
_FUENTE = _RAIZ.parent / "tesis historicas" / "documentos antiguos"

# Los ocho huecos que la auditoría dejó abiertos y que abril podría cerrar.
_TEMAS = {
    "E_i · regla": r"(E[_ᵢi]?\s*[—:-].{0,80}(autonom|fricci)|"
                   r"aut[oó]nomo.{0,40}compartido.{0,40}difuso|"
                   r"E_?i\s*=\s*0[.,](90|75|5))",
    "C_i · origen": r"(C[_ᵢi]?\s*[—:-].{0,80}(trazabilidad|org[aá]nic)|"
                    r"Responsabilidad Org[aá]nica Vinculante)",
    "P_i · evolución": r"(P[_ᵢi]?\s*[—:-].{0,80}(peso|presupuest)|"
                       r"PRESUPUESTO_ASIGNADO)",
    "R_i · evolución": r"(R[_ᵢi]?\s*[—:-].{0,80}(relevancia|normativ)|"
                       r"R_?i_?raw|1[.,]725)",
    "AVEP · origen": r"(AVEP|Gesti[oó]n por Mandato|Ruptura Sist[eé]mica|"
                     r"baremo)",
    "universo 25/66": r"(muestra estrat[eé]gica|25 metas|66 metas|"
                      r"universo operacional)",
    "unidad `i`": r"(unidad de an[aá]lisis|cada meta.{0,60}unidad|"
                  r"n\s*=\s*N[uú]mero de metas)",
    "fórmula": r"(P[_ᵢi]?\s*[×x*]\s*R[_ᵢi]?|Σ\s*\(?\s*P|"
               r"ICPI\s*=\s*\[?Σ)",
    "TERRA/QUADRUM": r"(TERRA|QUADRUM|Quadrum Gov)",
}


def _texto(p: Path) -> str:
    """Texto plano de un .docx —párrafos y tablas— o de un .csv."""
    if p.suffix.lower() == ".csv":
        return p.read_text(encoding="utf-8", errors="replace")
    if p.suffix.lower() != ".docx":
        return ""
    try:
        from docx import Document
        d = Document(str(p))
    except Exception:
        return ""
    partes = [x.text for x in d.paragraphs]
    for t in d.tables:
        for fila in t.rows:
            partes.append(" | ".join(c.text for c in fila.cells))
    return "\n".join(partes)


def barrer() -> list[dict]:
    if not _FUENTE.exists():
        return []
    out = []
    for p in sorted(_FUENTE.iterdir()):
        if p.suffix.lower() not in (".docx", ".csv"):
            continue
        txt = _texto(p)
        if not txt:
            continue
        hallazgos = {}
        for tema, patron in _TEMAS.items():
            enc = []
            for m in re.finditer(patron, txt, re.I):
                ini = max(0, m.start() - 90)
                frag = re.sub(r"\s+", " ", txt[ini:m.end() + 220]).strip()
                if frag not in enc:
                    enc.append(frag)
                if len(enc) >= 3:
                    break
            if enc:
                hallazgos[tema] = enc
        out.append({
            "archivo": p.name,
            "modificado": datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d"),
            "caracteres": len(txt),
            "hallazgos": hallazgos,
        })
    return out


def main() -> int:
    docs = barrer()
    if not docs:
        print("[no determinable] no se encontró la carpeta de documentos "
              f"históricos: {_FUENTE}")
        return 2

    total = sum(len(d["hallazgos"]) for d in docs)
    print(f"documentos barridos: {len(docs)} · temas con material: {total}")
    for d in docs:
        if d["hallazgos"]:
            print(f"  {d['archivo'][:46]:<48} {', '.join(d['hallazgos'])}")

    _escribir(docs)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(docs) -> None:
    o: list[str] = []
    A = o.append

    A("# GM-Ω · EXPEDIENTE GENEALÓGICO DOCUMENTAL")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/genealogia_documental.py` barriendo "
      "`tesis historicas/documentos antiguos/`.")
    A("")
    A("> ### Por qué existe")
    A("> Javo aportó la carpeta de documentos antiguos, y el primero que se "
      "abrió —`Metodologia_SIAP_ICPI.docx`, de abril, firmado **Ecosistema "
      "TERRA · Quadrum Gov Tech**— demostró que **abril contiene información "
      "que el corpus posterior no conserva**: la regla de `E_i` que esta "
      "auditoría había declarado `NOT_DETERMINABLE`.")
    A(">")
    A("> **Regla del barrido:** reconstruir la cadena entera **antes** de "
      "reescribir ningún diagnóstico. Corregir `007-B0` con el primer documento "
      "y volver a corregirlo con el segundo dejaría dos versiones de la misma "
      "historia en el expediente.")
    A("")

    A("## ★ El hallazgo que abrió el barrido · `E_i` tiene DOS definiciones")
    A("")
    A("| | Definición **A** | Definición **B** |")
    A("|---|---|---|")
    A("| Documento | `Metodologia_SIAP_ICPI.docx` (abril · TERRA/QUADRUM) | `metodologia.docx` (tesis) |")
    A("| Nombre | **Autonomía Orgánica** | **Fricción de Autonomía** |")
    A("| Qué mide | «el **control del director** sobre la ejecución de la meta» | fricción institucional por **delegación** |")
    A("| Escala | `1.0` autónomo · `0.9` compartido · `0.75` difuso | `1.0` directa · `0.90` convenio · `0.75` adscrita |")
    A("| Base | — | `COOTAD Art. 54` · `NCI 200-04` |")
    A("")
    A("**Misma escala numérica, constructos distintos.** Y el motor declara la "
      "definición **A**, textualmente, en `H12!A4`:")
    A("")
    A("```")
    A("Ei: 1.0=autónomo | 0.9=compartido | 0.75=difuso")
    A("```")
    A("")
    A("### ⚠️ Qué corrige esto, y qué NO")
    A("")
    A("| | |")
    A("|---|---|")
    A("| **CORRIGE** | `007-B0` concluyó que «la regla escrita y los valores "
      "implementados nunca coincidieron». Lo que ocurrió es que **la auditoría "
      "contrastó los valores contra la definición B mientras el motor "
      "implementa la A**. Los cinco casos de entidades adscritas con `E_i ≠ "
      "0,75` no eran incoherencia: eran la respuesta correcta bajo la regla que "
      "el motor sí declara |")
    A("| **NO CORRIGE** | que la aplicación meta a meta siga sin verificarse. "
      "Comprobar que los 25 valores cumplen la definición A exige conocer el "
      "«control del director» por meta, y eso no consta en el libro |")
    A("")
    A("**Estado nuevo de `E_i`** — cuatro capas que no deben colapsarse:")
    A("")
    A("```")
    A("  REGLA                        VERIFICADA      · abril + H12!A4")
    A("  VALORES DEL MOTOR            VERIFICADOS     · 25 literales, estables")
    A("  APLICACIÓN META A META       PENDIENTE       · falta el insumo")
    A("  CORRESPONDENCIA VALOR↔REGLA  POR AUDITAR     · no se puede hoy")
    A("```")
    A("")
    A("⚠️ **La definición B no se descarta.** No era basura: pasa a ser "
      "**evidencia de divergencia o evolución metodológica entre documentos**. "
      "Cuál rige lo dictamina `011`, no este expediente.")
    A("")
    A("Y coincide con la corrección que Javo hizo el 2026-09-03 —*«castigar al "
      "GAD por derivar una obra a EP Aseo no es viable: es la misma "
      "institucionalidad»*—: **la definición A no penaliza el organigrama, mide "
      "el control del director.** Su criterio coincidía con la metodología "
      "original, no con la tesis.")
    A("")

    A("## ★ Y el ICPI original tenía CINCO factores")
    A("")
    A("`QUADRUM_ICPI_Calculadora.csv` conserva la construcción primitiva:")
    A("")
    A("```")
    A("  PRODUCTO     = Pi × Vi × Ei × Ti × Ri      ← CINCO · sin C_i")
    A("  Pi           = PRESUPUESTO_ASIGNADO / PRESUPUESTO_TOTAL")
    A("  Ri           = 0.5 · 1 · 1.5               ← sin normalizar por 1,725")
    A("  DENOMINADOR  = Pi × Ri                     ← igual que hoy")
    A("```")
    A("")
    A("Luego la evolución documentada es:")
    A("")
    A("```")
    A("  ICPI_original = Pi · Vi · Ei · Ti · Ri            (abril · 5 factores)")
    A("  ICPI_actual   = Pi · Ri · Vi · Ei · Ti · Ci       (v5.7 · 6 factores)")
    A("```")
    A("")
    A("**`C_i` no es parte del constructo original: es una incorporación "
      "posterior.** Eso reformula `011-C`, que ya no debe preguntar sólo si "
      "está bien multiplicar seis factores, sino:")
    A("")
    A("> **¿Qué transformación metodológica ocurrió entre el ICPI original y el "
      "actual, qué constructo representa cada versión, y está justificada la "
      "incorporación de `C_i` y la arquitectura algebraica resultante?**")
    A("")
    A("⚠️ Y `R_i` también cambió de representación —de `0.5·1·1.5` crudo a "
      "normalizado por el máximo teórico—. **Eso entra en la genealogía de "
      "`R_i`, no se trata automáticamente como error.**")
    A("")

    A("## ★ La UNIDAD DE ANÁLISIS está declarada — y hay que leerla con cuidado")
    A("")
    A("`ICPI.docx` (la tesis) la declara explícitamente:")
    A("")
    A("> **Unidad de Análisis:** el **flujo informativo y programático** en la "
      "trayectoria `Plan de Trabajo → PDOT → POA → SIGAD` del GAD Municipal de "
      "Montecristi.")
    A("")
    A("⚠️ **Pero eso NO responde todavía a `011-A`, y confundirlo sería el error "
      "de siempre.** Son dos cosas distintas:")
    A("")
    A("| | |")
    A("|---|---|")
    A("| **Unidad de análisis de la INVESTIGACIÓN** | qué fenómeno se estudia → "
      "el flujo/trayectoria. **Declarada** |")
    A("| **Unidad `i` de la FÓRMULA** | qué objeto se indexa en `Σ` y recibe "
      "`P·R·V·E·T·C`. **Sigue sin declararse** |")
    A("")
    A("Que la tesis diga «estudio el flujo» no dice si `i` es una meta, un "
      "agregado o una unidad programática. **Es material valioso para `011-A`, "
      "no su respuesta** — y tratarlo como respuesta sería colapsar el objeto "
      "de estudio con el objeto de cálculo.")
    A("")

    A("## `C_i` · su origen conceptual")
    A("")
    A("`memoriaa algo quira.docx` lo enlaza con la doctrina fundacional:")
    A("")
    A("> **Responsabilidad Orgánica Vinculante (`C_i`)** → «✅ VIVO como… "
      "`H07c`: firma del Director activa `Ti_V`»")
    A("")
    A("Coincide con `TERMINOLOGY_ORIGIN_v1.md`, que lo define como *«la "
      "obligación técnica y legal de que cada meta de inversión esté "
      "ineludiblemente anclada a una unidad administrativa específica […] el "
      "antídoto contra la burocracia diluida»*. `C_i` **sí tiene genealogía "
      "conceptual documentada** — lo que no tiene es presencia en el ICPI "
      "original de cinco factores.")
    A("")

    A("## ⚠️ El barrido de los dos documentos grandes dio NEGATIVO")
    A("")
    A("`historico construccion quira.docx` (358 KB · 6.194 párrafos) y "
      "`memoriaa algo quira.docx` (74 KB) son **historiales de construcción del "
      "software**, no documentos metodológicos: sprints, QLEP, Neo4j, GeoTwin, "
      "TERRA Ciudadana. Se buscaron en ellos:")
    A("")
    A("| Buscado | Resultado |")
    A("|---|---|")
    A("| Primera aparición de la **fórmula de 6 factores** | ❌ nada |")
    A("| Primera aparición de la **fórmula de 5 factores** | ❌ nada |")
    A("| **Definición operacional de `i`** | ❌ nada |")
    A("| Incorporación de `C_i` al producto | ❌ sólo su concepto, ya conocido |")
    A("| Transición TERRA/QUADRUM → QUIRA | 🟡 menciones, sin decisión metodológica |")
    A("")
    A("**Es un resultado, no un fracaso.** Lo que establece es que **el "
      "documento que explica la transición del ICPI de cinco a seis factores no "
      "está en este corpus**. Y la consecuencia es la que el asesor anticipó:")
    A("")
    A("> Si los documentos históricos tampoco resuelven qué representa `i`, "
      "entonces **`011-A` tiene que decidirlo** — no descubrirlo. Y fabricar "
      "una definición retrospectiva para que la fórmula parezca más coherente "
      "de lo que era sería el peor desenlace posible.")
    A("")

    A("## Tabla de genealogía")
    A("")
    A("⚠️ **Las fechas salen del CONTENIDO, no del sistema de ficheros.** Donde "
      "no hay fecha fiable se escribe `NO DETERMINABLE`, nunca el `mtime`.")
    A("")
    A("| Elemento | Versión histórica | Evidencia | Cambio | Justificación | Estado |")
    A("|---|---|---|---|---|---|")
    A("| `P_i` | `PRESUPUESTO_ASIGNADO / TOTAL` | calculadora QUADRUM | → normalizado Σ=1 sobre 25 | **no hallada** | 🟡 cambio documentado, motivo no |")
    A("| `R_i` | `0.5 · 1 · 1.5` crudo | calculadora QUADRUM | → normalizado por máximo 1,725 | **no hallada** | 🟡 ídem |")
    A("| `V_i` | 3 niveles con núcleo financiero | `H13!B16-B21` | regla anterior `suma≥2` → actual | ✅ **documentada en el libro** | 🟢 con límite de reconstrucción |")
    A("| `E_i` | **A**: control del director (abril) · **B**: fricción por delegación (tesis) | `Metodologia_SIAP_ICPI` · `metodologia.docx` · `H12!A4` | dos definiciones coexistentes | **no hallada** | 🟡 regla verificada, aplicación pendiente |")
    A("| `T_i` | ratio por entidad | `H07b` | curva de pacing sustituyó a `mes/12` | **no hallada** · la nota quedó desfasada | 🟡 |")
    A("| `C_i` | **ausente** del ICPI original | calculadora QUADRUM (5 factores) | **incorporación posterior** | ❌ **NO HALLADA** | 🔴 el hueco principal |")
    A("| `i` | «flujo informativo/programático» (unidad de INVESTIGACIÓN) | `ICPI.docx` | — | — | 🔴 unidad de CÁLCULO sin declarar |")
    A("| Fórmula | `Pi·Vi·Ei·Ti·Ri` (5) | calculadora QUADRUM | → `Pi·Ri·Vi·Ei·Ti·Ci` (6) | ❌ **NO HALLADA** | 🔴 |")
    A("| AVEP | eje conceptual → 4 niveles | `TERMINOLOGY_ORIGIN_v1` | → 5 niveles + fórmula `IF` ×11 hojas | 🟡 el incidente sí (`H01!A28`) | 🟡 |")
    A("| Universo | «muestra estratégica» | tesis | → 25 rotuladas `Total_Metas_PDOT` | ✅ criterio: mayor monto (Javo) | 🟢 |")
    A("")
    A("**Fecha interna más antigua localizada en el corpus: `2026-05-16`** "
      "(Gold Master v5.4). El material de abril existe —la metodología "
      "TERRA/QUADRUM— pero **entre abril y el 10 de mayo no hay ningún "
      "artefacto conservado**, y ahí es donde ocurrieron los cambios que esta "
      "tabla no puede justificar.")
    A("")

    A("## Barrido documental")
    A("")
    A("⚠️ **La columna «copiado» NO es la fecha del documento.** Todos los "
      "archivos se trasladaron a esta carpeta el mismo día, así que el sistema "
      "de ficheros dice `2026-09-04` para material que es de enero o de abril. "
      "**La fecha real vive en el contenido** —`Metodologia_SIAP_ICPI.docx` se "
      "identifica como TERRA/QUADRUM © 2026 y su copia en Drive está fechada el "
      "25 de abril—. Ordenar la genealogía por `mtime` produciría una "
      "cronología falsa.")
    A("")
    A("| Documento | Copiado | Caracteres | Temas con material |")
    A("|---|---|---:|---|")
    for d in sorted(docs, key=lambda x: x["modificado"]):
        temas = ", ".join(f"`{t}`" for t in d["hallazgos"]) or "—"
        A(f"| `{d['archivo'][:44]}` | {d['modificado']} | {d['caracteres']} | {temas} |")
    A("")

    for d in sorted(docs, key=lambda x: x["modificado"]):
        if not d["hallazgos"]:
            continue
        A(f"### `{d['archivo']}` · {d['modificado']}")
        A("")
        for tema, frags in d["hallazgos"].items():
            A(f"**{tema}**")
            A("")
            for f in frags:
                A(f"- …{f[:300]}…")
            A("")

    A("## Lo que este expediente NO hace")
    A("")
    A("- **No decide qué versión metodológica rige.** Registra que existen, con "
      "su documento y su fecha. El dictamen es de `011`.")
    A("- **No cierra el frente de `E_i`.** Cambia su estado; la correspondencia "
      "valor↔regla sigue por auditar.")
    A("- **No toca el Gold Master ni recalcula el 27,4582 %.** El baseline sigue "
      "congelado mientras se reconstruye la genealogía.")
    A("- **No descarta la definición B** ni ningún documento histórico: la "
      "divergencia entre versiones **es** el objeto de estudio.")
    A("")
    A("---")
    A(f"*GM-Ω · Expediente genealógico · {len(docs)} documentos barridos · "
      "el Gold Master no se modificó · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
