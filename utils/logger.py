"""
utils/logger.py — QUIRA OS v0.1
Logging centralizado con rotación de archivos y formato estructurado.

Uso:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Pipeline iniciado")
    logger.warning("SAT-III activa")
    logger.error("Fallo al conectar DPE")

Salida:
  · Consola: nivel INFO+ con formato legible
  · Archivo: logs/quira.log nivel DEBUG+, rotación 5 MB × 5 backups

Dylus Lab © 2026
"""
from __future__ import annotations

import logging
import logging.handlers
import os
from pathlib import Path

# ── Raíz del proyecto ─────────────────────────────────────────────────────────
_ROOT = Path(__file__).parent.parent

# ── Configuración global (se puede sobreescribir desde config.py) ─────────────
_CONSOLE_LEVEL = logging.INFO
_FILE_LEVEL    = logging.DEBUG
_MAX_BYTES     = 5 * 1024 * 1024   # 5 MB por archivo
_BACKUP_COUNT  = 5
_LOG_DIR       = _ROOT / "logs"
_LOG_FILE      = _LOG_DIR / "quira.log"

_FMT_CONSOLE = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_FMT_FILE    = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s"
_DATEFMT     = "%Y-%m-%d %H:%M:%S"

# Tracking de loggers ya inicializados
_INITIALIZED: set[str] = set()

# Flag para suprimir advertencias de permiso (cloud env)
_FILE_HANDLER_FAILED = False


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Retorna un logger QUIRA configurado con handlers de consola y archivo.

    Es idempotente: si el logger ya fue configurado, lo devuelve sin
    añadir handlers duplicados.

    Args:
        name:  Nombre del logger (tipicamente __name__ del módulo).
        level: Nivel de consola: "DEBUG" | "INFO" | "WARNING" | "ERROR".
               Si None, usa el nivel configurado en config.py o INFO.

    Returns:
        logging.Logger configurado.
    """
    global _FILE_HANDLER_FAILED

    # ── Resolver nivel de consola ────────────────────────────────────────────
    if level is None:
        try:
            import config as cfg
            level = getattr(cfg, "LOG_LEVEL", "INFO")
        except ImportError:
            level = "INFO"

    console_level = getattr(logging, str(level).upper(), logging.INFO)

    logger = logging.getLogger(name)

    # Idempotencia: no añadir handlers si ya están configurados
    if name in _INITIALIZED:
        return logger

    logger.setLevel(logging.DEBUG)  # capture everything; handlers filtran

    # ── Handler de consola ───────────────────────────────────────────────────
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
               for h in logger.handlers):
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(logging.Formatter(_FMT_CONSOLE, datefmt=_DATEFMT))
        logger.addHandler(ch)

    # ── Handler de archivo (con rotación) ────────────────────────────────────
    if not _FILE_HANDLER_FAILED and not any(
        isinstance(h, logging.handlers.RotatingFileHandler) for h in logger.handlers
    ):
        try:
            _LOG_DIR.mkdir(parents=True, exist_ok=True)
            fh = logging.handlers.RotatingFileHandler(
                _LOG_FILE,
                maxBytes=_MAX_BYTES,
                backupCount=_BACKUP_COUNT,
                encoding="utf-8",
            )
            fh.setLevel(_FILE_LEVEL)
            fh.setFormatter(logging.Formatter(_FMT_FILE, datefmt=_DATEFMT))
            logger.addHandler(fh)
        except (PermissionError, OSError):
            # Cloud / read-only filesystem — solo consola
            _FILE_HANDLER_FAILED = True

    logger.propagate = False
    _INITIALIZED.add(name)
    return logger


def configure_root(level: str = "WARNING") -> None:
    """Configura el logger raíz para silenciar librerías externas.

    Llamar una vez al inicio de la app (app.py o entry-point CLI).
    """
    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(getattr(logging, level.upper(), logging.WARNING))
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, level.upper(), logging.WARNING))
        ch.setFormatter(logging.Formatter(_FMT_CONSOLE, datefmt=_DATEFMT))
        root.addHandler(ch)
    # Silenciar librerías ruidosas
    for noisy in ("httpx", "httpcore", "urllib3", "requests", "hpack", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
