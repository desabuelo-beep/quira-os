"""
QUIRA Gov — Sprint 2: Neo4j QTMP Loader
========================================
Carga los 3 circuitos QTMP de Montecristi en Neo4j.
Objetivo: preparar el grafo para la consulta bautismal (ADR-010).

Circuitos cargados (en orden de prioridad):
  1. GAP_10PCT   — COOTAD_249 paradoja causal (datos confirmados)
  2. AGUA_POTABLE — CE_12 cobertura 34.9% ROJO
  3. EQUIDAD     — COOTAD_228 brecha NBI 32pp ROJO

Uso:
  pip install neo4j pyyaml
  python neo4j_load_qtmp.py --uri bolt://localhost:7687 --user neo4j --password <tu_password>

Luego ejecutar el query bautismal (ADR-010):
  python neo4j_bautismal_query.py --uri bolt://localhost:7687 --user neo4j --password <tu_password>

DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones
"""

import argparse
import sys
from neo4j import GraphDatabase


# ============================================================
# CONEXION
# ============================================================

def get_driver(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))


def test_connection(driver):
    with driver.session() as session:
        result = session.run("RETURN 'QUIRA Neo4j conectado' AS msg")
        print(result.single()["msg"])


# ============================================================
# UTILIDAD: MERGE NODO CON PROPIEDADES
# ============================================================

def run(session, cypher, **params):
    """Ejecuta un statement Cypher con params y retorna el resultado."""
    return session.run(cypher, **params)


# ============================================================
# BLOQUE 0 — CANTON Y CORPUS NORMATIVO (ACK ATOMS)
# ============================================================

CYPHER_CANTON = """
MERGE (c:Canton {id: 'ECU-13-MONTECRISTI'})
SET c.nombre = 'Montecristi',
    c.provincia = 'Manabí',
    c.codigo_dpa = '13',
    c.pais = 'Ecuador',
    c.quira_activo = true
"""

# Los ACK atoms que materializan los 3 circuitos
ACK_ATOMS = [
    {
        "id": "COOTAD_249",
        "tipo": "obligacion",
        "nombre": "10% Presupuesto GAP obligatorio",
        "norma": "Código Orgánico de Organización Territorial, Autonomía y Descentralización",
        "sigla": "COOTAD",
        "articulo": "249",
        "jerarquia": 1,
        "obligacion": (
            "Los gobiernos autónomos descentralizados municipales asignarán en sus presupuestos "
            "una partida de al menos el diez por ciento de sus ingresos no tributarios para el "
            "financiamiento de la planificación y ejecución de programas sociales para la atención "
            "a grupos de atención prioritaria."
        ),
        "actor_obligado": "GAD-Municipal",
        "actor_beneficiario": "Grupos de Atención Prioritaria",
        "dominio_quira": "Dom12",
        "consecuencia_tipo": "glosa-cge",
        "organo_sancionador": "CGE",
    },
    {
        "id": "CE_12",
        "tipo": "derecho",
        "nombre": "Agua como derecho humano irrenunciable",
        "norma": "Constitución del Ecuador 2008",
        "sigla": "CE",
        "articulo": "12",
        "jerarquia": 0,
        "obligacion": (
            "El derecho humano al agua es fundamental e irrenunciable. El agua constituye "
            "patrimonio nacional estratégico de uso público, inalienable, imprescriptible, "
            "inembargable y esencial para la vida."
        ),
        "actor_obligado": "GAD-Municipal",
        "actor_beneficiario": "Ciudadanos",
        "dominio_quira": "Dom04",
        "consecuencia_tipo": "nulidad",
        "organo_sancionador": "Judicatura",
    },
    {
        "id": "CE_264",
        "tipo": "competencia_exclusiva",
        "nombre": "Competencia exclusiva agua potable cantonal",
        "norma": "Constitución del Ecuador 2008",
        "sigla": "CE",
        "articulo": "264",
        "jerarquia": 0,
        "obligacion": (
            "Los gobiernos municipales tendrán las siguientes competencias exclusivas: "
            "numeral 4 — Prestar los servicios públicos de agua potable, alcantarillado, "
            "depuración de aguas residuales, manejo de desechos sólidos, actividades de saneamiento ambiental."
        ),
        "actor_obligado": "GAD-Municipal",
        "actor_beneficiario": "Ciudadanos",
        "dominio_quira": "Dom04",
        "consecuencia_tipo": "responsabilidad-administrativa",
        "organo_sancionador": "CGE",
    },
    {
        "id": "COOTAD_228",
        "tipo": "obligacion",
        "nombre": "Criterios equidad distribución inversión territorial",
        "norma": "Código Orgánico de Organización Territorial, Autonomía y Descentralización",
        "sigla": "COOTAD",
        "articulo": "228",
        "jerarquia": 1,
        "obligacion": (
            "Los presupuestos de los gobiernos autónomos descentralizados se formularán de conformidad con "
            "el Plan de Desarrollo y de Ordenamiento Territorial, aplicando criterios de equidad territorial "
            "en la distribución de la inversión: densidad poblacional, necesidades básicas insatisfechas, "
            "logros de desarrollo y brechas existentes."
        ),
        "actor_obligado": "GAD-Municipal",
        "actor_beneficiario": "Parroquias rurales y zonas de alta NBI",
        "dominio_quira": "Dom04",
        "consecuencia_tipo": "observacion-cpccs",
        "organo_sancionador": "CPCCS",
    },
    {
        "id": "CE_35",
        "tipo": "derecho",
        "nombre": "Derechos grupos atención prioritaria",
        "norma": "Constitución del Ecuador 2008",
        "sigla": "CE",
        "articulo": "35",
        "jerarquia": 0,
        "obligacion": (
            "Las personas adultas mayores, niñas, niños y adolescentes, mujeres embarazadas, "
            "personas con discapacidad, personas privadas de libertad y quienes adolezcan de "
            "enfermedades catastróficas o de alta complejidad, recibirán atención prioritaria "
            "y especializada en los ámbitos público y privado."
        ),
        "actor_obligado": "GAD-Municipal",
        "actor_beneficiario": "Grupos de Atención Prioritaria",
        "dominio_quira": "Dom12",
        "consecuencia_tipo": "responsabilidad-administrativa",
        "organo_sancionador": "DPE",
    },
    {
        "id": "CE_274",
        "tipo": "obligacion",
        "nombre": "Criterio equidad asignación recursos subnacionales",
        "norma": "Constitución del Ecuador 2008",
        "sigla": "CE",
        "articulo": "274",
        "jerarquia": 0,
        "obligacion": (
            "Los gobiernos autónomos descentralizados en cuyo territorio se exploten o industrialicen "
            "recursos naturales tendrán derecho a participar de las rentas que perciba el Estado por "
            "esta actividad, de acuerdo con la ley. El criterio de equidad rige la asignación de recursos."
        ),
        "actor_obligado": "Estado-Central",
        "actor_beneficiario": "GAD y ciudadanos",
        "dominio_quira": "Dom04",
        "consecuencia_tipo": "ninguna",
        "organo_sancionador": "",
    },
]

