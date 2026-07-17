# PROTOCOLO · Puente de Conocimiento Lexis IA → BRN (Javo · 2026-07-17)

**Estado:** vigente · procedimiento operativo · complementa ADR-038 (BRN) y ADR-005 (corpus).
**Fin:** poblar el **Corpus Jurídico Nacional** (Nivel 0) con toda la norma que genera obligación
operativa, en calidad de fuente para las CNO de la BRN — **sin errores de escaneo y actualizada**.

---

## Por qué Lexis

Lexis posee la **normativa nacional completa, codificada, actualizada a 2026 y libre de errores
de OCR**. Es la mejor materia prima disponible en el país. El problema no es de datos —los tiene
Lexis— sino de **puente**: Lexis IA no se conecta por código a este sistema. **Javo es el
orquestador del puente**: Lexis IA actúa como *procesadora de materia prima*; el Claude del
proyecto, como *arquitecto* que audita y estructura. Es el ADR-035 §5 en acción — la IA (Lexis)
propone la cadena; el humano (Javo) y el arquitecto la validan antes de que entre al canon.

## El protocolo (3 fases)

```
[ FASE 1 · Claude ]              [ FASE 2 · Lexis IA ]            [ FASE 3 · Claude ]
 genera la ORDEN de       ➔      extrae la CADENA de       ➔      recibe, AUDITA y
 investigación                   artículos vinculados,            consolida la CNO
 (por eje jurídico GAD)          en Markdown limpio               lista para el corpus
```

### FASE 1 · La orden de búsqueda (Claude genera)
No se pide "un artículo". Se pide una **red normativa** por **eje jurídico del GAD** (finanzas
municipales, planificación, contratación, participación, talento humano, transparencia…). La
orden obliga a Lexis a buscar la **cadena completa**, no piezas sueltas:
- norma raíz + **todas** sus reformas vigentes a 2026,
- artículos concordantes (la propia norma los cita: "en concordancia con…"),
- **disposiciones transitorias** aplicables,
- reglamentos, acuerdos, **metodologías y procedimientos** que la operativizan,
- fecha de vigencia y estado (vigente / derogado / suspendido).
> Antídoto contra el error del 65%: la orden **prohíbe** entregar un artículo sin su cadena.

### FASE 2 · El extractor de EVIDENCIA (en Lexis IA)
**Lexis no propone la cadena — propone EVIDENCIA** (precisión del colega · 2026-07-17: la cadena
responde a una decisión metodológica de QUIRA, no de Lexis; construirla en Lexis cedería la
soberanía metodológica). Lexis devuelve **el texto** en Markdown limpio, un bloque por artículo,
con: norma · artículo · texto literal · fecha de vigencia · reforma que lo modificó (si aplica).
**La CADENA la arma QUIRA** en Fase 3, decidiendo qué eslabones la componen. Ese Markdown es
**materia prima** —aún no es canon—.

### FASE 3 · Consolidación en la BRN (Claude, de vuelta)
El arquitecto:
1. **audita** la cadena contra el corpus existente (¿ya está? ¿coincide el texto? ¿falta un
   eslabón?),
2. **ingesta** al Corpus (Nivel 0) lo que falte, vía la infraestructura ya existente
   (`scripts/normativa/ingest.py` · `chunker.py` · `manifest.py`) — cada chunk con su **SHA256**,
3. **propone** la **CNO** (Nivel 1: la cadena) y la **Regla Operativa** (Nivel 2: variable ·
   umbral · periodo · consecuencia), en estado `propuesta`,
4. **Javo valida** → la CNO/RO pasa a `vigente` (ADR-035 §5 · ADR-038). Ninguna entra sin su firma.

## Líneas rojas (heredadas del canon)
- **El texto oficial es de Lexis; la verdad es el SHA.** Todo eslabón se ingesta al corpus con su
  huella; nada "queda en Lexis". Si no está en el corpus verificado, no sostiene una CNO (Regla 3).
- **Lexis propone, Javo valida.** La IA de Lexis nunca declara una regla vigente — solo aporta el
  texto. La derivación a CNO/RO la audita el arquitecto y la ratifica Javo (ADR-035 §5).
- **Se sube por eje jurídico, no por volumen.** No "todo Lexis de una vez": se traen las cadenas
  de los ejes que los DOM ya consumen, empezando por **Finanzas Públicas Municipales** (el eje del
  65%, ya en curso).

---
*Protocolo Puente Lexis → BRN · Dylus Lab © 2026 · "Lexis tiene el Derecho sin errores; QUIRA lo vuelve operativo. Javo es el puente — y el único que dice qué regla queda vigente."*
