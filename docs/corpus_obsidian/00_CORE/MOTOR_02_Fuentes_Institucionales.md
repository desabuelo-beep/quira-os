---
name: "Motor QUIRA — Fuentes Institucionales"
description: "Mapa de las fuentes institucionales del Motor QUIRA: qué organismos del Estado ecuatoriano producen los datos que alimentan cada silo del SIAP-ICPI. La cadena de custodia entre la realidad y el score TGI."
tipo: motor-fuentes
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
fecha: "2026-05-17"
tags: [motor, fuentes, instituciones, esigef, sigad, sercop, inec, cpccs, cne, d1, d2, d3, d4, d5]
---

# Motor QUIRA — Fuentes Institucionales

> El TGI Score no nace de una opinión. Nace de datos que producen instituciones del Estado ecuatoriano con mandato legal para hacerlo. Esta nota mapea esa cadena: de la institución al dato, del dato al silo, del silo al score.

→ [[MOTOR_00_Arquitectura_Logica]] · [[MOTOR_01_Silos_Epistemicos]] · [[03_SIAP_ICPI_METHOD]]

---

## Mapa de Fuentes por Silo

### S1 · Silo Normatividad → D1

| Fuente | Institución | Qué produce | Mandato legal |
|--------|-------------|-------------|--------------|
| Registro Oficial | Asamblea / Presidencia | Marco legal vigente | Constitución Art. 132 |
| Resoluciones CPCCS | Consejo Participación Ciudadana | Obligaciones accountability | LOPC Art. 77 |
| Informes CGE | Contraloría General del Estado | Auditorías de cumplimiento | LOC Art. 31 |
| Normativa interna GAD | GADM Montecristi | Ordenanzas, reglamentos | COOTAD Art. 57 |
| Registro SERCOP | SERCOP | Procesos contratación vigentes | LOSNCP Art. 10 |

**Flujo al Motor:** El Motor lee la coherencia entre estos instrumentos — no verifica cada coma, sino si el sistema legal en que opera el GAD es internamente consistente y actualizado.

→ [[_Indice_Normativa]] · [[D1 Legalidad y Coherencia Normativa]]

---

### S2 · Silo Planificación → D2 (ICPI)

| Fuente | Institución | Qué produce | Mandato legal |
|--------|-------------|-------------|--------------|
| SIGAD | SNP / SETEPLAN | Reporte de metas PDyOT por ciclo | COPFP Art. 50 |
| PDyOT 2023-2027 | GADM Montecristi | 25 metas estratégicas | COOTAD Art. 295 |
| POA anual | GADM + 3 entes adscritos | Programación operativa anual | COPFP Art. 97 |
| Plan de Gobierno CNE | Candidato electo | Compromisos electorales | Código Democracia |
| Informes semestrales | GADM | Avance S1 y S2 | COPFP Art. 51 |

**Flujo al Motor:** El ICPI cruza las 25 metas del PDyOT con lo que el POA programó, lo que el SIGAD reportó y lo que el Plan de Gobierno prometió. La verificación es a cuatro niveles (existencia, verificabilidad, recursos, ejecución).

→ [[ICM_SIGAD_2023_2024]] · [[POA_2026_Contexto]] · [[Plan_CNE_Alcalde_Montecristi]]

---

### S3 · Silo Ejecución Fiscal → D3

| Fuente | Institución | Qué produce | Mandato legal |
|--------|-------------|-------------|--------------|
| eSIGEF | Ministerio de Finanzas | Cédula presupuestaria (codificado/devengado/pagado) | COPFP Art. 77 |
| SERCOP Portal | SERCOP | Procesos de contratación publicados | LOSNCP Art. 22 |
| PAC | GADM + 3 entes | Plan Anual de Contrataciones | LOSNCP Art. 22 |
| Reformas presupuestarias | GADM | Modificaciones presupuesto vigente | COPFP Art. 118 |
| Cédulas adscritas | Bomberos · Aseo EP · Patronato | eSIGEF por ente | COPFP Art. 77 |

**Flujo al Motor:** El Motor lee el devengado de los grupos 7 y 8 (inversión) de los 4 entes y calcula D3_Ti = Devengado/Codificado ponderado. Un proceso PAC no publicado = devengado 0 en esa partida.

→ [[ALERTA-D3_Ejecucion_Critica]] · [[PAC_2026_Contexto]] · [[FUENTES_Holding_Operativa]]

