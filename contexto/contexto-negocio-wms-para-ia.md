# Contexto del negocio — WMS Bodegas Asociadas

> **Para qué sirve:** darle a un agente sin historial el negocio, el vocabulario y las reglas que el sistema implementa hoy, antes de proponer o tocar código.
> **Fecha de corte:** 2026-10-23. Verificado contra el código de backend `develop` `35a61b2` y frontend `develop` `c924a8b`. Reemplaza la versión del 14-sep-2026, que se conserva en el historial de git de este repo.
> **Rutas:** relativas a `code_workspace/`.
> **Idioma:** el negocio, la UI, los mensajes de error y la documentación están en español; el código, en inglés.

---

## 0. Cómo leer este documento

Este documento describe **qué hace el sistema y por qué**. Lo complementan:

| Documento | Contenido |
| --- | --- |
| `contexto/decisiones.md` | Decisiones vigentes del usuario y del negocio (`DEC-nnn`). Mandan sobre este documento si difieren |
| `contexto/estado.md` | Qué está hecho, qué hay en staging, qué está pendiente y qué decisiones siguen abiertas |
| `contexto/convenciones-tecnicas.md` | Stack, arquitectura, permisos, migraciones, pruebas y trampas técnicas |
| `contexto/mapa-de-fuentes.md` | Dónde está cada cosa |

La precedencia de las fuentes está en `README.md` del hub. Si este documento y el código difieren, el código dice qué pasa hoy y `contexto/decisiones.md` dice qué debe pasar: pregunta antes de «corregir» cualquiera de los dos.

---

## 1. El negocio en una página

**Bodegas Asociadas** opera una bodega en **Ipiales (Nariño, Colombia)**, junto al paso fronterizo de **Rumichaca** con Ecuador. La DIAN la habilita como **depósito público aduanero**: la mercancía que cruza la frontera se queda ahí mientras se tramita su nacionalización, su exportación o su inspección.

| Servicio | Qué pasa |
| --- | --- |
| Importación | Un camión del exterior deja mercancía que espera el levante de la DIAN (nacionalización). Sale completa o por partes cuando el cliente la pide. |
| Exportación | Mercancía nacional espera para salir del país. Puede descargarse o quedarse en el vehículo o la unidad de carga. |
| Inspección | La mercancía permanece hasta que la DIAN la inspecciona. |
| Otros (solo báscula) | El camión solo se pesa y sale. |

La bodega cobra **báscula**, **montacargas**, **guía de salida** y **almacenamiento**. Los tres primeros son de contado, o quedan «pendientes por facturar» para una factura consolidada. El almacenamiento es a crédito, por períodos y por depósito, según los convenios con cada cliente.

El WMS reemplaza al sistema legacy «Bodegas» (PHP), del que ya se migraron los datos a staging, y a una bitácora manual en portería. El legacy pesa un camión en ~30 s: esa es la meta de velocidad de la báscula. **El WMS no emite factura electrónica:** la factura legal se hace en **SIIGO** y Facturación copia su número en el WMS.

La mercancía típica son perecederos (p. ej. cebolla), líquidos en tanqueros y carga en contenedores. Hay terceros y vehículos colombianos y ecuatorianos: existe el tipo de identificación RUC y se registra el país del vehículo. Monedas: COP y USD.

---

## 2. Glosario

