# MOTOR NARRATIVO DE QUIRA — Verificación de Coherencia Pública

> **PROPUESTA v0.2 · incorpora el feedback del asesor externo (2026-07-04).**
> Renombrado de "Motor NLP": el sistema ya no hará *solo* NLP. Hará transcripción, diarización,
> extracción semántica, clasificación, detección de relaciones, contraste documental, inferencia
> causal, razonamiento LLM, scoring y **aprendizaje**. Eso no es NLP — es el **Motor Narrativo**,
> una pieza de la cadena de motores de QUIRA. *(Nombres en evaluación: Motor Narrativo · MVN Motor
> de Verificación Narrativa · MIN Motor de Inteligencia Narrativa — Javo decide el definitivo.)*

## 0 · El salto conceptual (asesor)
Con este motor, QUIRA deja de ser un **observatorio de datos** y se vuelve un **observatorio de
decisiones, discursos y coherencia institucional.** El Motor Narrativo nace dentro de la cadena:

> **Matemático → Documental → Relacional → NARRATIVO → Causal → Prospectivo → Conversacional**

Es uno de los mayores saltos arquitectónicos de QUIRA hasta hoy.

## 1 · El diferenciador REAL (asesor · punto 5)
NO es "cruzar discurso vs. evidencia" —eso cualquiera lo intenta—. El diferenciador es verificar la
**coherencia entre las capas de la realidad pública**:

> **NARRATIVA → PROMESA → PLANIFICACIÓN → PRESUPUESTO → EJECUCIÓN → TERRITORIO**

QUIRA **no verifica frases; verifica coherencia entre capas.** Eso sí es único.

## 2 · El pipeline — con **etapa 0 · IDENTIDAD** (asesor · punto 2)
```
VIDEO
  │ [0] IDENTIDAD — antes de descargar: autoridad · institución · cargo · fecha · evento ·
  │     período · enlace · HASH. (registro auditable — fundamental para la trazabilidad posterior)
  ▼
  │ [1] ADQUISICIÓN — yt-dlp baja el audio + metadatos
  ▼
  │ [2] TRANSCRIPCIÓN — Whisper → texto con timestamps · diarización (quién habla)
  ▼
  │ [3] UNIDADES NARRATIVAS — el LLM extrae UNIDADES, no claims (ver §3)
  ▼
  │ [4] NORMALIZACIÓN — cada unidad se descompone en sus claims verificables
  ▼
  │ [5] CLAIMS VERIFICABLES {afirmación · timestamp · tipo · magnitud · eje · promesa implícita}
  ▼
  │ [6] CRUCE DE 5 CAPAS — cada claim ↔ promesa (CNE) · plan (PDOT/POA) · presupuesto · ejecución ·
  │     territorio (reusa el motor semántico de aportes + corpus + Gold Master)
  ▼
  │ [7] SCORING — IF_n (evaluación experta trazable: la máquina propone, el humano ratifica)
  ▼
MFN → Neo4j → Motor Relacional → Motores Prospectivos → QUIRA IA → UI   (§7: la MFN es el inicio)
```

## 3 · Unidades Narrativas, NO claims (asesor · puntos 3-4)
Una autoridad dice: *"Construimos tres parques para mejorar la seguridad."* Eso **no es un claim** —
contiene una **obra** (tres parques) + un **objetivo** (seguridad) + una **causalidad** (parques→seguridad)
+ una **promesa implícita**. Es una **unidad narrativa**. Recién la **normalización** la descompone en
claims verificables (una frase puede generar varios). Verificar la unidad completa —incluida la
causalidad declarada— es parte del diferenciador.

## 4 · Genérico y escalable (Javo) — mismo motor, distinta evidencia
| Sujeto | Fuente de evidencia (el "hecho") |
|---|---|
| **Alcalde / GAD** (piloto) | POA · PAC/SERCOP · eSIGEF · PDOT · corpus local |
| **Presidente / Ministros** | **PND** · Presupuesto General del Estado · SERCOP · corpus normativo |
| **Entidad pública/privada con recursos públicos** | sus informes · contratación · presupuesto ejecutado |

## 5 · El **Motor de Relaciones** — motor independiente (asesor · puntos 6, 9)
Las relaciones **no son un apartado; son un motor**. De aquí nace una familia de análisis:
- **Visibles:** A dijo X · existe contrato · existe presupuesto · existe obra.
- **Invisibles (la mina de oro):** obra que **nunca fue prometida** · promesa que **nunca fue
  presupuestada** · dinero que **nunca produjo resultado** · obra terminada que **nunca fue mencionada** ·
  narrativa que cambió mientras el presupuesto no.
- **Silencios · Redes de actores · Patrones** (promesa reciclada año a año).
- **Contradicciones (asesor · punto 9):** *"No existe déficit"* vs. *"Recibimos un municipio quebrado"* —
  contradicción narrativa a detectar, aunque ambas frases sean por separado defendibles.

## 6 · El aprendizaje: **Banco de Casos** (asesor · punto 8)
QUIRA debe **aprender** — no el modelo (nada de fine-tuning), sino **QUIRA**. Cada vez que un humano
**corrige, acepta o rechaza** un match, eso alimenta un **Banco de Casos**: una **memoria metodológica**
versionada. *(El `aportes_validacion.json` ya es el germen de ese banco.)* Dentro de un año, QUIRA será
mucho mejor sin reentrenar ningún modelo.

## 7 · La MFN es el inicio, no el final (asesor · punto 7)
`MFN → Neo4j → Motor Relacional → Motores Prospectivos → QUIRA IA → UI`. La Matriz de Fidelidad no
termina en una tabla: siembra el grafo, del que emergen relaciones, prospectiva y conversación.

## 8 · Modelos maestro-aprendiz (Javo)
**Haiku 4.5** opera en volumen (transcripción→unidades, cruce); **Sonnet 5 / Opus 4.8** son el maestro
(rúbricas, casos difíciles, criterio). La maestría vive en **canon + rúbricas + system prompt**, no en
pesos destilados.

## 9 · Firewall y **protección jurídica** (asesor · punto 10)
> **QUIRA transforma narrativa pública en conocimiento verificable, preservando la separación entre
> evidencia, interpretación y decisión.**

La IA **extrae y propone; nunca produce la verdad**. El humano ratifica. Lenguaje de gobernanza, no
acusatorio (Regla 2/3). Cada claim «verificado» **muestra su prueba** (partida, contrato, norma SHA-256).

## 10 · Construcción y prueba
- **Videos (Javo):** RDC 2024 `https://www.youtube.com/watch?v=mqDT5jKXHW8` · RDC 2025
  `https://www.youtube.com/watch?v=Qexwg7EKmUo`. Piloto = **2024** (expande la prueba rápida de 9
  afirmaciones en `H34b`) → luego **2025**.
- **Deps:** `yt-dlp` · `faster-whisper` (STT local, modelo `small`) · `anthropic` (✓, key en secrets).
- **Módulos:** `scripts/motor_narrativo/` → `identidad.py` · `adquirir.py` · `transcribir.py` ·
  `unidades.py` · `normalizar.py` · `cruzar_5capas.py` · `scoring_mfn.py`.
- **Cierre:** con el motor completo y los análisis de relaciones → cierra **PCD-D09**.

---
*Motor Narrativo de QUIRA · Dylus Lab © 2026 · v0.2 (asesor + Javo + Claude) · el observatorio de la
coherencia institucional. Pendiente aval final del nombre y del alcance por Javo.*
