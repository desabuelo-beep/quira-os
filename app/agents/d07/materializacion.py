"""
app/agents/d07/materializacion.py — obligación ↔ evidencia, no archivo ↔ numeral
================================================================================
POR QUÉ EXISTE (2026-08-20). El director propuso recorrer los 636 artefactos «por
numeral» o «por artefacto». Javo lo corrigió de raíz:

> *«No se puede separar los artefactos de los numerales: están transversalizados
> por la normativa legal vigente y sus procedimientos técnicos, que también son
> ley. El universo de información de transparencia activa del GAD no debe
> interpretarse como una colección arbitraria de archivos, sino como una
> **materialización documental de obligaciones normativas y procedimentales**.»*

El error era doble. De método —«por numeral» y «por artefacto» son técnicas de
recorrido, no la estructura del fenómeno— y, más grave, de epistemología: se
ofreció declarar que los artefactos sin obligación asociada «revelan que el GAD
publica lo que la norma no le pide». Eso es **presumir en vez de determinar**, y
es exactamente lo que este dominio existe para impedir.

LA UNIDAD ES LA RELACIÓN, no ninguno de sus extremos:

    ordenamiento normativo
        → obligación            qué exige la norma, con su procedencia
        → objeto exigible       qué información concreta debe existir
        → materialización       qué documento sería esperable
        → evidencia             qué se encontró, con qué SHA
        → verificación          quién lo interpretó y con qué prueba
        → afirmación            qué puede sostenerse sobre el sujeto

Y la regla que impide repetir con los documentos el error de los enlaces:

    **La ausencia de un artefacto no constituye por sí misma incumplimiento:
    constituye ausencia de evidencia respecto de una obligación cuya
    materialización esperada debe haber sido previamente determinada.**

QUÉ NO HACE. No decide qué información debería existir —eso lo fija el
ordenamiento, y llega aquí por la vara sellada—. No califica jurídicamente. No
presume el significado de un artefacto que no logra asociar: lo declara
`sin_obligacion_identificada`, que es una limitación del análisis y no un
hallazgo sobre el GAD.

Uso:  python -m app.agents.d07.materializacion --anio 2025 [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                    # noqa: E402
from app.agents import sujeto as S                         # noqa: E402

_VARA = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
_INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
_CONTENIDO = RAIZ / "data" / "lotaip" / "contenido.json"
_INVENTARIO = RAIZ / "data" / "lotaip" / "inventario_documental.json"
_CONTENEDORES = RAIZ / "data" / "lotaip" / "contenido_contenedores.json"
_SALIDA = RAIZ / "data" / "d07" / "matriz_materializacion.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ── Estados de la relación, no del archivo ──────────────────────────────────────
# Describen qué le pasa a la OBLIGACIÓN frente a la evidencia hallada. Ninguno
# afirma cumplimiento o incumplimiento: eso es calificación jurídica y no
# corresponde a este módulo (PCD-D07 · Principio Rector).
MATERIALIZADA = "materializada"              # hay evidencia que la acredita
PARCIAL = "materializacion_parcial"          # hay evidencia, no cubre lo exigido
SIN_EVIDENCIA = "sin_evidencia_hallada"      # se buscó y no se encontró
NO_DETERMINABLE = "no_determinable"          # la cadena no sostiene ninguna lectura


@dataclass
class Obligacion:
    """Una exigencia del ordenamiento, con lo que hace falta para verificarla."""
    numeral: str
    texto: str
    campos_exigidos: list[str]
    periodicidad: dict
    procedencia_normativa: dict
    estructura_formal: dict = field(default_factory=dict)

    @property
    def periodicidad_declarada(self) -> bool:
        """La Guía no declara periodicidad para todos los numerales. Donde no la
        declara, exigirla sería inventar la obligación."""
        return self.periodicidad.get("estado") not in (None, "no_sustentado")


@dataclass
class Relacion:
    """La unidad del análisis: una obligación frente a la evidencia hallada."""
    obligacion: Obligacion
    periodo: str
    estado: str
    artefactos: list[dict] = field(default_factory=list)
    campos_hallados: list[str] = field(default_factory=list)
    campos_no_hallados: list[str] = field(default_factory=list)
    sostenida: P.Sostenida | None = None
    nota: str = ""


def cargar_obligaciones() -> list[Obligacion]:
    """Las obligaciones, tal como las declara la vara sellada.

    No se editan aquí ni se completan: si la Guía no declara periodicidad para
    un numeral, ese numeral llega sin ella y el análisis lo dirá."""
    d = json.loads(_VARA.read_text(encoding="utf-8"))
    fuera = [Obligacion(
        numeral=str(n["numeral"]),
        texto=n.get("obligacion", ""),
        campos_exigidos=list(n.get("campos_exigidos") or []),
        periodicidad=dict(n.get("periodicidad") or {}),
        procedencia_normativa=dict(n.get("_procedencia") or {}),
        estructura_formal=dict(n.get("estructura_formal") or {}),
    ) for n in d["numerales"]]

    # El art. 24 vive aparte en la vara —es la obligación específica de los GAD,
    # no un numeral del art. 19— y el portal le da su propia entrada. Omitirlo
    # dejaba 48 artefactos «sin obligación identificada» que sí la tienen, y de
    # las más importantes: es donde la norma pide las ACTAS del Concejo.
    a24 = d.get("articulo_24_gad")
    if a24:
        fuera.append(Obligacion(
            numeral="Art.24",
            texto=a24.get("obligacion", "Obligación específica de los GAD · art. 24"),
            campos_exigidos=list(a24.get("campos_exigidos") or []),
            periodicidad=dict(a24.get("periodicidad") or {}),
            procedencia_normativa=dict(a24.get("_procedencia") or {}),
            estructura_formal=dict(a24.get("estructura_formal") or {}),
        ))
    return fuera


def _clave(numeral: str) -> str:
    """Cómo nombra el portal de la DPE al numeral.

    ⚠️ SE CORRIGIÓ EN LA PRIMERA CORRIDA (2026-08-20). El mapeo devolvía `"5"`
    para los numerales 5 y 22, pero **el portal los publica juntos bajo
    `Numeral 5-22`**: la búsqueda no encontraba nada y la matriz declaraba
    «numeral 5 sin evidencia hallada» habiendo 30 artefactos. Un falso hallazgo
    producido por el instrumento, no por el GAD — el mismo patrón que este
    dominio lleva toda la sesión corrigiendo."""
    return {"5": "5-22", "22": "5-22", "Art.24": "Art."}.get(numeral, numeral)


def evidencia_por_numeral(anio: int) -> dict[str, list[dict]]:
    """Qué se descargó para cada numeral, con su identidad física.

    Se une el índice de descargas —que sabe de qué numeral y período es cada
    archivo— con el inventario —que sabe qué ES cada artefacto—."""
    idx = json.loads(_INDICE.read_text(encoding="utf-8"))["archivos"]
    inv = {}
    if _INVENTARIO.exists():
        inv = {a.get("url"): a
               for a in json.loads(_INVENTARIO.read_text(encoding="utf-8"))["artefactos"]}

    fuera: dict[str, list[dict]] = defaultdict(list)
    for a in idx:
        if str(a.get("anio")) != str(anio):
            continue
        num = (a.get("numeral") or "").replace("Numeral ", "").split(" ")[0]
        if not num:
            continue
        reg = {"archivo": a.get("archivo"), "mes": a.get("mes"),
               "sha256": a.get("sha256"), "estado": a.get("estado"),
               "ruta": a.get("ruta")}
        detalle = inv.get(a.get("url"))
        if detalle:
            reg["naturaleza"] = detalle.get("naturaleza_material")
        fuera[num].append(reg)
    return dict(fuera)


def campos_publicados(numeral: str, anio: int) -> set[str]:
    """Qué campos aparecen realmente en los conjuntos de datos publicados.

    Se leen del análisis de contenido, que ya normalizó codificación y
    delimitador. Hallar un campo prueba su presencia; **no hallarlo no prueba su
    ausencia** —puede publicarse con otro nombre— y por eso el resultado se usa
    para acreditar, nunca para negar (lección del numeral 8)."""
    if not _CONTENIDO.exists():
        return set()
    d = json.loads(_CONTENIDO.read_text(encoding="utf-8"))
    filas = d.get("conjuntos") or d.get("archivos") or []
    fuera: set[str] = set()
    for c in filas:
        num = (c.get("numeral") or "").replace("Numeral ", "").split(" ")[0]
        if num != numeral or str(c.get("anio")) != str(anio):
            continue
        for cab in (c.get("cabecera") or c.get("campos") or []):
            if cab:
                fuera.add(str(cab).strip())
    return fuera


def _procedencia_de(o: Obligacion, artefactos: list[dict]) -> P.Procedencia:
    """Las siete respuestas para esta relación concreta."""
    con_sha = [a for a in artefactos if a.get("sha256")]
    captura = ""
    if _INDICE.exists():
        captura = _dt.datetime.fromtimestamp(
            _INDICE.stat().st_mtime).isoformat(timespec="minutes")
    return P.Procedencia(
        fuente="Portal Nacional de Transparencia · Defensoría del Pueblo",
        captura=captura,
        estado_adquisicion=("descargado" if con_sha else
                            "sin_publicacion_registrada" if not artefactos else
                            "descarga_incompleta"),
        evidencia=con_sha[0]["sha256"][:16] if con_sha else "",
        verificador="materializacion.evaluar" if con_sha else "",
        # 2026-08-26 · deuda #1. Apuntaba a `test_la_ausencia_de_artefacto_no_es_
        # incumplimiento`, que comprueba los NOMBRES de los estados y nunca llama a
        # `evaluar()`. Prueba real, verificador real, sin relación entre ambos —y
        # ninguna otra prueba lo ejercitaba. `respalda()` ahora exige que la prueba
        # nombre al verificador, así que esta referencia degradaba la afirmación.
        prueba_del_verificador=(
            "test_evaluar_no_afirma_incumplimiento_cuando_no_halla_evidencia"
            if con_sha else ""),
        sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}",
    )


def evaluar(o: Obligacion, anio: int, evidencia: dict[str, list[dict]]) -> Relacion:
    """Confronta UNA obligación con la evidencia hallada.

    El estado describe la relación, no el archivo, y en ningún caso afirma
    cumplimiento: eso es calificación jurídica."""
    arte = evidencia.get(_clave(o.numeral), [])
    publicados = campos_publicados(_clave(o.numeral), anio)

    hallados = [c for c in o.campos_exigidos
                if any(c.lower() in p.lower() or p.lower() in c.lower()
                       for p in publicados)]
    no_hallados = [c for c in o.campos_exigidos if c not in hallados]

    if not arte:
        estado = SIN_EVIDENCIA
        nota = ("no se halló publicación para esta obligación en el período. "
                "Ausencia de evidencia, NO incumplimiento: la calificación "
                "jurídica corresponde al motor normativo.")
    elif o.campos_exigidos and not hallados:
        estado = PARCIAL
        nota = ("hay publicación pero ninguno de los campos exigidos se "
                "reconoció por nombre. NO prueba su ausencia: pueden estar "
                "publicados con otra denominación (lección del numeral 8).")
    elif no_hallados:
        estado = PARCIAL
        nota = f"{len(hallados)}/{len(o.campos_exigidos)} campos reconocidos por nombre"
    else:
        estado = MATERIALIZADA
        nota = "la evidencia acredita los campos que la obligación enumera"

    proc = _procedencia_de(o, arte)
    sost = P.sostener(f"numeral {o.numeral}: {estado}", proc,
                      P.HECHO_VERIFICABLE)
    if sost.peso == P.NO_DETERMINABLE:
        estado = NO_DETERMINABLE

    return Relacion(obligacion=o, periodo=str(anio), estado=estado,
                    artefactos=arte, campos_hallados=hallados,
                    campos_no_hallados=no_hallados, sostenida=sost, nota=nota)


def artefactos_sin_obligacion(anio: int, evidencia: dict[str, list[dict]],
                              obligaciones: list[Obligacion]) -> list[dict]:
    """Lo que se publicó y no se pudo asociar a ninguna obligación conocida.

    ⚠️ NO SE INTERPRETA. Puede significar cuatro cosas y sólo una de ellas es
    «el GAD publica lo que nadie le pide»: puede que no hallásemos la relación
    normativa, que exista una obligación transversal, que sea materialización
    complementaria, o que efectivamente no sea exigido. **Eso se determina, no
    se presume** (Javo, 2026-08-20)."""
    conocidos = {_clave(o.numeral) for o in obligaciones}
    return [{"numeral_portal": num, "artefactos": len(arte),
             "estado": "sin_obligacion_identificada",
             "lectura": "limitación del análisis, no hallazgo sobre el sujeto"}
            for num, arte in evidencia.items() if num not in conocidos]


def construir(anio: int) -> dict:
    """La matriz completa: cada obligación con su evidencia y su afirmación."""
    obligaciones = cargar_obligaciones()
    evidencia = evidencia_por_numeral(anio)
    relaciones = [evaluar(o, anio, evidencia) for o in obligaciones]
    huerfanos = artefactos_sin_obligacion(anio, evidencia, obligaciones)

    return {
        "_meta": {
            "que_es": "matriz de trazabilidad normativa-documental: la relación "
                      "verificable entre obligación, objeto exigible, evidencia "
                      "y afirmación sobre el sujeto",
            "regla": "la ausencia de un artefacto no constituye incumplimiento: "
                     "constituye ausencia de evidencia respecto de una obligación "
                     "cuya materialización esperada fue determinada por el corpus",
            "limite": "este módulo NO califica jurídicamente · describe la "
                      "relación entre obligación y evidencia",
            "generado": _dt.date.today().isoformat(),
            "sujeto": f"{S.POR_DEFECTO} {S.nombre_corto()}",
            "sujeto_huella": S.huella(),
            "anio": anio,
            "obligaciones": len(obligaciones),
        },
        "relaciones": [{
            "numeral": r.obligacion.numeral,
            "obligacion": r.obligacion.texto[:220],
            "procedencia_normativa": r.obligacion.procedencia_normativa,
            "campos_exigidos": len(r.obligacion.campos_exigidos),
            "campos_reconocidos": r.campos_hallados,
            "campos_no_reconocidos": r.campos_no_hallados,
            "periodicidad_declarada": r.obligacion.periodicidad_declarada,
            "artefactos_hallados": len(r.artefactos),
            "estado_materializacion": r.estado,
            "peso_de_la_afirmacion": r.sostenida.peso if r.sostenida else None,
            "explicacion": P.explicar(r.sostenida) if r.sostenida else "",
            "nota": r.nota,
        } for r in relaciones],
        "sin_obligacion_identificada": huerfanos,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", type=int, default=2025)
    ap.add_argument("--json", default=str(_SALIDA))
    args = ap.parse_args()

    m = construir(args.anio)
    rel = m["relaciones"]
    print(f"MATRIZ DE MATERIALIZACIÓN · {m['_meta']['sujeto']} · {args.anio}")
    print("obligación → objeto exigible → evidencia → afirmación\n")

    from collections import Counter
    for k, v in Counter(r["estado_materializacion"] for r in rel).most_common():
        print(f"   {k:28} {v:4}")
    print()
    for k, v in Counter(r["peso_de_la_afirmacion"] for r in rel).most_common():
        print(f"   peso {str(k):23} {v:4}")

    print("\n  OBLIGACIONES SIN EVIDENCIA HALLADA")
    for r in rel:
        if r["estado_materializacion"] == "sin_evidencia_hallada":
            print(f"     numeral {r['numeral']:5} {r['obligacion'][:62]}")

    if m["sin_obligacion_identificada"]:
        print("\n  ⚠ publicaciones sin obligación identificada "
              "(limitación del análisis, NO hallazgo):")
        for h in m["sin_obligacion_identificada"]:
            print(f"     {h['numeral_portal']:12} {h['artefactos']:4} artefactos")

    p = Path(args.json)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  → {p.relative_to(RAIZ) if p.is_absolute() else p}")


if __name__ == "__main__":
    main()