| Término | Significado | En el código |
| --- | --- | --- |
| **Depósito** | Lote de mercancía amparado por un mismo documento de ingreso (carta porte) y una modalidad. Es la unidad de inventario, de etiqueta y de cobro de almacenamiento. Puede llegar en varios camiones y tener varios productos. | `WarehouseStorage` |
| **Carta porte** | Documento de transporte internacional que ampara la carga. Carta porte + modalidad = un depósito. | `ServiceRecord.CargoManifestNumber` (el nombre engaña: es la carta porte) |
| **Manifiesto de carga** | Documento aduanero de cada camión. Comercio Exterior registra su número y su peso antes de confirmar. | `UpdateTruckManifest`; `ImportWarehouseStorage.ManifestNumber` |
| **Unidad de carga** | Contenedor, tanquero o remolque que entra con el camión. Se anotan su tipo y su placa; Bodega la recibe completa sin contar producto por producto; puede salir parcialmente. | `WarehouseStorageCargoUnit`, `WarehouseStorageCargoUnitProduct`, catálogo `CargoUnitType` |
| **Modo de carga** | Si el depósito es de mercancía suelta o de unidades de carga. Lo fija el primer camión; no se mezclan. | `WarehouseStorage.CargoHandling` (`LooseGoods`, `CargoUnits`) |
| **Levante** | Autorización de la DIAN para disponer de la mercancía importada, por producto. Lleva FOB en USD, tasa y FOB en COP. Se puede retirar. Comercio Exterior lo consulta en **MUISCA** (sin integración). | `ImportRelease` |
| **Nacionalizado** | Estado de la importación cuando tiene **al menos un levante**. El despacho de cada producto no puede superar lo nacionalizado. | `ImportLabelsStatus` |
| **Prórroga / abandono** | El depósito de importación cae en abandono a los 30 días sin prórroga, o a los 60 con ella; la alerta sale 10 días antes. La prórroga se registra una sola vez. | `AbandonmentCalculator`, `AbandonmentAlertBackgroundService` |
| **Etiqueta** | Rótulo de la mercancía. Importación: «SIN NACIONALIZAR» y luego «NACIONALIZADO». Exportación: cantidad o peso. Se reimprime cuando cambia la cantidad; se cuentan las impresiones. | `LabelGenerationService`, `WarehouseStorageLabelPrint` |
| **Tiquete de báscula** | Comprobante del pesaje. | `WeighbridgeCycle` |
| **Peso bruto / tara / neto** | Camión cargado / vacío / diferencia. Báscula captura un único peso bruto del manifiesto; no hay pesos por producto. | `TypeWeight` |
| **Orden de cargue (OC)** | Autorización interna para retirar mercancía de uno o varios depósitos, de uno o varios clientes. Registra la orden externa del cliente y reserva el stock. | `LoadingOrder`, `LoadingOrderItem`, `WarehouseReserve` |
| **Guía de salida** | Documento que acompaña la salida. Congela por línea la entrada, el saldo anterior, lo despachado y el nuevo saldo. Se cobra. | `DispatchGuide`, `DispatchGuideLine` |
| **Novedad** | Hallazgo de Bodega sobre la mercancía (daño, faltante…), con desglose e impresión («Reporte de mercancías»). | `WarehouseNovelty` |
| **Ubicación por cantidades** | Bodega ubica, mueve y libera cantidades de un producto en ubicaciones `A01-R01-N01`. | `WarehouseStorageProductPlacement` |
| **Lista de empaque** | Detalle del cliente que se importa y se asocia a los productos del depósito. | `PackingList*` |
| **Cuadrilla** | Grupo de cargue o descargue. | `Crew` |
| **Montacargas** | Servicio de descargue o cargue, con horómetro inicial y final y el camión con el que se inicia. | `ForkliftUse`, `ForkliftRate` |
| **TRM** | Tasa representativa del mercado (COP por USD), de la DIAN o manual. | `WarehouseStorage.Trm`, `TrmSource`, `TrmDate` |
| **Valor de la mercancía** | Valor del ingreso, equivalente al FOB (`DEC-029`); base de las tarifas por porcentaje. El código y algunos textos aún lo llaman «CIF». | `WarehouseStorage.CargoValue` + `Currency` |
| **Tercero** | Persona o empresa con uno o varios roles de negocio. | `Stakeholder`, `StakeholderBusinessRole` |
| **Agencia de aduanas = SIA = intermediario** | Un solo rol de negocio, código `CUSTOMS_AGENCY`. Un `"SIA"` o `"INTERMEDIARY"` en el código es un bug. | `BusinessRole` |
| **Convenio** | Tarifas pactadas con un cliente por servicio, producto, modalidad y perecedero, con fórmulas. | `Agreement` → `AgreementService` + `AgreementParameter` |
| **Tarifa base** | Tarifa por defecto de un servicio cuando no hay convenio. | `ServicePricingRule` + `ServicePricingRuleParameter` |
| **Valor mínimo** | Piso de cobro por servicio y modalidad; respaldo del almacenamiento. Puede incluir o no el IVA. | `ServiceMinimumValue`, parámetro `minimumIncludesVat` |
| **N.º SIIGO** | Número de la factura legal emitida en SIIGO. | `Invoice.InvoiceNumber` (nulable) |
| **Consumidor final** | Destinatario genérico, identificación `222222222222`. | `InvoiceRecipient` |
| **CE-7** | Ajuste de la cantidad de un depósito por Comercio Exterior. | `AdjustInventoryCommand` |
| **Depósito migrado** | Depósito vivo importado del legacy, con su número antiguo. | `IsMigrated`, `LegacyNumber` |
| **Datos de práctica / QA** | Datos de staging creados para operarios (`PRAC-`) o por QA (`QA-…`, placas `QS…`). | — |

**Siglas en comentarios, planes y commits:**

| Sigla | Significado |
| --- | --- |
| `WMS-n` | Issue de Linear |
| `CE-n`, `FAC-n` | Requerimientos de Comercio Exterior y de facturación |
| `ALM-n` | Hallazgos del análisis de almacenamiento |
| `F1-xx`…`F6-xx`, `P1`…`P17`, `DF1`… | Ítems y decisiones de los planes de paridad |
| `C-Fx-yy` | Endpoints del contrato de paridad |
| `CHG-nn` | Cambios del plan de corrección QA |
| `DEF-*` | Fichas de defecto |
| `Dn`, `D-n` | Decisión de un plan. **La numeración se reinicia en cada plan:** `D4` significa algo distinto según el documento |
| `DEC-nnn` | Decisiones vigentes de `contexto/decisiones.md` |
| `R01`–`R11`, Ola 1–3 | Racimos y olas del backlog de septiembre |

---

## 3. Actores y módulos

