# Contexto del proyecto WMS — Bodegas Asociadas

> **Para qué sirve:** darle a un agente de IA sin historial el contexto de negocio, el vocabulario, las reglas vigentes y el estado del trabajo antes de proponer o tocar código.
> **Fecha de corte:** 14 de septiembre de 2026. Backend `wms-api`, rama `develop` (`bc33aae`). Frontend `wms`, rama `develop` (`df6a526`).
> **Raíz del proyecto:** `/Volumes/Dock/Projects/bodegas_asociadas/`. Las rutas de este documento son relativas a ella salvo que se indique otra cosa.
> **Idioma:** el negocio, la UI, los mensajes de error y la documentación están en español. El código, en inglés.

---

## 0. Cómo leer este documento

El proyecto está en una ronda de ajustes tras las pruebas con los operarios. Conviven tres versiones de la verdad: cómo opera la bodega, las reglas ya decididas (que el código a veces no implementa todavía) y el código de `develop`. Cuando difieren, el documento lo marca con **Hoy** (código actual) y **Decidido** (regla que se va a implementar).

Precedencia de las fuentes, de mayor a menor:

1. Decisiones del 14-sep-2026, recogidas en el plan cerrado de la Ola 1 (`code_workspace/ajustes/plan-cerrado-ola-1-2026-09-14.md`).
2. Premisas de pruebas del 10-sep-2026 (§5.0).
3. Historias de usuario del backlog (`code_workspace/ajustes/historias-usuario-linear-2026-09-10.md`).
4. El código, para saber cómo se comporta hoy.
5. Documentos antiguos, que tienen partes superadas (ver §13).

---

## 1. El negocio en una página

**Bodegas Asociadas** opera una bodega en **Ipiales (Nariño, Colombia)**, junto al paso fronterizo de **Rumichaca** con Ecuador. La DIAN la habilita como **depósito público aduanero**: la mercancía que cruza la frontera se queda ahí mientras se tramita su nacionalización, su exportación o su inspección.

| Servicio | Qué pasa |
| --- | --- |
| Importación | Un camión del exterior deja mercancía que espera el levante de la DIAN (nacionalización). Sale completa o por partes cuando el cliente la pide. |
| Exportación | Mercancía nacional espera para salir del país. Puede descargarse o quedarse en el vehículo o contenedor. |
| Inspección | La mercancía permanece hasta que la DIAN la inspecciona. |
| Otros (solo báscula) | El camión solo se pesa y sale. |

La bodega cobra cuatro servicios: **báscula**, **montacargas**, **guía de salida** y **almacenamiento**. Los tres primeros son de contado, o se acumulan para una factura consolidada. El almacenamiento es a crédito, por períodos y por depósito, según los convenios con cada cliente.

El sistema reemplaza una bitácora manual en portería, el control manual de inventario, un sistema legacy de báscula y una facturación dispersa. El sistema legacy pesa un camión en ~30 s: esa es la meta de velocidad. **El WMS no emite factura electrónica.** La factura legal se hace en **SIIGO** (software contable) y Facturación copia el número en el WMS.

La mercancía típica son perecederos (p. ej. cebolla), líquidos en tanqueros y carga en contenedores. Hay terceros y vehículos colombianos y ecuatorianos: existe el tipo de identificación RUC y se registra el país del vehículo. Monedas: COP y USD.

---

## 2. Glosario

| Término | Significado | En el código |
| --- | --- | --- |
| **Depósito** | Lote de mercancía amparado por un mismo documento de ingreso (carta porte) y una modalidad. Es la unidad de inventario, de etiqueta y de cobro de almacenamiento. Puede llegar en varios camiones y tener varios productos. | `WarehouseStorage` (`warehouse_storages`) |
| **Carta porte** | Documento de transporte internacional que ampara la carga. Carta porte + modalidad = un depósito. | `ServiceRecord.CargoManifestNumber` (el nombre engaña: es la carta porte, no el manifiesto) |
| **Manifiesto de carga / manifiesto DIAN** | Documento aduanero de la carga. En importación, Comercio Exterior registra su número y fecha. | `Manifest`, campos de manifiesto en `ImportWarehouseStorage` |
| **Levante** | Autorización de la DIAN para disponer de la mercancía importada. Puede ser parcial. Comercio Exterior lo consulta en **MUISCA**, el portal de la DIAN (no hay integración). | `ImportRelease` |
| **Nacionalización** | Estado de la mercancía importada cuando los levantes cubren la cantidad. | `ImportLabelsStatus`: `SinNacionalizar` → `Nacionalizado` |
| **Etiqueta** | Rótulo impreso que se pega a la mercancía. Importación: «SIN NACIONALIZAR» y luego «NACIONALIZADO» con el levante. Exportación: cantidad contada o peso. Se reimprime cuando cambia la cantidad. | `LabelGenerationService` |
| **Tiquete de báscula** | Comprobante del pesaje que se entrega al conductor. | `WeighbridgeCycle` |
| **Peso bruto / tara / neto** | Camión cargado / camión vacío / diferencia. | `TypeWeight`: `Gross`, `Tare` |
| **Repesaje** | Segundo pesaje del ciclo. | — |
| **Orden de cargue (OC)** | Autorización interna de Comercio Exterior para retirar mercancía de uno o varios depósitos. Reserva el stock. | `LoadingOrder`, `LoadingOrderItem`, `WarehouseReserve` |
| **Guía de salida** | Documento que acompaña la salida. En importación se entrega al conductor; en exportación se genera sin entregarse. Se cobra. | `DispatchGuide` (`GuideType`: `Import`, `Export`, `Inspection`) |
| **Unidad de carga** | Contenedor, tanquero o remolque que entra con el camión: se anota su placa, no se descarga y sale completo. Concepto en construcción (WMS-30). | Hoy: `WarehouseStorageContainer`, `LoadingOrderContainer` |
| **Tanquero** | Remolque cisterna para líquidos. Hoy figura como producto y como embalaje (`PackagingType` `TANQUERO`), y eso confunde. | — |
| **Montacargas** | Servicio de descargue o cargue. Se registran horómetro inicial y final. | `ForkliftUse`, `ForkliftRate` |
| **TRM** | Tasa representativa del mercado (COP por USD). Convierte a pesos el valor de la carga en moneda extranjera. Se consulta a un servicio de la DIAN. | `WarehouseStorage.Trm`, `IDianTrmService` |
| **CIF / valor de la carga** | Valor declarado de la mercancía. Es la base de las tarifas por porcentaje. | `WarehouseStorage.CargoValue` + `Currency` |
| **Tercero (stakeholder)** | Persona o empresa con uno o varios roles de negocio. | `Stakeholder`, `StakeholderBusinessRole` |
| **Cliente del depósito** | Tercero al que se factura el almacenamiento. Lo asigna Comercio Exterior y es requisito para confirmar. | — |
| **Agencia de aduanas = SIA = intermediario** | Un solo rol de negocio, con código canónico `CUSTOMS_AGENCY`. Un `"SIA"` o `"INTERMEDIARY"` en el código es un bug. | `BusinessRole` |
| **Convenio (acuerdo)** | Tarifas pactadas con un cliente por servicio, producto y modalidad, con fórmulas. | `Agreement` → `AgreementService` + `AgreementParameter` |
| **Tarifa base** | Tarifa por defecto de un servicio por producto y modalidad cuando no hay convenio. | `ServicePricingRule` + `ServicePricingRuleParameter` |
| **Valor mínimo** | Piso de cobro por servicio y modalidad. También es el cargo de respaldo del almacenamiento. | `ServiceMinimumValue` |
| **N.º SIIGO** | Número de la factura legal emitida en SIIGO. Lo digita Facturación. | `Invoice.InvoiceNumber` (nulable) |
| **Consumidor final** | Destinatario genérico, con identificación `222222222222`. | `InvoiceRecipient` |
| **CE-7** | Ajuste de la cantidad de un depósito, hecho por Comercio Exterior. | `AdjustInventoryCommand` |
| **Racimo / Ola** | Organización del backlog. Un racimo (R01–R11) es un paquete de issues que un agente implementa de una vez; una ola agrupa racimos que pueden avanzar en paralelo. | Etiquetas de Linear |

