"""
app/agents/datos.py — CAPA 3 · qué procedencia llevan los artefactos de datos
================================================================================
POR QUÉ ES OTRA CAPA. `procedencia.py` modela la procedencia de **una
afirmación** —«d01 dice que el IPE es X»—. C3 pregunta por la de **los
artefactos**: los 2.213 archivos de `data/`. La deuda #2 de esta sesión ya lo
enunció y sólo se resolvió para cinco:

> *«La procedencia debe viajar con el artefacto hasta el límite en que el
> artefacto pueda ser consumido independientemente de la cadena que lo produjo.»*

EL HALLAZGO DE ESTA CAPA, y no es una acusación:

    1360000430001    27 ensayos · 2026-05-25 → 2026-06-16
    1360001010001   158 ensayos · 2026-08-18 → 2026-09-01
                    NO se solapan — sucesión limpia

**La identidad del sujeto tiene versiones.** El perfil declara hoy
`ruc = 1360001010001`, y su propia nota registra que el campo *«no estaba
huellado»* y se cerró el 2026-08-26. Los 27 artefactos anteriores llevan el RUC
previo — y son **correctos para su época**.

Lo que falta no es corregirlos: es que **ningún artefacto declara bajo qué
versión de la identidad se produjo**. Hoy se reconstruye por la fecha, lo que
exige que alguien recuerde cuándo cambió. Es el mismo patrón que los ADR
anteriores a ADR-035: *no consta ≠ defecto*, y convertirlo en imputación
retroactiva sería el error que este observatorio prohíbe.

⚠️ LÍMITE DEL DETECTOR, aprendido en el intento anterior. Buscar una lista de
marcas —`_procedencia`, `_meta`…— produjo 221 falsos positivos: `ack_registry`
lleva `meta` sin guion, `cadena_estado` guarda sus sellos dentro de las etapas, y
los 185 ensayos declaran `dry_run: true`, que la lista no contemplaba. Se busca
por **patrón y a profundidad**, y aun así el resultado se llama «sin marca
hallada», no «sin procedencia».

Dylus Lab © 2026
"""
from __future__ import annotations

import collections
import json
import re
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "data"

CON_MARCA = "con_marca_de_procedencia"
ENSAYO = "ensayo_declarado"
SIN_MARCA = "sin_marca_hallada"
ILEGIBLE = "ilegible"

# PATRÓN, no lista cerrada: cualquier clave que hable de origen, sello o
# identidad. Una lista escrita a mano es lo que produjo el falso positivo.
_PATRON_PROCEDENCIA = re.compile(
    r"sha|fuente|origen|proceden|sujeto|generado|firma|sello|captura|"
    r"_meta|^meta$|clase_epist|artifact|deriva|dry_run|run_id|ruc", re.I)

_EXCLUIDOS = (
    ("backups/", "copias de seguridad: duplican artefactos ya contados"),
    ("__pycache__", "artefactos de compilación"),
)


def _marcas(o, prof: int = 0) -> list[str]:
    """Claves de procedencia a cualquier profundidad (hasta 3 niveles).

    La procedencia de un artefacto puede vivir dentro de sus etapas y no en la
    raíz — `cadena_estado.json` guarda sus sellos en `captura`, `descarga`… y
    mirar sólo el primer nivel lo daba por huérfano."""
    if prof > 3:
        return []
    out: list[str] = []
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(k, str) and _PATRON_PROCEDENCIA.search(k):
                out.append(k)
            out += _marcas(v, prof + 1)
    elif isinstance(o, list):
        for v in o[:20]:
            out += _marcas(v, prof + 1)
    return out


@lru_cache(maxsize=1)
def artefactos_json() -> list[dict]:
    """Cada JSON de `data/` con lo que se puede decir de su procedencia."""
    salida = []
    for f in sorted(DATOS.rglob("*.json")):
        rel = f.relative_to(RAIZ).as_posix()
        if any(p in rel for p, _ in _EXCLUIDOS):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:                                # noqa: BLE001
            salida.append({"artefacto": rel, "estado": ILEGIBLE, "marcas": []})
            continue
        m = _marcas(d)
        es_ensayo = isinstance(d, dict) and d.get("dry_run") is True
        salida.append({
            "artefacto": rel,
            "estado": ENSAYO if es_ensayo else (CON_MARCA if m else SIN_MARCA),
            "marcas": sorted(set(m))[:6],
            "sujeto_declarado": (d.get("ruc") or d.get("municipio_code") or "")
                                if isinstance(d, dict) else "",
            "fecha": (str(d.get("generated_at") or "")[:10]
                      if isinstance(d, dict) else ""),
        })
    return salida


