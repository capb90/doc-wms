# Fase 4 — Bodega

> Lee antes `00-plan-maestro.md`. Rol principal: **Operario bodega** (`bodega`). Verificaciones con `c_exterior`, `facturacion`, `vigilancia` y Admin.

## 1. Objetivo

Validar la recepción de los camiones que vienen de báscula y de los que no pasan por ella, las unidades de carga, las ubicaciones por cantidad, el montacargas y su cobro, el inventario y sus movimientos, las novedades y la ejecución de las órdenes de cargue con su efecto en stock, períodos de facturación y cierre del depósito.

## 2. Alcance (funcionalidad real encontrada en el código)

| Pantalla | Ruta | Bloque |
|---|---|---|
| Tablero de Bodega | `/warehouse` | TAB |
| Ingresos pendientes desde báscula | `/warehouse/receptions/entry` | REC |
| Recepciones en progreso y recepción directa | `/warehouse/receptions` | REC, RSB, RUC |
| Historial y detalle de recepciones | `/warehouse/receptions/history`, `[id]` | REC |
| Montacargas e historial | `/warehouse/forklift`, `/history` | MON |
| Inventario (stock, movimientos, ubicaciones) | `/warehouse/inventory` | INV, UBI |
| Órdenes de cargue | `/warehouse/loading-orders`, `[id]` | CAR |
| Novedades | `/warehouse/novelties` | NOV |

**Reglas clave vigentes:**
- **La recepción con báscula no mueve stock** (WMS-9): guarda lo contado y, si difiere de lo declarado del camión, avisa a Comercio Exterior en la app. El stock viene de báscula.
- La **recepción sin báscula** sí crea stock con la cantidad declarada y abre el período de almacenamiento.
- El ajuste de inventario (CE-7) es de Comercio Exterior, no de Bodega.
- No hay paso «verificar orden» separado: se ejecuta el cargue con cantidades.

**Fuera:** creación de órdenes (fase 5), facturas (fase 6).

## 3. Criterios de entrada

1. Fase 3 aprobada. Depósitos de la fase 3 con entradas pendientes de recepción.
2. Ingreso abierto `QAB204` (Solo bodega) de la fase 2.
3. Cuadrilla, ubicaciones y tarifas de montacargas de la fase 1.
4. Para el bloque CAR: una orden de cargue `Pending` (ver «Preparación asistida»).

## 4. Preparación asistida

| Dato | Cómo | Rol |
|---|---|---|
| OC de importación `Pending` | CE confirma el depósito `QA-CP-0001` (F5-CNF-001), registra un levante de 100 (F5-LEV-001) y crea una OC de 80 `QA Cebolla` para `QAB205` (F5-OC-001). Si ya se hizo en la preparación de la fase 3, reutilizarla. | `c_exterior` |
| OC de exportación `Pending` | CE confirma el depósito EXP de la fase 3 y crea una OC por el total. | `c_exterior` |
| Cliente bloqueado | Ver fase 6, palancas de tiempo. Si no está disponible, F4-MON-010 y F4-RSB-006 quedan `BLOQUEADO`. | Admin |

## 5. Casos

### 5.1 Tablero (TAB)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-TAB-001 | Tarjetas | Abrir `/warehouse`. | Ingresos, Recepción, Historial, Montacargas, Historial montacargas, Órdenes, Inventario; cada una navega bien. | P1 | FUN |
| F4-TAB-002 | Menú | Revisar el menú de Bodega. | Incluye Novedades. | P3 | UX |