**Siglas en comentarios y nombres:** `WMS-n` (issue de Linear), `CE-n` (requerimiento de Comercio Exterior), `FAC-n` (facturación), `ALM-n` (hallazgo del análisis de almacenamiento), `B-n` y `F-n` (pasos de planes backend y frontend), `Dn` (decisión de un plan cerrado). La numeración `Dn` se reinicia en cada plan: `D4` significa algo distinto según el documento que la cite. Varios documentos citados en esos comentarios (`requerimientos_funcionales.md`, `arquitectura_y_plan_*.md`, `analisis_cobro_almacenamiento.md`) ya no están en `code_workspace/docs/planes/`.

---

## 3. Actores, roles y permisos

| Rol (código) | Nombre en la UI | Módulo · ruta | Responsabilidad |
| --- | --- | --- | --- |
| `Receiving` | Operario vigilancia | Vigilancia · `/operations/entries` | Registra el ingreso y la salida de vehículos con captura mínima (placa, motivo). Su hora de ingreso es la «fecha de ingreso» del depósito (decidido). |
| `Scale` | Operario báscula | Báscula · `/operations/weighbridge` | Toma el camión de la cola, registra documentos, terceros y cantidades declaradas, cobra, pesa e imprime el tiquete. Crea el depósito o asocia el camión a uno existente. |
| `Warehouse` | Operario bodega | Bodega · `/warehouse` | Recepción (conteo, fotos, ubicación), montacargas, verificación y ejecución de órdenes de cargue, inventario. |
| `ForeignTrade` | Comercio exterior | `/foreign-trade` | Dueño del depósito: asigna cliente, confirma, ajusta cantidades (CE-7), imprime etiquetas, registra levantes, crea órdenes de cargue y guías, cierra el ingreso de camiones. |
| `Billing` | Facturación | `/billing` | Facturas, N.º SIIGO, aprobación, pagos, configuración de facturación por cliente, depósitos pendientes por facturar, TRM manual. |
| `Admin` | Administrador | `/admin` | Todo, más los catálogos: terceros, productos, servicios y tarifas, usuarios, ubicaciones, embalajes, parámetros, auditoría. |

Un usuario puede tener varios roles (p. ej. Facturación + Comercio exterior). Los reportes están en `/reports` y las notificaciones en `/notifications`.

Políticas del backend (`Backend/wms-api/Wms.Api/Common/Identity/WmsAuthentication.cs`):

| Política | Roles |
| --- | --- |
| `AdminOnly` | Admin |
| `ScaleAccess` | Admin, Scale |
| `WarehouseAccess` | Admin, Warehouse, Receiving |
| `ForeignTradeAccess` | Admin, ForeignTrade |
| `BillingAccess` | Admin, Billing |
| `WeighingCorrectionAccess` | Admin, Scale, Billing |
| `OperationalAccess` | Admin, Warehouse, Receiving, Scale |
| `ActiveUser` | Cualquier usuario activo |

**Convención del proyecto:** los permisos se aflojan **por endpoint**, no por controlador. Las lecturas y catálogos que usan los flujos operativos van a `ActiveUser`; las escrituras operativas, a `OperationalAccess`; la configuración de tarifas y de facturación sigue restringida. Los `[Authorize]` de ASP.NET se suman (AND): para aflojar una acción de un controlador restringido hay que moverla a otro controlador. Así nacieron `WeighbridgeCatalogController`, `WeighbridgeSharedController`, `BillingPreviewController`, `InventoryAdjustmentController` y `WarehouseMovementsReportController`. En el frontend, cada página declara `definePageMeta.requiredRoles` y el menú se filtra en `app/components/layout/AppMenu.vue`.

---

## 4. Modalidades de operación

| Código | Nombre | ¿Crea depósito? | Particularidades |
| --- | --- | --- | --- |
| `IMP001` | Importación | Sí, más `ImportWarehouseStorage` | Etiquetas SIN NACIONALIZAR → NACIONALIZADO; levantes por producto; la orden de cargue exige mercancía nacionalizada; la guía se entrega al conductor. |
| `EXP001` | Exportación | Sí | Puede quedarse en el vehículo o contenedor; la etiqueta lleva la cantidad contada o el peso; la guía se genera sin entregarse. |
| `INSP001` | Depósito por inspección | Sí | Un solo pesaje, con primer peso bruto forzado. |
| `OTH001` | Otros | No | Solo báscula: un pesaje, cobro y tiquete. No tiene serie de consecutivos de depósito. |

El código detecta la modalidad por prefijo (`IMP*`, `EXP*`, `INSP*`). En las tarifas, «tipo de depósito» es esta misma dimensión (`OperationModality`), no un concepto aparte.

---

## 5. Flujos operativos

### 5.0 Premisas de pruebas (10-sep-2026)

Salieron de las pruebas con los operarios y rigen todos los ajustes. Donde una historia las contradecía, se reescribió.

