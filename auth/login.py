"""
QUIRA OS — Auth entry point
Solo delega al controlador. No contiene lógica ni HTML.
Dylus Lab © 2026
"""
from controllers.auth_controller import run as render_login

__all__ = ["render_login"]
