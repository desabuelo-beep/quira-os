# GM-Ω · ICPI — MATRIZ DE PROCEDENCIA  `004/005`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/matriz_procedencia_icpi.py` leyendo el Gold Master vigente. Escribirlo a mano lo dejaría atrás el día que el Excel cambie, que es el patrón que esta auditoría persigue.

`150` celdas · 25 metas × 6 variables · baseline congelado **27,4582 %** (regla GM-Ω-ICPI-000)

## Estado de trazabilidad por variable

| Var | Constructo (tesis) | Estado provisional | Por qué |
|---|---|---|---|
| `P_i` | Coeficiente de Peso Presupuestario | **PARCIALMENTE_VERIFICADO** | referencia directa a H14!G; falta la cédula presupuestaria por meta |
| `R_i` | Coeficiente de Relevancia Normativa | **VERIFICADO** | fórmula + artículo del COOTAD citado meta a meta |
| `V_i` | Inmutabilidad Documental | **TEMPORAL_SEMANTIC_GAP** | la columna leída se llama `Vi_2025` |
| `E_i` | Coeficiente de Fricción de Autonomía | **REGLA_VERIFICADA · aplicación pendiente** | «Autonomía Orgánica» definida en Metodologia_SIAP_ICPI (abril) y citada en H12!A4; el CONTROL DEL DIRECTOR por meta no consta |
| `T_i` | Materialización Temporal | **VERIFICADO · sensibilidad pendiente** | ratio por ENTIDAD ejecutora; el tope MIN(1,…) se juzga en 007 |
| `C_i` | Trazabilidad Orgánica | **PARCIALMENTE_VERIFICADO** | VLOOKUP a TBL_CALIBRACION_Ci; falta la regla que calibra la tabla |

⚠️ Estos NO son veredictos: son estados de la auditoría mientras `GM-Ω-ICPI-011` no dictamine.

## Las 150 celdas