1. **Báscula rápida.** Hoy el pesaje tarda ~2 min, frente a ~30 s del sistema legacy. Sobran clics y el «Continuar» de cada paso. Se rediseña como pantalla única con cola de camiones, porque puede haber varios esperando (WMS-31).
2. **Las cantidades del depósito son las declaradas en báscula**, tomadas de los documentos. Bodega solo informa y confirma. Comercio Exterior confirma el depósito e imprime la etiqueta apenas se genera, sin esperar la descarga ni la recepción (WMS-9).
3. **La unidad de carga es un concepto propio.** El camión entra con su contenedor, tanquero o remolque; se pesa y se anotan sus placas; Bodega recibe la unidad completa sin descargar ni contar producto por producto; en la salida se recoge completa. Un mismo documento puede amparar varias unidades (WMS-30).
4. **Fechas editables.** Si el camión entra el sábado y se procesa el lunes, el depósito, los pesajes y la etiqueta llevan la fecha del sábado (WMS-33).

No propongas diseños que hagan esperar a Comercio Exterior por Bodega, ni que cuenten producto por producto dentro de unidades de carga.

### 5.1 Ingreso con depósito (importación, exportación, inspección)

1. **Vigilancia** registra el ingreso: placa (si no existe, se crea el vehículo) y motivo. Un vehículo no puede tener dos ingresos abiertos. Queda un `EntryLog` con `DateTimeEntry`.
2. **Báscula** toma el camión de la cola (ingreso abierto sin servicio asignado), elige «Ingreso con depósito» y registra: carta porte y su fecha, modalidad, cliente, terceros documentales (importador o exportador, agencia de aduanas, transportadora), vehículo, conductor, país del vehículo y productos con **cantidad, peso neto y peso bruto declarados**, embalaje, unidad de medida, valor de la carga y moneda. Comando: `InitiateStorageWeighing`.
   - Primer camión con esa carta porte: crea el `ServiceRecord` (tipo `Input`), el `WarehouseStorage` en `Draft` y, si es importación, el `ImportWarehouseStorage` (`SinNacionalizar`). Notifica a Comercio Exterior.
   - Camión adicional con la misma carta porte y modalidad: reutiliza el servicio y el depósito, y crea otra `WarehouseStorageEntry` (una por camión, con su desglose por producto). Una modalidad distinta para un documento existente es error.
3. **Cobro de báscula**, antes de pesar: inmediato (factura y pago en el acto) o «pendiente por facturar» para clientes con facturación consolidada. Valida que el cliente no esté bloqueado por mora.
4. **Pesajes:** primer peso bruto; segundo peso (tara) cuando el camión vuelve; neto = bruto − tara; tiquete. Inspección: un solo pesaje. Corregir un peso exige `WeighingCorrectionAccess`; el requerimiento original pide notificar al administrador de toda modificación manual.
5. **Bodega** recibe: cantidad contada por producto, fotos, ubicación y montacargas si aplica.
6. **Comercio Exterior**, en el detalle del depósito: asigna el cliente, revisa, **confirma** (`Draft → Confirmed`) e imprime la etiqueta. Confirmar abre el primer período de almacenamiento con su factura (§7.4).
7. **Vigilancia** registra la salida.

**Hoy vs decidido (Ola 1, WMS-9, sin implementar):**

- **Hoy** el stock lo crea la recepción de Bodega (`ReceiveQuantity` en `CreateReception` y `CompleteReception`), y confirmar exige recepciones completadas. Si lo contado difiere más de 5 %, se envía un correo al administrador. `EntryDate` lo fija la recepción con la hora del servidor. La recepción también abre el período de facturación.
- **Decidido:** cada camión suma su cantidad declarada al stock en báscula. Confirmar solo exige cliente. La recepción no mueve stock ni factura: guarda lo contado y, si difiere de lo declarado para ese camión, notifica en la app a Comercio Exterior, que corrige con CE-7 si corresponde. `ReceivedQuantity` pasa a significar «cantidad del depósito» (declarada + ajustes CE-7) y no se renombra. La fecha de ingreso es la de Vigilancia para el primer camión.

### 5.2 Varios camiones con la misma carta porte

Lo normal es que los camiones de un documento lleguen juntos; a veces uno llega tarde.

- **Hoy (bug WMS-26):** al completar el ciclo del primer camión, el `ServiceRecord` pasa a `Completed` y rechaza a los siguientes.
- **Decidido (Ola 1):** completar el ciclo de un camión ya no cierra el servicio. Comercio Exterior cierra el ingreso de camiones de forma explícita («Cerrar ingreso de camiones», sin reapertura). Después, báscula no asocia más camiones y el error dice quién cerró y cuándo. Báscula muestra «Camiones ingresados: N».
- **Camión tardío en un depósito confirmado (decidido):** su cantidad entra al stock, se recalcula la factura del período (§7.7) y se avisa a Comercio Exterior para reimprimir la etiqueta. Un error de facturación nunca bloquea báscula: se notifica a Facturación.

### 5.3 Salida de importación

1. El cliente pide la salida, normalmente por correo, parcial o total.
2. **Comercio Exterior** crea la orden de cargue. Puede incluir uno o varios depósitos, y desde CE-12 puede mezclar clientes. Exige depósito confirmado (no en Borrador), mercancía nacionalizada, stock disponible por producto y cliente no bloqueado. Crea reservas y un PDF.
3. El conductor entra por Vigilancia. En **báscula** se hace la operación «Salida de mercancía» con la orden: pesaje del camión vacío y cobro.
4. **Bodega** verifica la orden y carga. El stock se descuenta por producto y quedan movimientos de inventario.
5. **Comercio Exterior** emite la guía de salida (servicio `GUIA_SALIDA`, que se cobra) y la entrega al conductor. Si queda saldo, reimprime la etiqueta NACIONALIZADO con la cantidad nueva.
6. Repesaje del camión cargado y salida por Vigilancia.
7. Cuando ningún producto tiene stock, el depósito pasa a `Closed` y sus períodos de almacenamiento se cierran.

La guía imprime, por línea, la entrada, el saldo anterior, lo despachado y el nuevo saldo. **Bug WMS-19 (urgente):** el saldo anterior sale duplicado. Decidido: congelar los saldos al emitir, en la tabla nueva `dispatch_guide_lines`. Saldo anterior = cantidad del depósito − lo despachado en guías emitidas antes, estén ejecutadas o no. **WMS-17 (abierto):** simplificar la orden de cargue para que el operario solo registre la orden externa.

### 5.4 Exportación

