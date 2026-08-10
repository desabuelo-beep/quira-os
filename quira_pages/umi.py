"""
QUIRA OS — UMI · Unidad Metodológica de Investigación
═══════════════════════════════════════════════════════════════════════════════
El KERNEL del expediente de inteligencia institucional. NO es un componente
visual: es una MÁQUINA METODOLÓGICA datos-primero. El expediente existe como un
objeto puro (independiente de cómo se exponga); el render es solo UNO de sus
métodos de salida.

        InvestigacionQUIRA  (objeto puro · el expediente)
              │
              ├── to_streamlit()   ← la vista web (Variante A · layout 30cac66)
              ├── to_json()        ← Operations · API · versionado
              ├── to_pdf()         ← expediente CAF / Contraloría / CPCCS  (planificado)
              ├── to_html()        ← informe ciudadano                      (planificado)
              └── export_api()     ← consumo entre productos                (planificado)

Las 13 investigaciones (QINV-001 … QINV-013) son INSTANCIAS de esta clase, con
control de versiones histórico (QINV-006 · v2026-07). Operations produce el
expediente; Institucional / Ciudadana / Cooperación lo CONSUMEN. Un solo
expediente, cero duplicación.

Anatomía de 4 momentos forenses (heredada por las 13):
  1. PREGUNTA FORENSE      — el encabezado soberano (reemplaza el título del widget)
  2. EVIDENCIA (50% izq)   — la prueba física del motor (indicadores + vista viva)
  3. PERITAJE QUIRA (50% der) — el dictamen vinculante (causa, no síntoma)
  4. CONCLUSIÓN EJECUTIVA  — el veredicto para actuar en segundos

"QUIRA no visualiza datos: construye expedientes de inteligencia institucional
para la toma de decisiones." — la mesa, 2026-06-21.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

import streamlit as st

from utils.css_tokens import C

# Paleta del kernel de expedientes. Antes era propia —#FF4D4D, #FFB020, #22C55E,
# #00D4FF— y eso la convertía en una SEGUNDA VERDAD visual: el sistema de color
# vive en `utils/css_tokens`, y este módulo renderiza TODOS los expedientes QINV,
# no una pantalla suelta. Hallado curando d06 (2026-08-10).
#
# El cambio de fondo es `verde`. El sistema visual no tiene color de «bien»
# porque QUIRA mide VERIFICABILIDAD, no bondad: decir «verde» sobre un municipio
# es un juicio de valor que este sistema no puede emitir. Se mapea a SIN_SENAL —
# no hay nada que señalar aquí—, que es lo que de verdad significa.
_TEMP: dict[str, str] = {
    "critico": C.CRITICO,
    "alerta":  C.OCRE,
    "normal":  C.ACENTO,
    "verde":   C.SIN_SENAL,   # NO es verde. Es «sin señal que reportar».
    "dim":     C.V_TX3,
}
_IA = C.ACENTO  # el color del perito (QUIRA)


# ═══════════════════════════════════════════════════════════════════════════════
# EL KERNEL — objeto puro del expediente (datos-primero)
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class InvestigacionQUIRA:
    """Un expediente de inteligencia institucional. Objeto puro: el contenido vive
    como DATOS; los métodos `to_*` lo compilan a cada formato. Cada dominio lo
    instancia con su canon (Diccionario + motor) — jamás con datos inventados (Regla 3).

        QINV006 = InvestigacionQUIRA(
            id="QINV-006", dominio="d06", nombre="Salud Institucional",
            version="2026-06",
            pregunta="¿Tiene esta institución capacidad para sostener el gobierno?",
            estado="BAJO UMBRAL", dato="58.6%", temp="critico",
            indicadores={...},                 # datos duros (serializables)
            evidencia=_evidencia_d06,          # vista web viva (solo to_streamlit)
            peritaje_headline="El deterioro es estructural, no coyuntural.",
            peritaje=["El cumplimiento está 11.4 pts bajo el umbral…"],
            veredicto_label="Capacidad institucional", veredicto_pct=59,
            divergencias="4 dimensiones en rojo",
            prioridad="Prioridad 1 · sostenibilidad financiera",
            conclusion="La institución sostiene el gobierno, pero…",
        )
        QINV006.to_streamlit(on_volver=_volver)   # web
        QINV006.to_json()                         # Operations / API
    """
    # — Identidad del expediente —
    id: str                                  # "QINV-006" · número de caso PÚBLICO
    dominio: str                             # "d06" · enlace INTERNO al canon (no UI)
    nombre: str                              # "Salud Institucional"
    version: str = ""                        # "2026-06" · control de versiones histórico

    # — 1 · Pregunta forense —
    pregunta: str = ""
    estado: str = ""
    dato: str = ""
    temp: str = "normal"
    hipotesis: str = ""                       # la hipótesis de la investigación (opcional)

    # — 2 · Evidencia —
    indicadores: dict[str, Any] = field(default_factory=dict)  # datos duros (puros · serializables)
    evidencia: Callable[[], None] | None = None                # vista web viva (charts · solo to_streamlit)

    # — 3 · Peritaje QUIRA (criterio IA · el perito) —
    peritaje_headline: str = ""
    peritaje: Sequence[str] = field(default_factory=list)
    contradicciones: Sequence[str] = field(default_factory=list)  # divergencias (3 mundos · d09)

    # — 4 · Conclusión ejecutiva (veredicto) —
    veredicto_label: str = ""
    veredicto_pct: int | None = None
    divergencias: str = ""
    prioridad: str = ""
    prioridad_temp: str = "critico"
    conclusion: str = ""
    anexos: Sequence[str] = field(default_factory=list)          # links/evidencia adjunta
    # — visuales de síntesis OPCIONALES (graph+text en peritaje/conclusión · Javo 2026-06-23) —
    peritaje_viz: Callable[[], None] | None = None               # síntesis visual del peritaje
    conclusion_viz: Callable[[], None] | None = None             # visual del veredicto
    criterio_ia: str | None = None                               # Cable Interpretación (Haiku · ADR-031 · ADR-030 §4)

    # ── salida WEB (la vista de 30cac66, ahora como método) ──────────────────
    def to_streamlit(self, on_volver: Callable[[], None] | None = None) -> None:
        color = _TEMP.get(self.temp, _IA)
        st.markdown(_css(color), unsafe_allow_html=True)

        if on_volver is not None:
            if st.button("← Volver al Centro de Mando", key=f"umi_volver_{self.dominio}"):
                on_volver()

        st.markdown('<div class="umi-wrap">', unsafe_allow_html=True)

        # 1 · PREGUNTA FORENSE (encabezado soberano)
        badge = f"INVESTIGACIÓN {self.id} · {self.nombre}"
        if self.version:
            badge += f" · v{self.version}"
        hcol, dcol = st.columns([4.6, 1.4])
        with hcol:
            st.markdown(
                f'<div class="umi-badge">{badge}</div>'
                f'<div class="umi-pregunta">{self.pregunta}</div>',
                unsafe_allow_html=True,
            )
        with dcol:
            st.markdown(
                f'<div style="text-align:right;padding-top:4px">'
                f'<div class="umi-dato">{self.dato}</div>'
                f'<div style="margin-top:7px"><span class="umi-estado">● {self.estado}</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<hr class="umi-div">', unsafe_allow_html=True)

        # 2 · EVIDENCIA (70% · el universo de pruebas · ANCHO COMPLETO · protagonista)
        # Regla 20/70/10: la evidencia del Excel/motor JAMÁS se minimiza ni se esconde.
        # QUIRA resume el método validado en Montecristi; no lo reemplaza.
        st.markdown(
            '<div class="umi-sec umi-sec-ev">▎ EVIDENCIA — todo lo que observa el motor</div>',
            unsafe_allow_html=True,
        )
        if self.evidencia is not None:
            self.evidencia()
        else:
            st.markdown(
                '<div style="font-size:11px;color:#5A6B7E">— evidencia pendiente de cosecha —</div>',
                unsafe_allow_html=True,
            )

        # 3 · PERITAJE QUIRA (10% · el dictamen DESPUÉS de toda la evidencia, jamás antes)
        st.markdown('<hr class="umi-div">', unsafe_allow_html=True)
        st.markdown(
            '<div class="umi-sec umi-sec-ia">▎ LECTURA DE QUIRA — interpretación tras analizar la evidencia</div>',
            unsafe_allow_html=True,
        )
        if self.criterio_ia:                                     # Cable de Interpretación (Haiku · ADR-030 §4)
            st.markdown(self.criterio_ia)                        # el criterio dinámico ES la lectura
        elif self.peritaje or self.peritaje_headline:
            _ph = _peritaje_html(self.peritaje_headline, self.peritaje, self.contradicciones)
            if self.peritaje_viz is not None:                    # graph + text (síntesis)
                _vc, _tc = st.columns([1, 1.18], gap="medium")
                with _vc:
                    self.peritaje_viz()
                with _tc:
                    st.markdown(_ph, unsafe_allow_html=True)
            else:
                st.markdown(_ph, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-size:11px;color:#5A6B7E">— lectura en proceso —</div>',
                unsafe_allow_html=True,
            )

        # 4 · CONCLUSIÓN EJECUTIVA (el veredicto para actuar · con visual opcional)
        if self.conclusion_viz is not None:
            _cc1, _cc2 = st.columns([1, 1.18], gap="medium")
            with _cc1:
                self.conclusion_viz()
            with _cc2:
                st.markdown(_conclusion_html(self), unsafe_allow_html=True)
        else:
            st.markdown(_conclusion_html(self), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── salida DATOS (Operations · API · versionado) ─────────────────────────
    def to_json(self) -> dict[str, Any]:
        """El expediente como dato puro — lo que consumen Operations, la API y el
        control de versiones. Excluye la vista viva (callable, no serializable)."""
        return {
            "id": self.id,
            "dominio": self.dominio,
            "nombre": self.nombre,
            "version": self.version,
            "pregunta": self.pregunta,
            "estado": self.estado,
            "dato": self.dato,
            "hipotesis": self.hipotesis,
            "indicadores": dict(self.indicadores),
            "peritaje": {"headline": self.peritaje_headline, "dictamenes": list(self.peritaje)},
            "contradicciones": list(self.contradicciones),
            "veredicto": {
                "label": self.veredicto_label,
                "pct": self.veredicto_pct,
                "divergencias": self.divergencias,
                "prioridad": self.prioridad,
            },
            "conclusion": self.conclusion,
            "anexos": list(self.anexos),
            "tiene_evidencia_viva": self.evidencia is not None,
        }

    # ── salidas PLANIFICADAS (se construyen cuando un consumidor real las pida) ─
    def to_pdf(self) -> bytes:
        raise NotImplementedError(
            "Expediente PDF — planificado (consumidores: CAF · Contraloría · CPCCS). "
            "El dato ya vive en to_json(); falta solo la plantilla de salida."
        )

    def to_html(self) -> str:
        raise NotImplementedError(
            "Informe HTML — planificado (consumidor: ciudadano). Deriva de to_json()."
        )

    def export_api(self) -> dict[str, Any]:
        raise NotImplementedError(
            "Contrato API entre productos — planificado. Hoy usar to_json()."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Render helpers (la vista — subordinada al kernel)
# ═══════════════════════════════════════════════════════════════════════════════
def _peritaje_html(headline: str, dictamenes: Sequence[str], contradicciones: Sequence[str]) -> str:
    head = '<div class="umi-perito-head">◎ QUIRA interpreta</div>'
    lead = f'<div class="umi-dic"><b>{headline}</b></div>' if headline else ""
    cuerpo = "".join(
        f'<div class="umi-dic"><span class="umi-dic-mk">▸</span><span>{d}</span></div>'
        for d in dictamenes
    )
    contra = "".join(
        f'<div class="umi-dic"><span class="umi-dic-mk" style="color:#FF4D4D">⚠</span><span>{c}</span></div>'
        for c in contradicciones
    )
    return f'<div class="umi-perito">{head}{lead}{cuerpo}{contra}</div>'


def _conclusion_html(inv: "InvestigacionQUIRA") -> str:
    color = _TEMP.get(inv.temp, _IA)
    pct = max(0, min(100, int(inv.veredicto_pct))) if inv.veredicto_pct is not None else None
    barra = (
        f'<div class="umi-bar"><div class="umi-bar-fill" style="width:{pct}%;background:{color}"></div></div>'
        if pct is not None else ""
    )
    bigpct = f'<span class="umi-bigpct" style="color:{color}">{pct}%</span>' if pct is not None else ""
    pcolor = _TEMP.get(inv.prioridad_temp, "#FF4D4D")
    div_html = (
        f'<span class="umi-concl-lbl">Señales</span><br>'
        f'<span style="font-size:15px;font-weight:800;color:#E8EDF4">{inv.divergencias}</span>'
        if inv.divergencias else ""
    )
    prio_html = (
        f'<span class="umi-chip" style="background:{pcolor}1f;color:{pcolor};'
        f'border:1px solid {pcolor}55">⚑ {inv.prioridad}</span>'
        if inv.prioridad else ""
    )
    concl_txt = f'<div class="umi-concl-txt">{inv.conclusion}</div>' if inv.conclusion else ""
    return (
        f'<div class="umi-concl">'
        f'<div class="umi-concl-lbl">Conclusión ejecutiva — {inv.veredicto_label}</div>'
        f'<div style="display:flex;align-items:flex-end;gap:18px;margin-top:4px">'
        f'<div style="flex:1">{barra}</div>{bigpct}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'gap:14px;margin-top:10px;flex-wrap:wrap">'
        f'<div>{div_html}</div><div>{prio_html}</div></div>'
        f'{concl_txt}</div>'
    )


def render_investigacion(inv: "InvestigacionQUIRA", on_volver: Callable[[], None] | None = None) -> None:
    """Atajo histórico (30cac66): hoy delega en el método de salida web del expediente."""
    inv.to_streamlit(on_volver=on_volver)


def _css(color: str) -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
.umi-wrap, .umi-wrap * {{ font-family:'Inter',system-ui,sans-serif; }}

/* 1 · Pregunta forense */
.umi-badge {{ font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700;
  letter-spacing:.14em; color:{color}; text-transform:uppercase; }}
.umi-pregunta {{ font-size:27px; font-weight:800; color:#E8EDF4; line-height:1.18;
  margin:4px 0 2px; max-width:62ch; }}
.umi-dato {{ font-family:'JetBrains Mono',monospace; font-size:30px; font-weight:900;
  color:{color}; line-height:1; text-align:right; }}
.umi-estado {{ font-size:9.5px; font-weight:800; letter-spacing:.06em; color:{color};
  border:1px solid {color}55; border-radius:11px; padding:3px 11px; }}

/* secciones evidencia / peritaje */
.umi-sec {{ font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700;
  letter-spacing:.1em; margin:2px 0 8px; }}
.umi-sec-ev {{ color:#8892B0; }}
.umi-sec-ia {{ color:{_IA}; }}

/* peritaje — el dictamen */
.umi-perito {{ background:rgba(0,212,255,.04); border:1px solid rgba(0,212,255,.22);
  border-left:3px solid {_IA}; border-radius:12px; padding:14px 16px; }}
.umi-perito-head {{ font-size:12px; font-weight:800; color:{_IA}; margin-bottom:9px; }}
.umi-dic {{ display:flex; gap:9px; align-items:flex-start; margin-bottom:9px;
  font-size:12.5px; color:#C7D2E0; line-height:1.5; }}
.umi-dic b {{ color:#E8EDF4; }}
.umi-dic-mk {{ color:{_IA}; font-weight:800; flex-shrink:0; }}

/* 4 · conclusión ejecutiva */
.umi-concl {{ background:rgba(255,255,255,.02); border:1px solid rgba(255,255,255,.09);
  border-radius:14px; padding:16px 18px; margin-top:6px; }}
.umi-concl-lbl {{ font-size:10.5px; font-weight:800; letter-spacing:.1em; color:#8892B0;
  text-transform:uppercase; }}
.umi-bar {{ height:13px; background:rgba(255,255,255,.07); border-radius:8px;
  overflow:hidden; margin:7px 0 4px; }}
.umi-bar-fill {{ height:100%; border-radius:8px; }}
.umi-bigpct {{ font-family:'JetBrains Mono',monospace; font-size:34px; font-weight:900;
  line-height:1; }}
.umi-chip {{ display:inline-block; font-size:11px; font-weight:700; border-radius:9px;
  padding:4px 11px; }}
.umi-concl-txt {{ font-size:13px; color:#C7D2E0; line-height:1.55; margin-top:6px; }}
hr.umi-div {{ border:none; border-top:1px solid rgba(255,255,255,.08); margin:10px 0; }}
</style>"""
