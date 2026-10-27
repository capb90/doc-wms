# Fase 5 — Comercio Exterior

> Lee antes `00-plan-maestro.md`. Rol principal: **Comercio exterior** (`c_exterior`). Verificaciones con `bascula`, `bodega`, `facturacion` y Admin.

## 1. Objetivo

Validar que Comercio Exterior, dueño del depósito, puede completarlo y confirmarlo, corregirlo, anularlo y cerrar el ingreso de camiones; registrar manifiesto y levantes y obtener la nacionalización; crear, modificar, cancelar y revertir órdenes de cargue; emitir y anular guías de salida con saldos congelados; controlar el abandono; imprimir etiquetas, y que cada acción tenga el efecto correcto en stock, facturación y notificaciones.

## 2. Alcance

| Pantalla | Ruta | Bloques |
|---|---|---|
| Tablero | `/foreign-trade` | TAB |
| Depósitos (kanban) | `/foreign-trade/deposits` | LIS |
| Importaciones, exportaciones, inspecciones (listas con filtros multicriterio WMS-13) | `/foreign-trade/imports|exports|inspections` | LIS |
| Detalle del depósito | `…/[id]` | CNF, PRD, COR, ANU, AJU, FEC, ETI, IMP, LEV, VAL |
| Órdenes de cargue | `/foreign-trade/loading-orders[/create|/[id]]` | OC |
| Guías de salida, pendientes, crear | `/foreign-trade/dispatch-guides[/pending|/create]` | GUI |
| Levantes (consulta) | `/foreign-trade/releases` | REL |
| Listas de empaque | `/foreign-trade/packing-lists` | PKL |
| Abandono | `/foreign-trade/abandonment` | ABA |

**Fuera:** importes de facturas (fase 6); reportes de CE (fase 7).

## 3. Criterios de entrada

1. Fases 3 y 4 aprobadas (o con CRITICAL aceptados).
2. Depósitos en Borrador de la fase 3: IMP `QA-CP-0001` (2+ camiones), EXP `QA-CP-0002`, INSP `QA-CP-0003`, IMP con unidades de carga `QA-CP-0005`.
3. `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` configurado (F1-PAR-002).
4. Ciudades y cuadrillas de la fase 1.
5. Si ya se ejecutó la «Preparación asistida» de las fases 3 o 4, reutilizar esos datos y anotarlo.

## 4. Reglas que se verifican

- **Confirmar** (Draft → Confirmed) exige, en orden: cliente; fecha del documento; terceros por modalidad (IMP: importador y agencia de aduanas; EXP: exportador; INSP: ninguno); en IMP, el número del manifiesto DIAN (`DEC-057` D8; la fecha no); moneda; valor > 0; por camión, N.º y peso de manifiesto > 0; con unidades de carga, mercancía en cada unidad y suma por unidad = declarado. Mensaje: «No se puede confirmar el depósito {n}. Falta: a; b; c.». **No exige la recepción de Bodega.** Confirmar abre el período de almacenamiento y su factura en la misma transacción.
- **Levantes:** solo con el depósito confirmado; por producto; cantidad ≤ recibido − otros levantes; duplicados de número/aceptación entre depósitos rechazados; FOB con TRM DIAN del día (3 s) o tasa manual. Nacionalizado = suma de levantes > 0. Nacionalizado disponible por producto = máx(0, levantes − (despachado + reservado)).
- **Orden de cargue:** ningún depósito en Borrador; al menos un cliente; IMP nacionalizado; cliente no bloqueado; stock disponible; tope de nacionalizado disponible; coherencia de unidades de carga; ciudad activa; orden externa (emisor agencia o importador, número único por emisor, fecha no futura); cuadrilla activa. Multi-cliente permitido (CE-12).
- **Guía (IMP):** depósitos no en Borrador; tipo por el primer ítem; orden no Dispatched/Complete/Cancelled/Reverted; una guía vigente por orden; cargo GUIA_SALIDA; saldos congelados por línea (WMS-19). EXP: guía automática al cargar, sin cargo.
- **Abandono:** plazo 30 días (60 con prórroga) desde la fecha de ingreso; alerta desde plazo − 10.
- Consecutivos: `2026OC00001`, `2026S00001`.

## 5. Casos

### 5.1 Tablero (TAB)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-TAB-001 | Tarjetas | Abrir `/foreign-trade`. | Sin nacionalizar, Nacionalizados, Órdenes pendientes, Guías pendientes, aviso de abandono, accesos directos. | P1 | FUN |
| F5-TAB-002 | Conteos | Comparar cada tarjeta con las listas filtradas. | Coinciden. Riesgo R-CE-04: Sin nacionalizar/Nacionalizados pueden contar depósitos anulados o cerrados (verificar tras F5-ANU-001 y un depósito cerrado). | P1 | RN |
| F5-TAB-003 | Enlace de Guías pendientes | Clic en la tarjeta. | Esperado: `/dispatch-guides/pending`. Riesgo R-CE-04: lleva al historial. | P3 | UX |