El ingreso es como el de importación, pero la mercancía puede quedarse en el vehículo o contenedor (se deja el remolque). La etiqueta lleva la cantidad contada si hubo descargue, o el peso si quedó el vehículo completo. En la salida, Comercio Exterior genera la orden de cargue; Bodega verifica y carga; el sistema genera la guía (no se entrega al conductor) y finaliza el depósito.

### 5.5 Inspección

Es un depósito normal con un solo pesaje (primer peso bruto forzado). La mercancía queda en la bodega hasta que la DIAN la inspecciona.

### 5.6 Solo báscula (`OTH001`)

Un pesaje, cobro y tiquete, sin depósito. En el levantamiento de 2025 la tarifa de referencia era $23.000 por pesaje.

### 5.7 Recepción sin báscula

Si el camión no pasa por báscula (motivo «Solo bodega»), Bodega crea el depósito desde la recepción, con cantidades declaradas manuales (`CreateReceptionWithoutWeighbridge`).

### 5.8 Montacargas

Bodega inicia el uso con el horómetro inicial. Puede empezar antes de que Comercio Exterior asigne el cliente. Al finalizar (horómetro final) se cobra con el formulario de cobro: la tarifa depende del tipo de vehículo (`ForkliftRate`: tractomula, doble troque, sencillo, turbo, guacal/estiba) y el valor es editable. **Decidido (WMS-28):** el servicio `MONTACARGAS` no admite impuestos configurados; el formulario trae un check «Agregar IVA», desmarcado por defecto, que suma el IVA sobre el valor digitado.

### 5.9 Operaciones incompletas

Báscula puede retomar una operación a medias o descartarla (`ServiceRecord` → `Discarded`) desde `/operations/weighbridge/recover`.

### 5.10 Destinatario del cobro

El destinatario de un cobro puede ser un tercero registrado, una persona no registrada (p. ej. el conductor: basta con su cédula, y sus datos se precargan, WMS-23) o el consumidor final.

---

## 6. El depósito en detalle

```
ServiceRecord (Input: carta porte, modalidad, terceros documentales)
 └─ WarehouseStorage (número, estado, CIF, moneda, TRM, fecha de ingreso, cliente)
     ├─ WarehouseStorageProduct        una fila por producto: declarado, recibido, stock,
     │                                 reservado, disponible, embalaje, unidad, ubicación
     ├─ WarehouseStorageEntry          una fila por camión (EntryLog, ciclo de báscula)
     │   └─ WarehouseStorageEntryProduct   declarado por producto en ese camión
     ├─ WarehouseStorageContainer      contenedores y tanqueros
     ├─ ReceptionLog → ReceptionLogProduct   conteo de Bodega por producto
     └─ ImportWarehouseStorage         solo IMP: etiquetas, manifiesto DIAN, levantes por producto
```

`ServiceRecord` y `EntryLog` se relacionan N:M (`service_record_entry_logs`).

**Estados** (`WarehouseStorageStatus`):

| Estado | Significado |
| --- | --- |
| `Draft` | Inicial y editable. |
| `Confirmed` | Lo confirma Comercio Exterior. Admite recepciones, reservas y despachos. `MarkForCorrection` lo devuelve a `Draft`. |
| `Closed` | Todos los productos quedaron con `CurrentStock = 0`. |
| `Cancelled` | Anulado con motivo (p. ej. operación descartada en báscula). |

Las órdenes de cargue y las guías rechazan depósitos en `Draft`.

**Stock por producto:** `AvailableStock = CurrentStock − ReservedStock`, nunca negativo. La orden de cargue reserva; el despacho descuenta `CurrentStock` y libera la reserva.

**Importación:** cada levante (`ImportRelease`) apunta a un producto. El depósito queda `Nacionalizado` cuando la cantidad nacionalizada de cada producto alcanza `min(CurrentStock, ReceivedQuantity)`.

**Fecha de ingreso** (`WarehouseStorage.EntryDate`). **Hoy** la fija la recepción con la hora del servidor. **Decidido:** es el `EntryLog.DateTimeEntry` del primer camión y no cambia con los siguientes. Rige la etiqueta, la fecha de la TRM y el año de los consecutivos. El período de almacenamiento sigue contando desde la confirmación; WMS-33 decidirá si cuenta desde el ingreso.

**Numeración:**

| Documento | Hoy (`develop`) | Decidido (WMS-16) |
| --- | --- | --- |
| Depósito de importación | `DEP-IMP-2026-0001` | `2026BA00001` |
| Depósito de exportación | `DEP-EXP-2026-0001` | `2026EXP00001` |
| Depósito por inspección | `DEP-INS-2026-0001` | `2026INSP00001` |
| Tiquete de báscula | `TKT-2026-0001` | `2026T00001` |
| Guía de salida | `{tipo}-{aaaammdd}-0001` | `2026S00001` (una serie para importación, exportación e inspección) |
| Orden de cargue | `OC-{aaaammdd}-0001` | `2026OC00001` |

Reglas decididas: 5 dígitos, reinicio anual y sin saltos (tabla `document_sequences` con `SELECT … FOR UPDATE` dentro de la transacción del documento). El año es el de Colombia: tiquetes y depósitos toman el de la fecha de ingreso; guías y órdenes, el de su emisión. `OTH` no tiene serie de depósito.

---

## 7. Facturación

### 7.1 Modelo

| Servicio (código) | Cuándo nace el cargo | Cómo se cobra |
| --- | --- | --- |
| `BASCULA` | En el cobro de báscula, antes de pesar (ingreso, salida o solo báscula) | Contado inmediato (factura y pago) o pendiente para consolidación |
| `MONTACARGAS` | Al finalizar el uso | Igual que báscula |
| `GUIA_SALIDA` | Al emitir la guía | Igual que báscula |
| `ALMACENAMIENTO` | Al confirmar el depósito y en cada renovación de período | Crédito: una factura por depósito, o la consolidada del cliente |

`ServicePaymentMode` distingue `Immediate` (factura y pago al registrar el servicio) de `PendingBilling` (el cargo espera la consolidación). Un job diario consolida los cargos de los clientes con preferencia `Consolidated`.

**No existe creación manual de facturas en el frontend.** El sistema las genera; Facturación asigna el N.º SIIGO, aprueba, envía y registra pagos. `pages/billing/invoices/create.vue`, `BillingPreviewPanel.vue` y la consulta `GetStorageInvoiceDraft` son restos congelados, sin entrada en la UI: no los revivas. Para corregir un valor se sobrescribe una línea (`POST billing/invoice-items/{id}/override`, entidad `BillingAmountOverride`).

