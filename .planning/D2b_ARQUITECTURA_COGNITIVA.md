# D.2b — Arquitectura Cognitiva de Atención
## QUIRA OS · Capa de Inteligencia Pública Municipal

**Estado:** CERRADO — Insumo obligatorio para D.3  
**Fecha:** 2026-05-28  
**Prerrequisito:** D.2 Mapeo Ontológico ✅  
**Entrega:** D.3 Pantalla Principal (CAPA 1) depende de este documento  

---

## Pregunta Central

> **¿Qué siente el alcalde cuando abre QUIRA?**

La respuesta a esa pregunta determina el diseño, el valor político y la adopción institucional.

**La respuesta correcta:**
> *"Tengo el municipio en la mano. Sé exactamente dónde está el riesgo. Esto no es un reporte: es una sala de mando."*

**La respuesta que hay que evitar:**
> *"Hay que navegar para encontrar información."*
> *"Esto parece un informe Excel en la web."*
> *"No sé por dónde empezar."*

---

## 1. Modelo de Atención — Los 4 Niveles

La atención humana ante un sistema de información compleja se organiza en capas temporales. QUIRA debe diseñarse contra esas capas, no contra una lista de módulos.

```
┌─────────────────────────────────────────────────────────────┐
│  NIVEL 0 — PULSO VITAL          0 – 3 segundos              │
│  Pre-atencional. Imposible ignorar.                          │
│  El alcalde sabe si el municipio está bien o mal ANTES       │
│  de leer una sola etiqueta.                                  │
├─────────────────────────────────────────────────────────────┤
│  NIVEL 1 — NÚCLEO DOMINANTE     3 – 15 segundos             │
│  Atención focalizada. ¿Qué necesita acción ahora?            │
│  Alertas críticas. Fondos bloqueados. Desvíos activos.       │
├─────────────────────────────────────────────────────────────┤
│  NIVEL 2 — CINTURÓN COGNITIVO   15 – 60 segundos            │
│  Lectura contextual. Los 13 dominios agrupados por CAPA.     │
│  NO 13 tarjetas iguales. Peso visual = urgencia institucional│
├─────────────────────────────────────────────────────────────┤
│  NIVEL 3 — EXPLORACIÓN          60 segundos en adelante      │
│  Profundidad bajo demanda. El usuario navega hacia adentro.  │
│  Histórico, causalidades, módulos completos.                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Jerarquía Visual — Lo que Domina

### 2.1 Dominancia por Función Cognitiva

La pantalla principal NO es una colección de módulos. Es un espacio con **tres zonas cognitivas permanentes**:

```
╔══════════════════════════════════════════════════════════════╗
║  BANDA VITAL (parte superior, 80-100px)                      ║
║  4 indicadores. Siempre visibles. Sin scroll.                ║
║  Son el "electrocardiograma" del municipio.                  ╠══╗
╠══════════════════════════════════════════════════════════════╣  ║
║                           ║                                  ║  ║
║   NÚCLEO TERRITORIAL      ║   PANEL DE ESTADO               ║  ║
║   Mapa de Montecristi      ║   Alertas activas               ║  ║
║   como ancla espacial      ║   Fondos bloqueados             ║A ║
║                           ║   Acciones pendientes           ║L ║
║   [parroquias coloreadas   ║                                 ║E ║
║    por índice de urgencia] ║   Compromisos próximos          ║R ║
║                           ║                                  ║T ║
╠═══════════════════════════╩══════════════════════════════════╣A ║
║                                                              ║S ║
║  CINTURÓN COGNITIVO — 4 CAPAS × DOMINIOS                    ║  ║
║  (peso visual variable según estado real)                    ╚══╝
╚══════════════════════════════════════════════════════════════╝
```

### 2.2 Pesos Visuales — Regla de Dominancia

La jerarquía visual NO es estética. Es funcional. El tamaño y la saturación de color de cada elemento depende de su estado real:

| Estado del dominio     | Peso visual en pantalla     | Color                  |
|------------------------|-----------------------------|------------------------|
| Alerta crítica activa  | Grande, saturado, con borde | Rojo / Naranja         |
| Riesgo moderado        | Mediano, visible            | Amarillo / Ámbar       |
| En monitoreo           | Normal                      | Azul institucional     |
| Cumpliendo / Verde     | Compacto, sin énfasis       | Verde suave            |

**Principio rector:** La pantalla principal de QUIRA debe verse diferente cada día. Un día con alertas debe verse distinto a un día verde. El color y el tamaño deben comunicar estado, no decoración.

### 2.3 Anti-patrones de Dominancia (PROHIBIDOS)

| Lo que NO hacer                        | Por qué mata la jerarquía               |
|----------------------------------------|-----------------------------------------|
| 13 tarjetas del mismo tamaño           | Implica que todo tiene igual importancia|
| Colores fijos por módulo               | El color debe comunicar estado, no identidad |
| Gráficos decorativos                   | Ocupan espacio sin comunicar urgencia   |
| Banner "Bienvenido, Alcalde"           | Consume atención sin aportar información|
| Menú lateral con todos los módulos     | Democratiza lo que debe tener jerarquía |
| Barras de progreso sin umbral de alerta| Números sin acción posible              |
| Tipografía uniforme (mismo peso)       | El ojo no sabe dónde mirar primero      |

---

## 3. Flujo de Lectura — Patrón Sala de Mando

Los patrones estándar (F-pattern, Z-pattern) son para contenido editorial. QUIRA no es contenido: es infraestructura operacional. El patrón correcto es el **patrón sala de mando (Command Center)**.

```
FLUJO DE LECTURA EN QUIRA:

