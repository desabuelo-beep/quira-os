# TOP — Trayectoria Operativa Proyectada
**QUIRA_DOCTRINE_v1.3 · Sección 1.6**
**Motor Predictivo Institucional v1 — Sprint B**

---

## Definición canónica

**TOP (Trayectoria Operativa Proyectada)** es la métrica nuclear del Motor Predictivo Institucional de QUIRA. Mide si una institución avanza al ritmo requerido para cumplir su presupuesto anual, ajustado al comportamiento histórico de ejecución ecuatoriana por trimestre.

> TOP no mide cuánto has ejecutado.  
> TOP mide si vas a llegar.

---

## Fórmula

```
TOP = Ti_acumulado / W_Q
```

Donde:
- **Ti_acumulado** = % de ejecución (devengado/codificado) acumulado al corte
- **W_Q** = peso estacional del quarter (calibrado con datos eSIGEF Ecuador)

---

## Constantes W_Q — inmutables

Calibradas con el comportamiento real del sistema eSIGEF Ecuador. Reflejan el "letargo administrativo" del inicio fiscal y la aceleración del cierre.

| Quarter | W_Q  | Explicación |
|---------|------|-------------|
| Q1      | 0.13 | Letargo administrativo — contratos, procesos, arranque |
| Q2      | 0.35 | Aceleración operativa — obras en marcha |
| Q3      | 0.60 | Ejecución sostenida — cierre de etapas |
| Q4      | 1.00 | Cierre fiscal — el peso es la identidad |

**Propiedad W_Q:** `Q1 < Q2 < Q3 < Q4 = 1.00` — monótonamente creciente.  
**En Q4:** TOP = Ti (el divisor es 1, identidad perfecta).

---

## Umbrales canónicos (NOMENCLATURA 7.2)

| TOP       | Categoría     | Color   | Icono | Interpretación |
|-----------|---------------|---------|-------|----------------|
| ≥ 75%     | `sostenible`  | #22C55E | 🟢    | Trayectoria al ritmo esperado |
| ≥ 55%     | `atencion`    | #F59E0B | 🟡    | Monitoreo activo — puede recuperar |
| ≥ 35%     | `alerta`      | #F97316 | 🟠    | Riesgo de incumplimiento — acción preventiva |
| < 35%     | `ruptura`     | #EF4444 | 🔴    | Trayectoria rota — intervención urgente |

---

## Regla de cap — TOP > 100% (DOCTRINA)

Cuando TOP supera 100%, la institución va **sobre ritmo esperado**. Esto es matemáticamente válido y metodológicamente correcto.

**Regla de visualización:**
- `sobre_ritmo = True` cuando TOP > 100
- `top_display = None` — NO mostrar el número
- Mostrar label: **"Sobre ritmo esperado"**

**Razón doctrinal:** Mostrar "150%" o "230%" genera confusión política en Concejo. El alcalde no necesita el número exacto; necesita saber que esa entidad está bien y puede avanzar.

---

## Gold Assertions — Holding Municipal Montecristi Q1-2026

Fuente: **SIAP-ICPI_GOLD_MASTER_v5.5_TGI · H90_PRESUPUESTO_CONSOLIDADO**

| Entidad              | Ti Q1-2026 | TOP Q1-2026 | Categoría    |
|----------------------|-----------|-------------|--------------|
| GAD Municipal (G71-78) | 1.05%   | **8.1%**    | 🔴 ruptura   |
| Patronato Municipal  | 19.56%    | 150.5%      | 🟢 sobre ritmo |
| EP Aseo              | 18.17%    | 139.8%      | 🟢 sobre ritmo |
| Cuerpo de Bomberos   | 19.43%    | 149.5%      | 🟢 sobre ritmo |

**Hallazgo doctrinal central (Sprint B):**  
El ecosistema periférico está sobre ritmo. El GAD inversión está en ruptura. El problema es específico, localizado y accionable — no es una crisis generalizada.

---

## Narrativa Ejecutiva de Contraste

> "GAD inversión (G71-78) mantiene ruptura crítica de trayectoria: TOP 8.1% en Q1-2026.
> El ecosistema institucional — Patronato, EP Aseo, Bomberos — opera sobre ritmo esperado.
> El problema es específico: flujo de inversión GAD requiere intervención urgente antes del cierre Q2."

Esta narrativa tiene **autoridad algorítmica** — no es opinión, es el resultado del motor predictivo con datos reales del Gold Master.

---

## Contrato de Autoridad (QUIRA_DOCTRINE_v1.3 · Sección 1.6)

Cuando el alcalde presenta TOP en Concejo:

1. **Cita el TOP**: "La trayectoria de inversión GAD es 8.1% sobre ritmo histórico Q1"
2. **Muestra el contraste**: "El ecosistema periférico está sobre ritmo"
3. **Indica la acción**: "El flujo BDE debe desbloquearse antes del 15 de junio"

Ningún concejal puede refutar el TOP sin refutar el sistema eSIGEF Ecuador — que es el origen de los W_Q. La autoridad no es del alcalde: es del motor.

---

## Implementación técnica

**Módulo:** `utils/top.py` — `quira-os`

```python
from utils.top import top_entidad, narrativa_ia

# Pipeline completo
r = top_entidad(ti_pct=1.05, corte="Q1-2026", nombre="GAD Municipal")
# r["top"]       == 8.1
# r["categoria"] == "ruptura"
# r["sobre_ritmo"] == False
# r["top_display"] == "8.1%"

texto = narrativa_ia(r)
# → brief ejecutivo institucional, sin chatbot
```

**Tests:** `tests/test_top.py` — 56 gold assertions verificadas  
**Doctrina:** `docs/QUIRA_DOCTRINE_v1.md` Sección 1.6  
**Nomenclatura:** `docs/NOMENCLATURA_CANONICA.md` Sección 7.2

---

## Evolución futura

| Sprint | Extensión TOP |
|--------|---------------|
| Sprint C | TOP para velocidad SAT (respuesta institucional) |
| Sprint D | TOP para velocidad IFE (requiere datos CNE) |
| Año 2   | Recalibración W_Q con datos históricos Montecristi reales |
| MultiGAD | W_Q diferenciados por región (costa vs sierra vs amazonia) |

---

## Relaciones

- [[01_TGI_FRAMEWORK]] — TOP es el tercer pilar del TGI
- [[08_MMP_MENSUAL]] — MMP usa TOP para proyecciones mensuales
- [[ALERTA-D3_Ejecucion_Critica]] — La alerta de ejecución GAD que TOP formaliza
- [[ALERTA-Holding_Ti_Critico_2026]] — Contexto del ecosistema Q1-2026
- [[D3_EJECUCION]] — Fuente canónica de Ti para el motor

---

*Última actualización: 2026-05-27*  
*Fuente de datos: SIAP-ICPI_GOLD_MASTER_v5.5_TGI*  
*Motor: utils/top.py · QUIRA Intelligence · Dylus Lab*