### 7.2 Configuración de facturación por cliente

`StakeholderBillingConfiguration` define:

- Ciclo: `Weekly`, `Biweekly`, `Monthly` u `OnDemand`.
- Días de plazo.
- Límite de crédito (opcional).
- Preferencia: `Consolidated`, `PerService` o `PerWeighbridgeCycle`.
- Si está activa.

Sin configuración, el almacenamiento usa el ciclo mensual.

### 7.3 Resolución de tarifa

Vive en `Backend/wms-api/Wms.Application/Billing/Services/BillingResolver.cs`. Para un servicio, cliente, producto y modalidad gana el primer nivel que tenga regla:

1. **Convenio del cliente** (`AgreementService` activo), evaluado con una escalera de especificidad entre servicio, producto y modalidad. Dentro de un peldaño gana el más reciente.
2. **Tarifa base del servicio** (`ServicePricingRule`), con la misma escalera.
3. **Precio base vigente** del servicio (`ServicePrice`, respetando su vigencia).
4. **Sin tarifa:** error, salvo en almacenamiento, que cae al valor mínimo.

Si no hay cliente (`Guid.Empty`), se omite el nivel 1. El cálculo (cantidad facturable, redondeo, IVA) existe una sola vez; no lo dupliques.

**Fórmulas** (`FormulaType`). Sus parámetros viven en `AgreementParameter` o `ServicePricingRuleParameter`.

| Código | Qué cobra |
| --- | --- |
| `FIXED` | Valor fijo. Admite tarifas cotizadas «IVA incluido». |
| `PERCENTAGE_OF_VALUE` | Un % del CIF en pesos, con `minimum` y `minimumThreshold`. **No se multiplica por el stock**: el CIF ya es del lote completo. |
| `PERCENTAGE_OF_VALUE_PRORATED` | Un % de `CIF × (CurrentStock / ReceivedQuantity)`. Base plana; el mínimo no se prorratea. Existe aparte porque el cliente no ha confirmado si el almacenamiento se prorratea por saldo. No modifiques la fórmula original: cambiaría el importe de convenios firmados. |
| `PER_UOM` | Valor × cantidad en una unidad de medida. El parámetro `uom` debe coincidir con la `UnitMeasure` de los productos. |
| `PER_VEHICLE` | Valor × vehículos del depósito. Ejemplo real: $257.600 por vehículo. |
| `PER_CONTAINER`, `FIXED_PER_CONTAINER` | Por contenedor. Ejemplo real: $40.000 por contenedor. |
| `PER_PACKAGING_UNIT` | Valor × unidades de un embalaje del depósito. Ejemplo real: $291.200 por tanquero. |
| `PER_VEHICLE_TYPE` | Solo montacargas: tarifa por tipo de vehículo. |
| `BASE_PRICE` | Precio base plano (nivel 3). |

`ALMACENAMIENTO` admite todas las fórmulas salvo `PER_VEHICLE_TYPE`. No prohíbas fórmulas a partir de lo que le falta al modelo de datos: el cliente las usa en convenios reales.

### 7.4 Almacenamiento

- **Unidad de trabajo: el depósito.** Los productos con stock se agrupan por la regla que les resuelve, y cada grupo es un cargo. Hay un `StorageBillingPeriod` por cargo, con sus productos en `StorageBillingPeriodProduct`. La factura es una por depósito (o la consolidada del cliente), con una línea por cargo más las de servicios complementarios.
- **Las magnitudes del depósito se cobran una sola vez:** CIF, contenedores y vehículos. Si dos grupos reclaman la misma magnitud, esos grupos caen al respaldo. El CIF de un grupo se prorratea por `ReceivedQuantity`.
- **La factura de almacenamiento siempre se genera.** Sin tarifa, o si la regla falla, el cargo usa el valor mínimo de la modalidad (`ServiceMinimumValue`); sin mínimo, sale en $0. En ambos casos la advertencia va al `Detail` de la factura y a una notificación para Facturación, que corrige con un override. Nunca dejes una advertencia sin factura: el operario no tiene cómo regenerarla.
- **Período:** empieza al confirmar el depósito y dura según el ciclo del cliente: semanal 7 días, quincenal **14 días**, mensual 1 mes. Con `OnDemand` no se abren períodos automáticos.
- **Qué cobra cada período:** el primero cobra la cantidad total; las renovaciones cobran sobre el saldo en las fórmulas por cantidad y en la prorrateada. `PERCENTAGE_OF_VALUE` cobra el CIF completo en cada renovación.
- **Se cobra por adelantado:** si el stock se agota antes del fin del período, el período conserva lo facturado.
- **Renovación y cierre:** un job cierra los períodos vencidos y renueva los de depósitos que aún tienen stock. Los períodos cuyos productos llegan a stock 0 se cierran.
- `Invoice.Detail` (máx. 1000 caracteres) lleva un bloque descriptivo por depósito.
- **Hoy** la factura inicial se abre al confirmar y también desde las recepciones; la apertura es idempotente. **Decidido:** las recepciones dejan de facturar.
- **Observación sin confirmar:** el levantamiento dice que en exportación «el cliente paga por cada 15 días», y el ciclo quincenal del código es de 14 días.

### 7.5 TRM

Aplica cuando la moneda del depósito no es COP.

- **Hoy:** báscula consulta la TRM al crear el depósito. Si la DIAN no responde, el formulario se bloquea (bug WMS-24) y la TRM del depósito queda inmutable.
- **Decidido (Ola 1):** báscula no toca la TRM.
  - Se consulta al crear la factura del período: en la confirmación y en cada renovación si falta. Usa la fecha de ingreso y espera 3 s como máximo.
  - Si la consulta falla, el depósito queda con **TRM pendiente** y la factura se genera igual, con el valor mínimo y la leyenda «TRM PENDIENTE…».
  - Facturación registra la TRM manual (roles Billing y Admin, motivo de 10 a 500 caracteres). Mientras falte, no se puede asignar el N.º SIIGO ni aprobar la factura.
  - Se guardan el origen (`Dian` o `Manual`) y la fecha. La DIAN nunca reemplaza una TRM manual, y una TRM de la DIAN no se reemplaza a mano.
  - Registrar la TRM recalcula la factura (§7.7).

### 7.6 Facturas

Estados: `Draft` → `PendingApproval` → `Approved` → `Sent` → `PartiallyPaid` / `Paid`. El job marca `Overdue` al vencer. `Cancelled` exige motivo.

