# -*- coding: utf-8 -*-
"""
tests/test_d07_autonomia.py — las trampas de la corrida del 2026-08-17, fijadas
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE. La corrida sobre 936 archivos funcionó, pero **cada defecto lo
encontró una persona leyendo salidas**. Eso no es un dominio autónomo: es un
dominio con un vigilante. De ahí la regla que fijó el colega:

> **Cada corrección manual descubierta durante una corrida debe terminar
> convertida en una regla, gate o prueba automatizada antes de considerar
> autónomo el dominio.**

Cada test de este archivo es un error real que se cometió ese día, con su
consecuencia. No son casos hipotéticos: son el registro de lo que d07 ya sabe no
volver a hacer.

Dylus Lab © 2026
"""
from __future__ import annotations

import datetime as _dt
import os
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents.d07 import evidencia as ev                    # noqa: E402
from app.agents.d07.orquestador import _periodos_del_anio     # noqa: E402
from app.agents.d07.scoring import EvidenciaCD, evaluar_cd    # noqa: E402


# ── 1 · el tipo de archivo se decide por el descriptor, no por «datos abiertos» ──
def test_metadatos_no_se_confunden_con_conjunto_de_datos():
    """Muchos archivos se llaman `…-datos-abiertos-metadatos.csv`. Comprobar
    «datos abiertos» antes que «metadato» los clasificaba como conjunto de datos,
    y sus ~25 columnas descriptivas aparecían como si el numeral publicara 25
    campos donde la guía exige 9."""
    assert ev._tipo_archivo("2-directorio-datos-abiertos-metadatos.csv") == "metadatos"
    assert ev._tipo_archivo("6. Diccionario.csv") == "diccionario"
    assert ev._tipo_archivo("6. Conjunto de datos.csv") == "conjunto_de_datos"


# ── 2 · el numeral 5-22 es UN conjunto compartido ───────────────────────────────
def test_numeral_5_22_es_un_solo_conjunto():
    """La guía desarrolla el 5 (servicios) y el 22 (formularios) en un mismo
    bloque, con una lista de campos y una periodicidad. El portal de la DPE los
    publica igual: `Numeral 5-22`. Separarlos inventaba dos exigencias donde la
    norma pone una, y dejaba al 5 con cero campos."""
    assert ev._clave_numeral("Numeral 5-22") == "5"
    assert ev._clave_numeral("Numeral 1.3") == "1.3"
    assert ev._clave_numeral("Art. 24 Gobiernos Autónomos Descentralizados") == "Art.24"
    # Lo que no es del art. 19 no se cuela en su matriz.
    assert ev._clave_numeral("Otra cosa") is None


# ── 3 · las columnas vacías del final no son campos publicados ──────────────────
def test_columnas_vacias_al_final_no_cuentan_como_campos():
    """El directorio del numeral 2 trae sus 9 campos con nombre y 10 columnas
    mudas detrás, artefacto de exportar desde Excel. Contarlas producía «19
    columnas» frente a 9 exigidas: una discrepancia inventada por el lector."""
    filas = [["No.", "Nombre", "Puesto", "", "", ""],
             ["1", "Ana", "Analista", "", "", ""]]
    assert ev._columnas_utiles(filas) == 3


def test_columna_util_si_algun_dato_la_ocupa():
    """El recorte mira TODAS las filas, no sólo la cabecera: una columna sin
    título pero con datos sigue siendo información publicada."""
    filas = [["A", "B", ""], ["1", "2", "valor"]]
    assert ev._columnas_utiles(filas) == 3


# ── 4 · el delimitador se elige por estabilidad, no por frecuencia ──────────────
def test_delimitador_no_se_decide_contando_separadores(tmp_path):
    """Los campos de texto llevan comas dentro («Dirección de Ambiente, Espacios
    públicos»). Elegir `,` por mayoría partía una tabla de 3 columnas en 5. Gana
    el delimitador que produce un número de columnas ESTABLE entre filas."""
    p = tmp_path / "t.csv"
    p.write_text("Unidad;Objetivo;Meta\n"
                 "Dirección de Ambiente, Espacios públicos;Reducir, mitigar;80%\n"
                 "Planificación, Obras;Ampliar, mejorar;60%\n", encoding="utf-8")
    filas = ev._leer_tabla(p)
    assert all(len(f) == 3 for f in filas), f"se partió mal: {filas}"


def test_codificacion_dos_antes_que_latin1(tmp_path):
    """`latin-1` nunca falla —acepta cualquier byte— así que probarla antes de
    `cp850` fijaba la lectura corrupta («Direcci¢n») como si fuera el texto real."""
    p = tmp_path / "dos.csv"
    p.write_bytes("Código;Descripción\n510105;Salario\n".encode("cp850"))
    filas = ev._leer_tabla(p)
    assert filas[0][0] == "Código", f"decodificó mal: {filas[0]}"


# ── 5 · fechas en los tres formatos que mezcla la fuente ────────────────────────
@pytest.mark.parametrize("txt,esperado", [
    ("31/1/2025", _dt.date(2025, 1, 31)),
    ("2025-01-31", _dt.date(2025, 1, 31)),
    ("31-01-2025", _dt.date(2025, 1, 31)),
    ("", None),
    ("sin fecha", None),
])
def test_fecha_admite_los_formatos_de_la_fuente(txt, esperado):
    assert ev._fecha(txt) == esperado


# ── 6 · un período exigido y no publicado CALIFICA CERO ─────────────────────────
def test_periodo_no_publicado_puntua_cero_y_no_se_omite():
    """La primera corrida saltaba los meses sin publicación y SITA salía 0,97 con
    dos conjuntos que no publicaron nada en todo el año. Omitir el cero premia al
    que no publica; el Instructivo califica «Sin información» con 0."""
    vacia = EvidenciaCD(existe=False, formato_archivo=None, campos_completos=False,
                        fecha_dato=None, fecha_registro=None)
    s = evaluar_cd("CD-07", vacia)
    assert s.sita == 0.0
    assert s.cta == 0.0 and s.eta == 0 and s.rp == 0 and s.ci == 0


# ── 7 · la cadencia normativa define cuántas oportunidades de cumplir hay ───────
def test_cadencia_trimestral_no_exige_doce_periodos():
    """Evaluar un conjunto trimestral mes a mes le fabrica ocho faltas que la
    norma no impone. Fue el error que produjo el «3/12» aplicado a todos."""
    assert len(_periodos_del_anio("trimestral", list(range(1, 13)))) == 4
    assert len(_periodos_del_anio("mensual", list(range(1, 13)))) == 12
    assert len(_periodos_del_anio("semestral", list(range(1, 13)))) == 2
    assert len(_periodos_del_anio("anual", list(range(1, 13)))) == 1


def test_tramo_parcial_no_exige_periodos_no_vencidos():
    """2026 se evalúa hasta mayo: un conjunto trimestral tiene DOS períodos
    vencidos, no cuatro. Contar el año completo bajaría el cumplimiento por
    meses que aún no debía publicar."""
    assert len(_periodos_del_anio("trimestral", [1, 2, 3, 4, 5])) == 2
    assert len(_periodos_del_anio("anual", [1, 2, 3, 4, 5])) == 1


# ── 8 · registro fuera de plazo se detecta (Instructivo, día 15) ────────────────
def test_registro_posterior_al_dia_15_pierde_rp():
    base = dict(existe=True, formato_archivo="csv", campos_completos=True,
                fecha_dato=_dt.date(2025, 1, 31))
    a_tiempo = evaluar_cd("CD-12", EvidenciaCD(**base, fecha_registro=_dt.date(2025, 2, 14)),
                          fecha_monitoreo=_dt.date(2025, 2, 20))
    tarde = evaluar_cd("CD-12", EvidenciaCD(**base, fecha_registro=_dt.date(2025, 2, 17)),
                       fecha_monitoreo=_dt.date(2025, 2, 20))
    assert a_tiempo.rp == 1 and tarde.rp == 0


