# QNKC-001 — Regla Arquitectónica Canónica
## Función Universal · Institución Contingente · Territorio Observable

**Versión**: 1.0  
**Fecha**: 2026-05-30  
**Proyecto**: QUIRA Gov — QNKC (QUIRA National Knowledge Core)  
**Alcance**: Ecuador (221 GADs) + LAC (cantones equivalentes)  
**Estado**: CONGELADO

---

## La Frase Canónica

> **Los derechos son universales.**  
> **Las competencias son normativas.**  
> **Las funciones son permanentes.**  
> **Las instituciones son contingentes.**  
> **Los territorios son la realidad observable.**

Esta frase es el principio rector de toda la arquitectura de materialización territorial de QUIRA. Ningún modelo de datos, indicador o protocolo puede contradecirla.

---

## La Regla

**QUIRA no modela:** "Quién presta el servicio"  
**QUIRA modela:** "Qué obligación pública existe y cómo se materializa en un territorio específico"

---

## La Cadena Canónica de 9 Capas

```
Capa 1 — DERECHO            Universal
         (CE, COOTAD, norma equivalente en LAC)
              ↓
Capa 2 — COMPETENCIA        Normativa
         (atribuida por ley al nivel de gobierno)
              ↓
Capa 3 — FUNCIÓN PÚBLICA    Permanente
         (obligación de resultado, independiente de la forma institucional)
              ↓
Capa 4 — SERVICIO           Variable
         (cómo se organiza la prestación en el territorio)
              ↓
Capa 5 — ACTOR EJECUTOR     Contingente
         (EP / Dirección / Concesión / Mancomunidad / Sistema Comunitario)
              ↓
Capa 6 — PROCESO            Local
         (trámite, POA, contrato — viene del orgánico del cantón)
              ↓
Capa 7 — EVIDENCIA          Observable
         (LOTAIP / SIGEF / Catastro / Contratos)
              ↓
Capa 8 — INDICADOR          Medible
         (TGI, KPI, cobertura — definición universal, valor local)
              ↓
Capa 9 — TERRITORIO         La realidad
         (parroquia, zona, comunidad — lo que se gobierna)
```

**Capas 1-2**: Protocolo QLEP  
**Capas 3-9**: Protocolo QTMP (futuro)

---

## Ejemplo Canónico — Derecho Humano al Agua

| Capa | Universal | Montecristi | Manta | Cuenca | Colombia |
|---|---|---|---|---|---|
| **Derecho** | CE Art. 12 | CE Art. 12 | CE Art. 12 | CE Art. 12 | Ley 142 / CN Art. 365 |
| **Competencia** | CE 264.4 | CE 264.4 | CE 264.4 | CE 264.4 | Ley OSP |
| **Función** | Proveer agua potable segura y continua | ← | ← | ← | ← |
| **Servicio** | Agua domiciliaria municipal | Municipal directo | EP Agua | ETAPA (EP) | ESP mixta |
| **Actor** | (variable) | Pendiente verificar orgánico | EMAPAM | ETAPA | ESP local |
| **Proceso** | (variable) | Según orgánico GADM | Proceso EMAPAM | Proceso ETAPA | Proceso ESP |
| **Evidencia** | LOTAIP Num. 6, 10 | LOTAIP GADM | LOTAIP Manta | LOTAIP Cuenca | SUI Colombia |
| **Indicador** | Cobertura agua potable % | Por parroquia Montecristi | Por parroquia Manta | Por parroquia Cuenca | Por municipio |
| **Territorio** | Parroquia / Zona | Isabel Muentes: brecha | Zona rural: brecha | Parroquias altas | Municipio rural |

**El derecho es el mismo. La institución es diferente. La función es la misma.**

---

## La Pregunta que QUIRA Puede Responder

Un repositorio legal responde:
> "¿Qué dice el Artículo 12 de la Constitución?"

QUIRA responde:
> "¿Dónde está incumpliéndose el Derecho Humano al Agua en el cantón Montecristi?"

```
CE_12 (Derecho)
  ↓ CE_264.4 (Competencia GAD)
    ↓ Provisión agua potable (Función)
      ↓ [Actor local - pendiente orgánico] (Actor)
        ↓ LOTAIP Numeral 6: ejecución presupuestaria
          ↓ Cobertura agua potable por parroquia
            ↓ Parroquia Isabel Muentes: NBI=61.2%
              ↓ Brecha estimada: ~40% sin cobertura
                ↓ Personas afectadas: ~3,200
```

Eso es gobernanza territorial preventiva.

---

## Implicación para el Orgánico Municipal

El orgánico de cada cantón **no es un dato de contexto**. Es el **dato de Capa 5** que conecta la función pública con el actor ejecutor.

Por lo tanto:
- El orgánico de Montecristi (Resolución Orgánica del GADM) es fuente primaria del QTMP
- El Gold Master es la fuente canónica para los datos financieros del actor
- El PDOT es la fuente para los datos de brecha territorial

Ningún modelo QUIRA puede inferenciar el actor ejecutor desde el nombre de la competencia. Solo el orgánico lo dice.

---

## Implicación para LAC

La misma cadena de 9 capas funciona en cualquier sistema municipal de LAC porque:
- Las Capas 1-3 (Derecho, Competencia, Función) varían en nombre pero son análogas
- Las Capas 4-9 varían en forma pero son observables

QUIRA puede escalar a cualquier cantón LAC mapeando:
1. El equivalente normativo local al ACK correspondiente
2. El actor local al nodo `:ActorLocal` de Neo4j
3. El sistema de evidencia pública (LOTAIP / SUI Colombia / SIAF Perú / etc.)

El grafo es el mismo. Los nodos son locales. Las relaciones son universales.

---

## Lo que Está FUERA de QNKC-001

Esta regla NO dice:
- Que el orgánico sea irrelevante (es Capa 5 — crítica)
- Que todas las instituciones son iguales (son contingentes, no irrelevantes)
- Que no se modele el actor ejecutor (sí se modela — en el QTMP, no en el QLEP)
- Que el orgánico no importa para Montecristi (importa muchísimo — es la fuente canónica del QTMP)

Esta regla SÍ dice:
- El QLEP no puede inferir el actor desde el derecho
- El actor viene siempre de fuente documental (orgánico / Gold Master)
- La función existe aunque el actor cambie o no exista aún
- El modelo es escalable porque está anclado en la función, no en la institución

---

## Protocolos del QNKC

| Protocolo | Nombre completo | Fuente | Capa |
|---|---|---|---|
| **QLEP** | QUIRA Legal Extraction Protocol | Texto legal | 1-2 |
| **QTMP** | QUIRA Territorial Materialization Protocol | Orgánico + Gold Master + POA + PDOT | 3-7 |
| TGI | Tablero de Gobernanza Institucional (existente) | Gold Master | 8-9 |

---

*QNKC-001 v1.0 — QUIRA Gov · Dylus Lab © 2026*  
*Principio elaborado en colaboración directora durante Sprint F0 — 2026-05-30*