### 5.2 Listados y búsqueda multicriterio — WMS-13 (LIS)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-LIS-001 | Kanban de depósitos | `/deposits`: filtrar por tipo y fechas; «Limpiar filtros»; clic en una tarjeta. | Columnas Borrador, Confirmado, Anulado y Cerrado, cada una con su total; navega al detalle de la modalidad correcta. **Actualizado (`DEC-058`, K3):** arriba quedan solo el tipo (Importación, Exportación, Inspección), «Desde», «Hasta» y «Limpiar filtros», que limpia las fechas y deja el tipo. Ya no hay buscador general de número ni selector de estado: se busca en cada columna (F5-LIS-009). Al cambiar un filtro, el tablero no se vacía mientras carga. | P1 | FUN |
| F5-LIS-002 | Filtros de importación | En `/imports`, probar cada criterio: estado, depósito, carta porte, manifiesto, placa de unidad de carga, cliente, importador, agencia, transportadora, producto, rango de fechas, placa del camión, levante/aceptación. | Cada criterio filtra; combinados son Y lógico; texto sin tildes ni mayúsculas. | P1 | FUN |
| F5-LIS-003 | Filtros en la URL | Aplicar filtros, copiar la URL, abrirla en otra pestaña. | Mismos filtros y resultados; al cambiar un filtro vuelve a la página 1. | P2 | PER |
| F5-LIS-004 | Rango de fechas invertido | Desde > hasta. | «La fecha inicial no puede ser posterior a la final.». | P2 | VAL |
| F5-LIS-005 | Exportar Excel | Exportar con filtro. | Todas las filas del filtro. | P2 | FUN |
| F5-LIS-006 | Listas EXP e INSP | Repetir filtros básicos. | Funcionan (sin criterios exclusivos de IMP). | P2 | FUN |
| F5-LIS-007 | Scroll por columna | `/deposits` a 1366×768 y a 1920×1080, con más de 20 depósitos en una columna (en `wms_qa_preprod`, Confirmado). Bajar dentro de la columna. | **Nuevo (`DEC-058`, K4):** cada columna se desplaza por dentro, sin paginador; la página no se alarga con los depósitos y el pie de las columnas se ve sin bajar la página; sin scroll horizontal. Cada tarjeta tiene su borde y sus etiquetas pequeñas. | P1 | UI |
| F5-LIS-008 | Carga infinita | Seguir bajando la columna de F5-LIS-007 hasta el final. | **Nuevo (`DEC-058`, K2 y K4):** carga de 20 en 20 con «Cargando más…», sin repetir ni saltar depósitos: al final, la cantidad de tarjetas es igual al total del encabezado y sale «No hay más depósitos». | P1 | FUN |
| F5-LIS-009 | Buscador por columna | En el buscador de una columna («Documento, depósito, tercero o producto»), buscar por: número de depósito; carta porte; número de un documento adicional; nombre del cliente sin tildes; una agencia de aduanas (no sale en la tarjeta); un producto. Probar un texto sin resultados y uno con `%` o `_`. | **Nuevo (`DEC-058`, K1 y K4):** cada búsqueda filtra solo esa columna, tras una espera corta y con una sola consulta; la columna vuelve al inicio y su total cambia; las demás columnas no cambian. Sin resultados, «Sin depósitos». `%` y `_` se buscan tal cual, no como comodines. | P1 | FUN |
| F5-LIS-010 | Búsqueda demasiado larga | Por API, `GET foreign-trade/deposits?status=Draft&search=` con 101 caracteres. | **Nuevo (`DEC-058`, K1):** 400 «La búsqueda admite hasta 100 caracteres.». | P3 | VAL |

### 5.3 Completar y confirmar el depósito (CNF)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-CNF-001 | Confirmar IMP completo | Detalle de `QA-CP-0001`: asignar cliente `QA Cliente Uno`; datos de Borrador (fecha del documento, moneda USD, valor 50.000); terceros importador `QA Importador` y agencia `QA Agencia SIA`; manifiesto por camión (N.º y peso); manifiesto DIAN `QA-DIAN-0001` (F5-IMP-001) → «Confirmar depósito». | `Confirmed`; sugiere reimprimir etiqueta; período de almacenamiento y factura abiertos (ver en Facturación). Con USD, TRM DIAN o «TRM pendiente» (aviso a Facturación). | P0 | FUN |
| F5-CNF-002 | Requisitos pendientes | En un depósito sin nada, revisar el botón «Confirmar». | Deshabilitado con el motivo; por API: «No se puede confirmar el depósito … Falta: cliente; fecha del documento; importador; agencia de aduanas; número del manifiesto DIAN; moneda; valor…; manifiesto…». | P0 | RN |
| F5-CNF-003 | Requisitos por modalidad | EXP sin exportador; INSP sin importador ni agencia. | EXP rechazado por exportador; INSP no los pide. | P0 | RN |
| F5-CNF-004 | Confirmar sin recepción | Confirmar un depósito cuya recepción no se hizo. | Se permite (WMS-9). | P0 | RN |
| F5-CNF-005 | Asignar cliente sin rol | Asignar un tercero sin rol CUSTOMER (por API si la UI lo filtra). | «El tercero seleccionado no tiene el rol CUSTOMER.». | P1 | VAL |
| F5-CNF-006 | Propagación del cliente | Asignar cliente a un depósito cuya factura de báscula no tenía destinatario. | La factura de báscula y los períodos sin cliente toman el cliente. | P1 | INT |
| F5-CNF-007 | Fecha del documento | Fecha futura; la misma de otro depósito abierto del mismo documento. | Rechazados (la segunda con 409). | P2 | VAL |
| F5-CNF-008 | Terceros duplicados | Dos importadores. | Rechazado (sin roles duplicados). | P2 | VAL |
| F5-CNF-009 | Editar Borrador tras confirmar | En Confirmed, intentar cambiar moneda o valor. | «Solo se puede editar un depósito en estado Draft. Estado actual: Confirmed.» (estado en inglés, R-CE-07). | P1 | RN |
| F5-CNF-010 | Cerrar ingreso de camiones | «Cerrar ingreso de camiones» en `QA-CP-0001` (tras F3-MCA-009 si se quiere probar camión tardío antes). | Confirmación; el servicio pasa a Completed; báscula ya no acepta camiones (F3-MCA-007); un segundo cierre → 409 «…ya fue cerrado.». | P0 | INT |
| F5-CNF-011 | Confirmar EXP e INSP | Completar y confirmar `QA-CP-0002` y `QA-CP-0003`. | `Confirmed`. | P0 | FUN |
| F5-CNF-012 | Confirmar con unidades de carga | `QA-CP-0005`: confirmar con la mercancía por unidad cuadrada; luego un caso descuadrado (si se puede preparar con 2 unidades). | Cuadrado: confirma; descuadrado: «Falta: …» por unidad. | P1 | RN |
| F5-CNF-013 | Planilla de envío (WMS-14) | Editar en Draft, Confirmed y Closed; 101 caracteres; vacía. | Editable en los tres estados; > 100 rechazado; vacía la borra; en Cancelled rechazada. | P2 | RN |
| F5-CNF-014 | Manifiesto por camión | Editar N.º y peso del manifiesto de un camión en Confirmed. | Se guarda; recalcula la factura (WEIGHT_THRESHOLD si aplica). | P2 | INT |
| F5-CNF-015 | Corregir placa de unidad de carga | Cambiar la placa de `QAT001` (Draft/Confirmed); poner una placa ya existente en el depósito. | Se guarda; duplicada rechazada. | P3 | RN |
| F5-CNF-016 | Documentos (PDF consolidado) | «Documentos». | PDF consolidado del depósito. | P3 | FUN |
| F5-CNF-017 | Manifiesto DIAN para confirmar la importación | IMP completo salvo el manifiesto DIAN: ver «Para confirmar el depósito … falta:» y pulsar el requisito; «Confirmar» por API. Registrar solo el número (sin fecha) y confirmar. Repetir con EXP e INSP. | **Nuevo (`DEC-057`, D8):** la lista dice «número del manifiesto DIAN» y su enlace lleva a la sección «Manifiesto DIAN»; por API, 400 «No se puede confirmar el depósito {N}. Falta: número del manifiesto DIAN.». Al guardar el número, la lista se actualiza sola y el depósito confirma; la fecha no se exige. EXP e INSP no lo piden. Un migrado que vuelve a Borrador también lo necesita al reconfirmar. | P0 | RN |

