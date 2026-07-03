# MOTOR NLP DE FIDELIDAD NARRATIVA — Verificación del Discurso Público

> **PROPUESTA v0.1 · para revisión de Javo** (Regla 9: nace como doctrina, no en Python).
> Sesión 2026-07-04 · el **diferenciador** de QUIRA. Convierte **cualquier discurso público de una
> autoridad** (video en la web) en **afirmaciones verificables** cruzadas contra la **evidencia real** —
> y expone la brecha entre lo que se DICE y lo que se HACE, con la prueba al lado.

## 1 · El problema y el diferenciador
Una autoridad **habla** en un evento (rendición, entrevista, cadena) y **afirma** logros, cifras y
compromisos. Hoy nadie contrasta ese discurso con la evidencia de forma sistemática. QUIRA sí: extrae
cada afirmación del video y la cruza con el **dato duro** (presupuesto, contratación, obra, norma).
Donde el discurso y el hecho coinciden → integridad; donde difieren → **la brecha queda a la vista, con
evidencia, no con opinión**. Esto **no lo hace ningún otro sistema**.

## 2 · Genérico y escalable (decisión Javo 2026-07-04)
El pipeline es **el mismo** para cualquier sujeto; **cambia solo la fuente de evidencia**:

| Sujeto | Fuente de evidencia (el "hecho") |
|---|---|
| **Alcalde / GAD** (piloto) | POA · PAC/SERCOP · eSIGEF · PDOT · corpus local (lo que ya tenemos) |
| **Presidente / Ministros** | **PND** · Presupuesto General del Estado (eSIGEF nacional) · SERCOP · corpus normativo |
| **Entidad pública o privada con recursos públicos** | sus informes · contratación · presupuesto ejecutado |

Un video → el mismo motor → distinta biblioteca de evidencia según quién habla. Así el diferenciador
escala de lo municipal a lo nacional sin reescribir el motor.

## 3 · El pipeline (5 etapas)
```
Video público (YouTube / web)
   │ [1] ADQUISICIÓN — yt-dlp descarga el audio (+ metadatos: fecha, autor, evento)
   ▼
Audio
   │ [2] TRANSCRIPCIÓN (STT) — Whisper → texto con timestamps · diarización (quién habla)
   ▼
Transcripción con marcas de tiempo
   │ [3] EXTRACCIÓN DE AFIRMACIONES — LLM (Haiku volumen · Sonnet/Opus criterio) identifica las
   │     afirmaciones VERIFICABLES del sujeto: cifras, compromisos, logros ("invertimos $X", "hicimos Y")
   ▼
Claims estructurados {afirmación, timestamp, tipo, magnitud declarada, eje}
   │ [4] CRUCE CON EVIDENCIA — cada claim ↔ corpus (Supabase) + Gold Master + POA/eSIGEF/SERCOP
   │     → la prueba que lo confirma o lo contradice (mismo motor semántico de los aportes)
   ▼
Matriz claim ↔ evidencia
   │ [5] SCORING — IF_n (evaluación experta trazable): la máquina propone, el humano ratifica
   ▼
MFN — Matriz de Fidelidad Narrativa (alimenta H34b · snapshot · UI · grafo)
```

## 4 · Los modelos (arquitectura maestro-aprendiz · intuición de Javo)
- **Haiku 4.5** — el operativo: transcribe-a-claims y cruza en **volumen** (barato, rápido). Vía API.
- **Sonnet 5 / Opus 4.8** — el maestro: diseña las rúbricas, valida los casos difíciles, cura el prompt
  y el criterio de fidelidad. La "maestría" vive en el **canon + rúbricas + system prompt**, no en pesos
  de un modelo destilado. (Piloto: prueba con Haiku vía API; recarga $5 cuando arranquemos.)

## 5 · Las relaciones que se VEN y las que NO se ven (lo que pidió Javo)
El NLP no solo mide fidelidad; **alimenta el grafo (Neo4j)** con claims + evidencia, y de ahí emergen
relaciones que ningún tablero muestra solo:

**Visibles (contraste directo):**
- Discurso ↔ evidencia (fidelidad narrativa).
- Aporte ciudadano ↔ obra ejecutada (trazabilidad · ya construida).
- Promesa de campaña (CNE) ↔ PDOT ↔ ejecución.

**Invisibles (las que el grafo revela):**
- **Compromiso hablado SIN correlato** en presupuesto/POA → brecha oculta ("lo prometido que no se presupuestó").
- **Obra ejecutada SIN mandato** → gasto que no responde a ninguna promesa ni demanda ciudadana.
- **Silencios:** lo que la evidencia registra pero el discurso **NO menciona** (y viceversa).
- **Patrones temporales:** temas que se repiten en el discurso año a año vs. su ejecución real (¿promesa reciclada?).
- **Redes de actores:** quién promete qué, quién ejecuta qué, qué se financia con qué partida.

> Con el NLP completo se construyen **todos los gráficos, análisis y conceptos** de estas relaciones
> (Javo 2026-07-04). Ahí —no antes— cierra **PCD-D09**.

## 6 · Firewall y honestidad
- La IA **extrae y propone**; **nunca produce la verdad**. La fidelidad final es **evaluación experta
  trazable** (IF_n), como los aportes: la máquina sugiere, el humano ratifica (archivo versionado).
- Lenguaje de **gobernanza**, no acusatorio: «brecha», «en seguimiento», «sin correlato» — nunca
  «mintió». Demagogia **expuesta con evidencia**, no con opinión (Regla 2/3).
- Cada claim «verificado» **muestra su prueba** (partida, contrato, norma con SHA-256).

## 7 · Construcción y prueba
- **Piloto: RDC 2024** — hoy solo hay una **prueba rápida** (9 claims manuales en `H34b`, con timestamps).
  El NLP la **expande** (extrae del video completo) y valida. **Luego 2025.**
- Dependencias: `yt-dlp` (adquisición) · `whisper`/`faster-whisper` (STT) · `anthropic` (extracción, ✓ instalado).
- Módulos (a construir): `scripts/nlp/adquirir.py` · `transcribir.py` · `extraer_claims.py` ·
  `cruzar_evidencia.py` (reusa el motor semántico de aportes) · `scoring_mfn.py`.
- **Necesario de Javo:** el **link del video RDC 2024** en YouTube · recarga de API Haiku ($5) · OK para
  instalar `yt-dlp`/`whisper`.

---
*Motor NLP de Fidelidad Narrativa · Dylus Lab © 2026 · PROPUESTA v0.1 (el diferenciador) · pendiente aval de Javo.*
