# -*- coding: utf-8 -*-
"""
manifest.py — Manifiesto canónico del Corpus Normativo Ecuatoriano
QUIRA Gov · Dylus Lab © 2026

Mapeo explícito de los 41 documentos DOCX en Normativa_Word/ hacia sus metadatos
jurídicos. Fuente de verdad para todos los scripts de ingesta.

Jerarquía normativa:
  0 = Constitución / Tratados internacionales
  1 = Leyes Orgánicas
  2 = Reglamentos
  3 = Resoluciones / Acuerdos ministeriales / Planes nacionales
  4 = Ordenanzas / Normativa local
  5 = Pronunciamientos / Guías metodológicas
"""

NORMATIVA_BASE = (
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Normativa_Word"
)

# ── MANIFIESTO ────────────────────────────────────────────────────────────────
# Cada entrada: archivo relativo a NORMATIVA_BASE, con metadatos completos.
# dominios: lista de Dom01..Dom12 que aplican a esta norma.
# milestone: bloque de atomización QLEP (F0.1..F0.8).
# vigente: True = norma en vigor activo.

MANIFEST: list[dict] = [

    # ── F0.1 CONSTITUCIONAL ──────────────────────────────────────────────────
    {
        "archivo":   "Constitución del Ecuador.docx",
        "sigla":     "CE",
        "nombre":    "Constitución de la República del Ecuador",
        "jerarquia": 0,
        "milestone": "F0.1",
        "tipo":      "constitucion",
        "dominios":  ["Dom01","Dom02","Dom03","Dom04","Dom05","Dom06",
                      "Dom07","Dom08","Dom09","Dom10","Dom11","Dom12"],
        "vigente":   True,
    },

    # ── F0.2 TRANSPARENCIA + DEMOCRACIA ─────────────────────────────────────
    {
        "archivo":   "LOTAIP.docx",
        "sigla":     "LOTAIP",
        "nombre":    "Ley Orgánica de Transparencia y Acceso a la Información Pública",
        "jerarquia": 1,
        "milestone": "F0.2",
        "tipo":      "ley_organica",
        "dominios":  ["Dom07","Dom08"],
        "vigente":   True,
    },
    {
        "archivo":   "LOTAIP - REGLAMENTO-24-01-2024.docx",
        "sigla":     "RLOTAIP",
        "nombre":    "Reglamento General a la Ley Orgánica de Transparencia y Acceso a la Información Pública",
        "jerarquia": 2,
        "milestone": "F0.2",
        "tipo":      "reglamento",
        "dominios":  ["Dom07","Dom08"],
        "vigente":   True,
    },
    {
        "archivo":   "LOTAIP - guia-metodologica-mecanismos.docx",
        "sigla":     "GUIA-LOTAIP-MEC",
        "nombre":    "Guía Metodológica de Mecanismos de Transparencia Activa — DPE",
        "jerarquia": 5,
        "milestone": "F0.2",
        "tipo":      "guia",
        "dominios":  ["Dom07"],
        "vigente":   True,
    },
    {
        "archivo":   "LOTAIP - guia-para-el-cumplimiento-entidades-obligadas-LOTAIP.docx",
        "sigla":     "GUIA-LOTAIP-ENT",
        "nombre":    "Guía para el Cumplimiento de Entidades Obligadas — LOTAIP",
        "jerarquia": 5,
        "milestone": "F0.2",
        "tipo":      "guia",
        "dominios":  ["Dom07"],
        "vigente":   True,
    },
    {
        "archivo":   "LEY-ORGANICA-DE-PARTICIPACION-CIUDADANA.docx",
        "sigla":     "LOPC",
        "nombre":    "Ley Orgánica de Participación Ciudadana",
        "jerarquia": 1,
        "milestone": "F0.2",
        "tipo":      "ley_organica",
        "dominios":  ["Dom07","Dom08"],
        "vigente":   True,
    },
    {
        "archivo":   "Codigo-de-la-Democracia.docx",
        "sigla":     "COD",
        "nombre":    "Código de la Democracia (Ley Orgánica Electoral y de Organizaciones Políticas)",
        "jerarquia": 1,
        "milestone": "F0.2",
        "tipo":      "ley_organica",
        "dominios":  ["Dom07","Dom08"],
        "vigente":   True,
    },
    {
        "archivo":   "CODIFICACION_DEL_REGLAMENTO_DE_DEMOCRACIA_INTERNA.docx",
        "sigla":     "RCOD",
        "nombre":    "Codificación del Reglamento de Democracia Interna",
        "jerarquia": 2,
        "milestone": "F0.2",
        "tipo":      "reglamento",
        "dominios":  ["Dom08"],
        "vigente":   True,
    },

    # ── F0.3 TERRITORIAL / PLANIFICACIÓN ────────────────────────────────────
    {
        "archivo":   "COOTAD.docx",
        "sigla":     "COOTAD",
        "nombre":    "Código Orgánico de Organización Territorial, Autonomía y Descentralización",
        "jerarquia": 1,
        "milestone": "F0.3",
        "tipo":      "ley_organica",
        "dominios":  ["Dom01","Dom02","Dom03","Dom04","Dom06",
                      "Dom07","Dom09","Dom10","Dom11","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "COOTAD PARA LA SOSTENIBILIDAD Y EFICIENCIA 2026.docx",
        "sigla":     "COOTAD-2026",
        "nombre":    "Reforma al COOTAD — Ley Orgánica para la Sostenibilidad y Eficiencia 2026",
        "jerarquia": 1,
        "milestone": "F0.3",
        "tipo":      "reforma",
        "dominios":  ["Dom01","Dom02","Dom04"],
        "vigente":   True,
    },
    {
        "archivo":   "CODIGO_PLANIFICACION_FINAZAS_PÚBLICAS.docx",
        "sigla":     "COPLAFIP",
        "nombre":    "Código Orgánico de Planificación y Finanzas Públicas",
        "jerarquia": 1,
        "milestone": "F0.3",
        "tipo":      "ley_organica",
        "dominios":  ["Dom02","Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "Reglamento-al-COPFP.docx",
        "sigla":     "RCOPLAFIP",
        "nombre":    "Reglamento al Código Orgánico de Planificación y Finanzas Públicas",
        "jerarquia": 2,
        "milestone": "F0.3",
        "tipo":      "reglamento",
        "dominios":  ["Dom02","Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "Plan Nacional de Desarrollo 2025-2029.docx",
        "sigla":     "PND-2025",
        "nombre":    "Plan Nacional de Desarrollo 2025-2029",
        "jerarquia": 3,
        "milestone": "F0.3",
        "tipo":      "plan",
        "dominios":  ["Dom02","Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "PDOT-ACUERDO-Nro.-SNP-SNP-2023-0049-A.docx",
        "sigla":     "ACUERDO-PDOT-2023",
        "nombre":    "Acuerdo Ministerial SNP-SNP-2023-0049-A — Lineamientos PDOT",
        "jerarquia": 3,
        "milestone": "F0.3",
        "tipo":      "acuerdo",
        "dominios":  ["Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "SNP-SNP-2023-0049-A-PDOT-2023.docx",
        "sigla":     "LINEAMIENTOS-PDOT-2023",
        "nombre":    "Lineamientos y Metodología para la Actualización de PDOTs 2023 — SENPLADES",
        "jerarquia": 3,
        "milestone": "F0.3",
        "tipo":      "guia",
        "dominios":  ["Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "Lineamientos-para-el-monitoreo-y-seguimiento-de-los-planes-de-fortalecimiento-institucional (2).docx",
        "sigla":     "LINEAMIENTOS-PFI",
        "nombre":    "Lineamientos para el Monitoreo y Seguimiento de Planes de Fortalecimiento Institucional",
        "jerarquia": 3,
        "milestone": "F0.3",
        "tipo":      "guia",
        "dominios":  ["Dom04","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "Ley-Organica-de-Ordenamiento-Territorial-Uso-y-Gestion-de-Suelo1.docx",
        "sigla":     "LOTUGS",
        "nombre":    "Ley Orgánica de Ordenamiento Territorial, Uso y Gestión del Suelo",
        "jerarquia": 1,
        "milestone": "F0.3",
        "tipo":      "ley_organica",
        "dominios":  ["Dom04","Dom09","Dom11"],
        "vigente":   True,
    },

    # ── F0.4 CONTROL ────────────────────────────────────────────────────────
    {
        "archivo":   "Ley Orgánica de la Contraloría General del Estado.docx",
        "sigla":     "LOC-CGE",
        "nombre":    "Ley Orgánica de la Contraloría General del Estado",
        "jerarquia": 1,
        "milestone": "F0.4",
        "tipo":      "ley_organica",
        "dominios":  ["Dom01","Dom02","Dom03","Dom07"],
        "vigente":   True,
    },
    {
        "archivo":   "Normas de control INterno CGE.docx",
        "sigla":     "NCI-CGE",
        "nombre":    "Normas de Control Interno — Contraloría General del Estado",
        "jerarquia": 3,
        "milestone": "F0.4",
        "tipo":      "resolucion",
        "dominios":  ["Dom01","Dom07"],
        "vigente":   True,
    },

    # ── F0.5 GRUPOS DE ATENCIÓN PRIORITARIA ─────────────────────────────────
    {
        "archivo":   "codigo_ninezyadolescencia.docx",
        "sigla":     "CONA",
        "nombre":    "Código de la Niñez y Adolescencia",
        "jerarquia": 1,
        "milestone": "F0.5",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "ley_organica_discapacidades.docx",
        "sigla":     "LODISC",
        "nombre":    "Ley Orgánica de Discapacidades",
        "jerarquia": 1,
        "milestone": "F0.5",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "LEY ORGANICA DE LAS PERSONAS ADULTAS MAYORES.docx",
        "sigla":     "LOPAM",
        "nombre":    "Ley Orgánica de las Personas Adultas Mayores",
        "jerarquia": 1,
        "milestone": "F0.5",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "ley_de_movilidad_humana_oficial.docx",
        "sigla":     "LMH",
        "nombre":    "Ley Orgánica de Movilidad Humana",
        "jerarquia": 1,
        "milestone": "F0.5",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "ley_prevenir_y_erradicar_violencia_mujeres.docx",
        "sigla":     "LPEVM",
        "nombre":    "Ley Orgánica Integral para Prevenir y Erradicar la Violencia contra las Mujeres",
        "jerarquia": 1,
        "milestone": "F0.5",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "cedaw-recomendacionespanama_26dic.docx",
        "sigla":     "CEDAW",
        "nombre":    "Convención sobre la Eliminación de todas las Formas de Discriminación contra la Mujer — Recomendaciones",
        "jerarquia": 0,
        "milestone": "F0.5",
        "tipo":      "convenio_internacional",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "convencion-americana-derechos-humanos.docx",
        "sigla":     "CADH",
        "nombre":    "Convención Americana sobre Derechos Humanos (Pacto de San José)",
        "jerarquia": 0,
        "milestone": "F0.5",
        "tipo":      "convenio_internacional",
        "dominios":  ["Dom01","Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "derechos CDN Niños.docx",
        "sigla":     "CDN",
        "nombre":    "Convención sobre los Derechos del Niño",
        "jerarquia": 0,
        "milestone": "F0.5",
        "tipo":      "convenio_internacional",
        "dominios":  ["Dom06","Dom12"],
        "vigente":   True,
    },
    {
        "archivo":   "Pacto PIDESC.docx",
        "sigla":     "PIDESC",
        "nombre":    "Pacto Internacional de Derechos Económicos, Sociales y Culturales",
        "jerarquia": 0,
        "milestone": "F0.5",
        "tipo":      "convenio_internacional",
        "dominios":  ["Dom01","Dom06","Dom10","Dom12"],
        "vigente":   True,
    },

    # ── F0.6 OPERATIVO ───────────────────────────────────────────────────────
    {
        "archivo":   "losncp.docx",
        "sigla":     "LOSNCP",
        "nombre":    "Ley Orgánica del Sistema Nacional de Contratación Pública",
        "jerarquia": 1,
        "milestone": "F0.6",
        "tipo":      "ley_organica",
        "dominios":  ["Dom03","Dom07"],
        "vigente":   True,
    },
    {
        "archivo":   "Reglamento-LOSNCP-20251030.docx",
        "sigla":     "RLOSNCP",
        "nombre":    "Reglamento General a la Ley Orgánica del Sistema Nacional de Contratación Pública",
        "jerarquia": 2,
        "milestone": "F0.6",
        "tipo":      "reglamento",
        "dominios":  ["Dom03"],
        "vigente":   True,
    },
    {
        "archivo":   "LEY_SPRGANICA_ERVICIO_PUBLICO LOSEP.docx",
        "sigla":     "LOSEP",
        "nombre":    "Ley Orgánica del Servicio Público",
        "jerarquia": 1,
        "milestone": "F0.6",
        "tipo":      "ley_organica",
        "dominios":  ["Dom01","Dom05"],
        "vigente":   True,
    },
    {
        "archivo":   "REGLAMENTO_LEY_SPRGANICA_ERVICIO_PUBLICO LOSEP.docx",
        "sigla":     "RLOSEP",
        "nombre":    "Reglamento General a la Ley Orgánica del Servicio Público",
        "jerarquia": 2,
        "milestone": "F0.6",
        "tipo":      "reglamento",
        "dominios":  ["Dom01","Dom05"],
        "vigente":   True,
    },
    {
        "archivo":   "Codigo Organico Administrativo.docx",
        "sigla":     "COA",
        "nombre":    "Código Orgánico Administrativo",
        "jerarquia": 1,
        "milestone": "F0.6",
        "tipo":      "ley_organica",
        "dominios":  ["Dom01","Dom07"],
        "vigente":   True,
    },
    {
        "archivo":   "CODIGO_ORGANICO_AMBIENTE-2qzoag.docx",
        "sigla":     "COA-AMB",
        "nombre":    "Código Orgánico del Ambiente",
        "jerarquia": 1,
        "milestone": "F0.6",
        "tipo":      "ley_organica",
        "dominios":  ["Dom04","Dom11"],
        "vigente":   True,
    },
    {
        "archivo":   "REGLAMENTO AL CODIGO ORGANICO DEL AMBIENTE.docx",
        "sigla":     "RCOA-AMB",
        "nombre":    "Reglamento al Código Orgánico del Ambiente",
        "jerarquia": 2,
        "milestone": "F0.6",
        "tipo":      "reglamento",
        "dominios":  ["Dom04","Dom11"],
        "vigente":   True,
    },
    {
        "archivo":   "Ley-organica-para-la-transformacion-digital.docx",
        "sigla":     "LOTD",
        "nombre":    "Ley Orgánica para la Transformación Digital y Audiovisual",
        "jerarquia": 1,
        "milestone": "F0.6",
        "tipo":      "ley_organica",
        "dominios":  ["Dom07","Dom11"],
        "vigente":   True,
    },
    {
        "archivo":   "clasificador_presupuestario_2026.docx",
        "sigla":     "CLASP-2026",
        "nombre":    "Clasificador Presupuestario de Ingresos y Gastos del Sector Público 2026",
        "jerarquia": 3,
        "milestone": "F0.6",
        "tipo":      "resolucion",
        "dominios":  ["Dom02"],
        "vigente":   True,
    },

    # ── F0.7 LOCAL ───────────────────────────────────────────────────────────
    {
        "archivo":   "RESOLUCIÓN ADMINISTRATIVA No. 040-2025-ALC-LJTL-GADMCM ORGANICO.docx",
        "sigla":     "RES-ORG-GADMCM-2025",
        "nombre":    "Resolución Administrativa No. 040-2025 — Estructura Orgánica GADMCM",
        "jerarquia": 4,
        "milestone": "F0.7",
        "tipo":      "resolucion_local",
        "dominios":  ["Dom01","Dom05"],
        "vigente":   True,
    },
    {
        "archivo":   "resolución_no_cpccs-ple-sg-004-o-2026-0030 Rendición de Cuentas.docx",
        "sigla":     "RES-CPCCS-RC-2026",
        "nombre":    "Resolución CPCCS-PLE-SG-004-O-2026-0030 — Rendición de Cuentas",
        "jerarquia": 3,
        "milestone": "F0.7",
        "tipo":      "resolucion",
        "dominios":  ["Dom07","Dom08"],
        "vigente":   True,
    },

    # ── F0.8 COMPLEMENTARIO ──────────────────────────────────────────────────
    {
        "archivo":   "PAGCC-ECUADOR-2024.docx",
        "sigla":     "PAGCC-2024",
        "nombre":    "Plan de Acción de Gobierno de Calidad Centrado en el Ciudadano — Ecuador 2024",
        "jerarquia": 3,
        "milestone": "F0.8",
        "tipo":      "plan",
        "dominios":  ["Dom07","Dom08","Dom09"],
        "vigente":   True,
    },
    {
        "archivo":   "Ley Orgánica para Impulsar la Economía de las Mujeres Emprendedoras.docx",
        "sigla":     "LOIEME",
        "nombre":    "Ley Orgánica para Impulsar la Economía de las Mujeres Emprendedoras",
        "jerarquia": 1,
        "milestone": "F0.8",
        "tipo":      "ley_organica",
        "dominios":  ["Dom06","Dom11","Dom12"],
        "vigente":   True,
    },
]

# ── ÍNDICES DE ACCESO RÁPIDO ──────────────────────────────────────────────────
_BY_SIGLA     = {e["sigla"]: e for e in MANIFEST}
_BY_MILESTONE = {}
for e in MANIFEST:
    _BY_MILESTONE.setdefault(e["milestone"], []).append(e)

def get_by_sigla(sigla: str) -> dict | None:
    return _BY_SIGLA.get(sigla)

def get_by_milestone(milestone: str) -> list[dict]:
    return _BY_MILESTONE.get(milestone, [])

def get_all_siglas() -> list[str]:
    return list(_BY_SIGLA.keys())

def get_milestones() -> list[str]:
    return sorted(set(e["milestone"] for e in MANIFEST))


if __name__ == "__main__":
    # Verificar integridad del manifiesto
    import os
    print(f"Manifiesto: {len(MANIFEST)} documentos\n")
    ok, missing = 0, 0
    for e in MANIFEST:
        path = os.path.join(NORMATIVA_BASE, e["archivo"])
        exists = os.path.exists(path)
        status = "OK     " if exists else "MISSING"
        if exists:
            ok += 1
        else:
            missing += 1
        print(f"  [{status}] {e['sigla']:25s} {e['milestone']}  {e['archivo'][:60]}")
    print(f"\n  OK: {ok}  |  MISSING: {missing}  |  Total: {len(MANIFEST)}")
