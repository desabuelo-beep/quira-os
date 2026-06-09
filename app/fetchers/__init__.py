"""
app/fetchers — Capa Fetcher de /fondos-radar · QUIRA OS
========================================================
ADR-026 §D02.2 · Fetcher Layer

Responsabilidad: Observación (Tipo A en taxonomía QUIRA)
    Descubrir convocatorias de financiamiento en fuentes externas,
    normalizarlas al schema canónico y persistirlas en Supabase.

Separación estricta (Colega v3):
    Fetcher (este módulo)   ≠  Motor (fondos_matcher.py)
    Observación             ≠  Interpretación

Pipeline:
    Adapter → Normalizer → Staging → Validator → Insert → Run Matcher

Módulos:
    base_adapter.py       — Clase base + contrato FondoRaw
    fondos_normalizer.py  — Haiku como motor semántico
    fondos_radar_runner.py — Orquestador del pipeline completo
    adapter_pnud.py       — Adaptador PNUD Ecuador
    adapter_bid.py        — Adaptador BID / IADB
    adapter_aecid.py      — Adaptador AECID España

Dylus Lab © 2026 · ADR-026 §D02
"""
