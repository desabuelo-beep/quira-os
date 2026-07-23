"""
scripts/cypher/apply_cypher.py — Aplicar scripts Cypher a AuraDB · QUIRA OS
===========================================================================
Dylus Lab © 2026

USO:
    python scripts/cypher/apply_cypher.py scripts/cypher/001_crdc_circuit.cypher
    python scripts/cypher/apply_cypher.py scripts/cypher/001_crdc_circuit.cypher --dry-run

PRERREQUISITO:
    AuraDB debe estar activo (no pausado).
    Reanudar en: https://console.neo4j.io → instancia 8dc8519a → Resume

NOTA:
    Si AuraDB está pausado, el script falla con ServiceUnavailable.
    Reanudar la instancia (gratuito, tarda ~30 segundos) y volver a ejecutar.
"""
from __future__ import annotations

import logging
import pathlib
import re
import sys

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
logger = logging.getLogger(__name__)


def _get_neo4j_creds() -> tuple[str, str, str]:
    """Resuelve credenciales Neo4j desde secrets.toml."""
    import re as _re
    content = pathlib.Path(".streamlit/secrets.toml").read_text(encoding="utf-8")
    block   = _re.search(r"\[neo4j\](.*?)(?=\n\[|\Z)", content, _re.DOTALL).group(1)
    uri  = _re.search(r'uri\s*=\s*"([^"]+)"',      block).group(1)
    user = _re.search(r'user\s*=\s*"([^"]+)"',     block).group(1)
    pw   = _re.search(r'password\s*=\s*"([^"]+)"', block).group(1)
    return uri, user, pw


def _split_statements(cypher_text: str) -> list[str]:
    """
    Divide un script Cypher en statements individuales.
    Separador: punto y coma (;) seguido de nueva línea.
    Ignora comentarios (//) y líneas vacías.
    """
    # Eliminar bloques de comentario
    text = re.sub(r"//[^\n]*", "", cypher_text)
    # Dividir por ;
    raw_statements = text.split(";")
    statements = []
    for s in raw_statements:
        clean = s.strip()
        if clean and len(clean) > 10:
            statements.append(clean)
    return statements


def apply_cypher_file(filepath: str, dry_run: bool = False) -> dict:
    """
    Aplica un archivo Cypher completo a AuraDB.

    Args:
        filepath: Ruta al archivo .cypher
        dry_run:  True = solo parsear y mostrar statements, no ejecutar

    Returns:
        dict con resultado: statements_total, ok, errores, mensajes
    """
    path = pathlib.Path(filepath)
    if not path.exists():
        logger.error(f"Archivo no encontrado: {filepath}")
        return {"ok": 0, "errores": 1, "mensajes": [f"File not found: {filepath}"]}

    cypher_text = path.read_text(encoding="utf-8")
    statements  = _split_statements(cypher_text)

    logger.info(f"Archivo: {path.name} · {len(statements)} statements")

    if dry_run:
        print(f"\n[DRY-RUN] {len(statements)} statements a ejecutar:")
        for i, s in enumerate(statements, 1):
            preview = s[:80].replace("\n", " ")
            print(f"  {i:02d}. {preview}...")
        return {"ok": len(statements), "errores": 0, "dry_run": True}

    # Conectar AuraDB
    try:
        from neo4j import GraphDatabase
        uri, user, pw = _get_neo4j_creds()
        driver = GraphDatabase.driver(uri, auth=(user, pw))
        driver.verify_connectivity()
        logger.info(f"AuraDB conectado: {uri}")
    except Exception as e:
        logger.error(
            f"No se pudo conectar a AuraDB: {e}\n"
            f"  → Reanudar instancia en https://console.neo4j.io\n"
            f"  → Instancia: 8dc8519a → Resume"
        )
        return {"ok": 0, "errores": 1, "mensajes": [str(e)]}

    ok      = 0
    errores = 0
    mensajes= []

    with driver.session() as session:
        for i, stmt in enumerate(statements, 1):
            try:
                result = session.run(stmt)
                summary = result.consume()
                counters = summary.counters
                logger.info(
                    f"  [{i:02d}/{len(statements)}] OK · "
                    f"nodes_created={counters.nodes_created} "
                    f"rels_created={counters.relationships_created} "
                    f"props_set={counters.properties_set}"
                )
                ok += 1
            except Exception as exc:
                errores += 1
                msg = f"[{i:02d}] ERROR: {exc.__class__.__name__}: {str(exc)[:200]}"
                logger.error(msg)
                mensajes.append(msg)

    driver.close()

    logger.info(
        f"\nResultado: {ok} OK · {errores} errores · "
        f"{'EXITOSO' if errores == 0 else 'CON ERRORES'}"
    )
    return {
        "statements_total": len(statements),
        "ok":               ok,
        "errores":          errores,
        "mensajes":         mensajes,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/cypher/apply_cypher.py <archivo.cypher> [--dry-run]")
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run  = "--dry-run" in sys.argv

    result = apply_cypher_file(filepath, dry_run=dry_run)
    sys.exit(0 if result.get("errores", 0) == 0 else 1)
