"""
utils/page_guards.py — QUIRA OS v0.1
Helpers de acceso seguro a st.session_state y componentes de estado vacío estándar.

PROBLEMA CATALOGADO (Auditoría R1):
  26 de 28 páginas usan session_state["key"] (acceso directo) en lugar de
  session_state.get("key"), exponiéndolas a KeyError en recargas parciales.

SOLUCIÓN: Todas las páginas deben importar y usar las funciones de este módulo.
  from utils.page_guards import sget, require_data, empty_notice, data_stale_notice

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st


# ── 1. Acceso seguro a session_state ────────────────────────────────────────────────────────────

def sget(key: str, default=None):
    """Acceso seguro a st.session_state con valor por defecto.

    Reemplaza: st.session_state["key"]
    Con:        sget("key")          → None si no existe
                sget("key", [])     → [] si no existe

    Args:
        key:     Clave de session_state.
        default: Valor devuelto si la clave no existe o es None.

    Returns:
        Valor almacenado en session_state, o default.
    """
    return st.session_state.get(key, default)


def sget_nested(key: str, subkey: str, default=None):
    """Acceso seguro a un dict anidado dentro de session_state.

    Reemplaza: st.session_state["key"]["subkey"]
    Con:        sget_nested("key", "subkey")

    Args:
        key:     Clave de primer nivel en session_state.
        subkey:  Clave dentro del dict almacenado.
        default: Valor devuelto si cualquiera de los dos niveles no existe.

    Returns:
        Valor anidado, o default.
    """
    outer = st.session_state.get(key)
    if outer is None or not isinstance(outer, dict):
        return default
    return outer.get(subkey, default)


def require_data(*keys: str) -> bool:
    """Verifica que todas las claves requeridas existan y no sean None en session_state.

    Útil como guard al inicio de una función de página para saber si los datos
    están disponibles antes de intentar renderizar.

    Args:
        *keys: Claves que deben estar presentes.

    Returns:
        True si todas las claves existen y no son None; False en caso contrario.
    """
    return all(st.session_state.get(k) is not None for k in keys)


def safe_dict_get(d: dict | None, key: str, default=None):
    """Acceso seguro a una clave de un dict que podría ser None.

    Reemplaza: some_dict["key"]
    Con:        safe_dict_get(some_dict, "key")

    Args:
        d:       Dict a inspeccionar (puede ser None).
        key:     Clave a buscar.
        default: Valor devuelto si d es None o key no existe.

    Returns:
        Valor del dict, o default.
    """
    if d is None or not isinstance(d, dict):
        return default
    return d.get(key, default)


# ── 2. Componentes de estado vacío estándar ─────────────────────────────────────────────────────

def empty_notice(
    message: str = "Sin datos disponibles para el período seleccionado.",
    icon: str = "📂",
    hint: str | None = None,
) -> None:
    """Muestra un aviso estándar de estado vacío.

    Uso: cuando la página no tiene datos para renderizar pero no debe colapsar.

    Args:
        message: Mensaje principal a mostrar.
        icon:    Icono visual para el contenedor de información.
        hint:    Texto de ayuda adicional (opcional, aparece como caption).
    """
    st.info(message, icon=icon)
    if hint:
        st.caption(hint)


def data_stale_notice(
    entity: str = "entidad",
    action: str = "Ejecuta una nueva ingesta desde el Panel de Carga Mensual.",
) -> None:
    """Avisa al funcionario que los datos están desactualizados.

    Args:
        entity: Nombre de la entidad o módulo sin datos frescos.
        action: Instrucción de qué hacer para actualizarlos.
    """
    st.warning(
        f"Los datos de **{entity}** no están disponibles o están desactualizados. "
        f"{action}",
        icon="⚠️",
    )


def auth_required_notice() -> None:
    """Avisa al usuario que necesita autenticarse para ver este módulo."""
    st.warning(
        "🔒 Acceso restringido — inicia sesión para continuar.",
        icon="🔐",
    )
    st.stop()


def loading_placeholder(label: str = "Cargando información institucional…") -> None:
    """Muestra un indicador de carga estándar."""
    with st.spinner(label):
        pass  # El caller decide cuándo termina el spinner


# ── 3. Guards de componentes críticos ───────────────────────────────────────────────────────────

def guard_suggestion(suggestion: dict | None, key: str, default="") -> str:
    """Acceso seguro a un campo de un dict de sugerencia (build_resolution_suggestion).

    Reemplaza: suggestion["borrador_resolucion"]
    Con:        guard_suggestion(suggestion, "borrador_resolucion")

    Args:
        suggestion: Dict devuelto por build_resolution_suggestion (puede ser None o incompleto).
        key:        Clave a acceder.
        default:    Valor por defecto si la clave no existe.

    Returns:
        Valor de la clave, o default.
    """
    if not suggestion or not isinstance(suggestion, dict):
        return default
    return suggestion.get(key, default)
