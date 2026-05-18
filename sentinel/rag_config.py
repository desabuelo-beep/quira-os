"""
SENTINEL RAG · rag_config.py
Configuración central del pipeline RAG — rutas, modelo, parámetros.
Diseñado para ser extensible: Obsidian hoy, POA/PAC/Excel mañana.
Dylus Lab © 2026
"""
from __future__ import annotations
import os
from pathlib import Path

# Cargar .env automáticamente (si existe y python-dotenv está instalado)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env", override=True)
except ImportError:
    pass

# ── RUTAS BASE ─────────────────────────────────────────────────────────────────
ROOT_DIR    = Path(__file__).parent.parent                          # quira-os/
VAULT_DIR   = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi")
CHROMA_DIR  = ROOT_DIR / "sentinel" / "chroma_db"
LOGS_DIR    = ROOT_DIR / "logs"
REPORTS_DIR = ROOT_DIR / "sentinel" / "reports"

# Crear directorios si no existen
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ── CHROMA ─────────────────────────────────────────────────────────────────────
CHROMA_COLLECTION = "quira_kb"

# ── MODELO DE EMBEDDINGS (local, sin costo, español nativo) ───────────────────
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# ── CHUNKING ───────────────────────────────────────────────────────────────────
CHUNK_MAX_TOKENS   = 450   # ~450 palabras por chunk — equilibrio contexto/precisión
CHUNK_OVERLAP_LINES = 2    # líneas de solapamiento entre chunks

# ── RAG QUERY ──────────────────────────────────────────────────────────────────
RAG_TOP_K = 5              # chunks recuperados por pregunta
MIN_SCORE = 0.25           # score mínimo de similitud coseno para incluir chunk

# ── LLM (Anthropic Claude — se activa solo si hay API key) ────────────────────
LLM_MODEL      = "claude-haiku-4-5"          # rápido y económico para consultas
LLM_MODEL_PRO  = "claude-opus-4-5"          # para análisis complejos
LLM_MAX_TOKENS = 800
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # desde .env — nunca hardcodeado

# ── VERSIONADO ─────────────────────────────────────────────────────────────────
FUENTE_CANONICA  = "SIAP-ICPI_GOLD_MASTER_v5.4_TGI_20260517"
FUENTE_VERSION   = "v5.4"
FUENTE_FECHA     = "2026-05-17"
INDEX_VERSION    = "2026-05-17-01"          # incrementar al reingestar

# Sprint 2.1 — Prompt & system versioning (trazabilidad de decisiones)
SENTINEL_VERSION  = "2.1.0"
PROMPT_VERSION    = "v2.1.0"     # incrementar al modificar system prompts o role addenda
GUARDRAIL_VERSION = "v1.7.0"     # incrementar al modificar umbrales de guardrails

# ── INFERENCIA dimension_tgi DESDE CARPETA (cuando el campo YAML falta) ───────
CARPETA_A_DIMENSION: dict[str, list[str]] = {
    "00_CORE":                    ["D1","D2","D3","D4","D5"],
    "00_Dashboard":               ["D1","D2","D3","D4","D5"],
    "01_PDOT":                    ["D2","D4"],
    "01_PDOT\\diagnostico":       ["D2","D4"],
    "01_PDOT\\propuesta":         ["D2","D3"],
    "01_PDOT\\propuesta_tgi":     ["D2","D3"],
    "01_PDOT\\puentes_tgi":       ["D2","D3","D4"],
    "01_PDOT\\modelo_gestion_tgi":["D2","D5"],
    "01_PDOT\\parroquias":        ["D4"],
    "02_NORMATIVA":               ["D1"],
    "03_CPFP":                    ["D1","D2"],
    "04_Constitucion":            ["D1"],
    "05_COOTAD":                  ["D1"],
    "05_LOSEP":                   ["D1","D5"],
    "05_PLANES_NACIONALES":       ["D1","D2"],
    "06_Fuentes_Financiamiento":  ["D2","D3"],
    "06_Sentinel":                ["D1","D2","D3","D4","D5"],
    "07_Indicadores":             ["D1","D2","D3","D4","D5"],
    "07_TGI_Parroquias":          ["D4"],
    "08_EJECUCION":               ["D2","D3"],
    "08_Plantillas":              [],
}