### 5.4 Productos del depósito por camión — WMS-29 (PRD)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-PRD-001 | Editar cantidad en Borrador | En un depósito Draft, cambiar la cantidad de un producto de un camión con motivo ≥ 10. | Total del depósito = suma de camiones; stock ajustado; aviso a CE si queda diferencia con lo contado por Bodega. | P1 | RN |
| F5-PRD-002 | Agregar producto | Agregar `QA Aceite` a un camión. | Aparece en el depósito con stock. | P1 | FUN |
| F5-PRD-003 | Eliminar producto con dependencias | Eliminar un producto con recepción, levante, reserva o movimientos. | Bloqueado con el motivo (orden: recepción, levante, reserva, movimientos, orden). | P1 | RN |
| F5-PRD-004 | Cambiar producto del catálogo | «Cambiar producto» en una línea con solo el ingreso declarado. | Se permite (ignora el movimiento de ingreso declarado). Anotar si la UI muestra igualmente «ya tiene movimientos de inventario». | P2 | RN |
| F5-PRD-005 | Editar en Confirmed | Intentar editar productos en Confirmed. | «Solo se pueden editar los productos de un depósito en Borrador.». | P1 | RN |
| F5-PRD-006 | Motivo | Motivo de 9 caracteres. | Rechazado (10–500). | P2 | VAL |
| F5-PRD-007 | Reparto en unidades de carga | `PUT …/cargo-unit-breakdown` desde la UI en Draft. | Se guarda; en Confirmed rechazado. | P3 | RN |

### 5.5 Devolver a Borrador (COR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-COR-001 | Devolver para corrección | En un depósito Confirmed sin dependencias: tabla de productos → devolver. | `Draft`; observaciones con «Corrección solicitada: …». | P1 | FUN |
| F5-COR-002 | Reconfirmar | Corregir y confirmar otra vez. | `Confirmed`; la factura del período se recalcula con lo corregido (valor, moneda, agencia, cliente o productos), sin duplicarse (DEF-F11-030, DEC-056). | P0 | PER |
| F5-COR-003 | Desde Draft | Devolver uno en Draft (por API). | «Solo se puede devolver para corrección un depósito en estado Confirmed…». | P2 | RN |
| F5-COR-004 | Depósito migrado | (Si hay migrados.) | 409 «…viene del legacy: corrija sus cantidades con un ajuste de inventario.». | P3 | RN |
| F5-COR-005 | Devolver con OC activa | Depósito con OC `Pending` → devolver a Borrador. | Esperado de negocio: bloquear o advertir. Riesgo R-CE-05: se permite. Luego F4-CAR-014. | P1 | RN |
| F5-COR-006 | Guía con depósito en Borrador | Con el depósito de F5-COR-005 en Draft, intentar emitir la guía de la OC. | «No se pueden generar guías de salida para depósitos en estado Borrador…». | P1 | RN |
| F5-COR-007 | Corregir valor o moneda en Borrador recalcula la factura | Depósito `Confirmed` con tarifa `PERCENTAGE_OF_VALUE` y factura del período en Borrador → devolver a Borrador → cambiar el valor (p. ej. USD 10.000 → 20.000) o la moneda (COP → USD) o la agencia → guardar → reconfirmar. | **Nuevo (DEF-F11-030, DEC-056):** al guardar, la misma factura se recalcula con lo nuevo (al pasar a USD toma la TRM de la DIAN o queda «TRM pendiente»); con la agencia nueva, el detalle dice «AGENCIA: …». Con la factura aprobada conserva el número y avisa a Facturación con el total anterior y el nuevo. Reconfirmar no duplica ni vuelve a recalcular. | P0 | PER |
| F5-COR-008 | Cambiar el cliente con factura de almacenamiento | Depósito devuelto a Borrador: cambiar el cliente con la factura del período en Borrador; repetir con la factura aprobada; y con la factura anulada sin refacturar, refacturar. | **Nuevo (DEC-056):** en Borrador, la factura y los períodos pasan al cliente nuevo con su convenio. Aprobada (o consolidada): 409 «La factura de almacenamiento {N.º} del depósito {número} está aprobada: Facturación debe anularla antes de cambiar el cliente.» y nada cambia. Anulada: la refacturación sale al cliente nuevo. | P0 | RN |