def identidades_del_sujeto() -> list[dict]:
    """Qué identidades del sujeto aparecen en los artefactos, y cuándo.

    ⚠️ Que un artefacto lleve una identidad distinta de la vigente **no es un
    defecto**: puede ser correcto para su época. Lo que este método permite es
    ver si las versiones se suceden —sucesión limpia— o conviven, que sería
    mucho más grave: dos identidades activas a la vez sobre el mismo sujeto."""
    por: dict[str, list[str]] = collections.defaultdict(list)
    for a in artefactos_json():
        ruc = str(a.get("sujeto_declarado") or "")
        if re.fullmatch(r"\d{10,13}", ruc) and a.get("fecha"):
            por[ruc].append(a["fecha"])
    filas = []
    for ruc, fechas in por.items():
        fs = sorted(fechas)
        filas.append({"identidad": ruc, "artefactos": len(fs),
                      "desde": fs[0], "hasta": fs[-1]})
    filas.sort(key=lambda r: r["desde"])
    for i in range(1, len(filas)):
        filas[i]["solapa_con_anterior"] = filas[i]["desde"] <= filas[i - 1]["hasta"]
    if filas:
        filas[0]["solapa_con_anterior"] = False
    return filas


def cobertura_de_datos() -> dict:
    """La capa 3, con su universo declarado (C0 lo exige)."""
    arts = artefactos_json()
    por_estado = collections.Counter(a["estado"] for a in arts)
    ident = identidades_del_sujeto()
    conviven = [i for i in ident if i.get("solapa_con_anterior")]
    return {
        "artefactos": len(arts),
        "por_estado": dict(por_estado),
        "identidades_del_sujeto": ident,
        "identidades_que_conviven": [i["identidad"] for i in conviven],
        "sin_marca": [a["artefacto"] for a in arts if a["estado"] == SIN_MARCA],
        "universo": {
            "que": "artefactos JSON del directorio de datos",
            "donde": "data/**/*.json",
            "como": "búsqueda de claves de procedencia por PATRÓN y hasta 3 "
                    "niveles de profundidad, no por una lista de nombres",
            "hallados": len(arts),
            "mecanismo": {
                "tipo": "derivado",
                "operacion": "rglob",
                "por_que": "se recorre el árbol de datos; ninguna lista enumera "
                           "los artefactos",
            },
            "exclusiones": [
                {"patron": p, "motivo": m,
                 "autoridad": "decisión de alcance de este módulo, revisable"}
                for p, m in _EXCLUIDOS],
            "fuera_de_alcance": [
                "los 943 CSV, 774 .bin, 16 PDF y 13 xlsx de `data/`: este "
                "detector sólo lee JSON, así que la mayoría del volumen NO está "
                "medida",
                "hallar una clave de procedencia no dice que su contenido sea "
                "correcto — sólo que el artefacto la lleva",
                "una identidad distinta puede ser correcta para su época: este "
                "módulo observa la sucesión, no juzga los valores",
                "⚠️ LA EVIDENCIA PRIMARIA DEL GOLD MASTER NO ESTÁ EN `data/`: son "
                "258 documentos oficiales en `Holding_Municipal_Montecristi` "
                "—web del GAD, pedidos de acceso a la información, SERCOP, "
                "CPCCS— y este universo no los incluye. Se miden aparte, en "
                "`evidencia_primaria()`",
            ],
        },
        "afirmacion_sostenible": _afirmar(arts, por_estado, ident, conviven),
    }


def _afirmar(arts, por_estado, ident, conviven) -> str:
    base = (f"De {len(arts)} artefactos JSON de datos, "
            f"{por_estado.get(CON_MARCA, 0)} llevan alguna marca de procedencia, "
            f"{por_estado.get(ENSAYO, 0)} se declaran ensayos (`dry_run`) y "
            f"{por_estado.get(SIN_MARCA, 0)} no muestran ninguna. **Los CSV, "
            f"binarios y hojas de cálculo —la mayor parte del volumen— no están "
            f"medidos.**")
    if len(ident) > 1:
        base += (f" Se observan {len(ident)} identidades del sujeto en los "
                 f"artefactos fechados: " +
                 " · ".join(f"{i['identidad']} ({i['desde']}→{i['hasta']})"
                            for i in ident) + ".")
        base += (" No se solapan: la sucesión es limpia y cada artefacto puede "
                 "ser correcto para su época."
                 if not conviven else
                 f" ⚠️ CONVIVEN: {', '.join(i['identidad'] for i in conviven)} — "
                 f"dos identidades activas a la vez sobre el mismo sujeto.")
        base += (" Lo que ningún artefacto declara es **bajo qué versión de la "
                 "identidad se produjo**: hoy se reconstruye por la fecha, y eso "
                 "exige recordar cuándo cambió.")
    return base