| Rol (código) | Nombre en la UI | Módulo · ruta | Responsabilidad |
| --- | --- | --- | --- |
| `Receiving` | Operario vigilancia | Vigilancia · `/operations/entries`, `/exits`, `/history` | Registra el ingreso y la salida de vehículos con captura mínima. Su hora de ingreso es la fecha de ingreso del depósito. Corrige sus propios registros. |
| `Scale` | Operario báscula | Báscula · `/operations/weighbridge` | Toma el camión de la cola, registra documento, productos y cantidades declaradas, cobra, pesa e imprime el tiquete. Repesajes, recuperar operaciones, historial. |
| `Warehouse` | Operario bodega | Bodega · `/warehouse` | Recepción informativa, ubicación por cantidades, montacargas, novedades, verificación y ejecución de órdenes de cargue, inventario. |
| `ForeignTrade` | Comercio exterior | `/foreign-trade` | Dueño del depósito: completa datos, confirma, ajusta cantidades (CE-7), etiquetas, levantes, prórroga y abandono, listas de empaque, órdenes de cargue y guías, cierra el ingreso de camiones. |
| `Billing` | Facturación | `/billing` | Facturas, N.º SIIGO, aprobación, pagos, TRM manual, configuración de facturación por cliente, depósitos pendientes por facturar, reportes de facturación. |
| `Admin` | Administrador | `/admin` | Todo, más los catálogos: terceros, productos, servicios y tarifas, usuarios, ubicaciones, embalajes, unidades de medida, tipos de unidad de carga, ciudades, cuadrillas, conductores, vehículos, motivos de ingreso, tarifas de montacargas, parámetros y auditoría. Respaldos e importación legacy, solo por API. |

- Un usuario puede tener varios roles.
- Reportes en `/reports`; notificaciones en `/notifications`; trazabilidad por placa en `/` (Admin y Comercio Exterior).
- El centro de ayuda con los video tutoriales está en `/ayuda` y se abre sin sesión.
- Las políticas del API por rol están en `contexto/convenciones-tecnicas.md` §4.

---

## 4. Modalidades de operación

| Código | Nombre | ¿Crea depósito? | Particularidades |
| --- | --- | --- | --- |
| `IMP001` | Importación | Sí, más `ImportWarehouseStorage` | Etiquetas SIN NACIONALIZAR → NACIONALIZADO; levantes por producto; tope de despacho por lo nacionalizado; prórroga y abandono; la guía se entrega al conductor. |
| `EXP001` | Exportación | Sí | Puede quedarse en el vehículo o la unidad de carga; la etiqueta lleva la cantidad o el peso. |
| `INSP001` | Depósito por inspección | Sí | Un solo pesaje, con primer peso bruto forzado. |
| `OTH001` | Otros | No | Solo báscula: un pesaje, cobro y tiquete. |

El código detecta la modalidad por prefijo (`IMP*`, `EXP*`, `INSP*`). En las tarifas, «tipo de depósito» es esta misma dimensión (`OperationModality`).

---

## 5. Flujos operativos

### 5.0 Premisas

Las cuatro premisas de las pruebas con operarios (10-sep-2026) rigen todo diseño (`DEC-010`):

1. Báscula rápida (~30 s).
2. Las cantidades del depósito son las declaradas en báscula.
3. La unidad de carga es un concepto propio.
4. Las fechas son editables.

No propongas diseños que hagan esperar a Comercio Exterior por Bodega, ni que cuenten producto por producto dentro de unidades de carga.

### 5.1 Ingreso con depósito (importación, exportación, inspección)

1. **Vigilancia** registra el ingreso: placa (si no existe, se crea el vehículo) y motivo. Un vehículo no puede tener dos ingresos abiertos. Queda un `EntryLog` con `DateTimeEntry`.
2. **Báscula** toma el camión de la **cola** (pantalla única) y registra el ingreso con depósito en un solo paso (`RegisterStorageEntry` → `InitiateStorageWeighing`). Captura:
   - carta porte, modalidad, vehículo, país del vehículo y conductor (con el selector, `DEC-017`);
   - por producto: cantidad declarada, embalaje y unidad de medida;
   - un peso bruto del manifiesto;
   - las unidades de carga, si las hay.

   El producto se puede escribir como descripción libre: si no existe, báscula lo crea y avisa a Comercio Exterior. Cliente, terceros documentales, moneda, valor y fecha del documento son **opcionales en báscula** y se exigen al confirmar.
   - **Primer camión con esa carta porte:** crea el `ServiceRecord` (tipo `Input`), el `WarehouseStorage` en `Draft` y, si es importación, el `ImportWarehouseStorage`. **La cantidad declarada entra al stock** con un movimiento `DeclaredEntry`. Notifica a Comercio Exterior.
   - **Camión adicional con la misma carta porte y modalidad:** reutiliza servicio y depósito, crea otra `WarehouseStorageEntry` y suma su cantidad declarada al stock. Báscula muestra «Camiones ingresados: N». Con una modalidad distinta para el mismo documento, el sistema responde con error.
   - Un mismo camión puede traer mercancía de **varios depósitos** (depósito adicional).
3. **Cobro de báscula**, antes de pesar: inmediato (factura y pago en el acto) o «pendiente por facturar». Valida que el cliente no esté bloqueado por mora.
4. **Pesajes:** primer peso bruto; tara cuando el camión vuelve; neto = bruto − tara; tiquete. Inspección: un solo pesaje. Corregir un peso o su fecha exige `WeighingCorrectionAccess` y avisa al administrador. Un pesaje se puede **anular**; si el depósito queda sin camiones, se anula.
5. **Bodega** registra la recepción, que es **informativa**: cantidad contada por producto, fotos, ubicación y montacargas si aplica. La recepción no mueve stock, no fija fechas y no factura. Si lo contado difiere de lo declarado para ese camión, avisa en la app a Comercio Exterior, que corrige con CE-7 si corresponde. Las unidades de carga se reciben completas, sin conteo. Funciona con el depósito en Borrador o Confirmado.
6. **Comercio Exterior**, en el detalle del depósito:
   - **Completa** lo que báscula dejó pendiente: cliente, fecha del documento, importador y agencia de aduanas (IMP) o exportador (EXP), moneda y valor mayor que 0, número y peso del manifiesto de cada camión y, con varias unidades de carga, el reparto de la mercancía por unidad.
   - **Confirma** (`Draft → Confirmed`). En la misma transacción se abre el primer período de almacenamiento con su factura (§7.4).
   - Imprime la etiqueta y, cuando ya no llegarán más camiones, **cierra el ingreso de camiones** (sin reapertura).
