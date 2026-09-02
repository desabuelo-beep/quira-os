"""
app/agents/deuda.py — lo que falta, con su ataque al lado
================================================================================
POR QUÉ EXISTE (2026-09-01). La macro-auditoría de C0→C3 produjo una docena de
hallazgos y **ninguno se reparó**: era la disciplina correcta —medir antes de
tocar— pero deja una pregunta abierta que nadie puede responder de memoria:
*¿qué está abierto, con qué gravedad, y en qué orden se cierra?*

Javo, al confirmar la deuda de las metas:

> *«no se puede trabajar sobre la realidad del GAD con una muestra de 25 metas
> […] no debemos dejar ninguna deuda; estamos en construcción y todo lo cerrado
> debe subsanarse si tocara el caso.»*

LA REGLA QUE HACE ÚTIL ESTE REGISTRO, y sale de toda la sesión:

    Una deuda no se declara sola: viene con la prueba que la fija.

Sin ataque asociado, una deuda es una nota que envejece —y este sistema ya sabe
lo que pasa con las notas—. Con ataque, el día que se subsane **la prueba
falla**, y ese fallo es la señal de progreso. Por eso `test_toda_deuda_tiene_su
_ataque` verifica que cada entrada nombre una prueba que existe de verdad.

⚠️ Y NO TODO PENDIENTE ES DEUDA. La sesión demostró tres estados legítimos que
no lo son: `demostrado`, `no_determinable` y `excepción declarada`. Once ADR sin
validador son anteriores a la norma que lo exige; 31 artefactos con el RUC
previo son correctos para su época; d01 y d08 leyendo el Excel directo son
excepciones con decisión de Javo.

    PENDIENTE + DECLARADO  ≠  DEUDA
    PENDIENTE + NO DECLARADO  =  DEUDA

Aquí sólo entra lo segundo, más lo que el propio dueño del dominio declaró deuda.

Dylus Lab © 2026
"""
from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# Gravedad, y su criterio — no una escala de sensaciones.
FALSEA = "puede_falsear_una_cifra_publica"      # produce un número que engaña
DESACOPLA = "el_canon_no_gobierna_al_motor"     # la regla existe y no se aplica
CIEGA = "un_instrumento_no_ve_su_territorio"    # cobertura declarada de menos
DESFASA = "el_canon_dice_algo_que_el_codigo_no" # divergencia declarado/real

# El estado que este registro NO puede negar: que existan deudas no encontradas.
# Sin una constante que lo nombre, «6 deudas» se leería como «hay 6», y este
# registro recoge — no barre. La Capa 0 lo detectó en cuanto nació el módulo.
SIN_BARRER = "sin_barrer_puede_haber_mas"

