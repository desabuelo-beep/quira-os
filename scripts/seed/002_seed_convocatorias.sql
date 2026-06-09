-- ============================================================
-- Seed 002 — Convocatorias de prueba · Motor Elegibilidad D02
-- QUIRA Gov · Dylus Lab © 2026
-- Propósito: poblar fondos_convocatorias + fondos_conv_requisitos
--   para verificar el Matcher end-to-end antes del skill /fondos-radar.
-- Cubre los 4 posibles estados: elegible_hoy · elegible_con_brecha ·
--   no_elegible · pendiente_datos
-- Referencias: ADR-026 §D02 · fondos_matcher.py · 002_fondos_oportunidades.sql
-- ============================================================

-- ── CONVOCATORIAS (5 anclas de prueba) ───────────────────────────────────────

INSERT INTO fondos_convocatorias
    (codigo, emisor_id, nombre, estado, monto_min_usd, monto_max_usd, elegibles, temas,
     url, descripcion, snapshot_date, proxima_revision)
VALUES

-- 1. BDE Agua Potable — reembolsable · ISP gate crítico
-- Esperado: no_elegible (ISP 14.58% << 65% requerido)
(
  'BDE-AGUA-2026',
  (SELECT id FROM fondos_emisores WHERE codigo = 'BDE'),
  'BDE — Crédito Agua Potable y Saneamiento 2026',
  'abierta',
  200000, 5000000,
  ARRAY['GAD'],
  ARRAY['agua','saneamiento','infraestructura'],
  'https://bde.fin.ec/agua-saneamiento',
  'Crédito reembolsable para infraestructura de agua potable y alcantarillado. '
  'Requiere salud presupuestaria mínima para garantizar servicio de deuda.',
  CURRENT_DATE,
  CURRENT_DATE + 90
),

-- 2. ONU Mujeres — Fondo Mujeres Rurales · PSG gate crítico
-- Esperado: no_elegible (PSG 12.83% < 20% requerido)
(
  'ONUMUJERES-RURAL-2026',
  (SELECT id FROM fondos_emisores WHERE codigo = 'ONU_MUJERES'),
  'ONU Mujeres — Fondo Mujeres Rurales Ecuador 2026',
  'abierta',
  30000, 300000,
  ARRAY['GAD','ONG','OSC'],
  ARRAY['genero','agua','participacion'],
  'https://unwomen.org/fondos/mujeres-rurales',
  'Fondo no reembolsable para proyectos de acceso a agua potable '
  'con enfoque de género en zonas rurales. Requiere PSG mínimo demostrable.',
  CURRENT_DATE,
  CURRENT_DATE + 60
),

-- 3. PNUD — Gobernanza Local Democrática · IGP como gate no crítico
-- Esperado: elegible_hoy (POA=True, RDC=True, IGP=27.98 > 20 requerido)
(
  'PNUD-GOB-LOCAL-2026',
  (SELECT id FROM fondos_emisores WHERE codigo = 'PNUD'),
  'PNUD — Gobernanza Local Democrática Ecuador 2026',
  'abierta',
  80000, 500000,
  ARRAY['GAD','ONG','OSC'],
  ARRAY['gobernanza','democracia','participacion'],
  'https://undp.org/ecuador/gobernanza-local',
  'Fondo no reembolsable para fortalecimiento de mecanismos de participación '
  'ciudadana y rendición de cuentas en municipios.',
  CURRENT_DATE,
  CURRENT_DATE + 45
),

-- 4. AECID — Gobernanza Participativa · ITAM como gate no crítico
-- Esperado: elegible_con_brecha (POA=True, IGP>=25 OK, ITAM=56 < 65 → brecha -9pp)
(
  'AECID-GOBERNANZA-2026',
  (SELECT id FROM fondos_emisores WHERE codigo = 'AECID'),
  'AECID — Programa Gobernanza Participativa LAT 2026',
  'abierta',
  50000, 400000,
  ARRAY['GAD','ONG','academia'],
  ARRAY['gobernanza','transparencia','participacion'],
  'https://aecid.es/cooperacion/gobernanza-lat',
  'Fondo no reembolsable para proyectos de fortalecimiento institucional '
  'con énfasis en transparencia y participación ciudadana.',
  CURRENT_DATE,
  CURRENT_DATE + 75
),

