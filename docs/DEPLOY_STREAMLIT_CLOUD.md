# QUIRA Intelligence — Guía de Despliegue Streamlit Cloud
**Guía operacional — Equipo Dylus Lab**
*Última actualización: 2026-05-26 · Sprint 3 Semana 4*

> Objetivo: conectar GitHub → Streamlit Cloud para que cada push a `main` desplegue automáticamente la aplicación QUIRA Intelligence.

---

## Arquitectura del Despliegue

```
Desarrollador local
       ↓  git push
GitHub (desabuelo-beep/quira-os)
       ↓  CI/CD automático
Streamlit Cloud
       ↓  lee
  gm_snapshot.json + Supabase
       ↓
  QUIRA Intelligence App (pública/privada)
```

**Por qué no el Excel directo:**
Streamlit Cloud no tiene acceso al sistema de archivos local. El Gold Master Excel vive en la máquina del equipo Dylus Lab. La app en Cloud lee `data/gm_snapshot.json` (que sí está en el repo) y Supabase para datos longitudinales.

---

## Paso 1 — Verificar repositorio

El repositorio `desabuelo-beep/quira-os` debe tener:

```
quira-os/
├── app.py                          ← entry point Streamlit ✅
├── requirements.txt                ← dependencias ✅
├── .streamlit/
│   ├── config.toml                 ← tema QUIRA ✅
│   └── secrets.toml.template       ← plantilla (no el real) ✅
├── data/
│   └── gm_snapshot.json            ← fallback Gold Master ✅
└── docs/                           ← documentación ✅
```

**Verificar que NO están en el repo:**
- `.streamlit/secrets.toml` (está en .gitignore ✅)
- `TGI_GOLD_MASTER*.xlsx` (está en .gitignore ✅)
- `sentinel/data/` (SQLite DB con datos reales — en .gitignore ✅)

---

## Paso 2 — Crear app en Streamlit Cloud