# ── 9 · la cobertura material no declara ausencia sin regla objetiva ────────────
def test_cobertura_no_inventa_ausencias_por_busqueda_literal():
    """La búsqueda de términos marcó como ausentes los cinco componentes del
    numeral 8 —y estaban todos: «Objetivos» se publica como `OBJETO DEL PROCESO`,
    «Proveedores» como `IDENTIFICACIÓN DEL CONTRATISTA`—. Hallar el término prueba
    presencia; no hallarlo NO prueba ausencia."""
    from app.agents.d07.componentes import verificar_cobertura
    cob = verificar_cobertura("CD-08", 2025, 10)
    assert cob.no_hallados == [], (
        f"la búsqueda literal volvió a declarar ausencias: {cob.no_hallados}")


def test_cobertura_si_declara_ausencia_cuando_la_norma_da_regla():
    """El numeral 6 remite expresamente a «los clasificadores presupuestales», y
    ahí sí hay regla objetiva: el primer dígito del código. Los ocho períodos
    publicados traen cero filas de los grupos 1 y 2 — ingresos."""
    from app.agents.d07.componentes import verificar_cobertura
    cob = verificar_cobertura("CD-06", 2025, 10)
    if not cob.por_componente:
        pytest.skip("sin evidencia descargada para el período")
    assert "Ingresos" in cob.no_hallados
    assert cob.por_componente["Gastos"]["estado"] == "cubierto"


# ── 10 · los sub-numerales de CD-01 no son dimensiones materiales ───────────────
def test_subnumerales_no_se_miden_como_cobertura_material():
    """CD-01 lista `1.1, 1.2, 1.3` en `componentes`, pero son conjuntos con
    periodicidad propia, no dimensiones internas de uno solo."""
    from app.agents.d07.componentes import verificar_cobertura
    assert verificar_cobertura("CD-01", 2025, 10).por_componente == {}


# ══ ADR-051 · el dominio consume la norma, no la interpreta ═══════════════════
# Estos son los invariantes que hacen VERIFICABLE la regla de autonomía. Sin
# ellos, «ningún criterio normativo vive en el código» sería una intención.

def test_el_dominio_consume_la_cadencia_de_la_regla_operativa():
    """La periodicidad la declara `RO-VII-001`, conjunto por conjunto.

    Antes la deducía un script leyendo el .docx de la Guía y el orquestador
    aplicaba por su cuenta la regla de «la menos exigente». Eso era criterio
    normativo dentro del código: invisible, sin cadena y sin fundamento citable."""
    from app.agents.d07 import reglas as R
    assert R.cadencia_aplicable("CD-06")[0] == "mensual"
    assert R.cadencia_aplicable("CD-21")[0] == "trimestral"
    assert R.cadencia_aplicable("CD-18")[0] == "semestral"
    # sin cadencia declarada → no se mide, y la razón se explica
    cad, razon = R.cadencia_aplicable("CD-03")
    assert cad is None and "no declara" in razon


def test_la_norma_admite_dos_cadencias_y_la_regla_decide_cual():
    """«semestral o anual, según varíen los contenidos». El dominio no elige:
    aplica lo que la RO manda, y la razón queda registrada en el resultado."""
    from app.agents.d07 import reglas as R
    cad, razon = R.cadencia_aplicable("CD-16")
    assert cad == "anual" and "regla operativa manda" in razon


def test_parametros_normativos_vienen_de_la_ro_no_del_codigo():
    """Plazo, formatos y fórmulas de ausencia estaban escritos a mano en
    `scoring.py` y en constantes de módulo. Ahora se consultan."""
    from app.agents.d07 import reglas as R
    assert R.dia_limite_registro() == 15
    assert "csv" in R.formatos_datos_abiertos()
    assert R.formulas_ausencia() == ["NO APLICA", "INFORMACIÓN NO DISPONIBLE"]
    assert R.periodos_no_publicados_califican_cero() is True


def test_el_clasificador_no_vive_en_el_modulo():
    """Los grupos del clasificador presupuestario eran una constante de
    `componentes.py`. Se comprueba que el módulo ya no los declara y que la RO
    sí — si alguien los reintroduce en el código, este test lo detecta."""
    import app.agents.d07.componentes as C
    from app.agents.d07 import reglas as R
    assert not hasattr(C, "_GRUPOS_CLASIFICADOR"), (
        "el clasificador volvió al módulo: es criterio normativo, va en la RO")
    grupos = R.grupos_clasificador()
    assert grupos["Ingresos"] == ("1", "2") and grupos["Gastos"] == ("5", "6", "7", "8")


def test_el_caso_cero_sobre_cero_lo_decide_la_norma():
    """Qué ocurre si NINGUNA dimensión es determinable no puede resolverlo el
    módulo en tiempo de ejecución: eso devolvería el criterio al código."""
    from app.agents.d07 import reglas as R
    caso = R.caso_sin_dimensiones_determinables()
    assert caso["estado"] == "no_determinable"
    assert caso["score"] is None and caso["excluye_del_promedio"] is True


def test_escalar_a_incumplimiento_exige_las_seis_condiciones():
    """Ningún agente puede saltar del hecho verificable a la calificación
    jurídica. Las condiciones las declara la RO, no el que programa."""
    from app.agents.d07 import reglas as R
    assert len(R.condiciones_de_escalamiento()) == 6


def test_la_corrida_declara_si_sus_reglas_estan_vigentes():
    """Un resultado calculado con reglas en `propuesta` no es lo mismo que uno
    calculado con reglas vigentes, y esa diferencia debe quedar visible en la
    corrida — no perdida en un comentario."""
    from app.agents.d07 import reglas as R
    estados = R.estado_reglas()
    assert set(estados) == {f"RO-VII-00{n}" for n in range(1, 6)}
    assert all(v in ("propuesta", "vigente", "obsoleta", "retirada")
               for v in estados.values())


# ── transparencia pasiva y difusión · las dos últimas cadenas del dominio ───────
def test_el_plazo_de_respuesta_sale_de_la_ley_no_del_codigo():
    """Art. 34: diez días, prorrogable cinco. La prórroga exige causa justificada
    E informada: una no comunicada no extiende el término."""
    from app.agents.d07 import reglas as R
    p = R.plazo_respuesta_solicitud()
    assert p["dias"] == 10 and p["prorroga_dias"] == 5
    assert len(p["prorroga_condiciones"]) == 2


def test_el_silencio_equivale_a_denegacion():
    """Art. 36: no contestar no es una respuesta neutra. Habilita la gestión
    oficiosa y la acción constitucional — QUIRA registra el hecho, no las ejerce."""
    from app.agents.d07 import reglas as R
    s = R.silencio_administrativo()
    assert s["equivale_a"] == "denegacion" and len(s["habilita"]) == 2


def test_sin_solicitudes_no_hay_incumplimiento():
    """La obligación sólo se activa cuando alguien la ejerce. Contar cero
    solicitudes como falta convertiría el silencio ciudadano en culpa del GAD."""
    from app.agents.d07 import reglas as R
    c = R.caso_sin_solicitudes()
    assert c["estado"] == "no_observable" and c["excluye_del_promedio"] is True


def test_la_difusion_exige_tres_veces_al_ano():
    """Reglamento art. 10 — la obligación más simple de verificar del dominio, y
    la que ningún monitoreo estaba comprobando."""
    from app.agents.d07 import reglas as R
    assert R.frecuencia_minima_difusion()["veces_por_anio"] == 3
    assert {d["id"] for d in R.destinatarios_difusion()} == {
        "servidores", "poblacion_servida"}


def test_lo_que_no_se_puede_observar_no_se_califica_como_incumplido():
    """El invariante que evita repetir OBS-030 por adelantado: sin fuente
    verificada el estado es `no_observable`, jamás «no cumple». Un GAD que sí
    capacita no puede aparecer incumpliendo porque el observador mira mal."""
    from app.agents.d07 import reglas as R
    o = R.observabilidad_difusion()
    assert o["estado_por_defecto"] == "no_observable"
    assert o["score"] is None and o["excluye_del_promedio"] is True
    assert len(o["vias_para_habilitar"]) >= 2


