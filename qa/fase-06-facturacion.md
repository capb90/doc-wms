# Fase 6 — Facturación

> Lee antes `00-plan-maestro.md`. Rol principal: **Facturación** (`facturacion`). Verificaciones con Admin, `c_exterior`, `bascula` y `bodega`.
> **Dinero = severidad CRITICAL por defecto.** Todo importe se verifica con cálculo manual (hoja de cálculo) y se anota la fórmula usada.

## 1. Objetivo

Validar que cada cargo nace donde debe y por el valor correcto (BASCULA, MONTACARGAS, GUIA_SALIDA, ALMACENAMIENTO); la resolución de tarifas (convenio → tarifa base → precio base → mínimo) y cada fórmula; impuestos, subtotales, totales y redondeos; el ciclo de vida de la factura y sus acciones por estado; el N.º SIIGO; los overrides; la TRM manual; el recálculo; los pagos; la cartera y el bloqueo por mora; los jobs, y la refacturación.

## 2. Alcance

| Pantalla | Ruta | Bloques |
|---|---|---|
| Dashboard | `/billing` | DSH |
| Facturas (pestañas Báscula, Montacargas, Guía de salida, Almacenamiento) | `/billing/invoices` | INV, ACC |
| Detalle de factura | `/billing/invoices/[id]` | INV, OVR, ACC, TRM |
| Pagos | `/billing/payments` | PAG |
| Depósitos pendientes | `/billing/pending-deposits` | ALM, REF |
| Configuración por cliente | `/billing/configurations` | CFG |
| Reportes anual y por CPI | `/billing/reports/*` | (fase 7) |
| Tarifas y convenios (Admin) | `/admin/services`, `/admin/stakeholders/[id]` | TAR, FOR, PRE |

**No existe creación manual de facturas en la UI** (el sistema las genera). `billing/invoices/create` es una pantalla congelada: solo se verifica que no esté expuesta (F6-INV-020).

## 3. Criterios de entrada

1. Fases 3, 4 y 5 aprobadas.
2. Facturas existentes: BASCULA inmediata y por facturar (fase 3), MONTACARGAS con y sin IVA (fase 4), GUIA_SALIDA (fase 5), ALMACENAMIENTO de depósitos confirmados IMP (USD), EXP, INSP (fase 5).
3. Hoja de cálculo preparada con los valores del convenio y tarifas del registro de datos.
4. Para los bloques CAR, JOB y renovación de ALM: **ambiente local** y autorización del usuario para las palancas de tiempo.

## 4. Palancas de tiempo (solo local, con autorización explícita del usuario)

Los jobs no tienen endpoint manual ni reloj inyectable. Corren al arrancar la API (Overdue +30 s, conciliación +45 s, períodos +30 s, avisos de vencimiento +1 min) y luego cada 24 h (períodos: dinámico, mínimo 5 min). Opciones, de menos a más invasiva:

1. **Cerrar y renovar períodos sin esperar:** `POST billing/storage-periods/close` con `{warehouseStorageId, closedById}` (Billing/Admin). Cierra los períodos abiertos del depósito y abre el siguiente.
2. **Mover fechas en la base** y reiniciar la API para que los jobs corran. Ejemplos ilustrativos (verificar nombres de columnas antes; ejecutar solo sobre datos `QA`):
   ```sql
   -- Factura vencida (para Overdue y mora)
   UPDATE invoices SET due_date = now() - interval '2 days' WHERE id = '<id factura QA>';
   -- Período vencido (para renovación automática)
   UPDATE storage_billing_periods SET limit_date = (now() - interval '1 day')::date WHERE warehouse_storage_id = '<id depósito QA>' AND status = 'Open';
   ```
3. Cambiar el reloj del servidor (no recomendado).

> Por el riesgo R-FAC-02, una factura sin pagos puede necesitar **dos** reinicios para pasar a Overdue (primero la conciliación pone `AmountPaid = 0`). Documentar cuántos hicieron falta.

Anota en el informe cada palanca usada (SQL exacto, hora, reinicios).

## 5. Reglas que se verifican (resumen del código)

- **Resolución:** 1) convenio activo del cliente (escalera de especificidad producto+modalidad → … → genérico; desempate por más reciente; perecedero exacto antes que genérico); 2) `ServicePricingRule`; 3) `ServicePrice` vigente; 4) sin tarifa: error, salvo almacenamiento, que cae al mínimo de la modalidad o a $0 con advertencia y notificación.
- **Cálculo:** cantidad facturable según la base de la fórmula → bruto → unitario (si IVA incluido y la fórmula lo admite, ÷ 1,19) → unitario redondeado a 2 decimales (AwayFromZero) → neto e IVA. Solo suman impuestos `Added` asociados al servicio (`ServiceTax`). RETE_FUENTE no suma.
- **Fórmulas vigentes:** `FIXED`, `PER_UOM`, `PERCENTAGE_OF_VALUE` (CIF en pesos, mínimo IVA incluido, umbral), `PERCENTAGE_OF_VALUE_PRORATED` (CIF × stock/recibido), `PER_VEHICLE`, `PER_VEHICLE_TYPE` (prohibida en almacenamiento), `PER_CARGO_UNIT`, `WEIGHT_THRESHOLD`, `BASE_PRICE`. Piso por unidad de carga `minimumPerCargoUnit`.
- **Almacenamiento:** período desde el día de ingreso (Colombia); fin = inicio + N días (inclusivo: semanal cubre 8 días, quincenal 14 cubre 15); límite = fin + 3. Una factura por depósito (o consolidada). Magnitudes del depósito (CIF, vehículos, contenedores, unidades) se cobran una sola vez. Factura siempre se genera.
- **Factura:** `Draft → (PendingApproval) → Approved → Sent → PartiallyPaid/Paid`; `Overdue` por job; `Cancelled` con motivo ≥ 10. N.º SIIGO único, ≤ 50, solo en Draft/PendingApproval, no en facturas $0, no con TRM pendiente. Aprobar exige número (salvo $0) y TRM. Detalle editable solo en Draft (≤ 1000). Notas salvo en anuladas.
- **Pagos:** monto > 0 y ≤ saldo; métodos Efectivo, Transferencia, Cheque, TC, TD, Otro; nacen Received → Verified.
- **Mora:** deuda vencida > límite de crédito → `Blocked`; si no → `OverdueWarning`; sin límite nunca bloquea; límite 0 bloquea con cualquier mora.