CYPHER_ATOM = """
MERGE (a:Atom {id: $id})
SET a.tipo = $tipo,
    a.nombre = $nombre,
    a.norma = $norma,
    a.sigla = $sigla,
    a.articulo = $articulo,
    a.jerarquia = $jerarquia,
    a.obligacion = $obligacion,
    a.actor_obligado = $actor_obligado,
    a.actor_beneficiario = $actor_beneficiario,
    a.dominio_quira = $dominio_quira,
    a.consecuencia_tipo = $consecuencia_tipo,
    a.organo_sancionador = $organo_sancionador,
    a.capa_qnkc = 'C1'
"""


# ============================================================
# BLOQUE 1 — CIRCUITO GAP_10PCT
# ============================================================

def load_gap_10pct(session):
    print("\n  Cargando GAP_10PCT...")

    # C3 — Servicio Público
    run(session, """
    MERGE (sp:C3ServicioPublico {id: 'SP_G10P_MCR'})
    SET sp.nombre = 'Atención Integral a Grupos de Atención Prioritaria — Montecristi',
        sp.circuito_id = 'GAP_10PCT',
        sp.canton_id = 'ECU-13-MONTECRISTI',
        sp.dominio_tgi = 'Dom12',
        sp.modalidad = 'entidad_adscrita',
        sp.capa_qnkc = 'C3',
        sp.qtmp_id = 'QTMP_GAP_10PCT_MCR'
    WITH sp
    MATCH (c:Canton {id: 'ECU-13-MONTECRISTI'})
    MERGE (sp)-[:ANCLADO_EN]->(c)
    WITH sp
    MATCH (ack:Atom {id: 'COOTAD_249'})
    MERGE (ack)-[:MATERIALIZA_VIA]->(sp)
    WITH sp
    MATCH (ack2:Atom {id: 'CE_35'})
    MERGE (ack2)-[:HABILITA]->(sp)
    """)

    # C4 — Procesos
    procesos_gap = [
        {
            "id": "PRO_G10P_01_MCR",
            "nombre": "Programación Presupuestaria 10% GAP",
            "tipo": "administrativo",
            "estado": "activo",
        },
        {
            "id": "PRO_G10P_02_MCR",
            "nombre": "Programas para Adultos Mayores",
            "tipo": "operativo",
            "estado": "activo",
        },
        {
            "id": "PRO_G10P_03_MCR",
            "nombre": "Programas para Personas con Discapacidad",
            "tipo": "operativo",
            "estado": "activo",
        },
        {
            "id": "PRO_G10P_04_MCR",
            "nombre": "Protección de Niñez y Adolescencia (NNA)",
            "tipo": "operativo",
            "estado": "activo",
        },
        {
            "id": "PRO_G10P_05_MCR",
            "nombre": "Atención a Personas en Movilidad Humana",
            "tipo": "operativo",
            "estado": "activo",
        },
        {
            "id": "PRO_G10P_06_MCR",
            "nombre": "Seguimiento y Rendición de Cuentas GAP",
            "tipo": "control_interno",
            "estado": "activo",
        },
    ]
    for p in procesos_gap:
        run(session, """
        MERGE (proc:C4Proceso {id: $id})
        SET proc.nombre = $nombre, proc.tipo = $tipo, proc.estado = $estado,
            proc.canton_id = 'ECU-13-MONTECRISTI', proc.circuito_id = 'GAP_10PCT',
            proc.capa_qnkc = 'C4'
        WITH proc
        MATCH (sp:C3ServicioPublico {id: 'SP_G10P_MCR'})
        MERGE (sp)-[:SE_EJECUTA_EN]->(proc)
        """, **p)

    # C5 — Evidencias
    evidencias_gap = [
        {
            "id": "EVD_G10P_01_MCR",
            "tipo": "documento_presupuestario",
            "descripcion": "Cédula presupuestaria GADMCM — partidas GAP",
            "obligatoria": True,
            "fuente": "SIGEF",
            "vinculo_ack": "COOTAD_249",
        },
        {
            "id": "EVD_G10P_02_MCR",
            "tipo": "registro_administrativo",
            "descripcion": "Registro beneficiarios Patronato por grupo prioritario",
            "obligatoria": True,
            "fuente": "Patronato",
            "vinculo_ack": "CE_35",
        },
        {
            "id": "EVD_G10P_03_MCR",
            "tipo": "registro_administrativo",
            "descripcion": "Nómina GADMCM — 4% inclusión laboral discapacidad",
            "obligatoria": True,
            "fuente": "SIGEF",
            "vinculo_ack": "LOD_47",
        },
        {
            "id": "EVD_G10P_04_MCR",
            "tipo": "acta_institucional",
            "descripcion": "Actas JCPD — medidas protección NNA",
            "obligatoria": True,
            "fuente": "JCPD",
            "vinculo_ack": "CONA_207",
        },
        {
            "id": "EVD_G10P_05_MCR",
            "tipo": "publicacion_transparencia",
            "descripcion": "Portal LOTAIP — programas Patronato",
            "obligatoria": True,
            "fuente": "LOTAIP",
            "vinculo_ack": "LOTAIP_19_6",
        },
        {
            "id": "EVD_G10P_06_MCR",
            "tipo": "informe_tecnico",
            "descripcion": "Informe gestión anual Patronato",
            "obligatoria": True,
            "fuente": "Patronato",
            "vinculo_ack": "COOTAD_302",
        },
        {
            "id": "EVD_G10P_07_MCR",
            "tipo": "documento_presupuestario",
            "descripcion": "POA Patronato 2026",
            "obligatoria": False,
            "fuente": "Patronato",
            "vinculo_ack": "COOTAD_249",
        },
    ]
    for e in evidencias_gap:
        run(session, """
        MERGE (ev:C5Evidencia {id: $id})
        SET ev.tipo = $tipo, ev.descripcion = $descripcion,
            ev.obligatoria = $obligatoria, ev.fuente = $fuente,
            ev.vinculo_ack = $vinculo_ack,
            ev.canton_id = 'ECU-13-MONTECRISTI', ev.circuito_id = 'GAP_10PCT',
            ev.capa_qnkc = 'C5'
        """, **e)

    # Conectar evidencias a procesos
    ev_proc_map = {
        "EVD_G10P_01_MCR": "PRO_G10P_01_MCR",
        "EVD_G10P_02_MCR": "PRO_G10P_02_MCR",
        "EVD_G10P_03_MCR": "PRO_G10P_03_MCR",
        "EVD_G10P_04_MCR": "PRO_G10P_04_MCR",
        "EVD_G10P_05_MCR": "PRO_G10P_06_MCR",
        "EVD_G10P_06_MCR": "PRO_G10P_06_MCR",
        "EVD_G10P_07_MCR": "PRO_G10P_01_MCR",
    }
    for ev_id, proc_id in ev_proc_map.items():
        run(session, """
        MATCH (proc:C4Proceso {id: $proc_id})
        MATCH (ev:C5Evidencia {id: $ev_id})
        MERGE (proc)-[:GENERA]->(ev)
        """, proc_id=proc_id, ev_id=ev_id)

    # C6 — Controles
    controles_gap = [
        {
            "id": "CTL_G10P_01_MCR",
            "nombre": "CGE — Auditoría Cumplimiento COOTAD_249",
            "organo": "CGE",
            "tipo": "financiero",
        },
        {
            "id": "CTL_G10P_02_MCR",
            "nombre": "MIES — Control Programas Sociales",
            "organo": "MIES",
            "tipo": "regulatorio",
        },
        {
            "id": "CTL_G10P_03_MCR",
            "nombre": "DPE — Defensoría del Pueblo",
            "organo": "DPE",
            "tipo": "defensa_derechos",
        },
        {
            "id": "CTL_G10P_04_MCR",
            "nombre": "CPCCS — Control Social y Rendición de Cuentas",
            "organo": "CPCCS",
            "tipo": "ciudadano",
        },
        {
            "id": "CTL_G10P_05_MCR",
            "nombre": "JCPD — Concejo de Derechos Cantonal",
            "organo": "JCPD",
            "tipo": "institucional_local",
        },
    ]
    for ctrl in controles_gap:
        run(session, """
        MERGE (ctl:C6Control {id: $id})
        SET ctl.nombre = $nombre, ctl.organo = $organo, ctl.tipo = $tipo,
            ctl.canton_id = 'ECU-13-MONTECRISTI', ctl.circuito_id = 'GAP_10PCT',
            ctl.capa_qnkc = 'C6'
        WITH ctl
        MATCH (ev:C5Evidencia {id: 'EVD_G10P_01_MCR'})
        MERGE (ev)-[:CONTROLADA_POR]->(ctl)
        """, **ctrl)

    # C7 — Observabilidad
    obs_gap = [
        {
            "id": "OBS_G10P_01_MCR",
            "descripcion": "SIGEF — ejecución partidas GAP",
            "frecuencia": "mensual",
            "fuente_ack": "COOTAD_249",
        },
        {
            "id": "OBS_G10P_02_MCR",
            "descripcion": "Portal LOTAIP — programas sociales Patronato",
            "frecuencia": "trimestral",
            "fuente_ack": "LOTAIP_19_6",
        },
        {
            "id": "OBS_G10P_03_MCR",
            "descripcion": "Rendición de cuentas anual — Dom12",
            "frecuencia": "anual",
            "fuente_ack": "COOTAD_302",
        },
        {
            "id": "OBS_G10P_04_MCR",
            "descripcion": "Nómina GADMCM — 4% inclusión discapacidad",
            "frecuencia": "anual",
            "fuente_ack": "LOD_47",
        },
    ]
    for obs in obs_gap:
        run(session, """
        MERGE (o:C7Observabilidad {id: $id})
        SET o.descripcion = $descripcion, o.frecuencia = $frecuencia,
            o.fuente_ack = $fuente_ack,
            o.canton_id = 'ECU-13-MONTECRISTI', o.circuito_id = 'GAP_10PCT',
            o.capa_qnkc = 'C7'
        WITH o
        MATCH (ctl:C6Control {id: 'CTL_G10P_01_MCR'})
        MERGE (ctl)-[:EXPONE_A]->(o)
        """, **obs)

    # C8 — Indicadores
    indicadores_gap = [
        {
            "id": "IND_G10P_01_MCR",
            "nombre": "Cumplimiento Asignación 10% Presupuesto GAP",
            "formula": "(partida_GAP_codificada / presupuesto_GAD_no_salarial_codificado) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 10",
            "umbral_rojo": "< 7",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_G10P_02_MCR",
            "nombre": "Cobertura Adultos Mayores Atendidos",
            "formula": "(adultos_mayores_atendidos / poblacion_adultos_mayores) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 30",
            "umbral_rojo": "< 15",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_G10P_03_MCR",
            "nombre": "Inclusión Laboral Discapacidad GADMCM (4%)",
            "formula": "(servidores_discapacidad / total_servidores) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 4",
            "umbral_rojo": "< 2",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_G10P_04_MCR",
            "nombre": "Ejecución Presupuestaria Patronato Municipal — Ti_Patronato",
            "formula": "(Devengado_G7+G8_Patronato / Codificado_G7+G8_Patronato) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 85",
            "umbral_rojo": "< 70",
            "estado_dato": "confirmado",
            "valor_linea_base": 35.03,
            "serie_2023": 35.03,
            "serie_2024": 53.77,
            "serie_2025": 50.0,
            "fuente_dato": "Gold Master SIAP-ICPI v5.5_TGI — H07b_Ti_INVERSIÓN",
        },
        {
            "id": "IND_G10P_05_MCR",
            "nombre": "Programas NNA con JCPD Operativa",
            "formula": "binario: JCPD_operativa + medidas_proteccion_dictadas_anio",
            "unidad": "binario_conteo",
            "umbral_verde": "JCPD operativa Y medidas > 0",
            "umbral_rojo": "JCPD no operativa",
            "estado_dato": "pendiente_validacion",
        },
    ]
    for ind in indicadores_gap:
        run(session, """
        MERGE (i:C8Indicador {id: $id})
        SET i += $props,
            i.canton_id = 'ECU-13-MONTECRISTI',
            i.circuito_id = 'GAP_10PCT',
            i.dominio_tgi = 'Dom12',
            i.capa_qnkc = 'C8'
        WITH i
        MATCH (o:C7Observabilidad {id: 'OBS_G10P_01_MCR'})
        MERGE (o)-[:MIDE]->(i)
        """, id=ind["id"], props={k: v for k, v in ind.items() if k != "id"})

    # C9 — Resultados Territoriales
    resultados_gap = [
        {
            "id": "RES_G10P_01_MCR",
            "indicador_ref": "IND_G10P_01_MCR",
            "nombre": "Ratio COOTAD_249 — Asignación GAP 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 20.84,
            "valor_devengado_pct": 14.19,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "calculado",
            "semaforo": "VERDE",
            "fuente_documental": "SIGEF cédulas reales: GAD dic-2025 anual + Patronato nov-2025",
            "interpretacion": (
                "GAD asigna 20.84% (2.08x el mínimo legal 10%). "
                "EL PROBLEMA NO ES LA ASIGNACION. El problema es la ejecución Ti=50%."
            ),
        },
        {
            "id": "RES_G10P_02_MCR",
            "indicador_ref": "IND_G10P_02_MCR",
            "nombre": "Cobertura Adultos Mayores 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "observado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "Registro beneficiarios Patronato / INEC 2022",
            "interpretacion": "Requiere datos Patronato RDC 2025",
        },
        {
            "id": "RES_G10P_03_MCR",
            "indicador_ref": "IND_G10P_03_MCR",
            "nombre": "Inclusión Laboral Discapacidad GADMCM 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "calculado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "Nómina GADMCM SIGEF + CONADIS",
            "interpretacion": "Requiere cruce nómina GADMCM x registro CONADIS",
        },
        {
            "id": "RES_G10P_04_MCR",
            "indicador_ref": "IND_G10P_04_MCR",
            "nombre": "Ti_Patronato_2025 — Ejecución Inversión Patronato",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 50.0,
            "periodo": "2025",
            "estado_dato": "confirmado",
            "naturaleza_valor": "calculado",
            "semaforo": "ROJO",
            "fuente_documental": "Gold Master SIAP-ICPI v5.5_TGI — H07b_Ti_INVERSIÓN fila 18",
            "interpretacion": (
                "Patronato ejecutó solo el 50% de su presupuesto de inversión en 2025. "
                "Serie 2023->2024->2025: 35%->54%->50% — mejora lenta, persistentemente ROJO. "
                "$2,048,280 no ejecutados no llegan a grupos prioritarios. "
                "COOTAD_249 cumplido en PAPEL pero no en TERRITORIO."
            ),
            "norma_base": "COOTAD_249",
            "g73_programas": 29.7,
        },
        {
            "id": "RES_G10P_05_MCR",
            "indicador_ref": "IND_G10P_05_MCR",
            "nombre": "JCPD Operativa Montecristi 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "observado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "Actas JCPD Montecristi / MIES",
            "interpretacion": "Verificar si JCPD operativa con medidas dictadas",
        },
    ]
    for res in resultados_gap:
        run(session, """
        MERGE (r:C9ResultadoTerritorial {id: $id})
        SET r += $props,
            r.canton_id = 'ECU-13-MONTECRISTI',
            r.circuito_id = 'GAP_10PCT',
            r.capa_qnkc = 'C9'
        WITH r
        MATCH (i:C8Indicador {id: $indicador_ref})
        MERGE (i)-[:REGISTRA]->(r)
        """, id=res["id"], indicador_ref=res["indicador_ref"],
            props={k: v for k, v in res.items() if k not in ("id", "indicador_ref") and v is not None})

    print("    GAP_10PCT: Canton + 6ACK + 1C3 + 6C4 + 7C5 + 5C6 + 4C7 + 5C8 + 5C9 cargados")


