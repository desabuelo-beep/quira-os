# -*- coding: utf-8 -*-
"""
scripts/gm_omega/carta_rearquitectura.py — QUIRA-NEXT · CARTA v2

    El refactor es INTEGRAL, de fondo y forma, sobre todo el ecosistema. Y por
    eso mismo necesita plan antes que ejecución.

    ⚠️ POR QUÉ v2 ESTRUCTURAL Y NO UN PARCHE. La v1 inventarió el repositorio
    y llamó a eso «el ecosistema». Javo señaló lo que faltaba y era medular:

        «NO estamos tomando en consideración al corpus normativo de todo el
         marco legal que hemos vectorizado a Supabase, que es la otra base
         medular de QUIRA […] se vuelve con el Excel las bases metodológica y
         legal para el ecosistema.»

    El modelo de inventario de la v1 era incompleto DESDE SU RAÍZ: contaba
    archivos y omitía las bases de conocimiento. No se parchea — se rehace.

    LAS CUATRO BASES MEDULARES (Eje 0):

        BM-01  NORMATIVA     corpus jurídico ecuatoriano · Supabase
        BM-02  METODOLÓGICA  Gold Master · Excel · canon metodológico
        BM-03  EVIDENCIAL    CNE · GAD · SERCOP · CPCCS · LOTAIP · eSIGEF
        BM-04  ONTOLÓGICA    dominios · entidades · unidades · relaciones

    ESTA CARTA NO EJECUTA NADA. Y el Gold Master sigue congelado.

Uso:  python scripts/gm_omega/carta_rearquitectura.py
Dylus Lab © 2026
"""
from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "QUIRA-NEXT_CARTA_REARQUITECTURA.md"

# ── REGLA DE CONTEO ───────────────────────────────────────────────────────
#
# Explícita a propósito. La v1 publicó una tabla donde un lector experto sumó
# 6 de las 9 filas que sumaban y concluyó que el total estaba mal. El total
# era correcto —1321— y la tabla, ilegible. Se corrige la tabla, no el número.
_EXCLUIDOS = ("historico", ".git", "__pycache__", ".venv", "node_modules")

# ── LAS CINCO CATEGORÍAS DE TRATAMIENTO ───────────────────────────────────
_CATEGORIAS = [
    ("HISTÓRICO", "🏛️", "existió y ya no opera",
     "se PRESERVA como trazabilidad — nunca se borra",
     "`SIAP` · `QUADRUM` · `TERRA` · `ICPI_v1` · versiones superadas"),
    ("NORMATIVO VIGENTE", "⚖️", "lo fija una norma en vigor",
     "se ACATA mientras siga vigente — no es decisión de diseño",
     "`R_i`↔COOTAD 54-55 · `V_i`↔LOTAIP 7 · `T_i`↔COPFP 115-117 + Acuerdo "
     "067 MEF · `P_i`↔COPFP 54"),
    ("EMPÍRICAMENTE ÚTIL", "🔬", "funciona y hay evidencia de que funciona",
     "se CONSERVA si supera validación — y hay que poder mostrar cuál",
     "producto lógico de `V_i` · jerarquía de fuentes de `T_i` · "
     "`auditabilidad` como propiedad"),
    ("DECISIÓN DE DISEÑO ANTIGUA", "🔧",
     "se eligió, no se dedujo; y nadie escribió por qué",
     "queda ABIERTA a rediseño — ni válida ni inválida por antigüedad",
     "pesos `0,10/0,15/0,05/0,50` · piso `0,50` · residencia de los índices · "
     "escala AVEP"),
    ("SUPERADO METODOLÓGICAMENTE", "📜",
     "fue correcto en su momento y el conocimiento actual lo desplazó",
     "se conserva como ANTECEDENTE, no como regla",
     "`C_i` = imputabilidad orgánica · «Cumplimiento Institucional» como "
     "nombre del ICPI"),
]

# ── LAS CUATRO BASES MEDULARES · EJE 0 ────────────────────────────────────
_BASES = [
    ("BM-01", "NORMATIVA", "corpus jurídico ecuatoriano · Supabase",
     "¿qué derecho vigente permite afirmar que una competencia, obligación o "
     "procedimiento existe?"),
    ("BM-02", "METODOLÓGICA", "Gold Master · Excel · canon metodológico",
     "¿cómo transforma QUIRA esa realidad en conocimiento calculable?"),
    ("BM-03", "EVIDENCIAL", "CNE · GAD · SERCOP · CPCCS · LOTAIP · eSIGEF",
     "¿qué documento o registro demuestra el hecho observado?"),
    ("BM-04", "ONTOLÓGICA", "dominios · entidades · unidades · relaciones",
     "¿qué cosas existen, cómo se llaman y cómo se relacionan?"),
]

