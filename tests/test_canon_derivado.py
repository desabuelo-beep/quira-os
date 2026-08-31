# -*- coding: utf-8 -*-
"""
tests/test_canon_derivado.py — el estado de lo construido, sin depender de memoria
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30). En una sola sesión el director propuso tres veces
reconstruir cosas que ya existían: la matriz jurídica de d09 (vigente, 10/10
SHA), los artículos que iba a buscar en Supabase (estaban en `docs/brn/`), y una
degradación a «advisory» contra un CNO que ya modela d09 como obligación de
hacer. Javo lo nombró antes de que se viera el tercero:

> *«hay que hacer algo para navegar toda la documentación y no perder contexto
> de todo lo que tenemos construido»*

La respuesta no fue otro documento —envejecen en silencio— sino **derivar el
estado y poder atacarlo**, que es lo que estas pruebas hacen.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import canon as C                        # noqa: E402


# ── CRITERIOS ─────────────────────────────────────────────────────────────────
def test_el_inventario_deriva_el_dominio_del_canon_y_no_del_numeral():
    """`CNO-IV` es de **d02**, no de d04. El romano no es el número del dominio,
    así que el mapeo se lee de `opera_en` en la RO. Suponerlo sería inferir el
    dueño de una cadena normativa — justo lo que el sistema no se permite."""
    fam = C._familia_a_dominio()
    assert fam.get("IV") == "d02", f"el mapeo romano→dominio se rompió: {fam}"
    assert fam.get("IX") == "d09"
    assert fam.get("I") == "d01"


def test_los_sha_coinciden_con_la_matriz_de_cobertura():
    """VALIDACIÓN CRUZADA contra fuente independiente: `BRN_MATRIZ_COBERTURA.md`
    se escribió a mano, mucho antes que este módulo. Si el inventario derivado y
    la matriz escrita divergen, uno de los dos miente y hay que saberlo."""
    matriz = (RAIZ / "docs" / "architecture" / "BRN_MATRIZ_COBERTURA.md")
    if not matriz.exists():
        import pytest
        pytest.skip("no está la matriz de cobertura")
    texto = matriz.read_text(encoding="utf-8", errors="replace")

    for dom, esperado in (("d09", "10/10"), ("d02", "6/6"), ("d03", "9/9")):
        e = C.estado_canonico(dom)
        derivado = f"{e['sha_sellados']}/{e['sha_totales']}"
        assert derivado == esperado, (
            f"{dom}: el inventario deriva {derivado} y la matriz dice {esperado}")
        assert esperado in texto, f"la matriz ya no declara {esperado} para {dom}"


def test_d07_es_el_unico_que_carga_el_yaml_de_su_regla():
    """El estado medido hoy, con trinquete hacia arriba: si otro dominio empieza
    a cargarla, esta prueba lo obliga a constar; si d07 dejara de hacerlo, se
    entera alguien. No juzga si la implementa bien — dice si la tiene delante."""
    c = C.cobertura_canonica()
    cargan = [f["dominio"] for f in c["dominios"]
              if f["vinculo_con_el_motor"] == C.CARGA]
    assert "d07" in cargan
    assert set(c["sin_vinculo_efectivo"]) >= {"d09"}, (
        "d09 tiene RO-IX-001 vigente; si dejara de aparecer aquí sería porque "
        "empezó a cargarla — y eso hay que celebrarlo, no esconderlo")


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_un_cno_sin_RO_no_puede_desaparecer_del_inventario():
    """REGRESIÓN de un falso negativo REAL de este mismo módulo.

    La primera versión navegaba `dominio ← RO ← CNO`. Los siete `CNO-VIII-00x`
    que **ninguna RO reclama** eran por eso invisibles, y d08 reportaba 3/3 SHA
    cuando tiene 29/29. Un canon huérfano es un tramo ANTES del problema de d09:
    allí la regla existe y el motor no la carga; aquí la cadena se modeló y
    nunca llegó a ser regla. Invisibilizarlo es la peor de las dos."""
    e = C.estado_canonico("d08")
    assert len(e["cno_huerfanos"]) >= 7, (
        "volvieron a perderse los CNO que ninguna RO deriva")
    assert e["sha_totales"] >= 29, (
        f"d08 reporta {e['sha_totales']} eslabones: se está contando sólo lo "
        f"que alguna RO alcanza")


def test_ataque_citar_la_regla_no_cuenta_como_cargarla():
    """`d09/fuentes.py` nombra RO-IX-001 en un docstring. Eso no es obedecerla.

    Es la misma lección que costó cuatro correcciones en la escalera de
    apropiación: **la mención no es el uso**. Si el inventario aceptara la cita,
    d09 aparecería conforme y el hallazgo de hoy no existiría."""
    e = C.estado_canonico("d09")
    assert e["vinculo_con_el_motor"] == C.CITA
    assert e["modulos_que_la_nombran"], "d09 sí nombra su RO en alguna parte"
    assert C.CARGA != e["vinculo_con_el_motor"]


def test_ataque_el_inventario_no_recuenta_los_ataques_por_su_cuenta():
    """No reimplementa lo que `apropiacion` ya deriva. Dos formas de contar lo
    mismo divergen siempre —`test_12` se rompió cuatro veces por eso— y un
    inventario que contradice a otro es peor que no tener ninguno."""
    from app.agents import apropiacion as A

    fuente = (RAIZ / "app" / "agents" / "canon.py").read_text(encoding="utf-8")
    assert "def test_" not in fuente and "adversarial" not in fuente, (
        "canon.py está deduciendo ataques por su cuenta en vez de consumirlos")

    oficial = {f["dominio"]: f.get("ataques_ejecutados", 0)
               for f in A.cobertura_de_la_plataforma()["dominios"]}
    for fila in C.cobertura_canonica()["dominios"]:
        if fila["dominio"] in oficial:
            assert fila["ataques_ejecutados"] == oficial[fila["dominio"]]


def test_ataque_un_dominio_sin_RO_no_se_reporta_como_incumplidor():
    """Sin RO vigente no hay regla que cargar, y eso **no es un incumplimiento**:
    es una etapa anterior. Colapsarlos acusaría de desobedecer a quien todavía
    no tiene qué obedecer — el mismo error que el dominio persigue afuera."""
    c = C.cobertura_canonica()
    for fila in c["dominios"]:
        if not fila["ro_vigentes"]:
            assert fila["dominio"] not in c["sin_vinculo_efectivo"]


def test_la_afirmacion_se_compone_del_estado_medido():
    """No hay frase escrita a mano: si cambia el estado, cambia la frase. Un
    texto fijo sobreviviría a la corrección del defecto que describe."""
    c = C.cobertura_canonica()
    frase = c["afirmacion_sostenible"]
    for d in c["sin_vinculo_efectivo"]:
        assert d in frase, f"{d} no aparece en la afirmación que lo describe"
    assert "d07" in frase


def test_el_inventario_responde_lo_que_hoy_nadie_podia_consultar():
    """La prueba de propósito. Estas cuatro preguntas son exactamente las que se
    respondieron mal hoy por no poder consultarlas."""
    e = C.estado_canonico("d09")
    assert e["cno_vigentes"] == ["CNO-IX-001"]      # ¿existe el canon jurídico?
    assert e["sha_sellados"] == 10                  # ¿está sellado?
    assert e["ro_vigentes"] == ["RO-IX-001"]        # ¿hay regla operativa?
    assert e["vinculo_con_el_motor"] != C.CARGA     # ¿el motor la obedece?


# ── ATAQUES NACIDOS DE LA ACUSACIÓN FALSA A d02 (2026-08-30) ─────────────────
def test_ataque_el_universo_de_un_dominio_no_es_su_carpeta():
    """REGRESIÓN del error que hizo acusar a d02 injustamente.

    El universo de d02 no es `app/agents/d02/`: es eso **más
    `scripts/enrich_presupuesto.py`**, donde su motor delega y donde vive el
    parámetro. Mirar sólo la carpeta dejaba fuera justo el archivo que importaba.
    Los scripts delegados se derivan del código, no de una lista escrita a mano."""
    u = C.universo_del_dominio("d02")
    rel = [p.as_posix() for p in u]
    assert any("scripts/enrich_presupuesto.py" in r for r in rel), (
        "el universo volvió a reducirse a la carpeta del paquete")
    assert any("app/agents/d02/motor.py" in r for r in rel)


def test_ataque_d02_no_puede_volver_a_reportarse_como_el_peor_caso():
    """La acusación falsa, fijada como regresión.

    El inventario dijo que d02 «ni siquiera nombra su RO», sugiriendo el peor
    estado de todos. Falso: `ADR-038/039` definen que la RO de d02 se
    **materializa por compilación**, y d02 es el que mejor se ajusta a ese
    diseño. Medir una sola vía convirtió un dominio conforme en el acusado."""
    e = C.estado_canonico("d02")
    assert e["vinculo_con_el_motor"] != C.AUSENTE, (
        "el inventario volvió a medir una sola vía de consumo")
    assert e["ro_vigentes"] == ["RO-IV-001"]
    assert C._familia_a_dominio()["IV"] == "d02"


def test_ataque_una_copia_caduca_se_detecta_antes_de_su_fecha():
    """LA ALARMA, no el inventario.

    `enrich_presupuesto.py` fija 65 y `RO-IV-001` declara 65 hasta 2026-12-31 y
    **70 desde 2027-01-01**. Hoy no hay error de dato; el 1 de enero de 2027 lo
    habrá y nada avisaría. Detectarlo antes es la diferencia entre saber que algo
    se rompió y saber que va a romperse."""
    e = C.estado_canonico("d02")
    caducas = e["copias_caducas"]
    assert caducas, "dejó de verse la copia del umbral COOTAD"
    assert any(c["archivo"].endswith("enrich_presupuesto.py") for c in caducas)
    una = next(c for c in caducas if c["umbral"] == 65)
    assert 70 in una["cambia_a"], f"no ve el tramo futuro: {una}"


def test_la_afirmacion_distingue_las_tres_vias():
    """La frase ya no puede decir «no cargan su RO» a secas: debe decir POR CUÁL
    vía llega cada dominio. Una acusación sin universo declarado es lo que hubo
    que retirar."""
    f = C.cobertura_canonica()["afirmacion_sostenible"]
    assert "carga_el_yaml" in f and "d07" in f
    assert "parametro_copiado" in f and "d02" in f
    assert "65" in f and "70" in f, "la alarma de caducidad no llega a la frase"


def test_nadie_lee_todavia_el_puente_compilado():
    """El hallazgo estructural, con trinquete al revés: las 13 RO están
    compiladas en `snapshot["brn_cno"]` con `umbral_vigente` y
    `vigencia_operativa` —el puente está tendido, firmado y al día— y ningún
    motor lo cruza. El día que uno lo haga, esta prueba lo obliga a constar."""
    c = C.cobertura_canonica()
    leen = [f["dominio"] for f in c["dominios"]
            if f["vinculo_con_el_motor"] == C.COMPILADO]
    assert leen == [], (
        f"{leen} empezó a leer el compilado — actualizar el hallazgo: la vía "
        f"canónica de ADR-038/039 dejó de estar sin tráfico")


# ── BARRIDO DE PARÁMETROS COPIADOS · d01·d03·d07·d08·d09 (2026-08-30) ────────
def test_d03_esta_limpio_Y_ESO_ES_DEMOSTRABLE():
    """d03 declara `umbral: 85` — un valor **buscable** — y no aparece copiado en
    su universo. Es el único veredicto de limpieza que se sostiene: hay algo que
    buscar, se buscó, y no está."""
    e = C.estado_canonico("d03")
    assert e["veredicto_parametros"] == "limpio_comprobado"
    assert e["parametros_copiados"] == []
    assert e["parametros_no_verificables"] == [], (
        "si a d03 le apareciera un parámetro indistinguible, su limpieza dejaría "
        "de estar demostrada y pasaría a ser sólo no comprobable")


def test_ataque_limpio_no_es_lo_mismo_que_no_comprobable():
    """LA DISTINCIÓN QUE SALVA EL INVENTARIO DE MENTIR.

    d01 y d09 declaran `umbral: 100`, indistinguible de cualquier porcentaje del
    código. No se halló copia **porque no se pudo buscar**, y eso no es una
    absolución. Colapsar ambos casos en «limpio» sería exactamente el error que
    el dominio persigue afuera: *«no lo encontré» ≠ «no existe»*."""
    for dom in ("d01", "d09"):
        e = C.estado_canonico(dom)
        assert e["veredicto_parametros"] == "no_comprobable", (
            f"{dom} se está declarando limpio sin poder demostrarlo")
        assert e["parametros_no_verificables"], (
            f"{dom} debe declarar QUÉ parámetros no pudo buscar")


def test_la_obsolescencia_programada_es_un_caso_aislado():
    """El resultado del barrido, con trinquete. Sólo d02 tiene copias que
    caducan. Si mañana apareciera otra, esta prueba obliga a mirarla en vez de
    dejarla pasar entre las que ya se conocen."""
    c = C.cobertura_canonica()
    con_caducas = sorted({x["archivo"].split("/")[-1] and f["dominio"]
                          for f in c["dominios"] for x in f["copias_caducas"]})
    assert con_caducas == ["d02"], (
        f"apareció obsolescencia programada fuera de d02: {con_caducas}")


def test_d07_replica_su_plazo_normativo_como_respaldo():
    """MATIZ, no acusación. d07 **sí** carga su RO, y aun así
    `scoring.py` fija `else 15` cuando el plazo no llega. Un respaldo que repite
    el valor normativo hace que, si la RO deja de leerse, el sistema siga
    calculando en silencio con el número viejo en lugar de detenerse — el mismo
    patrón del cable que escribía vacío al no hallar su fuente."""
    e = C.estado_canonico("d07")
    assert e["vinculo_con_el_motor"] == C.CARGA, "d07 dejó de cargar su RO"
    respaldo = [c for c in e["parametros_copiados"]
                if c["archivo"].endswith("scoring.py")]
    assert respaldo, "dejó de verse el respaldo del día 15 en d07/scoring.py"
    assert not e["copias_caducas"], "el plazo de d07 no tiene tramo futuro"