7. **Vigilancia** registra la salida.

### 5.2 Varios camiones con la misma carta porte

- Completar el ciclo de un camión no cierra el servicio.
- Después de «Cerrar ingreso de camiones», báscula no asocia más camiones y el error dice quién cerró y cuándo.
- Un **camión tardío** en un depósito confirmado suma su cantidad al stock, recalcula la factura del período (§7.7) y avisa a Comercio Exterior para reimprimir la etiqueta. Un error de facturación nunca bloquea báscula.

### 5.3 Salida de importación

1. El cliente pide la salida (normalmente por correo), parcial o total.
2. **Comercio Exterior** crea la **orden de cargue**:
   - **Qué registra:** la orden externa del cliente (número, emisor, fecha y soporte opcional) y la ciudad de destino, que es obligatoria.
   - **Alcance:** uno o varios depósitos, de uno o varios clientes.
   - **Validaciones:** depósito confirmado, mercancía nacionalizada, que lo pedido no supere lo nacionalizado por producto, stock disponible y cliente no bloqueado.
   - **Efecto:** reserva el stock. La orden **ya no emite PDF**; Bodega conserva su impresión de trabajo. Con unidades de carga, cada ítem apunta a una unidad.
3. El conductor entra por Vigilancia. En **báscula**, «Salida de mercancía»: tara y cobro.
   - Con el mismo pesaje se pueden sacar **órdenes adicionales**, sin cobro adicional.
   - También existe la salida con el tiquete de ingreso.
4. **Bodega** verifica la orden y carga. El stock se descuenta por producto y quedan movimientos de inventario. Una unidad de carga pasa a `PartiallyDispatched` o `Dispatched`.
5. **Comercio Exterior** emite la **guía de salida** (servicio `GUIA_SALIDA`, que se cobra; su modo de pago se puede cambiar) y la entrega al conductor.
   - Las líneas de la guía congelan la entrada, el saldo anterior, lo despachado y el nuevo saldo. Saldo anterior = cantidad del depósito − lo despachado en guías emitidas antes.
   - Si queda saldo, reimprime la etiqueta.
6. **Repesaje** del camión cargado: responde 409 mientras alguna orden del camión no esté cargada. Después, salida por Vigilancia.
7. Cuando ningún producto tiene stock, el depósito pasa a `Closed` y sus períodos se cierran. Revertir una salida puede devolverlo a `Confirmed`.

Correcciones de salida: modificar, cancelar (con motivo) o revertir una orden; anular una guía (con motivo).

### 5.4 Exportación

Como la importación, pero la mercancía puede quedarse en el vehículo o la unidad de carga. La etiqueta lleva la cantidad o el peso. En la salida, Comercio Exterior genera la orden; Bodega verifica y carga; la guía se genera sin entregarse al conductor.

### 5.5 Inspección

Depósito normal con un solo pesaje (primer peso bruto forzado). La mercancía queda hasta que la DIAN la inspecciona.

### 5.6 Solo báscula (`OTH001`)

Un pesaje, cobro y tiquete, sin depósito.

### 5.7 Recepción sin báscula

Si el camión no pasa por báscula (motivo «Solo bodega»), Bodega crea el depósito desde la recepción, en Borrador, con cantidades declaradas manuales (`CreateReceptionWithoutWeighbridge`).

### 5.8 Montacargas

- Bodega inicia el uso con el horómetro y el camión; puede empezar antes de que Comercio Exterior asigne el cliente.
- Al finalizar se cobra. La tarifa depende del tipo de vehículo (tractomula, doble troque, sencillo, turbo, guacal/estiba) y el valor es editable.
- El servicio no lleva impuestos configurados: el check «Agregar IVA», desmarcado por defecto, suma el IVA sobre el valor digitado (`DEC-018`).

### 5.9 Control aduanero (importación)

- Levantes por producto, con FOB en USD, tasa y FOB en COP congelados. Se pueden retirar.
- Prórroga, una sola vez. Abandono a los 30 o 60 días, con alerta diaria (07:00) 10 días antes y página `/foreign-trade/abandonment`.
- Catálogo de ciudades con días de tránsito y marca de destino de abandono; el vencimiento de la guía se calcula a partir de ellos.

### 5.10 Bodega y mercancía

- **Ubicación:** por cantidades (ubicar, mover, liberar).
- **Novedades:** con desglose, impresión y anulación.
- **Listas de empaque:** se importan y se asocian a los productos.
- **Cuadrillas.**
- **Etiquetas:** se registra cada impresión.

### 5.11 Correcciones y anulaciones