# ============================================================
# BLOQUE 2 — CIRCUITO AGUA_POTABLE
# ============================================================

def load_agua_potable(session):
    print("\n  Cargando AGUA_POTABLE...")

    # C3
    run(session, """
    MERGE (sp:C3ServicioPublico {id: 'SP_AGPT_MCR'})
    SET sp.nombre = 'Agua Potable Municipal — Montecristi',
        sp.circuito_id = 'AGUA_POTABLE',
        sp.canton_id = 'ECU-13-MONTECRISTI',
        sp.dominio_tgi = 'Dom04',
        sp.modalidad = 'directa',
        sp.capa_qnkc = 'C3',
        sp.qtmp_id = 'QTMP_AGUA_POTABLE_MCR'
    WITH sp
    MATCH (c:Canton {id: 'ECU-13-MONTECRISTI'})
    MERGE (sp)-[:ANCLADO_EN]->(c)
    WITH sp
    MATCH (ack:Atom {id: 'CE_264'})
    MERGE (ack)-[:MATERIALIZA_VIA]->(sp)
    WITH sp
    MATCH (ack2:Atom {id: 'CE_12'})
    MERGE (ack2)-[:FUNDA]->(sp)
    """)

    # C4
    procesos_agua = [
        ("PRO_AGPT_01_MCR", "Captación y Tratamiento de Agua", "operativo"),
        ("PRO_AGPT_02_MCR", "Distribución y Presión de Red", "operativo"),
        ("PRO_AGPT_03_MCR", "Control de Calidad del Agua Potable", "control_interno"),
        ("PRO_AGPT_04_MCR", "Gestión Comercial — Catastro y Facturación", "administrativo"),
        ("PRO_AGPT_05_MCR", "Mantenimiento y Rehabilitación de Red", "operativo"),
    ]
    for pid, nombre, tipo in procesos_agua:
        run(session, """
        MERGE (proc:C4Proceso {id: $id})
        SET proc.nombre = $nombre, proc.tipo = $tipo, proc.estado = 'activo',
            proc.canton_id = 'ECU-13-MONTECRISTI', proc.circuito_id = 'AGUA_POTABLE',
            proc.capa_qnkc = 'C4'
        WITH proc
        MATCH (sp:C3ServicioPublico {id: 'SP_AGPT_MCR'})
        MERGE (sp)-[:SE_EJECUTA_EN]->(proc)
        """, id=pid, nombre=nombre, tipo=tipo)

    # C8 — Indicadores (incluyendo el CRÍTICO: cobertura 34.9%)
    indicadores_agua = [
        {
            "id": "IND_AGPT_01_MCR",
            "nombre": "Cobertura de Agua Potable",
            "formula": "(hogares_con_agua_potable / total_hogares_canton) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 90",
            "umbral_amarillo": ">= 70 y < 90",
            "umbral_rojo": "< 70",
            "estado_dato": "confirmado",
            "meta_pdot_2027": 42.38,
        },
        {
            "id": "IND_AGPT_02_MCR",
            "nombre": "Continuidad del Servicio (horas/día promedio)",
            "formula": "promedio_horas_servicio_dia_por_zona",
            "unidad": "horas_por_dia",
            "umbral_verde": ">= 20",
            "umbral_rojo": "< 12",
            "estado_dato": "confirmado",
        },
        {
            "id": "IND_AGPT_03_MCR",
            "nombre": "Cumplimiento Norma Calidad INEN 1108",
            "formula": "(parametros_dentro_norma / total_parametros) x 100",
            "unidad": "porcentaje",
            "umbral_verde": "= 100",
            "umbral_rojo": "< 95",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_AGPT_04_MCR",
            "nombre": "Ejecución Presupuestaria Inversión Agua Potable",
            "formula": "(devengado_agua / codificado_agua) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 85",
            "umbral_rojo": "< 70",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_AGPT_05_MCR",
            "nombre": "Coincidencia PAC-Participativo (agua potable)",
            "formula": "(proyectos_agua_PAC_en_participativo / total_agua_priorizados) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 80",
            "umbral_rojo": "< 50",
            "estado_dato": "pendiente_validacion",
        },
    ]
    for ind in indicadores_agua:
        run(session, """
        MERGE (i:C8Indicador {id: $id})
        SET i += $props,
            i.canton_id = 'ECU-13-MONTECRISTI',
            i.circuito_id = 'AGUA_POTABLE',
            i.dominio_tgi = 'Dom04',
            i.capa_qnkc = 'C8'
        """, id=ind["id"], props={k: v for k, v in ind.items() if k != "id"})

    # C9 — Resultados (los 2 confirmados son críticos)
    resultados_agua = [
        {
            "id": "RES_AGPT_01_MCR",
            "indicador_ref": "IND_AGPT_01_MCR",
            "nombre": "Cobertura Agua Potable — Montecristi 2022",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 34.9,
            "unidad": "porcentaje_viviendas_red_publica",
            "periodo": "2022",
            "estado_dato": "confirmado",
            "naturaleza_valor": "observado",
            "semaforo": "ROJO",
            "fuente_documental": "INEC Censo de Población y Vivienda 2022",
            "meta_pdot_lb_2023": 39.25,
            "meta_pdot_2027": 42.38,
            "norma_base": "CE_264",
            "interpretacion": (
                "34.9% viviendas con acceso a red pública. "
                "60.19% sin cobertura se abastece por tanqueros. "
                "Servicio continuo 24/7 = 0% en todo el cantón."
            ),
        },
        {
            "id": "RES_AGPT_02_MCR",
            "indicador_ref": "IND_AGPT_02_MCR",
            "nombre": "Continuidad Servicio 24/7 — Montecristi 2024",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 0,
            "unidad": "porcentaje_continuidad_24_7",
            "periodo": "2024",
            "estado_dato": "confirmado",
            "naturaleza_valor": "observado",
            "semaforo": "ROJO",
            "fuente_documental": "Dirección de Agua Potable GADMCM / PDOT Bicentenario 2023",
            "meta_pdot_2027": 10,
            "norma_base": "CE_264",
            "interpretacion": (
                "Ninguna zona del cantón recibe agua de forma continua. "
                "Montecristi + Aníbal San Andrés: 1 vez/semana. "
                "Colorado + Leónidas Proaño + General Eloy Alfaro: 1 vez cada 15 días."
            ),
        },
        {
            "id": "RES_AGPT_03_MCR",
            "indicador_ref": "IND_AGPT_03_MCR",
            "nombre": "Calidad INEN 1108 — Montecristi 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "observado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "MSP Zona 4 Manabí",
            "norma_base": "CE_264",
            "interpretacion": "Pendiente informes mensuales calidad agua",
        },
        {
            "id": "RES_AGPT_04_MCR",
            "indicador_ref": "IND_AGPT_04_MCR",
            "nombre": "Ejecución Inversión Agua 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "calculado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "SIGEF cédula presupuestaria 2025",
            "norma_base": "CE_264",
            "interpretacion": "Verificar partidas agua vs D3=59.85% promedio GAD",
        },
        {
            "id": "RES_AGPT_05_MCR",
            "indicador_ref": "IND_AGPT_05_MCR",
            "nombre": "Coincidencia PAC-Participativo Agua 2025",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": None,
            "periodo": "2025",
            "estado_dato": "pendiente_validacion",
            "naturaleza_valor": "calculado",
            "semaforo": "PENDIENTE",
            "fuente_documental": "Actas Asamblea Ciudadana vs PAC SERCOP",
            "norma_base": "CE_264",
            "interpretacion": "Cierra circuito H3 Dom08→Dom03",
        },
    ]
    for res in resultados_agua:
        run(session, """
        MERGE (r:C9ResultadoTerritorial {id: $id})
        SET r += $props,
            r.canton_id = 'ECU-13-MONTECRISTI',
            r.circuito_id = 'AGUA_POTABLE',
            r.capa_qnkc = 'C9'
        WITH r
        MATCH (i:C8Indicador {id: $indicador_ref})
        MERGE (i)-[:REGISTRA]->(r)
        """, id=res["id"], indicador_ref=res["indicador_ref"],
            props={k: v for k, v in res.items() if k not in ("id", "indicador_ref") and v is not None})

    print("    AGUA_POTABLE: 1C3 + 5C4 + 5C8 + 5C9 cargados (cobertura 34.9% ROJO, continuidad 0% ROJO)")


