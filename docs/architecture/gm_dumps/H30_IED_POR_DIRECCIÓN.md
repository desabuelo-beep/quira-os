# H30_IED_POR_DIRECCIÓN — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=35 · pobladas=30 · fórmulas=49
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO, H17_IED
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H17_IED!B6
C6	=H17_IED!B7
A10	=H17_IED!A11
B10	=H17_IED!B11
C10	=IF(H17_IED!B11>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B11>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B11>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B11>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D10	=IF(H17_IED!B11<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A11	=H17_IED!A12
B11	=H17_IED!B12
C11	=IF(H17_IED!B12>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B12>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B12>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B12>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D11	=IF(H17_IED!B12<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A12	=H17_IED!A13
B12	=H17_IED!B13
C12	=IF(H17_IED!B13>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B13>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B13>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B13>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D12	=IF(H17_IED!B13<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A13	=H17_IED!A14
B13	=H17_IED!B14
C13	=IF(H17_IED!B14>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B14>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B14>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B14>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D13	=IF(H17_IED!B14<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A14	=H17_IED!A15
B14	=H17_IED!B15
C14	=IF(H17_IED!B15>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B15>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B15>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B15>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D14	=IF(H17_IED!B15<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A15	=H17_IED!A16
B15	=H17_IED!B16
C15	=IF(H17_IED!B16>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B16>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B16>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B16>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D15	=IF(H17_IED!B16<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A16	=H17_IED!A17
B16	=H17_IED!B17
C16	=IF(H17_IED!B17>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B17>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B17>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B17>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D16	=IF(H17_IED!B17<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A17	=H17_IED!A18
B17	=H17_IED!B18
C17	=IF(H17_IED!B18>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B18>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B18>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B18>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D17	=IF(H17_IED!B18<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A18	=H17_IED!A19
B18	=H17_IED!B19
C18	=IF(H17_IED!B19>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B19>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B19>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B19>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D18	=IF(H17_IED!B19<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A19	=H17_IED!A20
B19	=H17_IED!B20
C19	=IF(H17_IED!B20>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B20>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B20>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B20>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D19	=IF(H17_IED!B20<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
A20	=H17_IED!A21
B20	=H17_IED!B21
C20	=IF(H17_IED!B21>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B21>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B21>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B21>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
D20	=IF(H17_IED!B21<0.7,"Fortalecer documentación de evidencia y regularizar registro en eSIGEF. Revisar avance de metas asignadas.","✅ IED en rango — mantener ritmo de gestión")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H30_IED_POR_DIRECCIÓN
A2	H30 — IED POR DIRECCIÓN — REPORTE OPERATIVO PARA DIRECTORES
A3	Vista detallada del IED para cada dirección. Para uso del Director y su equipo técnico.
A5	▌ IED GLOBAL
A6	IED_Global_2025:
A8	▌ IED POR DIRECCIÓN — DETALLE OPERATIVO
A9	Dirección
B9	IED_%
C9	Nivel_AVEP
D9	Plan de Acción
A23	▌ EVALUACIÓN DE EFICIENCIA POR SERVIDOR PÚBLICO — LOSEP Art.76-82
A24	Marco legal: LOSEP Art.76-82 · Objetivo: evaluación objetiva sin subjetivismo · Fuente: eSIGEF + SERCOP + PDOT
A25	Nota: La evaluación individual se construye sumando el Cumplimiento POA de cada meta asignada al servidor, verificada en eSIGEF.
A26	ID_Servidor
B26	Nombre_Servidor
C26	Cargo / Puesto
D26	Dirección
E26	Metas_Asignadas
F26	Metas_Cumplidas
G26	IE_Individual_%
H26	Clasif_LOSEP
I26	Calificación_LOSEP
J26	Derechos_Protegidos
A27	→ Completar con datos de Talento Humano y eSIGEF 2026
B27	→ IE_Individual = Metas_Cumplidas / Metas_Asignadas (verificadas eSIGEF)
C27	→ Clasif.: ≥90%=Excelente · ≥70%=Satisfactorio · ≥50%=En proceso · <50%=Insatisfactorio
A29	▌ METODOLOGÍA LOSEP — PRINCIPIOS DE EVALUACIÓN ALGORÍTMICA
A30	P-1: La evaluación mide exclusivamente el cumplimiento de metas PDOT registradas en eSIGEF (evidencia objetiva)
A31	P-2: El servidor conoce sus metas al inicio del período (Art.76 LOSEP). No hay retroactividad.
A32	P-3: El resultado es impugnable ante el mismo sistema — toda brecha entre POA y eSIGEF es auditable
A33	P-4: La evaluación NO es un mecanismo de sanción automática — activa planes de mejora (Art.77 LOSEP)
A34	P-5: Los derechos del servidor (estabilidad, dignidad, no discriminación) son inviolables — LOSEP Art.22-26
A35	Fuente legal: LOSEP Art.76-82 · Reglamento LOSEP Art.216-234 · Constitución Art.326 (trabajo como derecho)
```