1. HORIZONTAL SUPERIOR (0-2s)
   Los ojos barren la Banda Vital de izquierda a derecha.
   Leen: ¿cuánto es el índice? ¿hay alertas? ¿cómo está el presupuesto?

2. DESCENSO DIAGONAL AL MAPA (2-5s)
   El mapa territorial actúa como ancla visual gravitacional.
   El alcalde busca: ¿en qué parroquia hay un problema?

3. BARRIDO AL PANEL DERECHO (5-10s)
   Las alertas activas capturan la mirada.
   El alcalde lee: ¿qué necesito decidir hoy?

4. EXPLORACIÓN DEL CINTURÓN (10-30s)
   Recién ahora el alcalde lee los 4 grupos de dominios.
   Busca: ¿en qué área está el problema?

5. ENTRADA PROFUNDA (30s+)
   Click en el dominio o alerta relevante.
   Navega hacia el módulo específico.
```

**Implicación para D.3:** El mapa de Montecristi no es un módulo más. Es el ancla gravitacional visual de toda la pantalla principal.

---

## 4. Teoría de Navegación — Cómo se Mueve el Alcalde

### 4.1 Modelo de Navegación: Contextual, no Jerárquico

QUIRA no debe tener una barra lateral con 13 módulos listados. La navegación debe ser **contextual**: emerge de lo que el alcalde ve, no de una lista predefinida.

```
MODELO INCORRECTO (menu-driven):
  [sidebar] > Salud Institucional > Fidelidad > Metas... 
  El alcalde busca en el mapa de módulos.
  Resultado: igual a cualquier sistema GovTech.

MODELO CORRECTO (state-driven):
  Pantalla principal muestra: "FONDOS BLOQUEADOS — $3.66M"
  El alcalde hace click en esa alerta.
  QUIRA lo lleva directamente al módulo de Cooperación Internacional.
  Resultado: el sistema conduce la atención hacia donde importa.
