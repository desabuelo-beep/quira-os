# -*- coding: utf-8 -*-
"""
tests/test_datos_procedencia.py — CAPA 3 · procedencia de los ARTEFACTOS
════════════════════════════════════════════════════════════════════════════════
`procedencia.py` modela la procedencia de una **afirmación**. C3 pregunta por la
de los **artefactos**: los 2.213 archivos de `data/`. Son cosas distintas y
sólo la primera estaba cubierta.

EL HALLAZGO, y no es una acusación:

    1360000430001    31 artefactos · 2026-05-25 → 2026-06-16
    1360001010001   158 artefactos · 2026-08-18 → 2026-09-01
                    NO se solapan — sucesión limpia

La identidad del sujeto **tiene versiones**. Los artefactos anteriores al cambio
llevan el RUC previo y son correctos para su época; lo que falta es que declaren
bajo qué versión se produjeron.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import datos as D                         # noqa: E402


def test_las_identidades_del_sujeto_se_suceden_y_no_conviven():
    """LA PROPIEDAD GRAVE, con trinquete.

    Que un artefacto lleve una identidad anterior es normal: la del perfil
    cambió y su propia nota lo registra («no estaba huellado», cerrado el
    2026-08-26). Lo que sería grave es que **dos identidades estuvieran activas
    a la vez** sobre el mismo sujeto — eso ya no sería historia, sería
    ambigüedad viva."""
    c = D.cobertura_de_datos()
    assert not c["identidades_que_conviven"], (
        f"dos identidades del sujeto activas a la vez: "
        f"{c['identidades_que_conviven']}")
    assert len(c["identidades_del_sujeto"]) >= 2, (
        "dejó de verse la sucesión de identidades: el hallazgo se perdió")


def test_el_ruc_vigente_es_el_ultimo_de_la_sucesion():
    """La identidad más reciente en los artefactos debe ser la que el perfil
    declara. Si divergieran, el sistema estaría produciendo evidencia bajo una
    identidad que su propio canon no reconoce."""
    from app.agents import sujeto as S
    import json

    perfil = json.loads((S._SUJETOS / f"{S.POR_DEFECTO}.json").read_text(encoding="utf-8"))
    canonico = str(perfil["identidad_en_fuentes"]["ruc"])
    ultima = D.identidades_del_sujeto()[-1]["identidad"]
    assert ultima == canonico, (
        f"los artefactos más recientes usan {ultima} y el perfil declara "
        f"{canonico}")


# ── ATAQUES AL DETECTOR ───────────────────────────────────────────────────────
def test_ataque_un_ensayo_no_es_un_artefacto_sin_procedencia():
    """REGRESIÓN del octavo falso positivo, evitado por poco.

    185 archivos viven en un directorio llamado **`provenance/ensayos`** y no
    llevaban ninguna de las marcas que el detector buscaba. Parecía «artefactos
    de procedencia sin procedencia». Declaran `dry_run: true`: **son ensayos que
    declaran serlo**, material de ingeniería, no evidencia de observación."""
    c = D.cobertura_de_datos()
    assert c["por_estado"].get(D.ENSAYO, 0) >= 180, (
        "los ensayos dejaron de reconocerse y volverán a contarse como huérfanos")
    ensayos = [a for a in D.artefactos_json() if a["estado"] == D.ENSAYO]
    assert all("ensayo" in a["artefacto"] or "provenance" in a["artefacto"]
               for a in ensayos[:20])


def test_ataque_el_detector_busca_por_patron_y_a_profundidad():
    """El primer detector usaba una LISTA de marcas y sólo el primer nivel: dio
    **221 falsos positivos**. `ack_registry.json` lleva `meta` sin guion bajo y
    `cadena_estado.json` guarda sus sellos dentro de las etapas. Con patrón y
    profundidad quedan 13 — y aun así se llaman «sin marca hallada», no «sin
    procedencia»: el detector no es autoridad sobre lo que no ve."""
    c = D.cobertura_de_datos()
    assert c["por_estado"].get(D.SIN_MARCA, 999) < 40, (
        f"volvieron los falsos positivos: {c['por_estado'].get(D.SIN_MARCA)}")
    fuente = (RAIZ / "app" / "agents" / "datos.py").read_text(encoding="utf-8")
    assert "prof + 1" in fuente, "el detector dejó de mirar en profundidad"
    assert D.SIN_MARCA == "sin_marca_hallada", (
        "el estado se renombró a algo que afirma más de lo medido")


def test_el_universo_declara_que_no_mide_la_mayor_parte_del_volumen():
    """`data/` tiene 943 CSV, 774 binarios, 16 PDF y 13 hojas de cálculo. Este
    detector sólo lee JSON. Decir «85 con procedencia» sin decir eso invitaría a
    leer como medido lo que ni siquiera se miró."""
    limites = " ".join(D.cobertura_de_datos()["universo"]["fuera_de_alcance"]).lower()
    assert "csv" in limites and "no está medida" in limites
    assert "mayor parte del volumen" in D.cobertura_de_datos()["afirmacion_sostenible"]


# ── A · LA CADENA DE CAPTURA · ¿puede el artefacto volver a su origen? ────────
def test_los_binarios_capturados_pueden_volver_a_su_url_de_origen():
    """LA PREGUNTA FUERTE DE C3, y la respuesta es sí de la forma más sólida
    posible: **el nombre del `.bin` es el SHA-256 de su URL de origen**.

        clave = hashlib.sha256(url.encode()).hexdigest()[:16]

    422 binarios, 422 registros con URL, correspondencia 422/422 en ambas
    direcciones. La procedencia viaja en el nombre del archivo."""
    c = D.cadena_de_captura()
    if c["estado"] == "no_determinable":
        import pytest
        pytest.skip(c["por_que"])
    assert c["estado"] == D.RESUELTA
    assert c["correspondencia"] == c["binarios"] == c["registros_con_url"]
    assert not c["binarios_sin_registro"] and not c["registros_sin_binario"]


def test_ataque_buscar_una_ruta_literal_no_demuestra_ausencia():
    """REGRESIÓN DE UN FALSO POSITIVO PROPIO, y de los más instructivos.

    La primera búsqueda concluyó «422 binarios sin registro de procedencia».
    Buscó `data/lotaip/artefactos` como texto literal — y el código la
    **compone**: `CACHE = RAIZ / "data" / "lotaip" / "artefactos"`. El grafo de
    acoplamiento ya declaraba ese límite —83% de rutas no resolubles— y el
    ataque siguiente lo ignoró al interpretar su propio resultado.

    **Declarar un límite no sirve de nada si no se respeta al leer.**"""
    productor = (RAIZ / "scripts" / "normativa" / "inventario_contenido.py").read_text(encoding="utf-8")
    assert 'CACHE = RAIZ / "data" / "lotaip" / "artefactos"' in productor, (
        "cambió la forma de componer la ruta: revisar si el hallazgo sigue")
    assert "hashlib.sha256(c[\"url\"].encode()).hexdigest()[:16]" in productor, (
        "cambió la derivación de la clave: la procedencia ya no viajaría en el "
        "nombre del artefacto")


# ── B · EL ARTEFACTO QUE EL MECANISMO NO PUEDE INTERPRETAR ────────────────────
def test_el_json_ilegible_es_un_formulario_humano_sin_consumidor():
    """No «hay un JSON corrupto», sino **«hay un artefacto que el mecanismo
    actual no puede interpretar»** — y su naturaleza importa.

    `data/validacion_reconciliacion_2025.json` se declara «Muestra para
    validación humana · reconciliación PAC↔POA 2025 · llenar
    revision_humana=OK/ERROR». Falla porque una respuesta quedó **sin comillas**
    (`"revision_humana": ok`), y ningún código lo consume.

    ⚠️ NO SE REPARA. Que el formato pedido a un humano sea JSON —que se rompe
    con unas comillas— es una decisión de diseño, no un error a parchear aquí."""
    f = RAIZ / "data" / "validacion_reconciliacion_2025.json"
    if not f.exists():
        import pytest
        pytest.skip("el artefacto ya no está")
    crudo = f.read_text(encoding="utf-8", errors="replace")
    assert "validación humana" in crudo and "revision_humana" in crudo
    ilegibles = [a for a in D.artefactos_json() if a["estado"] == D.ILEGIBLE]
    assert len(ilegibles) == 1, f"cambió el conjunto de ilegibles: {ilegibles}"


# ── C · IDENTIDAD TEMPORAL, generalizada ─────────────────────────────────────
def test_ningun_artefacto_declara_bajo_que_version_de_identidad_se_produjo():
    """LA PROPIEDAD GENERALIZABLE, más allá del caso Montecristi:

    > cuando cambia un atributo que participa en la identificación del sujeto,
    > ¿los artefactos históricos conservan explícitamente la versión de
    > identidad bajo la cual fueron producidos?

    Hoy **no**. Se reconstruye por la fecha, lo que exige recordar cuándo
    cambió. Esta prueba fija ese estado: el día que un artefacto declare su
    versión de identidad, habrá que reescribirla — y ése será el progreso."""
    con_version = [a for a in D.artefactos_json()
                   if any("version_identidad" in m or "identidad_vigente" in m
                          for m in a.get("marcas", []))]
    assert not con_version, (
        f"{len(con_version)} artefactos ya declaran su versión de identidad: "
        f"actualizar el hallazgo, esto dejó de ser una carencia")
    assert len(D.identidades_del_sujeto()) >= 2, (
        "sin al menos dos identidades observadas, la propiedad no es medible aquí")


# ── C3 CONSOLIDADA · los cuatro estados, juntos ──────────────────────────────
def test_el_estado_de_la_capa_3_es_el_demostrado():
    """LA CONSOLIDACIÓN, tal como el colega la fijó — y ninguno de los cuatro
    estados es automáticamente un «defecto»:

        A  BIN → índice → origen     procedencia_resuelta   422/422
        B  JSON ilegible             ilegible               1
        C  identidad temporal        no versionada          demostrado
        D  resto del universo        NO medido              declarado

    Esa disciplina —no convertir un estado en acusación— es lo que hizo que esta
    capa produjera más evidencia y menos falsos positivos que ninguna otra."""
    c = D.cobertura_de_datos()
    cadena = D.cadena_de_captura()

    # A · resuelta y completa
    assert cadena["estado"] == D.RESUELTA and cadena["correspondencia"] == 422
    # B · exactamente un ilegible, y no se llama «corrupto»
    assert c["por_estado"].get(D.ILEGIBLE, 0) == 1
    # C · identidades en sucesión, sin versión declarada en el artefacto
    assert len(c["identidades_del_sujeto"]) >= 2
    assert not c["identidades_que_conviven"]
    # D · el límite sigue declarado, no disimulado
    limites = " ".join(c["universo"]["fuera_de_alcance"]).lower()
    assert "csv" in limites and "no está medida" in limites


# ── LA EVIDENCIA PRIMARIA VIVE FUERA DEL REPOSITORIO (2026-09-01) ────────────
def test_el_universo_declara_que_la_evidencia_primaria_esta_fuera():
    """CORRECCIÓN DE JAVO, y es la décima vez del mismo patrón:

    > *«para trabajar el Excel canónico Gold Master, eso se construyó con los
    > documentos de la carpeta local»* — `Holding_Municipal_Montecristi`, con
    > documentos de la web del GAD, pedidos de acceso a la información, SERCOP y
    > CPCCS.

    C3 midió `data/` del repositorio. La evidencia primaria **no está ahí**. Y
    el sistema sí conocía ese territorio —`config.DATOS_DIR` apunta a él y
    `check_portabilidad` lo llama «la frontera»—: quien no lo miró fue este
    módulo. Ahora el límite está escrito en el universo."""
    limites = " ".join(D.cobertura_de_datos()["universo"]["fuera_de_alcance"])
    assert "Holding_Municipal_Montecristi" in limites
    assert "EVIDENCIA PRIMARIA" in limites.upper()


def test_los_documentos_no_hallados_son_no_determinables_no_ausentes():
    """APLICACIÓN DE LA REGLA 2 DE C0 A ESTE PROPIO MÓDULO.

    De 258 documentos oficiales, el barrido señala 36. Los otros 204 **no se
    llaman «sin trazabilidad»**: este instrumento sólo lee JSON/YAML del
    repositorio y busca por nombre — el Gold Master es `.xlsx`, como 91 de esos
    documentos, y no se abre aquí.

    Leer el silencio del instrumento como ausencia es exactamente lo que la
    sesión acaba de prohibir, y costó un falso positivo hace dos turnos."""
    e = D.evidencia_primaria()
    if e.get("estado") == "no_determinable":
        import pytest
        pytest.skip(e["por_que"])
    # 249, no 258: al excluir `desktop.ini` el universo bajó 9. Esta prueba
    # falló al hacerlo — y ése era su trabajo: un umbral que no se entera de que
    # el universo cambió no está midiendo nada.
    assert e["documentos"] >= 240
    assert e["citados_por_artefactos"] + e["no_determinables"] == e["nombres_unicos"]
    assert "no determinables" in e["limite"], (
        "el resultado dejó de declarar que los no hallados son indeterminados")
    assert "sin trazabilidad" in e["limite"], (
        "debe decir EXPLÍCITAMENTE lo que NO significa el número")


def test_la_raiz_de_evidencia_primaria_se_deriva_de_config():
    """0 rutas fijas: el territorio se alcanza por `config.DATOS_DIR`, nunca
    escribiendo el disco de una persona — la regla que `sentinel/` incumple y
    que este módulo no puede empezar a incumplir también."""
    fuente = (RAIZ / "app" / "agents" / "datos.py").read_text(encoding="utf-8")
    assert "from config import DATOS_DIR" in fuente
    assert "C:\\Users" not in fuente and "C:/Users" not in fuente


def test_la_metrica_declara_su_unidad_y_excluye_el_ruido():
    """UNA CIFRA SIN UNIDAD NO ES COMPARABLE NI CONSIGO MISMA.

    El colega detectó la incoherencia: 258 − 36 = 222 y yo reportaba 204.
    Ninguno era «documentos sin trazabilidad» — la métrica contaba **nombres
    únicos** (18 se repiten en varias carpetas) y no lo decía.

    Y el universo incluía `desktop.ini`: ruido de Windows contado como documento
    oficial del GAD, inflando cualquier porcentaje derivado."""
    e = D.evidencia_primaria()
    if e.get("estado") == "no_determinable":
        import pytest
        pytest.skip(e["por_que"])
    assert e["unidad"], "la métrica no declara en qué unidad cuenta"
    assert "nombres" in e["unidad"]
    assert e["nombres_unicos"] <= e["documentos"], (
        "más nombres únicos que documentos: la unidad se rompió")
    assert e["citados_por_artefactos"] + e["no_determinables"] == e["nombres_unicos"], (
        "las partes no suman el total en su propia unidad")
    H = D.raiz_de_evidencia_primaria()
    if H:
        assert not any(f.name.lower() == "desktop.ini"
                       for f in H.rglob("*") if f.is_file()) or e["documentos"] < 258, (
            "volvió a contarse el ruido del sistema de archivos")


def test_los_territorios_no_inspeccionados_se_declaran_sin_veredicto():
    """Supabase y Obsidian son **territorios conocidos y no consultados**. Su
    estado no es «cumple» ni «falla»: es `declarado_no_inspeccionado`, con el
    motivo escrito. Un territorio del que se sabe que existe y no se mira debe
    constar — callarlo es lo que hizo que `corpus_externo/` costara el 23% del
    universo de ADR."""
    e = D.evidencia_primaria()
    if e.get("estado") == "no_determinable":
        import pytest
        pytest.skip(e["por_que"])
    ts = {t["territorio"].split(" ·")[0]: t for t in e["territorios_no_inspeccionados"]}
    assert {"Supabase", "Obsidian"} <= set(ts)
    for t in ts.values():
        assert t["estado"] == "declarado_no_inspeccionado"
        assert t["por_que"], f"territorio sin motivo declarado: {t}"
