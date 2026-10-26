# Videos publicados que `DEC-057` deja desactualizados

> **Fecha:** 26 de octubre de 2026. **Origen:** `planes/plan-cerrado-dec-057-hallazgos-operarios-2026-10-26.md`, §7.
> **Código de referencia:** Backend `develop` `a8d06dd` · Frontend `develop` `18f79f1`.
> **Publicación revisada:** `video-tutoriales-trabajo/salida/publicacion/` (subtítulos `.vtt` de las series 3, 5 y 7). Solo lectura: no se editan los `.vtt` ni los videos publicados.
> **Regrabar en una tarea aparte**, como los de `videos-desactualizados-dec-029.md`. A diferencia de `DEC-029`, este plan **no** ajustó los guiones (`videos/guiones/guiones-video-tutoriales.md`) ni los scripts de grabación (`Frontend/wms/tools/video-tutoriales/`): la tarea de regrabación los actualiza primero.

## 1. Qué cambió en pantalla

| Antes | Ahora | Decisión |
| --- | --- | --- |
| Al salir del número del documento, un aviso «Se asociará al depósito …» y el camión entraba solo al depósito abierto | Selector: una tarjeta por depósito abierto (cliente, importador o exportador, agencia, transportadora, fecha del documento, placas y camiones) y «Es otro documento: crear depósito nuevo». «Guardar» espera la elección. Los cerrados y migrados se ven en gris, con candado, sin poder elegirlos | D1–D4 |
| «N.º de manifiesto (opcional)» y «Peso según manifiesto (kg) (opcional)» | «N.º de manifiesto» y «Peso según manifiesto (kg)», obligatorios en el ingreso a depósito | D7 |
| Primer pesaje: «Peso capturado (kg)» | Primer pesaje Bruto de un ingreso a depósito: «P. indicador (kg)» y el bloque P. indicador · P. manifiesto · T. vehículo · P. mercancía | D13 |
| Detalle del ciclo e historial con el neto solo por diferencia de pesajes | Los cuatro pesos, el neto «según manifiesto» con un solo pesaje y la columna «Manifiesto (kg)» en el historial | D12, D13 |
| Tiquete sin P. MANIFIESTO ni T. VEHÍCULO | «P. MANIFIESTO», «T. VEHÍCULO» (sin segundo pesaje) y «Kilogramos (según manifiesto)»; con convenio en $0, «SIN COBRO POR CONVENIO» | D12, D16 |
| Cobro con total y modo de pago siempre | Con convenio de báscula en $0: «Sin cobro por convenio.» sin total ni modo de pago | D16 |
| Requisitos para confirmar una importación sin el manifiesto DIAN | «número del manifiesto DIAN» en la lista «Para confirmar el depósito … falta:» | D8 |
| Tarjeta con «Transportadora», «Carta Porte: … » con la fecha de ingreso y la tabla Ampara · Saldo · Unidad · Embalaje · Mercancía | Sin transportadora; «{tipo}: {número} ({fecha del documento})»; Ampara · Saldo · Mercancía con el embalaje en el texto | D17, D18 |
| Una sola tarjeta por depósito | Además, «Tarjeta del camión» en la tabla de camiones del detalle del depósito, y la columna «Tarjeta» en el historial de impresiones | D19, D20 |
| Detalle de la factura sin acción sobre el destinatario | «Cambiar destinatario» en Borrador, con los terceros de los depósitos de la factura | D23 |

## 2. Subtítulos con narración desactualizada

Rutas relativas a `video-tutoriales-trabajo/salida/publicacion/subtitulos/`.

| Archivo | Línea | Dice | Debe decir |
| --- | ---: | --- | --- |
| `serie-5/5-03-ingreso-con-deposito.vtt` | 17–21 | «El manifiesto de cada camión lo exige Comercio Exterior para confirmar; si lo tienes a la mano, digítalo aquí.» | El número y el peso del manifiesto del camión son obligatorios para guardar el ingreso |
| `serie-5/5-07-mismo-documento-varios-camiones.vtt` | 9 | «Una carta porte puede llegar en varios camiones, y todos van al mismo depósito.» | Si la carta porte ya tiene depósitos, el operario elige el depósito del camión o crea uno nuevo |
| `serie-5/5-07-mismo-documento-varios-camiones.vtt` | 29–33 | «Cuando Comercio Exterior cierra el ingreso de camiones del documento, báscula ya no puede asociar más camiones y ve quién lo cerró y cuándo.» | El depósito cerrado se ve en gris, con quién lo cerró y cuándo; no se elige, y el camión nuevo abre otro depósito |

Los demás subtítulos de las series 3, 5 y 7 no contradicen `DEC-057` (grep del 2026-10-26 de «manifiesto», «asocia», «transportadora», «tara», «neto», «etiqueta», «destinatario» y «cero»). Algunos videos quedan incompletos, sin estar errados; van en el §3.

## 3. Videos con imagen desactualizada o incompleta

Rutas relativas a `video-tutoriales-trabajo/salida/publicacion/videos/`.

| Video | Qué se ve viejo o falta |
| --- | --- |
| `serie-5/5-03-ingreso-con-deposito.mp4` | Manifiesto «(opcional)»; aviso del documento sin el selector |
| `serie-5/5-05-pesos-y-tiquete.mp4` | Primer pesaje sin los cuatro pesos; tiquete sin P. MANIFIESTO |
| `serie-5/5-06-unidades-de-carga-e-inspeccion.mp4` | Inspección de un solo pesaje sin la tara ni la mercancía según manifiesto |
| `serie-5/5-07-mismo-documento-varios-camiones.mp4` | Asociación automática al depósito y bloqueo por ingreso cerrado (§2) |
| `serie-5/5-04-el-cobro.mp4` | Falta el cobro en $0 por convenio (escena nueva) |
| `serie-5/5-08-multideposito.mp4` | Falta que el depósito adicional no acepta un documento con un depósito abierto (cambio menor) |
| `serie-5/5-11-historial-de-bascula.mp4` | Sin la columna «Manifiesto (kg)» ni el neto «según manifiesto» |
| `serie-7/7-03-confirmar-el-deposito.mp4` | La lista de requisitos de una importación no incluye el manifiesto DIAN |
| `serie-7/7-04-etiqueta-y-documentos.mp4` | Tarjeta con transportadora, fecha de ingreso junto a la carta porte y columnas Unidad y Embalaje; falta la tarjeta del camión |
| `serie-3/3-04-facturas-de-bascula-montacargas-y-guia.mp4` | Falta el cambio de destinatario de una factura en Borrador (escena nueva, o un video aparte) |

## 4. Para la tarea de regrabación

- Ajustar primero los guiones y los scripts de grabación (§1); este plan no los tocó.
- Regrabar los 10 videos del §3, que incluyen los 2 del §2, y republicar sus `.vtt`.
- `pronunciacion.json`: revisar «P. indicador», «T. vehículo» y «P. mercancía» (se leen «peso indicador», «tara del vehículo» y «peso de la mercancía»).