```

### 4.2 Tres Tipos de Entrada

| Tipo de entrada        | Trigger                          | Destino                          |
|------------------------|----------------------------------|----------------------------------|
| **Por alerta**         | Click en alerta del Panel Derecho | Módulo del dominio afectado      |
| **Por territorio**     | Click en parroquia del mapa      | Vista parroquial filtrada        |
| **Por dominio**        | Click en grupo del Cinturón      | Panel de dominios de esa CAPA    |

### 4.3 La Regla de los 3 Clicks

El alcalde debe poder llegar a cualquier dato crítico en máximo 3 interacciones:
1. **Click 1:** Alerta / Parroquia / Dominio en pantalla principal
2. **Click 2:** Módulo específico dentro del dominio
3. **Click 3:** Dato o acción específica dentro del módulo

---

## 5. Sensación Operacional — El Concepto Central

### 5.1 La Diferencia entre Dashboard y Sala de Mando

| Dashboard genérico                  | Sala de Mando (QUIRA)               |
|-------------------------------------|-------------------------------------|
| Muestra datos                       | Muestra estado + implicaciones      |
| El usuario busca lo importante      | Lo importante está ya destacado     |
| Actualización pasiva                | Alerta activa cuando algo cambia    |
| Todos los módulos con igual peso    | Jerarquía dinámica según estado real|
| Decoración como diseño              | Función como diseño                 |
| El usuario interpreta               | El sistema ya interpretó            |

### 5.2 El Diseño del Sentimiento — ¿Qué Produce Cada Zona?

```
BANDA VITAL
  Produce: certeza inmediata.
  El alcalde sabe en 2 segundos si hay algo urgente.
  Sin certeza = sin adopción política.

MAPA TERRITORIAL
  Produce: ubicación cognitiva.
  El alcalde siente que está mirando el municipio real,
  no una abstracción numérica.
  Sin territorio = sin autoridad espacial.

PANEL DE ALERTAS
  Produce: urgencia calibrada.
  El alcalde ve exactamente qué requiere su atención HOY.
  Sin calibración = todo parece urgente = parálisis.

CINTURÓN COGNITIVO (4 CAPAS)
  Produce: comprensión sistémica.
  El alcalde entiende en qué área institucional está el problema.
  Sin estructura = los datos flotan sin contexto.
```

### 5.3 El Contraste Visual — La Firma de QUIRA

QUIRA debe tener una paleta que comunique **autoridad institucional con precisión analítica**, no neutralidad corporativa.

**Paleta base propuesta para D.3:**

| Elemento                | Color                  | Justificación                                  |
|-------------------------|------------------------|------------------------------------------------|
| Fondo principal         | `#0A0E1A` (azul noche) | Sala de control, no oficina                   |
| Banda vital             | `#0F1629` + bordes     | Separación clara del pulso                     |
| Alerta crítica          | `#FF3B3B` (rojo puro)  | Imposible ignorar                              |
| Alerta moderada         | `#FF8C00` (ámbar)      | Atención requerida, no pánico                  |
| Estado saludable        | `#00E096` (verde QUIRA)| El color que el alcalde quiere ver             |
| Acento institucional    | `#7C5CFC` (violeta)    | QUIRA como marca, no como reporte              |
| Texto primario          | `#E8EAF0`              | Alta legibilidad sobre fondo oscuro            |
| Texto secundario        | `#8892A4`              | Jerarquía tipográfica sin decoración           |
| Mapa Folium base        | Tiles oscuros + capas  | Coherencia con paleta QUIRA                    |

**Tipografía:**
- Titulares: peso 700 o 800, no decorativos
- KPIs (Banda Vital): números grandes, fuente monoespaciada o tabular
- Etiquetas de alerta: peso 600, mayúsculas
- Texto de apoyo: peso 400, sin mayúsculas

---

## 6. Arquitectura de los 4 Grupos — Cinturón Cognitivo

Los 13 macro-dominios se presentan como **4 CAPAS agrupadas**, no como 13 elementos individuales. La CAPA es la unidad de lectura. El dominio específico es la unidad de navegación.