def test_las_clases_de_acto_no_viven_en_el_modulo():
    """Que un acta no sea una resolución lo decide la ley, no el lector. La lista
    era una constante de `documentos.py` y estuvo declarada como deuda en ADR-051
    hasta que `CNO-VII-002` le dio cadena. Si vuelve al código, esto falla."""
    import app.agents.d07.documentos as D
    from app.agents.d07 import reglas as R
    assert not hasattr(D, "_CLASES"), (
        "las clases de acto volvieron al módulo: son criterio normativo, van en la RO")
    ids = {c["id"] for c in R.clases_de_acto()}
    assert {"acta_de_sesion", "resoluciones_de_sesion"} <= ids


def test_el_certificado_de_resoluciones_no_sustituye_al_acta():
    """El hallazgo central del art. 24, convertido en regla ejecutable: la guía
    exige «Enlace para ver y descargar el acta», y lo publicado es un certificado
    de resoluciones. La RO declara que uno NO sustituye al otro, de modo que el
    agente no tiene que argumentarlo caso por caso."""
    from app.agents.d07 import documentos as D
    assert D.clases_admitidas("actas") == ["acta_de_sesion"]
    assert "resoluciones_de_sesion" in D.no_sustituible_por("actas")


def test_el_clasificador_documental_distingue_acta_de_certificado():
    """Sobre el texto real leído de los PDF del municipio piloto."""
    from app.agents.d07.documentos import clasificar, correlativo, tipo_sesion
    certificado = ("RESOLUCIONES DE LA SESIÓN ORDINARIA Nro. 112-06-03-2025 "
                   "EL PLENO DEL CONCEJO MUNICIPAL RESUELVE:")
    assert clasificar(certificado) == "resoluciones_de_sesion"
    assert correlativo(certificado) == 112
    assert tipo_sesion(certificado) == "ordinaria"
    assert clasificar("ACTA DE LA SESIÓN ORDINARIA Nro. 099") == "acta_de_sesion"


def test_tipo_de_sesion_solo_admite_los_valores_de_la_norma():
    """El campo de la guía dice «ordinaria o extraordinaria». El GAD publica
    «Resolución Legislativa», que no es un tipo de sesión: el dato queda sin
    declarar aunque la celda no esté vacía."""
    from app.agents.d07 import reglas as R
    from app.agents.d07.documentos import tipo_sesion
    assert R.tipos_de_sesion_admitidos() == ["ordinaria", "extraordinaria"]
    assert tipo_sesion("RESOLUCIÓN LEGISLATIVA Nro. 350") is None


def test_un_escaneo_no_se_transcribe_ni_se_supone():
    """Sin OCR, un documento escaneado no se juzga. Lo declara la RO para que el
    módulo no lo resuelva por su cuenta: no se afirma nada de lo que no se leyó."""
    from app.agents.d07 import reglas as R
    d = R.documento_no_procesable()
    assert d["estado"] == "no_determinable" and d["excluye_del_promedio"] is True


def test_sin_regla_operativa_el_dominio_no_improvisa():
    """Pedir un parámetro a una RO inexistente es un ERROR, no un valor por
    defecto. Un default silencioso es exactamente el criterio escondido que
    ADR-051 vino a prohibir."""
    from app.agents.d07 import reglas as R
    with pytest.raises(R.ReglaNoDisponible):
        R.cargar("RO-VII-999")


# ══════════════════════════════════════════════════════════════════════════════
# LA CADENA DE ADQUISICIÓN · «Claude no es QUIRA» (Javo, 2026-08-19)
# ══════════════════════════════════════════════════════════════════════════════
# Hasta esta fecha, la recolección de evidencia eran 31 programas sueltos que
# **una persona** ejecutaba desde una terminal: uno solo era invocable desde la
# aplicación. El sistema no podía saber si su evidencia estaba al día, y menos
# actualizarla. Estas pruebas fijan lo contrario, que es lo que hace falta para
# 222 municipios sin nadie mirando.

def _etapa_ficticia(tmp_path, monkeypatch, consume=(), produce=("out.json",)):
    """Etapa de laboratorio: la lógica de vigencia se prueba sin tocar la
    evidencia real ni la red."""
    from app.agents.d07 import etapas as E
    monkeypatch.setattr(E, "RAIZ", tmp_path)
    monkeypatch.setattr(E, "_SELLO_CADENA", tmp_path / "sello.json")
    return E, {"id": "prueba", "script": "x.py", "args": [],
               "consume": list(consume), "produce": list(produce),
               "descripcion": "etapa de prueba"}


def test_lo_que_nunca_se_produjo_no_se_da_por_hecho(tmp_path, monkeypatch):
    """Sin artefacto no hay medición posible: la etapa está pendiente y lo dice."""
    E, etapa = _etapa_ficticia(tmp_path, monkeypatch)
    ok, razon = E.al_dia(etapa)
    assert ok is False and "nunca se produjo" in razon


def test_una_descarga_nueva_invalida_el_analisis_viejo(tmp_path, monkeypatch):
    """EL ERROR QUE ESTO IMPIDE: todos los archivos existen, nada falla, y el
    sistema mide una descarga de hoy con un análisis de hace tres meses. Con un
    solo municipio se nota; con 222 nadie lo notaría jamás."""
    E, etapa = _etapa_ficticia(tmp_path, monkeypatch, consume=["in.json"])
    (tmp_path / "in.json").write_text("v1", encoding="utf-8")
    (tmp_path / "out.json").write_text("resultado", encoding="utf-8")
    E._sellar(etapa)
    assert E.al_dia(etapa)[0] is True

    (tmp_path / "in.json").write_text("v2 — el portal publicó algo distinto",
                                      encoding="utf-8")
    ok, razon = E.al_dia(etapa)
    assert ok is False and "cambió de contenido" in razon


def test_rehacer_una_etapa_no_invalida_a_las_que_dependen_de_ella(tmp_path, monkeypatch):
    """La cadena se invalida por CONTENIDO, no por fecha. Si el insumo se vuelve
    a escribir igual, lo que venía después sigue siendo válido: comparar por
    fecha de modificación obligaría a reverificar 1.254 enlaces sin motivo."""
    E, etapa = _etapa_ficticia(tmp_path, monkeypatch, consume=["in.json"])
    (tmp_path / "in.json").write_text("v1", encoding="utf-8")
    (tmp_path / "out.json").write_text("resultado", encoding="utf-8")
    E._sellar(etapa)

    import time as _t
    _t.sleep(0.01)
    (tmp_path / "in.json").write_text("v1", encoding="utf-8")   # mismo contenido
    assert E.al_dia(etapa)[0] is True, "rehacer sin cambios no debe propagar trabajo"


def test_lo_que_mira_a_la_fuente_caduca_por_calendario(tmp_path, monkeypatch):
    """Un análisis derivado no caduca solo; una consulta al portal sí. El portal
    de hace un trimestre describe un estado que ya no existe."""
    import os
    import time as _t
    E, etapa = _etapa_ficticia(tmp_path, monkeypatch)
    monkeypatch.setitem(E.VIGENCIA_DIAS, "prueba", 30)
    p = tmp_path / "out.json"
    p.write_text("captura", encoding="utf-8")
    viejo = _t.time() - 45 * 86400
    os.utime(p, (viejo, viejo))
    ok, razon = E.al_dia(etapa)
    assert ok is False and "45 días" in razon


def test_el_orquestador_declara_lo_que_adquirio_por_su_cuenta():
    """Un resultado calculado sobre evidencia recién recolectada y otro sobre lo
    que ya había en disco no son el mismo hecho. La corrida guarda cuál fue."""
    from app.agents.d07.orquestador import Corrida
    c = Corrida(run_id="X", municipio="montecristi", anio=2025)
    assert c.adquisicion == [], "la corrida debe poder registrar su adquisición"


def test_ninguna_etapa_declara_un_programa_inexistente():
    """Si el programa no está, la capacidad no existe — por más que la nómina de
    agentes la dé por buena. El registro no sustituye al sistema."""
    from app.agents.d07 import etapas as E
    faltan = [e["id"] for e in E.ETAPAS if not E.disponible(e)]
    assert not faltan, f"etapas sin programa: {faltan}"


