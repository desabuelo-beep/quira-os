---
id: OBS-030
authority:
  parent: ADR-042
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-17
dominio: método · captura
estado: VERIFICADA
---

# OBS-030 · QUIRA declaró inaccesible un portal del Estado que funcionaba

> **Durante seis días** el registro de QUIRA sostuvo que el Portal Nacional de Transparencia de la
> Defensoría del Pueblo no respondía. **Funcionaba.** El defecto estaba en la máquina de
> observación.

## Lo que se registró, y era falso

| Fecha | Afirmación registrada | Realidad |
|---|---|---|
| 12-ago | «`transparencia.dpe.gob.ec` no responde ni a ICMP» | responde |
| 12-ago | «probado con TLS 1.2, ciphers antiguos, HTTP/1.1 e IPv4» | el transporte no era el problema |
| 13-ago | «falla desde dos redes distintas — ya no es su conexión» | **la misma VPN en las dos** |
| 13-ago | «yo saturé la API de SERCOP con ~60 peticiones» | falso; misma causa |
| 12-17 ago | eslabón de contratación como `fuente_no_accesible` | el límite era propio, pero no por eso |

## Quién lo desmintió, y cómo

Javo (2026-08-17): *«hablé con DPE Manabí, está operativa; todo el mundo puede abrir, hasta en mi
teléfono móvil. **Sólo en esta computadora no abre.** ¿Qué pasó?»* — con dos capturas: una desde su
oficina, otra desde su casa.

**Esa prueba rompió la hipótesis**, y el director no la había intentado: se probó el transporte, el
endpoint, las cabeceras y el TLS, pero **nunca se contrastó contra un segundo dispositivo en la
misma red.**

## La causa, en cuatro medidas

```
1 · TCP 443 → conecta          181.113.20.28 · el puerto acepta
2 · TLS     → «Recv failure: Connection was reset» durante el handshake
3 · MTU     → payload 1400 no pasa · 1300 sí pasa
4 · ruta    → sale por «ProTUN» · IP origen 10.2.0.2 · métrica 1
```

Hay una **VPN activa** con prioridad sobre el Wi-Fi. Declara MTU 1420; la ruta real admite ~1300.
El saludo TLS moderno supera ese tamaño y **se pierde en silencio**; el handshake TCP, pequeño,
pasa sin problema.

Eso explica **todos** los síntomas, incluidos los que parecían contradictorios:

| Síntoma | Explicación |
|---|---|
| TCP conecta pero TLS muere | el paquete grande se pierde |
| Corte siempre a ~20 s | tiempo de espera de una respuesta que nunca llegará |
| Intermitente en SERCOP | según el tamaño del saludo y del certificado del servidor |
| Funciona en el teléfono | sin VPN |
| Dos proveedores TLS fallan igual | el problema es anterior al proveedor |

**Ni la DPE, ni McAfee, ni un filtro de TICs, ni saturación nuestra.** Una VPN mal ajustada.

## Por qué esto es grave, y no un contratiempo técnico

QUIRA existe para distinguir **«no existe»** de **«no pude obtener»** (ADR-042 §6). Durante seis
días el registro sostuvo lo primero cuando correspondía lo segundo — **en la herramienta construida
para impedir exactamente ese error**.

> Si esto hubiera llegado a un producto, **QUIRA habría publicado que un portal del Estado no
> funciona cuando funcionaba perfectamente.** Y lo habría hecho con procedencia, SHA, estados
> tipados y trazo punteado: con toda la maquinaria de rigor apuntando a una conclusión falsa.

La disciplina no falló por falta de método. Falló porque **el método sólo se aplicaba hacia
afuera**.

## La regla que este episodio obliga a fijar

> **Antes de atribuir una anomalía a la fuente observada, QUIRA debe intentar falsar la hipótesis
> de que la anomalía proviene de su propio instrumento de observación.**
> *(formulación del colega, 2026-08-17 — adoptada)*

**El observador también debe ser auditable.** Y auditarse no es repetir la misma prueba con más
cuidado: es **cambiar de instrumento**. Se probaron cinco variantes de TLS sobre la misma máquina
—cinco formas de repetir el mismo error—; bastaba un segundo dispositivo.

### Comprobaciones mínimas antes de declarar una fuente inaccesible

1. ¿Responde desde **otro dispositivo** en la misma red?
2. ¿El TCP conecta y sólo falla el TLS? → apunta al instrumento
3. ¿Por qué **interfaz** sale el tráfico? ¿Hay VPN, proxy o túnel?
4. ¿Cuál es la **MTU efectiva** de esa ruta?
5. ¿Fallan **dos clientes** con proveedores TLS distintos? → el problema es anterior a ambos

Si no se han hecho las cinco, el estado correcto no es `fuente_no_accesible` sino
**`instrumento_no_descartado`**.

## Corrección aplicada

- El eslabón de contratación deja de atribuirse a la fuente.
- Se retiran del registro las afirmaciones sobre la indisponibilidad de la DPE.
- Solución pendiente de ejecución con permisos de administrador:
  `netsh interface ipv4 set subinterface "ProTUN" mtu=1300 store=persistent` — o desconectar la VPN.

## Trazabilidad

| Evidencia | Medida |
|---|---|
| `Test-NetConnection` DPE:443 | `TcpTestSucceeded: True` · 181.113.20.28 |
| `curl -v` | `schannel: failed to receive handshake` |
| `ping -f -l 1400` / `-l 1300` | no pasa / pasa |
| `Find-NetRoute 181.113.20.28` | `ProTUN` · origen 10.2.0.2 |
| Capturas de Javo | portal operativo desde móvil, dos ubicaciones |

---
*OBS-030 · Dylus Lab © 2026 · desmentido por Javo · la evidencia estaba disponible desde el primer día.*