_DEUDAS = (
    dict(id="D-001", gravedad=FALSEA, capa="C1/C3", dueño="Javo",
         que="El ICPI se declara `ICPI_GLOBAL_SISTEMA` y se calcula sobre 25 "
             "metas que fueron una muestra inicial. `H04!B7` las etiqueta "
             "`Total_Metas_PDOT`. El trabajo de ampliación al total no aparece "
             "en v5.5, v5.7 ni v6.0, y Javo confirma que no lo encuentra.",
         ataque="test_el_parametro_llamado_total_es_el_tamano_de_la_muestra",
         no_es="un error de cálculo: el motor hace lo que dice y los "
               "ponderadores suman 1.0000 sobre esas 25. Es el ALCANCE lo que "
               "no corresponde al nombre"),
    dict(id="D-002", gravedad=DESFASA, capa="C1", dueño="Javo",
         estado="RESUELTA 2026-09-01 · config resuelve por sufijo _TGI y "
                "9 módulos migrados; cifras verificadas idénticas antes de migrar",
         que="BOOT declara `v5.7_TGI` y el código abre `v5.5_TGI` en 24 sitios. "
             "Las dos versiones coinciden hoy en metas e ICPI, así que el "
             "desfase no cambia ninguna cifra — todavía.",
         ataque="test_el_motor_lee_la_version_que_el_canon_declara",
         no_es="una divergencia de resultados: es una divergencia de referencia "
               "que se volverá de resultados en cuanto las versiones difieran"),
    dict(id="D-003", gravedad=DESACOPLA, capa="C1", dueño="Javo",
         estado="RESUELTA 2026-09-01 · catálogo recompilado, estado derivado, "
                "sellado por Javo con caducidad atada al canon, y lector "
                "verificable con 11 ataques. El puente ya se puede cruzar: "
                "falta conectar un consumidor, que es trabajo de dominio",
         que="D-003 NO era «el motor no consulta la BRN». Medido: el catálogo "
             "estaba desfasado —9 piezas de d07 con estado anterior— y se "
             "declaraba `propuesta` por un literal inmóvil. Cruzarlo habría "
             "acoplado nueve motores a un artefacto caducado.",
         ataque="test_d07_es_el_unico_que_carga_el_yaml_de_su_regla",
         no_es="negligencia de cuatro dominios: es una vía canónica construida "
               "que nadie usa"),
    dict(id="D-004", gravedad=CIEGA, capa="C2", dueño="Javo",
         estado="RESUELTA 2026-09-02 · el gate dejó de enumerar carpetas y "
                "deriva su universo de `RAIZ.rglob`, restando `_EXCLUIDOS` con "
                "motivo escrito al lado. Aparecieron 9 hallazgos donde veía 0: "
                "4 excluidos por decisión declarada —`config.py` ES la puerta, "
                "`tests/` cita rutas para vetarlas—, 1 reparado en el acto "
                "(`data/obsidian_bridge.py` duplicaba `config.VAULT_DIR`) y 3 "
                "en `sentinel/`, territorio legado. El tope subió de 0 a 3 y NO "
                "es regresión: el sistema no se ató más a una máquina, el "
                "instrumento dejó de ser ciego",
         que="`check_portabilidad.py` reporta «0 rutas fijas · objetivo "
             "cumplido» sobre `AMBITOS` que no incluye `sentinel/` —73 archivos "
             "con tres rutas absolutas al disco de una persona—. Su patrón SÍ "
             "las detectaría: falla el universo, no el detector.",
         ataque="test_el_gate_de_portabilidad_deriva_su_universo",
         no_es="una infracción demostrada: `AMBITOS` no declara motivo, así que "
               "no se puede saber si la exclusión fue decisión u omisión"),
    dict(id="D-005", gravedad=FALSEA, capa="C1", dueño="Javo",
         estado="RESUELTA 2026-09-01 · d02 dejó de tener el umbral y lo pide al "
                "puente BRN verificable. No se detecta mejor la copia caduca: "
                "no puede haberla. Cero copias caducas en todo el sistema",
         que="`enrich_presupuesto.py` fija el umbral 65 en cuatro lugares y "
             "`RO-IV-001` declara 65 hasta 2026-12-31 y **70 desde "
             "2027-01-01**. Hoy coinciden.",
         ataque="test_ataque_una_copia_caduca_se_detecta_antes_de_su_fecha",
         no_es="un error actual: es una obsolescencia con fecha conocida"),
    dict(id="D-006", gravedad=DESACOPLA, capa="C1", dueño="Javo",
         que="Siete `CNO-VIII-00x` no son reclamados por ninguna RO: cadenas "
             "normativas modeladas que nunca llegaron a regla operativa.",
         ataque="test_ataque_un_cno_sin_RO_no_puede_desaparecer_del_inventario",
         no_es="canon incorrecto: es canon que no llegó a la etapa siguiente"),
    dict(id="D-007", gravedad=CIEGA, capa="C2", dueño="Javo",
         que="Al cerrar D-004 apareció la misma falla un nivel arriba: de 12 "
             "gates en `scripts/ci/`, **sólo `check_health.py` se ejecuta** en "
             "un workflow, y `pytest` no es paso de ninguno — las 33 pruebas no "
             "corren en CI. Un gate ciego al menos corre; uno que no se ejecuta "
             "acredita cero hallazgos POR NO EXISTIR, y su verde es el silencio "
             "de nadie preguntando.",
         ataque="test_ataque_un_gate_que_no_se_ejecuta_no_acredita_nada",
         no_es="algo que yo pueda reparar: `.github/workflows/*` está congelado "
               "(Regla de Oro 5) y engancharlo es decisión de Javo. Tampoco es "
               "«enganchar los 11 de golpe»: eso daría un CI rojo de origen "
               "desconocido. Primero correr cada gate a mano, después enganchar "
               "el que ya esté verde"),
    dict(id="D-008", gravedad=CIEGA, capa="C2/C6", dueño="Javo",
         que="`check_sistema_visual` vigila 5 ambientes + `umi.py` y ahí no hay "
             "verde. Pero esos ambientes ENRUTAN a 25 páginas vivas que sí lo "
             "usan —`p_ejecutivo`, `p_command_center`, `p_concejo`, `m_rdc`…—. "
             "El gate protege la puerta y deja sin mirar las habitaciones. Ya le "
             "pasó el 2026-08-08 —cubría sólo `login_view` mientras `env_civic` "
             "usaba #22C55E en cinco sitios— y su propio comentario lo cuenta: "
             "«protegía la entrada y dejaba sin vigilar las pantallas donde la "
             "gente pasa el tiempo». Se amplió a los ambientes, que son otra vez "
             "la entrada. **Reincidencia del mismo defecto un nivel adentro.**",
         ataque="test_ataque_el_gate_visual_vigila_la_puerta_no_las_habitaciones",
         no_es="26 infracciones: `app/viz/` (9) está excluido CON motivo escrito "
               "—una rampa de color puede ser legítima— y `p11_ods` usa los "
               "verdes oficiales de Naciones Unidas, que son identidad ajena y "
               "no un juicio de «bien». Cada uno de los 25 exige decidir QUÉ "
               "dice ese verde, y eso es curación de dominio, no un barrido"),
)