## 6. Casos

### 6.1 Dashboard (DSH)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-DSH-001 | KPIs | Abrir `/billing`. | Facturado del mes, cartera pendiente, vencidas, borradores, total del mes; enlaces correctos. | P1 | FUN |
| F6-DSH-002 | Coherencia | Comparar los KPIs con el listado filtrado. | Coinciden (anotar que la cartera incluye pendientes de borradores). | P1 | RN |
| F6-DSH-003 | Borde de mes | (Si se ejecuta el último día del mes después de las 19:00 hora Colombia, o con una factura creada a esa hora.) | Esperado: mes de Colombia. Riesgo R-FAC-11: usa UTC. | P3 | RN |

### 6.2 Listado y detalle de facturas (INV)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-INV-001 | Pestañas por servicio | Recorrer Báscula, Montacargas, Guía de salida, Almacenamiento. | Cada factura en su pestaña; paginación independiente. Una consolidada con varios servicios aparece en varias pestañas. | P0 | FUN |
| F6-INV-002 | Columnas WMS-21 | Revisar columnas. | N.º («Pendiente de número» si falta, salvo $0), Identificación (tipo + número), Destinatario (nombre; «Consumidor Final»; «Pendiente de asignar»; etiqueta «No registrado» para el conductor), Estado, Total, Pendiente (rojo si > 0), Vencimiento, Creada. | P0 | FUN |
| F6-INV-003 | Filtros | Estado, N.º (parcial), destinatario por nombre o identificación, día de creación. | Filtran correctamente; día en hora Colombia. | P1 | FUN |
| F6-INV-004 | Exportar Excel | Exportar una pestaña filtrada. | Todas las filas del filtro. | P2 | FUN |
| F6-INV-005 | Detalle | Abrir una factura de almacenamiento. | Líneas con etiqueta de origen (Acuerdo nivel 1 / Tarifa base nivel 2 / Precio base nivel 3 / Valor mínimo), depósitos con TRM, historial, pagos, PDF. | P0 | FUN |
| F6-INV-006 | PDF de la factura | Descargar PDF. | Datos del destinatario, líneas, subtotal, IVA, total y detalle del depósito iguales a la pantalla. | P1 | FUN |
| F6-INV-007 | Factura BASCULA inmediata | Revisar la de F3-COB-001. | `Paid`, total = el cobrado, desglose subtotal + IVA según `ServiceTax` de BASCULA (sin ServiceTax, IVA 0). | P0 | RN |
| F6-INV-008 | Factura BASCULA por facturar | Revisar la de F3-COB-007. | Sin pago, sin número, `Draft` (o el estado inicial que muestre), destinatario el cliente. | P0 | RN |
| F6-INV-009 | Factura MONTACARGAS | Revisar las de F4-MON-003 y 007. | Sin IVA: total = valor; con IVA: valor + 19 %; redondeo a 2 decimales. Anotar la descripción «Servicio de montacargas — {tipo}». | P0 | RN |
| F6-INV-010 | Factura GUIA_SALIDA | Revisar la de F5-GUI-002. | Precio del convenio × número de depósitos; enlazada a la guía. | P0 | RN |
| F6-INV-011 | Factura en $0 | Depósito adicional en cero (si F3-MUL funcionó) o almacenamiento sin tarifa con mínimo 0. | Total 0; no lleva número fiscal; no aparece «Pendiente de número». | P1 | RN |
| F6-INV-020 | Pantalla de creación congelada | Abrir `/billing/invoices/create` por URL; `POST billing/invoices` por API. | Esperado: sin acceso desde la UI (sin menú). Anotar si la página carga y si el endpoint crea facturas (R-FAC-13). | P2 | SEG |
| F6-INV-021 | Cambiar el destinatario (BR-06-007) | Factura de almacenamiento en Borrador de un IMP con agencia y transportadora: «Cambiar destinatario» junto a «Destinatario» → elegir la agencia → Guardar. Por API, `PATCH …/recipient` con un tercero ajeno al depósito y sin rol Cliente, y con la factura aprobada. | **Nuevo (`DEC-057`, D21–D23):** el botón solo aparece en Borrador; el diálogo lista «Terceros de los depósitos de la factura» con sus roles (cliente e importador, agencia, transportadora) y debajo «O busque otro cliente». Al guardar, la factura queda a nombre de la agencia sin recargar la página (204). Tercero ajeno: 400 «El tercero no está relacionado con la factura ni es cliente.»; factura aprobada: 400 como antes. | P1 | FUN |

