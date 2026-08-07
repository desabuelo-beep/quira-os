"""
QUIRA — Registro de corridas  ·  `app/observatorio/corrida.py`

Implementa ADR-042 §4, preguntas 2, 3, 5 y 6: qué corrida se ejecutó, qué
evidencia produjo, cómo terminó y **cuánto costó**.

────────────────────────────────────────────────────────────────────────────────
POR QUÉ EL COSTO ES PARTE DE LA TRAZABILIDAD, NO DE LA CONTABILIDAD
────────────────────────────────────────────────────────────────────────────────
El observatorio debe escalar de un municipio a 222 con financiamiento propio.
Una corrida cuyo costo no se conoce no se puede repetir a escala, y **un método
que no se puede repetir no es un método**: es un experimento que salió bien una
vez. Registrar el costo junto al resultado es lo que permite decir «este
procedimiento cuesta X por municipio-mes» antes de comprometerlo con 222.

────────────────────────────────────────────────────────────────────────────────
POR QUÉ SE REGISTRA EL PROCEDIMIENTO Y EL MODELO
────────────────────────────────────────────────────────────────────────────────
Reproducir un resultado exige saber con qué se produjo. Dos corridas del mismo
municipio y el mismo mes pueden diferir porque cambió la fuente —eso es
información— o porque cambió el procedimiento o el modelo —eso es ruido—. Sin
registrar ambos, esa diferencia es indistinguible, y la reproducibilidad que
la portada promete queda sin respaldo.

La primera corrida de 2025 es de CALIBRACIÓN, no de producción (ADR-042 §5-bis):
su fin es medir el comportamiento del procedimiento, no publicar cifras. Por eso
`tipo` distingue ambas, y `es_publicable()` niega la publicación a lo calibrado
mientras el método no esté acreditado.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from app.observatorio.estados import Estado, semantica

#: Dónde se deja el registro cuando no hay base disponible. Un registro local
#: es peor que uno central, pero infinitamente mejor que ninguno: sin él, una
#: corrida que falló no deja rastro de haber existido.
_BITACORA = Path(__file__).resolve().parents[2] / "logs" / "corridas.jsonl"

#: Precio por millón de tokens, en dólares. Se declara aquí para que el cálculo
#: sea inspeccionable — no se consulta a ningún servicio en tiempo de ejecución.
#: Si cambia la tarifa, cambia este número y las corridas viejas conservan la
#: que tenían: por eso se guarda `tarifa_usada` en cada registro.
TARIFAS: dict[str, tuple[float, float]] = {
    # modelo: (entrada, salida)
    "claude-haiku-4-5-20251001": (1.00, 5.00),
    "claude-sonnet-5":           (3.00, 15.00),
    "claude-opus-5":            (15.00, 75.00),
    "local-gguf":                (0.00, 0.00),   # inferencia local — sin costo
}


@dataclass
class Corrida:
    """Una ejecución de captura, con todo lo necesario para repetirla."""

    # ── Qué se corrió ────────────────────────────────────────────────────────
    municipio: str
    fuente: str
    periodo: str                      # «2025» · «2025-03» · «2023-2027»
    procedimiento: str                # p. ej. «captura_dpe_mensual»
    version_procedimiento: str        # cambia cuando cambia el método
    modelo: str = "local-gguf"

    #: `calibracion` mide el procedimiento; `produccion` genera evidencia
    #: publicable. La distinción no es formal: lo calibrado NO se publica.
    tipo: str = "calibracion"

    # ── Cómo fue ─────────────────────────────────────────────────────────────
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    inicio: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    fin: str | None = None
    estado: str = Estado.CAPTURADA.value

    # ── Qué produjo ──────────────────────────────────────────────────────────
    documentos: int = 0
    huellas: list[str] = field(default_factory=list)   # sha256 de lo capturado
    incidencias: list[str] = field(default_factory=list)

    # ── Cuánto costó ─────────────────────────────────────────────────────────
    tokens_entrada: int = 0
    tokens_salida: int = 0
    tarifa_usada: tuple[float, float] | None = None

    # ── Cálculos ─────────────────────────────────────────────────────────────
    def costo_usd(self) -> float:
        """Costo en dólares con la tarifa vigente al registrarse.

        Se guarda la tarifa usada, no solo el total: si mañana cambia el precio,
        una corrida vieja debe seguir diciendo lo que costó entonces."""
        tarifa = self.tarifa_usada or TARIFAS.get(self.modelo, (0.0, 0.0))
        entrada, salida = tarifa
        return round(self.tokens_entrada / 1e6 * entrada +
                     self.tokens_salida / 1e6 * salida, 6)

    def duracion_s(self) -> float | None:
        if not self.fin:
            return None
        t0 = datetime.fromisoformat(self.inicio)
        t1 = datetime.fromisoformat(self.fin)
        return round((t1 - t0).total_seconds(), 2)

    def es_publicable(self) -> bool:
        """Una corrida de CALIBRACIÓN nunca publica, aunque su estado lo permita.

        Es la aplicación de ADR-042 §5-bis: el fin de la primera corrida es
        demostrar que el procedimiento funciona. Publicar sus cifras sería dar
        por bueno un método que todavía se estaba probando."""
        if self.tipo != "produccion":
            return False
        return semantica(self.estado).publicable

    # ── Cierre ───────────────────────────────────────────────────────────────
    def cerrar(self, estado: Estado | str, *, documentos: int | None = None,
               incidencia: str | None = None) -> "Corrida":
        """Marca el final y deja el registro escrito."""
        self.fin = datetime.now(timezone.utc).isoformat()
        self.estado = Estado(estado).value if not isinstance(estado, str) else estado
        if documentos is not None:
            self.documentos = documentos
        if incidencia:
            self.incidencias.append(incidencia)
        if self.tarifa_usada is None:
            self.tarifa_usada = TARIFAS.get(self.modelo, (0.0, 0.0))
        registrar(self)
        return self

    def resumen(self) -> dict:
        d = asdict(self)
        d["costo_usd"] = self.costo_usd()
        d["duracion_s"] = self.duracion_s()
        d["publicable"] = self.es_publicable()
        return d


def registrar(corrida: Corrida) -> bool:
    """Deja constancia de la corrida. Devuelve si pudo escribirse.

    No levanta: una corrida que terminó bien no debe fallar porque su registro
    no se pudo escribir. Pero tampoco calla — devuelve `False` y quien llama
    decide, en lugar de creer que quedó anotada."""
    try:
        _BITACORA.parent.mkdir(parents=True, exist_ok=True)
        with open(_BITACORA, "a", encoding="utf-8") as f:
            f.write(json.dumps(corrida.resumen(), ensure_ascii=False) + "\n")
        return True
    except Exception:  # noqa: BLE001
        import logging
        logging.getLogger(__name__).error(
            "la corrida %s terminó pero NO pudo registrarse: su costo y su "
            "resultado no quedaron anotados", corrida.id)
        return False


def leer(limite: int = 100) -> list[dict]:
    """Últimas corridas registradas, de la más reciente a la más antigua."""
    try:
        lineas = _BITACORA.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    except Exception:  # noqa: BLE001
        return []
    salida = []
    for l in reversed(lineas[-limite:]):
        try:
            salida.append(json.loads(l))
        except json.JSONDecodeError:
            continue
    return salida


def gasto_del_mes(anio: int, mes: int) -> dict:
    """Cuánto se lleva gastado en un mes, y en qué.

    Es la cifra que decide si el barrido puede ampliarse: escalar a 222
    municipios multiplica este número, y conviene saberlo antes."""
    prefijo = f"{anio:04d}-{mes:02d}"
    total, n, por_modelo = 0.0, 0, {}
    for c in leer(limite=100_000):
        if not str(c.get("inicio", "")).startswith(prefijo):
            continue
        n += 1
        costo = float(c.get("costo_usd") or 0)
        total += costo
        m = c.get("modelo", "?")
        por_modelo[m] = round(por_modelo.get(m, 0.0) + costo, 6)
    return {"periodo": prefijo, "corridas": n, "total_usd": round(total, 4),
            "por_modelo": por_modelo,
            "promedio_usd": round(total / n, 6) if n else 0.0}