# ============================================================
# BLOQUE 3 — CIRCUITO EQUIDAD
# ============================================================

def load_equidad(session):
    print("\n  Cargando EQUIDAD...")

    # C3
    run(session, """
    MERGE (sp:C3ServicioPublico {id: 'SP_EQUD_MCR'})
    SET sp.nombre = 'Equidad Territorial de la Inversión Pública Cantonal — Montecristi',
        sp.circuito_id = 'EQUIDAD',
        sp.canton_id = 'ECU-13-MONTECRISTI',
        sp.dominio_tgi = 'Dom04',
        sp.dominio_tgi_secundario = 'Dom02',
        sp.dominio_tgi_terciario = 'Dom12',
        sp.modalidad = 'directa',
        sp.capa_qnkc = 'C3',
        sp.qtmp_id = 'QTMP_EQUIDAD_MCR'
    WITH sp
    MATCH (c:Canton {id: 'ECU-13-MONTECRISTI'})
    MERGE (sp)-[:ANCLADO_EN]->(c)
    WITH sp
    MATCH (ack:Atom {id: 'COOTAD_228'})
    MERGE (ack)-[:MATERIALIZA_VIA]->(sp)
    WITH sp
    MATCH (ack2:Atom {id: 'CE_274'})
    MERGE (ack2)-[:HABILITA]->(sp)
    """)

    # Parroquias del cantón
    parroquias = [
        ("ECU-13-MONTECRISTI-MCU", "Montecristi", "MCU", "urbana"),
        ("ECU-13-MONTECRISTI-LPL", "La Pila", "LPL", "rural"),
        ("ECU-13-MONTECRISTI-CLR", "Colorado", "CLR", "urbana"),
        ("ECU-13-MONTECRISTI-PRN", "Leonidas Proaño", "PRN", "urbana"),
        ("ECU-13-MONTECRISTI-ANS", "Aníbal San Andrés", "ANS", "urbana"),
        ("ECU-13-MONTECRISTI-GEA", "General Eloy Alfaro", "GEA", "urbana"),
        ("ECU-13-MONTECRISTI-ISM", "Isabel Muentes", "ISM", "urbana"),
    ]
    for par_id, nombre, short, tipo in parroquias:
        run(session, """
        MERGE (par:Parroquia {id: $id})
        SET par.nombre = $nombre, par.short = $short, par.tipo = $tipo,
            par.canton_id = 'ECU-13-MONTECRISTI'
        WITH par
        MATCH (c:Canton {id: 'ECU-13-MONTECRISTI'})
        MERGE (par)-[:PERTENECE_A]->(c)
        """, id=par_id, nombre=nombre, short=short, tipo=tipo)

    # C8 — Indicadores EQUIDAD
    indicadores_eq = [
        {
            "id": "IND_EQUD_01_MCR",
            "nombre": "IRS Cantonal — Índice de Redistribución Social",
            "formula": "(inversion_quintiles_pobres / inversion_total_canton) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 85",
            "umbral_amarillo": ">= 70 y < 85",
            "umbral_rojo": "< 70",
            "valor_actual": 79.7,
            "estado_dato": "confirmado",
            "semaforo_actual": "amarillo",
        },
        {
            "id": "IND_EQUD_02_MCR",
            "nombre": "Tasa de Inversión Rural vs Total",
            "formula": "(inversion_ejecutada_rural / inversion_total_ejecutada) x 100",
            "unidad": "porcentaje",
            "umbral_verde": "Diferencia < 5pp respecto a pct_poblacion_rural",
            "umbral_rojo": "Diferencia > 15pp (subinversión rural)",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_EQUD_03_MCR",
            "nombre": "Cumplimiento Metas PDOT Parroquiales",
            "formula": "promedio(cumplimiento_meta_parroquia_i) para parroquias rurales",
            "unidad": "porcentaje",
            "umbral_verde": ">= 70",
            "umbral_rojo": "< 50",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_EQUD_04_MCR",
            "nombre": "Brecha NBI Urbano-Rural",
            "formula": "NBI_parroquias_rurales_promedio - NBI_parroquia_urbana",
            "unidad": "puntos_porcentuales",
            "umbral_verde": "Brecha reduciéndose > 2pp vs período anterior",
            "umbral_rojo": "Brecha creciente",
            "valor_actual": 32.0,
            "estado_dato": "confirmado",
            "semaforo_actual": "rojo",
        },
        {
            "id": "IND_EQUD_05_MCR",
            "nombre": "Vinculación POA-PDOT (Equidad Territorial)",
            "formula": "(proyectos_poa_referencia_pdot_territorial / total_proyectos_poa) x 100",
            "unidad": "porcentaje",
            "umbral_verde": ">= 80",
            "umbral_rojo": "< 50",
            "estado_dato": "pendiente_validacion",
        },
        {
            "id": "IND_EQUD_06_MCR",
            "nombre": "Cobertura Rendición de Cuentas por Parroquia",
            "formula": "parroquias_con_rdc / total_parroquias_rurales_canton",
            "unidad": "fraccion",
            "umbral_verde": "= total parroquias rurales",
            "umbral_rojo": "< 50% parroquias rurales cubiertas",
            "estado_dato": "pendiente_validacion",
        },
    ]
    for ind in indicadores_eq:
        run(session, """
        MERGE (i:C8Indicador {id: $id})
        SET i += $props,
            i.canton_id = 'ECU-13-MONTECRISTI',
            i.circuito_id = 'EQUIDAD',
            i.dominio_tgi = 'Dom04',
            i.capa_qnkc = 'C8'
        """, id=ind["id"], props={k: v for k, v in ind.items() if k != "id"})

    # C9 — Resultados cantonales confirmados
    resultados_eq_canton = [
        {
            "id": "RES_EQUD_01_MCR",
            "indicador_ref": "IND_EQUD_01_MCR",
            "nombre": "IRS Montecristi — Línea Base",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 79.7,
            "periodo": "2022",
            "estado_dato": "confirmado",
            "naturaleza_valor": "derivado",
            "semaforo": "AMARILLO",
            "fuente_documental": "SNP / INEC — corpus QUIRA",
            "norma_base": "COOTAD_228",
            "interpretacion": (
                "79.7% inversión llega a sectores vulnerables. "
                "Gap 20.3% hacia equidad total. AMARILLO."
            ),
        },
        {
            "id": "RES_EQUD_04_MCR",
            "indicador_ref": "IND_EQUD_04_MCR",
            "nombre": "Brecha NBI Urbano vs Rural — Montecristi 2022",
            "nivel_territorial": "canton",
            "territorio": "Montecristi",
            "valor": 32.0,
            "nbi_urbano": 21.3,
            "nbi_rural": 53.3,
            "pobreza_multidim_urbana": 23.0,
            "pobreza_multidim_rural": 67.9,
            "periodo": "2022",
            "estado_dato": "confirmado",
            "naturaleza_valor": "calculado",
            "semaforo": "ROJO",
            "fuente_documental": "INEC Censo 2022 / PDOT Bicentenario págs. 316 y 375",
            "norma_base": "COOTAD_228",
            "interpretacion": (
                "Brecha 32pp (21.3% urbano vs 53.3% rural). "
                "Zona rural multiplica por 2.5x la pobreza NBI de zona urbana. "
                "Pobreza multidimensional: 67.9% rural vs 23.0% urbana."
            ),
        },
    ]
    for res in resultados_eq_canton:
        run(session, """
        MERGE (r:C9ResultadoTerritorial {id: $id})
        SET r += $props,
            r.canton_id = 'ECU-13-MONTECRISTI',
            r.circuito_id = 'EQUIDAD',
            r.capa_qnkc = 'C9'
        WITH r
        MATCH (i:C8Indicador {id: $indicador_ref})
        MERGE (i)-[:REGISTRA]->(r)
        """, id=res["id"], indicador_ref=res["indicador_ref"],
            props={k: v for k, v in res.items() if k not in ("id", "indicador_ref") and v is not None})

    # C9 parroquiales — NBI proxy (21 nodos, nivel 3)
    nbi_parroquial = [
        ("MCU", "Montecristi Urbano", 21.3, "provisional"),
        ("LPL", "La Pila", 53.3, "provisional"),
        ("CLR", "Colorado", 21.3, "provisional"),
        ("PRN", "Leonidas Proaño", 21.3, "provisional"),
        ("ANS", "Aníbal San Andrés", 21.3, "provisional"),
        ("GEA", "General Eloy Alfaro", 21.3, "provisional"),
        ("ISM", "Isabel Muentes", 21.3, "provisional"),
    ]
    for short, nombre, proxy_val, validez in nbi_parroquial:
        res_id = f"RES_EQUD_01_{short}"
        par_id = f"ECU-13-MONTECRISTI-{short}"
        run(session, """
        MERGE (r:C9ResultadoTerritorial {id: $res_id})
        SET r.nombre = $nombre,
            r.nivel_territorial = 'parroquia',
            r.territorio = $nombre,
            r.parroquia_id = $par_id,
            r.canton_id = 'ECU-13-MONTECRISTI',
            r.circuito_id = 'EQUIDAD',
            r.indicador_ref = 'IND_EQUD_01_MCR',
            r.valor_proxy = $proxy_val,
            r.estado_dato = 'pendiente_microdato',
            r.naturaleza_valor = 'proxy',
            r.proxy_validez = $validez,
            r.fuente_requerida = 'INEC_DPA_PARROQUIAL',
            r.capa_qnkc = 'C9'
        WITH r
        MATCH (canton_res:C9ResultadoTerritorial {id: 'RES_EQUD_01_MCR'})
        MERGE (canton_res)-[:DESAGREGA_EN]->(r)
        WITH r
        MATCH (par:Parroquia {id: $par_id})
        MERGE (r)-[:CORRESPONDE_A]->(par)
        """, res_id=res_id, nombre=nombre, par_id=par_id,
            proxy_val=proxy_val, validez=validez)

    print("    EQUIDAD: 7 parroquias + 1C3 + 6C8 + 2C9 cantonal (confirmados) + 7C9 parroquial (proxy)")