### 5.2 Recepción desde báscula (REC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-REC-001 | Pendientes desde báscula | `/receptions/entry`. | Una tarjeta por entrada de camión con primer peso (o completa si es de un pesaje): `QAA101`, `QAB201`, `QAA102`, `QAB203`… con depósito y productos declarados. | P0 | INT |
| F4-REC-002 | Registrar llegada | «Ingresar» en `QAA101`. | Recepción `InProgress`; desaparece de pendientes; aparece en `/receptions`. | P0 | FUN |
| F4-REC-003 | Doble llegada | «Ingresar» otra vez (o por API). | 409 «Ya existe una recepción en progreso para esta entrada de camión…». | P1 | RN |
| F4-REC-004 | Completar recepción igual a lo declarado | «Completar»: `QA Cebolla` 100, ubicación `A01-R01-N01`, cuadrilla, firma, 2 fotos. | Recepción `Completed`; sin aviso de diferencia. | P0 | FUN |
| F4-REC-005 | Stock no cambia | Inventario y detalle del depósito antes y después de F4-REC-004. | `CurrentStock` igual (WMS-9); el movimiento de recepción no altera el stock. | P0 | RN |
| F4-REC-006 | Diferencia con lo declarado | Completar `QAB201` contando 55 (declarado 60). | Recepción completa; CE recibe «Diferencia en recepción de Bodega … El stock no cambió; si corresponde, ajuste la cantidad (CE-7).» (R-ADM-01). Stock sin cambio. | P0 | INT |
| F4-REC-007 | Firma obligatoria | Completar sin firma. | «Debe capturar la firma del conductor». | P1 | VAL |
| F4-REC-008 | Cantidad 0 o negativa | Producto con 0 o −1. | Rechazado (> 0). Anotar si la UI omite los productos en 0. | P1 | VAL |
| F4-REC-009 | Fotos | 6 fotos; una de 6 MB; un PDF. | Máximo 5, ≤ 5 MB, jpg/png/webp: los demás rechazados con mensaje. | P2 | VAL |
| F4-REC-010 | Ubicación deshabilitada | Ubicar en la ubicación deshabilitada en F1-UBI-004. | «La ubicación … está deshabilitada.». | P2 | RN |
| F4-REC-011 | Ubicación parcial | Ubicar 60 de 100. | Quedan 40 por ubicar (visible en Ubicaciones). | P2 | RN |
| F4-REC-012 | Producto declarado no contado | En un depósito con 2 productos, contar solo uno. | Esperado: aviso de diferencia por el no contado. Riesgo R-BOD-05: no avisa. | P1 | RN |
| F4-REC-013 | Recepción completada repetida | Intentar otra recepción de la misma entrada. | 409 «Esta entrada de camión ya tiene una recepción completada.». | P2 | RN |
| F4-REC-014 | Detalle de la recepción (WMS-27, WMS-8) | Abrir `/receptions/[id]`. | Terceros (conductor con documento, importador, exportador si existe, cliente; faltantes «Sin asignar»), transporte (agencia, transportadora con NIT, unidades de carga), productos (declarado camión, unidad, embalaje, declarado depósito, contado, diferencia), fotos y firma. | P1 | FUN |
| F4-REC-015 | Historial y filtros | `/receptions/history`: estado, fechas, depósito, placa, número de depósito. | Filtros funcionan. | P2 | FUN |
| F4-REC-016 | Persistencia de fotos | Recargar el detalle. | Fotos visibles. (Si una recepción falla tras subir fotos, anotar fotos huérfanas, R-BOD-09.) | P2 | PER |
| F4-REC-017 | INSP y EXP | Recepcionar las entradas de `QAB203` (INSP) y `QAA102` (EXP). | Igual que IMP; la de un solo pesaje aparece al completarse. | P1 | FUN |
| F4-REC-018 | Depósito anulado o cerrado | Intentar registrar llegada de una entrada cuyo depósito se anuló. | «El depósito está cancelado.» / no aparece en pendientes. | P2 | RN |
| F4-REC-019 | Camión que ya salió | Registrar salida en Vigilancia de un camión con entrada pendiente; mirar pendientes. | Anotar: sigue en pendientes desde báscula (no filtra la salida) — R-VIG-03. | P2 | INT |

### 5.3 Recepción de unidades de carga — WMS-30 (RUC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-RUC-001 | Recepción de tanquero completo | Entrada de `QAB202` (tanquero `QAT001`) → Ingresar → Completar marcando «Recibida completa». | Esperado: recepción completa sin contar productos. Riesgo R-BOD-02: los validadores exigen productos y el handler los prohíbe → error. Si falla: CRITICAL (flujo de tanqueros bloqueado). | P0 | RN |
| F4-RUC-002 | Unidad sin confirmar | Completar sin marcar la unidad. | «Confirme que llegaron completas todas las unidades de carga del camión: QAT001.». | P1 | VAL |
| F4-RUC-003 | Contar productos en unidades | Enviar productos contados en un depósito de unidades. | «En un depósito de unidades de carga no se cuentan productos…». | P2 | RN |
| F4-RUC-004 | Estado de la unidad | Detalle de recepción y del depósito (CE). | La unidad figura recibida. | P2 | INT |

