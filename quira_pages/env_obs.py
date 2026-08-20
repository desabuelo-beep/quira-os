"""
QUIRA — Ambiente OBSERVATORIO  ·  `quira_pages/env_obs.py`

El Observatorio de Integridad Territorial: el instrumento con el que se observa
la gestión pública de forma progresiva y verificable. Es el PRODUCTO PRINCIPAL
(ADR-041 §5.1), no una herramienta interna.

────────────────────────────────────────────────────────────────────────────────
NO ES OPERACIONES — la distinción es de Javo (2026-08-06) y corrige al director
────────────────────────────────────────────────────────────────────────────────
El director había alojado este panel dentro del ambiente de Operaciones
razonando que evitaba duplicar (Regla 7). Estaba mal: no son el mismo concepto
con dos nombres, son dos cosas distintas.

  · OPERACIONES (`env_ops.py`) → mantenimiento TÉCNICO del sistema. Lo hace
    Dylus Lab cuando algo se rompe: cargas, conectores, cache, versiones.
  · OBSERVATORIO (este archivo) → instrumento de ADMINISTRACIÓN PÚBLICA y
    desarrollo. Sus interlocutores son entidades del sector público, organismos
    multilaterales y agencias de cooperación. Lo que se ve aquí se enseña.

Alojar el segundo dentro del primero lo degradaba de producto a herramienta de
soporte, y contradecía al propio ADR-041, que lo nombra el producto principal.

────────────────────────────────────────────────────────────────────────────────
LA VÍA — portal de transparencia de la Defensoría del Pueblo
────────────────────────────────────────────────────────────────────────────────
Bajo LOTAIP la obligación de publicar es del GAD y la Defensoría registra el
cumplimiento mes a mes. El Observatorio lee ese registro: no requiere que ningún
municipio entregue nada ni que medie acuerdo. De ahí sale la cobertura
progresiva de los 222 sin tener toda su información — y el identificador que
devuelve el portal es la llave para cruzar después con los demás sistemas.

La secuencia es progresiva por diseño (Javo): se valida el cantón piloto —2025
completo y lo que va de 2026— antes de ampliar el barrido.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo


def _tab_estado() -> None:
    """Monitoreo de Fuentes — la consola desde la que se despacha la captura."""
    try:
        from quira_pages.p_monitoreo_fuentes import render as _consola
        _consola()
    except Exception as e:  # noqa: BLE001
        st.error(f"Monitoreo de Fuentes no disponible: {e}")


def _panel_adquisicion() -> None:
    """Qué puede recolectar el sistema por sí mismo, y qué le falta.

    POR QUÉ ESTÁ AQUÍ (2026-08-19). Hasta hoy la recolección de evidencia era un
    conjunto de programas que **alguien** ejecutaba desde una terminal: existían
    en el repositorio, pero no en el sistema. Desde la aplicación no había forma
    de saber si la evidencia estaba al día ni de actualizarla.

    Este panel dice, sin intermediarios, qué está vigente y qué se rehará. Si
    algo falta, la verificación no lo pide: lo produce."""
    try:
        from app.agents.d07 import etapas as E
        estado = E.estado_evidencia()
    except Exception:                                   # noqa: BLE001
        return

    pend = [k for k, v in estado.items() if not v["al_dia"]]
    resumen = ("evidencia al día" if not pend else
               f"{len(pend)} de {len(estado)} tareas de recolección por rehacer")

    with st.expander(f"Recolección de evidencia — {resumen}", expanded=bool(pend)):
        st.markdown(
            f'<div style="font-size:11px;color:{C.V_TX2};line-height:1.6;'
            f'margin-bottom:8px">El sistema consulta la fuente oficial, descarga '
            f'lo publicado y lo examina <b>por su cuenta</b>. Cada tarea se '
            f'rehace cuando vence su plazo o cuando cambia aquello de lo que '
            f'depende; si el resultado vuelve a ser el mismo, no se rehace lo '
            f'que venía después.</div>', unsafe_allow_html=True)

        # El grado de apropiación se muestra junto al estado porque son dos
        # hechos distintos: una tarea puede estar al día y aun así no haberse
        # demostrado nunca que el sistema la reproduce por sí mismo.
        try:
            grados = E.autonomia()
        except Exception:                               # noqa: BLE001
            grados = {}
        _ETIQUETA = {"validado": ("Reproducible", "#22C55E"),
                     "ejecucion": ("El sistema la ejecuta", "#38BDF8"),
                     "capacidad": ("Sin ejecución registrada", "#94A3B8"),
                     "ausente": ("No disponible", "#EF4444")}

        for _id, v in estado.items():
            color = "#22C55E" if v["al_dia"] else "#F59E0B"
            if not v["script_disponible"]:
                color = "#EF4444"
            edad = f'{v["edad_dias"]} días' if v["edad_dias"] is not None else "nunca"
            g = grados.get(_id, {}).get("grado", "capacidad")
            txt_g, col_g = _ETIQUETA.get(g, _ETIQUETA["capacidad"])
            st.markdown(
                f'<div style="font-size:11px;color:{C.V_TX2};margin:3px 0;'
                f'line-height:1.6"><span style="color:{color}">●</span>  '
                f'<b>{v["descripcion"][0].upper() + v["descripcion"][1:]}</b>'
                f' <span style="opacity:.65">· {edad} · {v["razon"]}</span>'
                f' <span style="color:{col_g};opacity:.9">· {txt_g}</span></div>',
                unsafe_allow_html=True)

        st.markdown(
            f'<div style="font-size:10px;color:{C.V_TX2};margin-top:8px;'
            f'line-height:1.6;opacity:.8"><b>Reproducible</b> significa que se '
            f'borró el resultado y el sistema lo rehízo idéntico por su cuenta. '
            f'Mientras no se haya demostrado, la tarea figura por lo que se '
            f'puede probar, no por lo que se espera de ella.</div>',
            unsafe_allow_html=True)

        # El límite propio, declarado. Para un sistema de observación pública,
        # poder decir «esto todavía no lo sé hacer» vale tanto como producir un
        # resultado: es la misma exigencia que se le aplica al sujeto observado
        # cuando se le pide que declare lo que no publica.
        try:
            from app.agents import apropiacion as A
            r = A.resumir(E.grados())
            if r["limite_declarado"]:
                st.markdown(
                    f'<div style="border-left:2px solid {C.V_BD_FUERTE};'
                    f'padding:6px 10px;margin-top:8px;font-size:11px;'
                    f'color:{C.V_TX2};line-height:1.6">'
                    f'<b>Límite actual del sistema.</b> De {r["total"]} tareas de '
                    f'recolección, <b>{r["operativas"]}</b> se ha demostrado que el '
                    f'sistema las reproduce por sí mismo, y <b>{r["alcance"]}</b>. '
                    f'Las demás funcionan, pero esa demostración todavía no se ha '
                    f'hecho: {", ".join(r["limite_declarado"])}.<br>'
                    f'<span style="opacity:.8">Lo no demostrado puede haber '
                    f'producido resultados correctos durante el desarrollo; esos '
                    f'resultados sirven para construir el sistema, no para '
                    f'sostener una observación.</span></div>',
                    unsafe_allow_html=True)
        except Exception:                               # noqa: BLE001
            pass

        if st.button("↻  Actualizar evidencia desde la fuente",
                     key="obs_refrescar", use_container_width=True,
                     help="Vuelve a consultar el portal oficial y rehace el examen "
                          "completo. Puede tardar varios minutos."):
            with st.spinner("Consultando la fuente oficial y examinando lo publicado…"):
                res = E.preparar_evidencia(forzar=True)
            for r in res:
                (st.success if r.estado == "ejecutada" else
                 st.warning if r.estado == "omitida" else st.error)(
                    f"{r.etapa} — {r.estado} ({r.segundos}s) {r.detalle[:120]}")

        _revision_documental(E)


def _revision_documental(E) -> None:
    """Abrir los documentos, no sólo comprobar que el enlace existe.

    Javo, sobre el monitoreo que sólo miraba si el archivo estaba publicado:

    > *«Sería algarete que QUIRA deje ese análisis tan básico: debe revisar
    > todos los documentos del GAD —Excel, PDF, etc.— de los links para
    > determinar su cumplimiento.»*

    Esta revisión encontró que en 254 documentos del art. 24 no hay una sola
    acta. No corre en cada verificación porque abrir documento por documento
    cuesta horas; corre cuando se la manda desde aquí."""
    import json
    from pathlib import Path

    st.markdown(f'<div style="height:6px"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:11px;font-weight:700;color:{C.V_TX}">'
        f'Revisión documental</div>'
        f'<div style="font-size:11px;color:{C.V_TX2};line-height:1.6;margin:2px 0 6px">'
        f'Abre uno a uno los documentos enlazados y comprueba <b>qué contienen</b>: '
        f'clase de acto, número de referencia y si el texto es legible. Comprobar '
        f'que el enlace responde no acredita que el documento sea el que la norma '
        f'pide.</div>', unsafe_allow_html=True)

    idx = Path(E.RAIZ) / "data" / "lotaip" / "descargas_indice.json"
    if not idx.exists():
        st.caption("Sin evidencia descargada todavía.")
        return
    try:
        nums = sorted({r["numeral"] for r in
                       json.loads(idx.read_text(encoding="utf-8"))["archivos"]
                       if r.get("numeral")})
    except Exception:                                   # noqa: BLE001
        return

    hechos = E.numerales_analizados()
    d1, d2 = st.columns([3, 2])
    with d1:
        elegido = st.selectbox("Materia a revisar", nums, key="obs_num_doc",
                               label_visibility="collapsed")
    with d2:
        lanzar = st.button("Abrir los documentos", key="obs_docs",
                           use_container_width=True)

    slug = E._slug(elegido)
    if slug in hechos:
        st.caption(f"Ya revisado · {hechos[slug].get('generado') or 'sin fecha'}")

    if lanzar:
        with st.spinner(f"Abriendo los documentos de {elegido}…"):
            r = E.analizar_documentos(elegido, forzar=True)
        (st.success if r.estado == "ejecutada" else st.error)(
            f"{r.estado} ({r.segundos}s) {r.detalle[:160]}")


def _tab_monitoreo() -> None:
    """Verificación conjunto por conjunto — se despacha desde aquí.

    Deja de ser un aviso de «en preparación» (2026-08-18): el catálogo ya lleva,
    por cada conjunto de datos, la periodicidad y los campos que la Guía
    Metodológica exige, y el Instructivo aporta la escala. Con la vara completa,
    la verificación se ejecuta sola: **el botón despacha la corrida y el sistema
    hace el resto** — sin asistencia externa y sin consumo de servicios de IA."""
    from datetime import date

    st.markdown(
        f'<div style="font-size:12px;color:{C.V_TX2};line-height:1.7;'
        f'margin-bottom:10px">La verificación se mide contra la <b>periodicidad '
        f'que fija la norma para cada conjunto</b>, no contra un conteo uniforme '
        f'de meses: un conjunto de contenido trimestral tiene cuatro '
        f'oportunidades de cumplir, no doce. Lo que la Guía no declara '
        f'no se evalúa.</div>', unsafe_allow_html=True)

    _panel_adquisicion()

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        anio = st.selectbox("Ejercicio", [2025, 2026], index=1, key="obs_anio")
    with c2:
        tope = st.number_input("Hasta el mes", 1, 12,
                               value=12 if anio == 2025 else min(5, date.today().month),
                               key="obs_tope",
                               help="Un ejercicio en curso se evalúa sólo hasta el "
                                    "último mes vencido: contarlo completo bajaría "
                                    "el resultado por meses que aún no debía publicar.")
    with c3:
        st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
        lanzar = st.button("▶  Ejecutar verificación", type="primary",
                           use_container_width=True, key="obs_run")

    if not lanzar:
        return

    with st.spinner("Verificando la evidencia publicada contra la exigencia normativa…"):
        try:
            from app.agents.d07.orquestador import ejecutar
            corrida = ejecutar(int(anio), list(range(1, int(tope) + 1)), guardar=True)
        except Exception as e:  # noqa: BLE001
            st.error(f"No se pudo completar la verificación: {e}")
            return

    # Los controles previos se muestran SIEMPRE, también cuando pasan: son la
    # prueba de que el resultado se calculó sobre una vara intacta y evidencia
    # íntegra. Un resultado sin sus controles a la vista no es verificable.
    st.caption(f"Corrida `{corrida.run_id}`")

    # Lo que el sistema tuvo que recolectar antes de poder medir. Se declara
    # porque distingue un resultado calculado sobre evidencia recién obtenida de
    # otro calculado sobre lo que ya había en disco.
    if getattr(corrida, "adquisicion", None):
        hechas = [a for a in corrida.adquisicion if a["estado"] == "ejecutada"]
        if hechas:
            st.markdown(
                f'<div style="font-size:11px;color:{C.V_TX2};margin:4px 0 8px">'
                f'Antes de medir, el sistema recolectó evidencia por su cuenta: '
                f'<b>{", ".join(a["etapa"] for a in hechas)}</b> '
                f'({sum(a["segundos"] for a in hechas):.0f} s).</div>',
                unsafe_allow_html=True)

    for g in corrida.gates:
        st.markdown(
            f'<div style="font-size:11px;color:{C.V_TX2};margin:2px 0">'
            f'<span style="color:{"#22C55E" if g.ok else "#EF4444"}">'
            f'{"✓" if g.ok else "✗"}</span>  <b>{g.nombre.title()}</b> — '
            f'{g.detalle}</div>', unsafe_allow_html=True)

    if corrida.estado == "BLOCKED":
        # No se publica un resultado calculado sobre base dudosa: un resultado
        # ausente informa, uno calculado sobre evidencia sobrescrita engaña.
        st.error("Verificación detenida. No se emite resultado porque no puede "
                 "demostrarse la integridad de la evidencia o de la norma aplicada.")
        return

    s = getattr(corrida, "sita", {}) or {}
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Cumplimiento verificado", f"{s.get('SITA', 0) * 100:.0f}%")
    m2.metric("Publicaciones evaluadas", len(corrida.resultados))
    m3.metric("Hallazgos", len(corrida.hallazgos))
    m4.metric("Conjuntos del catálogo", corrida.canon.get("numerales", "—"))

    st.markdown(
        f'<div style="font-size:11px;color:{C.V_TX2};margin:6px 0 12px">'
        f'Completitud y actualización <b>{s.get("CTA", 0) * 100:.0f}%</b> · '
        f'Formato de datos abiertos <b>{s.get("ETA", 0) * 100:.0f}%</b> · '
        f'Registro dentro del plazo <b>{s.get("RP", 0) * 100:.0f}%</b> · '
        f'Calidad de la información <b>{s.get("CI", 0) * 100:.0f}%</b></div>',
        unsafe_allow_html=True)

    if corrida.hallazgos:
        st.markdown(f'<div style="font-size:12px;font-weight:700;color:{C.V_TX}">'
                    f'Hallazgos</div>', unsafe_allow_html=True)
        for h in corrida.hallazgos[:14]:
            if h["tipo"] == "cobertura_material":
                txt = (f'<b>{h["cd"]}</b> · {h["periodo"]} — la información publicada '
                       f'no acredita la dimensión <b>{h["componente"]}</b>, que el '
                       f'catálogo exige para este conjunto.')
            elif h["nivel"] == "sin_publicacion_alguna":
                txt = (f'<b>{h["cd"]}</b> · {h["periodo"]} — sin publicación en '
                       f'ninguno de los {len(h["periodos_exigidos"])} períodos que '
                       f'exige su periodicidad {h["cadencia"]}.')
            elif h["nivel"] == "no_determinable":
                txt = (f'<b>{h["cd"]}</b> · {h["periodo"]} — no evaluable en '
                       f'temporalidad: {h["razon"]}.')
            else:
                txt = (f'<b>{h["cd"]}</b> · {h["periodo"]} — publica en '
                       f'{len(h["periodos_exigidos"]) - len(h["periodos_faltantes"])} '
                       f'de {len(h["periodos_exigidos"])} períodos exigidos '
                       f'({h["cadencia"]}).')
            st.markdown(
                f'<div style="border-left:2px solid {C.V_BD_FUERTE};padding:4px 10px;'
                f'margin:3px 0;font-size:11px;color:{C.V_TX2};line-height:1.6">'
                f'{txt}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:10px;color:{C.V_TX2};margin-top:12px;'
        f'line-height:1.6">Fuente: registro de transparencia de la Defensoría del '
        f'Pueblo. Un hallazgo describe lo que la evidencia permite verificar; '
        f'no constituye una calificación jurídica. La ausencia de un dato se '
        f'registra como tal y nunca se sustituye por una estimación.</div>',
        unsafe_allow_html=True)


def render() -> None:
    """Ambiente Observatorio."""
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
    <span style="line-height:0">{logo("marfil", 26)}</span>
    <div>
      <div style="font-size:14px;font-weight:800;color:{C.V_TX}">
        Observatorio de Integridad Territorial</div>
      <div style="font-size:10px;color:{C.V_TX2}">Monitoreo progresivo de la
        gestión pública territorial · evidencia verificable</div>
    </div>
</div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["◷ Monitoreo de Fuentes",
                      "🗓 Verificación por dominio"])
    with t1:
        _tab_estado()
    with t2:
        _tab_monitoreo()
