# H86b_ALGORITHMIC_GOVERNANCE_PRO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=50 · pobladas=41 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	QUIRA by Dylus Lab (ICGI-T externo · ICPI motor) v1.0 | QUIRA by Dylus Lab (ICGI-T externo · ICPI motor) QUIRA by Dylus Lab
A2	QUIRA_GOVERNANCE_PROTOCOL — QUIRA by Dylus Lab
B2	Emitido: 2026-05-11 | RUN_ID: QUIRA-GOV-V2.0 | ICGI-T (externo) / ICPI (interno) | Montecristi Ecuador
A4	⚖️ LOS 5 PRINCIPIOS DE GOBERNANZA ALGORÍTMICA QUIRA
A5	N°
B5	PRINCIPIO
C5	DESCRIPCIÓN OPERATIVA
A6	P-01
B6	Delimitación Funcional
C6	SIAP-ICPI mide el grado de cumplimiento de compromisos institucionales registrados en instrumentos de planificación oficiales (PDOT, POA, PAC, LOTAIP). El sistema NO evalúa capacidad política, liderazgo personal ni decisiones estratégicas del gobierno local. El ICPI es un espejo algorítmico del desempeño normativo observable, no un juicio de valor político. Cualquier interpretación fuera de este alcance constituye un uso indebido del sistema.
A7	P-02
B7	Fuente Oficial de Datos
C7	Todos los datos que alimentan el motor SIAP-ICPI provienen exclusivamente de fuentes institucionales verificadas: eSIGEF (Ministerio de Finanzas), SERCOP (portal de contratación pública), SIGAD (SNP), LOTAIP, CPCCS y CNE. El sistema es un espejo de los datos institucionales oficiales — no genera datos propios ni realiza inferencias fuera del registro administrativo verificable. La trazabilidad de cada dato está garantizada mediante HASH_MODELO y H76_AUDIT_TRAIL.
A8	P-03
B8	No Sanción Automatizada
C8	SIAP-ICPI es un sistema de ALERTA TEMPRANA y CERTIFICACIÓN, no de sanción administrativa. El sistema detecta brechas, activa alertas SAT y genera reportes de integridad, pero en ningún caso reemplaza la decisión humana. Toda acción derivada de un resultado SIAP-ICPI — correcciones presupuestarias, auditorías, intervenciones — debe ser autorizada y ejecutada por autoridad competente. El humano decide; SIAP-ICPI informa. Este principio es inviolable bajo SIAP-ICPI.
A9	P-04
B9	Derecho de Réplica y Auditoría
C9	Todo score ICPI y todo resultado de subsistema (IED, IGP, IET, SAT) es completamente auditable y reproducible. Cualquier entidad, ciudadano o auditor externo puede reproducir el cálculo siguiendo el protocolo H40_PROTOCOLO_INGESTA y verificando H12!B33 = B31/B32*100 (Axioma de Invarianza Computacional). El RUN_ID y la cadena de hash H81_HASH_CHAIN garantizan que los resultados corresponden exactamente al estado del sistema en el momento de emisión. El Derecho de Réplica es un derecho institucional y ciudadano garantizado por este protocolo.
A10	P-05
B10	Versionado Obligatorio y Trazabilidad
C10	Cada reporte emitido bajo QUIRA by Dylus Lab (ICGI-T externo · ICPI motor) queda irrevocablemente atado a un RUN_ID único (SHA256 de Fecha_Corte + Hash_Modelo + Checksum_Pre) y a una MODEL_VERSION. Ningún resultado puede ser presentado sin identificación de versión. La actualización de parámetros, umbrales o modelos debe registrarse en H81_HASH_CHAIN como nuevo evento encadenado. El RUN_ID actual: 9F522CE87713EC0D22FF5BF6AADF16C7 | MODEL_VERSION: v2.1 Gold Master → QUIRA by Dylus Lab (ICGI-T externo · ICPI motor) QUIRA by Dylus Lab.
A12	🔐 FIRMA DIGITAL DEL PROTOCOLO
A13	HASH_PROTOCOLO
B13	114DC7A4BD0966B29FC7813791F43D56E541DD49D6AA6A14EAEF86A8035B25F7
C13	SHA256(5_principios + 2026-05-01 22:28:37 UTC)
A14	EMITIDO_POR
B14	DYLUS_LAB_CERTIFIER — QUIRA by Dylus Lab (ICGI-T externo · ICPI motor) QUIRA by Dylus Lab
C14	2026-05-01 22:28:37 UTC
A16	▌ NOTA CONCEPTUAL — NOMENCLATURA DUAL QUIRA
A17	Interno (motor): ICPI = Índice de Congruencia de Política Institucional
A18	Externo (ciudadano / PMV / organismos): ICGI-T = Índice de Congruencia de Gobernanza Intersistémica Territorial — QUIRA by Dylus Lab
A19	Principio: el motor es inmutable (ICPI). La capa de vista y comunicación usa ICGI-T.
A21	══════════════════════════════════════════════════════════════════
A22	▌ DOCTRINA QUIRA — FREEZE v1.0 · 2026-05-11
A23	══════════════════════════════════════════════════════════════════
A24	NOMENCLATURA DUAL (INMUTABLE DESDE v1.0)
A25	ICGI-T
B25	Producto / UI
C25	Índice de Congruencia de Gobernanza Intersistémica Territorial
A26	ICPI
B26	Motor canónico
C26	Índice de Congruencia Programática e Intersistémica · H12 INMUTABLE
A27	HPT-M
B27	Unidad de análisis
C27	Holding Público Territorial de Montecristi
A29	ARQUITECTURA DE NODOS HPT-M
A30	Nodo 01
B30	Núcleo de Gobierno
C30	Alcaldía · Direcciones · POA · PAC · eSIGEF · PDOT
A31	Nodo 02
B31	Operadores Públicos
C31	EP Aseo Integral · Patronato Municipal · BCBM Bomberos · EP Hábitat
A32	Nodo 03
B32	Territorio
C32	5 Parroquias · NBI · TPS · Georreferenciación · GeoTwin
A33	Nodo 04
B33	Ecosistema Externo
C33	CPCCS · Cooperación internacional · ODS · Participación ciudadana
A35	DOCTRINA ICGI-T — 4 CONGRUENCIAS (PUBLICABLE / PATENTABLE)
A36	1. Congruencia Política
B36	Promesa ↔ PDOT ↔ COOTAD ↔ Mandato
C36	¿El GAD gobierna con lo que prometió?
A37	2. Congruencia Operativa
B37	POA ↔ PAC ↔ eSIGEF ↔ Ejecución EP
C37	¿El holding entrega lo que planificó?
A38	3. Congruencia Territorial
B38	Inversión ↔ Brecha ↔ NBI ↔ Prioridad
C38	¿La inversión llega donde más se necesita?
A39	4. Congruencia Ecosistémica
B39	GAD ↔ EP ↔ Adscritas ↔ Ciudadanía
C39	¿El holding funciona como sistema, no como silos?
A41	REGLA METODOLÓGICA CLAVE (P-06 en adelante)
A42	Las EP y adscritas NO son fuentes de datos. Son NODOS INSTITUCIONALES INTEROPERABLES del HPT-M.
A43	Esto protege la defensa metodológica ante organismos de control, academia y cooperación internacional.
A45	POSICIONAMIENTO DE CATEGORÍA
A46	QUIRA Framework v1.0 — A Territorial Governance Intelligence Model for Municipal Holding Structures
A47	Mercado objetivo: Ecuador · Colombia · Perú · México · América Latina
A48	Diferenciador: el único sistema que mide el holding público territorial (no solo el GAD central)
A50	★ FREEZE v1.0 — Sellado por Dylus Lab · Javo Delgado Santana · 2026-05-11 · Montecristi Ecuador ★
```