| Acción | Condición |
| --- | --- |
| Editar productos del depósito (WMS-29) | Solo en Borrador. Se puede eliminar un producto declarado sin otros movimientos |
| Volver a Borrador (`MarkForCorrection`) | Se rechaza si el depósito tiene órdenes activas |
| Corregir la fecha de ingreso | En Borrador o Confirmado. Recalcula el período y borra la TRM de la DIAN si cambia el día |
| Anular un depósito, una guía o un pesaje | Con motivo de 10 a 500 caracteres; deshace todos sus efectos |

Para perecederos existe una guía global por depósito.

### 5.12 Operaciones incompletas

Báscula puede retomar o descartar una operación a medias desde `/operations/weighbridge/recover`. Al descartar, el camión se libera y la trazabilidad la muestra como «Cancelado».

### 5.13 Destinatario del cobro

Puede ser un tercero registrado, una persona no registrada (basta su cédula; los datos del conductor se precargan) o el consumidor final.

---

## 6. El depósito en detalle

```
ServiceRecord (Input: carta porte, modalidad, terceros documentales, cierre de ingreso de camiones)
 └─ WarehouseStorage (número, estado, modo de carga, CIF, moneda, TRM y su origen, fecha de ingreso, cliente)
     ├─ WarehouseStorageProduct            por producto: declarado, cantidad del depósito, stock,
     │   └─ WarehouseStorageProductPlacement   reservado, disponible, embalaje, unidad; ubicaciones
     ├─ WarehouseStorageEntry              una fila por camión (EntryLog, ciclo de báscula, manifiesto)
     │   └─ WarehouseStorageEntryProduct       declarado por producto en ese camión
     ├─ WarehouseStorageCargoUnit          unidades de carga (tipo, placa, estado)
     │   └─ WarehouseStorageCargoUnitProduct   mercancía de cada unidad
     ├─ ReceptionLog → ReceptionLogProduct conteo informativo de Bodega
     ├─ WarehouseNovelty                   novedades
     ├─ PackingList                        listas de empaque
     └─ ImportWarehouseStorage             solo IMP: etiquetas, manifiesto, levantes, prórroga, abandono
```

`ServiceRecord` y `EntryLog` se relacionan N:M (`service_record_entry_logs`).

**Estados** (`WarehouseStorageStatus`):

| Estado | Significado |
| --- | --- |
| `Draft` | Inicial y editable. Admite recepciones. |
| `Confirmed` | Confirmado por Comercio Exterior. Admite recepciones, reservas y despachos. `MarkForCorrection` lo devuelve a `Draft` si no hay órdenes activas. |
| `Closed` | Todos los productos con `CurrentStock = 0`. Una reversión de salida lo devuelve a `Confirmed`. |
| `Cancelled` | Anulado con motivo. |

- Órdenes de cargue y guías rechazan depósitos en `Draft`.
- **Stock por producto:** `AvailableStock = CurrentStock − ReservedStock`, nunca negativo. La orden reserva; el despacho descuenta `CurrentStock` y libera la reserva. `ReceivedQuantity` significa «cantidad del depósito» (declarada + ajustes CE-7), no «lo que contó Bodega»: no la renombres.
- **Fecha de ingreso** (`EntryDate`): la que elige el operario o, por defecto, el `DateTimeEntry` de Vigilancia del primer camión. Los siguientes no la cambian. Rige la etiqueta, la fecha de la TRM, el año del consecutivo y el inicio del primer período de almacenamiento (`DEC-012`).

**Numeración** (`DocumentNumberFormat`, tabla `document_sequences` con `SELECT … FOR UPDATE` en la transacción del documento, año de Colombia, 5 dígitos, sin saltos):

| Documento | Formato | Año |
| --- | --- | --- |
| Depósito de importación | `2026BA00001` | Fecha de ingreso |
| Depósito de exportación | `2026EXP00001` | Fecha de ingreso |
| Depósito por inspección | `2026INSP00001` | Fecha de ingreso |
| Tiquete de báscula | `2026T00001` | Fecha de referencia del pesaje |
| Guía de salida | `2026S00001` (una serie para todas) | Emisión |
| Orden de cargue | `2026OC00001` | Emisión |

`OTH001` no tiene serie de depósito. Los depósitos migrados conservan su número del legacy en `LegacyNumber`.

---

## 7. Facturación

### 7.1 Modelo

| Servicio | Cuándo nace el cargo | Cómo se cobra |
| --- | --- | --- |
| `BASCULA` | En el cobro de báscula, antes de pesar | Contado (factura y pago) o pendiente por facturar |
| `MONTACARGAS` | Al finalizar el uso | Igual que báscula |
| `GUIA_SALIDA` | Al emitir la guía | Igual que báscula |
| `PAPELERIA` | Sembrado («Papelería / Software / Comunicaciones»), sin flujo que lo cobre todavía | — |
| `ALMACENAMIENTO` | Al confirmar el depósito y en cada renovación del período | Crédito: una factura por depósito, o la consolidada del cliente |

`ServicePaymentMode`: `Immediate` (factura y pago al registrar) o `PendingBilling` (el cargo espera la consolidación). Los cobros pendientes de báscula y montacargas **no se consolidan** (`DEC-019`).

**No existe creación manual de facturas** (`DEC-021`). Para corregir un valor se sobrescribe una línea con un override (`POST billing/invoice-items/{id}/override`), solo en Borrador y una vez por línea.

