# B.1A — AUDITORÍA TEMÁTICA DEL CORPUS PDOT
**Sprint B · QUIRA OS · 2026-06-09**
*Pregunta: ¿la información territorial existe en el PDOT o realmente falta?*
*Método: barrido del corpus narrativo Supabase (PDOT-MONTECRISTI 594 chunks ·
PLAN-BICENTENARIO-MCR 824 · PAI-PLURIANUAL-GAD 169 = 1,587 chunks) ·
script `scripts/sprint_b/b1a_auditoria_pdot.py`*

---

## Veredicto ejecutivo

La sospecha del Colega se confirma **a medias — y la mitad confirmada vale meses**:

> **Movilidad y Ambiente NO son gaps de datos. Son gaps de EXTRACCIÓN.**
> **Género territorial SÍ es un gap real de datos** (verificado en doble fuente).

| Tema | Chunks | × parroquia nombrada | Veredicto |
|---|---|---|---|
| **Ambiente** | 211 | **65** | 🟢 RIQUEZA NO EXTRAÍDA — territorializado, sin explotar |
| **Movilidad** | 211 | **49** | 🟢 RIQUEZA NO EXTRAÍDA — vial documentado por tramo |
| **Residuos** (caso 06) | 158 | — | 🟢 MATERIAL ABUNDANTE — tonelajes por tipo, cobertura 96 % |
| **Juventud** | 67 | 13 | 🟡 PARCIAL — demografía territorial sí; tasa de empleo no |
| **Cooperación** | 48 | — | 🔴 DÉBIL en PDOT — pero D02 ya cubre por otra vía |
| **Género** | 18 | **0** | 🔴 GAP REAL — el PDOT no territorializa género |

---

## Hallazgos por tema

### 1. Género — G-09 confirmado como gap REAL, con una veta nueva

- 18 chunks de 1,587 (1.1 %) tocan género; **cero** lo cruzan con una
  parroquia nombrada. Coincide con el KB estructurado (0 filas). Doble
  fuente verificada: **la desagregación territorial de género NO está en
  el PDOT** — hay que buscarla afuera (censo INEC parroquial, DINASED, MSP).
- **HALLAZGO NUEVO — veta de protección de derechos (61 chunks):** la Junta
  Cantonal de Protección de Derechos registra serie 2022→2023:
  **casos de Mujer 120 → 198 (+65 % en un año)** · NNA 160 → 190 ·
  Adulto Mayor 9 → 17 · Bono Mil 8 → 52. Es un indicador de DEMANDA de
  protección con tendencia — cantonal, pero con valor y serie. FICHA-03
  decía "se interviene sobre un problema que no se mide": matiz — la Junta
  Cantonal SÍ mide demanda, y crece. **Extraer ya.**
- Segundo dato nuevo: **66.25 % de los casos de morbilidad registrados
  corresponden a población femenina** (PDOT, sistema sociocultural).

### 2. Movilidad — el pronóstico 🔴 de FICHA-04 era pesimista

211 chunks, 49 con parroquia nombrada: tablas de estado de vías, jerarquía
vial, tramos con longitud y tipo de pavimento, conectores de alto flujo,
clasificación urbana por parroquia. **La movilidad VIAL (infraestructura)
está documentada por tramo.** La frontera probable se desplaza a movilidad
de PERSONAS (transporte público, frecuencias, accesibilidad) — eso sí puede
no estar. FICHA-04 pasa de 🔴 a 🟡 con sección vial fuerte.

### 3. Ambiente — la mayor riqueza no explotada (y no está en la matriz)

211 chunks, 65 con parroquia: clases agrológicas de tierra, ecosistemas
frágiles no protegidos, datos de caracterización de residuos con tonelajes
por tipo (PET/cartón/plásticos/papel/lata). **Es el tema con mejor ratio
territorial del corpus y no tiene caso en la matriz ni dominio fuerte en el
motor** — exactamente lo que Javo señaló como flojo en el Gold Master.

### 4. Juventud — mixto

67 chunks, 13 con parroquia: estructura poblacional por unidad territorial,
atenciones CDBV, denuncias NNA. La demografía juvenil territorial es
extraíble. La **tasa de desempleo juvenil no existe en el PDOT** (es dato
ENEMDU/INEC) — esa parte de FICHA-05 sigue 🔴 y requiere fuente externa.

### 5. Cooperación — débil en PDOT, cubierta por D02

48 chunks reales (corrección metodológica: el conteo inicial de 120 estaba
contaminado — el término "ONG" matchea dentro de "l**ong**itud"). El PDOT
menciona cooperación como función del equipo, no como datos operables.
La fuente real de cooperación ya está construida: base de fondos D02.

### 6. Residuos — caso 06 con material asegurado

158 chunks: caracterización con tonelajes por tipo de material, cobertura
de recolección 96 % (2022, serie desde 78.3 % en 2010 ya vista en KB).

---

## Reclasificación de gaps (actualiza fichas 01-03)

| Gap | Era | Ahora |
|---|---|---|
| G-09 género territorial | Dato (crítico) | **CONFIRMADO gap real** — doble fuente. Ruta: censo INEC (jefatura parroquial, fuente pública) + DINASED/MSP (vía pública o D12-003 al descongelar) |
| G-09 género cantonal | — | **NUEVO sub-hallazgo:** Junta Cantonal 120→198 + morbilidad 66.25 % fem. — EXTRAÍBLES HOY del corpus |
| Movilidad (pre-FICHA-04) | presunto gap de dato | **Gap de EXTRACCIÓN** — 211 chunks/49 parroquiales sin estructurar |
| Ambiente | (sin caso) | **Gap de EXTRACCIÓN + gap de matriz** — candidato a caso 07 o refuerzo Gold Master |
| Juventud demografía | presunto gap de dato | Gap de extracción (parcial) |
| Juventud tasa empleo | — | Gap real — fuente ENEMDU/INEC externa |

## Insumo para la revisión del Gold Master (pedido de Javo)

Los dominios flojos tienen perfiles distintos — la revisión debe tratarlos distinto:

| Dominio flojo | Perfil del corpus | Estrategia de refuerzo |
|---|---|---|
| Ambiente | Rico y territorial (211/65) — sin explotar | EXTRAER del PDOT → proponer indicadores al Excel |
| Género | Pobre y no territorial (18/0) | Fuentes externas (INEC/DINASED) + institucional ya existe (PSG) |
| Cooperación | Casi nulo en PDOT (48) | D02/fondos_radar ya es la fuente — afinar reglas en Excel |
| Bonos/financiamiento | No es tema PDOT | Reglas D02 + requisitos completos (G-01) |

**La revisión del Excel es decisión de mesa (Javo + Director) con este mapa como insumo.**

## Recomendación de continuación

1. **FICHA-04 Movilidad** — proceder ya, con pronóstico revisado 🟡 (vial fuerte).
2. **FICHA-05 y 06** — proceder en secuencia.
3. **B.2 agrega dos extracciones de alto valor:** (a) Junta Cantonal serie
   protección → FICHA-03; (b) paquete vial parroquial → GeoTwin.
4. **Caso 07 Ambiente** — proponer a la mesa si entra a la matriz (el corpus
   lo sostiene; el motor hoy no).

---

*B.1A · Sprint B · QUIRA OS · Dylus Lab © 2026 — script reproducible en
`scripts/sprint_b/b1a_auditoria_pdot.py`*
