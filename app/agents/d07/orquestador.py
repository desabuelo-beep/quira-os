"""
app/agents/d07/orquestador.py — la corrida del dominio, sin nadie mirando
=========================================================================
POR QUÉ EXISTE (2026-08-17). Javo:

> *«Debemos ir modelando lo que QUIRA debe hacer ya de manera automática, sin la
> ayuda de Claude o Claude supervisando. QUIRA debe realizar todo esto de manera
> independiente cuando se la manda a través de los comandos o botones del
> sistema.»*

La corrida del 2026-08-17 sobre 936 archivos funcionó, pero **cada corrección la
hizo una persona leyendo salidas**: la colisión de nombres que sobrescribió 29
archivos, el delimitador que partía tablas de 9 columnas en 19, los falsos
positivos de ausencia que tomaron el nombre «NAPA MENDOZA GEOVER AUGUSTO» por una
carencia, el visor de Nextcloud confundido con enlace muerto. Ninguna la habría
detectado el sistema solo.

De ahí el principio que gobierna este módulo (colega, 2026-08-17):

> **Cada corrección manual descubierta en una corrida debe terminar convertida en
> regla, gate o prueba automatizada antes de considerar autónomo el dominio.**

Por eso los gates no informan: **detienen**. Una corrida que no puede probar la
integridad de su evidencia no publica un resultado peor — no publica ninguno.

LA CADENA, y dónde puede pararse:

    1 canon      vara sellada + catálogo v1.1.0        gate CANON
    2 evidencia  índice de descargas con SHA           gate EVIDENCIA
    3 integridad rutas únicas, sin sobrescritura       gate INTEGRIDAD
    4 levantar   DPE → EvidenciaCD (determinístico)
    5 cobertura  componentes del canon vs datos
    6 scoring    CTA/ETA/RP/CI → SITA (Instructivo)
    7 hallazgos  tipados, sin narrativa ni IA
    8 persistir  resultado con identidad de corrida

SIN IA. Ni una llamada a un modelo. La fuente canónica es la API de la DPE
(OBS-QNKC-02), que es estructurada, así que las etapas que se creyeron
cognitivas son determinísticas aquí. `reportes.redactar_observacion` sigue sin
usarse a propósito: la narrativa explicable exige presupuesto de API y este
dominio tiene que poder correr sin él.

QUÉ NO HACE: no captura ni descarga —eso son los scripts de `scripts/normativa/`,
que se ejecutan aparte y dejan la evidencia en disco—; no declara
incumplimientos; no escribe en el Gold Master.

Uso:  python -m app.agents.d07.orquestador --anio 2025 [--meses 1-12] [--guardar]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents.d07 import persistencia                       # noqa: E402
from app.agents.d07 import reglas as R                        # noqa: E402
from app.agents.d07.componentes import verificar_cobertura    # noqa: E402
from app.agents.d07.evidencia import levantar_evidencia_local # noqa: E402
from app.agents.d07.scoring import calcular_sita, evaluar_cd  # noqa: E402

_SELLO = RAIZ / "data" / "lotaip" / "VARA_SELLO.json"
_EXIGENCIAS = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
_CATALOGO = RAIZ / "data" / "d07" / "catalogo_cd_d07_v1.1.0.yaml"
_INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
_CORRIDAS = RAIZ / "data" / "d07" / "corridas"

# El sujeto observado se recibe, no se escribe aquí (OBS-032). Cuando esta
# cadena corra sobre el GAD 002, cambia el perfil — no este archivo.
from app.agents import sujeto as _S                       # noqa: E402
MUNICIPIO = _S.nombre_corto().lower()
CODIGO_SUJETO = _S.POR_DEFECTO


@dataclass
class Gate:
    nombre: str
    ok: bool
    detalle: str
    critico: bool = True


@dataclass
class Corrida:
    run_id: str
    municipio: str
    anio: int
    gates: list[Gate] = field(default_factory=list)
    resultados: list[dict] = field(default_factory=list)
    hallazgos: list[dict] = field(default_factory=list)
    canon: dict = field(default_factory=dict)
    # Qué produjo el agente por sí mismo en esta corrida. Queda en el registro
    # para distinguir la evidencia que QUIRA adquirió de la que ya encontró.
    adquisicion: list[dict] = field(default_factory=list)
    estado: str = "EN_CURSO"

    @property
    def bloqueada(self) -> bool:
        return any(g.critico and not g.ok for g in self.gates)


# ── 1-3 · gates de arranque ─────────────────────────────────────────────────────
def _gates_canon(c: Corrida) -> None:
    """Antes de medir a nadie, QUIRA prueba que su propia vara está intacta."""
    if not _SELLO.exists() or not _EXIGENCIAS.exists():
        c.gates.append(Gate("CANON", False, "falta la vara normativa o su sello"))
        return
    sello = json.loads(_SELLO.read_text(encoding="utf-8"))
    actual = hashlib.sha256(_EXIGENCIAS.read_bytes()).hexdigest()
    ok = actual == sello["sha256"]
    c.gates.append(Gate("CANON", ok,
                        f"vara {actual[:16]}… " +
                        ("coincide con el sello" if ok else
                         f"NO coincide con el sello {sello['sha256'][:16]}…")))
    if not _CATALOGO.exists():
        c.gates.append(Gate("CATALOGO", False, "no existe el catálogo v1.1.0"))
        return
    cat_sha = hashlib.sha256(_CATALOGO.read_bytes()).hexdigest()
    c.gates.append(Gate("CATALOGO", True, f"catálogo v1.1.0 {cat_sha[:16]}…"))

    # REGLAS · el dominio no mide sin su Regla Operativa. Antes los criterios vivían
    # en este archivo, así que la corrida siempre podía seguir; ahora, si la RO falta,
    # d07 no tiene con qué medir y debe detenerse en vez de improvisar (ADR-051 §2).
    try:
        estados = R.estado_reglas()
        propuestas = [k for k, v in estados.items() if v != "vigente"]
        c.gates.append(Gate(
            "REGLAS", True,
            " · ".join(f"{k} {v}" for k, v in estados.items()) +
            ("  ⚠ resultado calculado con reglas aún no promovidas" if propuestas else "")))
        c.canon["reglas"] = estados
        c.canon["reglas_vigentes"] = not propuestas
    except R.ReglaNoDisponible as e:
        c.gates.append(Gate("REGLAS", False, f"no se pudo cargar la regla operativa: {e}"))
        return

    c.canon.update({"vara_sha": actual, "catalogo_sha": cat_sha,
                    "sello": sello.get("_meta", {}).get("sellada"),
                    "numerales": sello.get("numerales"),
                    "campos_exigidos": sello.get("campos_exigidos")})


def _gates_evidencia(c: Corrida, adquirir: bool = True) -> None:
    # ⚠️ ANTES ESTE GATE DECÍA «ejecute la captura primero» (2026-08-18). Es
    # decir: el orquestador detectaba que faltaba evidencia y le pedía a una
    # PERSONA que corriera un script. Eso convertía a QUIRA en un calificador de
    # lo que otro había recolectado, no en un sistema autónomo — y contradecía el
    # punto 1 de su propio ADR-051 el mismo día en que se firmó.
    #
    # Javo lo señaló: *«Claude no es QUIRA […] 222 municipios, sin Claude, solo
    # QUIRA»*. Ahora el orquestador ADQUIERE: si falta la evidencia, la produce.
    #
    # La condición NO es «falta el índice». Es «alguna etapa no está al día»:
    # una descarga nueva con un análisis viejo tiene todos los archivos en su
    # sitio y aun así mide sobre datos que ya no corresponden.
    # SUJETO · antes de medir, QUIRA comprueba que la evidencia que tiene se
    # produjo observando a QUIEN va a medir. No se degrada: se DETIENE. Una
    # medición con evidencia de otro municipio no es un resultado más débil —
    # es una afirmación falsa sobre un tercero, y eso no se publica atenuado.
    from app.agents.d07 import etapas as E
    _sello = E._leer_sello()
    _activo = E._sujeto_actual()
    _huella = E._huella_actual()
    _ajenos = {k: v["sujeto"] for k, v in _sello.items()
               if v.get("sujeto") and v["sujeto"] != _activo}
    # Identidad completa, no sólo el nombre visible: un cambio en el
    # identificador del GAD dentro de la fuente deja la etiqueta intacta y
    # convierte la evidencia en ajena (ataque end-to-end 2026-08-19).
    _mutados = {k: "identidad en fuentes alterada" for k, v in _sello.items()
                if v.get("sujeto_huella") and v["sujeto_huella"] != _huella}
    _ajenos.update(_mutados)
    if _ajenos:
        c.gates.append(Gate(
            "SUJETO", False,
            f"evidencia producida sobre otro sujeto que el activo ({_activo}): " +
            " · ".join(f"{k}→{v}" for k, v in _ajenos.items())))
        return
    c.gates.append(Gate("SUJETO", True,
                        f"toda la evidencia se produjo observando a {_activo}"))

    if adquirir:
        pend = E.pendientes()
        if pend:
            c.gates.append(Gate("ADQUISICIÓN", True,
                                f"{len(pend)} etapa(s) por rehacer ({', '.join(pend)}) — "
                                f"el agente las ejecuta; no se pide a nadie",
                                critico=False))
            for r in E.preparar_evidencia():
                c.adquisicion.append({"etapa": r.etapa, "estado": r.estado,
                                      "segundos": r.segundos, "detalle": r.detalle})
                if r.estado == "fallida":
                    c.gates.append(Gate("ADQUISICIÓN", False,
                                        f"etapa «{r.etapa}» falló: {r.detalle}"))
                    return

    if not _INDICE.exists():
        c.gates.append(Gate("EVIDENCIA", False,
                            "no hay índice de descargas y la adquisición no lo produjo"))
        return
    arch = json.loads(_INDICE.read_text(encoding="utf-8"))["archivos"]
    del_anio = [a for a in arch if a.get("anio") == str(c.anio)]
    c.gates.append(Gate("EVIDENCIA", bool(del_anio),
                        f"{len(del_anio)} archivos indexados para {c.anio}"))

    # INTEGRIDAD: dos registros no pueden compartir ruta. El 2026-08-17 un truncado
    # de nombre hizo que 29 archivos distintos se sobrescribieran entre sí, y el
    # análisis los habría dado por buenos. Una colisión silenciosa no produce un
    # error: produce evidencia equivocada, que es peor.
    rutas = [a.get("ruta") for a in del_anio if a.get("ruta")]
    unicas = len(set(rutas))
    sin_sha = sum(1 for a in del_anio
                  if a.get("estado") == "descargado" and not a.get("sha256"))
    ok = unicas == len(rutas) and sin_sha == 0
    c.gates.append(Gate("INTEGRIDAD", ok,
                        f"{unicas}/{len(rutas)} rutas únicas · {sin_sha} sin SHA" +
                        ("" if ok else " — HAY EVIDENCIA SOBRESCRITA, no se publica")))


# ── Procedencia · qué sostiene cada hallazgo (ADR-042 §6-bis) ───────────────────
def _procedencia(cd_id: str, periodo: str, ev=None,
                 verificador: str = "", prueba: str = "") -> "P.Procedencia":
    """Las siete respuestas que este dominio puede dar sobre un hallazgo.

    Antes los hallazgos salían con su `nivel` escrito a mano en el sitio donde
    se creaban. Funcionaba mientras alguien recordara la regla; ahora el peso lo
    decide la cadena, y si una capa no responde **el hallazgo se degrada solo**."""
    from app.agents import procedencia as P
    return P.Procedencia(
        fuente="Portal Nacional de Transparencia · Defensoría del Pueblo",
        captura=c_captura(),
        estado_adquisicion="descargado" if (ev and getattr(ev, "sha256", "")) else "",
        evidencia=(getattr(ev, "sha256", "") or "") if ev else "",
        verificador=verificador,
        prueba_del_verificador=prueba,
        sujeto=f"{CODIGO_SUJETO} {MUNICIPIO}",
    )


def c_captura() -> str:
    """Cuándo se trajo la evidencia con la que se está midiendo."""
    if not _INDICE.exists():
        return ""
    import datetime as _d
    return _d.datetime.fromtimestamp(_INDICE.stat().st_mtime).isoformat(timespec="minutes")


def _con_peso(h: dict, proc, pretendido: str) -> dict:
    """Aplica la cadena al hallazgo y lo degrada si no la sostiene."""
    from app.agents import procedencia as P
    s = P.sostener(h.get("detalle") or h["tipo"], proc, pretendido)
    h["nivel"] = s.peso if s.peso != P.HECHO_VERIFICABLE else h["nivel"]
    h["procedencia"] = {k: v for k, v in vars(proc).items() if v}
    h["explicacion"] = P.explicar(s)
    if s.degradada_desde:
        h["degradado_desde"] = s.degradada_desde
        h["capas_sin_responder"] = s.faltan
    return h


# ── 4-7 · medición ──────────────────────────────────────────────────────────────
def _conjuntos() -> list[str]:
    import yaml
    cat = yaml.safe_load(_CATALOGO.read_text(encoding="utf-8"))
    return [cd["id"] for cd in cat["conjuntos_datos"]]


def _cadencia(cd_id: str) -> tuple[str | None, str]:
    """La cadencia la declara `RO-VII-001`, conjunto por conjunto.

    Antes se deducía leyendo el catálogo y aplicando aquí la regla de «la menos
    exigente». Eso era criterio normativo dentro del orquestador: ahora se
    consulta a la regla operativa, que además explica su fundamento."""
    return R.cadencia_aplicable(cd_id)


def _periodos_del_anio(cadencia: str | None, meses: list[int]) -> dict[str, list[int]]:
    """Agrupa los meses del tramo en los períodos que la norma exige.

    Un conjunto trimestral tiene cuatro oportunidades de cumplir, no doce:
    evaluarlo mes a mes le fabricaría ocho faltas que la norma no impone. El
    número de períodos sale de la cadencia que declara la RO; aquí sólo se hace
    la aritmética del calendario, que no es criterio."""
    if cadencia is None:
        # Sin cadencia declarada no se construyen períodos: se evalúa lo publicado
        # y la temporalidad queda `no_determinable`.
        return {f"{m:02d}": [m] for m in meses}
    por_anio = R.periodos_por_anio(cadencia)
    if not por_anio:
        return {f"{m:02d}": [m] for m in meses}
    ancho = 12 // por_anio
    fuera: dict[str, list[int]] = {}
    for m in meses:
        idx = (m - 1) // ancho + 1
        eti = f"{m:02d}" if ancho == 1 else f"{cadencia[:3].upper()}{idx}"
        fuera.setdefault(eti, []).append(m)
    return fuera


def _medir(c: Corrida, meses: list[int]) -> None:
    from app.agents.d07.scoring import ScoreCD
    scores_anio: list[ScoreCD] = []
    for cd_id in _conjuntos():
        cad, razon = _cadencia(cd_id)
        publicados: list[int] = []
        # Los períodos EXIGIDOS por la cadencia, no los publicados. Saltarse los
        # meses sin publicación dejaba SITA promediando sólo los aciertos: la
        # primera corrida dio 0,97 con dos conjuntos que no publicaron nada en todo
        # el año. El Instructivo lo dice al revés —«Sin información» califica 0—, y
        # omitir el cero premia justamente al que no publica.
        periodos = _periodos_del_anio(cad, meses)
        cuenta_cero = R.periodos_no_publicados_califican_cero()
        for etiqueta, ms in periodos.items():
            ev = None
            for mes in ms:
                cand = levantar_evidencia_local(cd_id, c.anio, mes)
                if cand.existe:
                    ev, publicados = cand, publicados + [mes]
                    break
            mes_ref = ms[-1]
            if ev is None and not cuenta_cero:
                # La RO decide si un período ausente entra al promedio. Si dijera
                # que no, se omite — pero lo dice la regla, no este bucle.
                continue
            if ev is None:
                # `existe=False` significa «no se halló publicación», nunca «el
                # hecho no existe» (ADR-042 §6). Califica 0 y así se declara.
                ev = levantar_evidencia_local(cd_id, c.anio, mes_ref)
            corte = _dt.date(c.anio, mes_ref, 1) + _dt.timedelta(days=32)
            mes = mes_ref
            # Los parámetros normativos los pone la RO, no el motor: si el órgano
            # rector mueve el plazo o admite otro formato, cambia la regla.
            s = evaluar_cd(cd_id, ev, fecha_monitoreo=corte,
                           formatos_abiertos=R.formatos_datos_abiertos(),
                           dia_limite=R.dia_limite_registro(),
                           # Qué parámetros cualitativos evalúa el Instructivo
                           # para ESTE conjunto. No son los mismos para todos.
                           parametros_cualitativos=R.parametros_cualitativos(cd_id))
            scores_anio.append(s)
            if not ev.existe:
                c.resultados.append({
                    "cd": cd_id, "periodo": f"{c.anio}-{etiqueta}", "sita": s.sita,
                    "cta": s.cta, "eta": s.eta, "rp": s.rp, "ci": s.ci,
                    "sha256": None, "url": None, "obs": s.observaciones,
                })
                continue
            c.resultados.append({
                "cd": cd_id, "periodo": f"{c.anio}-{mes:02d}", "sita": s.sita,
                "cta": s.cta, "eta": s.eta, "rp": s.rp, "ci": s.ci,
                "sha256": ev.sha256, "url": ev.url, "obs": s.observaciones,
            })
            # Cobertura material: hallazgo propio de QUIRA, NO entra en SITA.
            cob = verificar_cobertura(cd_id, c.anio, mes)
            for comp in cob.no_hallados:
                from app.agents import procedencia as P
                c.hallazgos.append(_con_peso({
                    "tipo": "cobertura_material",
                    "nivel": "hallazgo_verificable",
                    "cd": cd_id, "periodo": f"{c.anio}-{mes:02d}",
                    "componente": comp,
                    "detalle": cob.por_componente[comp],
                    "nota": "el canon exige esta dimensión y la evidencia no la "
                            "acredita. NO equivale a incumplimiento: la calificación "
                            "normativa la decide el motor jurídico.",
                }, _procedencia(cd_id, f"{c.anio}-{mes:02d}", ev,
                                verificador="componentes.verificar_cobertura",
                                prueba="test_cobertura_no_inventa_ausencias_por_busqueda_literal"),
                   P.HECHO_VERIFICABLE))

        # Temporalidad, sólo donde la norma fija cadencia.
        if cad is None:
            c.hallazgos.append({
                "tipo": "temporalidad", "nivel": "no_determinable",
                "cd": cd_id, "periodo": str(c.anio), "razon": razon,
                "meses_con_publicacion": publicados,
            })
            continue
        por_periodo = {"mensual": lambda m: m, "trimestral": lambda m: (m - 1) // 3 + 1,
                       "semestral": lambda m: (m - 1) // 6 + 1, "anual": lambda m: 1}[cad]
        exigidos = sorted({por_periodo(m) for m in meses})
        cubiertos = sorted({por_periodo(m) for m in publicados})
        faltan = [p for p in exigidos if p not in cubiertos]
        if faltan:
            from app.agents import procedencia as P
            # La temporalidad se juzga sobre el ÍNDICE de lo publicado, no sobre
            # un artefacto concreto: su evidencia es la captura misma.
            proc = _procedencia(cd_id, str(c.anio),
                                verificador="orquestador._periodos_del_anio",
                                prueba="test_cadencia_trimestral_no_exige_doce_periodos")
            proc = P.Procedencia(**{**vars(proc),
                                    "estado_adquisicion": "indice_completo",
                                    "evidencia": c.canon.get("vara_sha", "")[:16]})
            c.hallazgos.append(_con_peso({
                "tipo": "temporalidad",
                "nivel": ("sin_publicacion_alguna" if not cubiertos
                          else "hallazgo_verificable"),
                "cd": cd_id, "periodo": str(c.anio), "cadencia": cad,
                "razon_cadencia": razon,
                "periodos_exigidos": exigidos, "periodos_faltantes": faltan,
                "meses_con_publicacion": publicados,
            }, proc, P.HECHO_VERIFICABLE))

    c.sita = calcular_sita(scores_anio)
    c.scores = scores_anio


# ── 8 · persistencia ────────────────────────────────────────────────────────────
def ejecutar(anio: int, meses: list[int], guardar: bool = False) -> Corrida:
    _CORRIDAS.mkdir(parents=True, exist_ok=True)
    n = len(list(_CORRIDAS.glob(f"RUN-D07-{_dt.date.today()}-*.json"))) + 1
    c = Corrida(run_id=f"RUN-D07-{_dt.date.today()}-{n:04d}",
                municipio=MUNICIPIO, anio=anio)

    _gates_canon(c)
    if not c.bloqueada:
        _gates_evidencia(c)
    if c.bloqueada:
        # No se mide con la vara movida ni sobre evidencia sobrescrita. La corrida
        # queda registrada con su causa: un resultado ausente es informativo, uno
        # calculado sobre base dudosa es una mentira con formato de dato.
        c.estado = "BLOCKED"
        return c

    _medir(c, meses)
    c.estado = "COMPLETED"

    if guardar:
        salida = {
            "run_id": c.run_id, "estado": c.estado,
            "municipio": c.municipio, "anio": c.anio, "meses": meses,
            "canon": c.canon,
            "gates": [{"gate": g.nombre, "ok": g.ok, "detalle": g.detalle}
                      for g in c.gates],
            "adquisicion": c.adquisicion,
            "sita": getattr(c, "sita", {}),
            "resultados": c.resultados, "hallazgos": c.hallazgos,
            "ejecutado": _dt.datetime.now().isoformat(timespec="seconds"),
            "sin_ia": True,
        }
        p = _CORRIDAS / f"{c.run_id}.json"
        p.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        c.ruta = p
    return c


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", type=int, default=2025)
    ap.add_argument("--meses", default="1-12", help="p.ej. 1-12 o 1-5")
    ap.add_argument("--guardar", action="store_true")
    args = ap.parse_args()

    a, _, b = args.meses.partition("-")
    meses = list(range(int(a), int(b or a) + 1))

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    c = ejecutar(args.anio, meses, guardar=args.guardar)
    print(f"{c.run_id}   municipio={c.municipio}   {c.anio} meses {meses[0]}-{meses[-1]}\n")
    for g in c.gates:
        print(f"   [{'ok' if g.ok else 'XX'}] {g.nombre:12} {g.detalle}")
    if c.adquisicion:
        print("\n   EL AGENTE ADQUIRIÓ SU PROPIA EVIDENCIA (nadie corrió un script):")
        for ad in c.adquisicion:
            print(f"      {ad['etapa']:14} {ad['estado']:12} {ad['segundos']:7.1f}s  "
                  f"{ad.get('detalle','')[:48]}")
    if c.estado == "BLOCKED":
        print(f"\n   estado: BLOCKED · no se publica resultado")
        sys.exit(5)

    s = getattr(c, "sita", {})
    print(f"\n   evaluaciones: {len(c.resultados)}")
    print(f"   SITA institucional: {s.get('SITA')}   "
          f"CTA {s.get('CTA')} · ETA {s.get('ETA')} · RP {s.get('RP')} · CI {s.get('CI')}")

    from collections import Counter
    print(f"\n   hallazgos: {len(c.hallazgos)}")
    for k, v in Counter((h["tipo"], h["nivel"]) for h in c.hallazgos).most_common():
        print(f"      {k[0]:20} {k[1]:26} {v:3}")
    for h in [x for x in c.hallazgos if x["tipo"] == "cobertura_material"][:3]:
        print(f"      → {h['cd']} {h['periodo']}: falta «{h['componente']}»")
    print(f"\n   estado: {c.estado}")
    if getattr(c, "ruta", None):
        print(f"   → {c.ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
