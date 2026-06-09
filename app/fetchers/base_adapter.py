"""
app/fetchers/base_adapter.py — Contrato de Adaptadores · QUIRA OS
==================================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

Define:
    FondoRaw       — Objeto de salida de cada adaptador (contrato inmutable)
    FondoCanonical — Objeto normalizado listo para INSERT en fondos_convocatorias
    BaseAdapter    — Clase abstracta que todo adaptador debe implementar

CONTRATO (Colega v3 — D.2.1):
    Todos los adaptadores devuelven FondoRaw.
    Solo el Normalizador convierte FondoRaw → FondoCanonical.
    Ningún adaptador hace INSERT directo.

BLOOMBERG FIREWALL:
    Los campos de FondoRaw y FondoCanonical son públicos por diseño.
    Ninguno expone ICPI · TGI · Ti · QTMP · H73 · Gold Master.
"""
from __future__ import annotations

import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# ── Timeouts y reintentos ─────────────────────────────────────────────────────
HTTP_TIMEOUT   = 15   # segundos
HTTP_RETRIES   = 2
HTTP_BACKOFF_S = 3.0

# User-Agent neutral
HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; QUIRA-FondosRadar/1.0; "
        "+https://github.com/dylus-lab/quira-os)"
    ),
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
}


# ── Tipos de dato del contrato ────────────────────────────────────────────────

@dataclass
class FondoRaw:
    """
    Salida cruda de un adaptador.
    El Normalizador convierte esto en FondoCanonical.

    Campos opcionales son None si no están disponibles en la fuente.
    Siempre incluir: fuente_codigo, url, texto_fuente.
    """
    fuente_codigo:   str
    url:             str
    texto_fuente:    str
    # ^ Texto libre de la página/API (HTML, JSON, o texto plano).
    # El Normalizador (Haiku) extrae la estructura a partir de aquí.

    # Campos pre-extraídos (opcionales — si la fuente los entrega estructurados)
    titulo_raw:      Optional[str]   = None
    emisor_raw:      Optional[str]   = None
    monto_raw:       Optional[str]   = None     # "USD 200,000 – 500,000"
    fecha_cierre_raw:Optional[str]   = None     # "31 de diciembre de 2026"
    temas_raw:       Optional[list]  = None     # ["gobernanza", "género"]
    elegibles_raw:   Optional[list]  = None     # ["GAD", "ONG"]
    capturado_en:    Optional[str]   = None     # ISO datetime string


@dataclass
class FondoCanonical:
    """
    Objeto normalizado listo para INSERT en fondos_convocatorias.
    Producido exclusivamente por fondos_normalizer.py.

    Campos obligatorios: emisor_codigo, nombre, estado.
    Campos opcionales: el resto (None = no disponible).
    """
    # Obligatorios
    emisor_codigo:   str
    nombre:          str
    estado:          str = "abierta"   # abierta|cerrada|recurrente

    # Financiamiento
    monto_min_usd:   Optional[float] = None
    monto_max_usd:   Optional[float] = None
    moneda:          str              = "USD"

    # Fechas
    fecha_cierre:    Optional[date]  = None
    fecha_inicio:    Optional[date]  = None

    # Clasificación
    elegibles:       list = field(default_factory=list)
    # Valores válidos: GAD | ONG | OSC | academia | empresa | gobierno_central
    temas:           list = field(default_factory=list)
    # Valores válidos: gobernanza | genero | agua | democracia | medioambiente
    #                  infraestructura | participacion | transparencia | otros

    # Descripción
    descripcion:     Optional[str]  = None
    url:             Optional[str]  = None

    # Metadata del Normalizador
    confidence:      float = 0.0
    # Score 0.0–1.0: confianza del Normalizador en la extracción
    # < 0.5 → descartar · 0.5–0.7 → revisar manual · > 0.7 → auto-insertar

    fuente_codigo:   Optional[str]  = None
    raw_snippet:     Optional[str]  = None
    # Primeros 400 chars del texto fuente (para fondos_historial)

    # Errores de validación (poblado por el Validator)
    errores_validacion: list = field(default_factory=list)