### 5.4 Recepción sin báscula — «Solo bodega» (RSB)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-RSB-001 | Pendiente directo | «Recepción directa». | `QAB204` en la lista. | P0 | INT |
| F4-RSB-002 | Crear depósito desde la recepción | Elegir `QAB204` → formulario manual: cliente `QA Cliente Uno`, modalidad IMP, documento `QA-CP-0010`, `QA Repuestos` declarado 20, contado 20, cuadrilla, firma → guardar. | Esperado: recepción completa, depósito nuevo en Borrador con stock 20 (movimiento IN) y período de almacenamiento abierto. Riesgo R-BOD-01: el contrato FE/BE está roto (probable 400). Si falla: CRITICAL. | P0 | FUN |
| F4-RSB-003 | Stock creado | Si F4-RSB-002 pasa: inventario. | Stock 20 = declarado. | P0 | RN |
| F4-RSB-004 | Factura de almacenamiento | Si F4-RSB-002 pasa: Facturación. | Período y factura abiertos (fase 6 valida importes). | P1 | INT |
| F4-RSB-005 | Firma | Sin firma. | «La firma del conductor es requerida.». | P2 | VAL |
| F4-RSB-006 | Cliente bloqueado | Cliente `QA Cliente Mora` bloqueado. | «El cliente '…' está bloqueado por deuda pendiente…». | P1 | RN |
| F4-RSB-007 | Ingreso duplicado | Tras F4-RSB-002, revisar Vigilancia → Salida/Historial. | Esperado: un solo ingreso abierto para `QAB204`. Riesgo R-BOD-04: se crea un segundo `EntryLog` y el original sigue en pendientes directos. | P1 | PER |
| F4-RSB-008 | Recepción directa con el selector | Con `bodega`: «Recepción directa» → elegir un camión «Solo bodega» (`QSL1nn`) → en «Conductor», escribir parte del nombre de un conductor existente y elegirlo → completar cliente, modalidad, documento `QA-SEL-CP-nnnn`, producto, cantidades, cuadrilla y firma → guardar. | La recepción se guarda; se crea un depósito en Borrador y la recepción (y el ingreso) muestran el conductor elegido. | P0 | FUN |
| F4-RSB-009 | «+» desde Bodega | Con `bodega`, en el formulario de F4-RSB-008: «+» → CC, documento nuevo (`900000000n`), nombres y apellidos `QA-SEL …` → «Registrar conductor». | Se crea el conductor (sin 403 en `POST /drivers`) y queda seleccionado (D9, D13). | P0 | ROL |
| F4-RSB-010 | Lápiz desde Bodega | Con `bodega` y un conductor `QA-SEL` seleccionado: lápiz → cambiar el teléfono → «Guardar cambios». | Guarda (sin 403 en `PATCH /drivers/{id}`); el cambio se ve en Admin → Conductores (D13). | P1 | ROL |
| F4-RSB-011 | Sin conductor | Completar el formulario sin conductor (o limpiar el select) → guardar. | No guarda; mensaje «Conductor requerido: selecciónelo o regístrelo con «+».» (D18). | P1 | VAL |

> Casos 008-011 agregados el 2026-10-08 por el selector de conductor (plan `docs/planes/plan-cerrado-selector-conductor-2026-10-08.md`).

### 5.5 Ubicaciones por cantidad (UBI)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-UBI-001 | Ubicar pendiente | Inventario → «Ubicaciones» de `QA Cebolla` → ubicar 40 en `B01-R01-N01`. | Asignado; pendiente por ubicar baja. | P1 | FUN |
| F4-UBI-002 | Ubicar más de lo pendiente | Ubicar 50 si quedan 40. | «No se puede ubicar 50: solo quedan 40 por ubicar.». | P1 | VAL |
| F4-UBI-003 | Mover | Mover 20 de `A01-R01-N01` a `B01-R01-N01`. | Cantidades actualizadas en ambas. | P1 | FUN |
| F4-UBI-004 | Mover a la misma | Origen = destino. | «La ubicación de destino debe ser distinta de la de origen.». | P2 | VAL |
| F4-UBI-005 | Liberar | Liberar 10. | Vuelven a pendiente por ubicar. | P2 | FUN |
| F4-UBI-006 | Producto no ubicado | Mover desde una ubicación donde no está. | «El producto no está ubicado en …». | P2 | VAL |
| F4-UBI-007 | Pestaña Ubicaciones | Inventario → pestaña Ubicaciones. | Muestra ocupación por ubicación coherente con lo anterior. | P2 | FUN |

