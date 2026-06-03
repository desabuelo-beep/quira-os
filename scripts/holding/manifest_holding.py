# -*- coding: utf-8 -*-
"""
manifest_holding.py — Inventario del Holding Municipal Montecristi
QUIRA Gov · Capa C (Instrumento Territorial) + Capa D (Evidencia Observacional)
Dylus Lab © 2026

Fuente: C:\\Users\\DELL\\Desktop\\Javo\\Dylus Lab\\ProyecT\\Holding_Municipal_Montecristi
Canton: MCR (Montecristi)

Entidades del Holding:
  GAD_MCR       — GAD Montecristi (municipio)
  EP_ASEO_MCR   — EP Aseo (empresa pública de aseo)
  BOMBEROS_MCR  — Cuerpo de Bomberos Montecristi
  PATRONATO_MCR — Patronato Municipal (servicios sociales)

Modos de ingesta:
  text              → normativa_corpus (DOCX/PDF con embedding vectorial)
  structured        → holding_structured_data (XLSX/CSV, sin embeddings)
  image_pending_ocr → pendiente OCR antes de clasificar
  skip              → archivo duplicado o excluido, no ingestar

Capa C — INSTRUMENTO_TERRITORIAL:
  POA               authority_level=40
  PAC               authority_level=38
  PAI               authority_level=43
  Plan Plurianual   authority_level=45
  Cédula presup.    authority_level=35
  Resolución org.   authority_level=30

Capa D — EVIDENCIA_OBSERVACIONAL:
  Informe RC        authority_level=28  evidence_type='RC_INFORME'
  Informe PP        authority_level=25  evidence_type='PP_INFORME'
  Reporte ICM SIGAD authority_level=22  evidence_type='SIGAD_ICM'
  Plan gobierno CNE authority_level=15  evidence_type=None
"""

HOLDING_BASE = (
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
)

# Fases Gate 6.5 — Dos Circuitos (OBS-007)
#
# Circuito A (Democratico):  PP → POA → PAC → RC → PP
# Circuito B (Financiero):   POA → PAC → Cedulas → RC
#
FASE_1 = ["RC_INFORME", "PP_INFORME"]    # Circuito A+B: evidencia RC+PP  ✅ COMPLETA
FASE_2 = ["POA"]                          # Circuito A+B: planificacion → metas
FASE_3 = ["PAC"]                          # Circuito A+B: contratacion
FASE_4 = ["CEDULA_PRESUPUESTARIA"]        # Circuito B: ejecucion financiera (puente PAC→RC)
FASE_5 = ["SIGAD_ICM"]                    # Circuito B: evaluacion institucional