# ══════════════════════════════════════════════════════════════════════════════
# LA CADENA DE CAPTURA · ¿puede un artefacto volver a su origen?
# ══════════════════════════════════════════════════════════════════════════════
# La pregunta fuerte de C3, formulada por el colega:
#
# > *«¿Puede el sistema reconstruir de manera observable la cadena
# > artefacto → captura → URL/origen → sujeto/periodo?»*
#
# Para los 422 binarios de LOTAIP la respuesta es SÍ, y de la forma más fuerte
# posible: **el nombre del archivo es el SHA-256 de su URL de origen**.
#
#     clave = hashlib.sha256(url.encode()).hexdigest()[:16]
#     p = CACHE / f"{clave}.bin"
#
# El artefacto lleva su procedencia en el nombre, y la correspondencia con
# `inventario_documental.json` es 422/422 en ambas direcciones.
#
# ⚠️ ESTE MÉTODO NACIÓ DE UN FALSO POSITIVO PROPIO, y conviene que quede escrito.
# La primera búsqueda concluyó «422 binarios sin registro de procedencia»: buscó
# la ruta `data/lotaip/artefactos` como texto literal, y el código la **compone**
# (`CACHE = RAIZ / "data" / "lotaip" / "artefactos"`). Era exactamente el límite
# que el grafo de acoplamiento ya declaraba —83% de rutas no resolubles— y que
# el ataque siguiente ignoró al interpretar. **Declarar un límite no sirve si no
# se respeta al leer el resultado.**
RESUELTA = "procedencia_resuelta"
DECLARADA_NO_RESUELTA = "procedencia_declarada_no_resuelta"
SIN_REGISTRO = "sin_registro_de_procedencia"

_INVENTARIO = DATOS / "lotaip" / "inventario_documental.json"
_CACHE_BIN = DATOS / "lotaip" / "artefactos"


def cadena_de_captura() -> dict:
    """Si los binarios capturados pueden volver a su URL de origen.

    `sin_registro` NO significa «sin procedencia»: significa que este mecanismo
    no halló un registro que permita reconstruirla."""
    import hashlib

    if not _INVENTARIO.exists() or not _CACHE_BIN.is_dir():
        return {"estado": "no_determinable",
                "por_que": "no está el inventario o la caché de artefactos"}
    inv = json.loads(_INVENTARIO.read_text(encoding="utf-8")).get("artefactos", [])
    enel_disco = {p.stem for p in _CACHE_BIN.glob("*.bin")}
    claves = {hashlib.sha256(a["url"].encode()).hexdigest()[:16]: a
              for a in inv if a.get("url")}
    casan = enel_disco & set(claves)
    return {
        "estado": RESUELTA if casan and not (enel_disco - set(claves)) else SIN_REGISTRO,
        "binarios": len(enel_disco),
        "registros_con_url": len(claves),
        "correspondencia": len(casan),
        "binarios_sin_registro": sorted(enel_disco - set(claves))[:10],
        "registros_sin_binario": sorted(set(claves) - enel_disco)[:10],
        "como_se_reconstruye": "el nombre del .bin es sha256(url)[:16] — la "
                               "procedencia viaja en el nombre del artefacto",
    }


# ══════════════════════════════════════════════════════════════════════════════
# LA EVIDENCIA PRIMARIA VIVE FUERA DEL REPOSITORIO · corrección de Javo
# ══════════════════════════════════════════════════════════════════════════════
# > *«documentos oficiales no sólo hemos sacado de transparencia… construimos la
# > carpeta Holding_Municipal_Montecristi con los documentos oficiales sacados de
# > la página web del GAD y los pedidos de acceso a la información pública y de
# > otros portales como SERCOP y CPCCS. Lo del DOM de transparencia es ahora, en
# > la construcción del DOM; pero para trabajar el Excel canónico Gold Master,
# > eso se construyó con los documentos de la carpeta local.»*
#
# C3 midió `data/` del repositorio. **La evidencia primaria del Gold Master no
# está ahí**: son 258 documentos —91 xlsx, 59 PDF, 52 docx, 564 MB— organizados
# por dominio (Cédulas Presupuestarias, POA, PAC, Participación, Rendición).
#
# Décima vez el mismo patrón de la sesión: un territorio entero fuera del
# universo. Y el sistema sí lo conocía —`config.DATOS_DIR` apunta ahí y
# `check_portabilidad` lo llama «la frontera»—; quien no lo miró fue este módulo.
def raiz_de_evidencia_primaria() -> Path | None:
    """El territorio de los documentos oficiales. **Derivado de `config`**, nunca
    escrito: el sistema tiene trinquete en 0 rutas fijas."""
    try:
        from config import DATOS_DIR
        h = Path(DATOS_DIR) / "Holding_Municipal_Montecristi"
        return h if h.is_dir() else None
    except Exception:                                    # noqa: BLE001
        return None


