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

# ── ESTADO DE UNA CIFRA PUBLICADA (D-009 · taxonomía del colega, 2026-09-03) ──
# La deuda NO es «hay números escritos a mano»: eso no está demostrado y sería
# una acusación, no una medición. La deuda es:
#
#     hay afirmaciones numéricas publicadas cuya relación con una fuente
#     vigente no está formalmente establecida.
#
# Curar una cifra es CLASIFICARLA, no reemplazarla. Sólo dos de estos siete
# estados son defecto; los demás son usos legítimos que hay que poder declarar.
CIFRA_AUTORIDAD = "deriva_de_una_fuente_canonica_vigente"
CIFRA_DERIVADA = "se_calcula_desde_datos_canonicos"
CIFRA_REFERENCIA = "ilustrativa_o_metodologica_declarada"
CIFRA_HISTORICA = "se_conserva_por_razon_documental"
CIFRA_DEMO = "valor_explicitamente_demostrativo"
CIFRA_SIN_TRAZA = "no_se_pudo_establecer_su_origen"        # ← defecto
CIFRA_CONTRADICTORIA = "contradice_la_fuente_vigente"      # ← defecto grave

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
         estado="RESUELTA 2026-09-01 · config resuelve por sufijo _TGI y 9 "
                "módulos migrados. ⚠️ INCOMPLETA hasta el 2026-09-03: la "
                "destapó una pregunta sobre el IGP. Quedaban CINCO "
                "literales, y el peor estampaba `version_excel: v5.5_TGI` "
                "en el `_meta` del snapshot —la próxima regeneración habría "
                "declarado un origen que no era el suyo—. Además "
                "`test_recorrido_icpi` abría v5.5 a mano y, como esa "
                "versión sólo vive en `historial_gold_master/`, **las 4 "
                "pruebas del recorrido del ICPI se saltaban en silencio**: "
                "la cifra madre llevaba sin verificarse contra el motor. "
                "Un `except Exception: return None` convertía «no pude "
                "abrirlo» en «no está». Cerrada con ataque que exige "
                "resolver la versión, midiendo la ASIGNACIÓN y no la "
                "mención —citar el nombre al explicar el caso es legítimo",
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
    dict(id="D-006", gravedad=FALSEA, capa="C1/C3", dueño="Javo",
         estado="RESUELTA 2026-09-02 · Y EL ENUNCIADO ERA OTRO. Medido antes de "
                "tocar: los 7 CNO-VIII son `participacion_y_control_social` "
                "entero —el canon de d08, declarado ENTRABLE en BOOT— y todo el "
                "bloque VIII está en `propuesta`. PENDIENTE + DECLARADO ≠ DEUDA: "
                "siete cadenas sin RO en un dominio sin curar es el estado "
                "esperado. La deuda estaba al lado y era peor: d08 CONSUMÍA "
                "`RO-VIII-003` en `propuesta` y publicaba su umbral. Ahora pide "
                "la consumibilidad al puente; sin regla acreditada publica la "
                "medición y NO el veredicto. Los 7 siguen visibles: no se "
                "fabricó ninguna RO para hacer desaparecer el hallazgo",
         que="Enunciado original: «siete `CNO-VIII-00x` no son reclamados por "
             "ninguna RO». Enunciado real: `enrich_participacion.py` leía bien "
             "el YAML —vía canónica, no copia— pero tomaba `umbral_activacion: "
             "0.50` sin mirar `estado: propuesta` / `validada_por: null`, y el "
             "snapshot publicaba una señal ENCENDIDA (0,848 ≥ 0,50) sobre regla "
             "no acreditada. Además `p16_gobernanza` publicaba una nota con "
             "«48.33%» y el método de 3 componentes que Javo retiró el "
             "2026-07-29: 22 días contradiciendo al motor, que calcula 27,00.",
         ataque="test_d08_no_publica_un_veredicto_sobre_una_regla_no_acreditada",
         no_es="canon que no llegó a la etapa siguiente —eso era el enunciado "
               "viejo y se cayó al medirlo—. Tampoco es que falten siete reglas: "
               "fabricarlas para que un inventario dé cero habría sido peor que "
               "la deuda"),
    dict(id="D-007", gravedad=CIEGA, capa="C2", dueño="Javo",
         estado="RESUELTA 2026-09-02 · Javo autorizó tocar lo congelado con una "
                "condición —no dañar lo que funciona— y por eso NO se enganchó a "
                "ciegas: se replicó CI en clon limpio + venv virgen + el shell "
                "exacto de GitHub. Ahí aparecieron las 3 trampas que habrían "
                "dado un CI rojo el primer día: 3 pruebas exigían evidencia que "
                "`.gitignore:114` excluye por decisión (hoy la piden por fixture "
                "y se saltan diciendo por qué), `check_extraccion` salía VERDE "
                "diciendo «nada que verificar» (hoy devuelve 2 · no "
                "determinable), y `requirements.txt` no declara pytest/pyyaml/"
                "pdfplumber. ⚠️ Y LA SIMULACIÓN NO BASTÓ: el primer CI real "
                "encontró 3 más —sintaxis de Python 3.11, el clon que heredaba "
                "`ProyecT/` de la máquina, y la huella del canon que dependía "
                "del disco—. **CERRADA el 2026-09-02.** La API de GitHub registraba 427 ejecuciones históricas y NINGUNA con conclusión `success`; hoy registra ejecuciones consecutivas en verde. El estado que acredita NO es «todo verificado»: suite 674 PASS / 61 SKIP · gates 10 verificados / 1 no determinable / 0 con hallazgos. Y el verde NO acredita "
                "todo: lo saltado y lo no determinable se cuentan y se anuncian",
         que="Al cerrar D-004 apareció la misma falla un nivel arriba: de 12 "
             "gates en `scripts/ci/`, **sólo `check_health.py` se ejecuta** en "
             "un workflow, y `pytest` no es paso de ninguno — las 33 pruebas no "
             "corren en CI. Un gate ciego al menos corre; uno que no se ejecuta "
             "acredita cero hallazgos POR NO EXISTIR, y su verde es el silencio "
             "de nadie preguntando.",
         ataque="test_el_circuito_ejecuta_los_gates_y_la_suite",
         no_es="algo que yo pueda reparar: `.github/workflows/*` está congelado "
               "(Regla de Oro 5) y engancharlo es decisión de Javo. Tampoco es "
               "«enganchar los 11 de golpe»: eso daría un CI rojo de origen "
               "desconocido. Primero correr cada gate a mano, después enganchar "
               "el que ya esté verde"),
    dict(id="D-008", gravedad=CIEGA, capa="C2/C6", dueño="Javo",
         medicion="39 archivos detectados por el barrido → clasificación → 9 en "
                  "`app/viz/` excluidos CON motivo escrito · 3 en `_deprecated` "
                  "· 1 con los verdes oficiales de la ONU (`p11_ods`) · **25 "
                  "páginas vivas y ruteadas** que requieren curación. Las cifras "
                  "NO son intercambiables: decir «D-008 = 39 páginas» fabricaría "
                  "una precisión que la medición no sostiene (aviso del colega)",
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
    dict(id="D-010", gravedad=FALSEA, capa="C1/C4", dueño="Javo",
         que="Javo preguntó si el IGP está metodológicamente bien armado para "
             "representar la gobernanza participativa cantonal. Medido en el "
             "Gold Master v5.7 (`H20b`), aparecen DOS cosas distintas. "
             "**(1) ALCANCE**: el «Índice de Gobernanza Participativa» mide 2 "
             "componentes —Asamblea CPCCS y Presupuesto Participativo— y el "
             "canon de QUIRA modela 7 mecanismos (Sistema Cantonal, Asamblea, "
             "Consejo de Planificación, Audiencia Pública, PP, Cabildo Popular, "
             "Silla Vacía), que d08 documenta enteros. Es el patrón de D-001: "
             "un nombre que promete el universo sobre un alcance que es una "
             "parte. **(2) UN PENDIENTE ENTRA COMO CERO**: `IGP_2 = 0` con la "
             "nota «Actualizar desde H10b cuando PP 2026 esté disponible», y "
             "ese 0 pesa la mitad del promedio: IGP = (0,54 + 0)/2 = 0,27. "
             "Mientras tanto d08 tiene **191 demandas de PP 2026** medidas y "
             "trazadas. La ausencia de dato está funcionando como valor.",
         ataque="test_el_IGP_declara_su_alcance_y_no_computa_pendientes_como_cero",
         no_es="un error de cálculo: la fórmula hace exactamente lo que declara "
               "y `H20b` documenta el cambio metodológico con su fecha y su "
               "motivo. Tampoco es una acusación al GAD — al contrario: el "
               "hallazgo es que el índice puede estar penalizando al sujeto por "
               "un dato que QUIRA todavía no incorporó. Y NO se toca: la "
               "fórmula vive en el Gold Master, su corrección es cirugía sobre "
               "copia con evidencia (Regla de Oro 1) y la decide Javo"),
    dict(id="D-009", gravedad=FALSEA, capa="C6", dueño="Javo",
         medicion_2="⚠️ EL HALLAZGO YA EXISTÍA, DOCUMENTADO Y SIN ESCALAR. "
                    "`docs/architecture/AUDITORIA_MIGRACION_D1.5.md` lo tituló "
                    "«EL ENEMIGO: verdades simultáneas en lugares distintos», "
                    "hizo el mapa cajón→pantalla→fuente y señaló las 3 que "
                    "CONTRADICEN al motor (d05 Holding 68.7% vs ~17% · d08 IGP "
                    "27.98% · d12 PSG 12.83% vs 2.83%). Nunca llegó a este "
                    "registro. Una auditoría que no escala al mecanismo que "
                    "persigue las deudas es una nota que envejece — lo mismo "
                    "que este módulo existe para impedir.",
         caso_IGP_RESUELTO_EN_LA_FUENTE="⚠️ NO HABÍA TRES VALORES DEL MISMO "
             "ÍNDICE. Se fue al Gold Master —`H20b_IGP_GOBERNANZA_PARTIC`, "
             "v5.7_TGI, por la puerta canónica y sin recalcular— y la fuente lo "
             "resolvió: **27,00 es `IGP_Global` (B9), el índice VIGENTE 2026** = "
             "promedio de IGP_1 Asamblea CPCCS 0,54 e IGP_2 Presupuesto "
             "Participativo 0,00. **27,98 es `Ref_2025_IGP` (B11)**, una "
             "variable CANÓNICA DISTINTA con celda y rótulo propios "
             "«Gobernanza por Ocurrencia 2025». **48,33 es la composición "
             "obsoleta** previa a retirar IGP_3 (A8: «RETIRADO 2026-07-29 por "
             "decisión de Javo… es CONTROL SOCIAL d09, no participación d08 — "
             "frontera DEC-0004»). Luego 27,98 NO es un error: es un dato "
             "legítimo de otro año. Lo que puede estar mal es la ETIQUETA, y "
             "eso es §6-sexies: etiqueta incorrecta = número falso.",
         lo_que_ninguna_pantalla_puede_destruir="`H20b!B12`, textual: «La BAJA "
             "del indice NO es deterioro de gestion: es correccion de una "
             "composicion previa a la separacion d08/d09». Publicar 27,00 como "
             "caída frente a 48,33 imputaría al GAD un deterioro que no "
             "existe — lenguaje acusatorio por omisión de contexto (Regla 2).",
         clasificacion_de_las_4_superficies="`p11_ods:131` HISTÓRICA con "
             "etiqueta incompleta —el código declara `IGP_REF_2025 · fuente "
             "H73` en un comentario y el texto publicado omite el año—. "
             "`p14_eficiencia:18` DEMO. `p9_sat:46` DEMO con etiqueta "
             "CONTRADICTORIA: dato de 2025 dentro de «RDC 2026». "
             "`p16_gobernanza:278` CONTRADICTORIA: rotula «referencia 2025» un "
             "`indices['IGP']['valor']` que es la variable vigente. Esta última "
             "no exige decidir canon —exige pedir la variable correcta— pero "
             "cuál de las dos debe mostrar esa pantalla es diseño de dominio y "
             "lo decide Javo.",
         que="El patrón que el colega nombró tras el «48,33 %»: **derivado "
             "narrativo desacoplado de la fuente canónica**. Medido para saber "
             "si fue aislado — no lo fue: **11 superficies vivas publican cifras "
             "de dominio escritas dentro de su texto**. «Salud "
             "presupuestaria 14.58% bajo umbral COOTAD 65%», «Participación "
             "27.98%», «Cobertura agua 34.9% → 65% al 2027», «Fidelidad 72.73%: "
             "48/66 promesas CNE». Ninguna declara su fuente, y el 48,33 "
             "demostró qué pasa entonces: la cifra no se entera de que su fuente "
             "cambió, y sigue publicándose 22 días.",
         ataque="test_las_cifras_de_dominio_en_texto_publicado_estan_contadas",
         medicion="Se cuentan SUPERFICIES, no cadenas: el conteo de cadenas dio "
                  "23 en Windows y 25 en el runner —mismo código, mismo filtro— "
                  "porque los tokens STRING no son estables entre plataformas. "
                  "Una medición cuyo resultado depende del sistema operativo no "
                  "sostiene una cifra pública, ni siquiera la de una deuda",
         como_se_cura="CLASIFICANDO cada cifra, no reemplazándola: autoridad · "
                      "derivada · referencia · histórica · demo · sin traza · "
                      "contradictoria. Sólo las dos últimas son defecto. El "
                      "48,33 era CONTRADICTORIA —publicaba un método retirado— "
                      "y por eso se reparó; las demás exigen mirar una por una",
         no_es="un puñado de cifras falsas. NO se afirma que ninguna esté mal: se afirma "
               "que ninguna puede saberlo. Cada una exige determinar si es dato "
               "vivo, referencia histórica legítima o resto de la maqueta —y esa "
               "distinción es curación de dominio, no un reemplazo masivo. "
               "Tampoco cubre CSS ni cifras enteras (100%, 65%): el barrido se "
               "limitó a decimales dentro de prosa de dominio para no inflar el "
               "hallazgo con falsos positivos"),
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