# ============================================================
# BLOQUE 4 — CADENA BAUTISMAL (ADR-010 — Express Path)
# ============================================================

def build_bautismal_chain(session):
    """
    Crea la cadena causal directa para la consulta bautismal (ADR-010):

    COOTAD_249 (C1)
        ↓ FUNDA
    SP_G10P_MCR (C3 — competencia/servicio)
        ↓ HABILITA → RES_G10P_01_MCR (asignación 20.84% VERDE)
        ↓ HABILITA → IND_G10P_04_MCR (Ti_Patronato 50% ROJO)
    IND_G10P_04_MCR
        ↓ EXPLICA
    RES_G10P_04_MCR (C9 — brecha Dom12 ROJO)

    Esta cadena express permite la consulta bautismal directa.
    La cadena completa C3→C4→C5→C6→C7→C8→C9 también existe
    pero requiere path traversal más largo.
    """
    print("\n  Construyendo cadena bautismal (ADR-010)...")

    # COOTAD_249 → FUNDA → SP_G10P_MCR (ya existe vía MATERIALIZA_VIA)
    # Añadir también relación FUNDA para claridad semántica ADR-010
    run(session, """
    MATCH (norm:Atom {id: 'COOTAD_249'})
    MATCH (sp:C3ServicioPublico {id: 'SP_G10P_MCR'})
    MERGE (norm)-[:FUNDA {descripcion: 'Norma obliga al GAD a asignar 10% para GAP'}]->(sp)
    """)

    # SP_G10P_MCR → HABILITA → RES_G10P_01_MCR (asignación verde)
    run(session, """
    MATCH (sp:C3ServicioPublico {id: 'SP_G10P_MCR'})
    MATCH (res1:C9ResultadoTerritorial {id: 'RES_G10P_01_MCR'})
    MERGE (sp)-[:HABILITA {
        descripcion: 'La norma habilita la asignación presupuestaria',
        valor_observado: '20.84% cod (VERDE — cumple piso legal 10%)'
    }]->(res1)
    """)

    # RES_G10P_01_MCR → HABILITA → IND_G10P_04_MCR (Ti_Patronato)
    run(session, """
    MATCH (res1:C9ResultadoTerritorial {id: 'RES_G10P_01_MCR'})
    MATCH (ind4:C8Indicador {id: 'IND_G10P_04_MCR'})
    MERGE (res1)-[:HABILITA {
        descripcion: 'La asignación habilita la ejecución — pero no la garantiza',
        paradoja: 'COOTAD_249 cumplido en codificado ≠ ejecución efectiva'
    }]->(ind4)
    """)

    # IND_G10P_04_MCR → EXPLICA → RES_G10P_04_MCR (brecha Dom12)
    run(session, """
    MATCH (ind4:C8Indicador {id: 'IND_G10P_04_MCR'})
    MATCH (res4:C9ResultadoTerritorial {id: 'RES_G10P_04_MCR'})
    MERGE (ind4)-[:EXPLICA {
        descripcion: 'Ti_Patronato=50% ROJO explica por qué la brecha Dom12 persiste',
        evidencia: 'G73_programas=29.7% (fracción del 50% que llega a programas sociales)',
        g73_programas: 29.7,
        mecanismo: '$2,048,280 no ejecutados del presupuesto GAP no llegan a grupos prioritarios'
    }]->(res4)
    """)

    # Relaciones inter-circuito (EQUIDAD explica brechas sectoriales)
    run(session, """
    MATCH (sp_equd:C3ServicioPublico {id: 'SP_EQUD_MCR'})
    MATCH (sp_agpt:C3ServicioPublico {id: 'SP_AGPT_MCR'})
    MERGE (sp_equd)-[:CONDICIONA {
        descripcion: 'Distribución territorial de inversión determina cobertura agua potable rural'
    }]->(sp_agpt)
    """)

    run(session, """
    MATCH (ind_irs:C8Indicador {id: 'IND_EQUD_01_MCR'})
    MATCH (ind_gap:C8Indicador {id: 'IND_G10P_01_MCR'})
    MERGE (ind_irs)-[:CORRELACION_CAUSAL {
        descripcion: 'GAP < 10% → inversión grupos vulnerables baja → IRS deteriora'
    }]->(ind_gap)
    """)

    print("    Cadena bautismal: COOTAD_249 -FUNDA-> SP_G10P -HABILITA-> RES_01(20.84% VERDE)")
    print("                     RES_01 -HABILITA-> IND_04(Ti=50% ROJO) -EXPLICA-> RES_04(ROJO)")
    print("    Paradoja causal registrada en el grafo.")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="QUIRA Sprint 2 — Neo4j QTMP Loader")
    parser.add_argument("--uri", default="bolt://localhost:7687", help="Neo4j URI")
    parser.add_argument("--user", default="neo4j", help="Neo4j username")
    parser.add_argument("--password", required=True, help="Neo4j password")
    parser.add_argument("--reset", action="store_true", help="Borrar todos los datos antes de cargar")
    args = parser.parse_args()

    print("=" * 60)
    print("QUIRA Gov — Sprint 2: Neo4j QTMP Loader")
    print(f"URI: {args.uri} | User: {args.user}")
    print("=" * 60)

    driver = get_driver(args.uri, args.user, args.password)

    try:
        test_connection(driver)
    except Exception as e:
        print(f"\nERROR: No se puede conectar a Neo4j: {e}")
        print("\nVerifica que Neo4j Desktop esté ejecutándose:")
        print("  1. Abrir Neo4j Desktop")
        print("  2. Crear un proyecto QUIRA (si no existe)")
        print("  3. Agregar una base de datos local (Neo4j 5.x)")
        print("  4. Iniciar la base de datos (botón Start)")
        print("  5. Verificar que el puerto Bolt sea 7687")
        print(f"\nPassword configurado: {args.password}")
        sys.exit(1)

    with driver.session() as session:

        if args.reset:
            print("\n  [RESET] Borrando datos existentes...")
            run(session, "MATCH (n) DETACH DELETE n")
            print("  Grafo limpiado.")

        # Índices para performance
        print("\n  Creando índices...")
        for label, prop in [
            ("Atom", "id"), ("Canton", "id"), ("C3ServicioPublico", "id"),
            ("C4Proceso", "id"), ("C5Evidencia", "id"), ("C6Control", "id"),
            ("C7Observabilidad", "id"), ("C8Indicador", "id"),
            ("C9ResultadoTerritorial", "id"), ("Parroquia", "id"),
        ]:
            try:
                run(session,
                    f"CREATE INDEX IF NOT EXISTS FOR (n:{label}) ON (n.{prop})")
            except Exception:
                pass

        # Bloque 0 — Cantón + ACK atoms
        print("\n  Cargando Canton ECU-13-MONTECRISTI...")
        run(session, CYPHER_CANTON)

        print("  Cargando ACK Atoms (corpus normativo)...")
        for atom in ACK_ATOMS:
            run(session, CYPHER_ATOM, **atom)
        print(f"    {len(ACK_ATOMS)} ACK atoms cargados")

        # Bloque 1 — GAP_10PCT
        load_gap_10pct(session)

        # Bloque 2 — AGUA_POTABLE
        load_agua_potable(session)

        # Bloque 3 — EQUIDAD
        load_equidad(session)

        # Bloque 4 — Cadena Bautismal
        build_bautismal_chain(session)

        # Verificación final
        print("\n" + "=" * 60)
        print("VERIFICACION — Conteo de nodos en el grafo:")
        labels_to_count = [
            "Canton", "Atom", "C3ServicioPublico", "C4Proceso",
            "C5Evidencia", "C6Control", "C7Observabilidad",
            "C8Indicador", "C9ResultadoTerritorial", "Parroquia",
        ]
        total = 0
        for label in labels_to_count:
            result = session.run(f"MATCH (n:{label}) RETURN count(n) AS cnt")
            cnt = result.single()["cnt"]
            total += cnt
            print(f"  {label}: {cnt}")
        print(f"  TOTAL NODOS: {total}")

        print("\n  Nodos C9 confirmados:")
        confirmed = session.run("""
            MATCH (r:C9ResultadoTerritorial {estado_dato: 'confirmado'})
            RETURN r.id, r.valor, r.semaforo, r.circuito_id
            ORDER BY r.circuito_id, r.id
        """)
        for rec in confirmed:
            print(f"    {rec['r.id']}: valor={rec['r.valor']} semaforo={rec['r.semaforo']}")

        print("\n" + "=" * 60)
        print("CARGA COMPLETADA")
        print("Ejecutar consulta bautismal:")
        print("  python neo4j_bautismal_query.py --uri " + args.uri +
              " --user " + args.user + " --password <password>")
        print("=" * 60)

    driver.close()


if __name__ == "__main__":
    main()
