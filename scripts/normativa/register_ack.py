#!/usr/bin/env python3
"""
register_ack.py — ACK Registry Manager
QUIRA Gov · Dylus Lab · 2026-06-01

Gestiona el catálogo maestro de Átomos Canónicos de Conocimiento (ACK).

PRINCIPIO DE ALCANCE NACIONAL:
  Los ACKs representan normativa constitucional y orgánica aplicable a TODOS los
  GADs municipales del Ecuador. El campo canton_id no existe por diseño de
  arquitectura: la normativa es nacional; los datos operacionales (SIGEF, portales
  LOTAIP, ejecución presupuestaria) son cantonales y entran en L0 (Excel Canónico),
  nunca en el ACK Registry.

  Laboratorio:  GADMCM — Cantón Montecristi (validación)
  Destino:      221 municipios del Ecuador (escala)

  El mismo CE_18 aplica a Quito, Guayaquil, Cuenca y Montecristi por igual.
  Lo que cambia canton a canton es: ¿están cumpliendo con CE_18?

Uso:
  python register_ack.py --stats
  python register_ack.py --get CE_18
  python register_ack.py --filter-domain Dom07
  python register_ack.py --filter-circuit C01
  python register_ack.py --filter-fundante
  python register_ack.py --validate-all
  python register_ack.py --link-corpus CE_18   # popula chunk_refs desde normativa_corpus
  python register_ack.py --traverse CE_18      # CE_18 → Dom07 → C01 (recorrido completo)

Bloomberg Model:
  Este módulo es INTERNO. Los ack_ids y circuit_ids NUNCA se exponen en UI pública.
  Solo se exponen los nombres públicos aprobados (p.ej. "Transparencia Activa").
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ── Rutas canónicas ─────────────────────────────────────────────────────────────
REGISTRY_PATH = Path(__file__).parent.parent.parent / "data" / "ack_registry.json"
ADR_PATH = Path(__file__).parent.parent.parent / "docs" / "adr"

VALID_TIPOS = {
    "principio", "competencia_exclusiva", "competencia_concurrente",
    "obligacion", "derecho", "prohibicion", "procedimiento",
    "plazo", "sancion", "distribucion", "definicion",
}
VALID_DOMINIOS = {f"Dom{str(i).zfill(2)}" for i in range(1, 13)}
VALID_JERARQUIA = {0, 1, 2, 3, 4, 5}

# ── Carga y guardado ─────────────────────────────────────────────────────────────


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {
            "meta": {"version": "0.1", "total_acks": 0, "scope": "nacional"},
            "acks": [],
        }
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry: dict[str, Any]) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    registry["meta"]["total_acks"] = len(registry.get("acks", []))
    registry["meta"]["ultima_actualizacion"] = date.today().isoformat()
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"[OK] Registry guardado: {REGISTRY_PATH}")
    print(f"     Total ACKs: {registry['meta']['total_acks']}")


# ── Validación ──────────────────────────────────────────────────────────────────


def validate_ack(ack: dict[str, Any]) -> list[str]:
    """Devuelve lista de errores. Vacía = válido."""
    errors: list[str] = []

    required = [
        "ack_id", "tipo", "nombre", "norma", "dominios", "circuitos",
        "fundante", "vigente", "revisado_por_experto", "chunk_refs", "meta",
    ]
    for field in required:
        if field not in ack:
            errors.append(f"Campo obligatorio ausente: {field}")

    if "tipo" in ack and ack["tipo"] not in VALID_TIPOS:
        errors.append(f"Tipo invalido: '{ack['tipo']}'. Validos: {sorted(VALID_TIPOS)}")

    if "dominios" in ack:
        invalid = [d for d in ack["dominios"] if d not in VALID_DOMINIOS]
        if invalid:
            errors.append(f"Dominios invalidos: {invalid}")

    if "norma" in ack:
        norma = ack["norma"]
        for nf in ["sigla", "articulo", "jerarquia", "vigente"]:
            if nf not in norma:
                errors.append(f"Falta norma.{nf}")
        if "jerarquia" in norma and norma["jerarquia"] not in VALID_JERARQUIA:
            errors.append(f"Jerarquia invalida: {norma['jerarquia']} (valido: 0-5)")

    if "ack_id" in ack:
        parts = ack["ack_id"].split("_")
        if len(parts) < 2:
            errors.append(
                f"ack_id invalido: '{ack['ack_id']}'. Formato: SIGLA_ARTICULO[_INCISO]"
            )

    # Guardrail: canton_id nunca debe existir
    if "canton_id" in ack:
        errors.append(
            "canton_id no permitido en ACK. Los ACKs son nacionales. "
            "Los datos cantonales pertenecen a L0 (Excel Canonico)."
        )

    return errors


# ── Operaciones CRUD ─────────────────────────────────────────────────────────────


def get_ack(registry: dict, ack_id: str) -> dict | None:
    for ack in registry.get("acks", []):
        if ack["ack_id"] == ack_id:
            return ack
    return None


def filter_acks(
    registry: dict,
    *,
    dominio: str | None = None,
    circuito: str | None = None,
    tipo: str | None = None,
    fundante: bool | None = None,
    sigla: str | None = None,
) -> list[dict]:
    results = registry.get("acks", [])
    if dominio:
        results = [a for a in results if dominio in a.get("dominios", [])]
    if circuito:
        results = [a for a in results if circuito in a.get("circuitos", [])]
    if tipo:
        results = [a for a in results if a.get("tipo") == tipo]
    if fundante is not None:
        results = [a for a in results if a.get("fundante") == fundante]
    if sigla:
        results = [a for a in results if a.get("norma", {}).get("sigla") == sigla]
    return results


def add_ack(registry: dict, ack: dict, *, overwrite: bool = False) -> bool:
    errors = validate_ack(ack)
    if errors:
        print("[ERROR] ACK invalido:")
        for e in errors:
            print(f"  - {e}")
        return False

    existing = get_ack(registry, ack["ack_id"])
    if existing and not overwrite:
        print(f"[WARN] ACK {ack['ack_id']} ya existe. Usa --overwrite para reemplazar.")
        return False

    acks = [a for a in registry.get("acks", []) if a["ack_id"] != ack["ack_id"]]
    acks.append(ack)
    acks.sort(key=lambda a: (a["norma"]["sigla"], int(a["norma"]["articulo"].split("_")[0]
                                                       if "_" in a["norma"]["articulo"]
                                                       else a["norma"]["articulo"])))
    registry["acks"] = acks
    return True


# ── Link corpus ──────────────────────────────────────────────────────────────────


def link_corpus(registry: dict, ack_id: str) -> int:
    """
    Busca en normativa_corpus los chunks correspondientes al articulo del ACK
    y actualiza chunk_refs[] con sus SHA256.
    Requiere conexion a Supabase (sentinel.db_config).
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from sentinel.db_config import DbConn
    except ImportError:
        print("[ERROR] sentinel.db_config no disponible. Ejecutar desde quira-os/")
        return 0

    ack = get_ack(registry, ack_id)
    if not ack:
        print(f"[NOT FOUND] ACK {ack_id} no esta en el registry.")
        return 0

    sigla = ack["norma"]["sigla"]
    articulo_str = ack["norma"]["articulo"]

    try:
        articulo_num = int(articulo_str)
    except ValueError:
        print(f"[ERROR] articulo '{articulo_str}' no es un entero. Verifica el ACK.")
        return 0

    db = DbConn()
    conn = db.connect()
    if not conn:
        print("[ERROR] No se pudo conectar a la base de datos.")
        return 0

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sha256, articulo_num, chunk_seq, palabras
            FROM normativa_corpus
            WHERE norma_sigla = %s AND articulo_num = %s
            ORDER BY chunk_seq
            """,
            (sigla, articulo_num),
        )
        rows = cursor.fetchall()
        chunk_refs = [
            {
                "sha256": r[0],
                "articulo_num": r[1],
                "chunk_seq": r[2],
                "palabras": r[3],
            }
            for r in rows
        ]
        ack["chunk_refs"] = chunk_refs
        status = "OK" if chunk_refs else "WARN"
        print(f"[{status}] {len(chunk_refs)} chunks vinculados a {ack_id} ({sigla} Art.{articulo_num})")
        if not chunk_refs:
            print(f"       Verifica que {sigla} este en normativa_corpus (milestone F0.x completado).")
        return len(chunk_refs)
    except Exception as exc:
        print(f"[ERROR] Query fallida: {exc}")
        return 0
    finally:
        cursor.close()


# ── Traverse: recorrido completo ACK → Dominio → Circuito ───────────────────────


def traverse_ack(registry: dict, ack_id: str) -> None:
    """
    Recorre la cadena causal desde un ACK hasta los circuitos en los que participa.
    Este es el recorrido que demuestra que la arquitectura esta viva.

    Primer hito operacional: Portal LOTAIP sin actualizar
      -> ACK: LOTAIP_7 -> Dom07-A -> C01 -> CHS calculable -> Diagnostico
    """
    ack = get_ack(registry, ack_id)
    if not ack:
        print(f"[NOT FOUND] {ack_id}")
        return

    print(f"\n{'='*60}")
    print(f"  RECORRIDO: {ack_id}")
    print(f"{'='*60}")
    print(f"  Norma:    {ack['norma']['sigla']} Art.{ack['norma']['articulo']}")
    print(f"  Tipo:     {ack['tipo']}")
    print(f"  Nombre:   {ack['nombre']}")
    print(f"  Fundante: {'SI' if ack['fundante'] else 'no'}")
    print(f"  Chunks:   {len(ack['chunk_refs'])} en normativa_corpus {'✓' if ack['chunk_refs'] else '(pendiente --link-corpus)'}")

    print(f"\n  Dominios ancla:")
    for dom in ack.get("dominios", []):
        print(f"    -> {dom}")

    print(f"\n  Circuitos constitucionales:")
    circuits = ack.get("circuitos", [])
    if circuits:
        for circ in circuits:
            print(f"    -> {circ} (ver ADR-017)")
    else:
        print(f"    (ninguno — ACK ancla a dominio, no a circuito directamente)")

    relaciones = ack.get("relaciones", [])
    if relaciones:
        print(f"\n  Normas relacionadas:")
        for rel in relaciones:
            print(f"    ~ {rel}")

    if not ack["chunk_refs"] or not circuits:
        print(f"\n  ESTADO: Recorrido incompleto")
        if not ack["chunk_refs"]:
            print(f"    -> chunk_refs vacios: ejecutar --link-corpus {ack_id}")
        if not circuits:
            print(f"    -> Sin circuito: este ACK ancla dominio pero no es nodo de circuito aun")
    else:
        print(f"\n  ESTADO: Recorrido listo para Neo4j")
        print(f"    -> {ack_id} (chunk corpus) -> {ack['dominios']} (DCO) -> {circuits} (Circuito)")

    print(f"{'='*60}\n")


# ── Stats ────────────────────────────────────────────────────────────────────────


def print_stats(registry: dict) -> None:
    acks = registry.get("acks", [])
    meta = registry.get("meta", {})
    print(f"\n{'='*60}")
    print(f"  ACK Registry -- Estadisticas")
    print(f"{'='*60}")
    print(f"  Total ACKs        : {len(acks)}")
    print(f"  Alcance           : {meta.get('scope', 'nacional')} (canton_id prohibido por diseño)")
    print(f"  Laboratorio       : {meta.get('laboratorio', '--')}")
    print(f"  Destino           : {meta.get('destino', '--')}")
    print(f"  Ultima actualiz.  : {meta.get('ultima_actualizacion', '--')}")

    if not acks:
        print(f"\n  (sin ACKs cargados)")
        return

    by_tipo: dict[str, int] = {}
    by_dominio: dict[str, int] = {}
    by_circuito: dict[str, int] = {}
    by_sigla: dict[str, int] = {}
    con_chunks = 0
    revisados = 0
    fundantes = 0
    confianza_alta = 0

    for a in acks:
        by_tipo[a["tipo"]] = by_tipo.get(a["tipo"], 0) + 1
        for d in a.get("dominios", []):
            by_dominio[d] = by_dominio.get(d, 0) + 1
        for c in a.get("circuitos", []):
            by_circuito[c] = by_circuito.get(c, 0) + 1
        sigla = a.get("norma", {}).get("sigla", "?")
        by_sigla[sigla] = by_sigla.get(sigla, 0) + 1
        if a.get("chunk_refs"):
            con_chunks += 1
        if a.get("revisado_por_experto"):
            revisados += 1
        if a.get("fundante"):
            fundantes += 1
        if a.get("meta", {}).get("confianza") == "alta":
            confianza_alta += 1

    print(f"\n  Fundantes         : {fundantes}/{len(acks)}")
    print(f"  Con chunk_refs    : {con_chunks}/{len(acks)} {'OK' if con_chunks == len(acks) else '(pendiente --link-corpus)'}")
    print(f"  Revisados experto : {revisados}/{len(acks)} {'OK' if revisados == len(acks) else '(pendiente revision juridica)'}")
    print(f"  Confianza alta    : {confianza_alta}/{len(acks)}")

    print(f"\n  Por norma:")
    for sigla, count in sorted(by_sigla.items(), key=lambda x: -x[1]):
        print(f"    {sigla:<12} {count}")

    print(f"\n  Por tipo:")
    for tipo, count in sorted(by_tipo.items(), key=lambda x: -x[1]):
        print(f"    {tipo:<30} {count}")

    print(f"\n  Por dominio:")
    for dom, count in sorted(by_dominio.items()):
        print(f"    {dom}   {count}")

    if by_circuito:
        print(f"\n  Por circuito:")
        for circ, count in sorted(by_circuito.items()):
            print(f"    {circ}   {count}")

    print(f"\n  Primer hito operacional pendiente:")
    print(f"    LOTAIP_7 (chunks) -> Dom07-A (DCO) -> C01 (Circuito) -> CHS -> Diagnostico")
    print(f"    Ejecutar: python register_ack.py --link-corpus LOTAIP_7")
    print(f"              python register_ack.py --traverse LOTAIP_7")
    print(f"{'='*60}\n")


# ── CLI ──────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ACK Registry Manager -- QUIRA Gov / Dylus Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python register_ack.py --stats
  python register_ack.py --get CE_18
  python register_ack.py --filter-domain Dom07 --filter-fundante
  python register_ack.py --filter-circuit C01
  python register_ack.py --filter-sigla LOTAIP
  python register_ack.py --link-corpus CE_18
  python register_ack.py --traverse LOTAIP_7
  python register_ack.py --validate-all
        """,
    )
    parser.add_argument("--stats", action="store_true",
                        help="Mostrar estadisticas del registry")
    parser.add_argument("--get", metavar="ACK_ID",
                        help="Obtener ACK por ID (ej: CE_18)")
    parser.add_argument("--filter-domain", metavar="DOM",
                        help="Filtrar por dominio (ej: Dom07)")
    parser.add_argument("--filter-circuit", metavar="CIRC",
                        help="Filtrar por circuito (ej: C01)")
    parser.add_argument("--filter-tipo", metavar="TIPO",
                        help="Filtrar por tipo (ej: obligacion)")
    parser.add_argument("--filter-sigla", metavar="SIGLA",
                        help="Filtrar por sigla de norma (ej: LOTAIP)")
    parser.add_argument("--filter-fundante", action="store_true",
                        help="Solo ACKs fundantes")
    parser.add_argument("--link-corpus", metavar="ACK_ID",
                        help="Vincular chunks de normativa_corpus a un ACK (requiere Supabase)")
    parser.add_argument("--traverse", metavar="ACK_ID",
                        help="Recorrer cadena: ACK -> Dominio -> Circuito")
    parser.add_argument("--validate-all", action="store_true",
                        help="Validar todos los ACKs del registry")

    args = parser.parse_args()
    registry = load_registry()

    if args.stats:
        print_stats(registry)

    elif args.get:
        ack = get_ack(registry, args.get)
        if ack:
            print(json.dumps(ack, ensure_ascii=False, indent=2))
        else:
            print(f"[NOT FOUND] {args.get}")
            sys.exit(1)

    elif args.filter_domain or args.filter_circuit or args.filter_tipo or \
         args.filter_fundante or args.filter_sigla:
        results = filter_acks(
            registry,
            dominio=args.filter_domain,
            circuito=args.filter_circuit,
            tipo=args.filter_tipo,
            fundante=True if args.filter_fundante else None,
            sigla=args.filter_sigla,
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
        print(f"\n[{len(results)} resultado(s)]")

    elif args.link_corpus:
        n = link_corpus(registry, args.link_corpus)
        if n > 0:
            save_registry(registry)

    elif args.traverse:
        traverse_ack(registry, args.traverse)

    elif args.validate_all:
        acks = registry.get("acks", [])
        errors_found = 0
        for ack in acks:
            errs = validate_ack(ack)
            if errs:
                print(f"[INVALID] {ack.get('ack_id', '?')}:")
                for e in errs:
                    print(f"  - {e}")
                errors_found += 1
        if errors_found == 0:
            print(f"[OK] Todos los {len(acks)} ACKs son validos.")
        else:
            print(f"[ERROR] {errors_found} ACKs invalidos.")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