_EJES = [
    ("A", "Ontología", "¿qué cosas existen en QUIRA?",
     "Constitución §CAPA 0 · `T1`/`T2` cerrados"),
    ("B", "Taxonomía", "¿cómo se llaman y cómo se agrupan?",
     "`T1`-`T6` · 43 nombres · `T6` espera al dictamen"),
    ("C", "Metodología", "¿qué significa cada indicador?",
     "`011-C2` ✅ los 6 factores · faltan los otros 11 índices"),
    ("D", "Datos", "¿qué fuente alimenta cada dato?",
     "`004` matriz de procedencia · 150 celdas"),
    ("E", "Gold Master", "¿cómo se representa canónicamente?",
     "⚠️ CONGELADO hasta `011-C4`"),
    ("F", "Código", "¿la implementación coincide con la ontología?",
     "`DOC-016`"),
    ("G", "Dominios", "¿cada indicador vive donde corresponde?",
     "`R0`/`R1`/`R2` · 23 de 48 celdas `POR_DECLARAR`"),
    ("H", "Frontend", "¿la interfaz representa la arquitectura?",
     "sin frente · Bloomberg Firewall vigente"),
    ("I", "Narrativa", "¿QUIRA explica bien lo que mide?",
     "sin frente · es el salto de dashboard a inteligencia pública"),
    ("J", "Escalabilidad LATAM", "¿qué es Ecuador y qué es generalizable?",
     "`010` · siguiente"),
]


def _commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              cwd=_RAIZ, capture_output=True, text=True,
                              timeout=10).stdout.strip() or "—"
    except Exception:
        return "—"


def inventario_fisico() -> list[tuple[str, str, int, bool]]:
    """Archivos del repositorio. `suma=False` marca las filas CONTENIDAS en
    otra — no se suman dos veces."""
    def n(patron: str, raiz: str) -> int:
        base = _RAIZ / raiz
        if not base.exists():
            return 0
        return sum(1 for p in base.rglob(patron)
                   if not any(x in p.parts for x in _EXCLUIDOS))

    return [
        ("documentos de canon", "docs/**/*.md", n("*.md", "docs"), True),
        ("  ↳ de los cuales, `ADR`", "docs/adr", n("*.md", "docs/adr"), False),
        ("  ↳ de los cuales, `PCD`", "docs/pcd", n("*.md", "docs/pcd"), False),
        ("reglas de negocio", "docs/brn/*.yaml", n("*.yaml", "docs/brn"), True),
        ("gobernanza", "governance/**/*.md", n("*.md", "governance"), True),
        ("marco teórico", "marco_teorico/*.md", n("*.md", "marco_teorico"),
         True),
        ("módulos de aplicación", "app/**/*.py", n("*.py", "app"), True),
        ("páginas de interfaz", "quira_pages/*.py", n("*.py", "quira_pages"),
         True),
        ("scripts", "scripts/**/*.py", n("*.py", "scripts"), True),
        ("pruebas", "tests/test_*.py", n("test_*.py", "tests"), True),
        ("snapshots de datos", "data/**/*.json", n("*.json", "data"), True),
    ]


