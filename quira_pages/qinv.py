"""
QUIRA OS — Fábrica de Investigaciones (QINV)
═══════════════════════════════════════════════════════════════════════════════
Registro POLIMÓRFICO de las 13 investigaciones + renderer genérico sobre el kernel
(`InvestigacionQUIRA` · UMI). Una sola fuente, 13 instancias — DRY, escalable.

PASADA 1 (línea de montaje horizontal · mesa 2026-06-21): el ESQUELETO de los 13.
Cada uno carga su **pregunta estratégica REAL** + el **dato real** del motor + el
**lente dual** (GAD territorial / Central sectorial). Las pasadas 2-5 rellenan
evidencia, lectura IA, GeoTwin y consolidación L3.

Polimorfismo: la pregunta estratégica es PERMANENTE; el lente se adapta al sujeto
obligado (Municipio 001 → lente GAD · Ministerio/Secretaría → lente Central).
Deriva del DICCIONARIO + spec dual-lente (Javo · 2026-06-21). NO es un documento.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

# ── PASADA 2 · directrices de contenido (Javo · 2026-06-21) ───────────────────
# QUIRA NO es forense/auditora: descriptiva→preventiva→predictiva→prospectiva.
# d01 "Arquitectura Estratégica del Gobierno": cadena PDOT→POA→PAC→Presupuesto→
#     PresupParticip.→Rendición · avance financiero mensual · (ODS/PND MIGRAN a d02).
# d02 "Arquitectura Financiera del Desarrollo": dinero + Motor de Elegibilidad
#     (CAF·BID·BM·UE·GIZ·PNUD…) + articulación multinivel + ODS/PND. (hoy vacío)
# d03 métrica madre = Fidelidad del Mandato 72.73% (48/66 promesas CNE↔PDOT · NO 94.6).
# d05 Holding: desglose EP Agua/Aseo·Bomberos·Patronato, misma vara del Excel.
# d06 Salud: IED (Eficiencia Directiva) + talento humano + LOSEP + índices sin hogar.
# d07/08/09: SEPARAR de Holding (los 3 tableros ya existen · cantera de Javo).
# d10 Cobertura: NBI territorializadas del diagnóstico PDOT → GeoTwin.
# d12 Inclusión (deuda técnica): índice madre PRIMERO (sub-índices por grupo +
#     COOTAD corriente/inversión + Patronato gasta en personal, no PAC).
# Excel = motor canónico INVISIBLE (no se muestra/exporta/explica · Regla 1 + Firewall).

# ── MATRIZ DE LA FÁBRICA · 13 cajones (consenso 2026-06-21 · "definir antes de construir") ──
# Madre = índice REAL del Canon. Deuda = lo que falta para dejar el Canon EXPEDITO.
# REGLA DURA (Javo): ningún cajón se construye con métrica proxy — el Canon va primero (Regla 1).
# Leyenda deuda: 🟢 listo · 🟠 parcial · 🔴 bloquea construcción (Canon incompleto).
#
#  d01 Planif. Estratégica  madre: Fidelidad de Planificación 69.93% (REAL·tgi.d2) — ✅ CONSTRUIDA
#      hojas: H04·H05(POA ✓)·H05b·H21b · cosecha: p8_metas·p12_cadena·p3_congruencias · deuda: 🟢 ok
#  d02 Presupuesto          madre: devengado/ISP/IED · hojas: H07·H73
#      cosecha: p18_cooperacion · deuda: 🔴 cédula eSIGEF oficial→H07
#  d03 Gobernanza Mandato   madre: IFE-A 72.73% (REAL·48/66) · hojas: H03·H73
#      cosecha: p8_metas·p_concejo · deuda: 🟠 plan CNE/66 promesas (carga oficial)
#  d04 Alertas              madre: SAT activas (REAL) · hojas: H75·H24
#      cosecha: m2_alertas·p9_sat · deuda: 🟢 ok
#  d05 Holding              madre: promedio entidades · hojas: H12d
#      cosecha: p2_holding·m3_municipal · deuda: 🟠 Excel EP/Patronato flojo
#  d06 Salud Institucional  madre: ICPI (REAL·H12) — ya construida · hojas: H12·H73
#      cosecha: p_ejecutivo·p6_pulso·p7_brecha · deuda: 🟢 ok
#  d07 Transparencia        madre: LOTAIP 21/21 (REAL) · hojas: LOTAIP
#      cosecha: p07_transparencia · deuda: 🟢 ok
#  d08 Participación         madre: IGP · hojas: H73
#      cosecha: p16_gobernanza·p16_confianza · deuda: 🟢 base lista (cosechar de Holding)
#  d09 Rendición             madre: estado circuito RDC · hojas: H31(CPCCS)
#      cosecha: p17_rdc · deuda: 🟠 3 mundos (NLP discurso)
#  d10 Cobertura             madre: NBI/cobertura territorial · hojas: H04b·INEC·CAPA_TERR
#      cosecha: p10_territorio·p7_brecha · deuda: 🔴 GPS + NBI territorial (PDOT diag)
#  d11 Desarrollo Económico  madre: — (no existe) · hojas: corpus PDOT
#      cosecha: — · deuda: 🔴 índice madre inexistente (campo verde)
#  d12 Inclusión/Género      madre: PSG/IBSC · hojas: H04b·H73
#      cosecha: p19_genero · deuda: 🔴 GAP subíndices + IBSC datos + COOTAD
#  d13 Sostenibilidad        madre: ICODS (sub-eje) · hojas: corpus biofísico·KB_RIESGOS
#      cosecha: — · deuda: 🔴 ICODS sub-eje + biofísico
#
# SPRINT CANON (previo a pantallas · ingesta al Excel · método: Haiku docs + manual):
#   🔴 POA 2026→H05 · cédula eSIGEF→H07 · IBSC col F→H04b · plan CNE→H03 · GPS→CAPA_TERR.

# ── Registro canónico (clave = dominio interno · id público = QINV-NNN) ─────────
# pregunta = estratégica permanente · gad/central = los dos lentes · page = ya construida
QINV: dict[str, dict] = {
    "d01": {
        "id": "QINV-001", "nombre": "Planificación Estratégica",
        "pregunta": "¿La institución sostiene la correspondencia con sus metas "
                    "plurianuales, o registra desviaciones en su senda de desarrollo?",
        "gad": "Metas plurianuales del PDOT.",
        "central": "Objetivos del PEI alineados al Plan Nacional de Desarrollo.",
        "page": "m_planificacion",  # ✅ construida (evidencia real · Fidelidad de Planificación)
    },
    "d02": {
        "id": "QINV-002", "nombre": "Presupuesto & Financiamiento",
        "pregunta": "¿Con qué eficiencia y oportunidad se ejecutan los recursos "
                    "asignados frente a la rigidez del gasto y el riesgo de subejecución?",
        "gad": "Cédulas de ingreso/gasto · competencias del territorio (eSIGEF local).",
        "central": "Ejecución por programas sectoriales (Presupuesto General del Estado).",
        "page": "m_presupuesto",  # ✅ construida (capacidad financiera territorial · d02)
    },
    "d03": {
        "id": "QINV-003", "nombre": "Gobernanza del Mandato Electoral",
        "pregunta": "¿Existe correspondencia material entre el mandato rector "
                    "originario y la programación operativa real de la entidad?",
        "page": "m_mandato",  # ✅ construida (la palabra empeñada · d03)
        "gad": "Plan de Trabajo inscrito ante el CNE.",
        "central": "Agendas sectoriales · decretos · mandatos del Ejecutivo.",
    },
    "d04": {
        "id": "QINV-004", "nombre": "Alertas Institucionales",
        "pregunta": "¿Qué vectores de riesgo institucional están activos y exigen "
                    "intervención antes de comprometer la continuidad del servicio público?",
        "gad": "Alertas presupuestarias y contractuales del plan anual (PAC local).",
        "central": "Riesgos normativos y de transferencias a gran escala (Contraloría).",
    },
    "d05": {
        "id": "QINV-005", "nombre": "Holding e Integración Municipal",
        "pregunta": "¿Las unidades de la red institucional operan alineadas a la "
                    "estrategia, o registran asimetrías que lastran el rendimiento global?",
        "gad": "Empresas públicas locales (Aseo, Agua), Bomberos y Patronatos.",
        "central": "Coordinaciones Zonales · Direcciones Distritales · adscritas.",
    },
    "d06": {
        "id": "QINV-006", "nombre": "Salud Institucional",
        "pregunta": "¿El aparato institucional tiene la capacidad estructural y "
                    "operativa para sostener el cumplimiento de sus funciones de ley?",
        "gad": "Capacidad operativa instalada del GAD · talento humano local.",
        "central": "Brecha de capacidades · distribución del personal bajo LOSEP.",
        "page": "m1_situacion",  # ✅ ya construida (evidencia real)
    },
    "d07": {
        "id": "QINV-007", "nombre": "Transparencia",
        "pregunta": "¿La información obligatoria cumple los estándares de "
                    "verificabilidad, o hay opacidad estructural que impide el control social?",
        "gad": "Matriz de obligaciones de transparencia (LOTAIP) — universal.",
        "central": "Matriz de obligaciones de transparencia (LOTAIP) — universal.",
    },
    "d08": {
        "id": "QINV-008", "nombre": "Participación Ciudadana",
        "pregunta": "¿Los canales de articulación social ejercen incidencia "
                    "vinculante en la política institucional, o son un proceso meramente formal?",
        "gad": "Sistema de Participación local (asambleas, cabildos, silla vacía).",
        "central": "Consejos consultivos · audiencias públicas · veedurías nacionales.",
        "page": "m_participacion",  # ✅ construida (3 dimensiones · integridad · vitalidad · efectividad)
    },
    "d09": {
        "id": "QINV-009", "nombre": "Rendición de Cuentas",
        "pregunta": "¿La narrativa oficial de rendición coincide con la evidencia "
                    "física y financiera registrada por los sistemas de control del Estado?",
        "gad": "Triangulación: motor físico vs. informe CPCCS vs. discurso (NLP).",
        "central": "Triangulación: motor físico vs. informe CPCCS vs. discurso (NLP).",
        "page": "m_rdc",  # ✅ construida (réplica del molde · Fidelidad Narrativa + Participativo + CPCCS)
    },
    "d10": {
        "id": "QINV-010", "nombre": "Cobertura de Servicios e Infraestructura",
        "pregunta": "¿La distribución de la inversión y los servicios responde a la "
                    "reducción planificada de brechas de cobertura en el territorio?",
        "gad": "Brechas parroquiales (NBI, agua, alcantarillado, vialidad).",
        "central": "Despliegue nacional de infraestructura (salud, educación, conectividad).",
    },
    "d11": {
        "id": "QINV-011", "nombre": "Desarrollo Económico Territorial",
        "pregunta": "¿Qué efectividad registran los programas de la entidad para "
                    "dinamizar la competitividad, la sostenibilidad y el empleo de su sector?",
        "gad": "Dinamización productiva local (ferias, turismo, artesanía).",
        "central": "Competitividad industrial · comercio · encadenamiento (sector regulado).",
    },
    "d12": {
        "id": "QINV-012", "nombre": "Inclusión, Equidad y Género",
        "pregunta": "¿Las asignaciones obligatorias para los grupos de atención "
                    "prioritaria se traducen en un impacto material y medible?",
        "gad": "Porcentaje de ley a grupos prioritarios (matriz parroquial).",
        "central": "Agendas Nacionales para la Igualdad (transversales al servicio).",
    },
    "d13": {
        "id": "QINV-013", "nombre": "Sostenibilidad y Resiliencia Ambiental",
        "pregunta": "¿Las intervenciones institucionales mitigan la vulnerabilidad "
                    "biofísica y garantizan la resiliencia ecológica del entorno operativo?",
        "gad": "Riesgos biofísicos · cuencas · uso del suelo · áreas protegidas.",
        "central": "Descarbonización sectorial · transición energética · mitigación nacional.",
    },
}


def label_of(dom: str) -> str:
    """Nombre de la investigación (para el breadcrumb de retorno)."""
    return QINV.get(dom, {}).get("nombre", "Investigación")


def _placeholder_evidencia(spec: dict) -> None:
    """Evidencia del esqueleto (Pasada 1): el lente dual + aviso de Pasada 2."""
    st.markdown(
        f'<div style="background:rgba(255,255,255,.015);border:1px solid '
        f'rgba(255,255,255,.07);border-radius:12px;padding:14px 16px">'
        f'<div style="font-size:11px;color:#A8B4C8;line-height:1.7">'
        f'<b style="color:#E8EDF4">Lente GAD</b> (territorial): {spec["gad"]}<br>'
        f'<b style="color:#E8EDF4">Lente Central</b> (sectorial): {spec["central"]}'
        f'</div>'
        f'<div style="font-size:11px;color:#5A6B7E;margin-top:12px;'
        f'border-top:1px solid rgba(255,255,255,.06);padding-top:10px">'
        f'▸ Volcado de evidencia del motor — <b>Pasada 2</b> (en construcción).</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render(dom: str) -> None:
    """Renderiza la investigación del dominio `dom` (p.ej. 'd06'). Si ya está
    construida (campo `page`), delega; si no, dibuja el esqueleto (Pasada 1)."""
    spec = QINV.get(dom)
    if not spec:
        st.error(f"Investigación '{dom}' no encontrada en el registro QINV.")
        return

    # Investigación ya construida → delega a su página (evidencia real)
    page = spec.get("page")
    if page:
        try:
            from importlib import import_module
            import_module(f"quira_pages.{page}").render()
            return
        except Exception as e:
            st.caption(f"(evidencia base no disponible: {e})")

    # Esqueleto (Pasada 1): pregunta estratégica + dato real + lente dual + placeholders
    try:
        from quira_pages.p_command_center_v2 import _data, _metric_of, _DOMAINS_V2
        d = _data()
        card = next((x for x in _DOMAINS_V2 if x["id"] == dom), {})
        estado = card.get("estado", "—")
        temp = card.get("temp", "normal")
        metric = _metric_of(card, d) if card else "—"
    except Exception:
        estado, temp, metric = "—", "dim", "—"

    inv = InvestigacionQUIRA(
        id=spec["id"], dominio=dom, nombre=spec["nombre"], version="2026-Q1",
        pregunta=spec["pregunta"], estado=estado, dato=metric, temp=temp,
        evidencia=lambda: _placeholder_evidencia(spec),
        peritaje_headline="",
        peritaje=[],            # Pasada 3 (perito inferencial)
        veredicto_label=spec["nombre"],
        veredicto_pct=None,
        conclusion="",
    )
    inv.to_streamlit()
