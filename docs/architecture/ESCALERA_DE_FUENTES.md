---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 4]
  type: OPERATIVA
---

# ESCALERA DE FUENTES — extracción con recursos limitados a escala nacional

**2026-07-27 · deriva de OBS-018 · conecta con el IOC (índice ya existente)**

> **NO es una capa nueva del ecosistema** (Principio de Subsidiariedad · Carta Art. 1.2): es una
> regla de procedimiento técnico que se apoya en artefactos que **ya existen** — el IOC del Gold
> Master (`H41_IOC_OPACIDAD_CRITICA`) y la clasificación documental del catálogo d08.

## El problema estratégico

QUIRA debe escalar a **222 GAD de Ecuador** y potencialmente **+6.000 gobiernos locales de LAC**.
Toda su evidencia llega en PDF, Word y Excel — mayoritariamente PDF, con calidad heterogénea.
Si cada dominio depende de resolver extracción caso por caso, el proyecto se consume en ingeniería
de documentos y nunca llega a producir inteligencia pública.

## La decisión: no competir en extracción

**QUIRA no compite en OCR.** Los modelos de extracción son *commodity* y están dominados por
actores con recursos incomparables. Invertir ahí es perder por definición.

**QUIRA compite en algo que nadie mide:** *¿qué proporción de la evidencia pública de un GAD es
verificable automáticamente?* Esa pregunta:
- se responde **sin costo adicional** (se sabe al intentar extraer);
- es **comparable entre los 222 GAD** con la misma regla;
- es un **indicador real de madurez digital y de opacidad técnica**;
- **nadie más la está midiendo**.

> **La falencia se convierte en el dato.** Si un GAD publica únicamente PDF escaneado sin capa de
> texto, eso no es un problema técnico de QUIRA: es **opacidad técnica del GAD**, y es medible.
> Es el concepto *"el silencio como dato"* (Marco Teórico) aplicado al formato del documento.

## Los patrones reales de opacidad técnica *(aporte de Javo · 15 años en GAD)*

La ingesta **no es un problema técnico secundario: es el cuello de botella estructural nº 1 de la
gobernanza pública en Ecuador**, y el obstáculo real del DOM Transparencia al escalar a 222 GAD.

La **Guía Metodológica Integral de la LOTAIP 2024 exige datos abiertos y reutilizables**. Frente a
eso, la práctica municipal produce patrones identificables:

| Patrón | En qué consiste | Por qué importa |
|---|---|---|
| **Excel Cáscara** | el GAD sube la matriz Excel que exige el Numeral 10 (Planes y Programas), pero dentro **solo hay un enlace** a un PDF en Drive o en su servidor | cumple la forma, no el fondo |
| **PDF Trampa** | el enlace lleva a un documento **impreso y escaneado a 150 DPI** | ilegible para máquina — no es dato abierto |
| **Archipiélago de formatos** | CPCCS en PDF propio · SERCOP en PDF · portal del GAD con **accesos rotos** | fragmentación intersistémica (Postulado II) |

> **Consecuencia normativa:** si la LOTAIP 2024 exige datos **abiertos y reutilizables**, publicar
> un PDF ilegible **no es cumplir: es simular cumplimiento**. Eso convierte la opacidad técnica en
> un **hallazgo normativo verificable**, no en una queja de ingeniería.

**Dónde se audita:** el **DOM Transparencia (d07)** tiene ese trabajo — recorre el portal, sigue
los enlaces y registra el estado. d08 y los demás dominios *consumen* la evidencia; d07 *califica
cómo fue publicada*.

## La escalera de ingesta — buscar siempre el peldaño más alto disponible

| Nivel | Fuente encontrada | Acción del motor | Impacto en el ecosistema |
|---|---|---|---|
| **1 · Óptimo** | `.xlsx` / `.csv` nativo | extracción automática, ingesta directa al canon | **verificabilidad alta (100%)** |
| **2 · Aceptable** | `.pdf` con capa de texto | extracción determinística de texto | verificabilidad directa |
| **3 · Fricción** | `.pdf` escaneado (imagen) | OCR local ligero (Tesseract, gratis) **+ alerta de fricción** | **evidencia con fricción** — se declara |
| **4 · Opacidad** | enlace roto · archivo corrupto · escaneo ilegible | registra **ausencia de habilitación documental** | **castiga el IOC** (`H41`) |

El sistema **NUNCA falla ni se detiene**: marca `ESTADO_EXTRACCION: OPACIDAD_TECNICA_DOCUMENTAL`
y continúa. El fallo es el dato.

### Regla operativa (nace de OBS-018)
> **Antes de recurrir a OCR o a un corpus derivado, verificar si existe la fuente en un peldaño
> superior.** El GAD casi siempre tiene el XLSX aunque publique el PDF: se solicita por acceso a
> información pública.

En el cruce de d08 se usó un corpus vectorizado (nivel 4, corrupto) cuando el XLSX oficial
(nivel 1, limpio) estaba disponible. El canon ya advertía la corrupción y no se consultó. Esa es
exactamente la pérdida de tiempo que esta escalera evita.

### Regla de honestidad
El fallo de extracción **nunca se oculta ni se rellena con inferencias**: se registra con su nivel
y alimenta el indicador de opacidad. Un documento que no se pudo procesar es evidencia sobre el
GAD, no un hueco en QUIRA (Horizonte de Verdad · Principio de No-Inferencia).

## Conexión con artefactos existentes *(no se crea nada nuevo)*

| Ya existe | Se usa para |
|---|---|
| `IOC` — Índice de Opacidad Cantonal (`H41_IOC_OPACIDAD_CRITICA`, Gold Master) | recibir la proporción de evidencia no procesable como componente de opacidad técnica |
| `clasificacion_documental` (catálogo d08) | vocabulario ya definido: `procesable · ocr_certificado · parcial · no_localizada` |
| `extract_poa_pdf.py` · `enrich_*_docx.py` | extractores por nivel, ya operativos |

**Pendiente de decisión de Javo (Regla 1):** si la proporción de evidencia no procesable debe
incorporarse como componente del IOC, esa fórmula **se sella en el Gold Master**, no en QUIRA.
Aquí solo se produce el dato.

## Por qué esto es ventaja competitiva y no un parche

Un competidor puede comprar mejor OCR. **No puede comprar la serie histórica de qué tan
verificable ha sido la información pública de 222 cantones a lo largo de los años** — eso es
patrimonio cognitivo acumulado (Constitución Art. 19 · *longitudinalidad*).

La extracción es un medio. **La medición de la extractibilidad es el activo.**

---
*Escalera de Fuentes · Dylus Lab © 2026 · deriva de OBS-018 · alimenta el IOC.*
