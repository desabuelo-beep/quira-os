# PROTOCOLO DE CURACIÓN DE DOMINIO (PCD)

> **Doctrina (asesor + Javo · 2026-07-02):** No hacemos mantenimiento ni corregimos bugs.
> Hacemos **segunda ingeniería**: *auditar, curar y potenciar el ecosistema completo,
> empezando SIEMPRE desde el canon y siguiendo toda la cadena hasta la visualización final.*
> Se trabaja **dominio por dominio**, no pantalla por pantalla.

## 0 · El canon (fuente de verdad)
El canon NO es solo un archivo Excel. Es:
- **Gold Master (SIAP-ICPI v5.5)** — las **métricas** (ICPI/TGI/SAT, IPE, fidelidad `IF_n`, cumplimiento). Núcleo epistemológico del motor.
- **Corpus verificado (Supabase · SHA-256)** — los **documentos** (normativa, informes RDC, PDOT…).

Todo lo demás —snapshot, motores, cableado, UI, narrativa— **DERIVA** del canon. **Nunca inventa un segundo canon.**

## 1 · La cadena del dominio (nunca se saltan capas)
```
Gold Master / Corpus verificado
        │
        ▼
Auditoría metodológica  →  Corrección / potenciación del canon
        │
        ▼
Regeneración de dumps  →  Regeneración del snapshot
        │
        ▼
Motores matemáticos  →  Motores interpretativos (IA)
        │
        ▼
Cableado del cajón  →  Auditoría visual (UI/UX)
        │
        ▼
Patrón definitivo  →  PCD-DXX (documentación del dominio)
```

## 2 · La auditoría de 7 capas (reemplaza a "auditoría visual")
1. **Gold Master** — fórmulas · relaciones · consistencia · duplicados · métricas · lógica.
2. **Metodológica** — ¿la metodología sigue siendo la mejor? Si hoy sabemos algo mejor, se incorpora. **Nunca se rompe compatibilidad** (H12!B33 inmutable).
3. **Matemática** — ¿el indicador representa de verdad lo que dice? *No se acepta un proxy solo porque "funciona"* (caso IPE: ×0.84 → fórmula nativa `SUMAPRODUCTO`).
4. **Semántica** — nombres · conceptos · definiciones · relaciones · eliminar redundancias (Regla #7 anti-inflación).
5. **Cableado** — que la información viaje Excel/Corpus → Snapshot → Motor → Pantalla **sin pérdidas**.
6. **Visual (UI/UX)** — recién aquí entra la UI. No antes.
7. **Narrativa** — que el texto **explique** el dato (no adorne), a nivel de administración pública, con fundamento legal verificado.

## 3 · Reglas que nacen de este protocolo
- **R-A · Segunda ingeniería:** el propósito es *curar y potenciar todo*, no mantener.
- **R-B · Ningún cambio nace en Python.** Todo cambio **conceptual** (métrica, fórmula, definición) nace en el **canon** (Gold Master o corpus verificado). Python solo **implementa o deriva**. El código es reflejo del canon, jamás un segundo canon.
  *(Corolario: las cruces que "el Excel no cruza solo" —puentes de partidas, SERCOP— DERIVAN de datos del canon; no inventan verdad. Si una cruz se vuelve métrica de record, se estampa/formula en el canon, como el IPE.)*

*(Ratificación de R-A/R-B como Reglas de Oro en `CLAUDE.md` / `BOOT.md`: pendiente de Javo — son archivos congelados, Regla 5.)*

## 4 · Plantilla PCD-DXX (cada dominio cierra con su documento)
Cada cajón termina con `docs/pcd/PCD-DXX_<Dominio>.md`, con secciones:
- **Estado inicial** — cómo estaba el dominio.
- **Hallazgos** — lo que la auditoría de 7 capas reveló.
- **Cambios** — metodológicos · matemáticos · semánticos · visuales · narrativos.
- **Cambios en el canon** — Gold Master (hojas/fórmulas) · Corpus · Snapshot · Motores · UI.
- **Validación** — verificación (dumps, gates B33/guardián, Excel↔Python, render, firewall).
- **Estado final** — cómo quedó, y por qué quedó exactamente así.

Objetivo: que dentro de un año cualquiera pueda responder *"¿por qué este dominio quedó así?"* con trazabilidad completa.

## 5 · Estado de aplicación
| Dominio | PCD | Estado |
|---|---|---|
| d01 Planificación | [`PCD-D01`](../pcd/PCD-D01_Planificacion.md) ✅ redactado | Cerrado de cabo a rabo · IPE nativo en Excel |
| d09 Rendición de Cuentas | en curso | Re-aproximar por las 7 capas (auditar hojas H31/H34b/H10/H24b primero) |

---
*Protocolo de Curación de Dominio · Dylus Lab © 2026 · asesor externo + Javo + Claude (director técnico).*
