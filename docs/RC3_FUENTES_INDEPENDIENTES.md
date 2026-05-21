# RC-3 — Fuentes de Datos Independientes para Análisis Municipal

**QUIRA OS · Módulo RC-SCOUT / Expansión GADs Manabí**
Versión 1.0 · 2026-05-21 · Dylus Lab © 2026

> **Principio rector:** QUIRA opera en modo INDEPENDIENTE — analiza municipios sin acceso a sistemas internos (eSIGEF, SIGAD, redes del GAD). Todo dato proviene de fuentes públicas y portales oficiales. Este documento define la arquitectura de datos de esa operación independiente.

---

## Mapa de Fuentes — Vista General

```
QUIRA RC-SCOUT — FUENTES PÚBLICAS DISPONIBLES
═══════════════════════════════════════════════

[1] DPE (LOTAIP)          → Presupuesto mensual · Transparencia activa
[2] SERCOP                → PAC + Estado de procesos de contratación
[3] CPCCS                 → Rendición de cuentas (informe técnico + evento)
[4] Redes sociales        → Evidencia del evento público de RdC
[5] SIGAD / SNP           → ICM (Índice de Cumplimiento de Metas)
[6] SENAE / SRI           → Datos económicos territoriales (aux.)

LO QUE NO ENTRA AL SISTEMA INDEPENDIENTE:
✗ Informes internos de direcciones      → Solo se mide lo que está en sistemas públicos
✗ Memorándums y comunicaciones internas → No disponibles sin acceso al GAD
✗ eSIGEF directo                        → Requiere credenciales institucionales
✗ SIGAD interno                         → Solo la versión pública del ICM
```

---

## [1] FUENTE: Portal DPE (LOTAIP)

**URL:** `https://transparencia.dpe.gob.ec/entidades/{eid}`
**API:** `https://api.transparencia.dpe.gob.ec/backend/v1/`
**Script:** `scripts/rc_scout.py` + `scripts/_generate_snapshot_dpe.py`

### Datos disponibles (automatizable vía API)

| Dato | Endpoint | Periodicidad |
|------|----------|--------------|
| Datos de la entidad (RUC, autoridad, dirección, email) | `/admin/establishment/{id}` | Una vez + validación anual |
| Cobertura presupuestaria mensual (qué meses publicaron) | `/public/presupuesto` | Mensual |
| Reporte anual disponible (LOTAIP) | `/transp/anual-report/establishment` | Anual |
| Lista completa de entidades | `/admin/establishment/list?function=7` | Setup inicial |

### Datos disponibles (descarga manual — bug en URL de DPE)

| Dato | Formato | Acción requerida |
|------|---------|-----------------|
| Cédula presupuestaria mensual (devengado, codificado por partida) | CSV/XLSX | Descarga manual portal DPE → `data/{municipio}/cedulas/` |
| Informe de actividades de la entidad | PDF | Descarga manual si disponible |

### Scoring RC-SCOUT (DPE)

```python
score = 0
# Cobertura 2025 (12 meses = máximo)
score += len(meses_2025) * 5      # max: 60 pts
# Cobertura 2026 (4 meses evaluados)
score += len(meses_2026) * 5      # max: 20 pts
# Reporte anual disponible
score += 12 if reporte_anual else 0
# VIABLE si score >= 60
```

### Estado actual RC-SCOUT

| Municipio | DPE ID | Score | Estado |
|-----------|--------|-------|--------|
| El Carmen | 932 | 92 | ✅ Viable |
| 24 de Mayo | 944 | 92 | ✅ Viable |
| Manta | 936 | — | 🔄 Pendiente snapshot |
| Jipijapa | 934 | — | 🔄 Pendiente snapshot |

---

## [2] FUENTE: SERCOP — Contratación Pública

**URL:** `https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/`
**API SOCE:** `https://soce.gob.ec/soce/`
**Portal OCDS:** `https://opendataec.gob.ec/`

> **Principio crítico:** NO se descarga solo el PAC. Se analiza el **estado vivo de los procesos de contratación** mes a mes. El PAC es la planificación; los procesos son la ejecución legal real.

### A) Plan Anual de Contratación (PAC)

| Dato | Descripción | Uso en QUIRA |
|------|-------------|--------------|
| PAC publicado | Lista de procesos planificados para el año | Baseline de planificación |
| Fecha de publicación PAC | Oportunidad de publicación (obligatorio antes 15-ene) | D1 Legalidad |
| Total planificado ($) | Monto total PAC | Codificado inicial |
| # procesos planificados | Volumen de contratación previsto | Referencia Ti |