### 5.6 Anular depósito (ANU)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-ANU-001 | Anular depósito en Borrador | Crear (en báscula) un depósito de prueba `QA-CP-0020` y anularlo con motivo 10–500. | `Cancelled`; stock sacado con movimiento `StorageCancellation`; ubicaciones liberadas; servicio descartado; vuelve a `/deposits`. | P0 | FUN |
| F5-ANU-002 | Motivo obligatorio | Motivo vacío o de 9. | Rechazado. | P1 | VAL |
| F5-ANU-003 | Anular Confirmed con OC Pending | Depósito confirmado con OC pendiente (solo de ese depósito) → anular. | La OC se cancela y se liberan reservas; períodos cerrados; facturas anuladas según política; avisos a Bodega y Facturación. | P1 | INT |
| F5-ANU-004 | OC mixta | OC con ítems de dos depósitos → anular uno. | Se quitan sus ítems de la OC y se liberan sus reservas; la OC sigue con el otro. | P2 | RN |
| F5-ANU-005 | Con salida ejecutada | Depósito con OC Loaded/Dispatched. | 409 «…tiene salidas ejecutadas en la orden … Revierta primero la salida.». | P1 | RN |
| F5-ANU-006 | Con camión en báscula | Depósito con un ciclo abierto. | 409 (camión aún en báscula). | P2 | RN |
| F5-ANU-007 | Cerrado o ya anulado | Anular uno cerrado; anular dos veces. | «No se puede anular un depósito cerrado.» / «El depósito ya está anulado.». | P2 | RN |

### 5.7 Ajuste de inventario CE-7 (AJU)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-AJU-001 | Ajustar cantidad | Tras la diferencia de F4-REC-006, ajustar `QA Cebolla` del depósito a la cantidad real con observación. | Cantidad del depósito = valor absoluto nuevo; stock movido por la diferencia; correo al parámetro; factura del período recalculada. | P0 | RN |
| F5-AJU-002 | Observación obligatoria | Sin observación. | Rechazado. | P1 | VAL |
| F5-AJU-003 | Unidad de carga | En un depósito de unidades, sin indicar unidad. | Rechazado (exige la unidad). | P2 | VAL |
| F5-AJU-004 | Ajuste inválido envía correo | Ajustar a la misma cantidad actual; o por debajo de lo reservado. | Esperado: rechazo sin correo. Riesgo R-CE-01: se envía el correo antes de validar (revisar Mailtrap o el log). | P1 | RN |
| F5-AJU-005 | Por debajo de los levantes | Producto con levante 100 → ajustar a 50. | Esperado: rechazo (pendiente por nacionalizar negativo). Riesgo R-CE-01: se permite. | P1 | RN |
| F5-AJU-006 | Sin parámetro de correo | (Local) vaciar el parámetro temporalmente y ajustar; restaurar. | «No hay correo de administrador configurado para la edición de inventario…». | P2 | ERR |
| F5-AJU-007 | Estado | Ajustar un depósito Closed o Cancelled. | Rechazado (solo Draft o Confirmed). | P2 | RN |

### 5.8 Fecha de ingreso — WMS-33 (FEC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-FEC-001 | Corregir fecha de ingreso | En un depósito confirmado, cambiar la fecha dentro de la estadía del primer camión con motivo. | Se guarda; recalcula el período; si la TRM es DIAN y cambia el día, se borra y se vuelve a consultar. | P1 | RN |
| F5-FEC-002 | Fuera de rango o igual | Antes del ingreso del camión; la misma fecha. | Rechazados. | P2 | VAL |
| F5-FEC-003 | Etiqueta y abandono | Tras F5-FEC-001, reimprimir etiqueta y ver el plazo de abandono. | Ambos usan la nueva fecha. | P2 | INT |

