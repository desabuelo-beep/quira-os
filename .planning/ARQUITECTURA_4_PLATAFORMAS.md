# Arquitectura de 4 Plataformas QUIRA
## Decisión conceptual — 2026-05-28

**Estado:** DEFINIDA (conceptual) · implementación incremental  
**Fuente:** Sesión D.3a + análisis del colega + app.py preexistente  

---

## La Pregunta Resuelta

> ¿QUIRA es una plataforma, o es varias con identidad distinta?

**Respuesta:** Son 4 plataformas que comparten ontología, territorio, causalidad y Graphify.  
Cada una tiene una **intención de uso** distinta — no un tema distinto.

---

## Las 4 Plataformas

| Plataforma           | Pregunta que responde                        | Usuario primario                    | Estado        |
|----------------------|----------------------------------------------|-------------------------------------|---------------|
| **QUIRA Institucional** | ¿Cómo está funcionando el municipio?    | Alcalde · Directores · Concejo      | ACTIVO (GOV)  |
| **QUIRA Ciudadano**   | ¿Qué hace el municipio con mis impuestos?   | Ciudadano · Veedurías · CPCCS       | Roadmap       |
| **QUIRA Cooperación** | ¿Por qué invertir aquí?                     | BID · CAF · GIZ · COSUDE · ONGs     | Placeholder   |
| **QUIRA Operaciones** | ¿Está el sistema funcionando correctamente? | Equipo Dylus Lab · Administradores  | ACTIVO (OPS)  |

---

## La Diferencia Crítica: Intención, No Tema

El mismo dato puede vivir en las 4 plataformas con **lecturas completamente distintas**.

### Ejemplo: Cooperación Internacional

**En QUIRA Institucional:**
```
"Montecristi pierde elegibilidad CAF por ISP bajo"
"Gender Bond desbloqueable si PSG supera 30%"
"Fondos BID condicionados: $3.5M — requiere ISP > 65%"
```
→ Cooperación como **capacidad estratégica municipal**  
→ El alcalde necesita saber: ¿qué debo cambiar para desbloquear recursos?  
→ NO es portal internacional. NO es vitrina. NO es storytelling.

**En QUIRA Cooperación:**
```
"3 parroquias rurales cumplen criterios de financiamiento climático"
"Portafolio territorial elegible para fondos multilaterales"
"Brecha de inversión 5.4× entre cabecera y sector rural"
```
→ Cooperación como **evidencia para articular impacto**  
→ El organismo necesita saber: ¿este territorio justifica una inversión?  
→ Data room. Observatorio. Laboratorio territorial.

---

## La Analogía Exacta

| Plataforma           | Analogía                               |
|----------------------|----------------------------------------|
| QUIRA Institucional  | Cockpit del avión                      |
| QUIRA Ciudadano      | Tablero de llegadas/salidas público    |
| QUIRA Cooperación    | Presentación para inversionistas       |
| QUIRA Operaciones    | Torre de control                       |

---

## Cómo se Conectan

```
QUIRA Institucional detecta:
  → brecha + prioridad + readiness + elegibilidad

       ↓ (click / derivación)

QUIRA Cooperación articula:
  → "Portafolio territorial elegible para fondos climáticos"
  → tono diferente · visual diferente · narrativa diferente
```

El flujo correcto:
1. **Institucional** identifica la oportunidad o el riesgo
2. **Cooperación** construye la narrativa hacia el organismo
3. Comparten el mismo dato base — distinta intención

---

## La Visión Mayor

> "QUIRA puede convertirse en traductor entre territorio y financiamiento global."

América Latina tiene:
- Datos fragmentados
- Narrativa institucional pobre
- Cero traducibilidad entre municipios y financiamiento internacional

QUIRA puede ser la capa que convierte territorio en **activo legible** para cooperación global.  
Eso no es GovTech. Es **infraestructura de inteligencia territorial soberana**.

---

## Implicaciones para el Roadmap

### Para D.3b (Cooperación en QUIRA Institucional)
Debe sentirse como: **capacidad estratégica, no portal**

Elementos correctos:
- ¿Para qué fondos somos elegibles HOY?
- ¿Qué condiciones están bloqueando los recursos?
- ¿Cuánto se desbloquea si X indicador mejora?
- Causalidad: ISP ↓ → elegibilidad BDE ↓ → inversión rural ↓
- Llaves maestras: ISP 14.58%→65% · PSG 12.83%→30%

Elementos incorrectos para este contexto:
- Lista de organizaciones internacionales
- Descripción de programas
- Storytelling de impacto
- Vitrina institucional

### Para QUIRA Cooperación (futuro)
Debe sentirse como: **data room territorial para organismos multilaterales**

Usuarios: BID, CAF, GIZ, COSUDE, PNUD, ONGs, academia  
Tono: evidencia, rigor, narrativa de impacto  
Visual: diferente de QUIRA Institucional — más "observatorio", menos "sala de mando"

---

## Nota Técnica

Esta arquitectura ya existía implícitamente en `app.py` (líneas 7-10):
```python
🏛 GOV    — QUIRA Institucional · Ejecutivo + Técnico · ACTIVO
🌎 Civic  — QUIRA Ciudadano · acceso público · Fase 3
📑 Impact — QUIRA Cooperación · academia/cooperación · Placeholder
⚙  OPS   — Operaciones · Operador + Administrador · ACTIVO
```

La sesión D.3a clarificó la **intención de uso** de cada plataforma.  
La ontología y los datos (D.2) son el pegamento entre las 4.

---

*Documento de decisión conceptual. No requiere implementación inmediata.*  
*Referencia obligada al diseñar cualquier nuevo módulo o plataforma.*