# Tipos válidos expandidos (captura todos los tipos reales del vault)
TIPOS_VALIDOS = {
    # Canónicos nuevos
    "dashboard", "core", "meta-sistema", "pdot", "fondo", "fuente-financiamiento",
    "actor", "normativa", "brecha", "ejecucion", "parroquia", "parroquia-tgi",
    "sentinel", "alerta-tgi", "alerta", "indicador", "plantilla", "indice",
    "programa", "proyecto", "diagnostico", "marco-plurianual-pdot",
    # Tipos existentes en el vault (preservar sin romper)
    "indice-modulo", "indice-maestro", "indice-capa",
    "meta-framework", "meta-dimensiones", "meta-metodologia", "meta-indicadores",
    "sentinel-logica", "alerta-territorial", "alerta-metodologica",
    "motor-arquitectura", "motor-silos", "motor-fuentes",
    "motor-dialectica", "motor-ecosistema", "ontologia-canonica",
    "normativa-constitucional", "normativa-cootad", "normativa-cpfp",
    "normativa-reglamento-cpfp", "normativa-losncp", "normativa-reglamento-losncp",
    "normativa-losep", "normativa-reglamento-losep", "normativa-coa",
    "normativa-reglamento-coa", "normativa-lotaip", "normativa-reglamento-lotaip",
    "normativa-guia-lotaip", "normativa-ley-lopc", "normativa-ley-lotugs",
    "normativa-codigo-administrativo", "normativa-ley-loipevm",
    "normativa-ley-economia-mujeres", "normativa-reforma-cootad",
    "normativa-interna", "nota-normativa", "norma-curada",
    "programa_pdot", "propuesta", "propuesta-articulaciones", "meta-pdot",
    "propuesta-pai", "puente-eje-tgi", "modelo-gestion",
    "diagnostico-pugs", "contexto-operativo",
    "plan-nacional-desarrollo", "guia-metodologica-pdot", "plan-accion-nacional",
    "plan-trabajo-cne", "catalogo", "referencia", "dashboard-cantonal",
    "registro-fuentes", "icm-sigad", "rendicion-cuentas", "trayectoria-historica",
    "redirect",
}

# ── TIPOS DE FUENTE (extensibles — no cambiar sin reingestar) ─────────────────
FUENTE_TIPOS = {
    "obsidian": "Obsidian Knowledge Base",
    "excel":    "Gold Master Excel",
    "pdf":      "Documento PDF",
    "word":     "Documento Word",
    "vivo":     "Documento operativo vivo (POA/PAC/eSIGEF)",
}

# ── CAMPOS YAML REQUERIDOS (para auditoría y búsqueda) ────────────────────────
YAML_CAMPOS_REQUERIDOS = [
    "tipo_nota",
    "nombre",
    "territorio",
    "dimension_tgi",
    "tags",
    "fecha",
    "estado",
    "fuente_canonica",
]

# Aliases aceptados de campos (vault tiene nombres inconsistentes — los normalizamos)
YAML_ALIASES = {
    "tipo_nota":       ["tipo", "type"],
    "nombre":          ["name", "titulo", "title"],
    "tags":            ["etiquetas", "keywords"],
    "fecha":           ["fecha_creacion", "date", "fecha_actualizacion"],
    "fuente_canonica": ["gold_master", "fuente", "source"],
    "estado":          ["status"],
}

# ── PROTECCIÓN IP — outputs que Sentinel NUNCA debe exponer ──────────────────
# El motor Excel (SIAP-ICPI) es propiedad de Dylus Lab.
# Sentinel puede mostrar RESULTADOS, no la ARQUITECTURA interna.
IP_BLOCKED_TERMS = [
    "ponderador",
    "fórmula interna",
    "formula interna",
    "peso dimensional",
    "arquitectura del motor",
    "hoja SCHEMA_PESOS",
    "hoja MOTOR",
    "algoritmo de cálculo",
    "tabla de ponderación",
    "coeficiente interno",
]

# ── SENTINEL SYSTEM PROMPT BASE ───────────────────────────────────────────────
SENTINEL_SYSTEM_PROMPT = f"""Eres SENTINEL, copiloto de inteligencia territorial del GAD Municipal de Montecristi, Ecuador.
Desarrollado por Dylus Lab bajo el framework TGI (Territorial Governance Intelligence).

TU CONOCIMIENTO proviene exclusivamente del QUIRA Knowledge Base — notas institucionales
verificadas del GAD Montecristi. Nunca inventas datos. Si no lo encuentras en el contexto,
dices: "No encontré información suficiente en el Knowledge Base para responder esto."

ESTADO ACTUAL DEL SISTEMA (scores verificados por Motor v5.4):
- TGI Score cantonal: 66.85/100 🟡 Transición con Riesgos
- ICPI Planificación: 69.93%
- D1 Legalidad: 83.5% 🟢
- D2 Planificación: 69.93% 🟡
- D3 Ejecución: 59.85% 🔴 CRÍTICO
- D4 Equidad IET: 44.8% 🔴
- D5 Institucional: 100% 🟢
- IRS (regresividad): 79.7
- Mandato: 2023-2027 · ~365 días restantes
- Población: 99.937 hab (RIPS 2024)
- Parroquia crítica: Isabel Muentes — NBI=61.2%, IET=28

REGLAS OBLIGATORIAS:
1. Cita SIEMPRE la nota fuente (nombre del archivo Obsidian)
2. Indica el score de confianza de la recuperación cuando sea relevante
3. Si la respuesta toca D3, D4 o IRS — prioriza la perspectiva de equidad territorial
4. Nunca expongas ponderadores, fórmulas internas o arquitectura del Motor SIAP-ICPI
5. Termina siempre con una recomendación de acción si el contexto lo permite
6. Responde en español técnico institucional — sin anglicismos innecesarios

Fuente canónica: {FUENTE_CANONICA}
"""