**Descarga:** `https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/busqueda/buscarPAC`
**Filtro:** RUC de la entidad + año

### B) Estado de Procesos Activos (mensual)

> **Esta es la fuente crítica que determina si el dinero se está moviendo.**

| Indicador | Cómo se obtiene | Métrica QUIRA |
|-----------|-----------------|--------------|
| Procesos adjudicados | SOCE API o portal: estado="ADJUDICADO" | % PAC ejecutado |
| Procesos en publicación | Estado="EN_PUBLICACION" | Procesos vivos activos |
| Procesos cancelados | Estado="CANCELADO" | Señal de ejecución deficiente |
| Procesos desiertos | Estado="DESIERTO" | Alerta de capacidad técnica |
| Contratos firmados | Estado="CONTRATO_SUSCRITO" | Compromisos vinculantes |
| Contratos liquidados | Estado="CONTRATO_LIQUIDADO" | Ejecución completada |
| Procesos de emergencia | Tipo="CONTRATACION_EMERGENCIA" | Señal de capacidad planificación |
| Procesos sin resolución >90 días | Cálculo propio (fecha_inicio vs hoy) | Alerta de parálisis |

### C) Métricas calculadas por QUIRA (mensual)

```python
# Eficiencia de contratación
pct_adjudicados = n_adjudicados / n_pac_total * 100
pct_cancelados  = n_cancelados  / n_pac_total * 100

# Velocidad de ejecución (meses transcurridos)
if mes_actual >= 4:
    ejecucion_esperada = (mes_actual / 12) * 100
    brecha_ejecucion = ejecucion_esperada - pct_adjudicados

# Calidad de planificación
fraccionamiento_flag = any(proceso.tipo == "MENOR_CUANTIA" and
                           proceso.objeto_similar_count > 3
                           for proceso in procesos)
```

### D) Alertas SERCOP automáticas

| Alerta | Umbral | Base legal |
|--------|--------|-----------|
| PAC no publicado | Sin PAC a 31-ene | LOSNCP Art. 22 |
| Procesos cancelados > 15% | > 15% del PAC cancelado | Señal D3 |
| Parálisis de procesos | >5 procesos sin resolución +90 días | Capacidad técnica D5 |
| Fraccionamiento detectado | Patrones de objetos similares | LOSNCP Art. 78 |
| Emergencias > 10% PAC | Monto emergencias / PAC total | Planificación D5 |

### E) Fuente técnica de obtención

```
Opción 1 (API OCDS — preferida):
  GET https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/v1/contracts
  ?buyer.identifier.id={RUC}&year={YEAR}&page=1&limit=100

Opción 2 (Portal web — fallback):
  Acceder a compraspublicas.gob.ec
  → Búsqueda avanzada → Entidad → RUC
  → Filtrar por período → Exportar CSV

Actualización: mensual (días 1-5 de cada mes)
Script destino: scripts/fetch_sercop.py (pendiente)
```

---

## [3] FUENTE: CPCCS — Rendición de Cuentas

**Portal:** `https://rendiciondecuentas.cpccs.gob.ec/`
**Marco legal:** LOPC Arts. 88-95 · COOTAD Art. 302 · Res. CPCCS-004-2026

> **La RdC tiene DOS componentes evaluables de forma independiente — ambos deben incorporarse al análisis:**

### Componente A: Informe Técnico en Portal CPCCS

El informe técnico es el documento formal subido a la plataforma CPCCS. Es **público y verificable**.

| Dato | Cómo obtener | Métrica |
|------|-------------|---------|
| Número de informe CPCCS | Portal CPCCS → búsqueda por RUC/entidad | Verificación D5 (proceso cumplido) |
| Fecha de ingreso a plataforma | Metadata del informe | Oportunidad (¿dentro del período?) |
| Autoridad que rindió | Nombre y cédula del alcalde/alcaldesa | Verificación institucional |
| Asistentes al evento | Campo "# participantes" del formulario | Universalidad LOPC Art. 89 |
| ¿Evento en territorio rural? | Campo "lugar deliberación" | D4 Equidad |
| Plan de trabajo con sugerencias ciudadanas | Adjunto al informe | Ciclo retroalimentación |
| Aportes ciudadanos documentados | Actas y/o resumen en informe | Calidad participación |
| Obligaciones tributarias cumplidas | Campo formulario | D1 Legalidad |

```python
# Verificación CPCCS (automatizable)
def fetch_rdc_cpccs(ruc: str, year: int) -> dict | None:
    """
    Consulta el portal CPCCS por RUC y año.
    Retorna dict con: n_informe, fecha_ingreso, asistentes,
    lugar_deliberacion, plan_trabajo_publicado
    """
    # URL: rendiciondecuentas.cpccs.gob.ec/busqueda?ruc={ruc}&anio={year}
    ...
```

