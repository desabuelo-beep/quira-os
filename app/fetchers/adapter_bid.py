"""
app/fetchers/adapter_bid.py — Adaptador BID · QUIRA OS
=======================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

Patrón: Financiamiento mixto (reembolsable + no reembolsable)
Naturaleza: mixto (BID ofrece ambas líneas)
Temas prioritarios: infraestructura, agua, gobernanza, finanzas municipales

El BID tiene dos líneas relevantes para GADs ecuatorianos:
    1. Financiamiento reembolsable — créditos municipales (ISP gate)
    2. Donaciones/cooperación técnica — no reembolsable (otros gates)

MODO DEMO:
    2 convocatorias: una reembolsable (ISP gate) y una cooperación técnica.

MODO LIVE:
    URL base: https://www.iadb.org/es
    Estrategia: buscar proyectos abiertos en Ecuador
    TODO: Ajustar tras inspeccionar la búsqueda de proyectos del BID.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from app.fetchers.base_adapter import BaseAdapter, FondoRaw

BID_BUSQUEDA_URL = (
    "https://www.iadb.org/es/busqueda"
    "?keywords=ecuador+municipio&type=proyecto&status=activo"
)
BID_PROYECTOS_URL = "https://www.iadb.org/es/proyectos"


class AdapterBID(BaseAdapter):
    """Adaptador para BID — Banco Interamericano de Desarrollo."""

    FUENTE_CODIGO = "BID"
    NOMBRE        = "BID — Banco Interamericano de Desarrollo"
    URL_BASE      = "https://www.iadb.org/es"

    def _fetch_demo(self) -> list[FondoRaw]:
        """
        2 convocatorias demo BID:
        1. Crédito para agua potable (reembolsable — ISP gate crítico)
        2. Cooperación técnica de gobernanza (no reembolsable)
        """
        ahora     = datetime.now()
        cierre_1  = (ahora + timedelta(days=120)).strftime("%d de %B de %Y")
        cierre_2  = (ahora + timedelta(days=60)).strftime("%d de %B de %Y")

        return [
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.iadb.org/es/proyectos/agua-municipal-ec-2026",
                titulo_raw       = "BID — Financiamiento Municipal Agua y Saneamiento Ecuador 2026",
                emisor_raw       = "BID",
                monto_raw        = "USD 200.000 hasta USD 5.000.000",
                fecha_cierre_raw = cierre_1,
                elegibles_raw    = ["GAD"],
                temas_raw        = ["agua", "infraestructura"],
                texto_fuente     = f"""
BID — Línea de Financiamiento Municipal para Agua Potable y Saneamiento 2026

El Banco Interamericano de Desarrollo pone a disposición de los Gobiernos
Autónomos Descentralizados municipales del Ecuador una línea de crédito
reembolsable para proyectos de agua potable y alcantarillado sanitario.

INSTRUMENTO: Crédito reembolsable (préstamo a 15 años, tasa preferencial BID)
MONTO: Entre USD 200.000 y USD 5.000.000 por proyecto.
ELEGIBLES: Gobiernos Autónomos Descentralizados municipales. Se requiere
           dictamen técnico favorable del Banco del Estado o institución
           calificadora de riesgo municipal.
REQUISITO FINANCIERO: Indicador de Salud Presupuestaria (ISP) mínimo 65%.
                       La entidad debe demostrar capacidad de endeudamiento
                       conforme al COOTAD Art. 340-348.
CIERRE: {cierre_1} (ventanilla abierta por ciclos trimestrales)
TEMAS: Infraestructura de agua, saneamiento, servicios básicos municipales.
URL: https://www.iadb.org/es/proyectos/agua-municipal-ec-2026
""",
                capturado_en = ahora.isoformat(),
            ),
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.iadb.org/es/cooperacion/gobernanza-lac-2026",
                titulo_raw       = "BID Lab — Cooperación Técnica Gobernanza Municipal LAC 2026",
                emisor_raw       = "BID",
                monto_raw        = "USD 50.000 - USD 150.000",
                fecha_cierre_raw = cierre_2,
                elegibles_raw    = ["GAD", "academia", "ONG"],
                temas_raw        = ["gobernanza", "transparencia", "participacion"],
                texto_fuente     = f"""
BID Lab — Convocatoria Cooperación Técnica No Reembolsable
Fortalecimiento de Gobernanza Municipal en América Latina y el Caribe 2026

BID Lab abre convocatoria para proyectos piloto de fortalecimiento
institucional municipal con enfoque en transparencia, participación ciudadana
y uso de datos abiertos para la gestión pública.

INSTRUMENTO: Cooperación técnica no reembolsable.
MONTO: Entre USD 50.000 y USD 150.000 por proyecto piloto.
ELEGIBLES: GADs municipales, universidades, organizaciones de la sociedad civil.
REQUISITOS: Plan Operativo Anual (POA) aprobado y vigente. Portal de
            transparencia operativo (LOTAIP). Acceso a Información Pública
            (ITAM) demostrable.
CIERRE: {cierre_2}
TEMAS: Gobernanza, transparencia, datos abiertos, participación ciudadana.
URL: https://www.iadb.org/es/cooperacion/gobernanza-lac-2026
""",
                capturado_en = ahora.isoformat(),
            ),
        ]

    def _fetch_live(self) -> list[FondoRaw]:
        """
        Fetch real contra BID.

        Estrategia: buscar proyectos activos en Ecuador.
        TODO: Ajustar URL y extracción tras inspeccionar el buscador de BID.
        """
        from datetime import datetime as dt
        html = self._http_get(BID_BUSQUEDA_URL)
        if not html:
            self.error_msg = f"No se pudo acceder a {BID_BUSQUEDA_URL}"
            return []

        return [
            FondoRaw(
                fuente_codigo = self.FUENTE_CODIGO,
                url           = BID_BUSQUEDA_URL,
                texto_fuente  = html,
                emisor_raw    = "BID",
                capturado_en  = dt.now().isoformat(),
            )
        ]
        # TODO: El BID puede tener una API REST para proyectos.
        # Revisar: https://www.iadb.org/es/about-us/iadb-api
        # Si existe, usar _http_get_json() en vez de scraping HTML.