### 5.9 Etiquetas (ETI)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-ETI-001 | Etiqueta IMP sin nacionalizar | «Imprimir etiqueta» en un IMP sin levantes, con un producto cuya descripción repite el nombre (p. ej. «CEBOLLA FRESCA») y embalaje. | «MERCANCIA SIN NACIONALIZAR» en rojo; fecha de ingreso, importador, intermediario, placas y cantidades. **Actualizado (`DEC-057`, H10, H13–H15):** sin «Transportadora»; la línea del documento dice «{tipo}: {número} ({fecha del documento})», p. ej. «Carta Porte: QA-CP-0001 (2026-10-25)», o «N/A» sin fecha; la tabla es Ampara · Saldo · Mercancía, con el embalaje en el texto y el nombre sin repetir («CEBOLLA FRESCA (SACOS)»), sin columnas de unidad ni embalaje. | P0 | FUN |
| F5-ETI-002 | Etiqueta nacionalizada | Tras F5-LEV-001. | «MERCANCIA NACIONALIZADA» en verde. | P0 | RN |
| F5-ETI-003 | EXP e INSP | Imprimir. | «MERCANCIA PARA EXPORTACION» / «INSPECCION ADUANERA». **Actualizado (`DEC-057`):** sin «Transportadora», con el bloque «Documentos:» que lista cada documento como «{tipo}: {número} ({fecha})» y la tabla de 3 columnas de F5-ETI-001. | P1 | FUN |
| F5-ETI-004 | Nacionalizada con levante parcial | IMP con 2 productos, levante solo de uno y parcial. | Anotar: el código imprime «NACIONALIZADA» con cualquier levante (R-CE-06). Confirmar con el usuario si es correcto. | P2 | RN |
| F5-ETI-005 | Contador de impresiones (GAP-024) | Imprimir 3 veces; ver el badge. | El contador sube; lista de impresiones con usuario y fecha. | P2 | FUN |
| F5-ETI-006 | Anulado | Depósito anulado. | Botón no disponible. | P3 | RN |
| F5-ETI-007 | Cantidad tras despacho | Tras una salida parcial, reimprimir. | La etiqueta muestra el saldo. | P2 | INT |
| F5-ETI-008 | Tarjeta del camión | En el detalle de un IMP, un EXP y un INSP con 2 camiones: en la tabla de camiones, «Tarjeta del camión» de cada uno. | **Nuevo (`DEC-057`, H12, D19):** PDF con el encabezado de la tarjeta del depósito (número con código de barras, importador o exportador, intermediario, fecha de ingreso), «Placa: {placa}» y sus unidades de carga, la línea del documento, «Manifiesto No. {manifiesto del camión}», la tabla «Cant. ingresa · Mercancía» solo con lo que trajo ese camión y la franja de estado. Sin Ampara ni Saldo. | P1 | FUN |
| F5-ETI-009 | Tarjeta del camión: anulado, otro depósito y registro | Un camión anulado del depósito; por API, la tarjeta con el Id de un camión de otro depósito. Después, ver el historial de impresiones. | **Nuevo (`DEC-057`, D19 y D20):** el camión anulado no ofrece el botón (por API, 400 «No se puede imprimir la tarjeta de un camión anulado.»); el de otro depósito, 404 «El camión no pertenece al depósito.». El historial agrega la columna «Tarjeta» («Depósito» o «Camión {placa}») y el contador suma las dos tarjetas. Un depósito migrado (sin camiones) no la ofrece. | P2 | RN |

### 5.10 Importación: manifiesto, levantes, validación (IMP, LEV, VAL)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-IMP-001 | Manifiesto DIAN | Registrar N.º (≤ 200) y fecha (no futura). | Se guarda; 201 caracteres o fecha futura rechazados. Desde `DEC-057` (D8) el número es requisito para confirmar la importación (F5-CNF-017). | P1 | VAL |
| F5-LEV-001 | Registrar levante | En `QA-CP-0001` confirmado: levante N.º `QA-LEV-001`, aceptación, fecha, `QA Cebolla` cantidad 100, peso, FOB USD. | Se registra; tasa = TRM DIAN del día (o pide tasa manual si la DIAN no responde); estado `Nacionalizado`; nacionalizado disponible 100. | P0 | FUN |
| F5-LEV-002 | Levante en Borrador | En un IMP en Draft. | «No se pueden registrar levantes en un depósito en estado Borrador. Confirme primero el depósito.». | P0 | RN |
| F5-LEV-003 | Cantidad mayor a lo pendiente | Levante de 200 si el recibido es 160 y hay 100 levantados. | «La cantidad a levantar (200) supera lo pendiente por nacionalizar del producto (60).». | P0 | RN |
| F5-LEV-004 | Número duplicado en otro depósito | Usar `QA-LEV-001` en otro depósito. | 409. | P1 | RN |
| F5-LEV-005 | Mismo número, otro producto | `QA-LEV-001` para `QA Aceite` del mismo depósito. | Permitido (DF4: el FOB arranca vacío con aviso). | P2 | RN |
| F5-LEV-006 | Sin TRM | (Local, sin red a la DIAN) registrar levante sin tasa. | «No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el FOB.»; con tasa manual se registra. | P2 | ERR |
| F5-LEV-007 | Editar levante | Reducir de 100 a 70 sin despachos. | Se guarda; nacionalizado disponible 70. | P1 | FUN |
| F5-LEV-008 | Reducir por debajo de lo usado | Con 80 reservados, reducir a 70. | 409 «No se puede reducir el levante…». | P1 | RN |
| F5-LEV-009 | Retirar levante | Retirar uno con motivo 10–500 sin uso. | Borrado; si queda sin levantes, `SinNacionalizar` y aviso a CE. | P1 | FUN |
| F5-LEV-010 | Retirar con uso | Retirar uno cubierto por reservas. | 409. | P1 | RN |
| F5-LEV-011 | Fechas y cantidades | Fecha futura; cantidad 0. | Rechazados. | P2 | VAL |
| F5-LEV-012 | Levante en depósito anulado o cerrado | Por API (o UI si muestra el botón) registrar levante en Cancelled/Closed. | Esperado: rechazo. Riesgo R-CE-03: se permite. | P1 | RN |
| F5-LEV-013 | Botón en estados no válidos | Ver «Registrar levante» en Draft y en anulado. | Esperado: oculto. Riesgo R-CE-03: visible. | P3 | UI |
| F5-VAL-001 | Validar depósito e imprimir | «Validar depósito e imprimir etiqueta» con datos que cuadran. | Marca `ValidatedAt` una sola vez; imprime. | P2 | FUN |
| F5-VAL-002 | Validación con diferencia | Plantilla con peso distinto. | Observaciones obligatorias; correo a Admin. Anotar textos: riesgo R-CE-02 de caracteres corruptos («dep?sito»). | P2 | ERR |
| F5-VAL-003 | Varios camiones | Validar `QA-CP-0001` (2+ camiones) con el peso total correcto. | Esperado: sin descuadre. Riesgo R-CE-02: compara solo el último ciclo y marca descuadre falso. | P2 | RN |