def test_ningun_programa_queda_sin_clasificar():
    """LA TRAMPA QUE ESTO CIERRA: el 2026-08-19 hubo que leer los 31 programas de
    `scripts/normativa/` para saber cuáles eran capacidad del sistema y cuáles
    dependían de que alguien abriera una terminal. Ese inventario no puede vivir
    en la cabeza de nadie ni envejecer en silencio: un programa nuevo sin
    clasificar hace fallar esta prueba, y quien lo agregue debe declarar si es
    capacidad operativa o herramienta de construcción del canon."""
    from app.agents.d07 import etapas as E
    presentes = {p.name for p in (E._SCRIPTS).glob("*.py")} - {"__init__.py"}
    clasificados = set(E.clasificacion_scripts())
    sin_clasificar = presentes - clasificados
    assert not sin_clasificar, (
        f"programas sin declarar qué son: {sorted(sin_clasificar)} — "
        f"decláralos en ETAPAS o en NO_SON_ETAPAS")


def test_la_vara_normativa_no_se_regenera_sola():
    """Un sistema que reejecuta la extracción de su propia vara puede cambiarse
    el patrón con el que mide y presentar el resultado como si nada. Por eso la
    construcción del canon NUNCA es una etapa automática (ADR-051 §2b)."""
    from app.agents.d07 import etapas as E
    canon = set(E.NO_SON_ETAPAS["construccion_del_canon"]["scripts"])
    etapas = {e["script"] for e in E.ETAPAS}
    assert not (canon & etapas), "la vara no puede estar en la cadena automática"
    assert "extraer_exigencias_lotaip.py" in canon


def test_un_analisis_que_se_corto_solo_no_se_declara_completo():
    """EL ERROR, ENCONTRADO EL 2026-08-19 POR LA PROPIA INSTRUMENTACIÓN. La
    revisión documental del Numeral 10 escribió `completo: true` con **7 de 15
    documentos jamás intentados**: la fuente dejó de responder, el guardarraíl
    cortó, y el archivo resultante era indistinguible de un análisis entero.

    «Completo» tiene dos enemigos —el tope que pide quien invoca y el corte
    automático por fuente caída— y sólo se miraba el primero. Es la misma
    familia de los tres errores anteriores del dominio: «390 artefactos» era una
    resta, «24 escaneos» eran referencias, «94 documentos» era un tope de
    tamaño."""
    import json
    from pathlib import Path
    RUTA = RAIZ / "data" / "lotaip" / "documentos_n10.json"
    if not RUTA.exists():
        pytest.skip("no hay análisis del Numeral 10 en este entorno")
    meta = json.loads(RUTA.read_text(encoding="utf-8"))["_meta"]
    if meta.get("no_intentados"):
        assert meta["completo"] is False, (
            "un análisis con documentos no intentados NO puede declararse completo")


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBA E · reproducibilidad (colega, 2026-08-19)
# ══════════════════════════════════════════════════════════════════════════════
# > *«Eliminar los derivados —no la fuente— y decir: QUIRA reconstruye esto
# > sola. Ahí sí tendremos la primera demostración fuerte de ADR-051.»*
#
# Es la única prueba que separa «el programa existe» de «QUIRA se apropió de la
# capacidad». Todo lo demás —que corra, que devuelva 0, que escriba un archivo—
# lo cumple igual un script que alguien ejecuta a mano.

@pytest.mark.efecto_real(
    "borra un derivado y deja que la cadena lo reconstruya: el trabajo real NO "
    "es un medio para probar otra cosa, es exactamente lo que esta prueba "
    "demuestra. Eliminarlo la vaciaría de contenido.")
def test_quira_reconstruye_sus_derivados_sin_ayuda():
    """Se borra un derivado real y se comprueba que el agente lo rehace **igual**.

    Por qué se compara el SHA y no sólo que el archivo reaparezca: un
    reconstruido distinto significaría que el resultado depende de algo que no
    está en la evidencia —el momento, el orden, un estado en memoria— y
    entonces no es reproducible aunque exista.

    Se elige `contenido` porque no toca la red: la reproducibilidad debe poder
    demostrarse sin depender de que el portal del GAD esté vivo hoy.
    """
    from app.agents.d07 import etapas as E

    etapa = next(e for e in E.ETAPAS if e["id"] == "contenido")
    destino = RAIZ / etapa["produce"][0]
    if not destino.exists():
        pytest.skip("no hay evidencia local en este entorno")

    original = destino.read_bytes()          # respaldo en memoria, no en disco
    try:
        destino.unlink()
        assert not destino.exists()
        assert "contenido" in E.pendientes(), "el agente debe DARSE CUENTA de que falta"

        r = E.ejecutar_etapa(etapa)          # sin `forzar`: debe decidirlo solo
        assert r.estado == "ejecutada", f"no lo reconstruyó: {r.estado} · {r.detalle}"
        assert destino.exists(), "la etapa dijo haber corrido y no dejó su salida"

        rehecho = destino.read_bytes()
        assert rehecho == original, (
            "el reconstruido difiere del original: el resultado depende de algo "
            "que no está en la evidencia y por tanto no es reproducible")
    finally:
        if not destino.exists() or destino.read_bytes() != original:
            destino.write_bytes(original)    # el entorno queda como estaba


def test_el_grado_de_apropiacion_se_deriva_y_no_se_declara():
    """ADR-051 §2d. Una capacidad no puede llamarse «validada» porque alguien lo
    escriba: el grado se calcula sobre lo que el sistema puede demostrar —el
    programa existe, hay registro de una corrida del agente, y una prueba
    nombrada la reproduce—. Es la Regla de Oro 3 aplicada al propio sistema."""
    from app.agents.d07 import etapas as E

    etapa = next(e for e in E.ETAPAS if e["id"] == "contenido")
    grado, fundamento = E.grado_de_apropiacion(etapa)
    assert grado in (E.CAPACIDAD, E.EJECUCION, E.VALIDADO)
    assert fundamento, "un grado sin fundamento es una afirmación, no una medición"

    # Y la prueba declarada como acreditación debe EXISTIR: una referencia a una
    # prueba inexistente acreditaría reproducibilidad sin nada que la sostenga.
    for eid, nombre in E.PRUEBA_QUE_VALIDA.items():
        assert E._existe_prueba(nombre), (
            f"«{eid}» dice estar validada por «{nombre}», que no existe")


# ══════════════════════════════════════════════════════════════════════════════
# PRUEBAS B · C · D (colega, 2026-08-19) — sobre la evidencia ya producida
# ══════════════════════════════════════════════════════════════════════════════

def _cargar(rel: str):
    import json
    p = RAIZ / rel
    if not p.exists():
        pytest.skip(f"no existe {rel} en este entorno")
    return json.loads(p.read_text(encoding="utf-8"))


def test_b_cada_artefacto_interno_conserva_a_su_contenedor():
    """PRUEBA B · abrir un ZIP no puede desprender al hijo de su padre.

    Sin la cadena `contenedor → artefacto`, un documento hallado dentro de un
    comprimido se vuelve un archivo suelto sin procedencia: imposible decir de
    qué publicación salió, y por tanto imposible confrontarlo con la norma que
    obligaba a publicarlo."""
    d = _cargar("data/lotaip/contenido_contenedores.json")
    ok = [r for r in d["internos"] if r.get("estado") == "inspeccionado"]
    assert ok, "no hay artefactos internos inspeccionados"
    huerfanos = [r for r in ok if not r.get("contenedor_url")
                 or not r.get("sha256")]
    assert not huerfanos, (
        f"{len(huerfanos)} artefactos internos sin padre o sin identidad física")


def test_c_las_publicaciones_no_se_pierden_al_deduplicar():
    """PRUEBA C · conservación. Deduplicar por SHA y quedarse sólo con el objeto
    físico borraría la historia de publicación; contar publicaciones y llamarlas
    documentos infla el universo. Las dos cifras deben coexistir y cuadrar.

    Es el error que ya se cometió: «15 escaneos del numeral 15» era **un solo
    archivo, mismo SHA, publicado quince meses seguidos**."""
    from collections import Counter
    d = _cargar("data/lotaip/contenido_contenedores.json")
    ok = [r for r in d["internos"] if r.get("estado") == "inspeccionado"]
    apariciones = len(ok)
    unicos = len({r["sha256"] for r in ok if r.get("sha256")})
    assert unicos <= apariciones, "no puede haber más objetos físicos que apariciones"
    assert d["_meta"]["apariciones"] >= apariciones
    assert d["_meta"]["artefactos_unicos"] == unicos, (
        "el resumen y el detalle discrepan: uno de los dos miente")
    # Y la relación debe seguir siendo recuperable en ambos sentidos.
    veces = Counter(r["sha256"] for r in ok if r.get("sha256"))
    assert sum(veces.values()) == sum(1 for r in ok if r.get("sha256"))


