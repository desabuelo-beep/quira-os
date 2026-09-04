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

# ── LA SEGUNDA DIMENSIÓN · CAPA DE PRESENTACIÓN ───────────────────────────────────────
# Un nombre no se define sólo por QUÉ ES, sino por EN QUÉ CAPA debe ser visible.
# Sin esta dimensión el inventario obliga a una decisión binaria —publicar o
# esconder— y la respuesta correcta casi nunca es binaria.
#
# ⚠️ Y NO ES UN FILTRO DE PUBLICACIÓN. Javo corrigió el supuesto: **los índices
# están construidos para aparecer en el dominio que los representa**; esa
# decisión ya la tomó la arquitectura de dominios y no se relitiga aquí. Lo que
# esta dimensión decide es en qué CAPA DE LECTURA aparece cada nombre dentro de
# su dominio — no si el índice se publica.
_CAPA_PRESENTACION = {
    "PÚBLICO": "lenguaje de administración pública · primera capa de lectura",
    "INSTITUCIONAL": "ficha metodológica · segunda capa, al abrir el indicador",
    "TÉCNICO": "trazabilidad forense · tercera capa, usuario institucional",
    "INTERNO": "no cruza al producto (Regla de Oro 2)",
    "HISTÓRICO": "conservado por genealogía · fuera del runtime",
}