### 5.11 Órdenes de cargue (OC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-OC-001 | Crear OC de importación | Nueva orden: depósito `QA-CP-0001`, `QA Cebolla` 80, vehículo `QAB205`, conductor, ciudad `QA QUITO`, cuadrilla, orden externa (emisor `QA Agencia SIA`, N.º `QA-OE-001`, fecha hoy, soporte PDF ≤ 10 MB). | OC `2026OC000nn` `Pending`; reserva 80; disponible del producto baja; nacionalizado disponible baja. | P0 | FUN |
| F5-OC-002 | Selector de depósitos | Abrir el selector. | Solo depósitos activos, no Draft ni anulados, con cliente y disponible > 0; muestra «Nacionalizado disponible» y «Sin levante» si es 0. | P1 | RN |
| F5-OC-003 | Depósito en Borrador (API) | Crear por API con un depósito Draft. | «No se pueden crear órdenes de cargue para depósitos en estado Borrador…». | P1 | RN |
| F5-OC-004 | Sin nacionalizar | IMP confirmado sin levante. | «El depósito de importación … no está nacionalizado…». | P0 | RN |
| F5-OC-005 | Excede nacionalizado disponible | Pedir más que el nacionalizado disponible. | «La cantidad solicitada de «QA Cebolla» … supera lo nacionalizado disponible (…). Registre el levante antes de despachar.». | P0 | RN |
| F5-OC-006 | Excede stock | Pedir más que el disponible. | «Stock disponible insuficiente para producto … Disponible: x, Solicitado: y». | P0 | RN |
| F5-OC-007 | Cliente bloqueado | Depósito de `QA Cliente Mora` bloqueado. | «El cliente '…' está bloqueado por deuda pendiente…». | P0 | RN |
| F5-OC-008 | Orden externa | Emisor sin rol agencia ni importador; número repetido para el mismo emisor; fecha futura; soporte de 11 MB o .docx. | Rechazados con mensajes: «El emisor de la orden externa debe ser una agencia de aduanas o un importador registrado.», «La orden externa … ya está registrada para …». | P1 | VAL |
| F5-OC-009 | Ciudad o cuadrilla inactivas | Usar una inactiva. | Rechazado. | P2 | VAL |
| F5-OC-010 | Fecha programada | Más de 2 h en el pasado. | Rechazada. | P3 | VAL |
| F5-OC-011 | Exportación | OC del EXP confirmado (no exige nacionalización). | Se crea. | P0 | FUN |
| F5-OC-012 | Unidades de carga | OC de `QA-CP-0005` mezclando suelta y unidades. | Rechazado por coherencia; con la unidad correcta se crea. | P2 | RN |
| F5-OC-013 | Multi-depósito | OC con dos depósitos del mismo cliente. | Se crea; reservas en ambos. | P1 | FUN |
| F5-OC-014 | Multi-cliente (CE-12) | OC con depósitos de `QA Cliente Uno` y `QA Multirol`. | Se crea; valida mora de ambos. Anotar: `StakeholderId` y el firmante son el primer cliente; el DTO concatena nombres (R-CE-08). | P1 | RN |
| F5-OC-015 | Modificar ítems | En `Pending`, cambiar 80 → 60 con motivo. | Reserva 60; si estaba `InProgress`, aviso a Bodega. Con una guía vigente responde 409 «Anule primero la guía {n} de la orden {OC}: la guía tiene las cantidades de la orden.» (F5-OC-023). | P1 | FUN |
| F5-OC-016 | Cancelar | Cancelar una `Pending` con motivo 10–500. | `Cancelled`; reservas liberadas. Ya cargada: «…ya fue cargada: use «Revertir salida».». Con guía vigente: 409 «Anule primero la guía…» (F5-OC-023). | P0 | FUN |
| F5-OC-017 | Revertir salida | OC `Loaded`/`Dispatched` sin guía vigente → «Revertir salida». | Stock devuelto con movimiento; depósito cerrado se reabre (`Confirmed`); período reabierto o abierto. | P0 | RN |
| F5-OC-018 | Revertir con guía vigente | Con guía emitida. | «Anule primero la guía … de la orden …». | P1 | RN |
| F5-OC-019 | Listado y filtros | `/loading-orders`: estados y un criterio a la vez (orden interna/externa, documento, depósito, fecha de ingreso en dos formatos, importador, transportadora, manifiesto, producto, placa). | Filtros correctos; Excel. | P2 | FUN |
| F5-OC-020 | Orden de trabajo PDF | Desde el detalle. | PDF correcto (no se genera PDF al crear, WMS-17). | P3 | FUN |
| F5-OC-021 | Salida con tiquete de ingreso (desde CE) | Detalle del depósito → historial de pesaje → «Salida con este tiquete» eligiendo una OC del mismo vehículo. | La OC queda anclada al tiquete; se despacha al cargar (DF18). | P2 | FUN |
| F5-OC-022 | Dos órdenes simultáneas | Dos usuarios (o dos pestañas) crean a la vez una orden por más de la mitad de lo nacionalizado disponible del mismo producto. Repetir con un levante que se reduce mientras se crea otra orden. | **Nuevo (BR-05-002, D5):** una responde 201 y la otra 400 «La cantidad solicitada de «…» … supera lo nacionalizado disponible (…)» (o stock insuficiente); la reserva final nunca supera lo disponible ni los levantes. Sin interbloqueos. | P0 | PER |
| F5-OC-023 | Cancelar o modificar con guía vigente | Con una orden `Pending` con guía vigente: «Cancelar orden» y «Modificar ítems» en CE; «Cancelar» en Bodega; luego anular la guía y repetir. | **Nuevo (BR-05-001, D6):** CE y Bodega muestran «Esta orden tiene la guía {n} vigente: para cancelarla o modificarla, anule primero la guía» (botones deshabilitados) y el API responde 409 «Anule primero la guía {n} de la orden {OC}…»; la cancelación **no** anula la guía sola. Anulada la guía, las tres acciones pasan. El detalle trae `activeDispatchGuideNumber`. | P0 | RN |