def deudas() -> list[dict]:
    """El registro, con la prueba de cada una localizada en disco."""
    pruebas = {}
    for f in (RAIZ / "tests").glob("test_*.py"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        for d in _DEUDAS:
            if f"def {d['ataque']}(" in txt:
                pruebas[d["id"]] = f.relative_to(RAIZ).as_posix()
    return [{**d, "prueba_en": pruebas.get(d["id"], "")} for d in _DEUDAS]


def cobertura_de_deuda() -> dict:
    """Qué está abierto, con qué gravedad y con qué ataque lo fija."""
    filas = deudas()
    # ⚠️ ABIERTAS Y RESUELTAS SE DERIVAN, NO SE CUENTAN A MANO. La primera
    # versión afirmaba «ninguna reparada» en prosa fija y siguió diciéndolo con
    # cuatro ya cerradas: el mismo defecto que este registro persigue, dentro
    # del registro mismo.
    resueltas = [d["id"] for d in filas if d.get("estado", "").startswith("RESUELTA")]
    abiertas = [d["id"] for d in filas if d["id"] not in resueltas]
    por_gravedad: dict[str, list[str]] = {}
    for d in filas:
        if d["id"] in abiertas:
            por_gravedad.setdefault(d["gravedad"], []).append(d["id"])
    sin_ataque = [d["id"] for d in filas if not d["prueba_en"]]
    return {
        "deudas": filas,
        "abiertas": abiertas,
        "resueltas": resueltas,
        "por_gravedad": por_gravedad,
        "sin_ataque_localizado": sin_ataque,
        "exhaustividad": SIN_BARRER,
        "universo": {
            "que": "deudas declaradas de la macro-auditoría C0→C3",
            "donde": "app/agents/deuda.py, contrastado con tests/",
            "como": "SELECCIÓN DELIBERADA, no barrido: cada entrada la declara "
                    "quien la encontró y la fija una prueba. No pretende ser "
                    "exhaustiva y por eso se declara limitada (C0 · regla 1)",
            "hallados": len(filas),
            "mecanismo": {
                "tipo": "explicitamente_limitado",
                "operacion": "declaración",
                "por_que": "una deuda no se descubre barriendo: alguien la "
                           "encuentra, la declara y la ata a un ataque",
            },
            "exclusiones": [
                {"patron": "pendiente declarado", "motivo": "un pendiente con "
                 "constancia no es deuda: los ADR anteriores a ADR-035, los "
                 "artefactos con el RUC previo y las lecturas directas de d01/"
                 "d08 son legítimos y están declarados",
                 "autoridad": "criterio fijado con Javo, 2026-09-01"},
            ],
            "fuera_de_alcance": [
                "deudas que nadie ha encontrado todavía: este registro no barre, "
                "recoge",
                "las capas C4 a C7 —motores, Gold Master, productos, UI— no se "
                "han auditado: su ausencia aquí no significa que estén limpias",
            ],
        },
        "afirmacion_sostenible": _afirmar(filas, abiertas, resueltas, por_gravedad),
    }


def _afirmar(filas, abiertas, resueltas, por_gravedad) -> str:
    return (
        f"{len(filas)} deudas declaradas · {len(resueltas)} resueltas "
        f"({', '.join(resueltas) or '—'}) · {len(abiertas)} abiertas. " +
        " · ".join(f"{g}: {', '.join(ids)}" for g, ids in sorted(por_gravedad.items())) +
        ". Cada una nombra la prueba que la fija, así que el día que se subsane "
        "**la prueba falla** y ese fallo es la señal — así se cerraron D-002 a "
        "D-005, y así apareció D-007 al cerrar D-004. Lo que este registro NO "
        "dice es que no haya más: recoge lo encontrado, no barre el sistema, y "
        "las capas C4–C7 siguen sin auditar."
    )
