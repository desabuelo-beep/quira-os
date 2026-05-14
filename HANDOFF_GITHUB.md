# HANDOFF — QUIRA OS v0.1 → GitHub + Streamlit Cloud
## Para Claude Code o cualquier asistente con acceso a terminal

---

## CONTEXTO

El proyecto QUIRA OS v0.1 está completamente construido y listo para subir a GitHub.
Es una app Streamlit de gobernanza municipal (GAD Montecristi, Ecuador).
El objetivo es dejarlo desplegado en Streamlit Community Cloud para acceso público.

**Ruta local del proyecto:**
```
C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os\
```

**Archivos clave ya listos:**
- `app.py` — entry point principal
- `requirements.txt` — dependencias incluyendo anthropic
- `.gitignore` — excluye Excel, secrets, __pycache__
- `.streamlit/config.toml` — tema dark configurado
- `.streamlit/secrets.toml.template` — plantilla de secrets (NO subir secrets.toml real)

---

## LO QUE DEBE HACER EL AGENTE

### PASO 1 — Inicializar git local

```bash
cd "C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os"
git init
git add .
git status
```

Verificar que `.gitignore` está funcionando:
- NO deben aparecer archivos `.xlsx`
- NO debe aparecer `.streamlit/secrets.toml` (si existe)
- SÍ deben aparecer todos los `.py`, `requirements.txt`, `.streamlit/config.toml`

### PASO 2 — Primer commit

```bash
git commit -m "feat: QUIRA OS v0.1 — PMV Sistema de Gobernanza Municipal

Dashboard ejecutivo ICGI-T, Holding Municipal, Congruencias,
GeoTwin territorial, Operación HITL y Sentinel IA.
GAD Municipal de Montecristi · Dylus Lab © 2026"
```

### PASO 3 — Crear repo en GitHub

El usuario debe crear el repo en https://github.com/new con:
- Nombre sugerido: `quira-os` (o `quira-gov-pmv`)
- Visibilidad: **Public** (requerido para Streamlit Community Cloud gratis)
- Sin README inicial (ya tenemos archivos)

Luego conectar y hacer push:
```bash
git remote add origin https://github.com/USUARIO/quira-os.git
git branch -M main
git push -u origin main
```

### PASO 4 — Desplegar en Streamlit Community Cloud

1. Ir a: https://share.streamlit.io/
2. Sign in con la misma cuenta GitHub
3. Click "New app"
4. Repository: `USUARIO/quira-os`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Advanced settings" → Secrets → pegar:

```toml
ANTHROPIC_API_KEY = "sk-ant-TU-KEY-REAL-AQUI"
```

8. Click "Deploy"

La app estará disponible en:
`https://USUARIO-quira-os.streamlit.app`
(o similar — Streamlit asigna la URL)

---

## IMPORTANTE — QUÉ NO SUBIR

El `.gitignore` ya lo controla, pero verificar que NUNCA vayan al repo:
- `*.xlsx` — contienen datos reales del GAD
- `.streamlit/secrets.toml` — contiene la API key
- `__pycache__/` — archivos compilados Python

---

## COMPORTAMIENTO EN CLOUD (sin Excel local)

La app detecta automáticamente que está en la nube (`config.py → IS_CLOUD`).
En ese modo:
- Todos los datos vienen de `data/demo_data.py` (valores sellados Q1-2026)
- Sentinel funciona con el system prompt basado en demo_data (sin PDOT_KB)
- El header del dashboard muestra "⚠ Usando datos demo" — eso es correcto
- Todas las 6 páginas funcionan completamente

---

## CREDENCIALES DE LA APP (para compartir con demos)

| Usuario   | Password  | Rol       |
|-----------|-----------|-----------|
| alcalde   | quira2026 | Alcalde   |
| concejal  | quira2026 | Concejal  |
| tecnico   | quira2026 | Técnico   |

---

## VERIFICACIÓN FINAL

Después del deploy, abrir la URL y verificar:
- [ ] Login funciona con los 3 roles
- [ ] P-01 Tablero carga el gauge ICGI-T = 53.56
- [ ] P-04 GeoTwin muestra las 7 parroquias
- [ ] P-06 Sentinel acepta la API key y responde
- [ ] Modo Técnico muestra tech-labels y debug Sentinel