- **N.º SIIGO:** lo asigna Facturación y es único. Una factura en $0 no lleva número fiscal. Decidido (WMS-20): solo se asigna o cambia en Borrador o Pendiente de aprobación, y queda fijo al aprobar.
- **Destinatario:** tercero registrado, persona no registrada (conductor), consumidor final o pendiente. Decidido (WMS-21): el listado muestra las columnas «Identificación» y «Destinatario». Hoy solo se ve el NIT por un bug de contrato: el front pinta `recipientName` y el API envía `customerName`.
- **Diálogo de acciones** decidido (WMS-20):
  - Aprobar.
  - Anular, con motivo de al menos 10 caracteres.
  - Asignar o cambiar el N.º SIIGO.
  - Editar el detalle, solo en Borrador.
  - Notas, salvo en facturas anuladas.
  - Enviar.
  - Registrar pago.

### 7.7 Recálculo de una factura ya emitida (decidido, Ola 1)

Un solo mecanismo (`RecalculateOpenPeriodAsync`) sirve para tres causas: camión tardío, TRM manual y ajuste CE-7. Reemplaza los períodos abiertos del depósito y sus líneas, y conserva las fechas del período.

| Estado de la factura | Qué pasa |
| --- | --- |
| Borrador o Pendiente de aprobación | Se recalcula. |
| Aprobada, Enviada, Vencida, Pago parcial o Pagada | Se actualiza la misma factura, conserva el N.º SIIGO y se notifica a Facturación con el total anterior y el nuevo. Con pagos: si queda saldo, pasa a `PartiallyPaid`; si no, a `Paid`, y la notificación informa el saldo a favor del cliente. |
| Anulada | No se toca; se notifica. |

Las líneas sobrescritas (override) se reemplazan, y la notificación lista el valor descartado.

### 7.8 Pagos

Estados: `Pending` → `Received` → `Verified`, o `Rejected`. El monto no puede superar el saldo pendiente. Métodos: efectivo, transferencia, cheque, tarjeta de crédito, tarjeta débito y otro. Se guardan la referencia, el número de recibo y las fechas de pago y de consignación.

### 7.9 Cartera y bloqueo por mora

Un job diario marca como `Overdue` las facturas vencidas y suma la deuda vencida por cliente. Si esa deuda supera el límite de crédito de su configuración, el cliente pasa a `Blocked`; si no, a `OverdueWarning`. **Un cliente sin límite de crédito nunca queda bloqueado automáticamente.**

Un cliente `Blocked` no puede (`BillingService.ValidateFinancialStatusAsync`):

- pagar báscula (ingreso, salida o solo báscula);
- cerrar un uso de montacargas;
- recibir mercancía sin báscula;
- generar órdenes de cargue;
- emitir guías de salida.

Otro job avisa de las facturas próximas a vencer.

### 7.10 Impuestos

`IVA` 19 % (`TaxKind.Added`, se suma al neto) y `RETE_FUENTE` 3 % (`Withholding`, se descuenta del pago y no suma a la factura). Un servicio lleva impuestos mediante `ServiceTax`. Sin `ServiceTax` la tasa es 0 y el IVA no se suma aunque la tarifa diga «más IVA». Para el montacargas, ver §5.8.

### 7.11 Jobs en segundo plano

Viven en `Backend/wms-api/Wms.Api/BackgroundJobs`:

| Job | Qué hace |
| --- | --- |
| `OverdueDetectionBackgroundService` | Marca las facturas vencidas y recalcula el estado financiero de los clientes. |
| `DailyChargeConsolidationBackgroundService` | Consolida los cargos del día de los clientes con facturación consolidada. |
| `StoragePeriodAutoCloseBackgroundService` | Cierra los períodos vencidos y renueva los de depósitos con stock. |
| `InvoiceDueNotificationBackgroundService` | Avisa de las facturas próximas a vencer. |

---

## 8. Notificaciones, auditoría y reportes

- **Notificaciones** en la app por rol (SignalR, persistidas en `notifications`); algunas también por correo (SMTP). Ejemplos:
  - Nuevo depósito de importación → Comercio Exterior.
  - Diferencia de recepción → Comercio Exterior (decidido; hoy va por correo al administrador).
  - Cargo al valor mínimo, TRM pendiente o factura recalculada → Facturación.
  - Ajuste de inventario → correos del parámetro `INVENTORY_ADJUSTMENT_ADMIN_EMAIL`.
- **Auditoría genérica:** toda entidad `IAuditable` registra altas, cambios y bajas en `audit_logs`, con usuario, IP y valores anterior y nuevo. Un criterio «queda auditado» se cumple con esto: no crees tablas de auditoría. El motivo de una corrección irá en `AuditLog.Description` mediante `IAuditContext`, que se crea en la Ola 1.
- **Trazabilidad por placa:** tablero que sigue cada camión por etapas (`app/features/traceability`).
- **Reportes** (`/reports`): mercancía que entra por día, mercancía que sale por día, estadísticas y movimientos por depósito (con PDF).

---

## 9. Documentos impresos

PDF generados con QuestPDF: tiquete de báscula, etiqueta del depósito, orden de cargue, guía de salida y factura. Las guías también se descargan en un ZIP por depósito, que registra cada impresión en `DispatchGuidePrintLog`. Las fechas se imprimen en hora de Colombia.

Los formatos originales del cliente están en `code_workspace/docs/cliente/formatos/`: `DEPOSITO INGRESO.pdf`, `GUIA DE SALIDA CEBOLLA.pdf`, `guia_salida.jpg`, `TIQUETE BASCULA OK.xlsx` y `TIQUETE BASCULA MEGA OK.jpg`.

---

## 10. Catálogos sembrados

| Catálogo | Valores |
| --- | --- |
| Roles del sistema | Administrador, Facturación, Comercio exterior, Operario vigilancia, Operario báscula, Operario bodega |
| Roles de negocio | `CUSTOMER`, `IMPORTER`, `EXPORTER`, `CUSTOMS_AGENCY`, `TRANSPORT_COMPANY` |
| Modalidades | `IMP001`, `EXP001`, `OTH001`, `INSP001` |
| Impuestos | `IVA` 19 %, `RETE_FUENTE` 3 % |
| Motivos de ingreso | Piden pesaje: descargue de importación, cargue de importación, cargue de exportación, descargue de exportación, solo báscula. No piden pesaje: solo bodega, otro. |
| Documentos de envío | Carta porte, manifiesto de carga, guía de transporte, declaración de importación, certificado fitosanitario, factura comercial, remisión, otros |
| Embalajes | `TANQUERO` (saldrá de embalajes con WMS-30) |
| Unidades de medida | Tractomula, tonelada, kg, unidad, bulto (solo por compatibilidad), litro, metro cúbico, caja, pallet, saco, quintal |
| Tipos de identificación | NIT, RUT, CC, pasaporte, RUC |
| Ubicaciones de bodega | Pasillo-rack-nivel (`A01-R01-N01`…) |
| Parámetros | `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` |