### 6.3 Acciones por estado — WMS-20 (ACC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-ACC-001 | Diálogo de acciones | «Acciones» en una factura Draft. | Muestra solo las acciones válidas: asignar N.º, aprobar (deshabilitado sin N.º), editar detalle, notas, anular. | P0 | FUN |
| F6-ACC-002 | Asignar N.º SIIGO | Asignar `QA-SIIGO-0001`. | Se guarda; aparece en el listado. | P0 | FUN |
| F6-ACC-003 | N.º duplicado | Asignar el mismo número a otra factura. | 409 «Ya existe una factura con el número 'QA-SIIGO-0001'.». | P0 | RN |
| F6-ACC-004 | N.º vacío o largo | Vacío; 51 caracteres. | «El número de factura no puede estar vacío.»; > 50 rechazado. | P2 | VAL |
| F6-ACC-005 | N.º en factura $0 | Intentar asignar. | «Una factura en cero no requiere número fiscal.». | P2 | RN |
| F6-ACC-006 | Aprobar sin N.º | Aprobar una Draft sin número. | «Asigne el número de factura (SIIGO) antes de aprobar la factura.». | P0 | RN |
| F6-ACC-007 | Aprobar | Aprobar la de F6-ACC-002. | `Approved`; el N.º queda fijo (cambiarlo: «Solo se puede asignar o cambiar el número de factura en estado Borrador o Pendiente de aprobación.»). | P0 | RN |
| F6-ACC-008 | Editar detalle | En Draft, editar detalle (≤ 1000); en Approved intentar. | Draft: se guarda; 1001 caracteres rechazado; Approved: «Solo se puede actualizar el detalle de una factura en estado Draft.». | P1 | RN |
| F6-ACC-009 | Notas | Agregar notas en Approved; en Cancelled. | Approved: se guardan; Cancelled: «No se pueden editar las notas de una factura anulada.». | P2 | RN |
| F6-ACC-010 | Enviar | Enviar una Approved; enviar una Draft (por API). | Approved → `Sent`; Draft: «Solo se pueden enviar facturas aprobadas.». | P1 | RN |
| F6-ACC-011 | Anular | Anular una Draft con motivo de 10. | `Cancelled`; motivo visible en historial. | P0 | FUN |
| F6-ACC-012 | Motivo corto | Motivo de 9 (con espacios alrededor). | «El motivo de anulación debe tener al menos 10 caracteres.» (con trim). | P1 | VAL |
| F6-ACC-013 | Anular pagada | Anular una `Paid`. | «No se puede cancelar una factura pagada.». | P0 | RN |
| F6-ACC-014 | Anular dos veces | Anular una ya anulada. | «La factura ya está anulada.». | P2 | RN |
| F6-ACC-015 | Anular almacenamiento | Anular una factura de almacenamiento Draft. | Notificación «quedaron por refacturar»; aparece la opción Refacturar. | P1 | INT |
| F6-ACC-016 | Acciones con TRM pendiente | Factura de depósito USD con TRM pendiente. | Asignar N.º y aprobar deshabilitados; mensaje «Registre la TRM del depósito … antes de…». | P0 | RN |
| F6-ACC-017 | Factura inmediata pagada sin número | Asignar N.º SIIGO a una BASCULA inmediata (ya `Paid`). | Anotar: según el código no es posible (MAF-12). Confirmar con el usuario si Facturación necesita numerarla. | P1 | RN |
| F6-ACC-018 | Anular con pagos parciales | Factura `PartiallyPaid` → anular. | Anotar: el sistema lo permite y los pagos quedan en la anulada (R-FAC-16). Esperado de negocio: bloquear o exigir devolución. | P1 | RN |
| F6-ACC-019 | Estado PendingApproval | Buscar cómo llega una factura a «Pendiente de aprobación». | Anotar: el código no tiene ruta a ese estado. | P3 | RN |

### 6.4 Overrides de línea (OVR)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-OVR-001 | Override disponible solo en Draft | Ver el botón en Draft y en Approved. | Solo en Draft; una vez por línea. | P1 | RN |
| F6-OVR-002 | Override en línea de cantidad 1 | Línea con cantidad 1, valor 100.000 + IVA → sobrescribir a 95.000 con justificación. | Esperado: la línea queda en el valor indicado (definir con el usuario si es neto o con IVA). Anotar el total resultante. | P0 | RN |
| F6-OVR-003 | Override en línea con cantidad > 1 | Línea con cantidad 10 (p. ej. PER_UOM) → sobrescribir a 95.000. | Esperado: total de la línea 95.000 (o 95.000 + IVA). Riesgo R-FAC-01: queda en 95.000 × 10 × 1,19 = 1.130.500. Si se confirma: CRITICAL. | P0 | RN |
| F6-OVR-004 | Registro del override | Revisar el valor «original» guardado. | Anotar: el código guarda `UnitPrice × Quantity` sin IVA, mientras la UI envía el total con IVA. | P2 | PER |
| F6-OVR-005 | Validaciones | Monto 0; justificación vacía; justificación de 501. | Rechazados. | P2 | VAL |
| F6-OVR-006 | Segundo override | Sobrescribir la misma línea otra vez. | «Esta línea ya fue sobrescrita.». | P2 | RN |
| F6-OVR-007 | Override descartado por recálculo | Tras un override en almacenamiento, provocar un recálculo (CE-7). | La línea se reemplaza y la notificación lista el valor descartado. | P1 | INT |

