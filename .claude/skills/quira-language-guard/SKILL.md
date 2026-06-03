# /quira-language-guard — Guardián de Frontera de Lenguaje QUIRA

Verifica que ningún término interno de QUIRA aparezca en código visible al usuario.
Aplica el Bloomberg Model: el mundo ve el espejo, la metodología es del laboratorio.

## Cuándo usar este skill

Antes de hacer commit de cualquier archivo que toque:
- Archivos `p_*.py`, `m1-m5*.py` — vistas de usuario
- Templates HTML en strings de Python
- Cualquier `st.markdown()`, `st.write()`, `st.html()`
- Respuestas de Sentinel al usuario

## Términos prohibidos en capa pública

### Archivos del sistema de cálculo
```
Gold Master
SIAP-ICPI
_TGI
v5.5
```

### Hojas del Excel interno
```
H01  H02  H03  H04  H05  H06  H07  H07b
H08  H09  H10  H11  H12  H41  H73  H74
H75  H85  H90  H91
```

### Índices y siglas metodológicas
```
ICPI   TGI    IFE    IED    ITAM   IGP
IPE    PSG    ISP    IOC    IET    IEFR
```

### Variables de fórmula (cuando son labels visibles)
```
Ti_   Vi_   Pi_   Ri_   Ei_
_Patronato_   _GAD_   _Bomberos_  (cuando van como ID de fórmula)
```

### IDs internos de QTMP / grafo
```
SP_G10P    RES_G10P   IND_G10P
QTMP_ECU   ACK_       QNKC
```

### Protocolos y nomenclatura interna
```
QTMP    ACK     QLEP    QNKC-002    QNKC
Gold_Master    gm_snapshot   (en texto visible al usuario)
```

## Proceso de verificación

### Paso 1: Identificar archivos a revisar
```bash
# Archivos modificados en el commit actual
git diff --name-only HEAD

# Buscar términos prohibidos
grep -rn "Gold Master\|_TGI\|ICPI\|TGI\|H07b\|H73\|QTMP\|QNKC\|ACK_\|Ti_" \
  quira_pages/ components/ sentinel/ \
  --include="*.py" | grep -v "# INTERNO\|# noqa"
```

### Paso 2: Para cada resultado encontrado

1. **¿Está en un string visible al usuario?** (dentro de `st.markdown`, `st.write`, HTML, f-string de UI)
   → **ELIMINAR o reemplazar con lenguaje de gobernanza**

2. **¿Está en un comentario de código interno?**
   → **PERMITIDO** — los comentarios son capa interna

3. **¿Está en una variable Python (no string)?**
   → **PERMITIDO** — nombres de variables son capa interna

4. **¿Está en un log o mensaje de error del sistema?**
   → **REVISAR** — si el error llega al usuario → reemplazar

### Paso 3: Tabla de sustituciones canónicas

| Término interno | Sustitución pública |
|---|---|
| `ICPI: 17.4%` | `Cumplimiento institucional: 17.4%` |
| `TGI: 66.8%` | `Índice de gobernanza territorial: 66.8%` |
| `Ti_Patronato = 50%` | `Ejecución presupuestaria Patronato: 50%` |
| `Gold Master v5.5_TGI` | `Dylus Lab © 2026 · QUIRA Intelligence v1.0` |
| `H07b_Ti_INVERSIÓN fila 18` | `Fuente: SIGEF · noviembre 2025` |
| `IOC` | `Índice de opacidad informativa` |
| `SAT-III activa` | `Alerta de reincidencia activa` |
| `D3 brecha` | `Brecha en ejecución institucional` |

### Paso 4: Reporte final

Emite tabla con:
| Archivo | Línea | Término encontrado | Acción requerida | Estado |
|---|---|---|---|---|

Si todo está limpio:
```
✓ FRONTERA DE LENGUAJE VERIFICADA
  0 términos internos en capa pública
  Listo para commit / demo
```

Si hay violaciones:
```
⚠ VIOLACIONES DE FRONTERA: N términos internos encontrados
  [lista de archivo:línea:término]
  NO hacer commit hasta resolver
```

## Principio rector

> El alcalde de Montecristi usa QUIRA para gobernar su cantón.
> No necesita saber qué hoja de Excel calculó el 50%.
> Solo necesita saber que el Patronato ejecutó el 50% y qué significa eso para sus ciudadanos.