### 5.12 Guías de salida (GUI)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-GUI-001 | Pendientes | `/dispatch-guides/pending`. | OC de importación Pending/InProgress/Loaded sin guía vigente; «Generar guía». | P0 | FUN |
| F5-GUI-002 | Emitir guía IMP | Generar para la OC de F5-OC-001 **antes del cargue** (DEC-056): fecha de salida, ciudad con días de tránsito (vencimiento calculado), firmante, «Continuar al cobro» → destinatario cliente, inmediato. | Guía `2026S000nn`; factura GUIA_SALIDA (precio del convenio × N.º de depósitos); PDF. | P0 | FUN |
| F5-GUI-003 | Saldos congelados (WMS-19) | PDF de la guía. | Por línea: entrada (recibido), saldo anterior (= entrada − despachado en guías previas no anuladas), cantidad, nuevo saldo. Sin duplicar el saldo anterior. | P0 | RN |
| F5-GUI-004 | Saldos tras cambios posteriores | Hacer un CE-7 o un nuevo cargue y reabrir el PDF de la guía anterior. | Los saldos de la guía emitida no cambian. | P1 | RN |
| F5-GUI-005 | Segunda guía de la misma OC | Generar otra. | «Ya existe una guía de salida para esta orden de cargue.». | P1 | RN |
| F5-GUI-006 | Vencimiento | Ciudad sin días de tránsito; vencimiento anterior a la salida; fecha de salida > 24 h futura. | «Indique la fecha de vencimiento…», «La fecha de vencimiento debe ser posterior a la fecha de salida.», rechazo de > 24 h. Comparar el vencimiento calculado en UI y backend (R-CE-09) cerca de medianoche si es posible. | P2 | VAL |
| F5-GUI-007 | Guía antes del cargue | Emitir con la OC `Pending`. | Es el orden obligatorio en importación (DEC-056; Bodega no carga sin guía, F4-CAR-016): la guía usa lo pedido. Si el cargue difiere, ver F5-GUI-018. | P1 | RN |
| F5-GUI-008 | Estado de la OC no válido | OC Cancelled, Reverted o Dispatched. | «No se puede generar guía para una orden en estado '…'.». | P1 | RN |
| F5-GUI-009 | Sin precio | Cliente sin convenio GUIA_SALIDA y sin precio base (local). | «No se encontró precio para la guía de salida del cliente '…'…». | P2 | ERR |
| F5-GUI-010 | Total 0 | Destinatario único con total 0. | «El total a pagar debe ser mayor a cero.». | P2 | VAL |
| F5-GUI-011 | Cliente bloqueado | Guía de un cliente bloqueado. | Bloqueo por mora. | P1 | RN |
| F5-GUI-012 | ZIP por depósito | Descargar ZIP de una guía multi-depósito. | Un PDF por depósito `{Guía}-{n}`; se registra la impresión. | P2 | FUN |
| F5-GUI-013 | Anular guía | Anular con motivo 10–500. | Marca ANULADA; la factura se anula si estaba en borrador/pendiente sin pagos ni consolidación (si no, queda para Facturación); la OC vuelve a pendiente de guía; el número no se reutiliza. | P0 | RN |
| F5-GUI-014 | Cambiar modo de pago | «Cambiar modo de pago» en una guía IMP y en una EXP. | Anotar: solo aparece si no está facturada ni anulada; en IMP casi nunca (R-CE-10). | P3 | FUN |
| F5-GUI-015 | Guía de exportación automática | Tras F4-CAR-009. | Guía EXP creada, vence en los días de tránsito o 30; sin cargo. | P0 | INT |
| F5-GUI-016 | Consecutivo | Emitir dos guías (IMP y EXP). | Serie única `2026S…` sin saltos. | P1 | RN |
| F5-GUI-017 | Reimprimir etiqueta con saldo | Tras una guía parcial. | Etiqueta NACIONALIZADA con el saldo (F5-ETI-007). | P2 | INT |
| F5-GUI-018 | Guía antes de un cargue parcial | Emitir la guía de una orden `Pending` por 200 y que Bodega cargue 150. Anular la guía y emitirla de nuevo. | **Nuevo (DEC-052, BR-05-006, D7):** Comercio Exterior recibe el aviso «Guía con cantidades distintas a lo cargado» (`ActionRequired`: «…guía 200 · cargado 150. Anúlela y emítala de nuevo.») y el mensaje del cargue lo dice. El historial de guías y el detalle de la orden muestran «No coincide con lo cargado». No bloquea la salida. La guía nueva (150) no marca diferencia y cargar lo mismo no avisa. | P1 | RN |
| F5-GUI-019 | Cliente con salidas bloqueadas | Con el cliente de la orden marcado «sin salidas» (F1-TER-019): emitir la guía (incluso con otro destinatario) y, antes, probar la mora de un dueño con destinatario distinto. | **Nuevo (D9, D10, C3):** la guía responde 400 «…tiene las salidas bloqueadas…». Una guía de un solo dueño en mora con otro destinatario también se rechaza (se validan todos los dueños). La guía automática de exportación no se valida aparte (con el cargue bloqueado no se llega a ella). | P1 | RN |
| F5-GUI-020 | Guía con QR: escanear y verificar vigente | Con `GUIDE_CODE_TYPE = QR` (valor inicial): descargar el PDF de una guía, imprimirlo y escanear el QR con la cámara de un Android y de un iPhone. | **Nuevo (DEC-060, D35 a D42):** el QR, con la leyenda «Escanee para verificar esta guía», abre `/verificar/guia/{token}` sin iniciar sesión: franja verde «GUÍA VIGENTE», número, empresa, fechas, depósito(s), destino, productos y cantidades y la placa con 3 caracteres visibles. Nada de conductor, cliente, destinatario, documentos, teléfonos ni valores. La segunda copia y el PDF por depósito (ZIP) llevan el mismo QR. | P0 | FUN |
| F5-GUI-021 | Guía anulada: la verificación dice Anulada | Anular la guía de F5-GUI-020 y volver a escanear el mismo papel. | La página muestra la franja roja «GUÍA ANULADA el dd/MM/aaaa». | P0 | RN |
| F5-GUI-022 | Código alterado: la página dice que no es válido | Cambiar un carácter del token en la URL, o usar un token basura. | 404 con el mismo mensaje para todos los casos («La guía no existe o el código no es válido.») y la página «Esta guía no existe en el sistema o el código fue alterado.». No se distingue la causa. | P0 | SEG |
| F5-GUI-023 | `GUIDE_CODE_TYPE` = `BARCODE`: la guía sale con código de barras | Admin → Parámetros: poner `BARCODE`; reimprimir una guía (también las anteriores). Probar el valor `XYZ`. Devolver a `QR`. | Sale el código de barras de siempre, sin QR ni leyenda. `XYZ` responde 400 «El parámetro GUIDE_CODE_TYPE solo admite QR o BARCODE.». Cada edición queda auditada. Sin `DispatchGuides:VerificationKey` en modo QR, el PDF sale con código de barras y Admin recibe el aviso: nunca se bloquea la impresión (D38). | P1 | FUN |

