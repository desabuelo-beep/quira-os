"""
app/fetchers/adapter_pnud.py — Adaptador PNUD Ecuador · QUIRA OS
=================================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

Patrón: Cooperación multilateral ONU
Naturaleza: No reembolsable
Temas prioritarios: gobernanza, genero, medioambiente, democracia

MODO DEMO:
    Retorna 2 convocatorias representativas del universo PNUD Ecuador.
    Diseñadas para ejercitar el Normalizador sin HTTP.

MODO LIVE:
    URL base: https://www.undp.org/es/ecuador
    Estrategia: fetch página de grants → extraer bloques de convocatoria
    Haiku normaliza el texto de cada bloque.

    TODO (ajustar selectores tras inspeccionar la página):
    - Verificar URL de búsqueda actual de PNUD Ecuador
    - Ajustar selector HTML del listado de oportunidades
    - Validar paginación si hay más de una página
"""
from __future__ import annotations

from datetime import datetime, timedelta

from app.fetchers.base_adapter import BaseAdapter, FondoRaw

PNUD_GRANTS_URL = "https://www.undp.org/es/ecuador/grants-and-funding"
PNUD_BUSQUEDA   = "https://www.undp.org/es/buscar?f%5B0%5D=taxonomy_vocabulary_4%3A6"


class AdapterPNUD(BaseAdapter):
    """Adaptador para PNUD Ecuador — Cooperación multilateral ONU."""

    FUENTE_CODIGO = "PNUD"
    NOMBRE        = "PNUD Ecuador — Programa de las Naciones Unidas para el Desarrollo"
    URL_BASE      = "https://www.undp.org/es/ecuador"

    def _fetch_demo(self) -> list[FondoRaw]:
        """
        2 convocatorias demo representativas del universo PNUD Ecuador.
        Suficientes para ejercitar el pipeline completo.
        """
        ahora = datetime.now()
        cierre_1 = (ahora + timedelta(days=90)).strftime("%d de %B de %Y")
        cierre_2 = (ahora + timedelta(days=45)).strftime("%d de %B de %Y")

        return [
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.undp.org/es/ecuador/gobernanza-local-2026",
                titulo_raw       = "PNUD — Gobernanza Local Democrática Ecuador 2026",
                emisor_raw       = "PNUD",
                monto_raw        = "USD 80.000 hasta USD 500.000",
                fecha_cierre_raw = cierre_1,
                elegibles_raw    = ["GAD", "ONG", "OSC"],
                temas_raw        = ["gobernanza", "democracia", "participacion"],
                texto_fuente     = f"""
PNUD Ecuador — Convocatoria: Gobernanza Local Democrática 2026

El Programa de las Naciones Unidas para el Desarrollo abre convocatoria para
proyectos de fortalecimiento de mecanismos de participación ciudadana y
rendición de cuentas en gobiernos autónomos descentralizados del Ecuador.

MONTO: Entre USD 80.000 y USD 500.000 por proyecto.
CIERRE: {cierre_1}
ELEGIBLES: GADs municipales, organizaciones no gubernamentales, organizaciones
de la sociedad civil con experiencia en gobernanza local.
TEMAS: Gobernanza democrática, participación ciudadana, transparencia,
       rendición de cuentas, fortalecimiento institucional.
DOCUMENTOS REQUERIDOS: Plan Operativo Anual (POA) vigente, Rendición de
Cuentas presentada ante el CPCCS, carta de identidad institucional.
URL: https://www.undp.org/es/ecuador/gobernanza-local-2026
""",
                capturado_en = ahora.isoformat(),
            ),
            FondoRaw(
                fuente_codigo    = self.FUENTE_CODIGO,
                url              = "https://www.undp.org/es/ecuador/mujeres-rurales-2026",
                titulo_raw       = "PNUD/ONU Mujeres — Fondo Mujeres Rurales Ecuador 2026",
                emisor_raw       = "ONU_MUJERES",
                monto_raw        = "USD 30.000 - USD 300.000",
                fecha_cierre_raw = cierre_2,
                elegibles_raw    = ["GAD", "ONG", "OSC"],
                temas_raw        = ["genero", "agua", "participacion"],
                texto_fuente     = f"""
ONU Mujeres Ecuador — Fondo para Mujeres Rurales 2026

Convocatoria conjunta PNUD-ONU Mujeres para proyectos que promuevan el acceso
de mujeres rurales a servicios de agua potable y saneamiento con enfoque de
derechos y género.

MONTO: Desde USD 30.000 hasta USD 300.000 por proyecto.
PLAZO: Cierre de propuestas el {cierre_2}.
ELEGIBLES: GADs cantonales y parroquiales, ONG, organizaciones de mujeres.
REQUISITO CLAVE: Presupuesto Sensible al Género (PSG) mínimo verificable.
                 El municipio debe demostrar al menos 20% de inversión
                 presupuestaria con enfoque de género.
TEMAS: Género, agua, saneamiento, participación comunitaria.
URL: https://www.undp.org/es/ecuador/mujeres-rurales-2026
""",
                capturado_en = ahora.isoformat(),
            ),
        ]

    def _fetch_live(self) -> list[FondoRaw]:
        """
        Fetch real contra PNUD Ecuador.

        Estrategia:
        1. GET página de grants de PNUD Ecuador
        2. Extraer bloques de texto por convocatoria
        3. Retornar como FondoRaw (el Normalizador extrae los campos)

        TODO: Ajustar URL y extracción tras inspeccionar la página actual.
        """
        from datetime import datetime as dt
        html = self._http_get(PNUD_GRANTS_URL)
        if not html:
            # Intentar URL alternativa de búsqueda
            html = self._http_get(PNUD_BUSQUEDA)
        if not html:
            self.error_msg = f"No se pudo acceder a {PNUD_GRANTS_URL}"
            return []

        # Enviar HTML completo al normalizador — Haiku extrae las convocatorias
        # Para páginas grandes, el normalizador ya trunca a MAX_INPUT_CHARS
        return [
            FondoRaw(
                fuente_codigo = self.FUENTE_CODIGO,
                url           = PNUD_GRANTS_URL,
                texto_fuente  = html,
                emisor_raw    = "PNUD",
                capturado_en  = dt.now().isoformat(),
            )
        ]
        # TODO: Si la página tiene múltiples convocatorias listadas,
        # extraer cada bloque por separado para mejor precision.
        # Ejemplo con BeautifulSoup:
        #   soup = BeautifulSoup(html, 'html.parser')
        #   items = soup.select('.grant-item, .funding-opportunity, article')
        #   return [FondoRaw(..., texto_fuente=item.get_text()) for item in items]
