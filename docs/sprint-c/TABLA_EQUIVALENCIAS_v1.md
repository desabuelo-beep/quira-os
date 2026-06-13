# TABLA DE EQUIVALENCIAS QUIRA v1.0 — PROPUESTA
**Sprint C · C.0 · 2026-06-12 · PROPUESTA para ratificar en mesa (Javo + Colega + Director)**

> El documento más importante del refactor L2 (voto del Colega). Sin él, la
> nomenclatura prohibida reaparece en cada pantalla y se corrige 14 veces.
> **Estado: PROPUESTA.** Nada se aplica a dashboards hasta ratificación.
> Construida sobre nombres que YA existen (`demo_data.INDICES` + Nomenclatura
> Canónica) — no inventada. Lo que no se sabe con certeza, se marca ⚠️, no se alucina.

---

## La regla madre (3 categorías, no 1)

No todo "se traduce". Hay TRES destinos para cada término:

```
A · TRADUCIR        tiene nombre público de gobernanza → se muestra el público
B · NUNCA VISIBLE   jamás en UI bajo ninguna forma → se omite o se habla del concepto
C · YA PÚBLICO      estándar oficial que el usuario conoce → se mantiene tal cual
```

---

## CATEGORÍA A — TRADUCIR (se muestra el nombre público)

*Matiz de director: el mismo índice puede tener nombre distinto según el producto.
QUIRA Institucional (pantalla del alcalde) evita lenguaje acusatorio; QUIRA
Ciudadana puede ser más directa. Regla de oro: NUNCA "incumplió/violó/ilegal".*

| Interno (PROHIBIDO en UI) | Nombre actual (demo_data) | ✅ Público — Institucional | ✅ Público — Ciudadana |
|---|---|---|---|
| ICPI | — | Cumplimiento Institucional | Cumplimiento de la gestión |
| SAT | — | Alertas Institucionales | Alertas de gestión |
| Ti | — | Ejecución presupuestaria | Cuánto se ha gastado de lo planificado |
| TOP | (Trayectoria Operativa Proyectada) | Trayectoria de cumplimiento | ¿Va por buen camino? |
| ISP | Salud Presupuestaria | Sostenibilidad presupuestaria | Salud de las finanzas |
| IED | Eficiencia Direcciones | Eficiencia de gestión | Eficiencia de las áreas |
| IGP | Gobernanza Participativa | Participación ciudadana | Cuánto participa la gente |
| PSG | Presupuesto Género | Presupuesto con enfoque de género | Inversión en igualdad |
| ITAM | Transparencia Municipal | Transparencia activa | Qué tan transparente es |
| IOC | Opacidad Crítica | Transparencia pendiente *(no "opacidad" — acusatorio)* | Información que oculta |
| IET | Equidad Territorial | Equidad territorial | Reparto justo entre parroquias |
| ICODS | Cumplimiento ODS | Alineación con ODS | Compromisos globales (ODS) |
| IFE-A | Fidelidad Electoral | Cumplimiento del plan de campaña | Promesas cumplidas |
| IFE-E | Fidelidad Ejecución | Fidelidad de ejecución | Lo prometido vs lo hecho |
| NBI | — | Necesidades Básicas Insatisfechas *(ver Cat. C — estándar INEC)* | Pobreza por servicios |
| TPS | — | Déficit de servicios básicos | Hogares sin servicios |

---

## CATEGORÍA B — NUNCA VISIBLE (se oculta el nombre; se habla del concepto)

Estos términos **jamás aparecen en UI**, ni traducidos. Se habla del concepto
sin nombrarlos (ej. no "el Gold Master calcula" sino "el sistema determina").

| Interno | Por qué nunca | Cómo referirse al concepto (si hace falta) |
|---|---|---|
| Gold Master · SIAP-ICPI | motor propietario (caja negra) | "el motor de indicadores" / "el sistema" |
| H01–H99 / H73 | nodos internos del motor | (omitir) |
| Dom01–Dom12 | IDs de dominio | el nombre del dominio en lenguaje humano |
| C01–C99 | IDs de circuito causal | (omitir — hablar del fenómeno) |
| CE_xxx | IDs de nodo de evidencia | (omitir) |
| ACK | ontología propietaria | (omitir) |
| QTMP | protocolo interno | (omitir) |
| MNT_UUID | id de trazabilidad | (omitir — la trazabilidad existe, no se nombra) |
| AVEP / MMP | estados/métricas internas | ⚠️ confirmar significado con Javo antes de decidir |
| node IDs (Dom07·C01·CE_226) | identificadores internos | jamás |

---

## CATEGORÍA C — YA PÚBLICO (se mantiene tal cual — el usuario lo conoce)

Estándares oficiales ecuatorianos/internacionales. Cambiarlos confundiría.

`PDOT` · `PUGS` · `PAC` · `POA` · `NBI` (INEC) · `ODS` · `LOTAIP` · `COOTAD` ·
`CPCCS` · `CNE` · `SERCOP` · `eSIGEF` · `MIDUVI/MIES/SEPS` · `RDC` (rendición de cuentas)

*Regla: si es una sigla que un técnico municipal o ciudadano ya usa en su día a
día, se mantiene. Si es una sigla que solo existe dentro de QUIRA, va a A o B.*

---

## ⚠️ DECISIONES QUE NECESITAN A JAVO (no las invento)

1. **TGI** — aparece en el header canónico ("GAD · TGI · SAT") y en el nombre del
   Gold Master (v5.5_TGI). No tengo su significado exacto confirmado. ¿Qué es y
   cómo se llama en público? (¿"Gestión Territorial Integral"?)
2. **TOP** (Trayectoria Operativa Proyectada) — ¿se muestra el nombre "Trayectoria
   de cumplimiento" o solo el semáforo sin nombre técnico?
3. **ICPI público** — propongo "Cumplimiento Institucional" (ya usado en cajones v2).
   ¿Se ratifica como el nombre oficial público del índice madre?
4. **AVEP / MMP** — confirmar qué son para decidir A o B.
5. **¿Mostrar índices como sigla + nombre, o solo nombre?** Ej. "Transparencia
   activa: 56" vs "ITAM: 56". Propongo: SOLO nombre en Institucional/Ciudadana;
   la sigla puede vivir en el pie técnico de Operaciones (rol interno Dylus).

---

## Cómo se usa esta tabla en el refactor

1. Se ratifica (esta sesión de mesa).
2. Cada dashboard refactorizado aplica la columna del producto que le toca.
3. El gate Bloomberg de cada pantalla = 0 términos de Categoría A sin traducir y
   0 términos de Categoría B visibles.
4. `scripts/dev/audit_bloomberg_l2.py` verifica automáticamente.

---

*Tabla de Equivalencias QUIRA v1.0 · PROPUESTA · Dylus Lab © 2026 · ratificar antes de aplicar.*
