"""
QUIRA — Gate de consistencia documental  ·  `scripts/ci/check_consistencia.py`

Busca las tres formas en que el canon se desincroniza de la realidad:

 1 · TERMINOLOGÍA RETIRADA que sobrevive en superficies vivas. Un nombre que se
     cambió en un sitio y quedó en otro obliga a explicar dos veces lo mismo, y
     tarde o temprano alguien publica el viejo.
 2 · RUTAS QUE YA NO EXISTEN. Un documento que cita un archivo ausente manda a
     quien lo lea a buscar algo que no está.
 3 · CIFRAS DEL CANON que aparecen mal escritas.

Se revisa lo VIVO: no el histórico, que es registro de lo que se dijo entonces
y debe permanecer como está.

Uso:  python scripts/ci/check_consistencia.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# La consola de Windows abre en cp1252 y este gate imprime flechas y viñetas: sin
# esto reventaba con UnicodeEncodeError DESPUÉS de haber calculado sus resultados
# (2026-08-08). Un gate que muere al informar es un gate que no informa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parents[2]

# Lo que NO se revisa. Todo esto es REGISTRO de trabajo, no canon vivo: deja
# constancia de lo que se dijo o se vio en un momento dado y debe permanecer
# tal cual. Corregirle la terminología sería reescribir la memoria del proyecto.
_EXCLUIR = ("historico", "__pycache__", ".venv", "graphify-out", "worktrees",
            "site-packages", ".claude", "node_modules", ".git",
            ".planning",            # planes de sesiones anteriores
            ".playwright-mcp",      # capturas de páginas — evidencia de entonces
            "docs/superpowers",     # planes de trabajo, no canon
            "docs/audits",          # auditorías fechadas
            "docs/sprint")          # bitácoras de sprint

# (patrón, por qué salió, con qué se reemplaza, bloquea)
#
# `bloquea=False` se reserva para lo que depende de una DECISIÓN que aún no se
# ha tomado. Un gate que falla por algo que nadie resolvió obliga a apagarlo, y
# un gate apagado no vigila nada. Esos casos se informan y no detienen el paso.
# Cada regla lleva un 5º campo `salvo`: el uso en el que el término NO es un
# error, con su motivo escrito. Nació de un falso positivo real (2026-09-02) y
# la lección es la de siempre en este sistema: **se persigue el sentido, no la
# palabra**. Un `None` significa «esta regla no admite excepción», no «nadie lo
# pensó»: la diferencia entre decisión y omisión es justo lo que D-004 cerró.
_RETIRADAS = [
    # Errores verificables: bloquean.
    (r"quiraholding\.streamlit\.app", "el despliegue cambió de subdominio",
     "quiraintelligence.streamlit.app", True, None),
    # ⚠️ EL FALSO POSITIVO QUE ORIGINÓ `salvo`. Este gate llevaba meses sin
    # ejecutarse (D-007) y al correrlo bloqueó por «los otros 221 GAD» en
    # PCD-D07. Pero 222 − Montecristi = 221: la frase es ARITMÉTICAMENTE
    # CORRECTA. Lo que el canon prohíbe es afirmar que el TOTAL es 221, no
    # nombrar el complemento. El patrón medía el número; el error está en el
    # papel que el número ocupa en la frase.
    (r"\b221\s+(?:GAD|municipios|cantones)", "son 222 desde la ley del 8-oct-2024",
     "222", True,
     (r"(?:otros|restantes|dem[áa]s)\s+221",
      "«los otros 221» es el complemento de 222 menos Montecristi, no el total")),
    (r"QUIRA\s+Operations", "NOMENCLATURA_CANONICA prohíbe publicarlo",
     "Operaciones", True, None),

    # ⚠️ «QUIRA Institucional» YA NO SE PERSIGUE, y la razón importa
    # (2026-08-07). El término nombra DOS COSAS y solo una se renombró:
    #   · el AMBIENTE de observación → hoy Centro / Observatorio;
    #   · el PRODUCTO DE GESTIÓN para el GAD (ADR-041 §4-ter) → sigue siendo
    #     «QUIRA Institucional», es un producto de Fase 2 y CONSUME evidencia.
    # Un reemplazo masivo confundió ambos y llegó a escribir que el GAD «opera
    # el Observatorio» y que el Observatorio es a la vez entrada de Fase 1 y
    # consumidor de Fase 2. Cuatro reversiones después, la lección quedó clara:
    # este término no se persigue automáticamente — se decide caso por caso.
    #
    # Y una regla general que salió de ahí: **un ADR sellado no se renombra**.
    # Registra una decisión con el vocabulario de su momento; cambiarle las
    # palabras reescribe la decisión.
    (r"Panel\s+del\s+Observatorio", "se renombró al fijarse ADR-042",
     "Consola de Monitoreo", False, None),
]

_EXT_TEXTO = {".md", ".py", ".yaml", ".yml", ".json", ".toml"}


def _vivos():
    for p in RAIZ.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in _EXT_TEXTO:
            continue
        rel = p.relative_to(RAIZ).as_posix()
        if any(x in rel for x in _EXCLUIR):
            continue
        yield p, rel


def main() -> int:
    retiradas: list[str] = []       # bloquean
    avisos: list[str] = []          # informan
    rutas_rotas: list[str] = []
    revisados = 0

    _RUTA = re.compile(r"`((?:app|scripts|utils|quira_pages|views|models|"
                       r"controllers|docs|governance|data|sentinel|identity|"
                       r"marco_teorico|registry|components)/[\w./-]+\.\w{2,5})`")

    for ruta, rel in _vivos():
        try:
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        revisados += 1

        # El propio gate nombra los términos que persigue.
        if rel == "scripts/ci/check_consistencia.py":
            continue

        lineas = texto.splitlines()
        for patron, motivo, reemplazo, bloquea, salvo in _RETIRADAS:
            for m in re.finditer(patron, texto, re.I):
                n = texto[:m.start()].count("\n")
                # El uso legítimo declarado, si la regla tiene uno. Se comprueba
                # sobre la LÍNEA —no sobre la vecindad— porque «los otros 221»
                # es una propiedad de la frase, no del párrafo.
                if salvo and re.search(salvo[0], lineas[n], re.I):
                    continue
                # Mencionar un término para decir que se retiró NO es usarlo.
                # Se mira la línea y su vecindad: los comentarios que explican
                # un cambio suelen nombrar el término viejo a propósito, y
                # marcarlos obligaría a escribir la historia sin poder nombrar
                # lo que cambió.
                ventana = "\n".join(lineas[max(0, n - 4):n + 5]).lower()
                if any(x in ventana for x in (
                        "retir", "se cambió", "se cambio", "ya no", "decía",
                        "decia", "prohib", "no usar", "legacy", "obsolet",
                        "en vez de", "sustituy", "reemplaz", "renombr", "salió",
                        "salio", "dejó de", "dejo de", "histórico", "historico",
                        "corrigi", "corrigió", "error", "incorrect", "antes",
                        "se llamaba", "pasó a", "paso a")):
                    continue
                destino = retiradas if bloquea else avisos
                destino.append(f"{rel}:{n+1} — «{m.group(0)}» {motivo}; "
                               f"usar «{reemplazo}»")

        for m in _RUTA.finditer(texto):
            citada = m.group(1)
            if not (RAIZ / citada).exists():
                linea = texto[:m.start()].count("\n") + 1
                rutas_rotas.append(f"{rel}:{linea} → `{citada}`")

    print("=" * 70)
    print(f"  CONSISTENCIA DOCUMENTAL · {revisados} archivos vivos")
    print("=" * 70)

    print(f"\n[1/3] Terminología retirada — bloquea  ({len(retiradas)})")
    for h in retiradas[:20]:
        print(f"   >> {h}")
    if len(retiradas) > 20:
        print(f"   … +{len(retiradas)-20} más")
    if not retiradas:
        print("   OK   ninguna superficie viva usa un nombre ya corregido")

    print(f"\n[2/3] Pendiente de decisión — informa  ({len(avisos)})")
    if avisos:
        archivos = sorted({a.split(':')[0] for a in avisos})
        for a in archivos[:12]:
            n = sum(1 for x in avisos if x.startswith(a + ":"))
            print(f"   ·· {a}  ({n})")
        if len(archivos) > 12:
            print(f"   … +{len(archivos)-12} archivos más")
        print("      → el canon aún nombra el producto como antes de ADR-041;")
        print("        propagarlo a los documentos fundacionales lo decide Javo.")
    else:
        print("   OK   nada pendiente")

    print(f"\n[3/3] Rutas citadas que no existen  ({len(rutas_rotas)})")
    for h in rutas_rotas[:16]:
        print(f"   >> {h}")
    if len(rutas_rotas) > 16:
        print(f"   … +{len(rutas_rotas)-16} más")
    if not rutas_rotas:
        print("   OK   toda ruta citada existe en disco")

    print("\n" + "=" * 70)
    # Las rutas rotas informan pero no bloquean: muchas apuntan a artefactos de
    # sprints cerrados, y borrar la cita perdería el registro de qué hubo ahí.
    if retiradas:
        print(f"  {len(retiradas)} INCONSISTENCIA(S) QUE BLOQUEAN")
        print("=" * 70)
        return 1
    print(f"  TODO OK — sin términos corregidos en superficie viva"
          f"  ({len(avisos)} aviso(s), {len(rutas_rotas)} ruta(s) obsoleta(s))")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