### 7.2 Configuración de facturación por cliente

`StakeholderBillingConfiguration`:

- **Ciclo** (`BillingCycleCatalog`):
  - Semanal (7 días)
  - Quincenal (14 días)
  - Quincenal (15 días)
  - Mensual (mes calendario)
  - Mensual (30 días)
  - Trimestral (90 días)
  - Semestral (180 días)
  - Anual (360 días)

  `OnDemand` está retirado: solo se lee en configuraciones antiguas. Sin configuración, se usa el mensual.
- **Plazo** (días), **límite de crédito** (opcional) y **si está activa**.
- **Preferencia:** `Consolidated` o `PerService`. `PerWeighbridgeCycle` está retirado y se comporta como `PerService`.

### 7.3 Resolución de tarifa

Vive en `Backend/wms-api/Wms.Application/Billing/Services/BillingResolver.cs`. Gana el primer nivel con regla:

1. **Convenio del cliente** (`AgreementService` activo).
2. **Tarifa base** del servicio (`ServicePricingRule`).
3. **Precio base vigente** del servicio (`ServicePrice`, código interno `BASE_PRICE`).
4. **Sin tarifa:** error, salvo en almacenamiento, que cae al valor mínimo (§7.4).

En los niveles 1 y 2, la escalera de especificidad (`RuleSpecificity`) filtra primero por **perecedero** (coincidencia exacta, luego genérica). Después recorre producto + modalidad → producto → modalidad → ninguno. Dentro de un peldaño gana el más reciente. Sin cliente (`Guid.Empty`) se omite el nivel 1. El cálculo es uno solo (`FormulaPricing.Price`).

**Fórmulas** (`FormulaType`, 8 sembradas):

| Código | Qué cobra |
| --- | --- |
| `FIXED` | Valor fijo; admite tarifas «IVA incluido». |
| `PERCENTAGE_OF_VALUE` | Un % del CIF en pesos, con `minimum` y `minimumThreshold`. **No se multiplica por el stock.** |
| `PERCENTAGE_OF_VALUE_PRORATED` | Un % de `CIF × CurrentStock / ReceivedQuantity`; base plana; el mínimo no se prorratea. Convive con la anterior hasta que el cliente decida (`DEC-025`). |
| `PER_UOM` | Valor × cantidad en una unidad de medida; el parámetro `uom` debe coincidir con la de los productos. |
| `PER_VEHICLE` | Valor × vehículos del depósito. |
| `PER_CARGO_UNIT` | Valor × unidades de carga de un tipo (contenedor, tanquero…). |
| `WEIGHT_THRESHOLD` | Para perecederos (WMS-32): bajo el umbral cobra un mínimo; desde el umbral, por kilo. El peso es el bruto declarado del depósito (suma de los manifiestos). |
| `PER_VEHICLE_TYPE` | Solo montacargas: tarifa por tipo de vehículo. |

- `ALMACENAMIENTO` admite todas salvo `PER_VEHICLE_TYPE`.
- El parámetro `minimumIncludesVat` indica si el mínimo incluye IVA; por defecto se lee como incluido.

### 7.4 Almacenamiento

- **Unidad de trabajo: el depósito.** Los productos con stock se agrupan por la regla que les resuelve; cada grupo es un cargo con su `StorageBillingPeriod` y sus productos en `StorageBillingPeriodProduct`. La factura es una por depósito (o la consolidada), con una línea por cargo.
- **Magnitudes del depósito** (CIF, unidades de carga, vehículos): se cobran una sola vez. El CIF de un grupo se prorratea por `ReceivedQuantity`.
- **La factura siempre se genera** (`DEC-020`). Sin regla, o si la regla falla, el cargo usa el valor mínimo de la modalidad. Los mínimos sembrados son $0; los reales se configuran. La advertencia va al `Detail` de la factura (máx. 1000 caracteres) y a una notificación para Facturación.
- **Período:**
  - El primero se abre **solo al confirmar**, y empieza en la **fecha de ingreso** en Colombia, nunca en el futuro.
  - Fin = inicio + N días del ciclo (o un mes en el mensual). La renovación ocurre al día siguiente de la fecha límite (fin + 3). El siguiente período empieza en fin + 1.
- **Qué cobra cada período:**
  - El primero cobra la cantidad total.
  - Las renovaciones cobran el saldo en las fórmulas por cantidad y en la prorrateada. `PERCENTAGE_OF_VALUE` cobra el CIF completo en cada renovación.
  - El período se cobra por adelantado.
- **Renovación y cierre:** el job cierra los períodos vencidos y renueva los de depósitos con stock. Se puede cerrar a mano y refacturar.

### 7.5 TRM

Aplica cuando la moneda del depósito no es COP (`DEC-023`).

- Báscula no consulta la TRM.
- Se consulta a la DIAN al abrir el período (confirmación y renovaciones), con la fecha de ingreso y una espera máxima de 3 s.
- **Si falla:** el depósito queda con **TRM pendiente** y la factura sale con el mínimo y la leyenda «TRM PENDIENTE».
- **TRM manual:** la registra Facturación o el Admin (`PUT billing/warehouse-storages/{id}/trm`), con motivo de 10 a 500 caracteres y antes de aprobar la factura. Recalcula la factura.
- Mientras falte la TRM, no se asigna el N.º SIIGO ni se aprueba.
- Se guardan el origen (`Dian` o `Manual`) y la fecha. Ninguna reemplaza a la otra.