El administrador inicial lo crea `BootstrapAdminSeeder` al arrancar la API.

---

## 11. Arquitectura y convenciones técnicas

**Repositorios**, bajo `code_workspace/`:

- `Backend/wms-api` (git; ramas `main` y `develop`). .NET 10 (el README dice .NET 8, está desactualizado), ASP.NET Core, EF Core 10 con Npgsql (PostgreSQL, tablas en snake_case), MediatR 12 (CQRS: comandos y consultas por feature), FluentValidation, Identity con JWT y refresh tokens, SignalR, QuestPDF, xUnit.

  | Proyecto | Contenido |
  | --- | --- |
  | `Wms.Api` | Controladores `Controllers/v1`, jobs, identidad |
  | `Wms.Application` | Handlers, servicios y DTOs por feature |
  | `Wms.Domain` | Entidades con métodos de dominio, enums |
  | `Wms.Infrastructure` | `AppDbContext`, configuraciones, migraciones, servicios externos (`DianTrmService`) |
  | `Wms.Common` | Excepciones, paginación, `ColombiaTime` |
  | `Wms.Tests` | Pruebas xUnit |

- `Frontend/wms` (git; rama `develop`). Nuxt 4 como SPA (`ssr: false`), Vue 3.5, PrimeVue 4, Pinia 3, TanStack Vue Query 5, SignalR, VueUse y Tailwind 3. Las rutas están en `app/pages`; la lógica por dominio, en `app/features/<dominio>/` (services, composables, types, components). La base del API se configura con `NUXT_PUBLIC_API_BASE` (local: `http://localhost:5281/api/v1`).
- `code_workspace/docs/` y `code_workspace/docs/planes/` (sin git): documentación y planes.

**Convenciones:**

- Errores de negocio con `BadRequestException`, `ConflictException` y `NotFoundException`, con mensajes en español dirigidos al operario.
- Fechas de negocio con `ColombiaTime` (America/Bogota), nunca con `DateTimeOffset.UtcNow`. `UtcNow` sí se usa en `CreatedAt` y `UpdatedAt`.
- Paginación: `pageSize` se recorta en silencio a 50. Para traer todo (selects, catálogos) se envía `all=true`; nunca subas `pageSize`.
- **Las migraciones EF las genera el usuario.** El agente deja la entidad, la configuración y el `HasData`, sin tocar `Wms.Infrastructure/Migrations`, y lista los cambios de esquema. Las migraciones diferidas de julio ya están aplicadas (la última es `20260717214122_FixRolesCreatedAt`); los cambios de esquema de la Ola 1 aún no existen.
- La base de datos de pruebas se puede recrear: nada de backfills ni conversión de datos históricos.
- Frontend: `usePermissions` con import explícito (no auto-import); textos en español; tras cada mutación, invalidar el prefijo de la consulta (`['billing']`, `['foreign-trade']`…); búsquedas con `watchDebounced`.

**Ambientes:**

- **Staging en AWS Lightsail** (Docker Compose con Postgres, API y Caddy; frontend estático). Frontend `https://app.100-60-89-139.sslip.io`, API `https://api.100-60-89-139.sslip.io/api/v1`. Se despliega con `Backend/wms-api/scripts/deploy-staging.sh`; el runbook está en `Backend/wms-api/deploy/staging/README.md`.
- **Azure `test`** (README del backend): pendiente de darse de baja cuando el cliente valide staging.
- **Usuarios de prueba por rol:** en `Frontend/wms/README.md`. No copies contraseñas a otros documentos.

---

## 12. Estado del trabajo al 14-sep-2026

El backlog está en Linear, equipo **Wms**: WMS-5 a WMS-33, reescritos como historias de usuario (criterios BDD, subtareas, dudas) en `code_workspace/ajustes/historias-usuario-linear-2026-09-10.md`. **Antes de implementar un WMS-n, lee su historia ahí:** varios issues de Linear describen mal la causa, y estimar desde Linear lleva a construir cosas que ya existen.

| Ola | Racimo | Issues | Tema |
| --- | --- | --- | --- |
| 1 | R01 | WMS-9, WMS-26, WMS-24 | Stock declarado, varios camiones, TRM fuera de báscula |
| 1 | R02 | WMS-19, WMS-16 | Saldos de la guía, consecutivos |
| 1 | R03 | WMS-21, WMS-20, WMS-28, WMS-23 | Destinatario, acciones de factura, IVA del montacargas, conductor como destinatario |
| 1 | R04 | WMS-22, WMS-7 | Filtro y búsqueda de terceros |
| 2 | R05 | WMS-33, WMS-14, WMS-5 | Fechas operativas, planilla de envío, correcciones en Vigilancia |
| 2 | R06 | WMS-30, WMS-18, WMS-8, WMS-27 | Unidad de carga, embalaje frente a unidad, datos de recepción |
| 3 | R07 | WMS-31, WMS-10, WMS-6, WMS-25 | Báscula rápida (≤ 30 s) |
| 3 | R08 | WMS-12, WMS-11, WMS-15 | Etiqueta |
| 3 | R09 | WMS-17 | Orden de cargue simplificada |
| 3 | R10 | WMS-29, WMS-13 | Edición de productos del depósito, búsqueda multicriterio |
| 3 | R11 | WMS-32 | Tarifas mínimas de almacenamiento |

La Ola 2 depende de R01. La Ola 3 depende de R01, R05 y R06.

**Ola 1:** plan cerrado en `code_workspace/ajustes/plan-cerrado-ola-1-2026-09-14.md`, con las decisiones D01–D24, los archivos, los cambios de esquema, las pruebas y el orden de las ramas (`feature/ola1-r0N-…` desde `develop`). **Sin implementar.** Las respuestas del 14-sep mandan sobre las descripciones de Linear, y varias solo están en ese plan.

**Cambios de esquema que traerá la Ola 1** (migración a cargo del usuario): `document_sequences`, `dispatch_guide_lines`, `forklift_uses.apply_vat`, `service_records.truck_entries_closed_at` y `truck_entries_closed_by_id`, `warehouse_storages.trm_source` y `trm_date`, `invoice_items.storage_billing_period_id` y la extensión `unaccent`.