---

### S4 · Silo Territorial → D4

| Fuente | Institución | Qué produce | Mandato legal |
|--------|-------------|-------------|--------------|
| Censo de Población y Vivienda | INEC | NBI por parroquia, acceso servicios | Constitución Art. 154 |
| RIPS | Ministerio Salud / INEC | Población actualizada por zona | — |
| SIGAD inversiones | SNP / GAD | Inversión declarada por parroquia | COPFP Art. 50 |
| PDyOT Diagnóstico | GADM + equipo técnico | Análisis territorial base | COOTAD Art. 295 |
| Informe Presupuesto Participativo | GADM | Prioridades ciudadanas por parroquia | LOPC Art. 67 |

**Flujo al Motor:** El IRS correlaciona NBI% (INEC) con inversión per cápita (SIGAD). El IET compara la inversión de cada parroquia contra el promedio cantonal. El Composite Need pondera NBI + acceso agua + peso poblacional.

> La fuente más crítica de S4 es el **Censo INEC** — si los datos de NBI son de 2010, el IRS pierde precisión. El Motor usa el Censo 2022 para Montecristi.

→ [[ALERTA-Regresividad_IRS79]] · [[04_TGI_INDICADORES]] · [[07_TGI_Parroquias/_Índice_Parroquias]]

---

### S5 · Silo Institucionalidad → D5

| Fuente | Institución | Qué produce | Mandato legal |
|--------|-------------|-------------|--------------|
| Reporte ICM SIGAD | SNP / SETEPLAN | Índice Cumplimiento Metas por GAD | COPFP Art. 50 |
| Actas RdC | CPCCS | Verificación proceso rendición cuentas | LOPC Art. 89 · COOTAD Art. 302 |
| Orgánico estructural | GADM | Resolución estructura institucional | LOSEP Art. 52 |
| Contratos personal | GADM (Talento Humano) | Capacidad técnica instalada | LOSEP Art. 17 |
| Portal transparencia | GADM | Cumplimiento LOTAIP | LOTAIP Art. 7 |

**Flujo al Motor:** El Motor verifica si el GAD cumplió con los reportes SNP (ICM = 100% = D5 pleno), si ejecutó la RdC dentro de plazo y con contenido mínimo, y si su estructura orgánica está formalmente aprobada.

→ [[ICM_SIGAD_2023_2024]] · [[RDC_Holding_2023_2024]]

---

## El Ecosistema Institucional — Quién Controla Qué

```
PLANIFICACIÓN                    FISCALIZACIÓN
SNP / SETEPLAN                   Contraloría General del Estado (CGE)
    ↓ SIGAD, COPFP                   ↓ Auditorías, NCI
    
FINANZAS                         PARTICIPACIÓN
Ministerio de Economía           CPCCS
    ↓ eSIGEF, COPFP                  ↓ RdC, ICM, sanciones
    
CONTRATACIÓN                     ESTADÍSTICA
SERCOP                           INEC
    ↓ PAC, LOSNCP                    ↓ Censo, NBI, RIPS
    
TERRITORIO                       GOBIERNO LOCAL
SNP / SETEPLAN                   GADM Montecristi (4 entes)
    ↓ PDyOT, Ordenamiento           ↓ todo lo anterior
```

El Motor es el punto donde todos estos flujos institucionales **convergen** en un score único.

---

## Cadena de Custodia — Del Hecho al Score

```
Hecho territorial
(una parroquia sin agua potable)
    ↓
Dato INEC
(NBI parroquia X = 61.2%)
    ↓
Dato inversión
(eSIGEF inversión per cápita parroquia X)
    ↓
Motor QUIRA
(IRS = CORREL negativa NBI vs inversión)
    ↓
IRS = 79.7 → D4 ≈ 44.8%
    ↓
TGI Cantonal ≈ 66.85
    ↓
Señal accionable
(Redirigir PAC hacia parroquias rurales)
    ↓
Decisión institucional
(Alcaldía prioriza contratación rural en Q2)
```

Este es el ciclo completo — del hecho territorial al dato, del dato al score, del score a la decisión, de la decisión de vuelta al territorio.

→ [[MOTOR_03_Dialectica]]

---

*Motor QUIRA · Fuentes Institucionales · SIAP-ICPI_GOLD_MASTER_v5.4 · Dylus Lab © 2026*