### 5.6 Montacargas (MON)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-MON-001 | Iniciar uso | `/warehouse/forklift` → buscar placa `QAA101` → tipo Tractomula → horómetro inicial 100. | Uso activo asociado al servicio del camión. Puede iniciarse aunque el depósito no tenga cliente. | P0 | FUN |
| F4-MON-002 | Uso activo duplicado | Iniciar otro en el mismo servicio. | 409 «Ya existe un uso de montacargas activo…». | P1 | RN |
| F4-MON-003 | Finalizar y cobrar | Horómetro final 102 → modal de cobro: total precargado por tipo de vehículo (convenio de `QA Cliente Uno` si existe; si no, tarifa base), «Agregar IVA» desmarcado → Cobrar inmediato. | Factura MONTACARGAS pagada por el valor sin IVA. | P0 | FUN |
| F4-MON-004 | Horómetro final igual al inicial | Final = inicial. | Anotar: la UI exige mayor; el backend acepta igual (R-BOD-06). | P2 | VAL |
| F4-MON-005 | Horómetro final menor | Final < inicial. | «El horómetro final (x) no puede ser menor al inicial (y).». | P1 | VAL |
| F4-MON-006 | Horómetro inicial 0 | 0. | Anotar: la UI exige > 0; el backend acepta ≥ 0. | P3 | VAL |
| F4-MON-007 | Agregar IVA (WMS-28) | Otro uso: valor 100.000, marcar «Agregar IVA (19 %)». | Factura con subtotal 100.000 + IVA 19.000 = 119.000. Comparar el IVA mostrado en la UI y el de la factura (R-BOD-06: la UI redondea a entero, el backend a 2 decimales; probar con un valor que dé decimales, p. ej. 100.001). | P0 | RN |
| F4-MON-008 | Valor editable | Cambiar el total precargado a 80.000. | Factura por 80.000 (+ IVA si se marcó). Anotar si el «precio unitario» de la factura muestra la tarifa resuelta en vez del valor editado. | P1 | RN |
| F4-MON-009 | Por facturar | Cobro «Pendiente de facturar». | Factura sin pago; cambiar el modo luego desde el detalle (si no está facturado). | P1 | FUN |
| F4-MON-010 | Cliente bloqueado al finalizar | Destinatario `QA Cliente Mora` bloqueado. | Bloquea al finalizar con el mensaje de mora. Anotar que iniciar no valida la mora. | P1 | RN |
| F4-MON-011 | Sin tarifa del tipo | (Local) un tipo sin tarifa. | «No hay tarifa de montacargas configurada para el tipo de vehículo '…'…». | P2 | ERR |
| F4-MON-012 | Camión sin servicio | Intentar iniciar con `QAB204` (Solo bodega antes de recepción). | Anotar: necesita un servicio; documentar el mensaje (R-BOD-06). | P2 | RN |
| F4-MON-013 | Cambiar modo ya facturado | Cambiar el modo de un uso cuya factura ya está procesada. | «No se puede cambiar el modo de pago de un uso de montacargas ya facturado.». | P2 | RN |
| F4-MON-014 | Historial | `/forklift/history`. | Usos con horómetros, tipo, valor, IVA, modo, factura. | P2 | FUN |
| F4-MON-015 | GuacalEstiba | Iniciar con tipo GuacalEstiba. | Tarifa de GuacalEstiba (R-FAC-12). | P3 | RN |

### 5.7 Inventario (INV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-INV-001 | Consultar stock | Pestaña «Consultar Stock». | Por producto y depósito: actual, reservado, disponible = actual − reservado ≥ 0. | P0 | RN |
| F4-INV-002 | Movimientos | Pestaña «Movimientos». | `DeclaredEntry` de báscula, IN de recepción sin báscula, OUT de cargues, con usuario y fecha. | P1 | FUN |
| F4-INV-003 | Exportar Excel | Exportar movimientos. | Todas las filas del filtro (no solo la página). | P2 | FUN |
| F4-INV-004 | Reservado tras crear OC | Tras la preparación de la OC. | Reservado = cantidad de la OC; disponible baja. | P0 | INT |
| F4-INV-005 | Ajuste no disponible a Bodega | Buscar ajuste de cantidad. | No existe para Bodega (es CE-7). Por API `POST warehouse/inventory/adjustments` con `bodega` → 403. | P2 | ROL |

### 5.8 Novedades (NOV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-NOV-001 | Crear novedad | Nueva → depósito → producto → tipo Ingreso, camión (de las recepciones del depósito), cantidades total/buena/dañada/faltante, descripción. | Se crea; si dañada/faltante/sobrante > 0, CE recibe aviso. | P1 | FUN |
| F4-NOV-002 | Editar | Cambiar cantidades. | Se guarda; aviso a CE si cambian y quedan > 0. | P2 | FUN |
| F4-NOV-003 | Imprimir PDF | Imprimir. | PDF con los datos. | P2 | FUN |
| F4-NOV-004 | Anular | Motivo de 9 caracteres; de 10. | 9 rechazado; 10 anula; reanular: «La novedad ya está anulada.». | P2 | RN |
| F4-NOV-005 | Validaciones | Fin antes que inicio; cantidad negativa; descripción vacía o > 4000. | Rechazados. | P2 | VAL |
| F4-NOV-006 | Cuadre de cantidades | Total 100, buena 90, dañada 20. | Esperado: advertencia o rechazo. Riesgo R-BOD-07: no se valida. | P2 | RN |
| F4-NOV-007 | Camión de otro depósito | Elegir un camión que no es del depósito (por API). | «El camión no pertenece al depósito del producto.». | P3 | RN |
| F4-NOV-008 | Depósito anulado | Novedad en un depósito anulado. | 409 «El depósito … está anulado.». | P3 | RN |
| F4-NOV-009 | Exportar | Exportar Excel. | Archivo correcto. | P3 | FUN |

