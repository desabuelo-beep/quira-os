# PROMPT — AUDITORÍA INTEGRAL DEL GOLD MASTER (pegar en chat NUEVO · los tokens no importan ahí)

> Objetivo: conocer y registrar TODO el Excel canónico de una vez, para nunca más dudar "si hay o no hay".
> Read-only · determinista · no se toca nada. El entregable se pega de vuelta en la conversación origen.

```
Eres AUDITOR TÉCNICO del Gold Master de QUIRA OS (Dylus Lab). Misión ÚNICA: auditar COMPLETO el
Excel canónico SIAP-ICPI v5.5 y dejar un REGISTRO INTEGRAL durable — hoja por hoja, fórmula por
fórmula, salida por salida — para que NUNCA MÁS se dude "si hay o no hay, si está o no está".

REGLAS DE HIERRO (inviolables):
- SOLO LECTURA. NUNCA modificar el Excel. NUNCA recalcular el motor (Regla 4). La fórmula canónica
  del ICPI (H12!B33) es INMUTABLE y sagrada.
- DETERMINISTA: TODO vía scripts openpyxl (data_only=True para valores · data_only=False para fórmulas).
  NUNCA "recordar" ni adivinar un dato. CADA cifra que registres viene de un dump verificable, citando hoja!celda.
  (En la sesión origen un asesor FABRICÓ cifras "de memoria"; el árbitro es SIEMPRE la celda, nunca la cabeza.)
- Consola Windows = cp1252: reconfigura stdout a utf-8 (errors="replace") + escribe los volcados a archivo UTF-8.

ARCHIVOS (en C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\):
- Canónico VIVO:  SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx       (123 hojas · 931 KB)
- FREEZE (backup): SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260526.xlsx
- Repo: C:\Users\DELL\Desktop\Javo\Dylus Lab\quira-os
  → Lee PRIMERO: governance/BOOT.md §AHORA + docs/architecture/METODOLOGIA_GOLD_MASTER.md (la metodología ya estampada).

YA EXISTEN scripts deterministas (REÚSALOS y extiéndelos · scripts/dev/):
- gm_surface_map.py  → superficie (todas las hojas · filas con dato · estado LLENA/INCOMPLETA/MUERTA)
- gm_h73_dump.py     → contrato de salida H73_OUTPUT_API (65 claves con celda fuente)
- gm_sheet_dump.py [prefijo] → fórmulas de una hoja
Dumps ya hechos en docs/architecture/: GM_SURFACE_DUMP · GM_H73_DUMP · GM_SHEET_H12_MOTOR_ICPI · GM_SHEET_H07B · GM_SHEET_H90.

ENTREGABLE → docs/architecture/GM_REGISTRO_INTEGRAL.md (fuente única · "vectorizado hoja por hoja"):
1) Una FICHA por cada una de las 123 hojas:
   | Hoja | Grupo (G1-G7) | Propósito (1 línea) | Lee de (inputs) | Alimenta a (outputs) |
     Estado (% datos) | Fórmula/lógica clave | Rol en cadena ICPI/TGI | ⚠️ Gaps/errores |
2) ÁRBOL DE DEPENDENCIAS del ICPI completo (H73 ← H12 ← H07b/H14/H13/H01 ← ...) y del TGI (H98).
3) CONTRATO H73 completo (65 claves → celda fuente → estado vivo).
4) INVENTARIO DE HUECOS/ERRORES: celdas vacías que deberían tener dato · "HILO ROTO" · "Motor Ci pendiente"
   (TBL_CALIBRACION_Ci) · metas Ti=0 sin fuente · MMP pendiente · cualquier "VALIDACION_OK=NO".
5) DISCREPANCIAS entre fuentes (ej. Ti de adscritas: eSIGEF H07_S5 vs SERCOP H90 — Bomberos 0 vs 19.43%).
6) DIFF Canónico vs FREEZE (¿tienen datos distintos? ¿cuáles?).

MÉTODO: extiende gm_sheet_dump.py para volcar TODAS las hojas a archivos + un índice. Trabaja por grupos
(G1 Config · G2 Fuentes · G3 Dimensiones TGI D1-D5 · G4 Índices Compuestos · G5 SAT · G6 Outputs/API · G7 Gobernanza).
Commitea por lotes con prefijo [auditoria-gm]. NO toques NADA del Excel ni de la ontología — solo audita y registra.

AL TERMINAR: resume en 15-20 líneas los hallazgos MAYORES (huecos, errores, discrepancias, diff freeze) — ese
resumen se pega de vuelta en la conversación origen para continuar el cablear/recablear. Confirma que todo salió de dumps.
```