```
CAPA POLÍTICA          CAPA EJECUTIVA
┌────────────────┐     ┌────────────────┐
│ Dom 1          │     │ Dom 4          │
│ Salud Inst.    │     │ Holding Mun.   │
│                │     │                │
│ Dom 2          │     │ Dom 5          │
│ Fidelidad Pol. │     │ Eficiencia     │
│                │     │                │
│ Dom 3          │     │ Dom 6          │
│ Planificación  │     │ Eq. Territorial│
└────────────────┘     └────────────────┘

CAPA RENDICIÓN         CAPA TERRITORIAL
┌────────────────┐     ┌────────────────┐
│ Dom 7          │     │ Dom 11         │
│ Transparencia  │     │ Cooperación    │
│                │     │                │
│ Dom 8          │     │ Dom 12         │
│ Participación  │     │ Agenda 2030    │
│                │     │                │
│ Dom 9  Dom 10  │     │ Dom 13         │
│ Género Amb.    │     │ Observabilidad │
└────────────────┘     └────────────────┘
```

**Regla de peso visual por CAPA:**
- El peso visual de cada grupo depende del estado agregado de sus dominios
- Si Dom 1 (Salud Institucional) tiene alerta → la CAPA POLÍTICA crece visualmente
- Si todos los dominios de CAPA TERRITORIAL están verdes → ese grupo se compacta

---

## 7. La Banda Vital — Los 4 Indicadores Inamovibles

La Banda Vital son los únicos 4 elementos que el alcalde ve en ABSOLUTAMENTE TODA visita a QUIRA. No cambian de posición. Son el "electrocardiograma" del municipio.

| Posición | Indicador                | Fuente                     | Umbral de alerta         |
|----------|--------------------------|----------------------------|--------------------------|
| 1 (izq)  | Índice de Cumplimiento   | Gold Master → ICPI         | Rojo si < 60%            |
| 2        | Salud Presupuestaria     | Gold Master → ejecución    | Rojo si > 85% o < 40%    |
| 3        | Alertas Activas          | Motor SAT consolidado      | Número absoluto + ícono  |
| 4 (der)  | Fondos en Riesgo         | p18_cooperacion → bloqueado| Siempre visible en $      |

**Posición 4 — Fondos en Riesgo:** Este indicador es estratégicamente crítico porque $3.66M bloqueados representan el argumento político más poderoso de adopción. El alcalde SIEMPRE debe ver cuánto dinero está en riesgo.

---

## 8. El Mapa como Ancla — Principio Territorial

### 8.1 Por qué el Mapa va al Centro

El municipio de Montecristi tiene **5 parroquias** (1 rural: La Pila; 4 urbanas). El alcalde piensa espacialmente: "¿dónde está el problema?" no "¿en qué módulo está el problema?"

El mapa cumple tres funciones cognitivas simultáneas:
1. **Anclaje espacial** — conecta los datos con el territorio real
2. **Priorización visual** — parroquias con mayor riesgo aparecen más saturadas
3. **Entrada de navegación** — click en parroquia filtra toda la vista

### 8.2 Lo que el Mapa Comunica

```
PARROQUIA LA PILA (única rural)
→ Color según IET (Índice de Equidad Territorial)
→ Si IET < umbral: aparece con borde de alerta
→ Click: muestra estado de todas las metas PDOT para La Pila

PARROQUIAS URBANAS (4)
→ Color según índice de cumplimiento parroquial
→ Hover: tooltip con KPI resumen
→ Click: vista filtrada por parroquia
```

### 8.3 Corrección Canónica — Parroquias de Montecristi

```
PARROQUIA RURAL:    La Pila (1 — única rural)
PARROQUIAS URBANAS: Montecristi, Leonidas Plaza, 
                    Abdón Calderón, Eloy Alfaro (4)
TOTAL: 5 parroquias
```

Esta estructura debe estar hardcodeada correctamente en D.3. Error previo corregido.

---

## 9. Principios de Diseño — Mandatos para D.3