### `AH-AP-04`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B29` | 0.014583 | `=H14_PONDERADORES!G30` | — |
| `R_i` | `H12!C29` | 0.869565 | `=H14_PONDERADORES!F30` | — |
| `V_i` | `H12!D29` | 0 | `=IFERROR(VLOOKUP(A29,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E29` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F29` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I29` | 1 | `=IFERROR(VLOOKUP(A29,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `AH-C-X-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B15` | 0.010238 | `=H14_PONDERADORES!G16` | — |
| `R_i` | `H12!C15` | 0.333333 | `=H14_PONDERADORES!F16` | — |
| `V_i` | `H12!D15` | 1 | `=IFERROR(VLOOKUP(A15,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E15` | 1 | `LITERAL (sin origen declarado)` | ENTE-02 Patronato ↔ lo ejecuta ENTE-02 Patronato (adscrita) y la regla de la tesis pide 0.75 — divergencia entre definiciones A y B, no defecto |
| `T_i` | `H12!F15` | 0.656014 | `=H07b_Ti_INVERSIÓN_eSIGEF!C20` | ENTE-02 Patronato |
| `C_i` | `H12!I15` | 0.900000 | `=IFERROR(VLOOKUP(A15,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `AH-C-X-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B16` | 0.010614 | `=H14_PONDERADORES!G17` | — |
| `R_i` | `H12!C16` | 0.579710 | `=H14_PONDERADORES!F17` | — |
| `V_i` | `H12!D16` | 1 | `=IFERROR(VLOOKUP(A16,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E16` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F16` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I16` | 0.900000 | `=IFERROR(VLOOKUP(A16,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `AH-I-N-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B11` | 0.033545 | `=H14_PONDERADORES!G12` | — |
| `R_i` | `H12!C11` | 1.000000 | `=H14_PONDERADORES!F12` | — |
| `V_i` | `H12!D11` | 0.500000 | `=IFERROR(VLOOKUP(A11,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E11` | 0.750000 | `LITERAL (sin origen declarado)` | ENTE-04 EP Aseo |
| `T_i` | `H12!F11` | 1 | `=H07b_Ti_INVERSIÓN_eSIGEF!E20` | ENTE-04 EP Aseo |
| `C_i` | `H12!I11` | 0.750000 | `=IFERROR(VLOOKUP(A11,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `AH-I-X-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B8` | 0.117863 | `=H14_PONDERADORES!G9` | — |
| `R_i` | `H12!C8` | 0.579710 | `=H14_PONDERADORES!F9` | — |
| `V_i` | `H12!D8` | 1 | `=IFERROR(VLOOKUP(A8,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRADO` | — |
| `E_i` | `H12!E8` | 0.900000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F8` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I8` | 0.900000 | `=IFERROR(VLOOKUP(A8,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO"` | — |

### `AH-I-X-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B9` | 0.063685 | `=H14_PONDERADORES!G10` | — |
| `R_i` | `H12!C9` | 0.869565 | `=H14_PONDERADORES!F10` | — |
| `V_i` | `H12!D9` | 0 | `=IFERROR(VLOOKUP(A9,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRADO` | — |
| `E_i` | `H12!E9` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F9` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I9` | 1 | `=IFERROR(VLOOKUP(A9,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO"` | — |

### `AH-I-X-03`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B10` | 0.034314 | `=H14_PONDERADORES!G11` | — |
| `R_i` | `H12!C10` | 0.289855 | `=H14_PONDERADORES!F11` | — |
| `V_i` | `H12!D10` | 1 | `=IFERROR(VLOOKUP(A10,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E10` | 0.900000 | `LITERAL (sin origen declarado)` | ENTE-02 Patronato ↔ lo ejecuta ENTE-02 Patronato (adscrita) y la regla de la tesis pide 0.75 — divergencia entre definiciones A y B, no defecto |
| `T_i` | `H12!F10` | 0.656014 | `=H07b_Ti_INVERSIÓN_eSIGEF!C20` | ENTE-02 Patronato |
| `C_i` | `H12!I10` | 1 | `=IFERROR(VLOOKUP(A10,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `AH-I-X-04`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B13` | 0.021962 | `=H14_PONDERADORES!G14` | — |
| `R_i` | `H12!C13` | 0.579710 | `=H14_PONDERADORES!F14` | — |
| `V_i` | `H12!D13` | 1 | `=IFERROR(VLOOKUP(A13,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E13` | 0.750000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F13` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I13` | 0.750000 | `=IFERROR(VLOOKUP(A13,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `EP-L-N-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B24` | 0.001890 | `=H14_PONDERADORES!G25` | — |
| `R_i` | `H12!C24` | 0.579710 | `=H14_PONDERADORES!F25` | — |
| `V_i` | `H12!D24` | 1 | `=IFERROR(VLOOKUP(A24,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E24` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F24` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I24` | 0.900000 | `=IFERROR(VLOOKUP(A24,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `EP-L-X-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B25` | 0.001344 | `=H14_PONDERADORES!G26` | — |
| `R_i` | `H12!C25` | 0.289855 | `=H14_PONDERADORES!F26` | — |
| `V_i` | `H12!D25` | 1 | `=IFERROR(VLOOKUP(A25,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E25` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F25` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I25` | 0.900000 | `=IFERROR(VLOOKUP(A25,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-C-X-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B19` | 0.004142 | `=H14_PONDERADORES!G20` | — |
| `R_i` | `H12!C19` | 0.666667 | `=H14_PONDERADORES!F20` | — |
| `V_i` | `H12!D19` | 1 | `=IFERROR(VLOOKUP(A19,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E19` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F19` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I19` | 0.750000 | `=IFERROR(VLOOKUP(A19,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-CC-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B28` | 0.004667 | `=H14_PONDERADORES!G29` | — |
| `R_i` | `H12!C28` | 0.666667 | `=H14_PONDERADORES!F29` | — |
| `V_i` | `H12!D28` | 0 | `=IFERROR(VLOOKUP(A28,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E28` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F28` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I28` | 1 | `=IFERROR(VLOOKUP(A28,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-DIS-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B30` | 0.008750 | `=H14_PONDERADORES!G31` | — |
| `R_i` | `H12!C30` | 1.000000 | `=H14_PONDERADORES!F31` | — |
| `V_i` | `H12!D30` | 0 | `=IFERROR(VLOOKUP(A30,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E30` | 1 | `LITERAL (sin origen declarado)` | ENTE-04 EP Aseo ↔ lo ejecuta ENTE-04 EP Aseo (adscrita) y la regla de la tesis pide 0.75 — divergencia entre definiciones A y B, no defecto |
| `T_i` | `H12!F30` | 1 | `=H07b_Ti_INVERSIÓN_eSIGEF!E20` | ENTE-04 EP Aseo |
| `C_i` | `H12!I30` | 0.750000 | `=IFERROR(VLOOKUP(A30,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-I-X-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B18` | 0.005542 | `=H14_PONDERADORES!G19` | — |
| `R_i` | `H12!C18` | 0.666667 | `=H14_PONDERADORES!F19` | — |
| `V_i` | `H12!D18` | 1 | `=IFERROR(VLOOKUP(A18,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E18` | 1 | `LITERAL (sin origen declarado)` | ENTE-03 Bomberos ↔ lo ejecuta ENTE-03 Bomberos (adscrita) y la regla de la tesis pide 0.75 — divergencia entre definiciones A y B, no defecto |
| `T_i` | `H12!F18` | 0.916509 | `=H07b_Ti_INVERSIÓN_eSIGEF!D20` | ENTE-03 Bomberos |
| `C_i` | `H12!I18` | 1 | `=IFERROR(VLOOKUP(A18,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-I-X-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B20` | 0.029177 | `=H14_PONDERADORES!G21` | — |
| `R_i` | `H12!C20` | 0.579710 | `=H14_PONDERADORES!F21` | — |
| `V_i` | `H12!D20` | 1 | `=IFERROR(VLOOKUP(A20,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E20` | 0.900000 | `LITERAL (sin origen declarado)` | ENTE-04 EP Aseo ↔ lo ejecuta ENTE-04 EP Aseo (adscrita) y la regla de la tesis pide 0.75 — divergencia entre definiciones A y B, no defecto |
| `T_i` | `H12!F20` | 1 | `=H07b_Ti_INVERSIÓN_eSIGEF!E20` | ENTE-04 EP Aseo |
| `C_i` | `H12!I20` | 0.900000 | `=IFERROR(VLOOKUP(A20,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `FA-L-N-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B21` | 0.002908 | `=H14_PONDERADORES!G22` | — |
| `R_i` | `H12!C21` | 0.579710 | `=H14_PONDERADORES!F22` | — |
| `V_i` | `H12!D21` | 1 | `=IFERROR(VLOOKUP(A21,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E21` | 0.900000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F21` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I21` | 1 | `=IFERROR(VLOOKUP(A21,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `PI-I-G-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B14` | 0.015099 | `=H14_PONDERADORES!G15` | — |
| `R_i` | `H12!C14` | 0.579710 | `=H14_PONDERADORES!F15` | — |
| `V_i` | `H12!D14` | 1 | `=IFERROR(VLOOKUP(A14,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E14` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F14` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I14` | 1 | `=IFERROR(VLOOKUP(A14,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `PI-I-G-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B22` | 0.002759 | `=H14_PONDERADORES!G23` | — |
| `R_i` | `H12!C22` | 0.579710 | `=H14_PONDERADORES!F23` | — |
| `V_i` | `H12!D22` | 1 | `=IFERROR(VLOOKUP(A22,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E22` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F22` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I22` | 0.900000 | `=IFERROR(VLOOKUP(A22,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `PI-L-G-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B23` | 0.001580 | `=H14_PONDERADORES!G24` | — |
| `R_i` | `H12!C23` | 0.579710 | `=H14_PONDERADORES!F24` | — |
| `V_i` | `H12!D23` | 1 | `=IFERROR(VLOOKUP(A23,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E23` | 0.750000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F23` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I23` | 1 | `=IFERROR(VLOOKUP(A23,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `PI-TUR-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B26` | 0.018666 | `=H14_PONDERADORES!G27` | — |
| `R_i` | `H12!C26` | 0.289855 | `=H14_PONDERADORES!F27` | — |
| `V_i` | `H12!D26` | 0 | `=IFERROR(VLOOKUP(A26,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E26` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F26` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I26` | 0.900000 | `=IFERROR(VLOOKUP(A26,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `PI-TUR-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B27` | 0.007000 | `=H14_PONDERADORES!G28` | — |
| `R_i` | `H12!C27` | 0.289855 | `=H14_PONDERADORES!F28` | — |
| `V_i` | `H12!D27` | 0 | `=IFERROR(VLOOKUP(A27,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E27` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F27` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I27` | 1 | `=IFERROR(VLOOKUP(A27,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `SC-I-N-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B6` | 0.273604 | `=H14_PONDERADORES!G7` | — |
| `R_i` | `H12!C6` | 0.869565 | `=H14_PONDERADORES!F7` | — |
| `V_i` | `H12!D6` | 1 | `=IFERROR(VLOOKUP(A6,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRADO` | — |
| `E_i` | `H12!E6` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F6` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I6` | 1 | `=IFERROR(VLOOKUP(A6,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO"` | — |

### `SC-I-N-03`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B17` | 0.000804 | `=H14_PONDERADORES!G18` | — |
| `R_i` | `H12!C17` | 0.579710 | `=H14_PONDERADORES!F18` | — |
| `V_i` | `H12!D17` | 1 | `=IFERROR(VLOOKUP(A17,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E17` | 0.750000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F17` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I17` | 0.900000 | `=IFERROR(VLOOKUP(A17,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `SC-L-G-01`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B12` | 0.007407 | `=H14_PONDERADORES!G13` | — |
| `R_i` | `H12!C12` | 0.869565 | `=H14_PONDERADORES!F13` | — |
| `V_i` | `H12!D12` | 1 | `=IFERROR(VLOOKUP(A12,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRAD` | — |
| `E_i` | `H12!E12` | 0.750000 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F12` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I12` | 0.750000 | `=IFERROR(VLOOKUP(A12,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO` | — |

### `SC-L-N-02`

| Var | Celda | Valor | Origen | Entidad |
|---|---|---|---|---|
| `P_i` | `H12!B7` | 0.307857 | `=H14_PONDERADORES!G8` | — |
| `R_i` | `H12!C7` | 0.579710 | `=H14_PONDERADORES!F8` | — |
| `V_i` | `H12!D7` | 1 | `=IFERROR(VLOOKUP(A7,H13_VARIABLES_Vi!$A:$F,6,FALSE),"⚠️ Vi NO ENCONTRADO` | — |
| `E_i` | `H12!E7` | 1 | `LITERAL (sin origen declarado)` | ENTE-01 GAD central |
| `T_i` | `H12!F7` | 0.303498 | `=H07b_Ti_INVERSIÓN_eSIGEF!B20` | ENTE-01 GAD central |
| `C_i` | `H12!I7` | 1 | `=IFERROR(VLOOKUP(A7,H01_PARÁMETROS!$A$189:$G$213,6,FALSE),"⚠️ HILO ROTO"` | — |