def test_d_una_captura_que_fallo_no_es_una_ausencia():
    """PRUEBA D · la distinción que sostiene todo el dominio (ADR-042 §6):

        «no existe»  ≠  «no pude obtener»  ≠  «no lo intenté»

    Si un 404, un tiempo agotado o un corte de fuente se registraran como
    ausencia, QUIRA imputaría al GAD un incumplimiento que en realidad es una
    limitación del observador. La revisión del Numeral 10 es el caso real: 8
    enlaces devolvieron 404 y 7 no se intentaron — ninguno de los 15 puede
    contarse como «no publicado»."""
    d = _cargar("data/lotaip/documentos_n10.json")
    docs = d["documentos"]
    estados = {x.get("estado") for x in docs}
    # Ningún estado puede afirmar ausencia del documento en la fuente.
    prohibidos = {"no_publicado", "ausente", "inexistente", "sin_publicacion"}
    assert not (estados & prohibidos), (
        f"un fallo de captura se registró como ausencia: {estados & prohibidos}")
    # Y el resultado debe declararse parcial mientras haya algo sin intentar.
    if d["_meta"].get("no_intentados"):
        assert d["_meta"]["completo"] is False


@pytest.mark.skipif(
    os.environ.get("QUIRA_PRUEBA_DE_ORIGEN") != "1",
    reason="PRUEBA A · toca la fuente pública y rehace la captura completa. "
           "Se activa con QUIRA_PRUEBA_DE_ORIGEN=1 · no corre en la suite "
           "ordinaria porque golpear el portal del GAD en cada `pytest` sería "
           "usar al sujeto observado como banco de pruebas.")
def test_a_quira_adquiere_desde_la_fuente_sin_intervencion():
    """PRUEBA A · la demostración fuerte de ADR-051, y la única que falta.

        fuente pública → captura → descarga → SHA

    Que las etapas derivadas se reconstruyan (prueba E) demuestra que QUIRA
    procesa sola. Esta demuestra que QUIRA **obtiene** sola, que es distinto: es
    la mitad de la cadena que todavía depende de que alguien haya traído los
    archivos alguna vez.

    Se deja escrita y desactivada a propósito. Una prueba que no se puede correr
    hoy pero está especificada vale más que una promesa en un documento: el día
    que se autorice el gasto de red, se activa con una variable de entorno y el
    resultado es verificable, no narrado."""
    from app.agents.d07 import etapas as E

    resultados = E.preparar_evidencia(forzar=True, hasta="descarga")
    por_id = {r.etapa: r for r in resultados}
    assert por_id["captura"].estado == "ejecutada"
    assert por_id["descarga"].estado == "ejecutada"

    indice = _cargar("data/lotaip/descargas_indice.json")["archivos"]
    descargados = [a for a in indice if a.get("estado") == "descargado"]
    assert descargados, "la descarga no dejó un solo archivo"
    sin_sha = [a for a in descargados if not a.get("sha256")]
    assert not sin_sha, (
        f"{len(sin_sha)} archivos sin identidad física: sin SHA no hay evidencia")
    rutas = [a["ruta"] for a in descargados if a.get("ruta")]
    assert len(set(rutas)) == len(rutas), "hay archivos sobrescribiéndose entre sí"


# ══════════════════════════════════════════════════════════════════════════════
# OBS-032 · el instrumento no puede contener al sujeto
# ══════════════════════════════════════════════════════════════════════════════

# Puntos de código donde todavía aparece la identidad del sujeto observado. Eran
# **11** el 2026-08-19; hoy quedan los que fija este número. NO se exige llegar a
# cero de golpe —las rutas `dpe_montecristi.json` obligan a mover el árbol de
# datos y revalidar SHA, y eso se hace con cuidado, no de paso—. Lo que sí se
# prohíbe es **empeorar**: cada punto nuevo hace fallar la suite y obliga a
# justificarlo.
ACOPLAMIENTO_TOLERADO = 5


def _puntos_de_acoplamiento() -> list[str]:
    import re
    patron = re.compile(r"montecristi|130801|\b937\b", re.I)
    objetivos = list((RAIZ / "app" / "agents" / "d07").glob("*.py")) + [
        RAIZ / "scripts" / "normativa" / n for n in (
            "capturar_lotaip_dpe.py", "descargar_lotaip.py",
            "analizar_contenido_lotaip.py", "verificar_enlaces_lotaip.py",
            "inventario_documental.py", "inventario_contenido.py",
            "analizar_documentos_lotaip.py")]
    fuera = []
    for f in objetivos:
        if not f.exists():
            continue
        for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace")
                               .splitlines(), 1):
            d = ln.strip()
            es_prosa = (d.startswith("#") or d.startswith(">") or
                        d.startswith("*") or "«" in d)
            if patron.search(ln) and not es_prosa:
                fuera.append(f"{f.name}:{i}  {d[:70]}")
    return fuera


def test_el_sujeto_observado_no_crece_dentro_del_instrumento():
    """OBS-032 · *«No debemos construir d07 para Montecristi. Debemos utilizar
    Montecristi para construir el patrón que permita ejecutar d07 sobre 222
    GAD.»* (colega, 2026-08-19)

    Si aplicar la cadena a otro GAD exige editar código, la capacidad no existe
    como capacidad: existe como caso resuelto. Este tope es un trinquete — puede
    bajar, nunca subir."""
    puntos = _puntos_de_acoplamiento()
    assert len(puntos) <= ACOPLAMIENTO_TOLERADO, (
        f"la identidad del sujeto volvió a entrar al instrumento "
        f"({len(puntos)} > {ACOPLAMIENTO_TOLERADO}):\n  " + "\n  ".join(puntos))


def test_la_identidad_del_sujeto_tiene_una_sola_puerta():
    """La entidad `937` estaba escrita dos veces y con tipos distintos —`{937:
    ...}` en un script, `["937"]` en otro—, que es como una identidad duplicada
    empieza a divergir sin que nadie lo note."""
    from app.agents import sujeto as S
    assert S.entidad_dpe() == 937
    assert S.dominio_web() in S.dominios()
    assert "cloud.montecristi.gob.ec" in S.dominios(), (
        "el Nextcloud del GAD es publicación propia: tratarlo como ajeno "
        "convertiría contenido del sujeto en ausencia")
    with pytest.raises(S.SujetoNoDeclarado):
        S.cargar("999999")     # inventar la identidad de un GAD es peor que fallar


# El instrumento tampoco puede vivir en un escritorio concreto. Medido el
# 2026-08-19: 54 puntos en 49 archivos apuntan al disco de una persona, incluido
# el conector canónico del Gold Master y los motores de d01 y d08.
#
# Parte de eso NO es defecto —`ProyecT/` vive fuera del repositorio a propósito,
# porque los documentos fuente no se suben—; el defecto es que esa frontera esté
# escrita a mano 54 veces en vez de declararse una sola. Trinquete, no cruzada:
# puede bajar, no subir.
RUTAS_PERSONALES_TOLERADAS = 54


def test_el_sistema_no_se_ata_mas_a_un_escritorio():
    """Un programa que sólo corre en una máquina no es una capacidad de la
    plataforma. Para 222 GAD —y para cualquier despliegue— esto es bloqueante."""
    agujas = ("C:" + chr(92) + "Users", "C:" + chr(92) + "Proyectos")
    hits = []
    for base in ("scripts", "app", "quira_pages", "utils"):
        for f in (RAIZ / base).rglob("*.py"):
            for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace")
                                   .splitlines(), 1):
                if any(a in ln for a in agujas) and not ln.strip().startswith("#"):
                    hits.append(f"{f.relative_to(RAIZ)}:{i}")
    assert len(hits) <= RUTAS_PERSONALES_TOLERADAS, (
        f"{len(hits)} rutas al disco de una persona (tope {RUTAS_PERSONALES_TOLERADAS}). "
        f"Nuevas: {hits[RUTAS_PERSONALES_TOLERADAS:]}")


