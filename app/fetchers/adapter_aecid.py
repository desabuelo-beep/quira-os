"""
app/fetchers/adapter_aecid.py — Adaptador AECID · QUIRA OS
===========================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

Patrón: Cooperación bilateral España-Ecuador
Naturaleza: No reembolsable
Temas prioritarios: gobernanza, genero, agua, participacion, transparencia

AECID es especialmente relevante porque:
    1. Tiene histórico activo en Ecuador (programa bilateral)
    2. Publica convocatorias con criterios de transparencia explícitos
    3. ITAM y PSG son frecuentes en sus convocatorias

MODO DEMO:
    2 convocatorias AECID representativas del programa Ecuador.

MODO LIVE:
    URL base: https://www.aecid.es/es/convocatorias
    Estrategia: listar convocatorias abiertas para Ecuador/LAC
    TODO: Ajustar tras inspeccionar la página actual de AECID.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from app.fetchers.base_adapter import BaseAdapter, FondoRaw

AECID_CONVOCATORIAS_URL = "https://www.aecid.es/es/convocatorias"
AECID_COOPERACION_URL   = (
    "https://www.aecid.es/es/areas-geograficas/america-latina/"
    "programas-y-proyectos?pais=Ecuador"
)


class AdapterAECID(BaseAdapter):
    """Adaptador para AECID — Agencia Española de Cooperación Internacional."""

    FUENTE_CODIGO = "AECID"
    NOMBRE        = "AECID — Agencia Española de Cooperación Internacional para el Desarrollo"
    URL_BASE      = "https://www.aecid.es"

    def _fetch_demo(self) -> list[FondoRaw]:
        """
        2 convocatorias demo AECID:
        1. Gobernanza participativa (POA + IGP gates)
        2. Programa municipal de transparencia (ITAM gate)
        """
        ahora    = datetime.now()
        cierre_1 = (ahora + timedelta(days=75)).strftime("%d de %B de %Y")
        cierre_2 = (ahora + timedelta(days=100)).strftime("%d de %B de %Y")

        return [
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.aecid.es/es/convocatorias/gobernanza-lat-2026",
                titulo_raw       = "AECID — Programa Gobernanza Participativa LAT 2026",
                emisor_raw       = "AECID",
                monto_raw        = "USD 50.000 hasta USD 400.000",
                fecha_cierre_raw = cierre_1,
                elegibles_raw    = ["GAD", "ONG", "academia"],
                temas_raw        = ["gobernanza", "transparencia", "participacion"],
                texto_fuente     = f"""
AECID — Convocatoria: Programa Gobernanza Participativa en América Latina 2026

La Agencia Española de Cooperación Internacional para el Desarrollo (AECID)
abre convocatoria para proyectos de fortalecimiento institucional con énfasis
en participación ciudadana y transparencia en gobiernos locales de Ecuador.

INSTRUMENTO: Subvención no reembolsable.
MONTO: Entre USD 50.000 y USD 400.000 por proyecto.
ELEGIBLES: Gobiernos autónomos descentralizados, ONGs registradas, universidades
           con programas de gobernanza activos.
REQUISITOS OBLIGATORIOS:
    - Plan Operativo Anual (POA) aprobado y vigente
    - Mecanismos de participación ciudadana activos (IGP demostrable >= 25%)
REQUISITOS RECOMENDADOS:
    - Indicador de Transparencia y Acceso a la Información (ITAM) >= 65%
      (no bloqueante pero mejora el scoring de selección)
CIERRE: {cierre_1}
TEMAS: Gobernanza local, participación ciudadana, transparencia,
       rendición de cuentas, fortalecimiento institucional.
URL: https://www.aecid.es/es/convocatorias/gobernanza-lat-2026
""",
                capturado_en = ahora.isoformat(),
            ),
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.aecid.es/es/convocatorias/transparencia-ec-2026",
                titulo_raw       = "AECID — Fondo Municipal de Transparencia Ecuador 2026",
                emisor_raw       = "AECID",
                monto_raw        = "USD 30.000 - 200.000",
                fecha_cierre_raw = cierre_2,
                elegibles_raw    = ["GAD", "OSC"],
                temas_raw        = ["transparencia", "gobernanza", "participacion"],
                texto_fuente     = f"""
AECID Ecuador — Fondo Municipal de Transparencia y Gobierno Abierto 2026

Convocatoria abierta para municipios ecuatorianos que busquen fortalecer sus
sistemas de transparencia, acceso a la información pública y gobierno abierto,
en línea con la Agenda 2030 y los compromisos OGP del Ecuador.

INSTRUMENTO: No reembolsable.
MONTO: Proyectos entre USD 30.000 y USD 200.000.
ELEGIBLES: GADs municipales y parroquiales, organizaciones de sociedad civil.
CRITERIO PRINCIPAL: Transparencia y Acceso a la Información pública demostrable.
                    Se valora positivamente puntuación >= 65% en evaluaciones
                    de acceso a información institucional.
CIERRE: {cierre_2}
TEMAS: Transparencia activa, datos abiertos, gobierno electrónico,
       participación ciudadana digital.
URL: https://www.aecid.es/es/convocatorias/transparencia-ec-2026
""",
                capturado_en = ahora.isoformat(),
            ),
        ]

    def _fetch_live(self) -> list[FondoRaw]:
        """
        Fetch real contra AECID.

        Estrategia: página de convocatorias de AECID.
        TODO: Inspeccionar estructura HTML actual y ajustar.
        """
        from datetime import datetime as dt
        html = self._http_get(AECID_CONVOCATORIAS_URL)
        if not html:
            self.error_msg = f"No se pudo acceder a {AECID_CONVOCATORIAS_URL}"
            return []

        return [
            FondoRaw(
                fuente_codigo = self.FUENTE_CODIGO,
                url           = AECID_CONVOCATORIAS_URL,
                texto_fuente  = html,
                emisor_raw    = "AECID",
                capturado_en  = dt.now().isoformat(),
            )
        ]
        # TODO: AECID tiene filtros por país y tema en su portal.
        # Explorar: https://www.aecid.es/es/convocatorias?pais=Ecuador
        # Para mayor precisión, filtrar solo Ecuador + LAC antes de enviar a Haiku.