-- 5. Ford Foundation — Democracia y Mandato · IFE_A gate — diferenciador QUIRA
-- Esperado: elegible_hoy (IFE_A=72.73 >= 60 requerido, ITAM=56 >= 50 OK)
(
  'FORD-DEMOCRACIA-2026',
  (SELECT id FROM fondos_emisores WHERE codigo = 'FORD'),
  'Ford Foundation — Democracia y Mandato Local 2026',
  'abierta',
  100000, 400000,
  ARRAY['ONG','OSC','academia'],
  ARRAY['democracia','derechos_humanos','gobernanza'],
  'https://fordfoundation.org/grants/democracia',
  'Fondo para proyectos que demuestren fidelidad al mandato electoral '
  'y fortalezcan la conexión entre promesas de campaña y ejecución pública.',
  CURRENT_DATE,
  CURRENT_DATE + 90
);


-- ── REQUISITOS POR CONVOCATORIA ───────────────────────────────────────────────

-- 1. BDE Agua: ISP >= 65% (crítico) + PAC publicado (crítico)
INSERT INTO fondos_conv_requisitos
    (convocatoria_id, requisito_id, operador, valor, es_critico, notas)
VALUES
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'BDE-AGUA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'ISP'),
  'gte', 65.0, true,
  'Salud presupuestaria mínima para garantizar servicio de deuda BDE'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'BDE-AGUA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'PAC_APROBADO'),
  'eq_true', NULL, true,
  'PAC publicado requerido para inicio de proceso de contratación'
);

-- 2. ONU Mujeres Rural: PSG >= 20% (crítico) + RDC presentada (crítico)
INSERT INTO fondos_conv_requisitos
    (convocatoria_id, requisito_id, operador, valor, es_critico, notas)
VALUES
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'ONUMUJERES-RURAL-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'PSG'),
  'gte', 20.0, true,
  'PSG mínimo 20% para demostrar enfoque institucional de género'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'ONUMUJERES-RURAL-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'RDC_PRESENTADA'),
  'eq_true', NULL, true,
  'RDC presentada requerida como evidencia de accountability'
);

-- 3. PNUD Gobernanza: POA aprobado (crítico) + RDC presentada (crítico) + IGP >= 20% (no crítico)
INSERT INTO fondos_conv_requisitos
    (convocatoria_id, requisito_id, operador, valor, es_critico, notas)
VALUES
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'PNUD-GOB-LOCAL-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'POA_APROBADO'),
  'eq_true', NULL, true,
  'POA aprobado: evidencia de planificación anual vigente'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'PNUD-GOB-LOCAL-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'RDC_PRESENTADA'),
  'eq_true', NULL, true,
  'RDC presentada: condición de elegibilidad PNUD Ecuador'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'PNUD-GOB-LOCAL-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'IGP'),
  'gte', 20.0, false,
  'IGP >= 20% recomendado — no es bloqueante pero mejora scoring'
);

-- 4. AECID Gobernanza: POA (crítico) + IGP >= 25% (crítico) + ITAM >= 65% (no crítico → brecha)
INSERT INTO fondos_conv_requisitos
    (convocatoria_id, requisito_id, operador, valor, es_critico, notas)
VALUES
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'AECID-GOBERNANZA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'POA_APROBADO'),
  'eq_true', NULL, true,
  'POA aprobado obligatorio'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'AECID-GOBERNANZA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'IGP'),
  'gte', 25.0, true,
  'IGP >= 25% — evidencia de participación ciudadana real'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'AECID-GOBERNANZA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'ITAM'),
  'gte', 65.0, false,
  'ITAM >= 65% recomendado — no bloqueante pero prioritario para selección'
);

-- 5. Ford Foundation Democracia: IFE_A >= 60% (crítico) + ITAM >= 50% (no crítico)
-- Este fondo prueba el DIFERENCIADOR QUIRA: IFE_A como gate de elegibilidad
INSERT INTO fondos_conv_requisitos
    (convocatoria_id, requisito_id, operador, valor, es_critico, notas)
VALUES
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'FORD-DEMOCRACIA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'IFE_A'),
  'gte', 60.0, true,
  'IFE-A >= 60%: evidencia de fidelidad al mandato electoral — diferenciador QUIRA'
),
(
  (SELECT id FROM fondos_convocatorias WHERE codigo = 'FORD-DEMOCRACIA-2026'),
  (SELECT id FROM fondos_requisitos WHERE codigo = 'ITAM'),
  'gte', 50.0, false,
  'Transparencia institucional mínima recomendada'
);


-- ── VERIFICACIÓN ──────────────────────────────────────────────────────────────
-- SELECT c.codigo, c.nombre, COUNT(cr.id) AS n_requisitos
-- FROM fondos_convocatorias c
-- JOIN fondos_conv_requisitos cr ON cr.convocatoria_id = c.id
-- GROUP BY c.id, c.codigo, c.nombre ORDER BY c.id;