**Scoring RdC Componente A:**

| Criterio | Puntos | Máximo |
|----------|--------|--------|
| Informe presentado en el período | 30 | 30 |
| Asistentes > 100 | 10 | 10 |
| Lugar en zona rural | 10 | 10 |
| Plan de trabajo con sugerencias publicado | 10 | 10 |
| Informe también en LOTAIP Art. 19 num. 12 | 5 | 5 |
| **Total Componente A** | — | **65** |

### Componente B: Evento Público en Redes Sociales

> El evento de deliberación pública es obligatorio (LOPC Art. 89: "interactivo"). La evidencia del evento está en las redes oficiales del GAD (YouTube, Facebook). Este es un verificador independiente del cumplimiento real — no basta con que el formulario diga que se realizó.

| Dato | Fuente | Método de obtención |
|------|--------|---------------------|
| Video de la deliberación pública | YouTube oficial del GAD | Búsqueda: "{nombre GAD} rendición de cuentas {año}" |
| Transmisión en vivo / grabada | Facebook oficial del GAD | Búsqueda en página oficial |
| Fecha del video | Metadata YouTube/Facebook | Verificación vs fecha en informe CPCCS |
| Duración del evento | Duración del video | Proxy de profundidad del evento |
| Vistas / Alcance | Contador YouTube | Indicador de difusión |
| Comentarios ciudadanos | Sección comentarios | Participación digital |
| ¿Discurso del alcalde disponible? | Video principal | D5: autoridad presente en RdC |

```
PROCESO DE VERIFICACIÓN SOCIAL (mensual, manual):
  1. Buscar en YouTube: "{GAD} rendicion cuentas {año}"
  2. Buscar en Facebook: página oficial del GAD → videos → filtrar por período RdC
  3. Registrar: URL video, fecha, duración, vistas
  4. Comparar fecha video vs fecha en informe CPCCS (deben coincidir ±7 días)
  5. Registrar en snapshot bajo: accountability.rdc_evento_publico

Automatización futura:
  - YouTube Data API v3 → búsqueda por canal oficial del GAD
  - Facebook Graph API → videos públicos de la página
```

**Scoring RdC Componente B:**

| Criterio | Puntos | Máximo |
|----------|--------|--------|
| Video del evento encontrado | 15 | 15 |
| Fecha del video coincide con informe CPCCS | 10 | 10 |
| Duración > 45 minutos | 5 | 5 |
| Discurso del alcalde/alcaldesa verificado | 5 | 5 |
| **Total Componente B** | — | **35** |

### Scoring Total RdC = Componente A + B

```
RdC Score (0–100):
  ≥ 85 → "Rendición de cuentas excelente" (D5 fuerte)
  70–84 → "Rendición de cuentas completa" (D5 cumplido)
  50–69 → "Rendición de cuentas parcial" (D5 con observaciones)
  < 50 → "Rendición de cuentas deficiente" → ALERTA D5 crítica

Nota: Si Componente A = 0 (no presentó informe CPCCS) → Score total = 0
independientemente del Componente B.
```

### Estructura en el Snapshot (gm_snapshot.json)

```json
"accountability": {
  "rdc": {
    "year": 2024,
    "componente_a": {
      "n_informe_cpccs": "22844",
      "fecha_ingreso": "2025-08-08",
      "en_periodo_cpccs": true,
      "asistentes": 261,
      "lugar": "Comuna Toalla Grande",
      "zona_rural": true,
      "plan_trabajo_publicado": true,
      "publicado_lotaip": null,
      "score": 65
    },
    "componente_b": {
      "video_url": "https://youtube.com/watch?v=...",
      "fecha_video": "2025-07-11",
      "plataforma": "YouTube",
      "duracion_min": 120,
      "vistas": 1450,
      "score": 35
    },
    "score_total": 100,
    "clasificacion": "Rendición de cuentas excelente",
    "fuente": "Portal CPCCS + YouTube GAD Montecristi"
  }
}
```

---

## [4] FUENTE: SIGAD / SNP — ICM (Índice de Cumplimiento de Metas)

**URL:** `https://portalsigad.gob.ec/` (datos PDOT)
**Reporte:** SNP genera ICM municipal — dato público anual

| Dato | Periodicidad | Uso |
|------|-------------|-----|
| ICM anual por municipio | Anual (último trimestre) | ICPI componente D2 |
| % cumplimiento metas PDOT | Anual | D2 Planificación |
| Categoría de evaluación (Alto/Medio/Bajo) | Anual | Clasificación D2 |