### 5.9 Ejecución de órdenes de cargue (CAR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F4-CAR-001 | Ejecutar cargue completo | `/warehouse/loading-orders` → OC de la preparación → ejecutar: cantidad 80, sello, cuadrilla, firma, fotos. | OC `Loaded` (o `Dispatched` si el ciclo de salida ya cerró); stock `QA Cebolla` −80 con movimiento OUT; reserva liberada; resultado por ítem con posiciones liberadas (LIFO). | P0 | FUN |
| F4-CAR-002 | Aviso de guía (IMP) | Tras F4-CAR-001, notificaciones de CE. | «Guía de salida requerida» (R-ADM-01); Admin recibe «Cargue completado» por correo. | P1 | INT |
| F4-CAR-003 | Cargue parcial | Otra OC de 30: cargar 20. | 20 descontados; los 10 restantes liberados y disponibles otra vez; OC `Loaded`. | P0 | RN |
| F4-CAR-004 | Cargar más de lo pedido | 31 de 30. | «La cantidad a cargar (31) excede la cantidad solicitada (30)…». | P1 | VAL |
| F4-CAR-005 | Cargar 0 | Todo en 0. | «No se cargó mercancía: cancele la orden en lugar de ejecutarla.». | P1 | VAL |
| F4-CAR-006 | Disponible insuficiente | Si el disponible es menor que lo pedido. | La UI bloquea. | P2 | VAL |
| F4-CAR-007 | Orden cancelada o ya cargada | Ejecutar una OC cancelada o cargada. | «No se puede ejecutar una orden cancelada.» / «La orden ya fue cargada.». | P1 | RN |
| F4-CAR-008 | Despacho tras repesaje previo | Ciclo de salida cerrado antes del cargue (F3-SAL-007) → ejecutar. | OC pasa directo a `Dispatched`. | P1 | INT |
| F4-CAR-009 | Exportación | Ejecutar la OC de exportación. | Guía de exportación automática (ver en CE) y sin cargo; depósito cerrado si el stock queda en 0. | P0 | INT |
| F4-CAR-010 | Firma | Ejecutar sin firma. | La UI la exige. Anotar que el backend la acepta opcional y que `CompletedBy` lo envía el cliente (R-BOD-08). | P2 | VAL |
| F4-CAR-011 | Cierre del depósito con stock 0 | Cargar todo el saldo de un depósito. | Depósito `Closed`; períodos de almacenamiento agotados cerrados (fase 6 valida importes). | P0 | INT |
| F4-CAR-012 | Cancelar orden desde Bodega | OC `Pending` → «Cancelar orden» con motivo 10–500. | OC `Cancelled`; reservas liberadas. Motivo corto rechazado. | P1 | FUN |
| F4-CAR-013 | Orden de trabajo PDF | Imprimir la orden de trabajo. | PDF con ítems, depósitos, vehículo, cuadrilla. | P2 | FUN |
| F4-CAR-014 | Depósito devuelto a Borrador | CE devuelve a Borrador el depósito de una OC `Pending` (F5-COR-005) → Bodega ejecuta. | Esperado: bloqueo. Riesgo R-CE-05: el cargue se ejecuta sobre un depósito en Borrador. | P1 | RN |
| F4-CAR-015 | Item repetido o ajeno | Por API: ítem duplicado; ítem de otra orden. | «El item … está repetido en el cargue.» / «Los siguientes items no pertenecen a la orden…». | P3 | API |

## 6. Criterios de salida específicos

- P0 de REC, RSB, RUC, MON, INV y CAR ejecutados.
- Si F4-RSB-002 o F4-RUC-001 fallan (riesgos ★), se registran como CRITICAL y el usuario decide si seguir.
- Riesgos verificados: R-BOD-01 a 09; R-CE-05 (F4-CAR-014).
- Registro de datos con recepciones, usos de montacargas y órdenes ejecutadas.

## 7. Entregables

Informe de fase, defectos, registro de datos. Detenerse.