MANIFEST_HOLDING: list[dict] = [

    # ── FASE 1: RENDICION DE CUENTAS (RC) ─────────────────────────────────────
    # RC cierra los circuitos C01 (transparencia) + C02 (presupuesto) + C03 (planificacion)

    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\GAD Monteristi Rendición de cuentas 2023.docx",
        "sigla":          "RC-GAD-2023",
        "nombre":         "Informe de Rendición de Cuentas GAD Montecristi 2023",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\GAD Monteristi Rendición de cuentas 2024.docx",
        "sigla":          "RC-GAD-2024",
        "nombre":         "Informe de Rendición de Cuentas GAD Montecristi 2024",
        "entity":         "GAD",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Patronato Rendición de cuentas 2023.docx",
        "sigla":          "RC-PATRONATO-2023",
        "nombre":         "Informe de Rendición de Cuentas Patronato Municipal Montecristi 2023",
        "entity":         "PATRONATO",
        "year":           2023,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Patronato Rendición de cuentas 2024.docx",
        "sigla":          "RC-PATRONATO-2024",
        "nombre":         "Informe de Rendición de Cuentas Patronato Municipal Montecristi 2024",
        "entity":         "PATRONATO",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Aseo EP - Rendición de cuentas  2023.pdf",
        "sigla":          "RC-ASEO-2023",
        "nombre":         "Informe de Rendición de Cuentas EP Aseo Montecristi 2023",
        "entity":         "ASEO",
        "year":           2023,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Aseo EP - Rendición de cuentas  2024.pdf",
        "sigla":          "RC-ASEO-2024",
        "nombre":         "Informe de Rendición de Cuentas EP Aseo Montecristi 2024",
        "entity":         "ASEO",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Bomberos Rendición de cuentas 2023.pdf",
        "sigla":          "RC-BOMBEROS-2023",
        "nombre":         "Informe de Rendición de Cuentas Cuerpo de Bomberos Montecristi 2023",
        "entity":         "BOMBEROS",
        "year":           2023,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Rendiciones de cuentas 2023-2024\Bomberos Rendición de cuentas 2024.pdf",
        "sigla":          "RC-BOMBEROS-2024",
        "nombre":         "Informe de Rendición de Cuentas Cuerpo de Bomberos Montecristi 2024",
        "entity":         "BOMBEROS",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 28,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "RC_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },

    # ── FASE 1: PRESUPUESTO PARTICIPATIVO (PP) ─────────────────────────────────
    # PP cierra circuitos C01 (transparencia) + C02 (presupuesto) + C03 (planificacion)

    {
        "archivo":        r"Presupuesto participativo 2024-2026\GAD Montecristi Informe Presupuesto Participativo 2024.pdf",
        "sigla":          "PP-GAD-2024",
        "nombre":         "Informe de Presupuesto Participativo GAD Montecristi 2024",
        "entity":         "GAD",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 25,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "PP_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Presupuesto participativo 2024-2026\GAD Montecristi Informe Presupuesto Participativo 2025.pdf",
        "sigla":          "PP-GAD-2025",
        "nombre":         "Informe de Presupuesto Participativo GAD Montecristi 2025",
        "entity":         "GAD",
        "year":           2025,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 25,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "PP_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },
    {
        "archivo":        r"Presupuesto participativo 2024-2026\INFORME DE PRESUPUESTO PARTICIPATIVO 2026.pdf",
        "sigla":          "PP-GAD-2026",
        "nombre":         "Informe de Presupuesto Participativo GAD Montecristi 2026",
        "entity":         "GAD",
        "year":           2026,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 25,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "PP_INFORME",
        "circuit_refs":   ["C01", "C02", "C03"],
        "ingest_mode":    "text",
        "fase":           1,
    },

    # ── FASE 2: POA — PLAN OPERATIVO ANUAL ────────────────────────────────────
    # POA vincula Planificacion → Ejecucion (circuitos C02 + C03)

    # GAD POA (prefer DOCX over PDF; PDFs marcados skip)
    {
        "archivo":        r"Oficiales\GAD_Monteristi_POA_2023.docx",
        "sigla":          "POA-GAD-2023",
        "nombre":         "Plan Operativo Anual GAD Montecristi 2023",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales\GAD_Monteristi_POA_2024.docx",
        "sigla":          "POA-GAD-2024",
        "nombre":         "Plan Operativo Anual GAD Montecristi 2024",
        "entity":         "GAD",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales_2026\GAD Montecristi POA 2025.pdf",
        "sigla":          "POA-GAD-2025",
        "nombre":         "Plan Operativo Anual GAD Montecristi 2025",
        "entity":         "GAD",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        "Plan Operativo Anual POA_2026.pdf",
        "sigla":          "POA-GAD-2026-v2",
        "nombre":         "Plan Operativo Anual GAD Montecristi 2026 (versión 2)",
        "entity":         "GAD",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"POA 2023-2026\GAD Montecristi POA 2026.pdf",
        "sigla":          "POA-GAD-2026",
        "nombre":         "Plan Operativo Anual GAD Montecristi 2026",
        "entity":         "GAD",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },

    # Patronato POA (prefer DOCX)
    {
        "archivo":        r"Oficiales\POA 2023 Patronato Montecristi.docx",
        "sigla":          "POA-PATRONATO-2023",
        "nombre":         "Plan Operativo Anual Patronato Municipal Montecristi 2023",
        "entity":         "PATRONATO",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales\POA 2024 Patronato Montecristi.docx",
        "sigla":          "POA-PATRONATO-2024",
        "nombre":         "Plan Operativo Anual Patronato Municipal Montecristi 2024",
        "entity":         "PATRONATO",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },

    # EP Aseo POA
    {
        "archivo":        r"POA 2023-2026\ASEO EP POA 2024.pdf",
        "sigla":          "POA-ASEO-2024",
        "nombre":         "Plan Operativo Anual EP Aseo Montecristi 2024",
        "entity":         "ASEO",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"POA 2023-2026\Aseo Ep POA 2026.docx",
        "sigla":          "POA-ASEO-2026",
        "nombre":         "Plan Operativo Anual EP Aseo Montecristi 2026",
        "entity":         "ASEO",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        # Extraído de Google Drive via extensión Claude-in-Chrome (sin descarga directa).
        # Drive: https://drive.google.com/file/d/1Fwgw2smrUQJaEWFTkwBaXN7W-Qzz8Xd9/view
        # Texto limpiado: ! → espacios (artefacto de codificación PDF del visor Drive).
        "archivo":        r"POA 2023-2026\Aseo Ep POA 2025.txt",
        "sigla":          "POA-ASEO-2025",
        "nombre":         "Plan Operativo Anual EP Aseo Montecristi 2025",
        "entity":         "ASEO",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },

    # Bomberos POA
    {
        "archivo":        r"POA 2023-2026\Bomberos POA 2024.pdf",
        "sigla":          "POA-BOMBEROS-2024",
        "nombre":         "Plan Operativo Anual Cuerpo de Bomberos Montecristi 2024",
        "entity":         "BOMBEROS",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales_2026\Bomberos POA 2025.pdf",
        "sigla":          "POA-BOMBEROS-2025",
        "nombre":         "Plan Operativo Anual Cuerpo de Bomberos Montecristi 2025",
        "entity":         "BOMBEROS",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"POA 2023-2026\Bomberos Montecristi POA 2026.docx",
        "sigla":          "POA-BOMBEROS-2026",
        "nombre":         "Plan Operativo Anual Cuerpo de Bomberos Montecristi 2026",
        "entity":         "BOMBEROS",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 40,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },

    # ── FASE 3: PAC — PLAN ANUAL DE CONTRATACION ──────────────────────────────
    # PAC vincula Planificacion → Contratacion (circuito C03)

    # GAD PAC (prefer DOCX cuando existe; PDFs duplicados marcados skip)
    {
        "archivo":        r"Oficiales\GAD_Montecristi_PAC_2023.docx",
        "sigla":          "PAC-GAD-2023",
        "nombre":         "Plan Anual de Contratación GAD Montecristi 2023",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales\GAD_Montecristi_PAC_2024.docx",
        "sigla":          "PAC-GAD-2024",
        "nombre":         "Plan Anual de Contratación GAD Montecristi 2024",
        "entity":         "GAD",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\GAD_Montecristi_PAC_2025.pdf",
        "sigla":          "PAC-GAD-2025",
        "nombre":         "Plan Anual de Contratación GAD Montecristi 2025",
        "entity":         "GAD",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales_2026\GAD Montecristi PAC 2026.pdf",
        "sigla":          "PAC-GAD-2026",
        "nombre":         "Plan Anual de Contratación GAD Montecristi 2026",
        "entity":         "GAD",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # Patronato PAC (prefer DOCX)
    {
        "archivo":        r"Oficiales\PAc Patronato 2023.docx",
        "sigla":          "PAC-PATRONATO-2023",
        "nombre":         "Plan Anual de Contratación Patronato Municipal Montecristi 2023",
        "entity":         "PATRONATO",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales\PAc Patronato 2024.docx",
        "sigla":          "PAC-PATRONATO-2024",
        "nombre":         "Plan Anual de Contratación Patronato Municipal Montecristi 2024",
        "entity":         "PATRONATO",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\Patronato _PAC_2025.pdf",
        "sigla":          "PAC-PATRONATO-2025",
        "nombre":         "Plan Anual de Contratación Patronato Municipal Montecristi 2025",
        "entity":         "PATRONATO",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales_2026\Patronato PAC 2026.pdf",
        "sigla":          "PAC-PATRONATO-2026",
        "nombre":         "Plan Anual de Contratación Patronato Municipal Montecristi 2026",
        "entity":         "PATRONATO",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # EP Aseo PAC
    {
        "archivo":        r"PAC 2023-2026\Aseo EP - PAC 2023.pdf",
        "sigla":          "PAC-ASEO-2023",
        "nombre":         "Plan Anual de Contratación EP Aseo Montecristi 2023",
        "entity":         "ASEO",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\Aseo EP - PAC 2024.pdf",
        "sigla":          "PAC-ASEO-2024",
        "nombre":         "Plan Anual de Contratación EP Aseo Montecristi 2024",
        "entity":         "ASEO",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\Aseo EP - PAC 2025.pdf",
        "sigla":          "PAC-ASEO-2025",
        "nombre":         "Plan Anual de Contratación EP Aseo Montecristi 2025",
        "entity":         "ASEO",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales_2026\Aseo Ep PAC 2026.pdf",
        "sigla":          "PAC-ASEO-2026",
        "nombre":         "Plan Anual de Contratación EP Aseo Montecristi 2026",
        "entity":         "ASEO",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "EP_ASEO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # Bomberos PAC
    {
        "archivo":        r"PAC 2023-2026\Bomberos PAC 2023.pdf",
        "sigla":          "PAC-BOMBEROS-2023",
        "nombre":         "Plan Anual de Contratación Cuerpo de Bomberos Montecristi 2023",
        "entity":         "BOMBEROS",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\Bomberos PAC 2024.pdf",
        "sigla":          "PAC-BOMBEROS-2024",
        "nombre":         "Plan Anual de Contratación Cuerpo de Bomberos Montecristi 2024",
        "entity":         "BOMBEROS",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"PAC 2023-2026\Bomberos PAC 2025.pdf",
        "sigla":          "PAC-BOMBEROS-2025",
        "nombre":         "Plan Anual de Contratación Cuerpo de Bomberos Montecristi 2025",
        "entity":         "BOMBEROS",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },
    {
        "archivo":        r"Oficiales_2026\Bomberos Montecristi PAC 2026.pdf",
        "sigla":          "PAC-BOMBEROS-2026",
        "nombre":         "Plan Anual de Contratación Cuerpo de Bomberos Montecristi 2026",
        "entity":         "BOMBEROS",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 38,
        "source_entity":  "BOMBEROS_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # ── FASE 2/3: PAI — PLAN ANUAL DE INVERSION ───────────────────────────────
    # PAI vincula Planificacion → Ejecucion (C02 + C03)

    {
        "archivo":        "Plan Anual de Inversion (PAI) 2023.pdf",
        "sigla":          "PAI-GAD-2023",
        "nombre":         "Plan Anual de Inversión GAD Montecristi 2023",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 43,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        "Plan Anual de Inversion (PAI) 2025.pdf",
        "sigla":          "PAI-GAD-2025",
        "nombre":         "Plan Anual de Inversión GAD Montecristi 2025",
        "entity":         "GAD",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 43,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        "Plan Anual de inversion (PAI) 2026.pdf",
        "sigla":          "PAI-GAD-2026",
        "nombre":         "Plan Anual de Inversión GAD Montecristi 2026",
        "entity":         "GAD",
        "year":           2026,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 43,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales\PLAN PLURIANUAL DE INVERSIONES GAD Montecristi PDOT.docx",
        "sigla":          "PAI-PLURIANUAL-GAD",
        "nombre":         "Plan Plurianual de Inversiones GAD Montecristi — PDOT",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 45,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },
    {
        "archivo":        r"Oficiales\Plan Bicentenario1-comprimido.pdf",
        "sigla":          "PLAN-BICENTENARIO-MCR",
        "nombre":         "Plan Bicentenario — Cantón Montecristi",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 45,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           2,
    },

    # ── FASE 3: PRESUPUESTO / CEDULA DOCUMENTAL ────────────────────────────────

    {
        "archivo":        r"Oficiales\Patronato_Presupesto_2024.docx",
        "sigla":          "PRESUP-PATRONATO-2024-DOC",
        "nombre":         "Presupuesto Patronato Municipal Montecristi 2024 (documento)",
        "entity":         "PATRONATO",
        "year":           2024,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 35,
        "source_entity":  "PATRONATO_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # ── RESOLUCION ORGANICA ────────────────────────────────────────────────────

    {
        "archivo":        r"Oficiales\RESOLUCIÓN ADMINISTRATIVA No. 040-2025-ALC-LJTL-GADMCM ORGANICO ESTRUCTURAL.pdf",
        "sigla":          "RES-ORG-GAD-2025",
        "nombre":         "Resolución Administrativa No. 040-2025 — Orgánico Estructural GADMCM",
        "entity":         "GAD",
        "year":           2025,
        "document_class": "INSTRUMENTO_TERRITORIAL",
        "authority_level": 30,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  None,
        "circuit_refs":   ["C01"],
        "ingest_mode":    "text",
        "fase":           3,
    },

    # ── FASE 4: SIGAD ICM ─────────────────────────────────────────────────────
    # SIGAD cierra Ejecucion → Evaluacion

    # Prefer DOCX for SIGAD 2023 and 2024
    {
        "archivo":        r"Oficiales\Reporte ICM SIGAD 2023.docx",
        "sigla":          "SIGAD-GAD-2023-DOC",
        "nombre":         "Reporte ICM SIGAD GAD Montecristi 2023 (DOCX)",
        "entity":         "GAD",
        "year":           2023,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 22,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "SIGAD_ICM",
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           5,
    },
    {
        "archivo":        r"Oficiales\Reporte ICM SIGAD 2024.docx",
        "sigla":          "SIGAD-GAD-2024-DOC",
        "nombre":         "Reporte ICM SIGAD GAD Montecristi 2024 (DOCX)",
        "entity":         "GAD",
        "year":           2024,
        "document_class": "EVIDENCIA_OBSERVACIONAL",
        "authority_level": 22,
        "source_entity":  "GAD_MCR",
        "canton_id":      "MCR",
        "evidence_type":  "SIGAD_ICM",
        "circuit_refs":   ["C02", "C03"],
        "ingest_mode":    "text",
        "fase":           5,
    },

    # ── PLAN DE GOBIERNO CNE ──────────────────────────────────────────────────
    # SKIP — mismo doc ya ingresado en normativa_corpus con sigla PLAN-GOB-MCR

    {
        "archivo":        "Plan CNE ALcalde Montecristi.docx",
        "sigla":          "PLAN-GOB-MCR-HOLDING",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_in_normativa_corpus — sigla PLAN-GOB-MCR ya ingresada",
    },

    # ── DUPLICADOS: PDF vs DOCX — prefer DOCX ─────────────────────────────────

    {
        "archivo":        r"PAC 2023-2026\GAD_Montecristi_PAC_2023.pdf",
        "sigla":          "PAC-GAD-2023-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar GAD_Montecristi_PAC_2023.docx",
    },
    {
        "archivo":        r"PAC 2023-2026\GAD_Montecristi_PAC_2024.pdf",
        "sigla":          "PAC-GAD-2024-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar GAD_Montecristi_PAC_2024.docx",
    },
    {
        "archivo":        r"POA 2023-2026\GAD Montecristi POA 2023.pdf",
        "sigla":          "POA-GAD-2023-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar GAD_Monteristi_POA_2023.docx",
    },
    {
        "archivo":        r"POA 2023-2026\GAD Montecristi POA 2024.pdf",
        "sigla":          "POA-GAD-2024-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar GAD_Monteristi_POA_2024.docx",
    },
    {
        "archivo":        r"Oficiales_2026\GAD Monteristi POA 2025.pdf",
        "sigla":          "POA-GAD-2025-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate — misma entidad/año que POA-GAD-2025",
    },
    {
        "archivo":        r"PAC 2023-2026\Patronato PAC 2023.pdf",
        "sigla":          "PAC-PATRONATO-2023-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar PAc Patronato 2023.docx",
    },
    {
        "archivo":        r"PAC 2023-2026\Patronato PAC 2024.pdf",
        "sigla":          "PAC-PATRONATO-2024-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar PAc Patronato 2024.docx",
    },
    {
        "archivo":        r"POA 2023-2026\Patronato POA 2023.pdf",
        "sigla":          "POA-PATRONATO-2023-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar POA 2023 Patronato Montecristi.docx",
    },
    {
        "archivo":        r"POA 2023-2026\Patronato POA 2024.pdf",
        "sigla":          "POA-PATRONATO-2024-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar POA 2024 Patronato Montecristi.docx",
    },
    {
        "archivo":        "Reporte ICM SIGAD 2023.pdf",   # raiz
        "sigla":          "SIGAD-GAD-2023",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar Reporte ICM SIGAD 2023.docx",
    },
    {
        "archivo":        "Reporte ICM SIGAD 2024.pdf",   # raiz
        "sigla":          "SIGAD-GAD-2024",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar Reporte ICM SIGAD 2024.docx",
    },
    {
        "archivo":        r"POA 2023-2026\Aseo Ep POA 2026.pdf",
        "sigla":          "POA-ASEO-2026-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar POA 2023-2026\\Aseo Ep POA 2026.docx",
    },
    {
        "archivo":        r"POA 2023-2026\Bomberos Montecristi POA 2026.pdf",
        "sigla":          "POA-BOMBEROS-2026-PDF",
        "ingest_mode":    "skip",
        "motivo":         "duplicate_prefer_docx — usar POA 2023-2026\\Bomberos Montecristi POA 2026.docx",
    },

    # ── STRUCTURED DATA: XLSX / XLS / CSV ─────────────────────────────────────
    # Van a holding_structured_data — no generan embeddings vectoriales

    {
        "archivo":        r"Oficiales\Aseo EP - Presupuesto diciembre 2024.xlsx",
        "sigla":          "STRUCT-ASEO-PRESUP-DIC2024",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales\Bomberos Presupuesto 2024.xlsx",
        "sigla":          "STRUCT-BOMBEROS-PRESUP-2024",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\GAD Montecristi_Cedula_Presupuestaria_de_Gastos_ 2024.xls",
        "sigla":          "STRUCT-GAD-CEDULA-GASTOS-2024",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\GAD Montecristi_Diciembre_Cedula_Presupuestaria_de_Gastos_ 2023.xls",
        "sigla":          "STRUCT-GAD-CEDULA-GASTOS-DIC2023",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales\PAC INICIAL 2025 GAD MONTECRISTI-POSTERIOR DE PUBLICACION SUBSANADO (1).xlsx",
        "sigla":          "STRUCT-GAD-PAC-INICIAL-2025",
        "ingest_mode":    "structured",
        "motivo":         "pac_tabular — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales\Patronato_Presupesto_2024.xlsx",
        "sigla":          "STRUCT-PATRONATO-PRESUP-2024",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales_2026\Aseo Ep Presupuesto Marzo 2026.xlsx",
        "sigla":          "STRUCT-ASEO-PRESUP-MAR2026",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales_2026\Bomberos Montecristi Presupuesto 2026.xlsx",
        "sigla":          "STRUCT-BOMBEROS-PRESUP-2026",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Presupuestos 2026\GAD Montecristi Presupuesto abril 2026.xlsx",
        "sigla":          "STRUCT-GAD-PRESUP-ABR2026",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales_2026\Patronato Presupuesto Marzo 2026.xlsx",
        "sigla":          "STRUCT-PATRONATO-PRESUP-MAR2026",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Aseo EP Presupuesto Diciembre 2024.xlsx",
        "sigla":          "STRUCT-ASEO-PRESUP-DIC2024-B",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"POA 2023-2026\Bomberos POA 2023.xlsx",
        "sigla":          "STRUCT-BOMBEROS-POA-2023",
        "ingest_mode":    "structured",
        "motivo":         "poa_tabular — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Bomberos POA 2024.xlsx",
        "sigla":          "STRUCT-BOMBEROS-POA-2024",
        "ingest_mode":    "structured",
        "motivo":         "poa_tabular — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Patronato Presupesto Diciembre 2023.pdf",
        "sigla":          "STRUCT-PATRONATO-PRESUP-DIC2023",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria_pdf — holding_structured_data (tabular, no narrativo)",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Patronato Presupesto Diciembre 2024.xlsx",
        "sigla":          "STRUCT-PATRONATO-PRESUP-DIC2024",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Presupuestos 2023-2026\Presupuestos 2026\Bomberos Presupuesto abril 2026.xlsx",
        "sigla":          "STRUCT-BOMBEROS-PRESUP-2026-B",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria — holding_structured_data",
    },
    {
        "archivo":        r"Oficiales\GAD Montecrisi cedula presupuestaria 2025.pdf",
        "sigla":          "STRUCT-GAD-CEDULA-2025",
        "ingest_mode":    "structured",
        "motivo":         "cedula_presupuestaria_pdf — holding_structured_data (tabular, no narrativo)",
    },
    {
        "archivo":        r"POA 2023-2026\Patronato_POA_2025.xlsx",
        "sigla":          "STRUCT-PATRONATO-POA-2025",
        "ingest_mode":    "structured",
        "motivo":         "poa_tabular — holding_structured_data",
    },
    {
        "archivo":        r"POA 2023-2026\Patronato_POA_2026.xlsx",
        "sigla":          "STRUCT-PATRONATO-POA-2026",
        "ingest_mode":    "structured",
        "motivo":         "poa_tabular — holding_structured_data",
    },

    # ── IMAGE PENDING OCR ─────────────────────────────────────────────────────
    # pagina_01.png a pagina_17.png requieren OCR antes de clasificar y asignar metadatos

    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_01.png", "sigla": "IMG-HOLDING-01", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_02.png", "sigla": "IMG-HOLDING-02", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_03.png", "sigla": "IMG-HOLDING-03", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_04.png", "sigla": "IMG-HOLDING-04", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_05.png", "sigla": "IMG-HOLDING-05", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_06.png", "sigla": "IMG-HOLDING-06", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_07.png", "sigla": "IMG-HOLDING-07", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_08.png", "sigla": "IMG-HOLDING-08", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_09.png", "sigla": "IMG-HOLDING-09", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_10.png", "sigla": "IMG-HOLDING-10", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_11.png", "sigla": "IMG-HOLDING-11", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_12.png", "sigla": "IMG-HOLDING-12", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_13.png", "sigla": "IMG-HOLDING-13", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_14.png", "sigla": "IMG-HOLDING-14", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_15.png", "sigla": "IMG-HOLDING-15", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_16.png", "sigla": "IMG-HOLDING-16", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
    {"archivo": r"Oficiales\cedulas Presupuesto GAD 2025 JPG\pagina_17.png", "sigla": "IMG-HOLDING-17", "ingest_mode": "image_pending_ocr", "motivo": "requiere_ocr"},
]


# ── INDICES DE ACCESO RAPIDO ──────────────────────────────────────────────────

_BY_SIGLA = {e["sigla"]: e for e in MANIFEST_HOLDING if "sigla" in e}
_BY_FASE: dict[int, list[dict]] = {}
for e in MANIFEST_HOLDING:
    fase = e.get("fase")
    if fase:
        _BY_FASE.setdefault(fase, []).append(e)
_TEXT_DOCS = [e for e in MANIFEST_HOLDING if e.get("ingest_mode") == "text"]
_STRUCTURED = [e for e in MANIFEST_HOLDING if e.get("ingest_mode") == "structured"]
_FASE_1_DOCS = _BY_FASE.get(1, [])


def get_fase(n: int) -> list[dict]:
    return _BY_FASE.get(n, [])


def get_text_docs() -> list[dict]:
    return _TEXT_DOCS


def get_structured_docs() -> list[dict]:
    return _STRUCTURED


if __name__ == "__main__":
    total = len(MANIFEST_HOLDING)
    text = len(_TEXT_DOCS)
    structured = len(_STRUCTURED)
    skip = sum(1 for e in MANIFEST_HOLDING if e.get("ingest_mode") == "skip")
    img = sum(1 for e in MANIFEST_HOLDING if e.get("ingest_mode") == "image_pending_ocr")
    print(f"Manifest Holding MCR: {total} entradas")
    print(f"  text (normativa_corpus): {text}")
    print(f"  structured (holding_structured_data): {structured}")
    print(f"  skip (duplicados): {skip}")
    print(f"  image_pending_ocr: {img}")
    print(f"  Fase 1 (RC+PP): {len(get_fase(1))}")
    print(f"  Fase 2 (POA):  {len(get_fase(2))}")
    print(f"  Fase 3 (PAC):  {len(get_fase(3))}")
    print(f"  Fase 4 (SIGAD): {len(get_fase(4))}")