**Nota:** El ICM del SIGAD es la fuente canónica para D2 cuando se trabaja en modo independiente. No equivale al ICPI completo (que requiere Gold Master Excel), pero es el mejor proxy disponible desde fuentes públicas.

---

## [5] INFORMES INTERNOS DE DIRECCIONES — Política de no-colección

> **Decisión arquitectónica:** QUIRA en modo independiente NO requiere ni solicita informes internos de las direcciones del GAD (informes de gestión mensuales, memorándums, POA avance, etc.).

**Razón:** Operamos sobre fuentes públicas verificables. Los informes internos:
- No son de acceso público (no están en LOTAIP Numeral 6)
- Requieren acceso institucional
- Son subjetivos (preparados por la misma entidad que se evalúa)
- Generan dependencia del GAD para el análisis

### Qué medimos en lugar de los informes internos

Para cada dimensión que un informe interno cubriría, tenemos una fuente pública equivalente:

| Lo que mediría el informe interno | Fuente pública equivalente | Métrica QUIRA |
|----------------------------------|---------------------------|---------------|
| Avance presupuestario de la dirección | DPE / cédula eSIGEF | Ti por período |
| Procesos de contratación de la dirección | SERCOP procesos activos | % adjudicación |
| Cumplimiento de metas PDOT | SIGAD ICM público | ICM anual |
| Obras ejecutadas | RdC CPCCS + SERCOP contratos | Evidencia territorial D4 |
| Gestión de RRHH | LOSEP datos públicos (en construcción) | — |

### Eficiencia Directiva — Lo que sí medimos

> El modo independiente mide **eficiencia directiva desde afuera**: si los resultados aparecen en sistemas públicos, el director está ejecutando. Si no aparecen, la dirección es invisible desde los sistemas.

```
INDICADORES DE EFICIENCIA DIRECTIVA (fuentes públicas):
  ① Velocidad de ejecución SERCOP   → ¿Los procesos se abren y adjudican a tiempo?
  ② Cobertura LOTAIP                → ¿Se publica la información mensualmente?
  ③ Cumplimiento RdC                → ¿La dirección entregó datos al alcalde para RdC?
  ④ ICM SIGAD                       → ¿Las metas del PDOT avanzan?
  ⑤ Ti presupuestario (DPE)         → ¿El presupuesto se ejecuta en el período?

QUIRA NO mide:
  ✗ Reuniones internas de la dirección
  ✗ Informes de gestión mensuales (internos)
  ✗ Memorándums y comunicaciones
  ✗ Eficiencia personal del director (requiere evaluación LOSEP interna)
```

---

## Matriz Consolidada de Fuentes

| Fuente | Automatizable | Frecuencia | Dimensión TGI | Script |
|--------|:------------:|:----------:|:-------------:|--------|
| DPE presupuesto (API) | ✅ | Mensual | D3 Ti | `rc_scout.py` ✅ |
| DPE cédula CSV | ⚠️ Manual | Mensual | D3 Ti detallado | Manual → `data/{gad}/cedulas/` |
| SERCOP PAC | ⚠️ Semi-auto | Anual | D3, D5 | `fetch_sercop.py` 🔄 pendiente |
| SERCOP procesos activos | ⚠️ Semi-auto | Mensual | D3, D5 | `fetch_sercop.py` 🔄 pendiente |
| CPCCS RdC Informe (Comp. A) | ⚠️ Semi-auto | Anual | D5, D4, D1 | `fetch_rdc_cpccs.py` 🔄 pendiente |
| Redes sociales evento RdC (Comp. B) | ❌ Manual | Anual | D5 | Manual → snapshot |
| SIGAD ICM | ❌ Manual | Anual | D2 | Manual → snapshot |

**Leyenda:** ✅ Implementado · ⚠️ En construcción · ❌ Manual (por ahora) · 🔄 Pendiente

---

## Snapshot Schema — Secciones Nuevas (extensión)

El `gm_snapshot.json` generado por `_generate_snapshot_dpe.py` se extiende con:

```json
{
  "_meta": { "...": "..." },
  "gad": { "...": "..." },
  "tgi": { "...": "..." },
  "financiero": { "...": "..." },
  "series_longitudinal": { "...": "..." },
  "territorial": { "...": "..." },

  "contratacion": {
    "pac_year": 2026,
    "pac_publicado": true,
    "fecha_pac": "2026-01-12",
    "total_planificado_usd": 4500000,
    "n_procesos_planificados": 87,
    "estado_al_corte": {
      "adjudicados": 23,
      "en_publicacion": 15,
      "cancelados": 4,
      "desiertos": 2,
      "contratos_suscritos": 21,
      "contratos_liquidados": 8
    },
    "pct_adjudicados": 26.4,
    "pct_cancelados": 4.6,
    "alertas": ["parálisis_procesos", "fraccionamiento_detectado"],
    "fuente": "SERCOP SOCE API",
    "fecha_corte": "2026-04-30"
  },

  "accountability": {
    "rdc": {
      "year": 2025,
      "componente_a": {
        "n_informe_cpccs": null,
        "fecha_ingreso": null,
        "en_periodo_cpccs": null,
        "asistentes": null,
        "lugar": null,
        "zona_rural": null,
        "plan_trabajo_publicado": null,
        "publicado_lotaip": null,
        "score": 0,
        "fuente": "pendiente_verificacion_cpccs"
      },
      "componente_b": {
        "video_url": null,
        "fecha_video": null,
        "plataforma": null,
        "duracion_min": null,
        "vistas": null,
        "score": 0,
        "fuente": "pendiente_verificacion_redes"
      },
      "score_total": 0,
      "clasificacion": "Pendiente",
      "nota": "Verificar en rendiciondecuentas.cpccs.gob.ec y redes oficiales del GAD"
    }
  }
}
```

---

## Próximos Scripts a Construir

| Script | Propósito | Prioridad |
|--------|-----------|-----------|
| `scripts/fetch_sercop.py` | Descarga PAC + estado procesos de SERCOP por RUC | Alta |
| `scripts/fetch_rdc_cpccs.py` | Verifica informe RdC en portal CPCCS por RUC + año | Alta |
| `scripts/enrich_snapshot.py` | Combina DPE + SERCOP + CPCCS en un snapshot completo | Media |
| `scripts/score_independiente.py` | Calcula scores TGI desde fuentes públicas únicamente | Media |

---

## Checklist de Onboarding para un Nuevo Municipio

Cuando RC-SCOUT identifica un municipio viable, el proceso completo es:

```
FASE 1 — RC-SCOUT (automatizado)
  [x] Validar viabilidad DPE (score >= 60)
  [x] Generar gm_snapshot_{municipio}.json base

FASE 2 — SERCOP (semi-automatizado)
  [ ] Descargar PAC del año vigente
  [ ] Consultar estado de procesos activos
  [ ] Calcular métricas de contratación
  [ ] Añadir sección "contratacion" al snapshot

FASE 3 — CPCCS RdC (semi-manual)
  [ ] Buscar informe en rendiciondecuentas.cpccs.gob.ec
  [ ] Registrar Componente A (n_informe, asistentes, lugar)
  [ ] Buscar video del evento en YouTube/Facebook del GAD
  [ ] Registrar Componente B (URL video, fecha, duración)
  [ ] Calcular score RdC total
  [ ] Añadir sección "accountability.rdc" al snapshot

FASE 4 — SIGAD ICM (manual)
  [ ] Consultar ICM del municipio en portalsigad.gob.ec
  [ ] Añadir al snapshot bajo "tgi.indicadores.ICM"

FASE 5 — Subir snapshot a QUIRA
  [ ] Validar snapshot en Panel de Carga
  [ ] Activar en sistema
  [ ] Generar primer análisis TGI
```

---

## Notas de Diseño

**¿Por qué YouTube/Facebook y no solo el formulario CPCCS?**
El formulario CPCCS es auto-declarativo — el GAD llena los datos. El video en redes es evidencia independiente y verificable. Si el formulario dice "261 asistentes" y hay un video de 2 horas con plenario real, hay coherencia. Si el formulario dice que se realizó el evento pero no hay ningún registro en redes sociales oficiales del GAD, eso es una señal de alerta que QUIRA debe capturar.

**¿Por qué no medir los informes mensuales de las direcciones?**
Porque hacerlo requeriría que el GAD nos los envíe — creando dependencia institucional que rompe el modelo independiente de QUIRA. La eficiencia directiva se mide a través de sus resultados en sistemas públicos (SERCOP adjudica, DPE publica, CPCCS tiene el informe). Si el director ejecuta, los sistemas lo reflejan. Si no, QUIRA lo detecta desde afuera.

**¿Qué pasa con municipios que no tienen redes sociales activas?**
El Componente B de RdC queda en "evidencia_no_encontrada" con score 0. Esto penaliza la transparencia digital sin bloquear el análisis — el municipio puede tener Componente A perfecto (65/100) y seguir siendo analizable.

---

*RC3_FUENTES_INDEPENDIENTES.md v1.0 · QUIRA OS · Dylus Lab © 2026-05-21*