**Decisiones abiertas que cambian el alcance:**

- WMS-30: ¿la mercancía se declara por unidad de carga o por documento, para repartirla después?
- WMS-18 / WMS-27: ¿se imprime el embalaje, la unidad de medida o ambos?
- WMS-17: ¿la orden de cargue queda como registro interno invisible?
- WMS-32: ¿el mínimo de importación es $184.000 con 0,255 %? (El umbral de $72.156.863 coincide con $184.000 ÷ 0,255 %.) ¿El mínimo va antes o después de IVA?
- WMS-33: ¿el período de almacenamiento cuenta desde el ingreso o desde la confirmación?
- Almacenamiento prorrateado por saldo: falta confirmarlo con el cliente.

---

## 13. Lo que quedó obsoleto

No confíes en estas afirmaciones de documentos antiguos:

| Afirmación antigua | Dónde aparece | Realidad |
| --- | --- | --- |
| Estados del depósito `PENDING_RECEPTION`, `STORED`, `PARTIALLY_RESERVED`… | `documentos/INSTRUCCIONES_PROYECTO_BODEGAS.md` | `Draft`, `Confirmed`, `Closed`, `Cancelled` |
| El depósito se crea en el repesaje y el stock lo registra Bodega | Levantamiento, instrucciones, `code_workspace/docs/archivo/contexto-proyecto-wms.md` | El depósito se crea con el primer camión en báscula; el stock sale de lo declarado (decidido) |
| Confirmar exige la recepción completada | Plan E2E de julio | Revertido por la premisa 2 |
| Facturación crea facturas a mano en tres pasos | `code_workspace/docs/manuales/manual-modulo-facturacion.md` | No hay creación manual; el sistema genera las facturas |
| Períodos «Abierto / Cerrado / Facturado» con «tarifa diaria» | El mismo manual | `Open` / `Closed`; cobro por fórmula y por cargo |
| Los convenios solo tienen un precio fijo por producto (`AgreementPrice`) | `code_workspace/docs/archivo/contexto-proyecto-wms.md` | `AgreementService` + parámetros con fórmulas; los servicios están separados de los productos (`Service`) |
| La tarifa de báscula se configura en el producto `SRV-BASCULA` | `docs/manuales/MANUAL_OPERACION_INGRESOS_Y_BASCULA.md` | Se configura en el servicio `BASCULA` |
| La orden de cargue exige un solo cliente | `code_workspace/docs/archivo/contexto-proyecto-wms.md` | Multi-cliente desde CE-12 |
| La TRM se toma en báscula | Código actual | Sale de báscula (decidido) |
| Depósitos `DEP-IMP-AAAA-####` | Código actual | `2026BA00001` (decidido) |
| Roles `INTERMEDIARY` o `SIA` | Varios | `CUSTOMS_AGENCY` |
| .NET 8 | README del backend | .NET 10 |

---

## 14. Trampas conocidas

1. Con la Ola 1, `ReceivedQuantity` cambia de significado (cantidad del depósito = declarada + ajustes). No la renombres ni cambies a sus consumidores.
2. `PERCENTAGE_OF_VALUE` no se multiplica por el stock. Si marcas la fórmula prorrateada como «por cantidad», reintroduces el doble conteo.
3. El esquema de parámetros sembrado de una fórmula y su calculador pueden divergir (pasó con `PER_UOM`). Coteja ambos al tocar un calculador.
4. Sin `ServiceTax`, el IVA no se suma. `RETE_FUENTE` es una retención: no la sumes como si fuera IVA.
5. `[Authorize]` es aditivo. Un 403 de un rol operativo suele venir de un servicio compartido que otro módulo importa (`app/features/weighbridge`, `app/features/entries`), no de una llamada directa del módulo.
6. `pageSize > 50` se recorta sin avisar: usa `all=true`. Con `all=true`, `PageSize` vale `int.MaxValue`, así que no lo uses para aritmética ni para reservar memoria.
7. Antes de mejorar una pantalla, comprueba que una ronda anterior no la haya retirado (pasó con la creación manual de facturas).
8. Verifica el componente y también quién lo instancia: las props declaradas no dicen qué le pasa el padre.
9. No conviertas una carencia del modelo de datos en una prohibición de negocio.
10. `ServiceRecord.CargoManifestNumber` es la carta porte, no el manifiesto.

---

## 15. Cómo trabajar en este proyecto

- Escribe en español: el usuario, los operarios y los mensajes del sistema lo están.
- Para implementar issues, entrega primero un **plan cerrado y sin ambigüedades** en `code_workspace/docs/planes/`: cada duda resuelta con su fuente, más archivos, cambios de esquema, pruebas y orden. Junta las preguntas pendientes en un solo mensaje y espera la aprobación antes de tocar código.
- No generes migraciones EF: lista los cambios de esquema para que el usuario las genere.
- Si una historia de Linear contradice una premisa o una decisión de este documento, gana la premisa o la decisión. Si la duda persiste, pregunta.
- Las ramas de trabajo salen de `develop`.

---

## 16. Mapa de fuentes

| Tema | Archivo |
| --- | --- |
| Plan cerrado de la Ola 1 | `code_workspace/ajustes/plan-cerrado-ola-1-2026-09-14.md` |
| Historias del backlog | `code_workspace/ajustes/historias-usuario-linear-2026-09-10.md` |
| Triage técnico previo | `code_workspace/ajustes/triage-incidentes-linear-2026-09-02.md` |
| Contexto técnico de abril (modelo de datos, flujo de depósitos) | `code_workspace/docs/archivo/contexto-proyecto-wms.md` |
| Diagramas de secuencia del negocio | `diagramas/importacion.mmd`, `diagramas/exportacion.mmd`, `diagramas/facturacion_v1.mmd` |
| Levantamiento con el cliente | `documentos/Resumen levantamiento.docx`, `documentos/Contexto proyecto bodegas.docx`, `documentos/Especificación de requerimientos.docx`, `documentos/INSTRUCCIONES_PROYECTO_BODEGAS.md` |
| Manuales de usuario | `code_workspace/docs/manuales/Manual_Usuario_WMS.pdf`, `code_workspace/docs/manuales/MANUAL_OPERACION_INGRESOS_Y_BASCULA.md`, `code_workspace/docs/manuales/manual-modulo-facturacion.md` (desactualizado) |
| Formatos impresos del cliente | `code_workspace/docs/cliente/formatos/` |
| Staging | `code_workspace/Backend/wms-api/deploy/staging/README.md` |