Estos principios son **no negociables** para la implementación de D.3. Son consecuencia directa de la arquitectura cognitiva:

### Principio 1 — Heterogeneidad Visual Funcional
La pantalla principal NUNCA tendrá elementos de igual tamaño. El tamaño comunica importancia. Importancia = estado institucional actual.

### Principio 2 — El Color es Estado, no Identidad
Ningún módulo o dominio tiene un "color fijo". El color es siempre consecuencia del estado del indicador correspondiente. Un dominio verde hoy puede ser rojo mañana.

### Principio 3 — La Información Primaria no Requiere Click
Los 4 indicadores de la Banda Vital, las alertas activas y los fondos en riesgo son visibles sin ninguna interacción. El alcalde recibe el estado del municipio solo con abrir la pantalla.

### Principio 4 — Sin Nomenclatura Técnica Interna
Ningún elemento en la interfaz usa términos como: SAT, TGI, ICPI, RC-M, HPT-M, Dom 1, Dom 9, ni ninguna sigla interna. El lenguaje es institucional, ejecutivo y comprensible.

| Término interno  | Traducción para la UI                    |
|------------------|------------------------------------------|
| ICPI             | Cumplimiento Municipal                   |
| TGI              | Índice de Gestión Institucional          |
| SAT              | Estado de Alerta                         |
| HPT-M            | Estado del Holding Municipal             |
| IET              | Equidad entre Parroquias                 |
| RC-M             | Registro de Cumplimiento                 |
| HITL             | Validación Técnica                       |

### Principio 5 — La Pantalla Principal es Dinámica
La pantalla principal de QUIRA debe verse diferente según el estado real del municipio. Un mes de cumplimiento alto debe verse diferente a un mes con alertas. Esto genera sensación de sistema vivo.

### Principio 6 — Profesional, No Genérico
QUIRA no debe parecer construido con un template de dashboard. Cada elemento de diseño debe tomarse una decisión deliberada. La estética genérica de IA está prohibida. El diseño debe comunicar: *infraestructura de inteligencia pública soberana*.

---

## 10. Lo que D.3 Debe Construir

Este documento (D.2b) define la teoría. D.3 construye la implementación. La lista de entregables de D.3 derivados de este documento:

| Componente D.3                  | Base en D.2b                            |
|---------------------------------|-----------------------------------------|
| Banda Vital (4 KPIs)            | Sección 7 — Los 4 Indicadores           |
| Mapa central de Montecristi     | Sección 8 — El Mapa como Ancla          |
| Panel de alertas (derecha)      | Sección 2.1 — Zona Panel de Estado      |
| Cinturón de 4 CAPAS             | Sección 6 — Grupos del Cinturón         |
| Paleta y tipografía             | Sección 5.3 — El Contraste Visual       |
| Diccionario UI (sin siglas)     | Principio 4 — Sección 9                 |
| Pesos visuales dinámicos        | Sección 2.2 — Pesos Visuales            |
| Flujo de lectura implementado   | Sección 3 — Patrón Sala de Mando        |

---

## 11. Cierre — La Respuesta a la Pregunta Central

> **¿Qué siente el alcalde cuando abre QUIRA?**

**Siente control.**
Porque en 3 segundos sabe si el municipio está bien o mal, sin navegar nada.

**Siente ubicación.**
Porque el mapa de Montecristi le devuelve el territorio real, no una abstracción.

**Siente autoridad.**
Porque las alertas son calibradas: no todo es urgente, pero lo urgente es imposible de ignorar.

**Siente que esto no es un reporte.**
Porque la pantalla cambia según el estado real. Hoy puede ser verde. Mañana puede tener una alerta roja. El sistema respira con el municipio.

**Eso es QUIRA: no un sistema de información. Un centro de comando civil del territorio.**

---

*D.2b cerrado. Prerrequisito de D.3 cumplido.*  
*Siguiente fase: D.3 — Construcción de la Pantalla Principal (CAPA 1)*