# ── T1/T2/T3 · INVENTARIO CLASIFICADO ────────────────────────────────────────
# (nombre, categoría, autoridad que lo define, visibilidad, nota)
_INVENTARIO = [
    # Identidad
    ("QUIRA", "ARTEFACTO", "identity/CONSTITUCION_INSTITUCIONAL.md",
     "PÚBLICO",
     "plataforma de inteligencia pública · raíz de la cadena de autoridad"),
    ("Gold Master", "ARTEFACTO", "ADR-023 · METODOLOGIA_GOLD_MASTER.md",
     "TÉCNICO",
     "fuente canónica de verdad analítica reproducible · NO es «base de datos»"),
    ("Dylus Lab", "ARTEFACTO", "identity/",
     "PÚBLICO", "el laboratorio que construye QUIRA"),
    # ⚠️ El huérfano nº 2 del primer inventario (23 apariciones), resuelto por
    # Javo — y con la MISMA deriva que AVEP: la sigla sobrevivió, el nombre
    # completo divergió. Las tesis lo expanden de dos maneras incompatibles.
    ("SIAP", "ARTEFACTO", "tesis · da nombre al Gold Master",
     "HISTÓRICO",
     "⚠️ DOS expansiones: «Sistema de Integridad Algorítmica Preventiva» "
     "(tesis antigua) y «Sistema Integral de Auditoría y Planificación» "
     "(borrador inicial). Sistema antecesor de QUIRA · sobrevive en el nombre "
     "del archivo `SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx`"),

    # Funciones de adquisición
    ("Observatorio", "FUNCIÓN", "ADR-041 §4",
     "PÚBLICO",
     "adquisición y monitoreo progresivo de GAD · NO es un producto"),
    ("Ciudadana", "FUNCIÓN", "ADR-041 §4",
     "PÚBLICO",
     "adquisición de evidencia por control social · NO es el motor"),
    ("Motor", "FUNCIÓN", "H12_MOTOR_ICPI_CANÓNICO · ADR-023",
     "TÉCNICO",
     "integración, validación y cálculo del Gold Master"),
    ("Consola", "FUNCIÓN", "ADR-042",
     "INTERNO",
     "operación interna: fuentes, conectores, capturas, cobertura · NO es producto"),

    # Productos (ADR-041 §4 sellado)
    ("QUIRA Institucional", "PRODUCTO", "ADR-041 §4",
     "PÚBLICO", "F2"),
    ("QUIRA Impact", "PRODUCTO", "ADR-041 §4",
     "PÚBLICO", "F2"),
    ("QUIRA Cooperación", "PRODUCTO", "ADR-041 §4",
     "PÚBLICO", "F2"),
    ("QUIRA Economic", "PRODUCTO", "ADR-041 §4",
     "PÚBLICO", "F3"),

    # Capas transversales
    ("QUIRA IA", "CAPA", "ADR-035/037",
     "PÚBLICO", "IA propone · humano valida"),
    ("GeoTwin", "CAPA", "QTMP",
     "PÚBLICO", "gemelo territorial"),
    ("SAT", "CAPA", "H21-H24 · SAT_Catalogo",
     "INTERNO",
     "sistema de alertas tempranas · transversal a los índices"),

    # Indicadores
    ("ICPI", "INDICADOR", "tesis (abril 2026) · H12!B33",
     "INSTITUCIONAL",
     "Índice de Congruencia Programática e Intersistémica · indicador NUCLEAR "
     "del Gold Master, NO «el centro de QUIRA»"),
    ("TGI", "INDICADOR", "01_TGI_FRAMEWORK.md",
     "INTERNO", "índice de gobernanza integral 5D"),
    ("IED", "INDICADOR", "06_IED_DIRECTIVO.md",
     "INSTITUCIONAL", "Índice de Evaluación Directiva"),
    ("IGP", "INDICADOR", "H20b",
     "INSTITUCIONAL", "Índice de Gobernanza Participativa · ver D-010"),
    ("MMP", "INDICADOR", "08_MMP_MENSUAL.md",
     "INTERNO", "monitoreo mensual"),
    # Los nueve índices complementarios del Gold Master. Estaban fuera del
    # primer corte del inventario y eso lo hacía parecer más pequeño de lo que
    # es: un inventario incompleto subestima la deuda que pretende medir.
    ("IPE", "INDICADOR", "H16b · PCD-D01",
     "INSTITUCIONAL", "Índice de Planificación Ejecutada · d01 · fórmula nativa"),
    ("IFE", "INDICADOR", "H16",
     "INSTITUCIONAL", "Índice Financiero de Ejecución"),
    ("ITAM", "INDICADOR", "H18",
     "INSTITUCIONAL", "Índice de Transparencia Activa Municipal · d07"),
    ("ICODS", "INDICADOR", "H20",
     "INSTITUCIONAL", "Índice de Cumplimiento ODS"),
    ("IEF", "INDICADOR", "H20c",
     "INSTITUCIONAL", "Índice de Eficiencia Financiera"),
    ("PSG", "INDICADOR", "H16c",
     "INSTITUCIONAL", "Presupuesto Sensible al Género"),
    ("IBSC", "INDICADOR", "H12b_MOTOR_IBSC",
     "TÉCNICO", "motor complementario · categoría a confirmar en T3"),

    # Variables del ICPI
    ("P_i", "VARIABLE", "tesis · H14!G",
     "TÉCNICO", "coeficiente de peso presupuestario"),
    ("R_i", "VARIABLE", "tesis · H14!F",
     "TÉCNICO", "coeficiente de relevancia normativa"),
    ("V_i", "VARIABLE", "tesis · H13!F",
     "TÉCNICO", "verificación intersistémica"),
    ("E_i", "VARIABLE", "⚠️ NOT_DETERMINABLE (007-B0)",
     "TÉCNICO",
     "regla generadora no reconstruible desde el material conservado"),
    ("T_i", "VARIABLE", "H07b!fila 20",
     "TÉCNICO", "materialización temporal"),
    ("C_i", "VARIABLE", "H01 TBL_CALIBRACION_Ci",
     "TÉCNICO", "trazabilidad orgánica"),

    # Estados
    ("NOT_DETERMINABLE", "ESTADO", "Constitución CAPA 0",
     "INSTITUCIONAL", "no se pudo reconstruir"),
    ("UNTRACEABLE", "ESTADO", "GM-Ω taxonomía",
     "TÉCNICO", "sin fuente tras agotar la búsqueda"),
    ("TEMPORAL_SEMANTIC_GAP", "ESTADO", "GM-Ω taxonomía",
     "TÉCNICO",
     "la fuente existe pero su período o función no está bien declarado"),

    # Fuentes institucionales (ADR-029)
    ("SERCOP", "FUENTE", "LOSNCP",
     "PÚBLICO", "contratación pública"),
    ("eSIGEF", "FUENTE", "COPFP · MEF",
     "PÚBLICO", "ejecución presupuestaria"),
    ("LOTAIP", "FUENTE", "LOTAIP Art. 7",
     "PÚBLICO", "transparencia"),
    ("CPCCS", "FUENTE", "LOPC Art. 88",
     "PÚBLICO", "rendición de cuentas"),
    ("SIGAD", "FUENTE", "SENPLADES",
     "PÚBLICO", "autorreporte del GAD"),
    ("PDOT", "EVIDENCIA", "COOTAD · COPFP Art. 41",
     "PÚBLICO",
     "documento oficial y vinculante del mandato"),

    # ⚠️ El caso que abrió todo esto
    ("AVEP", "SIN_CATEGORÍA", "⚠️ ninguna autoridad vigente lo define",
     "HISTÓRICO",
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


# Las superficies de DOMINIO. Javo: «todos los índices están construidos para
# aparecer en los dom que los representan». Aquí se comprueba, no se supone.
_PAGS_DOMINIO = ("m_mandato", "m_planificacion", "m_presupuesto",
                 "m_participacion", "m_rdc", "p07_transparencia",
                 "p16_gobernanza", "p17_rdc")


def dominios_de(nombre: str, archivos: list[Path]) -> list[str]:
    """DERIVADO · en qué superficies de dominio aparece el nombre.

    ⚠️ Verifica la afirmación de Javo en vez de aceptarla o descartarla. Si un
    indicador no aparece en ninguna, hay dos lecturas posibles y NO se elige
    aquí: o su dominio todavía no está construido —d04, d05, d10-d13 siguen
    pendientes—, o el índice no tiene dominio que lo represente. Distinguirlas
    exige leer, no contar."""
    patron = re.compile(rf"(?<![\w_]){re.escape(nombre)}(?![\w_])")
    out = []
    for p in archivos:
        if p.parent.name != "quira_pages" or p.stem not in _PAGS_DOMINIO:
            continue
        try:
            if patron.search(p.read_text(encoding="utf-8", errors="replace")):
                out.append(p.stem)
        except OSError:
            continue
    return sorted(out)


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
    for nombre, cat, autoridad, vis, nota in _INVENTARIO:
        filas.append({"nombre": nombre, "cat": cat, "autoridad": autoridad,
                      "vis": vis, "nota": nota, **medir_uso(nombre, archivos),
                      "dominios": dominios_de(nombre, archivos)})

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
    A("| Nombre | Categoría | Capa | Autoridad que lo define | Archivos | En producto |")
    A("|---|---|---|---|---:|---:|")
    orden = {c: i for i, c in enumerate(_CATEGORIAS)}
    for f in sorted(filas, key=lambda x: (orden.get(x["cat"], 99), -x["archivos"])):
        marca = " ⚠️" if f["cat"] == "SIN_CATEGORÍA" else ""
        sup = f"{f['superficies']}" if f["superficies"] else "—"
        A(f"| `{f['nombre']}`{marca} | {f['cat']} | {f['vis']} | {f['autoridad']} | "
          f"{f['archivos']} | {sup} |")
    A("")
    A("## La segunda dimensión · capa de presentación")
    A("")
    A("| Capa | Qué significa |")
    A("|---|---|")
    for v, desc in _CAPA_PRESENTACION.items():
        A(f"| **{v}** | {desc} |")
    A("")
    A("⚠️ **No es un filtro de publicación**, y el matiz decide todo lo demás. "
      "Los índices **están construidos para aparecer en el dominio que los "
      "representa**: esa decisión ya la tomó la arquitectura de dominios y no se "
      "relitiga aquí. Lo que la visibilidad decide es **en qué capa de lectura** "
      "aparece cada nombre dentro de su dominio.")
    A("")
    A("La consecuencia práctica es la separación **nombre técnico ≠ nombre de "
      "presentación** (`DOC-014`):")
    A("")
    A("```")
    A("   PÚBLICO         ¿El mandato ofrecido puede seguirse hasta")
    A("                   su materialización?          27,46 %")
    A("        ↓ abrir")
    A("   INSTITUCIONAL   ICPI · corte abril 2026 · qué mide, período,")
    A("                   universo, fuentes, metodología")
    A("        ↓ abrir")
    A("   TÉCNICO         Índice de Congruencia Programática e Intersistémica")
    A("                   → Gold Master → P·R·V·E·T·C → fuentes → evidencia")
    A("```")
    A("")
    A("Así **no se oculta el indicador: se hace inteligible**. Y evita el riesgo "
      "opuesto —una portada de siglas y porcentajes flotantes— que induciría a "
      "leerlos como notas comparables entre sí. `DOC-012` ya dice por qué eso "
      "sería falso: **un porcentaje no significa nada por sí mismo**.")
    A("")

    # ── verificación de la afirmación de Javo ────────────────────────────────
    indicadores = [f for f in filas if f["cat"] == "INDICADOR"]
    con_dom = [f for f in indicadores if f["dominios"]]
    sin_dom = [f for f in indicadores if not f["dominios"]]
    A("### Verificación · ¿cada índice aparece en su dominio?")
    A("")
    A(f"De **{len(indicadores)} indicadores** inventariados, **{len(con_dom)}** "
      f"aparecen en alguna superficie de dominio:")
    A("")
    A("| Indicador | Superficies de dominio donde se le encontró |")
    A("|---|---|")
    for f in indicadores:
        d = ", ".join(f"`{x}`" for x in f["dominios"]) if f["dominios"] else "—"
        A(f"| `{f['nombre']}` | {d} |")
    A("")
    A("### ⚠️ Y aquí el resultado que importa NO es esa tabla")
    A("")
    A("**Esa tabla no demuestra nada, y hay que decirlo antes de que alguien la "
      "cite.** Se apoya en una lista de superficies de dominio **escrita a "
      "mano** en este mismo script "
      f"(`_PAGS_DOMINIO`, {len(_PAGS_DOMINIO)} de las 55 páginas del producto). "
      "Un índice que no aparece puede vivir perfectamente en una superficie que "
      "la lista no incluye. Medir contra una lista propia y presentar el "
      "resultado como hallazgo sería exactamente lo que `DOC-009` prohíbe.")
    A("")
    A("**Lo que sí quedó demostrado, al intentar la verificación:**")
    A("")
    A("> **No existe un artefacto que declare qué índice pertenece a qué "
      "dominio.**")
    A("")
    A("El mapeo existe —Javo lo tiene claro y la arquitectura lo aplica: *«todos "
      "los índices están construidos para aparecer en los dominios que los "
      "representan»*— pero **vive en el diseño, no en un artefacto verificable**. "
      "`PROTOCOLO_CURACION_DOMINIO` registra el estado de curación de cada "
      "dominio, no qué índice le corresponde.")
    A("")
    A("Y sin esa tabla, **ninguna verificación automática es posible**: ni ésta, "
      "ni una que compruebe que un índice no se publica fuera de su dominio, ni "
      "una que detecte un dominio que perdió su indicador. Es la misma forma del "
      "problema de `E_i` —una regla que opera sin estar escrita— y del de `AVEP` "
      "—un vocabulario que se propaga sin autoridad que lo defina—.")
    A("")
    A("**Producir ese mapeo es el primer entregable de `T3`.** No se improvisa "
      "aquí: exige leer dominio por dominio, y eso es curación, no inventario.")
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