# ══════════════════════════════════════════════════════════════════════════════
# LA CUARTA DIMENSIÓN · sin sujeto, el grado miente por omisión
# ══════════════════════════════════════════════════════════════════════════════

def test_una_capacidad_reproducible_declara_sobre_quien_lo_es():
    """ADR-051 §2d. *«QUIRA sabe hacer X»* y *«QUIRA sabe hacer X sobre
    Montecristi»* no son la misma afirmación, y sólo la segunda es verdadera
    hoy. El fallo que esto cierra es real: el sello registraba el sujeto, la
    escalera lo aceptaba, y `grados()` **lo perdía al reconstruir el objeto** —
    el informe decía «sujeto sin acreditar» teniendo la evidencia delante."""
    from app.agents import apropiacion as A
    from app.agents.d07 import etapas as E

    gs = E.grados()
    reproducibles = [g for g in gs if g.grado == A.VALIDADO]
    if not reproducibles:
        pytest.skip("ninguna capacidad reproducible en este entorno")
    for g in reproducibles:
        assert g.sujeto, f"«{g.capacidad}» se declara reproducible sin decir sobre quién"
        assert "sobre" in g.afirmacion()

    r = A.resumir(gs)
    assert r["sujetos_acreditados"], "no se puede acreditar sin sujeto"
    assert len(r["sujetos_acreditados"]) == 1, (
        "si aparecen más sujetos, revisar que el alcance publicado lo refleje")


def test_el_sistema_responde_por_si_mismo_que_sabe_y_que_no():
    """El cierre que pidió el colega: que la escalera deje de ser documentación
    y sea una propiedad del sistema. Ni una línea del informe puede ser una
    declaración: todo sale de sellos de ejecución y de pruebas que existen."""
    from app.agents import apropiacion as A
    from app.agents.d07 import etapas as E

    a = A.autoconocimiento(E.grados())
    for clave in ("que_se_hacer", "que_ejecute", "demuestro_que_reproduzco",
                  "sobre_que_sujetos", "que_todavia_no_se_hacer",
                  "atribuible_a_id_asistida"):
        assert clave in a

    # La escalera no se puede saltar: lo reproducible es subconjunto de lo
    # ejecutado, y lo ejecutado de lo que tiene código.
    assert set(a["demuestro_que_reproduzco"]) <= set(a["que_ejecute"])
    assert set(a["que_ejecute"]) <= set(a["que_se_hacer"])
    # Y lo no demostrado queda atribuido a I+D, nunca al sistema.
    assert set(a["atribuible_a_id_asistida"]) & set(a["demuestro_que_reproduzco"]) == set()


def test_la_frontera_de_datos_se_declara_una_sola_vez():
    """OBS-032 · Fase 3. `IS_CLOUD` preguntaba si existía el disco de una
    persona: en cualquier otro equipo QUIRA se declaraba «en la nube» y pasaba a
    datos de demostración **sin avisar**. Un sistema que se degrada en silencio
    al cambiar de máquina no es portable."""
    import os
    import config
    assert hasattr(config, "DATOS_DIR")
    assert str(config.BASE_EXCEL) == str(config.DATOS_DIR)
    # La frontera debe poder recibirse del entorno, no estar fijada en el código.
    fuente = (RAIZ / "config.py").read_text(encoding="utf-8")
    assert 'os.environ.get(\n    "QUIRA_DATOS"' in fuente or '"QUIRA_DATOS"' in fuente, (
        "la carpeta de datos debe declararse una vez y recibirse del entorno")


def test_una_ejecucion_sin_sujeto_se_degrada_en_vez_de_suponer():
    """ADR-042 §6-bis, corolario de grado epistemológico. Un sello que dice
    «esto se ejecutó» pero no dice sobre quién NO acredita ejecución: acredita
    que algo corrió. La afirmación baja al grado que la evidencia sostiene.

    Es la contrapartida exacta del Principio Rector, aplicada al propio sistema:
    así como la ausencia de evidencia no autoriza a inferir hechos sobre el
    sujeto observado, la ausencia de procedencia no autoriza a inferir solidez
    sobre la propia afirmación."""
    from app.agents import apropiacion as A
    g = A.derivar("x", hay_codigo=True, ejecutada_por_el_agente=True,
                  prueba="test_quira_reconstruye_sus_derivados_sin_ayuda",
                  sujeto="")
    assert g.grado == A.CAPACIDAD, "sin sujeto no puede acreditarse ejecución"
    assert "SIN sujeto" in g.fundamento


def test_no_se_puede_construir_una_afirmacion_ejecutada_sin_sujeto():
    """El invariante es ESTRUCTURAL, no una comprobación posterior: la
    afirmación inválida no llega a existir. Se hizo así porque la validación a
    posteriori ya falló una vez — `grados()` perdía el sujeto y nadie se
    enteraba hasta leer el informe."""
    from app.agents import apropiacion as A
    with pytest.raises(A.AfirmacionSinSujeto):
        A.Grado("x", A.VALIDADO, "porque sí", "d07", "")
    with pytest.raises(A.AfirmacionSinSujeto):
        A.Grado("x", A.EJECUCION, "porque sí", "d07", "")
    # Sin ejecución no hay sujeto que declarar, y eso sí es válido.
    assert A.Grado("x", A.CAPACIDAD, "sólo existe el código", "d07", "").sujeto == ""


def test_el_perimetro_propio_se_sella_y_es_estable():
    """ADR-051 §13. El autoconocimiento debe ser un artefacto citable, no un
    texto en pantalla: con SHA, fecha y fuentes. Y el SHA se calcula sobre el
    estado —no sobre la fecha— para poder distinguir «el sistema cambió» de «el
    reloj avanzó»."""
    from app.agents import apropiacion as A
    from app.agents.d07 import etapas as E

    gs = E.grados()
    d1 = A.sellar_autoconocimiento(gs)
    d2 = A.sellar_autoconocimiento(gs)
    assert d1["_meta"]["sha256_estado"] == d2["_meta"]["sha256_estado"], (
        "dos derivaciones del mismo estado deben dar el mismo sello")
    assert d1["_meta"]["fuentes"], "un artefacto sin fuentes no es citable"
    assert "DERIVADO POR QUIRA" in d1["_meta"]["advertencia_de_lectura"]
    assert A.leer_autoconocimiento()["_meta"]["sha256_estado"] == d1["_meta"]["sha256_estado"]


def test_un_artefacto_declara_su_naturaleza_epistemologica():
    """ADR-051 §10. Un JSON con 636 artefactos correctos es indistinguible de
    una observación oficial si no dice lo que es. La clase viaja DENTRO del
    artefacto para que no dependa de que quien lo abra recuerde el ADR."""
    import json
    from app.agents import apropiacion as A
    ruta = RAIZ / "data" / "lotaip" / "contenido_contenedores.json"
    if not ruta.exists():
        pytest.skip("sin inventario de contenedores en este entorno")
    meta = json.loads(ruta.read_text(encoding="utf-8"))["_meta"]
    assert meta.get("clase_epistemologica") == A.MATERIAL_DE_INGENIERIA, (
        "los 636 artefactos NO son todavía observación atribuible a QUIRA")
    with pytest.raises(ValueError):
        A.clasificar_artefacto("dato_bonito")