### 6.5 Tarifas y resolución (TAR)

Para cada caso, calcular el esperado en la hoja de cálculo y comparar con la línea de la factura generada.

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-TAR-001 | Nivel 1: convenio | Factura de almacenamiento de `QA Cliente Uno` (convenio `PERCENTAGE_OF_VALUE`). | Etiqueta «Acuerdo nivel 1»; valor = % del CIF en pesos (CIF × TRM si USD), aplicando mínimo y umbral. | P0 | RN |
| F6-TAR-002 | Nivel 2: tarifa base | Depósito de un cliente sin convenio (`QA Multirol`) en IMP con `QA Cebolla` (regla `PER_UOM`). | «Tarifa base nivel 2»; valor = rate × cantidad. | P0 | RN |
| F6-TAR-003 | Nivel 3: precio base | BASCULA de un cliente sin convenio. | Valor = `ServicePrice` vigente. | P0 | RN |
| F6-TAR-004 | Nivel 4: mínimo | Depósito de almacenamiento sin convenio ni regla aplicable (p. ej. INSP sin regla). | Línea «Valor mínimo» = `ServiceMinimumValue` de la modalidad (o $0) con advertencia en el detalle y notificación a Facturación. | P0 | RN |
| F6-TAR-005 | Convenio inactivo | Desactivar el servicio del convenio y generar un cargo nuevo (montacargas). | Cae al nivel siguiente. Reactivar después. | P1 | RN |
| F6-TAR-006 | Escalera: producto + modalidad | Convenio con una regla genérica y otra específica (producto + modalidad). | Gana la específica. | P1 | RN |
| F6-TAR-007 | Escalera: otra modalidad | Convenio con regla solo para EXP; depósito IMP del mismo cliente. | Esperado: no aplica la de EXP. Riesgo R-FAC-15 (MAF-02): puede aplicar la de otra modalidad. | P1 | RN |
| F6-TAR-008 | Porcentaje fuera de rango | Con el convenio de F1-CNV-006 (si se guardó con 150 %). | Anotar: cae al mínimo al facturar (MAF-07). | P2 | RN |
| F6-TAR-009 | Perecedero (WMS-32) | Regla con perecedero = sí y otra genérica; depósito de `QA Cebolla` perecedera. | Aplica la de perecedero; un producto no perecedero usa la genérica; una regla con el valor contrario nunca aplica. | P2 | RN |
| F6-TAR-010 | Desempate por fecha | Dos reglas del mismo peldaño. | Gana la más reciente. | P3 | RN |

### 6.6 Fórmulas (FOR)

| ID | Fórmula | Escenario | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-FOR-001 | `FIXED` | Valor fijo en BASCULA o GUIA_SALIDA. | Total = rate (+ IVA si hay ServiceTax). | P0 | RN |
| F6-FOR-002 | `FIXED` IVA incluido | Tarifa cotizada «IVA incluido». | Unitario = rate ÷ 1,19 redondeado a 2 decimales; total ≈ rate (anotar diferencia de centavos). | P1 | RN |
| F6-FOR-003 | `PER_UOM` | Almacenamiento IMP 160 bultos × rate. | Cantidad = stock; `uom` coincide con la unidad. Si no coincide, el grupo cae al mínimo (verificar con un producto de otra unidad). | P0 | RN |
| F6-FOR-004 | `PERCENTAGE_OF_VALUE` | CIF USD 50.000 × TRM × 0,255 %. | No se multiplica por el stock. Con CIF bajo el umbral aplica el mínimo (IVA incluido → neto); con CIF ≥ umbral no aplica. | P0 | RN |
| F6-FOR-005 | `PERCENTAGE_OF_VALUE` renovación | Segundo período. | Cobra el CIF completo otra vez. | P1 | RN |
| F6-FOR-006 | `PERCENTAGE_OF_VALUE_PRORATED` | Tras despachar la mitad, renovación. | CIF × (stock / recibido); el mínimo no se prorratea. | P1 | RN |
| F6-FOR-007 | `PER_VEHICLE` | Depósito con 2 camiones. | rate × 2 (vehículos distintos). | P1 | RN |
| F6-FOR-008 | `PER_CARGO_UNIT` | Depósito `QA-CP-0005` con 1 tanquero. | rate × unidades no despachadas del tipo. | P1 | RN |
| F6-FOR-009 | `WEIGHT_THRESHOLD` | Peso de manifiesto bajo y sobre el umbral. | Bajo: mínimo (IVA incluido); sobre: ratePerKg × peso. Peso = suma del manifiesto de camiones no anulados. | P2 | RN |
| F6-FOR-010 | `BASE_PRICE` | Servicio sin regla con precio base. | precio × cantidad; nunca aplica mínimos. | P2 | RN |
| F6-FOR-011 | `PER_VEHICLE_TYPE` en montacargas | Convenio de montacargas con tarifas por tipo. | Tarifa del tipo de vehículo del uso. | P1 | RN |
| F6-FOR-012 | Nombre Guacal | Comparar «Guacal» (PER_VEHICLE) y «GuacalEstiba» (PER_VEHICLE_TYPE/montacargas). | Anotar la inconsistencia (R-FAC-12); verificar que un uso GuacalEstiba no falle por nombre. | P3 | RN |
| F6-FOR-013 | Piso por unidad de carga | `minimumPerCargoUnit` en un depósito con 2 contenedores. | Piso = mínimo × 2 (IVA incluido); línea «(mínimo aplicado)». | P2 | RN |
| F6-FOR-014 | Magnitud cobrada dos veces | Dos grupos de productos con reglas `PER_VEHICLE` en el mismo depósito. | Los grupos con base de depósito caen al respaldo (un solo cargo de respaldo). | P2 | RN |

