# Auditoría Canónica de los 13 Cajones — Matriz de Curación y Cosecha

**2026-06-21 · Sprint D · fase CURAR (no crear) · mesa (colega + académico + Javo)**
**Rector del contenido:** `DICCIONARIO_CONCEPTUAL_QUIRA.md` (13 ADN sellados · fuente única).
**Rector de la forma:** `ADR-030` (Variante A · 50/50 · QUIRA IA = criterio). **Método:** cosecha (`PLANO_DE_CAJONES`).

> **No hay nada que inventar.** Todo el ADN ya existe y está anclado al motor. Esto es curación:
> qué se conserva de la cantera, qué se purga, qué brecha real nos separa del canon. Cero pixeles a ciegas.

## 🏛️ Regla de Derivación Canónica (axioma anti-amnesia · adoptado)

Antes de crear/definir cualquier concepto, todo agente (humano o IA) responde **5 preguntas**:
1. **¿Existe ya?** → `graph query` / Diccionario / Atlas.
2. **¿Dónde vive?** (documento)
3. **¿Quién es su rector?**
4. **¿Qué documento tiene autoridad?**
5. **¿Lo que voy a escribir DERIVA o REDEFINE?**

→ Si la respuesta es **REDEFINE → DETENERSE.** Se extrae del rector (símbolo único e inmutable). El grafo es
**autoridad**, no solo navegación. *(Esta regla nació porque la RdC y los 13 ADN se re-derivaron sin recordar
que ya estaban sellados. Cada concepto cuenta: si aparece dos veces, se paga dos veces.)*

## 📊 La Matriz (rector = Diccionario · estado = código vivo `p_command_center_v2.py`)

| # | Dominio canónico (rector) | UI actual | Conserva (cosecha) | Purga | Brecha (trabajo) |
|---|---|---|---|---|---|
| d01 | Planificación Estratégica | ✅ nombre OK | cálculo 4 ejes + metas PDOT (`p11_ods`·`p8_metas`) | botón "abrir" · textos marketing | render Variante A |
| d02 | Presupuesto & Financiamiento | ✅ nombre OK | pipeline financiero + radar D02 (`p18_cooperacion`) | widgets amontonados | dashboard 50/50 · *(devengado eSIGEF 2026 PENDIENTE)* |
| d03 | **Gobernanza del Mandato** | ⚠ dice "Metas PDOT·Mandato" | matriz CNE↔PDOT · IFE-A (`p8_metas`·`p_concejo`) | nombre viejo | **renombrar** + Variante A |
| d04 | Alertas Institucionales | ✅ nombre OK · dinámico | monitor SAT (`m2_alertas`·`p9_sat`) | texto superficial | pregunta macro-causal · *(matriz riesgo HARDCODED→`H75`)* |
| d05 | Holding e Integración Municipal | ⚠ **COMODÍN** | consolidación 4 entidades (`p2_holding`·`m3_municipal`) | **adelgazar:** RdC→d09 · Participación→d08 | redistribuir + Variante A |
| d06 | Salud Institucional | ✅ nombre OK | diagnóstico 41 métricas · síntesis (`m1_situacion`·`p7_brecha`·`p_ejecutivo`) | slogans · 2 rutas de datos a unificar | mapa de causalidad (enlaza a otros · no aislado) |
| d07 | Transparencia | ✅ nombre OK | evidencias + links LOTAIP (`p07_transparencia`) | fila redirección genérica | card clicable + Variante A |
| d08 | Participación Ciudadana | ✅ nombre OK | asambleas·PP·actas (`p16_gobernanza`·`p16_confianza`) | duplicados del menú viejo | **cosechar lo que estaba en Holding** |
| d09 | Rendición de Cuentas | ⚠ contenido inventado | circuito C-RDC (`p17_rdc`) + lo que estaba en Holding | **destruir ~70%** marketing actual | **RECONSTRUIR:** congruencia Gestión→CPCCS→Discurso + NLP |
| d10 | **Cobertura de Servicios e Infraestructura** | ⚠ dice "Territorio & Cobertura" | cobertura/parroquias (`p10_territorio`·`p10_inversion`) | nombre viejo · texto redundante | **renombrar** + Variante A + pregunta itálica al pie |
| d11 | Desarrollo Económico Territorial | ✅ deshabilitado seguro | esqueleto de variables (corpus PDOT) | nada | mantener bloqueo · *(campo verde · NO inventar madre)* |
| d12 | **Inclusión, Equidad y Género** | ⚠ dice "Protección Social & Grupos Prioritarios" | métricas PSG (`p19_genero`) | descriptor superficial | **renombrar** + Variante A · *(IGM/ODS5 MISSING externos)* |
| d13 | **Sostenibilidad y Resiliencia Ambiental** | ❌ **NO EXISTE (gap absoluto)** | modelo Atlas + corpus biofísico/riesgo (sellado) | nada | **CREAR el cajón 13** en la grilla *(ICODS sub-eje a precisar)* |

## 🧮 Resumen del trabajo (3 tipos · ninguno inventa contenido)

1. **Sincronizar la grilla** — 12 → **13 cajones**; renombrar **d03·d10·d12** al Nomenclátor; inyectar **d13**.
2. **Adelgazar Holding (d05)** — retirar RdC/Participación (viola sus Exclusiones · ADN campo 8) → cosechar en **d09** y **d08**.
3. **Aplicar el molde (ADR-030)** — el loop de render lee el ADN y dibuja la card Variante A (full-card click); dashboards por ola con cosecha + dashboard 50/50.

## 🛫 Orden de construcción (cuando se apruebe pasar a código)
sincronizar nombres+13 → A1 card (Variante A) → 4 Dominios de Exploración → dashboards por ola (cosecha):
**Ola 1** d06·d02·d10 (núcleo ejecutivo · CAF) → **Ola 2** d13·d12·d03 → **Ola 3** el resto. **d09 RdC** = reconstrucción dedicada. Verificación en deploy obligatoria por cajón.

---
*Auditoría Canónica v1 · Dylus Lab © 2026 · "No inventamos nada: el ADN ya existe. Curamos: conservar, purgar, sincronizar. El que redefine, se detiene."*