1. Ir a [share.streamlit.io](https://share.streamlit.io) e iniciar sesión con `desabuelo@gmail.com`
2. Clic en **"New app"**
3. Configurar:

| Campo | Valor |
|---|---|
| Repository | `desabuelo-beep/quira-os` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL (opcional) | `quira-intelligence` (o similar disponible) |

4. Clic en **"Deploy!"** — el primer deploy tardará 2-5 minutos.

---

## Paso 3 — Configurar Secrets

Una vez desplegada, ir a: **App → ⋮ (tres puntos) → Settings → Secrets**

Pegar el siguiente contenido (con valores reales):

```toml
# ── QUIRA Intelligence — Secrets de Producción ──
ANTHROPIC_API_KEY = "sk-ant-TU-KEY-REAL-AQUI"

[database]
mode = "supabase"
supabase_uri = "postgresql://postgres:TU-PASSWORD@db.TU-PROYECTO.supabase.co:5432/postgres"
```

**Guardar** y la app se reiniciará automáticamente.

---

## Paso 4 — Verificar dependencias

El `requirements.txt` cubre todas las dependencias de producción:

```
streamlit>=1.55.0
pandas>=2.0.0
plotly>=5.0.0
openpyxl>=3.1.0        ← lectura Gold Master en local
pillow>=10.0.0
requests>=2.28.0
pypdf>=3.0.0
streamlit-folium>=0.22.0
folium>=0.18.0
psycopg2-binary>=2.9.0  ← conexión PostgreSQL/Supabase
reportlab>=4.0.0
anthropic>=0.40.0       ← QUIRA IA (Fase 2+)
```

Si agregan nuevas dependencias al proyecto, **siempre actualizar `requirements.txt`**.

---

## Paso 5 — Flujo CI/CD automático

Una vez conectado, el flujo es completamente automático:

```bash
# Desarrollador hace cambios
git add .
git commit -m "feat: actualización mensual ciclo Mayo"
git push origin main

# → Streamlit Cloud detecta el push
# → Reinicia y despliega la nueva versión
# → La app está actualizada en ~2 minutos
```

El deploy aparece en la pestaña **"Manage app"** con logs en tiempo real.

---

## Paso 6 — Actualización mensual del Gold Master

Después de cada ciclo mensual, el flujo para actualizar los datos en Cloud es:

```bash
# 1. Actualizar el Gold Master localmente (Excel)
# 2. Ejecutar pipeline para sincronizar gm_snapshot.json
python scripts/ejecutar_ciclo_mensual.py --municipio 130801

# 3. Subir cambios al repo (gm_snapshot.json actualizado)
git add data/gm_snapshot.json
git commit -m "data: ciclo mensual Mayo 2026 — ICPI=66.85%"
git push origin main

# → Streamlit Cloud despliega automáticamente con nuevos datos
```

---

## Configuración de Supabase para Producción

Si el modo es `"supabase"` en secrets.toml:

1. Ir a [supabase.com](https://supabase.com) → proyecto QUIRA
2. Settings → Database → Connection string (URI)
3. Copiar la URI completa (incluye password)
4. Pegar en Streamlit Cloud Secrets bajo `[database] supabase_uri`

**Tablas requeridas en Supabase:**
```sql
-- Se crean automáticamente al arrancar la app (init_db())
municipality_snapshots   ← snapshots canónicos por municipio
document_uploads         ← documentos ingresados
monthly_kpis             ← KPIs calculados por período
alerts_history           ← historial SAT
scheduler_log            ← log del scheduler automático
```

---

## Troubleshooting

### "ModuleNotFoundError"
Agregar el módulo faltante a `requirements.txt` y hacer push.

### "FileNotFoundError: gm_snapshot.json"
El archivo `data/gm_snapshot.json` debe estar en el repo. Verificar que no esté en `.gitignore`.

### App muestra datos desactualizados
El `gm_snapshot.json` no se actualizó. Ejecutar el ciclo mensual localmente y hacer push.

### Secrets no disponibles
Verificar que estén configurados en: App → Settings → Secrets (no en el archivo local).

### Base de datos vacía en producción
En modo `"supabase"`, verificar que la URI sea correcta y que las tablas estén creadas (`init_db()` se ejecuta automáticamente al arrancar).

---

## Checklist de Deploy

```
[ ] Repositorio GitHub actualizado (git push main)
[ ] app.py es el entry point correcto
[ ] requirements.txt está completo y actualizado
[ ] .streamlit/config.toml está en el repo
[ ] .streamlit/secrets.toml NO está en el repo
[ ] data/gm_snapshot.json está en el repo y actualizado
[ ] Secrets configurados en Streamlit Cloud (ANTHROPIC_API_KEY, database)
[ ] App arranca sin errores (verificar logs en Manage app)
[ ] GOV tab carga con datos correctos (ICPI=66.85%)
[ ] Ops tab muestra Gold Master disponible
```

---

## Automatización — Windows Task Scheduler

Para ejecutar el ciclo mensual automáticamente el primer día de cada mes sin intervención manual, configurar una tarea en **Windows Task Scheduler**.

### Cómo abrir Task Scheduler

Presionar `Win + R`, escribir `taskschd.msc` y presionar **Enter**. Alternativamente, buscar **"Programador de tareas"** en el menú Inicio de Windows.

### Comando a configurar

```cmd
python "C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\scripts\ejecutar_ciclo_mensual.py" --municipio 130801
```

### Parámetros de la tarea

| Parámetro | Valor |
|---|---|
| **Nombre de la tarea** | `QUIRA - Ciclo Mensual Automático` |
| **Trigger** | Mensual — día 1 de cada mes, 09:00 hs |
| **Acción (programa/script)** | `python` |
| **Agregar argumentos** | `"C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\scripts\ejecutar_ciclo_mensual.py" --municipio 130801` |
| **Iniciar en (Start in)** | `C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os` |

### Pasos para crear la tarea

1. En Task Scheduler, clic en **"Crear tarea básica…"** (panel derecho).
2. Escribir nombre: `QUIRA - Ciclo Mensual Automático` → **Siguiente**.
3. Trigger: seleccionar **Mensual** → marcar todos los meses, día **1**, hora **09:00** → **Siguiente**.
4. Acción: seleccionar **Iniciar un programa** → **Siguiente**.
5. En **Programa/script** ingresar: `python`
6. En **Agregar argumentos** ingresar: `"C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\scripts\ejecutar_ciclo_mensual.py" --municipio 130801`
7. En **Iniciar en** ingresar: `C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os`
8. Clic en **Finalizar**.

> **Nota:** Asegurarse de que el entorno Python activo (virtualenv o conda) sea el correcto. Si se usa un entorno virtual, reemplazar `python` en el campo Programa/script por la ruta completa al ejecutable, por ejemplo: `C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\.venv\Scripts\python.exe`

---

*QUIRA Intelligence · Dylus Lab © 2026*