### 6.7 Previsualización (PRE)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-PRE-001 | `formula-preview` vs real (IVA incluido) | Previsualizar una `FIXED` IVA incluido y comparar con la factura real. | Esperado: iguales. Riesgo R-FAC-09: no aplica IVA incluido. | P2 | RN |
| F6-PRE-002 | Prorrateada | Previsualizar `PERCENTAGE_OF_VALUE_PRORATED`. | Riesgo R-FAC-09: siempre 100 %. | P3 | RN |
| F6-PRE-003 | PER_VEHICLE_TYPE / PER_CARGO_UNIT | Previsualizar. | Riesgo R-FAC-09: falla o da 0. | P3 | RN |
| F6-PRE-004 | `billing/preview` en báscula | Comparar el total precargado del cobro con la factura generada para un producto perecedero o con `WEIGHT_THRESHOLD`. | Anotar diferencias (no pasa perecedero ni peso). | P2 | RN |

### 6.8 Almacenamiento: períodos, factura y renovación (ALM)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-ALM-001 | Apertura al confirmar | Tras F5-CNF-001: pendientes de depósito → resumen. | Un período `Open` por cargo, inicio = día de ingreso (Colombia), fin según el ciclo del cliente (Mensual: mes calendario), límite = fin + 3; factura Draft con una línea por cargo y `Detail` del depósito. | P0 | RN |
| F6-ALM-002 | Primer período cobra el total | Comparar la cantidad facturada con el stock al confirmar. | Total del depósito (cantidad declarada + ajustes). | P0 | RN |
| F6-ALM-003 | Sin configuración del cliente | Depósito de un cliente sin configuración. | Ciclo mensual, preferencia PerService, 30 días de plazo. | P1 | RN |
| F6-ALM-004 | Ciclo quincenal y semanal | Cliente con Biweekly (14) y otro con Weekly (7). | Fin = inicio + 14 / + 7 (inclusivo: cubren 15 y 8 días). Anotar para la decisión abierta (15 días en el levantamiento). | P1 | RN |
| F6-ALM-005 | Ciclos legacy | Days15, Days30, Days90, Days180, Days360 en la configuración. | Duración correcta. | P2 | RN |
| F6-ALM-006 | OnDemand | Cliente OnDemand confirma un depósito. | No se abre período (MAF-15). Anotar si queda sin factura. | P2 | RN |
| F6-ALM-007 | Consolidated | Cliente `QA Cliente Consolidado` con 2 depósitos confirmados en la misma ventana. | Una factura Draft consolidada con líneas de ambos; vence al fin de la ventana + plazo. Si la consolidada ya fue aprobada, se crea otra. | P1 | RN |
| F6-ALM-008 | Renovación manual | `POST billing/storage-periods/close` sobre un depósito con stock. | Cierra el período; abre el siguiente con inicio = fin + 1; nueva factura (o línea en la consolidada); notificación. | P0 | RN |
| F6-ALM-009 | Renovación cobra el saldo | Tras despachar parte del stock, renovar. | **Actualizado (DEC-053, BR-06-005, D19):** la renovación, por el job o por el cierre manual, cobra la cantidad facturable **al cierre del día de inicio del período** (fin + 1), aunque el job corra después: lo que sale ese día no se cobra y lo despachado en los días de gracia sí. Las fórmulas por cantidad y `PER_CARGO_UNIT` cobran ese saldo; `PERCENTAGE_OF_VALUE` el CIF completo. | P0 | RN |
| F6-ALM-010 | Mínimo de modalidad con IVA | Factura caída al mínimo de IMP ($184.000). | Anotar si el total es 184.000 o 184.000 × 1,19 (el código trata el mínimo de modalidad como neto y el de fórmula como IVA incluido; decisión abierta WMS-32, R-FAC-14). | P1 | RN |
| F6-ALM-011 | Sin stock no factura | Depósito con stock 0 al renovar. | Período cerrado sin factura nueva. | P1 | RN |
| F6-ALM-012 | Cierre por agotamiento | Tras el cargue total (F4-CAR-011). | Períodos de productos agotados cerrados; el importe cobrado por adelantado se conserva. | P0 | RN |
| F6-ALM-013 | Reapertura por reversa | Revertir la salida (F5-OC-017). | Período reabierto o abierto. | P1 | RN |
| F6-ALM-014 | Servicio complementario sin tarifa | Activar el servicio complementario sin tarifa de F1-CNV-011 y confirmar un depósito del cliente. | **Actualizado (DEC-020, BR-06-004, D17):** la confirmación responde 200 y la factura se genera; la línea del complementario sale en $0 (o con el mínimo **de ese servicio** en la modalidad) con origen «Valor mínimo», la advertencia «No se pudo calcular el servicio complementario…» va al detalle y Facturación recibe el aviso «Almacenamiento facturado con valor mínimo». R-FAC-08 corregido. Desactivar después. | P1 | RN |
| F6-ALM-015 | Renovación automática por job | (Palanca 2) poner `limit_date` en el pasado y reiniciar la API. | El job renueva el período; un fallo no deja el depósito sin factura (aviso «No se pudo facturar el almacenamiento»). | P1 | RN |
| F6-ALM-016 | Recepción sin báscula | Si F4-RSB-002 pasó: su período y factura. | Período abierto con la cantidad declarada. | P2 | INT |
| F6-ALM-017 | Salida en los días de gracia | Depósito con una fórmula por cantidad (`PER_UOM`) y un período que vence; despachar parte del stock entre el fin del período y el día del job (fin + 2) y dejar correr el job (o cerrar a mano). | **Nuevo (D19):** la factura del período renovado cobra el saldo del cierre de su día de inicio (la salida del día de gracia **sí** se cobra, la del propio día de inicio no); un CE-7 sin cambio la deja igual. Un contenedor despachado en la gracia cuenta para `PER_CARGO_UNIT`. | P0 | RN |
| F6-ALM-018 | Depósito agotado con Borrador sin N.º | Cargar y despachar todo el stock de un depósito con su factura de almacenamiento en Borrador sin N.º SIIGO. Mirar «Depósitos pendientes» con y sin el interruptor; numerar la factura; anularla. | **Nuevo (DEC-053, BR-06-003):** el depósito queda `Closed` y sigue en la lista como «Por numerar» sin período abierto («Cerrado» en «Días»); al numerar sale del filtro «solo pendientes»; al anular la factura sin refacturar vuelve como «Por refacturar». Un depósito anulado (`Cancelled`) nunca aparece. | P0 | RN |
| F6-ALM-019 | Depósito agotado en la gracia: se cobra el período del día S | Depósito con `PER_UOM` cuyo período ya terminó pero sigue en los días de gracia (fin = hoy − 2; en local, fechar `period_end` y `limit_date` hacia atrás). Cargar y despachar todo el stock hoy. Revisar el período y «Depósitos pendientes». Después poner `limit_date` en el pasado y dejar correr el job (o cerrar a mano). Repetir con la salida fechada el día S (fin + 1). | **Nuevo (DEC-055, D43):** al cargar, el depósito queda `Closed` pero su período sigue abierto hasta el job (aparece en «Depósitos pendientes» con período abierto). El job abre el período que empieza el día S con la cantidad que había al cierre de ese día, emite su factura en Borrador, avisa «Almacenamiento renovado» y lo cierra por agotamiento en la misma corrida; sin aviso de fallo. Si todo salió el día S o antes, no se abre período y el viejo queda cerrado. Un agotamiento dentro del período en curso lo cierra al cargar, como antes. | P0 | RN |

