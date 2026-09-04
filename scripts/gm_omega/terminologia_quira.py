# -*- coding: utf-8 -*-
"""
scripts/gm_omega/terminologia_quira.py — GM-Ω · TERMINOLOGY FREEZE  `T1-T2`

Inventario y clasificación ontológica del vocabulario propio de QUIRA.

    POR QUÉ AHORA. Javo lo planteó y el colega lo formalizó: hemos llegado a un
    punto de madurez donde ya sabemos qué es QUIRA, qué es el Observatorio, qué
    es el Motor, qué es un producto y qué es una capa. Seguir construyendo sobre
    nombres heredados produciría una migración mucho más cara después.

    LA REGLA QUE LO GOBIERNA (`DOC-013`):
        QUIRA no conserva conceptos por herencia; conserva únicamente conceptos
        que cumplen una función verificable en su arquitectura.

    ⚠️ ESTE SCRIPT NO TOCA CÓDIGO. `T1-T5` son inventario, clasificación,
    autoridad, uso y necesidad. `T6` —CONSERVAR / RENOMBRAR / DEPRECAR /
    ELIMINAR / HISTÓRICO— se ejecuta después, y sólo con las decisiones tomadas.
    Primero se estabiliza el vocabulario; después se cambia lo mínimo.

    QUÉ SE MIDE Y QUÉ SE DECLARA, que no es lo mismo:
        · el USO se DERIVA   — en cuántos archivos vive cada nombre, y si cruza
                               a una superficie del producto
        · la CATEGORÍA se DECLARA — es un juicio ontológico con autoridad, no
                               una inferencia desde el patrón de uso (`DOC-009`)

    Y los nombres que se usan pero nadie clasificó emergen solos: son la deuda
    terminológica.

Uso:  python scripts/gm_omega/terminologia_quira.py
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

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_TERMINOLOGIA_T1-T2.md"

# ── LA TAXONOMÍA ─────────────────────────────────────────────────────────────
# El colega propuso seis categorías más una transversal. Al aplicarlas al
# inventario real aparecieron objetos que no encajaban en ninguna —el
# Observatorio no es fuente ni producto; el Gold Master no es evidencia ni
# indicador—, así que la taxonomía se extendió a ocho DECLARANDO la extensión.
#
# ⚠️ Que seis no bastaran es en sí un resultado de T2: la arquitectura real de
# QUIRA tiene más tipos de objeto de los que el primer corte suponía.
_CATEGORIAS = {
    "FUENTE": "origina evidencia — institución o sistema externo",
    "EVIDENCIA": "registro o documento verificable capturado",
    "VARIABLE": "dato operacionalizado que entra en un cálculo",
    "INDICADOR": "medida derivada de variables",
    "ESTADO": "condición epistemológica u operativa del dato",
    "PRODUCTO": "entrega funcional a un usuario",
    "CAPA": "capacidad transversal, no un producto",
    "FUNCIÓN": "actividad de la arquitectura — extensión declarada en T2",
    "ARTEFACTO": "objeto canónico del sistema — extensión declarada en T2",
    "SIN_CATEGORÍA": "⚠️ no responde a «¿qué tipo de objeto QUIRA soy?»",
}

# ── T1/T2/T3 · INVENTARIO CLASIFICADO ────────────────────────────────────────
# (nombre, categoría, autoridad que lo define, nota)
_INVENTARIO = [
    # Identidad
    ("QUIRA", "ARTEFACTO", "identity/CONSTITUCION_INSTITUCIONAL.md",
     "plataforma de inteligencia pública · raíz de la cadena de autoridad"),
    ("Gold Master", "ARTEFACTO", "ADR-023 · METODOLOGIA_GOLD_MASTER.md",
     "fuente canónica de verdad analítica reproducible · NO es «base de datos»"),
    ("Dylus Lab", "ARTEFACTO", "identity/", "el laboratorio que construye QUIRA"),

    # Funciones de adquisición
    ("Observatorio", "FUNCIÓN", "ADR-041 §4",
     "adquisición y monitoreo progresivo de GAD · NO es un producto"),
    ("Ciudadana", "FUNCIÓN", "ADR-041 §4",
     "adquisición de evidencia por control social · NO es el motor"),
    ("Motor", "FUNCIÓN", "H12_MOTOR_ICPI_CANÓNICO · ADR-023",
     "integración, validación y cálculo del Gold Master"),
    ("Consola", "FUNCIÓN", "ADR-042",
     "operación interna: fuentes, conectores, capturas, cobertura · NO es producto"),

    # Productos (ADR-041 §4 sellado)
    ("QUIRA Institucional", "PRODUCTO", "ADR-041 §4", "F2"),
    ("QUIRA Impact", "PRODUCTO", "ADR-041 §4", "F2"),
    ("QUIRA Cooperación", "PRODUCTO", "ADR-041 §4", "F2"),
    ("QUIRA Economic", "PRODUCTO", "ADR-041 §4", "F3"),

    # Capas transversales
    ("QUIRA IA", "CAPA", "ADR-035/037", "IA propone · humano valida"),
    ("GeoTwin", "CAPA", "QTMP", "gemelo territorial"),
    ("SAT", "CAPA", "H21-H24 · SAT_Catalogo",
     "sistema de alertas tempranas · transversal a los índices"),

    # Indicadores
    ("ICPI", "INDICADOR", "tesis (abril 2026) · H12!B33",
     "Índice de Congruencia Programática e Intersistémica · indicador NUCLEAR "
     "del Gold Master, NO «el centro de QUIRA»"),
    ("TGI", "INDICADOR", "01_TGI_FRAMEWORK.md", "índice de gobernanza integral 5D"),
    ("IED", "INDICADOR", "06_IED_DIRECTIVO.md", "Índice de Evaluación Directiva"),
    ("IGP", "INDICADOR", "H20b", "Índice de Gobernanza Participativa · ver D-010"),
    ("MMP", "INDICADOR", "08_MMP_MENSUAL.md", "monitoreo mensual"),

    # Variables del ICPI
    ("P_i", "VARIABLE", "tesis · H14!G", "coeficiente de peso presupuestario"),
    ("R_i", "VARIABLE", "tesis · H14!F", "coeficiente de relevancia normativa"),
    ("V_i", "VARIABLE", "tesis · H13!F", "verificación intersistémica"),
    ("E_i", "VARIABLE", "⚠️ NOT_DETERMINABLE (007-B0)",
     "regla generadora no reconstruible desde el material conservado"),
    ("T_i", "VARIABLE", "H07b!fila 20", "materialización temporal"),
    ("C_i", "VARIABLE", "H01 TBL_CALIBRACION_Ci", "trazabilidad orgánica"),

    # Estados
    ("NOT_DETERMINABLE", "ESTADO", "Constitución CAPA 0", "no se pudo reconstruir"),
    ("UNTRACEABLE", "ESTADO", "GM-Ω taxonomía", "sin fuente tras agotar la búsqueda"),
    ("TEMPORAL_SEMANTIC_GAP", "ESTADO", "GM-Ω taxonomía",
     "la fuente existe pero su período o función no está bien declarado"),

    # Fuentes institucionales (ADR-029)
    ("SERCOP", "FUENTE", "LOSNCP", "contratación pública"),
    ("eSIGEF", "FUENTE", "COPFP · MEF", "ejecución presupuestaria"),
    ("LOTAIP", "FUENTE", "LOTAIP Art. 7", "transparencia"),
    ("CPCCS", "FUENTE", "LOPC Art. 88", "rendición de cuentas"),
    ("SIGAD", "FUENTE", "SENPLADES", "autorreporte del GAD"),
    ("PDOT", "EVIDENCIA", "COOTAD · COPFP Art. 41",
     "documento oficial y vinculante del mandato"),

    # ⚠️ El caso que abrió todo esto
    ("AVEP", "SIN_CATEGORÍA", "⚠️ ninguna autoridad vigente lo define",
     "no es indicador, ni fuente, ni variable, ni estado, ni producto, ni capa. "
     "Nació como nombre de un eje conceptual, derivó a fórmula copiada en 11 "
     "hojas, y hoy existen DOS versiones incompatibles (D-012)"),
]

# Nombres que NO son vocabulario de QUIRA: son normas e instituciones externas.
# Se excluyen del rastreo de huérfanos para que no inflen la deuda terminológica.
_EXTERNOS = {
    "COOTAD", "COPFP", "LOSEP", "LOSNCP", "LOPC", "CGE", "MEF", "MIES", "MIDUVI",
    "INPC", "ODS", "CAF", "BID", "GIZ", "IVA", "PAC", "POA", "PUGS", "NBI",
    "CNE", "SENPLADES", "GAD", "EP", "URL", "PDF", "JSON", "CSV", "API", "SHA",
    "UUID", "HTML", "CI", "OK", "ID", "IP", "UI", "SQL", "MCP", "ADR", "PCD",
    "GADM", "USD", "INEC", "PNUD", "USAID", "BEI", "SETEPLAN", "SNP",
}

# Palabras españolas y marcadores que el detector de siglas confunde con
# nombres propios por estar en mayúsculas (títulos, encabezados, énfasis).
# ⚠️ La lista se DECLARA porque es un juicio: sin ella la deuda terminológica
# aparecía inflada con «ANTES», «META» o «ALTA», que no son nombres de nada.
_RUIDO = {
    "ALERTA", "ALTA", "ANTES", "CAPA", "META", "EJE", "MIN", "MAX", "SIN", "CON",
    "PROG", "III", "IIII", "ENGINE", "TOTAL", "NOTA", "REGLA", "FASE", "ESTADO",
    "TIPO", "NIVEL", "AHORA", "TODO", "DEBE", "PARA", "POR", "QUE", "DEL", "LAS",
    "LOS", "UNA", "SOLO", "MÁS", "ESTE", "ESTA", "SER", "HAY", "NUEVO", "AÑO",
    # `CORE` es el directorio del canon (`00_CORE`), no una sigla. Lo cazaba el
    # detector de siglas normativas mal formadas como si fuera «CRE» —el falso
    # positivo enseñó que la distancia de edición necesita un ancla de contexto.
    "CORE",
}


def _archivos_del_repo() -> list[Path]:
    """Sólo lo rastreado y vivo: sin worktrees, sin caché, sin deprecados."""
    out = []
    for p in _RAIZ.rglob("*"):
        if not p.is_file() or p.suffix not in (".py", ".md", ".yaml", ".yml"):
            continue
        partes = set(p.parts)
        if partes & {".git", "__pycache__", ".claude", "_deprecated", "historico"}:
            continue
        out.append(p)
    return out


_SUPERFICIES = ("quira_pages", "components", "views")


def medir_uso(nombre: str, archivos: list[Path]) -> dict:
    """DERIVADO: en cuántos archivos vive el nombre y si cruza al producto.

    Se busca con límite de palabra para que `EP` no case dentro de `eSIGEF` ni
    `SAT` dentro de `SATISFACTORIO`."""
    patron = re.compile(rf"(?<![\w_]){re.escape(nombre)}(?![\w_])")
    en, superficie = [], []
    for p in archivos:
        try:
            if patron.search(p.read_text(encoding="utf-8", errors="replace")):
                rel = p.relative_to(_RAIZ).as_posix()
                en.append(rel)
                if rel.split("/")[0] in _SUPERFICIES:
                    superficie.append(rel)
        except OSError:
            continue
    return {"archivos": len(en), "superficies": len(superficie),
            "ejemplos": sorted(superficie)[:3]}


def huerfanos(archivos: list[Path], clasificados: set[str]) -> list[tuple[str, int]]:
    """T1 · siglas propias que se usan y NADIE clasificó.

    Es la pregunta del colega vuelta prueba: todo nombre del repositorio debería
    poder responder «¿qué tipo de objeto QUIRA soy?». El que no puede es deuda
    terminológica."""
    cuenta: dict[str, int] = {}
    canon = [p for p in archivos
             if "corpus_obsidian" in p.parts or p.name in ("config.py", "BOOT.md")]
    for p in canon:
        txt = p.read_text(encoding="utf-8", errors="replace")
        for sigla in set(re.findall(r"(?<![\w_])([A-Z]{3,8})(?![\w_])", txt)):
            if sigla in _EXTERNOS or sigla in _RUIDO or sigla in clasificados:
                continue
            cuenta[sigla] = cuenta.get(sigla, 0) + 1
    return sorted(cuenta.items(), key=lambda kv: -kv[1])[:25]


_NORMAS = ("COOTAD", "COPFP", "LOSEP", "LOSNCP", "LOPC", "LOTAIP", "CRE")


def _dist1(a: str, b: str) -> bool:
    """¿`a` se obtiene de `b` quitando o cambiando un carácter? Suficiente para
    cazar siglas normativas mal formadas sin traer una librería."""
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    corta, larga = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(larga)):
        if larga[:i] + larga[i + 1:] == corta:
            return True
    return False


def siglas_normativas_mal_formadas(sueltos) -> list[tuple[str, str, int]]:
    """⚠️ Un hallazgo que el inventario produce de propina.

    La Regla de Oro 3 prohíbe citar normas sin verificar. Una sigla normativa a
    un carácter de la correcta —`CPFP` por `COPFP`— es una cita que no resuelve,
    y ninguna revisión de contenido la ve porque «parece» un código legal."""
    return [(s, n_, c) for s, c in sueltos for n_ in _NORMAS if _dist1(s, n_)]


def main() -> int:
    archivos = _archivos_del_repo()
    print(f"inventario sobre {len(archivos)} archivos vivos")

    filas = []
    for nombre, cat, autoridad, nota in _INVENTARIO:
        filas.append({"nombre": nombre, "cat": cat, "autoridad": autoridad,
                      "nota": nota, **medir_uso(nombre, archivos)})

    clasificados = {f["nombre"] for f in filas} | {
        n.split()[-1] for n in (f["nombre"] for f in filas) if " " in n}
    sueltos = huerfanos(archivos, clasificados)

    sin_cat = [f for f in filas if f["cat"] == "SIN_CATEGORÍA"]
    sin_uso = [f for f in filas if f["archivos"] == 0]
    print(f"clasificados: {len(filas)} · sin categoría: {len(sin_cat)} · "
          f"sin uso: {len(sin_uso)} · huérfanos frecuentes: {len(sueltos)}")

    _escribir(filas, sueltos, sin_cat, sin_uso)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(filas, sueltos, sin_cat, sin_uso) -> None:
    o: list[str] = []
    A = o.append

    A("# GM-Ω · TERMINOLOGY FREEZE — INVENTARIO Y CLASIFICACIÓN  `T1-T2`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/terminologia_quira.py`.")
    A("")
    A("> ### ⚠️ ESTA ETAPA NO TOCA CÓDIGO")
    A("> `T1` inventario · `T2` clasificación · `T3` autoridad · `T4` uso · "
      "`T5` necesidad. La acción —`T6`: CONSERVAR / RENOMBRAR / DEPRECAR / "
      "ELIMINAR / HISTÓRICO— se ejecuta **después**, y sólo con las decisiones "
      "tomadas. **Primero se estabiliza el vocabulario; después se cambia lo "
      "mínimo.** Cambiar código ahora sería la misma prisa que produjo el "
      "problema que este documento inventaria.")
    A("")
    A("> ### La regla que lo gobierna · `DOC-013`")
    A("> **QUIRA no conserva conceptos por herencia; conserva únicamente "
      "conceptos que cumplen una función verificable en su arquitectura.**")
    A(">")
    A("> Es la regla de Javo —*«si no aporta a QUIRA, sólo infla»*— elevada de "
      "criterio de canon a **higiene ontológica de toda la arquitectura**. Y "
      "tiene una salvaguarda que la separa de la destrucción de evidencia: "
      "**un concepto puede morir como componente activo sin desaparecer de la "
      "historia de QUIRA.**")
    A("")
    A("## Qué se mide y qué se declara")
    A("")
    A("| | |")
    A("|---|---|")
    A("| **USO** — en cuántos archivos vive, si cruza al producto | **derivado** |")
    A("| **CATEGORÍA** — qué tipo de objeto es | **declarado**: es un juicio "
      "ontológico con autoridad, no una inferencia desde el patrón de uso "
      "(`DOC-009`) |")
    A("")
    A("## La taxonomía")
    A("")
    A("| Categoría | Qué es |")
    A("|---|---|")
    for cat, desc in _CATEGORIAS.items():
        A(f"| **{cat}** | {desc} |")
    A("")
    A("⚠️ **La propuesta original tenía seis categorías más una transversal, y "
      "no bastaron.** El Observatorio no es fuente ni producto; el Gold Master "
      "no es evidencia ni indicador. Se extendió a `FUNCIÓN` y `ARTEFACTO` "
      "**declarando la extensión** — y que hicieran falta es en sí un resultado "
      "de `T2`: la arquitectura real de QUIRA tiene más tipos de objeto de los "
      "que el primer corte suponía.")
    A("")

    A("## T1-T4 · Inventario clasificado")
    A("")
    A("| Nombre | Categoría | Autoridad que lo define | Archivos | En producto |")
    A("|---|---|---|---:|---:|")
    orden = {c: i for i, c in enumerate(_CATEGORIAS)}
    for f in sorted(filas, key=lambda x: (orden.get(x["cat"], 99), -x["archivos"])):
        marca = " ⚠️" if f["cat"] == "SIN_CATEGORÍA" else ""
        sup = f"{f['superficies']}" if f["superficies"] else "—"
        A(f"| `{f['nombre']}`{marca} | {f['cat']} | {f['autoridad']} | "
          f"{f['archivos']} | {sup} |")
    A("")
    A("**«En producto»** cuenta archivos de `quira_pages/`, `components/` y "
      "`views/`. Un nombre interno con presencia ahí es candidato a revisión por "
      "Bloomberg Firewall — pero **no automáticamente una infracción**: puede "
      "aparecer en un comentario o en una clave de datos que nunca se pinta.")
    A("")

    if sin_cat:
        A("## T5 · ⚠️ Nombres que no responden a la pregunta")
        A("")
        A("> *¿Qué tipo de objeto QUIRA soy?*")
        A("")
        for f in sin_cat:
            A(f"### `{f['nombre']}`")
            A("")
            A(f"{f['nota']}")
            A("")
            A(f"Vive en **{f['archivos']} archivos**"
              + (f", de los cuales **{f['superficies']} son superficies del "
                 f"producto** (" + ", ".join(f"`{e}`" for e in f["ejemplos"]) + ")"
                 if f["superficies"] else ", ninguno en superficies del producto")
              + ".")
            A("")
            A("**Que se haya propagado no demuestra que deba existir: demuestra "
              "que se propagó.** Y ésa es exactamente la distinción que `DOC-013` "
              "introduce.")
            A("")

    if sueltos:
        A("## T1 · Siglas propias en uso que nadie clasificó")
        A("")
        A("Detectadas en canon, `config.py` y `BOOT.md`, excluidas las normas e "
          "instituciones externas. **No son necesariamente deuda** —muchas serán "
          "hojas del Gold Master o nombres legítimos aún sin ficha—, pero cada "
          "una debería poder responder a qué tipo de objeto pertenece.")
        A("")
        A("| Sigla | Archivos de canon donde aparece |")
        A("|---|---:|")
        for sigla, n in sueltos:
            A(f"| `{sigla}` | {n} |")
        A("")

    malf = siglas_normativas_mal_formadas(sueltos)
    if malf:
        A("## ⚠️ Hallazgo de propina · siglas normativas mal formadas")
        A("")
        A("La **Regla de Oro 3** prohíbe citar normas sin verificar. Una sigla a "
          "un solo carácter de la correcta es una cita que **no resuelve**, y "
          "ninguna revisión de contenido la ve: «parece» un código legal.")
        A("")
        A("| Sigla en uso | Probablemente | Archivos |")
        A("|---|---|---:|")
        for s, correcta, c in malf:
            A(f"| `{s}` | `{correcta}` | {c} |")
        A("")
        A("Lo detectó el inventario terminológico, no una revisión normativa — "
          "que es precisamente el argumento a favor de hacer este ejercicio. "
          "**Verificar dónde vive cada una antes de corregir**: una aparición en "
          "un backup del vault no es lo mismo que una en el canon vivo o en una "
          "cita publicada.")
        A("")

    A("## Lo que este documento NO decide")
    A("")
    A("- **No renombra nada.** `ICPI` sigue siendo *Índice de Congruencia "
      "Programática e Intersistémica*: es el nombre de la tesis, el documento "
      "con fecha anterior a todo Gold Master conservado, y **el único anclaje "
      "documental verificable que tiene el constructo**. Renombrarlo destruiría "
      "la genealogía que `001-007` reconstruyó.")
    A("- **No elimina AVEP.** Propone su categoría y mide su uso. La decisión "
      "—deprecar del runtime conservando la genealogía histórica— es de `T6`, "
      "y sólo después de que `011` dictamine si QUIRA necesita interpretar "
      "porcentajes mediante categorías para entregar su producto.")
    A("- **No construye el baremo parametrizable.** La arquitectura "
      "`país · institución · versión · constructo · umbrales · etiquetas · "
      "fundamento · vigencia` es un **patrón metodológico disponible**, no un "
      "componente obligatorio. Construirlo antes de saber si hace falta sería "
      "infringir `DOC-013` en el mismo documento que lo declara.")
    A("")
    A("---")
    A(f"*GM-Ω · Terminology Freeze T1-T2 · {len(filas)} nombres clasificados · "
      "ningún código modificado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
