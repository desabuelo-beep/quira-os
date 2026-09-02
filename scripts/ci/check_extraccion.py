# -*- coding: utf-8 -*-
"""
scripts/ci/check_extraccion.py — que ningún documento entre roto al corpus
══════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). El corpus tenía —y al escribir esto **todavía
tiene**— el POA del GAD con el texto destrozado por una conversión a `.docx`:
2,4 caracteres por palabra, 85 % de fragmentos de tres letras o menos sobre
24.000 palabras. De ahí se concluyó que «el POA no ancla al PDOT», y era falso
(OBS-027). El defecto era de la ingesta, no de la fuente.

Nada lo detectó durante meses porque **una extracción rota no falla: devuelve
texto**. Este gate mira lo único que la delata sin conocer el contenido: la
longitud media de palabra. El español ronda 5-7 caracteres; un texto troceado
carácter a carácter se hunde por debajo de 3,5.

QUÉ NO HACE. No juzga si el documento es correcto ni si está completo. Sólo si
lo que se guardó **se puede leer**.

Uso:  python scripts/ci/check_extraccion.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "normativa"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes            # noqa: E402

MUESTRA_POR_DOC = 60

# Tercer código de salida, y no es una convención inventada aquí: es la doctrina
# de los 8 estados aplicada al propio instrumento. Un gate que no pudo mirar no
# está bien ni está mal — está **no determinado**, y el circuito debe verlo.
NO_DETERMINABLE = 2


def main() -> int:
    print("=" * 70)
    print("  GATE DE EXTRACCIÓN — ¿el corpus guarda texto legible?")
    print("=" * 70)

    try:
        import tomllib

        import psycopg2
        raiz = Path(__file__).resolve().parents[2]
        uri = tomllib.load(open(raiz / ".streamlit" / "secrets.toml", "rb")
                           )["database"]["supabase_uri"]
        cn = psycopg2.connect(uri, connect_timeout=15)
    except Exception as e:
        # Sin corpus alcanzable no hay nada que auditar, y **un gate no debe
        # fallar por no poder mirar**: eso confundiría «no pude comprobar» con
        # «está mal», que es justo lo que este gate existe para evitar.
        #
        # ⚠️ PERO DEVOLVÍA 0, Y ÉSE ES EL ERROR SIMÉTRICO (D-007 · 2026-09-02).
        # Al replicar CI en un clon limpio —sin `secrets.toml`, que no se
        # rastrea— este gate imprimía «nada que verificar» y **salía verde**.
        # Enganchado a CI habría acreditado un corpus legible para siempre sin
        # haberlo mirado nunca: exactamente el defecto de D-004, en su forma
        # más pura.
        #
        # La casa ya tenía la respuesta y el gate no se la aplicaba a sí mismo:
        # **8 estados, no bool**. «No existe» ≠ «no pude obtener» ≠ «falló».
        #
        #     0 · verificado, sin hallazgos
        #     1 · verificado, hay hallazgos
        #     2 · NO DETERMINABLE — no se pudo mirar
        #
        # El 2 no bloquea el pipeline, pero tampoco dice que esté bien: obliga a
        # que el circuito lo muestre como lo que es.
        print(f"  [--] corpus no alcanzable ({type(e).__name__}); nada que verificar")
        print("  ESTADO: no_determinable — este gate NO acredita el corpus hoy.")
        print("=" * 70)
        return NO_DETERMINABLE

    cur = cn.cursor()
    cur.execute("""select norma_sigla, count(*) from normativa_corpus
                   group by 1 having count(*) >= 20 order by 2 desc""")
    docs = cur.fetchall()

    rotos: list[tuple[str, int, str]] = []
    sanos = 0
    for sigla, n in docs:
        cur.execute("select contenido from normativa_corpus where norma_sigla=%s "
                    "and contenido is not null limit %s", (sigla, MUESTRA_POR_DOC))
        textos = [r[0] for r in cur.fetchall()]
        inv = Invariantes(sigla)
        inv.texto_legible(textos)
        if inv.rotos:
            rotos.append((sigla, n, inv.rotos[0]["medido"]))
        else:
            sanos += 1

    print(f"  {len(docs)} documentos con ≥20 fragmentos · {sanos} legibles\n")
    if rotos:
        print(f"  {len(rotos)} DOCUMENTO(S) CON TEXTO DESTROZADO:")
        for sigla, n, medido in rotos:
            print(f"    ✗ {sigla:26} {n:6} fragmentos · {medido}")
        print("\n  Reingerir desde el ORIGINAL (.xlsx/.pdf nativo), no desde una")
        print("  conversión. Antes de atribuir una carencia a la fuente, descartar")
        print("  que sea del capturador — ADR-042 §6.")
        print("=" * 70)
        return 1

    print("  TODO OK — ningún documento del corpus quedó ilegible")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