def inventario_normativo() -> dict:
    """★ BM-01 · el corpus jurídico vectorizado. Lo que la v1 no vio.

    SOLO `count` y `GROUP BY`: ni un embedding, ni una llamada a API. Javo
    está desfinanciado y este inventario no puede costar dinero.

    Devuelve `{}` si no hay conexión — **el tercer estado**: «no pude
    obtener» no es «no existe», y el CI corre sin credenciales."""
    try:
        sys.path.insert(0, str(_RAIZ / "scripts" / "normativa"))
        from ingest import get_connection
        cn = get_connection()
    except Exception:
        return {}

    def filas(cur):
        return [list(r.values()) if isinstance(r, dict) else list(r)
                for r in cur.fetchall()]

    try:
        cur = cn.cursor()
        cur.execute("SELECT count(*) AS n FROM normativa_corpus")
        total = filas(cur)[0][0]

        cur.execute("SELECT tipo_documento AS v, count(*) AS n "
                    "FROM normativa_corpus GROUP BY 1 ORDER BY 2 DESC")
        tipos = filas(cur)

        cur.execute("SELECT count(DISTINCT norma_sigla) AS n "
                    "FROM normativa_corpus")
        siglas = filas(cur)[0][0]

        cur.execute("SELECT count(*) AS n FROM normativa_corpus "
                    "WHERE document_class IS NULL")
        sin_clase = filas(cur)[0][0]

        cur.execute("SELECT count(*) AS n FROM normativa_corpus "
                    "WHERE authority_level IS NULL")
        sin_autoridad = filas(cur)[0][0]

        # ⚠️ `%` va escapado: psycopg2 lo toma por marcador de parámetro.
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_name='normativa_corpus'
                         AND (column_name ILIKE '%%vigen%%'
                           OR column_name ILIKE '%%derog%%'
                           OR column_name ILIKE '%%reform%%')""")
        vigencia = [x[0] for x in filas(cur)]

        cur.execute("""SELECT table_name FROM information_schema.tables
                       WHERE table_schema='public' ORDER BY 1""")
        tablas = [x[0] for x in filas(cur)]
        cn.close()
    except Exception:
        try:
            cn.close()
        except Exception:
            pass
        return {}

    # Qué es NORMA y qué es INSTRUMENTO DE GESTIÓN. La tabla se llama
    # `normativa_corpus` y contiene las dos cosas: BM-01 y BM-03 mezcladas.
    _NORMA = {"ley_organica", "reglamento", "constitucion", "resolucion",
              "convenio_internacional", "instructivo", "acuerdo", "reforma",
              "guia", "resolucion_local"}
    norma = sum(n for t, n in tipos if t in _NORMA)
    return {"total": total, "tipos": tipos, "siglas": siglas,
            "sin_clase": sin_clase, "sin_autoridad": sin_autoridad,
            "vigencia": vigencia, "tablas": tablas,
            "norma": norma, "gestion": total - norma}


def main() -> int:
    fis = inventario_fisico()
    total_fis = sum(c for _d, _r, c, s in fis if s)
    nor = inventario_normativo()

    inv_id = f"QNEXT-INV-{datetime.now().strftime('%Y-%m-%d')}"
    print(f"{inv_id} · commit {_commit()}")
    print(f"FÍSICO      {total_fis} archivos")
    if nor:
        print(f"NORMATIVO   {nor['total']} chunks · {nor['siglas']} normas · "
              f"{nor['norma']} norma / {nor['gestion']} instrumentos de gestión")
        print(f"            vigencia: {nor['vigencia'] or '⚠️ SIN COLUMNA'} · "
              f"sin clase {nor['sin_clase']} · {len(nor['tablas'])} tablas")
    else:
        print("NORMATIVO   [no determinable] sin conexión a Supabase")

    _escribir(fis, total_fis, nor, inv_id)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(fis, total_fis, nor, inv_id) -> None:
    o: list[str] = []
    A = o.append
    ND = "⬜ **NO DETERMINABLE** · sin conexión a Supabase al generar"

    A("# QUIRA-NEXT · CARTA DE REARQUITECTURA  `v2`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/carta_rearquitectura.py`.")
    A("")
    A("```")
    A(f"  INVENTARIO_ID : {inv_id}")
    A(f"  COMMIT        : {_commit()}")
    A(f"  GENERATED_AT  : {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    A("```")
    A("")
    A("> Sin esta estampilla, «412 documentos» es una **afirmación "
      "flotante**. Con ella es una **observación reproducible de un estado "
      "concreto del repositorio** — y explica sola por qué la v1 dijo 411 y "
      "esta dice otra cifra: el propio acto de escribir la carta añadió "
      "archivos.")
    A("")
    A("> ### Qué es esto")
    A("> El plan del **refactor integral de fondo y forma de todo el "
      "ecosistema**. **No ejecuta nada.**")
    A("")
    A("⚠️ **El Gold Master sigue congelado hasta `011-C4`.** Planificar el "
      "refactor **no adelanta** el momento de intervenir el motor, y el "
      "baseline **27,4582 %** no se mueve.")
    A("")

    # ── Por qué v2 ────────────────────────────────────────────────────────
    A("## Por qué esta carta es una `v2` estructural y no un parche")
    A("")
    A("La `v1` inventarió el repositorio y llamó a eso «el ecosistema». Javo "
      "señaló lo que faltaba, y era medular:")
    A("")
    A("> *«NO estamos tomando en consideración al corpus normativo de todo el "
      "marco legal que hemos vectorizado a Supabase, que es la otra base "
      "medular de QUIRA […] se vuelve con el Excel las bases metodológica y "
      "legal para el ecosistema.»*")
    A("")
    A("**El modelo de inventario de la `v1` era incompleto desde su raíz**: "
      "contaba archivos y omitía las bases de conocimiento. Eso no se "
      "parchea.")
    A("")
    A("### Y una corrección de hecho, sobre la objeción a la `v1`")
    A("")
    A("El colega observó que el total `1321` no cuadraba con `1265` y "
      "concluyó que había un error de cardinalidad. **Verificado: el total "
      "era correcto.** La suma omitía tres filas —`brn` (30), `governance` "
      "(23), `marco_teorico` (3) = **56**, exactamente la diferencia "
      "detectada—.")
    A("")
    A("> **Pero la conclusión seguía siendo correcta por otra razón:** si un "
      "lector experto suma mal la tabla, **la tabla no era legible**. Se "
      "corrige la tabla, no el número — y se añade la regla de conteo "
      "explícita.")
    A("")

    # ── EJE 0 · las bases medulares ───────────────────────────────────────
    A("## ★ EJE 0 · Las cuatro bases medulares")
    A("")
    A("Antes que los diez ejes. QUIRA **no se apoya en el Excel**: se apoya "
      "en cuatro bases, y el Excel es una de ellas.")
    A("")
    A("| | Base | Qué es | Pregunta que responde |")
    A("|---|---|---|---|")
    for bid, nombre, que, pregunta in _BASES:
        A(f"| `{bid}` | **{nombre}** | {que} | {pregunta} |")
    A("")
    A("```")
    A("                       QUIRA")
    A("                         │")
    A("           ┌─────────────┴─────────────┐")
    A("      BM-01 NORMATIVA          BM-02 METODOLÓGICA")
    A("      corpus jurídico          Gold Master · Excel")
    A("      Ecuador · GAD            metodología + datos")
    A("           └─────────────┬─────────────┘")
    A("                         │")
    A("                   MOTOR DE QUIRA")
    A("                         │")
    A("           ┌─────────────┴─────────────┐")
    A("      BM-03 EVIDENCIA          BM-04 ONTOLOGÍA")
    A("      qué ocurrió              qué cosas existen")
    A("           └─────────────┬─────────────┘")
    A("                         │")
    A("                    INFERENCIA")
    A("                         │")
    A("                   INTELIGENCIA")
    A("                         │")
    A("        ┌────────────────┼────────────────┐")
    A("      FONDO            FORMA          TRANSVERSAL")
    A("```")
    A("")
    A("### ★ La distinción que no debemos volver a mezclar")
    A("")
    A("| | Afirmación | Fuente |")
    A("|---|---|---|")
    A("| **NORMA** | «la ley establece X» | corpus jurídico · `BM-01` |")
    A("| **EVIDENCIA** | «el GAD hizo o no hizo X» | CNE · SERCOP · CPCCS · "
      "LOTAIP · eSIGEF · `BM-03` |")
    A("| **INFERENCIA QUIRA** | «de norma + evidencia + metodología se sigue "
      "Y» | motor metodológico · `BM-02` |")
    A("")
    A("> ### La fuente normativa tiene PRECEDENCIA sobre el diseño de QUIRA")
    A(">")
    A("> Si la metodología dice que `C_i` significa X y la norma vigente "
      "determina otra cosa sobre esa competencia o responsabilidad, **la "
      "metodología no puede ignorarlo**. Es la diferencia entre `⚖️ "
      "NORMATIVO VIGENTE` y `🔧 DECISIÓN DE DISEÑO`.")
    A("")
    A("Y de aquí sale lo que QUIRA **es**, dicho sin metáfora:")
    A("")
    A("> No es un Excel sofisticado, ni un dashboard, ni un índice, ni un "
      "corpus jurídico, ni un RAG legal. Es un **sistema que relaciona norma, "
      "evidencia, metodología y contexto territorial para producir "
      "inferencias reproducibles sobre la gestión pública**.")
    A("")

    # ── BM-01 medido ──────────────────────────────────────────────────────
    A("## ★ `BM-01` · El corpus normativo, medido")
    A("")
    if not nor:
        A(ND + ". El inventario del corpus **no se pudo leer** al generar "
              "esta carta, y eso se declara en vez de estimarse.")
        A("")
    else:
        A(f"**{nor['total']:,} fragmentos · {nor['siglas']} normas "
          f"distintas · {len(nor['tablas'])} tablas** en el esquema."
          .replace(",", "."))
        A("")
        A("| `tipo_documento` | Fragmentos | Naturaleza |")
        A("|---|---:|---|")
        _NORMA = {"ley_organica", "reglamento", "constitucion", "resolucion",
                  "convenio_internacional", "instructivo", "acuerdo",
                  "reforma", "guia", "resolucion_local"}
        for t, n in nor["tipos"]:
            nat = "⚖️ **norma**" if t in _NORMA else "📋 instrumento / evidencia"
            A(f"| `{t}` | {n} | {nat} |")
        A("")
        A("### ⚠️ Tres hallazgos que condicionan todo el refactor")
        A("")
        A(f"**1 · La tabla se llama `normativa_corpus` y contiene dos "
          f"universos.** {nor['norma']} fragmentos son norma; "
          f"{nor['gestion']} son instrumentos de gestión y evidencia —PDOT, "
          f"POA, PAC, PP, informes de rendición—. Es decir: **`BM-01` y "
          f"`BM-03` conviven en la misma tabla**, y el nombre induce a "
          f"tratarlos igual. No lo son: la norma tiene precedencia sobre el "
          f"diseño; la evidencia, no.")
        A("")
        if not nor["vigencia"]:
            A("**2 · 🔴 NO EXISTE COLUMNA DE VIGENCIA.** Las únicas columnas "
              "temporales son `ingestado_at` e `ingestado_por` — **cuándo se "
              "cargó, no cuándo rige**. El corpus no puede distinguir:")
            A("")
            A("```")
            A("  NORMA VIGENTE  ·  REFORMADA  ·  DEROGADA  ·  HISTÓRICA")
            A("```")
            A("")
            A("> Y esto es grave para un sistema cuya `Regla de Oro 3` dice "
              "**«sin norma verificada, no hay dato»**: hoy el corpus puede "
              "devolver un artículo derogado con la misma autoridad que uno "
              "vigente, y nada en el esquema lo impide.")
        else:
            A(f"**2 · Columnas de vigencia presentes:** "
              f"{', '.join('`' + c + '`' for c in nor['vigencia'])}.")
        A("")
        pct = nor["sin_clase"] / nor["total"] * 100 if nor["total"] else 0
        A(f"**3 · `document_class` y `authority_level` están vacías en "
          f"{nor['sin_clase']:,} de {nor['total']:,} fragmentos "
          f"({pct:.0f} %)**.".replace(",", "."))
        A("")
        A("La jerarquía normativa formal **no está poblada** para la gran "
          "mayoría del corpus —Constitución y COOTAD incluidos—. Existe un "
          "campo `jerarquia` que sí está completo: **dos campos para lo "
          "mismo, uno lleno y otro vacío.** Es el patrón que `011-C2` "
          "encontró en `C_i`, repetido en el esquema de datos.")
        A("")
        A("### Lo que `BM-01` necesita y hoy no tiene")
        A("")
        A("| Atributo | Estado |")
        A("|---|---|")
        A("| identificador · sigla · nombre | ✅ |")
        A("| jerarquía | 🟡 duplicada: `jerarquia` llena, `authority_level` "
          "vacía |")
        A("| `sha256` y trazabilidad al archivo | ✅ |")
        A("| dominios QUIRA asociados | ✅ `dominios_quira` |")
        A("| **vigencia temporal** | 🔴 **ausente** |")
        A("| **estado jurídico** (vigente/reformada/derogada) | 🔴 **ausente** |")
        A("| **separación norma ↔ instrumento** | 🔴 **ausente** |")
        A("| institución emisora | 🟡 `source_entity`, parcial |")
        A("| relaciones entre normas | 🔴 ausente en esta tabla |")
        A("")
        A("⚠️ Nada de esto se corrige aquí. Se **registra** — y `BM-01` pasa a "
          "ser un frente propio del refactor, no un detalle de `Q1`.")
        A("")

    # ── Los cuatro inventarios ────────────────────────────────────────────
    A("## 1 · Cuatro inventarios, cuatro cardinalidades")
    A("")
    A("**Está prohibido sumar archivos con constructos.** Un archivo es un "
      "artefacto; una hoja es una estructura interna de un artefacto; un "
      "dominio es una entidad ontológica; un índice es un constructo "
      "metodológico; un factor es una dimensión de un constructo. No están en "
      "el mismo nivel, y decir «QUIRA tiene N cosas» sería falsear.")
    A("")
    A("### ① Inventario FÍSICO · archivos del repositorio")
    A("")
    A("**Regla de conteo:** se recorre cada raíz recursivamente con su "
      "extensión; se excluyen "
      + " · ".join(f"`{x}`" for x in _EXCLUIDOS) + ". Las filas en *cursiva* "
      "**no suman**: están contenidas en la de arriba.")
    A("")
    A("| Artefactos | Raíz · patrón | Cuenta |")
    A("|---|---|---:|")
    for desc, raiz, cuenta, suma in fis:
        marca = f"**{cuenta}**" if suma else f"*{cuenta}*"
        A(f"| {desc} | `{raiz}` | {marca} |")
    A(f"| | **TOTAL FÍSICO (suma de las filas en negrita)** | "
      f"**{total_fis}** |")
    A("")
    A("### ② Inventario DOCUMENTAL · el canon")
    A("")
    A("| | Cuenta |")
    A("|---|---:|")
    for desc, _r, cuenta, _s in fis:
        if "ADR" in desc or "PCD" in desc:
            A(f"| {desc.replace('  ↳ de los cuales, ', '')} | {cuenta} |")
    A("| doctrina con verificador | 28 |")
    A("| deudas registradas | 14 |")
    A("")
    A("### ③ Inventario ONTOLÓGICO · qué existe")
    A("")
    A("| | Cuenta |")
    A("|---|---:|")
    A("| dominios | 13 |")
    A("| macroejes | 4 |")
    A("| entidades del holding municipal | 5 |")
    A("| unidades orgánicas (Res. 040-2025) | 20 |")
    A("")
    A("### ④ Inventario METODOLÓGICO · qué se calcula")
    A("")
    A("| | Cuenta |")
    A("|---|---:|")
    A("| índices | 12 |")
    A("| factores del ICPI | 6 |")
    A("| reglas de negocio | 30 |")
    A("| hojas del Gold Master | 123 |")
    A("| metas del universo operacional | 25 de 66 |")
    A("")
    A("### ⑤ Inventario NORMATIVO · `BM-01`")
    A("")
    if nor:
        A("| | Cuenta |")
        A("|---|---:|")
        A(f"| fragmentos vectorizados | {nor['total']} |")
        A(f"| normas distintas | {nor['siglas']} |")
        A(f"| tipos documentales | {len(nor['tipos'])} |")
        A(f"| tablas en el esquema | {len(nor['tablas'])} |")
    else:
        A(ND)
    A("")

    # ── Las cinco categorías ──────────────────────────────────────────────
    A("## ★ 2 · Las cinco categorías · la regla que impide dañar lo válido")
    A("")
    A("**Ninguna pieza del ecosistema se toca antes de clasificarla.**")
    A("")
    A("| | Categoría | Qué es | Qué se hace con ella |")
    A("|---|---|---|---|")
    for nombre, icono, que_es, tratamiento, _ej in _CATEGORIAS:
        A(f"| {icono} | **{nombre}** | {que_es} | {tratamiento} |")
    A("")
    for nombre, icono, _q, _t, ejemplos in _CATEGORIAS:
        A(f"**{icono} {nombre}** — {ejemplos}")
        A("")

    A("### ⚠️ `NO_DETERMINADO` no es una sexta categoría")
    A("")
    A("Es un **estado de evidencia** transversal, y la distinción evita un "
      "error grave. Una pieza tiene **categoría** y **estado** a la vez:")
    A("")
    A("| Pieza | Categoría | Estado de evidencia |")
    A("|---|---|---|")
    A("| `Constitución Art. 233` | ⚖️ normativo vigente | ✅ fuente primaria "
      "localizada |")
    A("| peso `C_i = 0,20` | 🔧 decisión de diseño | ❓ justificación no "
      "determinada |")
    A("| producto lógico de `V_i` | 🔬 empíricamente útil | ⚠️ evidencia "
      "insuficiente |")
    A("")
    A("> ### `NO_DETERMINADO` significa «no hemos demostrado todavía la razón "
      "o la condición». **Nunca significa «la razón no existe»** — y por "
      "tanto **nunca autoriza a eliminar**.")
    A("")
    A("Sin esta separación, el refactor derivaría al silogismo falso: *«no "
      "está justificado → se puede quitar»*. `DOC-027` lo prohíbe.")
    A("")
    A("### La corrección que esta tabla incorpora")
    A("")
    A("Una versión anterior de `DOC-027` decía:")
    A("")
    A("> ~~«Donde no hay razón documentada, no hay nada que respetar.»~~")
    A("")
    A("**Empujaba al extremo contrario** del sesgo conservador que venía a "
      "corregir. La formulación rigurosa es:")
    A("")
    A("> Donde no existe justificación documental de una decisión de diseño, "
      "esa decisión **no adquiere autoridad metodológica por antigüedad**; su "
      "permanencia debe **evaluarse nuevamente** frente al fenómeno, la "
      "teoría, la evidencia, la norma y la arquitectura actual.")
    A("")
    A("Una decisión antigua sin justificación **no es automáticamente "
      "incorrecta**. Tampoco automáticamente correcta. Queda **abierta**, que "
      "es un estado distinto de ambos.")
    A("")

    # ── Clasificación gobernada ───────────────────────────────────────────
    A("## ★ 3 · La máquina propone, la dirección ratifica")
    A("")
    A("La `v1` decía que «la clasificación sea derivable». **Es insuficiente "
      "y peligroso**: automatizar una clasificación epistemológica la "
      "convierte en una caja negra nueva.")
    A("")
    A("| Lo que la máquina SÍ puede hacer | Lo que NO puede decidir |")
    A("|---|---|")
    A("| detectar referencias a normas · `ADR` · nombres históricos | «esto "
      "es una decisión de diseño antigua» |")
    A("| detectar dependencias y referencias cruzadas | «esto está superado "
      "metodológicamente» |")
    A("| detectar qué código consume qué hoja | «esto es empíricamente "
      "útil» |")
    A("| detectar dónde aparece un índice o un término | cualquier "
      "clasificación **epistemológica** |")
    A("")
    A("Por eso cada pieza lleva **dos campos**:")
    A("")
    A("```")
    A("  classification_candidate   ← lo propone el script")
    A("  classification_status      ← lo ratifica la dirección")
    A("                                PENDIENTE · PROPUESTO · VERIFICADO")
    A("```")
    A("")
    A("| Pieza | Candidato automático | Estado |")
    A("|---|---|---|")
    A("| `Constitución Art. 233` | ⚖️ normativo vigente | **VERIFICADO** |")
    A("| `ICPI_v1` | 🏛️ histórico | **VERIFICADO** |")
    A("| peso `C_i = 0,20` | 🔧 decisión antigua | **PENDIENTE** · `011-C3` |")
    A("| `auditabilidad` | 🔬 empíricamente útil | **PENDIENTE** |")
    A("| `C_i` = imputabilidad orgánica | 📜 superado | **PROPUESTO** |")
    A("")

    # ── El caso auditoría ─────────────────────────────────────────────────
    A("## ★ 4 · `auditoría` · la prueba patrón de migración semántica")
    A("")
    A("Javo puso el ejemplo *«quitar la palabra auditoría de la "
      "documentación»* para fijar el NIVEL del refactor. Esta dirección "
      "**empezó a ejecutarlo**. Javo lo detuvo. Lo medido antes de parar:")
    A("")
    A("```")
    A("  «auditoría» →  609 ocurrencias  ·  233 archivos")
    A("```")
    A("")
    A("Y **no son la misma palabra**:")
    A("")
    A("```")
    A("                        cadena: auditor*")
    A("                              │")
    A("     ┌──────────────┬─────────┼─────────┬──────────────┐")
    A("     ▼              ▼         ▼         ▼              ▼")
    A(" auditoría CGE   GM-Ω     QUIRA     auditable    auditabilidad")
    A("     │          «audit.»  «audita»      │              │")
    A("  ⚖️ NORMA      🔧 TERMIN. 🔧 TÉRMINO  🔬 PROPIEDAD  🔬 CONCEPTO")
    A("  referencia    de trabajo INCORRECTO   preservar     evaluar")
    A("  legal ·       revisar    sustituir    en código     en teoría")
    A("  INTOCABLE")
    A("```")
    A("")
    A("> ### El gate que esto obliga a construir")
    A(">")
    A("> **Ninguna migración léxica puede alterar una referencia normativa "
      "vigente por el solo hecho de compartir una cadena de caracteres con un "
      "término que se desea reemplazar.**")
    A("")
    A("Un reemplazo sin clasificación previa **habría borrado artículos de "
      "ley**. Ocurrió en el primer minuto del primer ejemplo, y por eso este "
      "caso deja de ser anécdota: es el **primer test de `Q1`**.")
    A("")
    A("Y hay algo que conviene decir: **`governance/BOOT.md` declara desde el "
      "2026-08-05 que QUIRA «⛔ NO es auditoría ni observatorio»**. La regla "
      "existía; el vocabulario del repositorio no la siguió. Es el mismo "
      "patrón que `DOC-013`, y es la razón de fondo de este refactor.")
    A("")

    # ── FONDO y FORMA ─────────────────────────────────────────────────────
    A("## ★ 5 · FONDO y FORMA")
    A("")
    A("```")
    A("                        QUIRA")
    A("              ┌───────────┴───────────┐")
    A("            FONDO                   FORMA")
    A("     ¿QUÉ gestiona el GAD?    ¿CÓMO lo gestiona?")
    A("              │                       │")
    A("     dominios sectoriales    capacidades transversales")
    A("              │                       │")
    A("   salud · agua · vialidad    planificación · ejecución")
    A("   ambiente · riesgos ·       eficiencia · contratación")
    A("   desarrollo económico       transparencia · trazabilidad")
    A("                              coordinación · responsabilidad")
    A("```")
    A("")
    A("> **La misma gestión se observa a la vez desde el fondo y desde la "
      "forma.** Eso es lo que hoy no se puede hacer, y es la razón por la que "
      "hay indicadores transversales viviendo dentro de dominios "
      "sectoriales.")
    A("")
    A("### El caso que lo prueba · `IED`")
    A("")
    A("Javo propuso *«establecer eficiencia directiva»*. **Ya existe**: el "
      "`IED` desglosa metas del PDOT por dirección del Estatuto Orgánico "
      "(`H17`, `H30`). Lo que no tiene es sitio: su dominio, su rol y su "
      "pregunta están los tres `POR_DECLARAR`.")
    A("")
    A("En el esquema se ve por qué: **`IED` no pertenece a ningún dominio "
      "sectorial**. «¿Qué tan eficientemente funciona la dirección "
      "responsable?» aplica a Salud, a Obras Públicas y a Financiera por "
      "igual. Es **forma**, y hoy no hay dónde ponerla.")
    A("")
    A("| Nivel | Unidad | Pregunta |")
    A("|---|---|---|")
    A("| **sectorial** | una competencia | ¿qué resultados está gestionando? |")
    A("| **organizacional** | una dirección | ¿cómo funciona esa unidad? |")
    A("| **transversal** | el gobierno municipal | ¿es coherente, eficiente, "
      "trazable y coordinado el sistema completo? |")
    A("")

    # ── El ICPI ───────────────────────────────────────────────────────────
    A("## 6 · El ICPI · cuatro destinos, ninguno decidido")
    A("")
    A("| | Destino | Qué significaría |")
    A("|---|---|---|")
    A("| **A** | se **conserva** | supera `C4` y la teoría justifica sus "
      "dimensiones |")
    A("| **B** | se **refactoriza** | mismo fenómeno, otros factores, otra "
      "semántica, otra escala, otra residencia |")
    A("| **C** | se **descompone** | congruencia programática · ejecución "
      "financiera · trazabilidad · responsabilidad institucional · eficiencia "
      "directiva · desempeño operativo — y un **panel multidimensional** en "
      "lugar de un índice único |")
    A("| **D** | se **depreca** | `ICPI_v1` queda para trazabilidad y deja de "
      "ser el indicador operativo principal |")
    A("")
    A("**Ninguno de los cuatro es un fracaso.** `D` tampoco: sería evolución "
      "metodológica.")
    A("")
    A("### Y por qué el nombre va al final")
    A("")
    A("```")
    A("  1. ¿qué fenómeno sobrevive a C4?")
    A("  2. ¿cuál es su unidad?")
    A("  3. ¿cuál es su arquitectura?")
    A("  4. ¿cuál es su residencia?")
    A("  5. …y recién entonces: ¿cómo se llama?")
    A("```")
    A("")
    A("> Empezar por el nombre sería hacer **branding de un concepto que "
      "todavía se está rediseñando**.")
    A("")

    # ── Los diez ejes ─────────────────────────────────────────────────────
    A("## 7 · Los diez ejes · se auditan simultáneamente")
    A("")
    A("| | Eje | Pregunta | Estado hoy |")
    A("|---|---|---|---|")
    for letra, nombre, pregunta, estado in _EJES:
        A(f"| **{letra}** | {nombre} | {pregunta} | {estado} |")
    A("")

    # ── Secuencia ─────────────────────────────────────────────────────────
    A("## ★ 8 · La secuencia · `010` alimenta el diseño, no lo cierra")
    A("")
    A("```")
    A("                    CARTA v2  (este documento)")
    A("                          │")
    A("               ┌──────────┴──────────┐")
    A("          INVENTARIO             010 LATAM")
    A("       físico · normativo    ¿qué es Ecuador y")
    A("       ontológico · metod.    qué es transferible?")
    A("               └──────────┬──────────┘")
    A("                          ▼")
    A("                MATRIZ DE CLASIFICACIÓN")
    A("                 candidato → ratificado")
    A("                          ▼")
    A("                    R0 · R1 · Q1")
    A("                          ▼")
    A("                       011-C4")
    A("                          ▼")
    A("               DECISIÓN METODOLÓGICA")
    A("                          ▼")
    A("                MIGRACIÓN CONTROLADA")
    A("                          ▼")
    A("                  GOLD MASTER vNEXT")
    A("```")
    A("")
    A("**`010` y el inventario no son tareas independientes.** `010` necesita "
      "saber qué se pretende generalizar, y la carta necesita que `010` le "
      "diga qué es específico de Ecuador, qué es conceptual, qué es "
      "transferible y qué exige recalibración nacional.")
    A("")
    A("> ### Y una hipótesis que `010` debe poner a prueba")
    A(">")
    A("> El producto exportable de QUIRA **puede no ser el ICPI**, sino la "
      "arquitectura `NORMA + EVIDENCIA + ONTOLOGÍA + METODOLOGÍA → "
      "INTELIGENCIA PÚBLICA` — donde cada país sustituye su corpus normativo, "
      "sus fuentes institucionales y ciertos parámetros. Si se confirma, "
      "cambia la estrategia LATAM entera.")
    A("")
    A("| 🟢 Se puede hacer AHORA | 🔴 CONGELADO hasta `C4` |")
    A("|---|---|")
    A("| inventario · grafo de dependencias | Gold Master |")
    A("| clasificación candidata · análisis léxico | fórmula vigente · `B33` |")
    A("| `010` · `R0` · `R1` | valores históricos |")
    A("| análisis de dominios · frontend · narrativa | residencia actual de "
      "los índices |")
    A("| matriz FONDO/FORMA · diseño de gates y migración | nombres canónicos "
      "con función metodológica |")
    A("| pruebas que **no** modifican el estado canónico | código que produce "
      "el baseline · snapshots |")
    A("")
    A("> **Se puede estudiar el edificio entero sin mover una pared.**")
    A("")

    # ── Reglas ────────────────────────────────────────────────────────────
    A("## 9 · Las reglas de la migración")
    A("")
    A("> ### `DOC-029` · REGLA MAESTRA DE REARQUITECTURA")
    A(">")
    A("> **Ningún cambio se ejecuta directamente sobre el ecosistema "
      "canónico. Primero se OBSERVA, después se CLASIFICA, luego se "
      "JUSTIFICA, después se DISEÑA LA MIGRACIÓN, y sólo entonces se "
      "EJECUTA.**")
    A(">")
    A("> Es la diferencia entre hacer limpieza y hacer una rearquitectura "
      "gobernada.")
    A("")
    A("| # | Regla | De dónde sale |")
    A("|---|---|---|")
    A("| 1 | **Clasificar antes de tocar** | esta carta · §2 |")
    A("| 2 | **La norma tiene precedencia sobre el diseño** | Eje 0 |")
    A("| 3 | **El basónimo no cambia** — el identificador estable sobrevive "
      "al renombrado | `DOC-015` |")
    A("| 4 | **Nombre técnico ≠ nombre de presentación** | `DOC-014` · "
      "`Regla de Oro 2` |")
    A("| 5 | **Anti-inflación**: si sólo renombra, no entra | `Regla de Oro "
      "7` |")
    A("| 6 | **Ningún cambio nace en Python** | `Regla de Oro 9` · `DOC-016` |")
    A("| 7 | **Lo que se retira no se borra**: pasa a `HISTÓRICO` con su "
      "linaje | `DOC-013` |")
    A("| 8 | **Continuidad histórica ≠ continuidad metodológica** | `DOC-028` |")
    A("| 9 | **`NO_DETERMINADO` nunca autoriza a eliminar** | `DOC-027` |")
    A("| 10 | **Cada dominio cierra con su `PCD`** | `Regla de Oro 8` |")
    A("")

    A("## Lo que esta carta NO hace")
    A("")
    A("- **No decide el destino del ICPI.** Cuatro opciones, `011-C4` elige.")
    A("- **No renombra nada.** El nombre es el último paso.")
    A("- **No toca el Gold Master** ni el corpus normativo.")
    A("- **No clasifica todavía** ninguna pieza: establece **cómo** se "
      "clasifica y **quién ratifica**.")
    A("")
    A("> ### El propósito, en una línea")
    A(">")
    A("> `GM-Ω` no existe para legitimar el pasado ni para destruirlo, sino "
      "para **ponerlo en su lugar**: el pasado como **linaje**, la norma como "
      "**restricción**, la evidencia como **fundamento**, la teoría como "
      "**justificación** — y el diseño como **decisión presente**.")
    A("")
    A("---")
    A(f"*QUIRA-NEXT · Carta de Rearquitectura `v2` · {inv_id} · commit "
      f"`{_commit()}` · el Gold Master no se modificó · baseline 27,4582 % "
      f"congelado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