### 5.13 Abandono (ABA), levantes (REL) y listas de empaque (PKL)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-ABA-001 | Listado | `/abandonment` (requiere un IMP con ≥ 20 días: usar fecha de ingreso corregida hacia atrás si la estadía lo permite, o datos migrados). | Filas con días, plazo, faltan (rojo si ≤ 10), estado EnPlazo/EnAlerta/EnAbandono. | P1 | RN |
| F5-ABA-002 | Cálculo del plazo | Comparar con la regla: 30 días sin prórroga; alerta desde 20; abandono > 30. | Coincide. | P1 | RN |
| F5-ABA-003 | Registrar prórroga | «Registrar prórroga» con notas. | Plazo 60; irreversible; segunda prórroga: 409 «…ya tiene prórroga registrada el … por …». | P1 | RN |
| F5-ABA-004 | Prórroga no permitida | En un EXP; en un IMP sin mercancía sin nacionalizar. | Mensajes de rechazo. | P2 | RN |
| F5-ABA-005 | Resumen | Aviso del tablero. | `{inAlert, abandoned}` coherente con la lista. | P2 | FUN |
| F5-ABA-006 | Alerta diaria | (Local) reiniciar el API antes de las 07:00 o esperar la corrida; revisar notificaciones de CE. | «Depósitos en ventana de abandono…». Riesgo R-ADM-01: puede no llegar a nadie. | P2 | INT |
| F5-REL-001 | Consulta de levantes | `/releases`: filtros levante/aceptación, depósito, importador, agencia, fechas. | Columnas FOB USD, tasa, FOB COP correctas (FOB COP = FOB USD × tasa); Excel. | P2 | FUN |
| F5-PKL-001 | Cargar lista de empaque | Cargar con proveedor e importador. | Artículos visibles; búsqueda por código o nombre. | P3 | FUN |
| F5-PKL-002 | Eliminar lista | Eliminar. | Se elimina. | P3 | FUN |

### 5.14 Integración (INT)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F5-INT-001 | Confirmar → Facturación | Tras F5-CNF-001, Facturación → pendientes de depósito y facturas de almacenamiento. | Depósito en «pendientes», período abierto, factura en Borrador con el detalle del depósito. | P0 | INT |
| F5-INT-002 | Camión tardío | Ver F3-MCA-009. | CE recibe aviso de reimprimir; la factura se recalcula. | P1 | INT |
| F5-INT-003 | Diferencia de recepción | Ver F4-REC-006. | Aviso en CE; CE-7 lo resuelve (F5-AJU-001). | P1 | INT |
| F5-INT-004 | Ciclo de salida completo | OC → báscula salida → cargue → guía → repesaje. | Estados: OC Pending → InProgress → Loaded → Dispatched; stock y saldos correctos en cada paso. | P0 | INT |
| F5-INT-005 | Cierre del depósito | Despachar todo el saldo. | Depósito `Closed`; en Closed solo se edita la planilla y se imprime. | P0 | INT |

## 6. Criterios de salida específicos

- P0 de CNF, LEV, OC, GUI e INT ejecutados; F5-CNF-001, F5-LEV-001, F5-OC-001, F5-GUI-002/003 en `PASA`.
- Riesgos verificados: R-CE-01 a R-CE-10, R-ADM-01 (vía avisos a CE).
- Depósitos confirmados, nacionalizados, con OC, guía, cerrado y anulado anotados en el registro de datos (los usa la fase 6).

## 7. Entregables

Informe de fase, defectos, registro de datos. Detenerse.