def evidencia_primaria() -> dict:
    """Cuántos documentos oficiales puede señalar el sistema — y cuántos no sabe.

    ⚠️ APLICACIÓN DE LA REGLA 2 DE C0 A SÍ MISMO. Este barrido sólo lee JSON y
    YAML del repositorio, y busca por **nombre de archivo**. El Gold Master es un
    `.xlsx` —como 91 de estos documentos— y no se abre aquí. Por eso los no
    hallados NO se llaman «sin trazabilidad»: se llaman `no_determinable`, y el
    motivo viaja con el número. Decir lo contrario sería leer el silencio del
    instrumento como ausencia, que es el error que este sistema acaba de fijar
    como prohibido."""
    H = raiz_de_evidencia_primaria()
    if H is None:
        return {"estado": "no_determinable",
                "por_que": "no se alcanza la raíz de evidencia primaria desde config"}
    # ⚠️ RUIDO DEL SISTEMA DE ARCHIVOS, excluido con motivo. `desktop.ini` no es
    # un documento oficial del GAD: contarlo infla el universo con basura de
    # Windows y ensucia cualquier porcentaje que se derive de él.
    docs = [f for f in H.rglob("*")
            if f.is_file() and f.name.lower() not in ("desktop.ini", "thumbs.db")]
    nombres = {f.name for f in docs}
    citados: set[str] = set()
    quien: dict[str, int] = {}
    for f in list(DATOS.rglob("*.json")) + list(DATOS.rglob("*.yaml")):
        if "backups" in f.as_posix():
            continue
        try:
            t = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = {n for n in nombres if n in t}
        if hits:
            quien[f.relative_to(RAIZ).as_posix()] = len(hits)
            citados |= hits
    return {
        "raiz": H.name,
        # ⚠️ LA UNIDAD, DECLARADA. El colega detectó la incoherencia: 258 − 36
        # da 222 y yo reportaba 204. Ninguno era «documentos sin trazabilidad»
        # — la métrica contaba **nombres únicos** (240, porque 18 se repiten en
        # varias carpetas) y no lo decía. Una cifra sin unidad declarada no es
        # comparable con nada, ni siquiera consigo misma.
        "unidad": "nombres de archivo únicos; un mismo nombre en dos carpetas "
                  "cuenta una vez",
        "documentos": len(docs),
        "nombres_unicos": len(nombres),
        "citados_por_artefactos": len(citados),
        "no_determinables": len(nombres) - len(citados),
        "quien_los_cita": dict(sorted(quien.items(), key=lambda x: -x[1])[:8]),
        "por_carpeta": {d.name: sum(1 for _ in d.rglob("*") if _.is_file())
                        for d in sorted(H.iterdir()) if d.is_dir()},
        "limite": "sólo se buscó el NOMBRE del documento dentro de JSON/YAML del "
                  "repositorio. El Gold Master es .xlsx y no se abre aquí, como "
                  "tampoco los 91 xlsx de este territorio: los no hallados son "
                  "**no determinables**, no documentos sin trazabilidad",
        "territorios_no_inspeccionados": [
            {"territorio": "Supabase · corpus vectorial",
             "estado": "declarado_no_inspeccionado",
             "por_que": "territorio externo; no se consulta sin autorización "
                        "explícita de Javo. La pregunta C3 pendiente es si el "
                        "corpus conserva identidad suficiente del documento para "
                        "volver a la evidencia primaria — vectorizar resuelve "
                        "recuperación semántica, no trazabilidad"},
            {"territorio": "Obsidian · notas de QUIRA",
             "estado": "declarado_no_inspeccionado",
             "por_que": "Javo: «quedó corto… allí se quedó info de QUIRA que "
                        "creo también se toca en la documentación canónica, pero "
                        "desfasada». Territorio conocido, ubicación no declarada "
                        "en el repositorio y contenido posiblemente superado"},
        ],
        "segundo_limite": "buena parte de estos documentos se vectorizó al corpus "
                          "de Supabase —«pero no están todos», Javo— y este "
                          "instrumento NO consulta ese corpus. Un documento "
                          "ausente aquí puede estar trazado allí, y este módulo "
                          "no puede saberlo sin conexión",
    }