### 7.6 Facturas

Estados: `Draft` → `PendingApproval` → `Approved` → `Sent` → `PartiallyPaid` / `Paid`. El job marca `Overdue`; `Cancelled` exige motivo.

- **Vencimiento:** se fija al aprobar.
- **N.º SIIGO:**
  - Sin número, se asigna en cualquier estado salvo Anulada.
  - Con número, solo se cambia en Borrador o Pendiente de aprobación.
  - Una factura no fiscal (`IsZeroValue` o total 0) no lleva número fiscal.
- **Anular:** motivo de 10 a 500 caracteres. No se anula una pagada ni una con dinero recibido.
- **Refacturar:** una anulada, una sola vez. Crea un Borrador sin número.
- **Listado:** columnas «Identificación» y «Destinatario».
- **Diálogo de acciones:** Registrar TRM, N.º SIIGO, Aprobar, Enviar, Registrar pago, Detalle, Notas, Refacturar y Anular.

### 7.7 Recálculo de una factura ya emitida

Un solo núcleo (`RecalculateOpenPeriodAsync` / `RebaseOpenPeriodAsync`) reemplaza los períodos abiertos del depósito y sus líneas (`DEC-022`).

- **Causas:** camión tardío, TRM manual, CE-7, edición de productos, manifiesto del camión, anulación de pesaje, reversión de salida, corrección de la fecha de ingreso (con rebase) y refacturación.
- **Factura anulada:** no se toca.
- **Las demás:** se actualiza la misma factura y conserva el N.º SIIGO. El estado sigue al saldo; con pagos de más se informa el saldo a favor.
- Se notifica a Facturación con el total anterior y el nuevo.
- Los overrides se descartan y se listan en la notificación.
- **Cantidad facturable:** el stock más las salidas netas por cargue desde que el período tomó su stock (`DEC-028`).

### 7.8 Pagos

- **Estados:** `Pending` → `Received` → `Verified`, o `Rejected`. El monto no supera el saldo y solo entra en facturas emitidas.
- **Métodos:** efectivo, transferencia, cheque, tarjeta de crédito, tarjeta débito y otro.
- **Efectivo y cambio:** el registro del efectivo recibido y del cambio se construyó y se retiró (CHG-53); las columnas quedan como historia.

### 7.9 Cartera y bloqueo por mora

Un job diario marca las facturas vencidas y suma la deuda vencida por cliente. Si supera el límite de crédito, el cliente pasa a `Blocked`. **Un cliente sin límite de crédito nunca se bloquea.**

Un cliente `Blocked` no puede (`BillingService.ValidateFinancialStatusAsync`):

- pagar báscula (ingreso, salida o solo báscula);
- cerrar un uso de montacargas;
- recibir mercancía sin báscula;
- crear o reservar órdenes de cargue;
- crear guías ni cambiar su modo de pago.

### 7.10 Impuestos

- `IVA` 19 % (`TaxKind.Added`, se suma) y `RETE_FUENTE` 3 % (`Withholding`, se descuenta del pago, no suma a la factura).
- Un servicio lleva impuestos con `ServiceTax`. El único sembrado es `ALMACENAMIENTO` con IVA; sin `ServiceTax` la tasa es 0.
- El montacargas usa el check «Agregar IVA» (§5.8).

### 7.11 Jobs

Ver `contexto/convenciones-tecnicas.md` §6: vencimientos y mora, conciliación de pagos, cierre y renovación de períodos, avisos de vencimiento, alerta de abandono y respaldos.

---

## 8. Notificaciones, auditoría y reportes

**Notificaciones:** en la app por rol (SignalR, persistidas en `notifications`); algunas también por correo.

| Destinatario | Avisos |
| --- | --- |
| Facturación | Cargo al mínimo, TRM pendiente, renovación, fecha de ingreso cambiada, factura recalculada (total anterior y nuevo), factura anulada, vencimientos |
| Comercio Exterior | Nuevo depósito, producto creado en báscula, diferencia de recepción, camión adicional, novedad, abandono |
| Bodega | Órdenes canceladas o modificadas, depósito anulado |
| Admin | Cambios de peso o fecha en báscula, ingreso manual, respaldo fallido |

**Auditoría genérica:** `IAuditable` → `audit_logs`, con usuario, IP y valores anterior y nuevo; el motivo de una corrección va por `IAuditContext`. No crees tablas de auditoría.

**Trazabilidad por placa:** tablero que sigue cada camión por etapas.

**Reportes:**

| Reporte | Formato |
| --- | --- |
| Entradas y salidas diarias | PDF |
| Movimientos / kardex por depósito, con levantes y despachos | PDF y Excel |
| Inventario general, ingresos por producto | Excel |
| Pólizas | Excel |
| Facturación anual y por depósito | Excel |
| Agencias de aduana | Excel |
| Abandono (candidatos y salidas) | Excel |
| Báscula por modalidad | Historial de báscula con filtros y Excel |
| Facturación diaria de báscula | PDF |
| Estadísticas | Oculta en el menú |

El Excel se arma en el frontend (`useExcelExport`).

---

## 9. Documentos impresos

PDF con QuestPDF:

