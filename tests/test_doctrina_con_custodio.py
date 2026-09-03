# -*- coding: utf-8 -*-
"""
tests/test_doctrina_con_custodio.py — que BOOT deje de crecer, y por construcción
════════════════════════════════════════════════════════════════════════════════
Javo, 2026-09-02:

> *«BOOT está crónicamente al límite. Ese es un problema para cada iteración, y
> vamos a seguir meses trabajando en QUIRA. Debemos resolverlo.»*

MEDIDO ANTES DE TOCAR:

  · BOOT lleva **doce revisiones pegado al techo** de 6000 bytes (29-ago → hoy);
  · §AHORA es el **48%** del archivo;
  · de sus 26 líneas, **sólo 7 son estado** — las otras 19 son doctrina
    permanente, y la doctrina no se sustituye: se acumula. Un ADR nuevo, una
    línea más, para siempre.

`check_health` declara BOOT «única fuente de estado vivo». Dejó de serlo, y el
presupuesto —dimensionado para estado— ahoga a la doctrina.

LA CAUSA DE QUE NADA PUDIERA SALIR: nadie podía saber qué línea era la ÚNICA
defensa de una regla y cuál un recordatorio de algo ya garantizado. Quitar la
equivocada desprotege el sistema, así que no se quitaba ninguna.

    Una regla en un documento de arranque es una nota que hay que recordar.
    Una regla con verificador es una regla que se aplica sola.

Estas pruebas fijan el mecanismo que lo resuelve, y la tercera es la que impide
que el problema vuelva: **una regla migrada no puede seguir ocupando BOOT**.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import doctrina as DOC                      # noqa: E402


# ── EL MECANISMO ──────────────────────────────────────────────────────────────
def test_toda_regla_migrada_nombra_un_verificador_que_existe():
    """La misma exigencia que `deuda.py` le hace a cada deuda, y por la misma
    razón: nombrar un verificador inexistente sería acreditar sin nada detrás.

    Es el escalón 2 de la escalera —declarado ≠ existente— aplicado a la
    custodia de la doctrina."""
    c = DOC.cobertura_de_doctrina()
    assert c["reglas"], "el registro de doctrina quedó vacío"
    assert not c["sin_verificador"], (
        f"reglas que declaran un verificador inexistente: {c['sin_verificador']}. "
        f"Salieron de BOOT y no las sostiene nada")


def test_el_registro_declara_que_es_parcial():
    """C0. Un registro de doctrina que no declarara su alcance haría creer que
    la doctrina restante de BOOT no tiene gate, cuando lo que pasa es que el
    vínculo no se ha establecido. La diferencia es la de siempre: «no medido» no
    es «no existe»."""
    u = DOC.cobertura_de_doctrina()["universo"]
    assert u["mecanismo"]["tipo"] == "explicitamente_limitado"
    assert any("todavía no se estableció" in x for x in u["fuera_de_alcance"])
    assert "leyendo" in u["como"].lower(), (
        "el registro dejó de declarar que el vínculo se establece leyendo: "
        "derivarlo por búsqueda de términos dio 18 de 19 y era falso")


# ── LO QUE IMPIDE QUE EL PROBLEMA VUELVA ─────────────────────────────────────
def test_una_regla_con_custodio_no_vuelve_a_ocupar_BOOT():
    """EL TRINQUETE. Sin esto, la doctrina migrada reaparecería en §AHORA en la
    siguiente sesión —«por si acaso»— y BOOT volvería al techo.

    Se comprueba por la frase que sólo esa línea tenía, no por el concepto: el
    concepto puede mencionarse al explicar otra cosa, y prohibirlo obligaría a
    escribir BOOT sin poder nombrar lo que el sistema hace."""
    boot = (RAIZ / "governance" / "BOOT.md").read_text(encoding="utf-8")
    migradas = {
        "DOC-002": "«no existe»≠«no pude obtener»≠«falló»",
        "DOC-001": "`conftest` corta subprocess/red",
        "DOC-004": "(`env_obs`≠`env_ops`)",
        "DOC-005": "nace en el GENERADOR sin reloj",
    }
    for rid, frase in migradas.items():
        assert frase not in boot, (
            f"{rid} volvió a BOOT: «{frase}». Ya la sostiene "
            f"{DOC.puede_salir_de_boot(rid)['por_que']} — repetirla en el "
            f"arranque devuelve el archivo al techo sin proteger nada nuevo")


def test_boot_apunta_al_registro():
    """Lo que salió no se perdió: cambió de custodio. Si BOOT no lo dice, quien
    arranque creerá que la doctrina desapareció — y la reescribirá."""
    boot = (RAIZ / "governance" / "BOOT.md").read_text(encoding="utf-8")
    assert "doctrina.py" in boot
    assert "cambia de custodio" in boot


# ── EL PATRÓN 48,33 APLICADO A LA GOBERNANZA ─────────────────────────────────
def test_las_cifras_de_boot_no_divergen_de_su_fuente():
    """*Derivado narrativo desacoplado de la fuente canónica* — el patrón que
    nombró el colega tras el «48,33 %», y BOOT tiene exactamente esa forma:
    prosa con números escritos a mano.

    En una sola sesión hubo que corregirle dos —«0 rutas fijas» cuando eran 3,
    «12 GATES» cuando sólo corría uno— y se corrigieron porque alguien miró, no
    porque algo avisara. Ahora avisa.

    ⚠️ NO SE GENERA BOOT. Generarlo lo volvería ilegible, y BOOT vale
    precisamente porque lo escribe una persona. Lo que se verifica es que lo
    escrito no contradiga a su fuente."""
    fuera = DOC.cifras_de_boot_divergentes()
    assert not fuera, (
        "BOOT afirma cifras que su fuente viva contradice: "
        + " · ".join(f"dice «{d['en_boot']}» y {d['fuente']} dice «{d['real']}»"
                     for d in fuera))


def test_el_tope_de_boot_sigue_siendo_una_decision_y_no_un_estorbo():
    """⚠️ LA TENTACIÓN QUE HABÍA QUE NO TOMAR, fijada como prueba.

    Ante «BOOT no cabe» la salida fácil era subir el tope: 6000 bytes son ~1500
    tokens, y en una sesión de millones eso no ahorra nada medible. Pero el tope
    NO existe para ahorrar tokens — existe para **forzar síntesis**. Un BOOT de
    20.000 bytes nadie lo lee bien, y entonces deja de proteger.

    Subirlo habría quitado la presión que produjo este registro. Si algún día se
    sube, que sea una decisión escrita y no el resultado de no encontrar qué
    recortar; esta prueba obliga a pasar por aquí."""
    fuente = (RAIZ / "scripts" / "ci" / "check_health.py").read_text(encoding="utf-8")
    import re
    m = re.search(r'"governance/BOOT\.md":\s*(\d+)', fuente)
    assert m, "cambió la forma del presupuesto de BOOT"
    assert int(m.group(1)) == 6000, (
        f"el tope de BOOT pasó a {m.group(1)}. Si fue deliberado, actualiza esta "
        f"prueba y deja escrito el motivo; si fue para hacer sitio, la salida "
        f"era migrar doctrina a `doctrina.py`, no ensanchar el arranque")


# ── D-009 · EL PATRÓN 48,33 EN EL RESTO DEL SISTEMA ──────────────────────────
def test_las_cifras_de_dominio_en_texto_publicado_estan_contadas():
    """D-009 · la microauditoría que pidió el colega: *¿el caso 48,33 fue
    aislado o es sistémico?*

    No fue aislado. **23 cifras de dominio escritas dentro de texto publicado,
    en 11 superficies vivas**: «Salud presupuestaria 14.58% bajo umbral COOTAD
    65%», «Participación 27.98%», «Fidelidad 72.73%: 48/66 promesas CNE».

    ⚠️ NO SE AFIRMA QUE LAS 23 ESTÉN MAL. Se afirma que **ninguna puede
    saberlo**: no declaran su fuente, y el 48,33 demostró qué ocurre entonces —
    la cifra no se entera de que su fuente cambió y sigue publicándose 22 días.
    Cada una exige decidir si es dato vivo, referencia histórica legítima o
    resto de la maqueta, y eso es curación, no un reemplazo masivo.

    EL BARRIDO SE ACOTÓ A PROPÓSITO para no inflar el hallazgo: sólo decimales
    (`14.58%`, no `100%`), sólo dentro de prosa de dominio, excluyendo CSS y
    `_deprecated`. La primera pasada daba 38 archivos contando `width:100%` —el
    mismo error de precisión falsa que el colega marcó con «39 vs 25»."""
    import io
    import re
    import tokenize

    CIFRA = re.compile(r"\d{1,3}[.,]\d{1,2}\s*%")
    CSS = re.compile(r"[{};:]\s*$|width|height|rgba|linear-gradient|@import|"
                     r"viewBox|flex|margin|padding", re.I)
    DOMINIO = re.compile(r"presupuest|particip|cobertura|meta|ejecu|salud|"
                         r"umbral|ICPI|IED|ICODS|autonom", re.I)

    halladas = []
    for d in ("quira_pages", "views", "components", "app/viz"):
        for f in (RAIZ / d).rglob("*.py"):
            rel = f.relative_to(RAIZ).as_posix()
            if "__pycache__" in rel or "_deprecated" in rel:
                continue
            try:
                toks = list(tokenize.generate_tokens(io.StringIO(
                    f.read_text(encoding="utf-8", errors="replace")).readline))
            except Exception:                               # noqa: BLE001
                continue
            for t in toks:
                if t.type != tokenize.STRING:
                    continue
                txt = " ".join(t.string.split())
                if (len(txt) <= 400 and not CSS.search(txt)
                        and CIFRA.search(txt) and DOMINIO.search(txt)):
                    halladas.append(f"{rel}:{t.start[0]}")

    # ⚠️ INVENTARIO DECLARADO, NO UN CONTEO, y la razón es un doble fallo de
    # esta misma prueba. Primero fijó «23 cadenas» y el runner contó 25.
    # Se cambió a contar archivos —«11»— y el runner contó 12, con una lista
    # DISTINTA: ve `m_planificacion` y `p10_inversion`, y no ve
    # `p_sentinel_hub`. Mismo código, mismo filtro, dos resultados.
    #
    # La causa exacta de la divergencia no se determinó, y esa es justamente la
    # razón para no seguir apoyando un trinquete en ella: un número que cambia
    # con el sistema operativo no acredita nada, y perseguirlo dos veces ya fue
    # suficiente aviso.
    #
    # Lo que SÍ es estable es la lista declarada — la unión de lo observado en
    # ambas plataformas. Se exige que lo hallado esté DENTRO de ella: si
    # aparece una superficie nueva, la prueba la nombra. Que una conocida no se
    # detecte en un sistema concreto no es señal de nada.
    CONOCIDAS = {
        "quira_pages/env_gov.py", "quira_pages/m_planificacion.py",
        "quira_pages/p10_inversion.py", "quira_pages/p11_ods.py",
        "quira_pages/p14_eficiencia.py", "quira_pages/p17_rdc.py",
        "quira_pages/p19_genero.py", "quira_pages/p3_congruencias.py",
        "quira_pages/p8_metas.py", "quira_pages/p9_sat.py",
        "quira_pages/p_command_center.py", "quira_pages/p_concejo.py",
        "quira_pages/p_sentinel_hub.py",
    }
    archivos = {h.split(":")[0] for h in halladas}
    nuevas = sorted(archivos - CONOCIDAS)
    assert not nuevas, (
        f"superficies nuevas publicando cifras escritas a mano: {nuevas}. "
        f"Publicar un número sin declarar su fuente es cómo nació el 48,33")
    assert archivos, (
        "el barrido no encontró ninguna: o D-009 se curó entera —y hay que "
        "actualizar el registro— o el filtro dejó de mirar")
