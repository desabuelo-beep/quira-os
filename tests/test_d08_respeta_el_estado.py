# -*- coding: utf-8 -*-
"""
tests/test_d08_respeta_el_estado.py — D-006, y el enunciado era otro
════════════════════════════════════════════════════════════════════════════════
D-006 estaba declarada así: *«siete `CNO-VIII-00x` no son reclamados por ninguna
RO: cadenas normativas modeladas que nunca llegaron a regla operativa»*, con
gravedad `DESACOPLA`.

MEDIDO ANTES DE TOCAR, y el enunciado no se sostuvo:

  · los siete NO son cadenas sueltas: son `participacion_y_control_social`
    entero, el canon de **d08**, y BOOT declara d08 «ENTRABLE» — sin curar;
  · todo el bloque VIII está en `propuesta`, también las tres RO que sí existen
    (`RO-VIII-001/002/003`, colgando de `CNO-VIII-000`);
  · luego **PENDIENTE + DECLARADO ≠ DEUDA**: siete cadenas sin RO en un dominio
    que aún no entra a curación es el estado esperado, no una deuda.

LA DEUDA ESTABA AL LADO, y era de otra gravedad:

    `enrich_participacion.py` leía `RO-VIII-003.yaml` —vía canónica, no una
    copia— y tomaba `umbral_activacion: 0.50` SIN mirar que la regla está en
    `estado: propuesta` con `validada_por: null`. El snapshot publicaba una
    señal ENCENDIDA (0,848 ≥ 0,50) sobre una regla que el canon declara no
    acreditada.

        D-005 fue: el umbral correcto, pero copiado.
        D-006 es: el umbral bien leído, de una regla que nadie validó.

Y al reejecutar el enricher apareció lo tercero: el índice madre publicado era
**48,33 cuando su fuente dice 27,00 desde el 2026-08-11**. Javo retiró IGP_3 el
2026-07-29 y el derivado no se volvió a correr en 22 días. La `_correccion` del
snapshot guarda la frase que lo explica todo: *«El metadato de verificacion del
2026-08-05 declaraba que coincidian y no era cierto.»*

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import brn_lector as L                      # noqa: E402


def _bloque() -> dict:
    return json.loads((RAIZ / "data" / "gm_snapshot.json").read_text(
        encoding="utf-8"))["participacion_dom"]


# ── EL CIERRE ─────────────────────────────────────────────────────────────────
def test_d08_no_publica_un_veredicto_sobre_una_regla_no_acreditada():
    """El cruce que cierra D-006. `RO-VIII-003` está en `propuesta`, así que el
    umbral no puede sostener un veredicto público — y el bloque lo DICE en vez
    de callarlo."""
    s = _bloque()["senal"]
    assert s["umbral"] is None, (
        "volvió el umbral de una regla en propuesta: D-006 se reabrió")
    assert s["estado_umbral"] == "no_consumible"
    assert "propuesta" in s["por_que"], (
        "no se dice POR QUÉ no hay umbral: sin motivo, la ausencia no es "
        "accionable")


def test_la_medicion_sobrevive_aunque_el_veredicto_no():
    """LA DISTINCIÓN QUE HACE ÚTIL EL CIERRE. Callar las dos cosas habría
    convertido «no puedo decidir» en «no hay nada que ver».

    Los 162 de 191 son un hecho de d08, medido contra el POA y verificable por
    su cuenta. Lo que carecía de autoridad era encender la señal."""
    s = _bloque()["senal"]
    assert s["numerador"] == 162 and s["denominador"] == 191
    assert round(s["valor"], 3) == 0.848


def test_el_render_declara_la_ausencia_no_la_esconde():
    """El render tenía `if not denominador: return ""` — callar. Ahora, sin
    umbral acreditado, publica la medición y dice que el veredicto no está
    disponible: la ausencia declarada es información (C0 · regla 2)."""
    fuente = (RAIZ / "app" / "viz" / "render" / "participacion_render.py").read_text(
        encoding="utf-8")
    assert 'estado_umbral") == "no_consumible"' in fuente
    assert "SIN UMBRAL ACREDITADO" in fuente
    cuerpo = fuente.split("def _senal(")[1].split("\ndef ")[0]
    assert "0.5" not in cuerpo and "0.50" not in cuerpo, (
        "el render se escribió un umbral propio: la copia volvió por otra puerta")


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_los_siete_CNO_sin_RO_siguen_visibles():
    """LO QUE NO SE REPARÓ, Y NO DEBÍA REPARARSE. El colega lo fijó: *«no cree
    reglas para satisfacer al gate»*.

    Fabricar siete RO habría hecho desaparecer el hallazgo sin que nada mejore,
    y habría sido peor que la deuda: reglas operativas inventadas para que un
    inventario dé cero. Los siete siguen ahí, en `propuesta`, contados y
    visibles — que es exactamente lo que un dominio sin curar debe mostrar."""
    from app.agents import canon as K

    ids = set(K.cno_huerfanos("d08"))
    assert len([x for x in ids if x.startswith("CNO-VIII-00")]) == 7, (
        f"cambió el número de CNO-VIII sin RO: {sorted(ids)}. Si BAJÓ, hay que "
        f"verificar que la RO nueva es canon real y no una regla fabricada")


def test_ataque_todo_el_bloque_VIII_esta_en_propuesta():
    """LA RAZÓN por la que los siete no son deuda, fijada como prueba. Si alguna
    pieza de VIII pasara a `vigente` sin que d08 se cure, este test falla — y
    ese fallo pregunta lo correcto: ¿quién la promovió, y con qué evidencia?"""
    for rid in ("RO-VIII-001", "RO-VIII-002", "RO-VIII-003"):
        r = L.regla(rid)
        assert r is not None, f"{rid} desapareció del catálogo"
        assert r.estado_pieza == "propuesta", (
            f"{rid} pasó a «{r.estado_pieza}»: si d08 se curó, D-006 avanzó y "
            f"esta prueba debe actualizarse; si no, alguien promovió una regla "
            f"sin curar el dominio")
        assert not r.es_consumible_como_vigente


def test_ataque_la_nota_publica_no_tiene_cifras_escritas_a_mano():
    """EL TERCER HALLAZGO, y era el más grave porque llegaba al lector.

    `p16_gobernanza` publicaba una «Nota metodológica» con `48.33%` y el método
    de TRES componentes — el que Javo retiró el 2026-07-29 al quitar IGP_3—.
    Estuvo 22 días contradiciendo al motor, que calcula 27,00.

    No fue una cifra que se quedó atrás por descuido: fue una cifra ESCRITA A
    MANO, y por eso no pudo enterarse de que su fuente había cambiado."""
    fuente = (RAIZ / "quira_pages" / "p16_gobernanza.py").read_text(encoding="utf-8")
    nota = fuente.split("igp_nota = f\"\"\"")[1].split('"""')[0]
    for cifra in ("48.33", "48,33", "(54%)", "(91%)", "27.98%"):
        assert cifra not in nota, (
            f"volvió una cifra escrita a mano a la nota publicada: «{cifra}»")
    assert "cargar_gm_snapshot()" in fuente, "la nota dejó de derivar del motor"


