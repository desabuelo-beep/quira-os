"""
app/agents/d07/etapas.py — las capacidades que QUIRA ejecuta por sí misma
=========================================================================
POR QUÉ EXISTE (2026-08-18). Javo, tras leer que «671 PDF son legibles»:

> *«Si Claude lo dice, por ser Claude. Pero Claude no es QUIRA. Estamos
> construyendo un ecosistema que deberá reportar más adelante 222 municipios,
> sin Claude, solo QUIRA. Parece que siempre se olvida: este no es un trabajo
> puntual.»*

La auditoría le dio la razón de forma incómoda: de 31 scripts en
`scripts/normativa/`, **uno solo era invocable desde la aplicación**. Captura,
descarga, verificación de enlaces, análisis de contenido e inventario existían
únicamente si una persona los ejecutaba a mano. La cadena real era:

    Claude corre scripts → deja JSON en data/ → el orquestador los lee
    sin Claude: el orquestador no tiene qué leer

Y el propio gate `EVIDENCIA` lo confesaba —*«ejecute la captura primero»*— el
mismo día en que se firmaba ADR-051, titulado «QUIRA ejecuta sin Claude».

QUÉ HACE ESTE MÓDULO. Convierte cada script suelto en una **etapa invocable del
agente**: el orquestador la llama, ella se ejecuta y devuelve un estado tipado.
Nadie tiene que abrir una terminal.

POR QUÉ SE INVOCA COMO PROCESO Y NO SE COPIA EL CÓDIGO. Los scripts ya están
probados contra el caso real y llevan dentro las correcciones de toda la sesión
—colisión de nombres, delimitador por estabilidad, Nextcloud `/download`,
insensibilidad a caja, topes que ocultaban evidencia—. Duplicar esa lógica aquí
crearía dos verdades que se desincronizarían. Se invoca lo probado y se registra
su resultado; la migración de cada script a módulo es refactor posterior, y su
orden lo fija la deuda declarada abajo, no la comodidad.

LO QUE ESTO **NO** RESUELVE TODAVÍA, y se declara para no repetir el error:
la etapa devuelve `ejecutada` o `fallida`, pero **no valida que su salida sea
correcta**. Que un script termine con código 0 no prueba que capturó todo — eso
lo dicen los gates del orquestador, que corren después.

Dylus Lab © 2026
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
_SCRIPTS = RAIZ / "scripts" / "normativa"

# Con qué insumos se produjo cada salida. Sin este registro, «rehacer» y «cambió»
# son indistinguibles y el sistema o recalcula de más o mide sobre datos viejos.
_SELLO_CADENA = RAIZ / "data" / "d07" / "cadena_estado.json"


@dataclass
class ResultadoEtapa:
    """Lo que una etapa devuelve al orquestador. Nunca un booleano: un `False`
    no distingue «no había nada que hacer» de «falló a mitad»."""
    etapa: str
    estado: str                  # ejecutada · omitida · fallida · no_disponible
    segundos: float = 0.0
    detalle: str = ""
    salidas: list[str] = field(default_factory=list)
    codigo: int | None = None


# Las etapas del dominio, en el orden en que deben correr. Cada una declara qué
# produce, para que el orquestador pueda saltarla si el artefacto ya existe y
# NO se vuelva a golpear la fuente sin necesidad.
ETAPAS = [
    {
        "id": "captura",
        "script": "capturar_lotaip_dpe.py",
        "args": ["--escribir"],
        "produce": ["data/lotaip/dpe_montecristi.json"],
        "consume": [],
        "descripcion": "consulta la API de la Defensoría e indexa lo publicado",
    },
    {
        "id": "descarga",
        "script": "descargar_lotaip.py",
        "args": [],
        "produce": ["data/lotaip/descargas_indice.json"],
        "consume": ["data/lotaip/dpe_montecristi.json"],
        "descripcion": "descarga los conjuntos de datos con SHA256 y anti-colisión",
    },
    {
        "id": "contenido",
        "script": "analizar_contenido_lotaip.py",
        "args": ["--json", "data/lotaip/contenido.json"],
        "produce": ["data/lotaip/contenido.json"],
        "consume": ["data/lotaip/descargas_indice.json"],
        "descripcion": "lee los CSV: campos, ausencias declaradas, enlaces",
    },
    {
        "id": "enlaces",
        "script": "verificar_enlaces_lotaip.py",
        "args": [],
        "produce": ["data/lotaip/enlaces.json"],
        "consume": ["data/lotaip/contenido.json"],
        "bandera_rehacer": "--rehacer",
        "descripcion": "comprueba que los enlaces entreguen el documento",
    },
    {
        "id": "inventario",
        "script": "inventario_documental.py",
        "args": ["--json", "data/lotaip/inventario_documental.json"],
        "produce": ["data/lotaip/inventario_documental.json"],
        "consume": ["data/lotaip/enlaces.json"],
        "descripcion": "qué ES cada artefacto: firma real, SHA, legibilidad",
    },
    {
        "id": "contenedores",
        "script": "inventario_contenido.py",
        "args": ["--json", "data/lotaip/contenido_contenedores.json"],
        "produce": ["data/lotaip/contenido_contenedores.json"],
        "consume": ["data/lotaip/inventario_documental.json"],
        "descripcion": "abre los contenedores y clasifica lo que guardan dentro",
    },
]

# CADUCIDAD DE LO QUE MIRA HACIA AFUERA. Sólo las dos etapas que golpean la
# fuente caducan por calendario: el portal cambia, y una captura de hace un
# trimestre describe un portal que ya no existe. Se fija en 30 días porque la
# corrida del dominio es mensual.
#
# Las etapas derivadas NO caducan por fecha: caducan cuando **su insumo cambió**.
# Eso es lo que evita el error inverso —recalcular sin motivo— y, sobre todo, el
# error grave: analizar con un resultado viejo una descarga nueva. Con 222
# municipios nadie va a recordar qué se rehizo y qué no; lo tiene que saber el
# sistema.
VIGENCIA_DIAS = {"captura": 30, "descarga": 30}

# Tiempos máximos por etapa. Un tope que corta en silencio ya ocultó evidencia
# una vez (94 artefactos donde había 935): aquí el corte produce estado
# `fallida` con su causa, nunca un resultado a medias que parezca completo.
TIMEOUT = {
    "captura": 900, "descarga": 1800, "contenido": 600,
    "enlaces": 1800, "inventario": 2400, "contenedores": 1200,
}


def disponible(etapa: dict) -> bool:
    return (_SCRIPTS / etapa["script"]).exists()


def ya_producida(etapa: dict) -> bool:
    """¿Existe en disco lo que esta etapa produce? Existir no es estar al día:
    para eso está `al_dia`. Se conserva porque responde otra pregunta."""
    return all((RAIZ / s).exists() for s in etapa["produce"])


def _mtime(rel: str) -> float:
    p = RAIZ / rel
    return p.stat().st_mtime if p.exists() else 0.0


def _sha(rel: str) -> str:
    p = RAIZ / rel
    if not p.exists():
        return ""
    h = hashlib.sha256()
    with p.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def _leer_sello() -> dict:
    if _SELLO_CADENA.exists():
        try:
            return json.loads(_SELLO_CADENA.read_text(encoding="utf-8"))
        except Exception:                                # noqa: BLE001
            return {}
    return {}


def _sujeto_actual() -> str:
    """Sobre quién se está ejecutando. Se lee del perfil, no se supone."""
    try:
        from app.agents import sujeto as S
        return f"{S.POR_DEFECTO} {S.nombre_corto()}"
    except Exception:                                    # noqa: BLE001
        return ""


def _huella_actual() -> str:
    try:
        from app.agents import sujeto as S
        return S.huella()
    except Exception:                                    # noqa: BLE001
        return ""


def _sellar(etapa: dict) -> None:
    """Registra con qué insumos se produjo esta salida.

    Es lo que permite distinguir «el insumo cambió» de «el insumo se volvió a
    escribir igual». La fecha de modificación no sabe esa diferencia; el SHA sí,
    y con 222 municipios esa diferencia son horas de red que no hay que gastar."""
    s = _leer_sello()
    s[etapa["id"]] = {
        "insumos": {i: _sha(i) for i in etapa.get("consume", [])},
        "salidas": {o: _sha(o) for o in etapa["produce"]},
        "sellado": _dt.datetime.now().isoformat(timespec="seconds"),
        # Quién la corrió. Es lo único que separa «existe el programa» de «QUIRA
        # lo ejecuta»: sin este registro, el grado de apropiación (ADR-051 §2d)
        # sería una afirmación en vez de una medición.
        "ejecutada_por": "agente",
        # ⚠️ AUTODECLARADO, y se dice. El colega lo separó bien (2026-08-19):
        # la identidad del ejecutor es **metadato de procedencia operacional**,
        # no una dimensión epistemológica de la afirmación. Lo escribe el propio
        # módulo, así que no es infalsificable: hoy no distingue una corrida del
        # agente de una que un operador dispare desde una terminal. Se registra
        # su nivel de confianza para que nadie lo lea como prueba.
        "confianza_del_ejecutor": "autodeclarado",
        # …y SOBRE QUIÉN. «Sé descargar conjuntos de datos» y «sé descargarlos
        # del portal de Montecristi» no son la misma afirmación (colega,
        # 2026-08-19): sin el sujeto, el grado miente por omisión.
        "sujeto": _sujeto_actual(),
        # La etiqueta es para leer; la huella es para verificar. Sin ella,
        # cambiar la identidad en la fuente pasaba inadvertido (ataque 2026-08-19).
        "sujeto_huella": _huella_actual(),
    }
    _SELLO_CADENA.parent.mkdir(parents=True, exist_ok=True)
    _SELLO_CADENA.write_text(json.dumps(s, ensure_ascii=False, indent=1),
                             encoding="utf-8")


def al_dia(etapa: dict) -> tuple[bool, str]:
    """¿Hace falta correr esta etapa? Devuelve la razón, siempre.

    ⚠️ POR QUÉ ESTA FUNCIÓN Y NO UN `exists()`. La versión anterior saltaba la
    etapa con sólo ver el archivo en disco. Sobre un municipio recién capturado
    da igual; sobre 222 municipios en corridas mensuales produce el peor error
    posible —**analizar con un resultado viejo una descarga nueva**— y lo
    produce en silencio, porque todos los archivos existen y nada falla.

    Dos causas de caducidad, y ninguna se puede sustituir por la otra:
      · calendario  — sólo lo que mira a la fuente (`VIGENCIA_DIAS`)
      · dependencia — el insumo con el que se produjo ya no es el que hay
    """
    faltan = [s for s in etapa["produce"] if not (RAIZ / s).exists()]
    if faltan:
        return False, f"nunca se produjo {Path(faltan[0]).name}"

    salida = min(_mtime(s) for s in etapa["produce"])

    dias = VIGENCIA_DIAS.get(etapa["id"])
    if dias is not None:
        edad = (time.time() - salida) / 86400
        if edad > dias:
            return False, (f"la última consulta a la fuente tiene {edad:.0f} días "
                           f"(vence a los {dias})")

    sello = _leer_sello().get(etapa["id"])

    # ⚠️ ¿SOBRE QUIÉN SE PRODUJO ESTO? (2026-08-19 · prueba adversarial 8). Un
    # resultado sellado observando al GAD 001 no sirve para medir al 002, aunque
    # el archivo esté fresco y su insumo no haya cambiado. Antes de esta
    # comprobación, alterar el sujeto dejaba TODO en verde: ninguna etapa
    # pendiente, ningún gate en rojo, corrida COMPLETED — y el informe afirmando
    # «reproducible sobre 130802» mientras medía a 130801.
    if sello and sello.get("sujeto") and sello["sujeto"] != _sujeto_actual():
        return False, (f"se produjo observando a «{sello['sujeto']}» y el sujeto "
                       f"activo es «{_sujeto_actual()}»")
    # …y la identidad completa, no sólo el nombre: cambiar el identificador del
    # GAD en la fuente no altera la etiqueta pero sí a quién se está observando.
    if sello and sello.get("sujeto_huella") and sello["sujeto_huella"] != _huella_actual():
        return False, ("la identidad del sujeto en las fuentes cambió desde que "
                       "se produjo esta evidencia")

    for ins in etapa.get("consume", []):
        if sello and ins in sello.get("insumos", {}):
            # Comparación por contenido: rehacer una etapa y obtener el mismo
            # resultado NO invalida a los que dependen de ella.
            if _sha(ins) != sello["insumos"][ins]:
                return False, f"su insumo {Path(ins).name} cambió de contenido"
        elif _mtime(ins) > salida:
            # Sin sello —evidencia producida a mano antes de que existiera este
            # módulo— se cae a la fecha. Es más grosero y puede rehacer de más,
            # que es el lado seguro del error.
            return False, f"su insumo {Path(ins).name} es más nuevo (sin sello previo)"

    return True, "al día"


def ejecutar_etapa(etapa: dict, forzar: bool = False) -> ResultadoEtapa:
    """Corre una etapa y devuelve su estado. No juzga la calidad de la salida:
    de eso se ocupan los gates del orquestador, que corren después."""
    eid = etapa["id"]
    if not disponible(etapa):
        return ResultadoEtapa(eid, "no_disponible",
                              detalle=f"falta {etapa['script']}")
    vigente, razon = al_dia(etapa)
    if vigente and not forzar:
        return ResultadoEtapa(eid, "omitida", salidas=etapa["produce"],
                              detalle=razon)

    # Forzar la etapa debe forzar el TRABAJO, no sólo saltarse el «al día». Los
    # scripts que reanudan desde su salida anterior necesitan que se les diga
    # explícitamente; sin esto, `forzar=True` producía una etapa «ejecutada» que
    # se había copiado a sí misma (2026-08-19).
    args_efectivos = list(etapa["args"])
    if forzar and etapa.get("bandera_rehacer"):
        args_efectivos.append(etapa["bandera_rehacer"])

    t0 = time.perf_counter()
    try:
        r = subprocess.run(
            [sys.executable, str(_SCRIPTS / etapa["script"]), *args_efectivos],
            cwd=str(RAIZ), capture_output=True,
            timeout=TIMEOUT.get(eid, 900))
        seg = round(time.perf_counter() - t0, 1)
        if r.returncode != 0:
            cola = (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()
            return ResultadoEtapa(eid, "fallida", seg, codigo=r.returncode,
                                  detalle=cola[-1][:160] if cola else "sin detalle")
        _sellar(etapa)
        return ResultadoEtapa(eid, "ejecutada", seg, salidas=etapa["produce"],
                              codigo=0)
    except subprocess.TimeoutExpired:
        return ResultadoEtapa(eid, "fallida", round(time.perf_counter() - t0, 1),
                              detalle=f"superó el tiempo máximo ({TIMEOUT.get(eid)}s) — "
                                      f"la salida puede estar incompleta y NO se da por buena")


def preparar_evidencia(forzar: bool = False,
                       hasta: str | None = None) -> list[ResultadoEtapa]:
    """Ejecuta la cadena de adquisición completa.

    Es la función que el orquestador llama cuando falta evidencia, y la que
    convierte «ejecute la captura primero» en algo que el sistema hace solo.
    Se detiene en la primera etapa fallida: seguir con evidencia incompleta
    produciría una medición que parece válida y no lo es."""
    fuera: list[ResultadoEtapa] = []
    for etapa in ETAPAS:
        r = ejecutar_etapa(etapa, forzar=forzar)
        fuera.append(r)
        if r.estado == "fallida":
            break
        if hasta and etapa["id"] == hasta:
            break
    return fuera


def estado_evidencia() -> dict:
    """Qué artefactos existen y cuáles están al día. El orquestador lo usa para
    decidir si necesita adquirir antes de medir, y la UI para mostrar qué falta.

    Es también la respuesta a «¿qué puede hacer QUIRA por sí misma?», que hasta
    hoy sólo se podía contestar leyendo el disco a mano."""
    fuera = {}
    for e in ETAPAS:
        vigente, razon = al_dia(e)
        prod = ya_producida(e)
        fuera[e["id"]] = {
            "producido": prod,
            "al_dia": vigente,
            "razon": razon,
            "script_disponible": disponible(e),
            "descripcion": e["descripcion"],
            "edad_dias": (round((time.time() - min(_mtime(s) for s in e["produce"]))
                                / 86400, 1) if prod else None),
        }
    return fuera


def pendientes() -> list[str]:
    """Las etapas que el agente correría ahora mismo si se le manda medir."""
    return [e["id"] for e in ETAPAS if not al_dia(e)[0]]

# ══════════════════════════════════════════════════════════════════════════════
# LO QUE NO ES ETAPA, Y POR QUÉ
# ══════════════════════════════════════════════════════════════════════════════
# La auditoría del 2026-08-19 contó 31 programas en `scripts/normativa/` y uno
# solo invocable desde la aplicación. Convertirlos todos en etapas habría sido
# la respuesta fácil y equivocada: **no todo programa debe ser una capacidad
# operativa**. Hay una distinción que el canon necesita fijar:
#
#     construcción del canon  corre UNA vez, bajo criterio humano, y su producto
#                             se sella con SHA (la vara, el catálogo, los ACK)
#     capacidad operativa     corre CADA mes, en 222 municipios, sin nadie
#
# Confundirlas tiene dos costos opuestos y ambos graves: automatizar la primera
# deja que el sistema se cambie su propia vara; dejar la segunda a mano es lo
# que Javo señaló hoy. Por eso cada programa queda clasificado, y una prueba
# verifica que **ninguno quede sin clasificar** — la lista no puede envejecer en
# silencio.
NO_SON_ETAPAS = {
    "construccion_del_canon": {
        "razon": "produce la vara con la que se mide; su salida se sella y NO se "
                 "regenera sola — un sistema que se reescribe su propio patrón "
                 "no mide nada",
        "scripts": ["extraer_exigencias_lotaip.py", "extraer_matriz_lotaip.py",
                    "enriquecer_catalogo_d07.py", "register_ack.py",
                    "manifest.py", "validate_f01.py"],
    },
    "biblioteca": {
        "razon": "no es ejecutable: lo importan otros módulos",
        "scripts": ["invariantes.py", "chunker.py"],
    },
    "ingesta_de_corpus": {
        "razon": "alimenta C1/C2 (corpus y grafo), no la corrida de d07 · cuesta "
                 "embeddings y no corre sin autorización de gasto",
        "scripts": ["ingest.py",   # el único que la app ya invocaba antes de hoy
                    "backup_corpus.py", "migrate.py", "reingerir_instrumentos.py",
                    "reingesta_replace.py", "load_c01_neo4j.py",
                    "extend_lopc_neo4j.py", "extend_dom09_cootad266.py"],
    },
    "otro_dominio": {
        "razon": "pertenece a d01/d02; su lugar es la cadena de ese dominio",
        "scripts": ["extraer_cedula.py", "extraer_pac.py", "extraer_pai.py",
                    "extraer_poa_xlsx.py", "cruce_poa_cedula.py"],
    },
    "superado": {
        "razon": "reemplazado por una pieza del agente; se conserva por el caso "
                 "que aún cubre",
        "scripts": ["medir_lotaip.py",            # → orquestador.py
                    "capturar_lotaip_portal.py"],  # → la DPE es API (OBS-QNKC-02);
                                                   #   sirve a GAD fuera de la DPE
    },
    "etapa_bajo_demanda": {
        "razon": "capacidad del agente (`analizar_documentos`), pero NO en la "
                 "corrida automática: abre uno por uno los documentos enlazados "
                 "de un numeral y eso son horas de red · el sistema sabe hacerlo; "
                 "cuándo hacerlo es una decisión, no un descuido",
        "scripts": ["analizar_documentos_lotaip.py"],
    },
}


def clasificacion_scripts() -> dict:
    """Cada programa de `scripts/normativa/`, y qué es dentro del sistema.

    Responde de una vez la pregunta que hubo que contestar leyendo código:
    ¿qué de todo esto puede hacer QUIRA sola, y qué sigue dependiendo de que
    alguien abra una terminal?"""
    fuera = {e["script"]: "etapa_del_agente" for e in ETAPAS}
    for clase, d in NO_SON_ETAPAS.items():
        for s in d["scripts"]:
            fuera[s] = clase
    return fuera

# ── Bajo demanda · el análisis pormenorizado ────────────────────────────────────
# Javo, sobre el monitoreo que sólo miraba si el archivo existía:
#
# > *«Sería algarete que QUIRA deje ese análisis tan básico. Debe revisar todos
# > los documentos del GAD —Excel, PDF, etc.— de los links para determinar su
# > cumplimiento.»*
#
# Esa revisión abre cada documento enlazado: descarga, extrae texto, clasifica la
# clase de acto y busca el correlativo. Es la que encontró **0 actas en 254
# documentos** del art. 24. No corre en cada corrida porque cuesta horas de red;
# corre cuando se la manda, desde la aplicación, sin abrir una terminal.
_DOCUMENTOS = {
    "id": "documentos",
    "script": "analizar_documentos_lotaip.py",
    "args": [],
    "produce": [],
    "consume": ["data/lotaip/descargas_indice.json"],
    "descripcion": "abre los documentos enlazados de un numeral y los clasifica",
}


def _slug(numeral: str) -> str:
    """`Art. 24` → `a24` · `Numeral 18` → `n18`. Mantiene el nombre que ya
    llevan los análisis hechos, para no partir la serie."""
    import re
    m = re.search(r"(\d+)", numeral)
    ini = "a" if numeral.strip().lower().startswith("art") else "n"
    return f"{ini}{m.group(1) if m else '0'}"


def analizar_documentos(numeral: str, limite: int = 0,
                        forzar: bool = False) -> ResultadoEtapa:
    """Abre los documentos enlazados de un numeral. Devuelve estado tipado.

    El resultado va a un archivo por numeral: un único `documentos.json` haría
    que cada análisis borrara al anterior y el dominio perdería su serie."""
    salida = f"data/lotaip/documentos_{_slug(numeral)}.json"
    etapa = dict(_DOCUMENTOS, produce=[salida],
                 args=["--numeral", numeral, "--json", salida]
                      + (["--limite", str(limite)] if limite else []))
    r = ejecutar_etapa(etapa, forzar=forzar)
    return ResultadoEtapa(f"documentos:{_slug(numeral)}", r.estado, r.segundos,
                          r.detalle, r.salidas, r.codigo)


def numerales_analizados() -> dict:
    """Qué numerales ya tienen su análisis documental y cuáles no.

    Es la respuesta a «¿está completo el dominio?» sin que nadie tenga que
    listar el directorio a mano."""
    import json as _json
    fuera = {}
    for f in sorted((RAIZ / "data" / "lotaip").glob("documentos_*.json")):
        try:
            meta = _json.loads(f.read_text(encoding="utf-8")).get("_meta", {})
        except Exception:                                # noqa: BLE001
            meta = {}
        fuera[f.stem.replace("documentos_", "")] = {
            "archivo": f.name,
            "generado": meta.get("generado"),
            "numeral": meta.get("numeral"),
        }
    return fuera

# ══════════════════════════════════════════════════════════════════════════════
# ESCALERA DE APROPIACIÓN · ADR-051 §2d
# ══════════════════════════════════════════════════════════════════════════════
# El colega, 2026-08-19, sobre la tentación de dar por hecho lo que apenas se
# había instrumentado:
#
# > *«Claude puede descubrir una capacidad. QUIRA debe apropiarse de ella. Sólo
# > después de que QUIRA pueda ejecutarla, conservar su procedencia y demostrar
# > su reproducibilidad puede considerarse parte del sistema.»*
#
# Los tres grados NO se declaran a mano: se **derivan** de lo que se puede
# demostrar. Declararlos sería repetir el error que este dominio combate —
# afirmar más de lo que la evidencia sostiene—, sólo que aplicado a sí mismo.
# Los tres grados y su derivación viven en `app/agents/apropiacion.py`: son de
# QUIRA, no de d07. Aquí sólo se aportan los hechos que este dominio conoce.
from app.agents import apropiacion as A                   # noqa: E402

CAPACIDAD = A.CAPACIDAD
EJECUCION = A.EJECUCION
VALIDADO = A.VALIDADO

# Qué prueba acredita la reproducibilidad de cada etapa. Sin entrada aquí, una
# etapa NO puede alcanzar `validado` por más veces que se haya ejecutado bien:
# funcionar no es lo mismo que estar demostrado.
#
# ⚠️ SÓLO `contenido` FIGURA AQUÍ, y es deliberado. La prueba de
# reproducibilidad ejercita esa etapa y ninguna otra. Listar también `enlaces`,
# `inventario` o `contenedores` las dejaría marcadas como validadas sin que
# ninguna prueba las reconstruya — el mismo error que el dominio corrige en el
# GAD, cometido contra nosotros mismos. Cada una entra el día que tenga su
# prueba, no antes.
PRUEBA_QUE_VALIDA = {
    "contenido": "test_quira_reconstruye_sus_derivados_sin_ayuda",
}


def _grado(etapa: dict):
    """El `Grado` completo —con su sujeto—, que es la unidad real.

    ⚠️ AQUÍ HUBO UN FALLO (2026-08-19). `grados()` reconstruía el objeto a mano
    y **perdía el sujeto por el camino**: el sello lo registraba, la escalera lo
    aceptaba, y aun así el informe decía «sujeto sin acreditar». Es el error que
    el propio colega acababa de advertir —la capacidad separada de su alcance—
    reproducido a las pocas líneas de haberlo corregido en el diseño.""" 
    sello = _leer_sello().get(etapa["id"], {})
    g = A.derivar(etapa["id"], dominio="d07",
                  hay_codigo=disponible(etapa),
                  ejecutada_por_el_agente=sello.get("ejecutada_por") == "agente",
                  prueba=PRUEBA_QUE_VALIDA.get(etapa["id"]),
                  sujeto=sello.get("sujeto", ""))
    if g.grado != A.AUSENTE and sello.get("sellado"):
        g = A.Grado(g.capacidad, g.grado,
                    g.fundamento.replace("QUIRA la ejecutó",
                                         f"QUIRA la ejecutó ({sello['sellado']})"),
                    g.dominio, g.sujeto)
    return g


def grado_de_apropiacion(etapa: dict) -> tuple[str, str]:
    """En qué grado esta capacidad es de QUIRA, y por qué. La escalera es
    transversal (ADR-051 §2d); d07 sólo aporta sus tres hechos."""
    g = _grado(etapa)
    return g.grado, g.fundamento


def _existe_prueba(nombre: str) -> bool:
    """Se conserva el nombre local: lo usan las pruebas del dominio."""
    return A.existe_prueba(nombre)


def grados() -> list:
    """Los grados de d07 como objetos, para que el resumen transversal pueda
    agregarlos junto a los de otros dominios."""
    return [_grado(e) for e in ETAPAS + [_DOCUMENTOS]]


def autonomia() -> dict:
    """El estado de apropiación de todo el dominio, etapa por etapa.

    Responde la pregunta del colega —*«si mañana desaparecen Claude, esta
    conversación y el operador humano, ¿QUIRA puede reproducir el resultado
    desde el origen?»*— con lo que el sistema puede demostrar, no con lo que
    alguien recuerde haber hecho."""
    fuera = {}
    for e in ETAPAS + [_DOCUMENTOS]:
        grado, porque = grado_de_apropiacion(e)
        fuera[e["id"]] = {"grado": grado, "fundamento": porque,
                          "descripcion": e["descripcion"]}
    return fuera