- tiquete de báscula y facturación diaria de báscula;
- etiqueta y consolidado de ingreso del depósito;
- orden de cargue (impresión de trabajo de Bodega) y guía de salida (también en un ZIP por depósito, que registra cada impresión);
- factura;
- reportes diarios y kardex;
- reporte de mercancías de una novedad.

Las fechas se imprimen en hora de Colombia. Los encabezados usan los parámetros de empresa (`COMPANY_*`).

Los formatos originales del cliente están en `docs/cliente/formatos/`.

---

## 10. Catálogos sembrados

| Catálogo | Valores |
| --- | --- |
| Roles del sistema | Administrador, Facturación, Comercio exterior, Operario vigilancia, Operario báscula, Operario bodega |
| Roles de negocio | `CUSTOMER`, `IMPORTER`, `EXPORTER`, `CUSTOMS_AGENCY`, `TRANSPORT_COMPANY` |
| Modalidades | `IMP001`, `EXP001`, `OTH001`, `INSP001` |
| Servicios | `BASCULA`, `ALMACENAMIENTO`, `MONTACARGAS`, `PAPELERIA`, `GUIA_SALIDA` |
| Impuestos | `IVA` 19 %, `RETE_FUENTE` 3 % |
| Tipos de unidad de carga | `CONTENEDOR`, `TANQUERO`, `REMOLQUE` (el Admin amplía el catálogo) |
| Unidades de medida | Catálogo administrable (ya no incluye «Tractomula») |
| Tipos de identificación | NIT, RUT, CC, pasaporte, RUC |
| Parámetros | `COMPANY_NAME`, `COMPANY_NIT`, `COMPANY_ADDRESS`, `COMPANY_PHONE`, `COMPANY_EMAIL`, `COMPANY_CITY`, `INVENTORY_ADJUSTMENT_ADMIN_EMAIL` |
| Mínimos de almacenamiento | $0 para IMP, EXP e INSP (los reales se configuran) |

- Productos, ubicaciones de ejemplo y ciudades **no se siembran**: en staging vienen de la migración del legacy.
- El administrador inicial lo crea `BootstrapAdminSeeder` al arrancar la API.

---

## 11. Afirmaciones antiguas que ya no son ciertas

Documentos anteriores (incluida la versión del 14-sep de este) dicen cosas que ya no son ciertas:

| Afirmación antigua | Realidad |
| --- | --- |
| El stock lo crea la recepción de Bodega; confirmar exige recepciones completadas | El stock nace con lo declarado en báscula; la recepción es informativa |
| Confirmar solo exige el cliente | Exige además los datos del documento, los terceros, la moneda y el valor, el manifiesto por camión y el reparto por unidad de carga |
| `EntryDate` la fija la recepción; el período cuenta desde la confirmación | `EntryDate` = Vigilancia del primer camión (editable); el período cuenta desde el ingreso |
| Consecutivos `DEP-IMP-2026-0001`, `TKT-…`, `OC-…` | `2026BA00001`, `2026T00001`, `2026OC00001`… |
| El primer camión que completa ciclo cierra el servicio (WMS-26) | Corregido; Comercio Exterior cierra el ingreso de camiones |
| La guía duplica el saldo anterior (WMS-19) | Corregido; las líneas se congelan en `dispatch_guide_lines` |
| La orden de cargue emite PDF y exige un solo cliente | Registra la orden externa, sin PDF, multicliente |
| Nacionalizado = la cantidad nacionalizada alcanza el stock | Nacionalizado = al menos un levante; el despacho tiene tope por producto |
| Báscula consulta la TRM | La TRM se consulta al crear la factura del período |
| Báscula registra peso neto y bruto por producto | Un único peso bruto del manifiesto |
| «Tanquero» es producto o embalaje | Es un tipo de unidad de carga |
| `WarehouseStorageContainer`, `PER_CONTAINER`, `FIXED_PER_CONTAINER`, `PER_PACKAGING_UNIT` | Unidades de carga y `PER_CARGO_UNIT` |
| Ciclos semanal, quincenal, mensual y bajo demanda | 8 ciclos, incluidos los del legacy; `OnDemand` retirado |
| Un job consolida los cargos del día | Los cobros pendientes no se consolidan; el job concilia pagos |
| Diferencia de recepción por correo al administrador | Aviso en la app a Comercio Exterior |
| Facturación crea facturas a mano (`manual-modulo-facturacion.md`) | No hay creación manual |
| Períodos «Abierto / Cerrado / Facturado» con «tarifa diaria» | `Open` / `Closed`; cobro por fórmula y por cargo |
| Convenios con precio fijo por producto (`AgreementPrice`) | `AgreementService` + parámetros con fórmulas |
| La tarifa de báscula se configura en el producto `SRV-BASCULA` | En el servicio `BASCULA` |
| Se registra efectivo recibido y cambio | Se construyó y se retiró (CHG-53) |
| Estados `PENDING_RECEPTION`, `STORED`… | `Draft`, `Confirmed`, `Closed`, `Cancelled` |
| Roles `INTERMEDIARY` o `SIA` | `CUSTOMS_AGENCY` |
| El agente no genera migraciones; ramas `feature/…` desde `develop` | Migraciones con `dotnet ef` por el agente; `develop` sin ramas (`DEC-003`, `DEC-004`) |
| .NET 8 (README del backend) | .NET 10 |