### 6.9 TRM (TRM)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-TRM-001 | TRM DIAN al confirmar | Depósito USD confirmado con la DIAN disponible. | TRM asignada con origen DIAN y fecha = fecha de ingreso; factura en pesos. | P0 | RN |
| F6-TRM-002 | TRM pendiente | (Local, sin red a la DIAN) confirmar un depósito USD. | Factura con valor mínimo y leyenda «TRM PENDIENTE…»; notificación a Facturación; acciones de N.º y aprobación bloqueadas. | P0 | RN |
| F6-TRM-003 | Registrar TRM manual | Desde la factura o depósitos pendientes: TRM 4.000, motivo 10–500. | Se guarda con origen Manual; recalcula la factura (ya con tarifa real); se habilitan N.º y aprobación. | P0 | RN |
| F6-TRM-004 | Validaciones | TRM 0; motivo de 9 o 501. | «La TRM debe ser mayor que cero.», «El motivo debe tener entre 10 y 500 caracteres.». | P1 | VAL |
| F6-TRM-005 | Depósito en COP | Registrar TRM en un depósito COP. | «El depósito está en pesos (COP); no requiere TRM.». | P2 | RN |
| F6-TRM-006 | Reemplazar TRM DIAN | En un depósito con TRM DIAN. | 409 «La TRM de este depósito ya fue consultada a la DIAN y no se puede reemplazar.». | P1 | RN |
| F6-TRM-007 | Factura aprobada | Cambiar TRM cuando la factura del período ya está aprobada. | «La factura … del período ya fue aprobada; la TRM no se puede cambiar.». | P1 | RN |
| F6-TRM-008 | TRM manual sobrescrita | Registrar otra TRM manual antes de aprobar. | Anotar: se permite por API. | P3 | RN |

### 6.10 Recálculo de facturas emitidas (REC)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-REC-001 | Camión tardío | Tras F3-MCA-009, revisar la factura del período. | Recalculada con la nueva cantidad; fechas del período conservadas. | P0 | RN |
| F6-REC-002 | CE-7 | Tras F5-AJU-001. | Recalculada. | P0 | RN |
| F6-REC-003 | Factura Draft | Recalcular con la factura en Draft. | Se reemplazan líneas; sin notificación (salvo override descartado). | P1 | RN |
| F6-REC-004 | Factura Approved/Sent | Recalcular con la factura aprobada con N.º. | Misma factura, conserva N.º y aprobación; notificación con total anterior y nuevo. | P0 | RN |
| F6-REC-005 | Factura con pagos | Recalcular una pagada parcialmente a un total menor que lo pagado. | Pasa a `Paid`; la notificación informa el saldo a favor. A un total mayor: `PartiallyPaid`. | P1 | RN |
| F6-REC-006 | Factura anulada | Recalcular un depósito cuya factura está anulada. | No se toca; notificación «Cambio de depósito sin facturar». | P1 | RN |
| F6-REC-007 | Otros disparadores | Anular pesaje de un camión de un depósito confirmado; cambiar fecha de ingreso; editar manifiesto. | Cada uno recalcula; un fallo de facturación no revierte el cambio y se notifica. | P1 | INT |

