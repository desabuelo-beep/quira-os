# -*- coding: utf-8 -*-
"""
scripts/cantera/ocr_harness.py — banco de pruebas OCR · sin motores, sin canon
═══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE, y por qué se escribe ANTES de instalar nada (colega · 2026-08-18):

> *«Construiría primero el benchmark harness aislado para los 123 documentos, sin
> instalar todavía los candidatos.»*

Si el banco se escribe después de elegir el motor, mide lo que ese motor hace bien.
Escribirlo antes obliga a declarar qué necesita QUIRA **con independencia de quién
pueda dárselo** — y deja el listón puesto para todos por igual.

DÓNDE VIVE Y POR QUÉ. En `scripts/cantera/`, fuera de `app/agents/`. Este módulo
**no importa nada del canon**: ni CNO, ni RO, ni catálogo, ni Gold Master. La
frontera de propiedad de ADR-050 empieza aquí, en el import.

    ⚠️ Si algún día este archivo necesita importar `reglas.py` o el Gold Master,
    algo se rompió: significaría que un motor de terceros está a un paso de ver
    el criterio normativo.

EL CONTRATO POBRE (registro de cantera · frontera de propiedad). Un motor recibe
un archivo y devuelve texto, geometría y confianza. **Nunca** recibe CNO, RO,
ponderaciones ni criterios de cumplimiento. Cambiar de motor mañana no mueve esa
línea: por eso `MotorOCR` es una interfaz mínima y no una clase que sepa de QUIRA.

QUÉ MIDE, y por qué siete cosas y no «accuracy». La pregunta de QUIRA no es cuál
lee mejor, sino cuál entrega materia prima que este sistema pueda **custodiar y
verificar**:

    1 texto            cuánto recupera
    2 orden            ¿mantiene el orden lógico de lectura?
    3 geometría        ¿devuelve coordenadas utilizables?
    4 estructura       tablas, columnas, encabezados, regiones
    5 confianza        ¿entrega puntajes calibrables o sólo texto?
    6 reproducibilidad mismo documento → mismo resultado
    7 trazabilidad     ¿puede reconstruirse cómo se produjo cada salida?

La séptima es la que ningún benchmark de OCR mide y a QUIRA le importa más: un
resultado que no puede reconstruirse no es evidencia, es una afirmación.

QUÉ NO HACE: no instala motores, no descarga modelos, no decide grados de cantera
y no toca los documentos originales. Prepara la muestra, define el contrato y
puntúa lo que cada candidato entregue.

Uso:  python scripts/cantera/ocr_harness.py --preparar-muestra
      python scripts/cantera/ocr_harness.py --listar-motores
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Protocol

RAIZ = Path(__file__).resolve().parents[2]
MUESTRA = RAIZ / "data" / "cantera" / "ocr_muestra"
RESULTADOS = RAIZ / "data" / "cantera" / "ocr_benchmark.json"
_ENLACES = RAIZ / "data" / "lotaip" / "enlaces.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ── El contrato pobre ───────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Region:
    """Una región reconocida. `bbox` en píxeles (x0, y0, x1, y1) sobre la página."""
    texto: str
    bbox: tuple[int, int, int, int] | None = None
    confianza: float | None = None
    tipo: str | None = None          # texto · tabla · titulo · figura, si el motor lo dice
    orden: int | None = None         # posición en el orden de lectura, si lo entrega


@dataclass
class SalidaOCR:
    """Lo ÚNICO que un motor externo devuelve a QUIRA.

    Nótese lo que NO contiene: ninguna interpretación, ninguna clase de acto,
    ninguna calificación. El motor dice qué pudo leer; qué significa lo decide el
    canon, mucho más adelante y en otro módulo."""
    paginas: int = 0
    regiones: list[Region] = field(default_factory=list)
    texto_plano: str = ""
    # Trazabilidad del instrumento — la séptima dimensión.
    motor: str = ""
    version_motor: str = ""
    modelo: str = ""
    version_modelo: str = ""
    configuracion: dict = field(default_factory=dict)
    segundos: float = 0.0
    error: str | None = None


class MotorOCR(Protocol):
    """Interfaz mínima que debe cumplir cualquier candidato.

    Deliberadamente pobre: recibe una ruta a un archivo y devuelve `SalidaOCR`.
    Un motor que necesitara más contexto para funcionar estaría pidiendo cruzar la
    frontera, y eso basta para descartarlo."""

    nombre: str

    def identificarse(self) -> dict:
        """Motor, versión, modelo y licencia declarada. Sin esto no hay trazabilidad."""
        ...

    def leer(self, archivo: Path) -> SalidaOCR:
        ...


# ── Muestra · pendiente de inventario visual ────────────────────────────────────
# ⚠️ CORRECCIÓN (2026-08-18). Aquí había una lista de perfiles —tablas, firmas,
# sellos, multipágina— descrita como «los 123 escaneos del numeral 17 son registros
# de asistencia». Javo abrió los archivos: son FOTOGRAFÍAS, todas nítidas, sin
# estructura documental alguna.
#
# El error fue tomar el nombre del campo normativo por descripción del contenido: la
# guía llama al enlace «registro de asistencia» y se dedujo qué habría dentro sin
# abrir un archivo. Es el mismo error que este proyecto lleva días corrigiendo.
#
# Por eso ya NO hay lista de perfiles predefinida. Las categorías salen del corpus,
# no del catálogo de dificultades que un OCR suele encontrar. Inventarlas antes de
# mirar produce una muestra que parece rigurosa y mide otra cosa.
PERFILES: list[tuple[str, str]] = []


def preparar_muestra(limite: int = 20) -> dict:
    """Selecciona candidatos de los escaneos ya verificados y fija su SHA.

    NO descarga: usa lo que la captura de enlaces ya identificó. Y no clasifica por
    perfil automáticamente —eso exige mirar el documento—: deja la ficha lista para
    que una persona la complete. Etiquetar a ciegas produciría una muestra que
    parece representativa sin serlo."""
    if not _ENLACES.exists():
        return {"error": "no hay verificación de enlaces; ejecute la captura primero"}
    enlaces = json.loads(_ENLACES.read_text(encoding="utf-8"))["enlaces"]
    img = [e for e in enlaces
           if str(e.get("tipo_documento", "")).startswith("image/")
           and e.get("estado") == "accesible"]

    MUESTRA.mkdir(parents=True, exist_ok=True)
    ficha = {
        "_meta": {
            "universo": len(img),
            "seleccionados": min(limite, len(img)),
            "origen": "numeral 17 · imágenes enlazadas desde el conjunto de datos",
            "estado": "PRELIMINAR · no representativa",
            "advertencia": "los primeros 20 revisados resultaron ser fotografías nítidas "
                           "sin estructura documental. NO usar como muestra de benchmark "
                           "hasta completar el inventario visual del corpus.",
            "regla": "las categorías salen del corpus observado, no de un catálogo previo "
                     "de dificultades de OCR",
        },
        "documentos": [
            {"url": e["url"], "tipo": e.get("tipo_documento"),
             "referencias": e.get("referencias"),
             "categoria_observada": None, "notas": None}
            for e in img[:limite]
        ],
    }
    (MUESTRA / "ficha_muestra.json").write_text(
        json.dumps(ficha, ensure_ascii=False, indent=1), encoding="utf-8")
    return ficha


# ── Medición ────────────────────────────────────────────────────────────────────
def evaluar(motor: MotorOCR, archivos: list[Path],
            repeticiones: int = 2) -> dict:
    """Corre un motor sobre la muestra y puntúa las siete dimensiones.

    `repeticiones` sirve a la sexta: un motor que devuelve resultados distintos
    para el mismo archivo no es utilizable como fuente de evidencia, por bueno que
    sea su reconocimiento."""
    ident = motor.identificarse()
    filas, huellas = [], {}
    for a in archivos:
        sha = hashlib.sha256(a.read_bytes()).hexdigest()
        salidas = []
        for _ in range(max(1, repeticiones)):
            t0 = time.perf_counter()
            try:
                s = motor.leer(a)
                s.segundos = round(time.perf_counter() - t0, 3)
            except Exception as e:                       # noqa: BLE001
                s = SalidaOCR(error=f"{type(e).__name__}: {e}",
                              segundos=round(time.perf_counter() - t0, 3))
            salidas.append(s)

        base = salidas[0]
        # 6 · reproducibilidad: el texto de todas las pasadas debe coincidir.
        estable = len({hashlib.sha256(s.texto_plano.encode()).hexdigest()
                       for s in salidas}) == 1
        con_bbox = sum(1 for r in base.regiones if r.bbox)
        con_conf = [r.confianza for r in base.regiones if r.confianza is not None]
        filas.append({
            "archivo": a.name,
            "sha256_documento": sha,
            "error": base.error,
            "1_texto": {"caracteres": len(base.texto_plano.strip()),
                        "regiones": len(base.regiones)},
            "2_orden": {"declarado": any(r.orden is not None for r in base.regiones)},
            "3_geometria": {"regiones_con_bbox": con_bbox,
                            "cobertura": round(con_bbox / len(base.regiones), 3)
                            if base.regiones else 0.0},
            "4_estructura": {"tipos": sorted({r.tipo for r in base.regiones if r.tipo})},
            "5_confianza": {"regiones_con_score": len(con_conf),
                            "media": round(sum(con_conf) / len(con_conf), 3)
                            if con_conf else None},
            "6_reproducibilidad": {"estable": estable, "pasadas": len(salidas)},
            "7_trazabilidad": {"motor": base.motor, "version": base.version_motor,
                               "modelo": base.modelo,
                               "version_modelo": base.version_modelo,
                               "configuracion": base.configuracion},
            "segundos": base.segundos,
        })
        huellas[a.name] = sha

    ok = [f for f in filas if not f["error"]]
    return {
        "motor": ident,
        "documentos": len(filas),
        "leidos": len(ok),
        "resumen": {
            "caracteres_medios": round(sum(f["1_texto"]["caracteres"] for f in ok)
                                       / len(ok), 1) if ok else 0,
            "entrega_bbox": sum(1 for f in ok if f["3_geometria"]["regiones_con_bbox"]),
            "entrega_confianza": sum(1 for f in ok if f["5_confianza"]["regiones_con_score"]),
            "declara_orden": sum(1 for f in ok if f["2_orden"]["declarado"]),
            "reproducibles": sum(1 for f in ok if f["6_reproducibilidad"]["estable"]),
            "segundos_medios": round(sum(f["segundos"] for f in ok) / len(ok), 3)
            if ok else 0,
        },
        "detalle": filas,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preparar-muestra", action="store_true")
    ap.add_argument("--limite", type=int, default=20)
    ap.add_argument("--listar-motores", action="store_true")
    args = ap.parse_args()

    if args.listar_motores:
        print("MOTORES REGISTRADOS EN EL BANCO\n")
        print("   (ninguno)\n")
        print("   Es lo correcto: ADR-050 §4 manda cadena de derechos y prueba contra")
        print("   caso real ANTES de incorporar. El banco existe para que ningún motor")
        print("   entre sin pasar por él — incluido el que parezca obvio.\n")
        print("   Un candidato se registra implementando `MotorOCR`, que sólo pide:")
        print("      identificarse() → motor · versión · modelo · licencia")
        print("      leer(archivo)   → SalidaOCR")
        print("   Si un motor necesita más contexto que un archivo para funcionar,")
        print("   está pidiendo cruzar la frontera de propiedad: se descarta.")
        return

    if args.preparar_muestra:
        f = preparar_muestra(args.limite)
        if "error" in f:
            print(f"[XX] {f['error']}")
            sys.exit(2)
        m = f["_meta"]
        print(f"MUESTRA · {m['seleccionados']} de {m['universo']} escaneos disponibles\n")
        print(f"   origen: {m['origen']}")
        print(f"   → {(MUESTRA / 'ficha_muestra.json').relative_to(RAIZ)}\n")
        print("   PERFILES a cubrir (los asigna una persona, mirando el documento):")
        for p, d in PERFILES:
            print(f"      {p:14} {d}")
        print("\n   La muestra no está lista hasta que cada documento tenga perfil.")
        print("   Una muestra sin clasificar mide comodidad del motor, no capacidad.")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