# ── Clase base de adaptadores ─────────────────────────────────────────────────

class BaseAdapter(ABC):
    """
    Clase abstracta que todo adaptador debe implementar.

    Contrato:
        fetch(mode='demo')   → list[FondoRaw]
        fetch(mode='live')   → list[FondoRaw]

    Modo 'demo': retorna datos hardcodeados de prueba (sin HTTP).
        Útil para tests y CI.
    Modo 'live': ejecuta el fetch real contra la URL de la fuente.
        Maneja reintentos y errores gracefully — nunca lanza excepciones.
        En caso de error: retorna [] y actualiza self.error_msg.
    """

    # Subclases DEBEN definir estos atributos
    FUENTE_CODIGO: str = ""
    NOMBRE:        str = ""
    URL_BASE:      str = ""

    def __init__(self) -> None:
        self.error_msg:        Optional[str]  = None
        self.duracion_ms:      Optional[int]  = None
        self._session: Optional[requests.Session] = None

    @abstractmethod
    def _fetch_demo(self) -> list[FondoRaw]:
        """Retorna datos de prueba hardcodeados (sin HTTP)."""
        ...

    @abstractmethod
    def _fetch_live(self) -> list[FondoRaw]:
        """Ejecuta el fetch real contra la fuente."""
        ...

    def fetch(self, mode: str = "demo") -> list[FondoRaw]:
        """
        Punto de entrada principal.

        Args:
            mode: 'demo' (sin HTTP) | 'live' (fetch real)

        Returns:
            Lista de FondoRaw. Vacía si error.
        """
        self.error_msg  = None
        t0              = time.time()
        try:
            if mode == "demo":
                result = self._fetch_demo()
            else:
                result = self._fetch_live()
            self.duracion_ms = int((time.time() - t0) * 1000)
            logger.info(
                f"[{self.FUENTE_CODIGO}] fetch({mode}) → "
                f"{len(result)} fondos · {self.duracion_ms}ms"
            )
            return result
        except Exception as exc:
            self.error_msg   = str(exc)
            self.duracion_ms = int((time.time() - t0) * 1000)
            logger.error(f"[{self.FUENTE_CODIGO}] fetch({mode}) error: {exc}")
            return []

    # ── Helpers HTTP ──────────────────────────────────────────────────────────

    def _http_get(self, url: str, params: dict = None) -> Optional[str]:
        """
        GET con reintentos y timeout.
        Retorna HTML/text o None si falla.
        """
        for attempt in range(1, HTTP_RETRIES + 1):
            try:
                resp = requests.get(
                    url,
                    headers=HTTP_HEADERS,
                    params=params,
                    timeout=HTTP_TIMEOUT,
                )
                resp.raise_for_status()
                return resp.text
            except requests.exceptions.Timeout:
                logger.warning(f"[{self.FUENTE_CODIGO}] Timeout GET {url} (intento {attempt})")
            except requests.exceptions.HTTPError as e:
                logger.warning(f"[{self.FUENTE_CODIGO}] HTTP {e.response.status_code} GET {url}")
                break  # No reintentar 4xx
            except requests.exceptions.RequestException as e:
                logger.warning(f"[{self.FUENTE_CODIGO}] Error GET {url}: {e} (intento {attempt})")
            if attempt < HTTP_RETRIES:
                time.sleep(HTTP_BACKOFF_S)
        return None

    def _http_get_json(self, url: str, params: dict = None) -> Optional[dict | list]:
        """GET que espera JSON. Retorna dict/list o None si falla."""
        text = self._http_get(url, params)
        if not text:
            return None
        try:
            import json
            return json.loads(text)
        except Exception as e:
            logger.warning(f"[{self.FUENTE_CODIGO}] JSON parse error: {e}")
            return None