def test_la_portabilidad_tiene_trinquete_por_clase():
    """OBS-032 · el colega: *«54 rutas absolutas no equivale a 54 defectos»*.
    Una frontera legítima replicada y una ruta al disco de alguien son problemas
    distintos y se cuentan por separado; mezclarlas oculta el progreso real.

    SE IMPORTA, NO SE LANZA (2026-08-25 · deuda 4-ter). Antes esto abría un
    subproceso para correr un script que sólo recorre archivos y cuenta. El
    resultado era idéntico y el coste, un `spawn` que la prueba no necesitaba:
    una capacidad de actuar sobre el mundo abierta sin motivo. La regla que
    queda: **si el efecto se puede eliminar, se elimina; sólo se declara el que
    es inherente a lo que la prueba demuestra.**"""
    import importlib.util

    ruta = RAIZ / "scripts" / "ci" / "check_portabilidad.py"
    spec = importlib.util.spec_from_file_location("_check_portabilidad", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    from collections import Counter
    por_clase = Counter(h[2] for h in mod.recorrer())
    excedidas = {c: (por_clase.get(c, 0), tope)
                 for c, tope in mod.TOPE.items() if por_clase.get(c, 0) > tope}
    assert not excedidas, (
        f"el sistema se ató más a una máquina concreta: {excedidas} "
        f"(clase: actual / tope). El trinquete sólo admite bajar.")


# ══════════════════════════════════════════════════════════════════════════════
# LA CADENA DE PROCEDENCIA · ADR-042 §6-bis, ejecutable
# ══════════════════════════════════════════════════════════════════════════════
# > *«Cuando la cadena no puede sostener una afirmación, QUIRA degrada la
# > afirmación; nunca rellena el vacío.»* (colega, 2026-08-19)

def test_sin_verificador_no_se_afirma_sobre_el_sujeto():
    """Una afirmación con fuente, captura y sujeto —pero sin evidencia
    conservada ni verificador ni prueba— NO puede decir nada del GAD. Puede
    decir que no fue posible acreditarlo, que es otra cosa y también es un
    resultado de auditoría."""
    from app.agents import procedencia as P
    p = P.Procedencia(fuente="DPE", captura="2026-08-19",
                      estado_adquisicion="descargado", sujeto="130801")
    s = P.sostener("el GAD no publicó X", p, P.HECHO_VERIFICABLE)
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert s.habla_del_sujeto is False
    assert s.degradada_desde == P.HECHO_VERIFICABLE
    # Y debe decir QUÉ faltó para el peso pretendido, no para el alcanzado:
    # «se degradó» sin causa es media respuesta, y la mitad accionable es la otra.
    assert set(s.faltan) == {"evidencia", "verificador", "prueba_del_verificador"}


def test_una_prueba_inexistente_no_acredita_la_interpretacion():
    """La capa `prueba_del_verificador` se COMPRUEBA, no se cree. Citar una
    prueba que no existe acreditaría un criterio sin nada que lo respalde — el
    mismo defecto ya cerrado en la escalera de apropiación, que aquí habría
    vuelto a entrar por otra puerta."""
    from app.agents import procedencia as P
    base = dict(fuente="DPE", captura="x", estado_adquisicion="descargado",
                evidencia="sha256…", verificador="componentes", sujeto="130801")
    falsa = P.Procedencia(**base, prueba_del_verificador="test_que_no_existe")
    assert P.sostener("x", falsa).peso == P.HALLAZGO_DE_VERIFICABILIDAD
    real = P.Procedencia(**base,
                         prueba_del_verificador="test_cadencia_trimestral_no_exige_doce_periodos")
    assert P.sostener("x", real).peso == P.HECHO_VERIFICABLE


def test_los_hallazgos_de_la_corrida_llevan_su_cadena():
    """Ningún hallazgo puede salir de una corrida sin decir de dónde viene. Es
    lo que permite responder «¿en qué se basa QUIRA para decir esto?» sin
    reconstruirlo a mano meses después."""
    from app.agents.d07.orquestador import ejecutar
    c = ejecutar(2025, list(range(1, 13)))
    assert c.hallazgos, "la corrida no produjo hallazgos"
    for h in c.hallazgos:
        if h["nivel"] == "no_determinable":
            continue                      # ya declara que no sostiene nada
        assert h.get("procedencia"), f"hallazgo sin cadena: {h['tipo']}"
        assert h.get("explicacion"), "un hallazgo sin explicación no es auditable"
        assert h["procedencia"].get("sujeto"), "no se afirma sin decir sobre quién"


def test_un_corte_de_fuente_no_condena_al_enlace_para_siempre():
    """EL DEFECTO, ENCONTRADO AL ACREDITAR LA ETAPA (2026-08-19).

    La verificación de enlaces reanuda desde su salida anterior, y copiaba
    cualquier registro cuyo estado no fuera `no_verificable`. Eso incluía
    `no_intentado_por_corte_de_fuente` — que **no dice nada del enlace**: dice
    que nuestro instrumento se detuvo aquella vez.

    Consecuencia real: 135 enlaces cortados por un fallo transitorio de SERCOP
    el 17-ago quedaban condenados a no intentarse nunca más, porque cada corrida
    copiaba el «no intentado» de la anterior. Y con ellos se arrastraban 417
    «accesibles» sin reverificar: una corrida de **10 segundos** declaraba haber
    comprobado 576 enlaces habiendo intentado **8**.

    La regla que esto fija: **se reutiliza lo que dice algo del enlace; se
    reintenta lo que dice algo de nuestro instrumento.**"""
    fuente = (RAIZ / "scripts" / "normativa" /
              "verificar_enlaces_lotaip.py").read_text(encoding="utf-8")
    assert "NO_REUTILIZABLES" in fuente
    i = fuente.index("NO_REUTILIZABLES = (")
    bloque = fuente[i:i + 220]
    assert "no_intentado_por_corte_de_fuente" in bloque, (
        "un corte de fuente es una limitación nuestra, no un resultado: debe "
        "reintentarse en la corrida siguiente")


def test_forzar_una_etapa_fuerza_su_trabajo_no_solo_su_estado():
    """`forzar=True` saltaba el «al día» pero no llegaba al script, que reanudaba
    desde su propia salida. La etapa terminaba en `ejecutada` sin haber
    ejecutado: `declarado ≠ ejecutado`, cometido por nosotros."""
    from app.agents.d07 import etapas as E
    enlaces = next(e for e in E.ETAPAS if e["id"] == "enlaces")
    assert enlaces.get("bandera_rehacer") == "--rehacer"
    fuente = (RAIZ / "app" / "agents" / "d07" / "etapas.py").read_text(encoding="utf-8")
    assert "bandera_rehacer" in fuente and "args_efectivos" in fuente


def test_cada_enlace_declara_si_se_comprobo_en_esta_corrida():
    """ADR-051 §12-bis. El JSON de enlaces ya demostró poder mentir por
    omisión: 576 registros con **8 comprobaciones reales** parecían una
    verificación completa, y sólo el reloj lo delató.

    Ahora cada registro dice a qué población pertenece, para que el recuento de
    «verificados» no pueda construirse mezclando lo comprobado hoy con lo
    heredado y con lo que nunca se intentó."""
    import json
    ruta = RAIZ / "data" / "lotaip" / "enlaces.json"
    if not ruta.exists():
        pytest.skip("sin verificación de enlaces en este entorno")
    fuente = (RAIZ / "scripts" / "normativa" /
              "verificar_enlaces_lotaip.py").read_text(encoding="utf-8")
    for poblacion in ("comprobado_en_esta_corrida",
                      "reutilizado_de_corrida_previa",
                      "no_intentado_en_esta_corrida"):
        assert poblacion in fuente, f"falta declarar la población «{poblacion}»"
    # Y el transporte debe publicarse: es la prueba independiente del trabajo.
    meta = json.loads(ruta.read_text(encoding="utf-8"))["_meta"]
    assert "transporte" in meta and "intentos" in meta["transporte"]


def test_ningun_artefacto_declara_su_fecha_a_mano():
    """Un artefacto rehecho hoy que dice haberse generado hace dos días miente
    sobre su propia procedencia — y la fecha de generación ES procedencia: la
    capa «captura» de ADR-042 §6-bis. Se encontró en 9 scripts, incluido el
    inventario que se acababa de regenerar."""
    import re
    patron = re.compile(r'"generado":\s*"20\d\d-\d\d-\d\d"')
    culpables = []
    for base in ("scripts", "app"):
        for f in (RAIZ / base).rglob("*.py"):
            if patron.search(f.read_text(encoding="utf-8", errors="replace")):
                culpables.append(str(f.relative_to(RAIZ)))
    assert not culpables, f"fecha de generación escrita a mano en: {culpables}"


def test_un_enlace_roto_de_un_tercero_no_penaliza_al_sujeto():
    """ADR-042 §6 aplicado al scoring. Los conjuntos del GAD enlazan a SERCOP,
    CPCCS y otros portales del Estado. Si uno de ésos cae, la calidad de la
    información **del GAD** no puede bajar por ello: `fuente_no_disponible`
    habla de la fuente, no del sujeto.

    El cálculo de `enlaces_vivos` no miraba la procedencia. El 2026-08-20 salía
    bien por casualidad —los 11 enlaces caídos eran todos de Montecristi— pero
    el día que SERCOP devolviera `acceso_restringido`, Montecristi habría pagado
    por ello."""
    fuente = (RAIZ / "app" / "agents" / "d07" /
              "evidencia.py").read_text(encoding="utf-8")
    i = fuente.index("rotos = [e for e in comprobados")
    bloque = fuente[i:i + 320]
    assert "_dominios_propios" in bloque, (
        "el cálculo de enlaces rotos debe acotarse a los dominios del sujeto "
        "obligado; si no, una caída de SERCOP baja la nota del GAD")


def test_los_enlaces_caidos_hoy_son_todos_del_sujeto_obligado():
    """Verificación del dato que sostiene el SITA 2025 actual: los 11 enlaces
    que penalizan calidad pertenecen a Montecristi, no a terceros. Si esto
    cambia, el número debe volver a explicarse antes de publicarse."""
    import json
    ruta = RAIZ / "data" / "lotaip" / "enlaces.json"
    if not ruta.exists():
        pytest.skip("sin verificación de enlaces en este entorno")
    from app.agents import sujeto as S
    en = json.loads(ruta.read_text(encoding="utf-8"))["enlaces"]
    penalizan = [e for e in en
                 if e.get("estado") in ("enlace_roto", "acceso_restringido")]
    ajenos = [e for e in penalizan
              if not any(d in (e.get("url") or "") for d in S.dominios())]
    assert not ajenos, (
        f"{len(ajenos)} enlaces de terceros estarían penalizando al sujeto: "
        f"{[e.get('procedencia') for e in ajenos]}")


# ══════════════════════════════════════════════════════════════════════════════
# AUDITORÍA DEL SCORING CONTRA EL INSTRUCTIVO · 2026-08-20
# ══════════════════════════════════════════════════════════════════════════════
# Javo: *«Sincerar todo en base a la norma y las metodologías para no
# inventarnos nada. Este DOM debe quedar impoluto e inexpugnable como base para
# los demás.»*
#
# Se confrontó `scoring.py` contra el Instructivo DPE 2024, parámetro por
# parámetro. Tres de cuatro coincidían. El cuarto no.

def test_los_parametros_cualitativos_no_aplican_a_todos_los_conjuntos():
    """EL DEFECTO QUE LA AUDITORÍA ENCONTRÓ. `CI` exigía los tres parámetros
    cualitativos a TODOS los conjuntos. El Anexo 1 del Instructivo los asigna
    uno por uno:

        estado_de_verificables      20 de 24 — NO al 2, 3, 4 ni 6
        vigencia_de_la_informacion  sólo a los numerales 16 y 18
        validez_de_la_informacion   sólo a los numerales 3 y 6

    Exigir un parámetro que la norma no aplica degrada la calificación del
    sujeto observado por una regla que nadie escribió."""
    from app.agents.d07 import reglas as R
    # Los que la norma exime de todo criterio cualitativo.
    assert R.parametros_cualitativos("CD-02") == []
    assert R.parametros_cualitativos("CD-04") == []
    # Vigencia: sólo dos numerales en todo el artículo 19.
    assert "vigencia_de_la_informacion" in R.parametros_cualitativos("CD-16")
    assert "vigencia_de_la_informacion" in R.parametros_cualitativos("CD-18")
    assert "vigencia_de_la_informacion" not in R.parametros_cualitativos("CD-09")
    # Validez: sólo el 3 (remuneraciones) y el 6 (presupuesto).
    assert "validez_de_la_informacion" in R.parametros_cualitativos("CD-03")
    assert "validez_de_la_informacion" in R.parametros_cualitativos("CD-06")
    assert "validez_de_la_informacion" not in R.parametros_cualitativos("CD-01")


def test_un_conjunto_sin_parametros_cualitativos_no_pierde_calidad():
    """Si el Instructivo no le asigna ninguno, la calidad no se degrada por
    criterios cualitativos: no hay ninguno que aplicar. Suponerlos sería
    inventarlos, y era lo que ocurría."""
    from app.agents.d07 import reglas as R
    from app.agents.d07.scoring import EvidenciaCD, evaluar_cd
    ev = EvidenciaCD(existe=True, formato_archivo="csv", campos_completos=True,
                     fecha_dato=_dt.date(2025, 1, 31),
                     fecha_registro=_dt.date(2025, 2, 10),
                     enlaces_vivos=True, vigencia_ok=False, validez_ok=False)
    corte = _dt.date(2025, 2, 20)
    # CD-02: el Instructivo no le asigna parámetros cualitativos.
    s = evaluar_cd("CD-02", ev, fecha_monitoreo=corte,
                   parametros_cualitativos=R.parametros_cualitativos("CD-02"))
    assert s.ci == 1, "se le exigió un criterio que la norma no le aplica"
    # CD-03: sí le exige validez, y la evidencia no la tiene.
    s3 = evaluar_cd("CD-03", ev, fecha_monitoreo=corte,
                    parametros_cualitativos=R.parametros_cualitativos("CD-03"))
    assert s3.ci == 0, "la validez SÍ le aplica al numeral 3 y debe pesar"


def test_la_formula_del_sita_es_la_del_instructivo():
    """Verificada contra el texto literal (Instructivo §Subíndice de
    Transparencia Activa, párrafo 268):

        SITA [%] = (CTA+ETA+RP+CI)/4

    y «el SITA será el promedio de los valores promedio de cada parámetro» —es
    decir, se promedia cada parámetro sobre los conjuntos y luego los cuatro
    entre sí; no se promedian SITAs individuales."""
    from app.agents.d07.scoring import ScoreCD, calcular_sita
    s = calcular_sita([ScoreCD("A", 1.0, 1, 1, 1, []),
                       ScoreCD("B", 0.5, 0, 1, 0, []),
                       ScoreCD("C", 0.0, 0, 0, 0, [])])
    assert s["CTA"] == round((1.0 + 0.5 + 0.0) / 3, 4)
    assert s["ETA"] == round((1 + 0 + 0) / 3, 4)
    assert s["SITA"] == round((s["CTA"] + s["ETA"] + s["RP"] + s["CI"]) / 4, 4)


def test_cta_admite_el_medio_punto_del_instructivo():
    """Tabla 1 del Instructivo: información **incompleta O desactualizada** vale
    0,5 — no 0. Un motor binario habría castigado como ausencia lo que la norma
    puntúa a la mitad."""
    from app.agents.d07.scoring import EvidenciaCD, evaluar_cd
    base = dict(existe=True, formato_archivo="csv",
                fecha_registro=_dt.date(2025, 2, 10),
                enlaces_vivos=True, vigencia_ok=True, validez_ok=True)
    corte = _dt.date(2025, 2, 20)
    completa = evaluar_cd("CD-02", EvidenciaCD(**base, campos_completos=True,
                                               fecha_dato=_dt.date(2025, 1, 31)),
                          fecha_monitoreo=corte, parametros_cualitativos=[])
    incompleta = evaluar_cd("CD-02", EvidenciaCD(**base, campos_completos=False,
                                                 fecha_dato=_dt.date(2025, 1, 31)),
                            fecha_monitoreo=corte, parametros_cualitativos=[])
    ausente = evaluar_cd("CD-02", EvidenciaCD(
        existe=False, formato_archivo=None, campos_completos=False,
        fecha_dato=None, fecha_registro=None), fecha_monitoreo=corte)
    assert (completa.cta, incompleta.cta, ausente.cta) == (1.0, 0.5, 0.0)