### 6.11 Refacturación (REF)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-REF-001 | Refacturar anulada | Factura de almacenamiento anulada → «Refacturar». | Nueva factura Draft sin número con las líneas clonadas; períodos, guías y ciclos re-enlazados; enlaces de refacturación en ambas. | P1 | FUN |
| F6-REF-002 | Refacturar no anulada | Por API sobre una Approved. | 409 «Solo se puede refacturar una factura anulada…». | P2 | RN |
| F6-REF-003 | Dos veces | Refacturar otra vez la misma. | 409 «La factura … ya fue refacturada como …». | P2 | RN |
| F6-REF-004 | Sin períodos | Refacturar una BASCULA anulada. | 400 «…no tiene períodos de almacenamiento; genere de nuevo el cobro desde su operación.». | P2 | RN |
| F6-REF-005 | Por refacturar visible | Pendientes de depósito tras anular la factura sin refacturar. | **Actualizado (DEC-053, BR-06-003):** la columna «Pendiente» muestra «Por refacturar» (y «Por numerar» para un Borrador sin N.º SIIGO); el interruptor «Solo con facturas por numerar o refacturar» deja solo esos depósitos. Un Borrador con N.º no cuenta. | P2 | UI |
| F6-REF-006 | Por refacturar con períodos cerrados | Anular la factura de un depósito cuyos períodos ya se cerraron. | Sigue visible para refacturar, aunque el depósito ya esté **Cerrado** (agotado) y no tenga período abierto (D22). R-FAC-10 corregido en el plan P1, fase 7. | P2 | RN |

### 6.12 Pagos (PAG)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-PAG-001 | Pago parcial | Factura Approved de 119.000 → pago 50.000 transferencia con referencia. | `PartiallyPaid`; pendiente 69.000; pago Received/Verified. | P0 | FUN |
| F6-PAG-002 | Pago total | Pagar el saldo. | `Paid`; pendiente 0. | P0 | FUN |
| F6-PAG-003 | Excede saldo | Pagar más del saldo. | «El monto del pago excede el saldo pendiente.». | P0 | VAL |
| F6-PAG-004 | Monto 0 | 0 o negativo. | «El monto del pago debe ser mayor a cero.». | P1 | VAL |
| F6-PAG-005 | Factura pagada o anulada | Pagar una `Paid`; una `Cancelled`. | «La factura ya está completamente pagada.» / «No se puede registrar un pago en una factura cancelada.». | P1 | RN |
| F6-PAG-006 | Métodos | Registrar con cada método. | Se guardan método, referencia, recibo, fechas de pago y consignación. | P2 | FUN |
| F6-PAG-007 | Pantalla de pagos | `/billing/payments`: buscar factura pagable. | Solo estados pagables; anotar si muestra «null — …» para facturas sin número. | P2 | UI |
| F6-PAG-008 | Comprobante adjunto | Adjuntar una imagen real (≥ 50 KB) al pago. | Esperado: se guarda. Riesgo R-FAC-04: error 500 (base64 en varchar(500)). Si se confirma: MAJOR/CRITICAL. | P1 | ERR |
| F6-PAG-009 | Error conserva el formulario | Provocar un error (monto > saldo por API mientras el diálogo está abierto, o comprobante grande). | Esperado: el formulario conserva los datos. Riesgo R-FAC-16: se limpia antes de la respuesta. | P2 | UX |
| F6-PAG-010 | Pago en Draft por API | `POST` de pago sobre una Draft. | Esperado: rechazo. Riesgo R-FAC-06: se acepta. | P2 | API |
| F6-PAG-011 | Verificar desde Pending | Botón «Verificar» en un pago Pending (si existe). | Riesgo R-FAC-06: «Solo se pueden verificar pagos recibidos.». | P3 | RN |
| F6-PAG-012 | Rechazar pago | Rechazar un pago Received. | Factura vuelve a Sent u Overdue (anotar si antes era Draft). | P2 | RN |
| F6-PAG-013 | Corregir un pago erróneo | Rechazar un pago Verified. | «No se puede rechazar un pago ya verificado.». Anotar que no hay forma de corregir un pago erróneo (R-FAC-06). | P2 | RN |
| F6-PAG-014 | Concurrencia | Dos pagos simultáneos que juntos exceden el saldo (dos pestañas). | Solo uno pasa (transacción serializable). | P2 | PER |