def test_ataque_el_indice_madre_no_se_queda_atras_de_su_fuente():
    """El derivado publicado debe coincidir con `vectores.igp`, que es su fuente.
    Estuvieron 22 días divergiendo —48,33 publicado contra 27,00 real— porque
    nadie reejecutó el enricher tras la corrección.

    ⚠️ ESTA PRUEBA NO REPARA LA CAUSA: sólo detecta la divergencia. Que un
    derivado se recalcule cuando su fuente cambia sigue sin estar garantizado,
    y eso vive en D-007 — los enrichers tampoco corren en CI."""
    snap = json.loads((RAIZ / "data" / "gm_snapshot.json").read_text(encoding="utf-8"))
    fuente = (snap.get("vectores") or {}).get("igp") or {}
    publicado = _bloque().get("indice_madre") or {}
    assert publicado.get("valor") == fuente.get("valor"), (
        f"el bloque publica {publicado.get('valor')} y su fuente dice "
        f"{fuente.get('valor')}: hay que reejecutar enrich_participacion.py")


# ── LA FRONTERA DOCUMENTAL d08 ↔ d09 ─────────────────────────────────────────
def test_d08_no_ilustra_su_vitalidad_con_evidencia_de_d09():
    """EL HALLAZGO DE JAVO (2026-09-03), y lo llamó garrafal con razón.

    `enrich_participacion.py` leía `snap["rendicion"]["serie"]` —el bloque de
    d09— y pintaba la asistencia a las JORNADAS DE RENDICIÓN como indicio de
    vitalidad democrática. El mismo gráfico —201 · 261 · 322— salía en los dos
    cajones, y un lector veía «participación creciente» en dos dominios
    distintos con un dato que sólo pertenece a uno.

    La regla que el colega fijó a partir de esto:

        Un documento puede ser evidencia para un dominio sin ser documento
        primigenio de ese dominio.

    El acta de rendición es primigenia de d09. Para d08 no es ni siquiera
    evidencia del mecanismo que esa dimensión mide.

    ⚠️ Y LA AFIRMACIÓN DE AUSENCIA ERA FALSA, que es lo más grave: el pie decía
    «el único registro de asistencia disponible». Medido sobre la carpeta del
    Holding: **31 actas de mecanismos PROPIOS declaran registro anexo** —28
    audiencias, 2 de PP, 1 cabildo— y sólo una lo expresa en cifras. No falta el
    registro: falta su digitalización. Decir «no hay» donde hay «hay,
    escaneado» convierte un límite del instrumento en una ausencia del sujeto."""
    # ⚠️ SE MIDE EL CÓDIGO, NO EL TEXTO. La primera versión de esta prueba
    # falló contra el comentario que explica qué se retiró —«aquí se leía
    # snap["rendicion"]["serie"]»—. Es el mismo falso positivo que ya cazó al
    # gate visual y a `canon.py`: documentar un defecto no es cometerlo, y una
    # prueba que lo confunde obliga a corregir sin poder explicar.
    import io
    import tokenize

    ruta = RAIZ / "scripts" / "enrich_participacion.py"
    toks = tokenize.generate_tokens(io.StringIO(
        ruta.read_text(encoding="utf-8")).readline)
    codigo = "\n".join(t.string for t in toks if t.type != tokenize.COMMENT)
    lecturas = [ln for ln in codigo.splitlines()
                if 'get("rendicion")' in ln or '["rendicion"]' in ln]
    assert not lecturas, (
        f"d08 volvió a leer el bloque de d09: {lecturas}. La evidencia de "
        f"rendición no puede ilustrar una dimensión de participación")

    v = _bloque()["vitalidad"]
    assert "dato_disponible" not in v, (
        "volvió el campo que traía la asistencia de las jornadas de rendición")
    assert v.get("expediente_propio"), (
        "d08 dejó de mostrar su expediente propio: sin él, la dimensión queda "
        "sin nada que la sostenga y vuelve la tentación de tomarlo prestado")
    assert "digitalización" in v.get("bloqueo", ""), (
        "el bloqueo dejó de decir que lo que falta es la DIGITALIZACIÓN del "
        "registro, no el registro")


def test_el_render_no_publica_asistencia_ajena():
    """La otra mitad: que el gráfico no vuelva por la puerta de la vista.

    Se comprueba la frase que sólo ese pie tenía, no el concepto: nombrar la
    rendición al explicar POR QUÉ no se usa aquí es legítimo — y de hecho el
    bloque nuevo lo hace."""
    fuente = (RAIZ / "app" / "viz" / "render" / "participacion_render.py").read_text(
        encoding="utf-8")
    cuerpo = fuente.split("def _vitalidad")[1].split("\ndef ")[0]
    assert "El único registro de asistencia disponible" not in cuerpo, (
        "volvió la afirmación de ausencia que 31 actas contradicen")
    assert 'x["asistentes"]' not in cuerpo, (
        "volvió el gráfico de asistencia a las jornadas de rendición")
    assert "no se muestra aquí" in cuerpo, (
        "el render dejó de declarar por qué la asistencia de rendición no está "
        "en esta dimensión — y sin decirlo, su ausencia parece un olvido")