### 6.13 Configuración por cliente (CFG)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-CFG-001 | Crear configuración | `QA Cliente Uno`: Mensual, plazo 30, sin límite, PerService. | Se guarda. | P0 | FUN |
| F6-CFG-002 | Cliente con límite | `QA Cliente Mora`: límite 1.000. | Se guarda. | P0 | FUN |
| F6-CFG-003 | Consolidado | `QA Cliente Consolidado`: Biweekly, Consolidated. | Se guarda. | P0 | FUN |
| F6-CFG-004 | Ciclos disponibles | Abrir el selector. | 9 ciclos (Weekly, Biweekly, Days15, Monthly, Days30, Days90, Days180, Days360, OnDemand). | P2 | FUN |
| F6-CFG-005 | Validaciones | Plazo −1; límite −1. | «Los días de plazo de pago no pueden ser negativos.», «El límite de crédito no puede ser negativo.». | P1 | VAL |
| F6-CFG-006 | Quitar límite de crédito | Borrar el límite de `QA Cliente Mora` y guardar. | Esperado: queda sin límite. Riesgo R-FAC-05: conserva el anterior. Restaurar 1.000. | P1 | PER |
| F6-CFG-007 | Valor por defecto | Formulario nuevo. | Anotar: el frontend propone Consolidated y el backend, sin configuración, usa PerService. | P3 | UX |

### 6.14 Cartera y mora (CAR)

Requiere palancas de tiempo (§4).

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-CAR-001 | Preparar deuda | Factura Approved de `QA Cliente Mora` por > 1.000, sin pagos; `due_date` en el pasado; reiniciar la API. | La factura pasa a `Overdue`; el cliente a `Blocked` (deuda > límite). | P0 | RN |
| F6-CAR-002 | Overdue con pago parcial | Igual con una factura con pago parcial. | `Overdue` en la primera corrida. | P1 | RN |
| F6-CAR-003 | Overdue sin pagos | Contar los reinicios necesarios en F6-CAR-001. | Esperado: 1. Riesgo R-FAC-02: hacen falta 2 (AmountPaid null). | P1 | RN |
| F6-CAR-004 | OverdueWarning | Cliente con deuda vencida menor que su límite. | `OverdueWarning`; no bloquea. | P1 | RN |
| F6-CAR-005 | Borrador vencido | Factura Draft (por facturar) con `due_date` pasado; reiniciar. | Esperado de negocio: no vence un borrador. Riesgo R-FAC-03: pasa a Overdue y ya no se puede asignar N.º ni aprobar. Si se confirma: CRITICAL. | P1 | RN |
| F6-CAR-006 | Sin límite nunca bloquea | `QA Cliente Uno` con deuda vencida. | Nunca `Blocked`. | P0 | RN |
| F6-CAR-007 | Límite 0 | Cliente con límite 0 y cualquier deuda vencida. | `Blocked`. | P2 | RN |
| F6-CAR-008 | Desbloqueo | Pagar la deuda del bloqueado; reiniciar. | Vuelve a `Active`. | P0 | RN |
| F6-CAR-009 | Efecto del bloqueo | Con `QA Cliente Mora` bloqueado: cobro de báscula (F3-COB-009), cierre de montacargas (F4-MON-010), recepción sin báscula (F4-RSB-006), orden de cargue (F5-OC-007), guía (F5-GUI-011). | Los cinco bloqueados con «El cliente '…' está bloqueado por deuda pendiente…». Re-ejecutar los casos que quedaron `BLOQUEADO` en fases anteriores. | P0 | INT |
| F6-CAR-010 | Destinatario no registrado | Factura vencida de un conductor no registrado. | No afecta a ningún estado financiero. | P3 | RN |
| F6-CAR-011 | Aviso de vencimiento | Factura que vence en ≤ 3 días; reiniciar (+1 min). | Notificación (y correo) a Facturación. | P2 | INT |

### 6.15 Cobros por facturar y consolidación (CON)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-CON-001 | Consolidación diaria | Cliente Consolidated con 2 cobros de báscula por facturar en el día; reiniciar la API. | Esperado (D-1, CHG-63): factura individual para báscula y montacargas; «Consolidada» agrupa solo almacenamiento y guías de salida a crédito. El job diario es la conciliación de pagos y no fusiona cargos. | P1 | RN |
| F6-CON-002 | PerWeighbridgeCycle | Cliente con esa preferencia. | Anotar: se comporta igual que PerService. | P3 | RN |
| F6-CON-003 | Vencimiento de por facturar | Factura por facturar de báscula. | Anotar: vence el mismo día (`UtcNow`), lo que dispara R-FAC-03 al día siguiente. | P2 | RN |

### 6.16 Jobs (JOB)

| ID | Caso | Pasos | Resultado esperado | P | Tipo |
|---|---|---|---|---|---|
| F6-JOB-001 | Arranque de jobs | Reiniciar la API y revisar el log. | Los 4 jobs de facturación corren sin excepciones. | P1 | FUN |
| F6-JOB-002 | Idempotencia | Reiniciar dos veces seguidas. | No duplican períodos, facturas ni notificaciones. | P1 | PER |
| F6-JOB-003 | Error en un depósito | (Local) forzar el fallo de un depósito (p. ej. regla inválida) y renovar. | Rollback de ese depósito, aviso «No se pudo facturar el almacenamiento», los demás se procesan. | P2 | ERR |

## 7. Criterios de salida específicos

- P0 de INV, ACC, TAR, FOR, ALM, TRM, REC, PAG, CFG y CAR ejecutados con cálculo manual adjunto.
- Ningún CRITICAL de dinero sin informar al usuario.
- Riesgos verificados: R-FAC-01 a R-FAC-16.
- Casos `BLOQUEADO` por mora de las fases 3, 4 y 5 re-ejecutados (F6-CAR-009).

## 8. Entregables

Informe de fase con la hoja de cálculo de verificación, las palancas de tiempo usadas, defectos y registro de datos. Detenerse.
