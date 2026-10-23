# Contexto del proyecto WMS (Bodegas Asociadas)

Documento de referencia para implementaciones y ajustes futuros. Describe backend, frontend, modelo de datos y el flujo operativo, con énfasis en cómo se **generan y evolucionan los depósitos** (`warehouse_storages`).

---

## 1. Visión general

El sistema es un **WMS (Warehouse Management System)** integrado con **báscula**, **comercio exterior** (importación, exportación, inspección), **recepción en bodega**, **órdenes de cargue**, **guías de despacho** y **facturación** (servicios de báscula y períodos de almacenamiento).

- **Backend:** API REST en .NET (`Wms.Api`), PostgreSQL, Entity Framework Core, MediatR (CQRS), Identity JWT.
- **Frontend:** SPA con **Nuxt 4** (SSR desactivado), **Vue 3**, **PrimeVue**, **Pinia**, **TanStack Vue Query**, **SignalR** para notificaciones en tiempo real.

**Rutas típicas de desarrollo**

- API: configurable en `appsettings`; el front usa por defecto `http://localhost:5281/api/v1` (`NUXT_PUBLIC_API_BASE` en `.env`).
- Front: proyecto en `Frontend/wms` (`npm run dev`).

---

## 2. Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| `Backend/wms-api/Wms.Api` | Host ASP.NET, controladores `Controllers/v1/*`, SignalR, jobs en segundo plano (facturación). |
| `Backend/wms-api/Wms.Application` | Casos de uso: comandos/consultas MediatR, servicios de aplicación (báscula, comercio exterior, facturación). |
| `Backend/wms-api/Wms.Domain` | Entidades de dominio, enums, reglas (p. ej. `WarehouseStorage`, `ServiceRecord`). |
| `Backend/wms-api/Wms.Infrastructure` | EF Core `AppDbContext`, migraciones, persistencia, seeds. |
| `Backend/wms-api/Wms.Common` | Excepciones y utilidades compartidas. |
| `Frontend/wms` | Aplicación Nuxt: `app/pages`, `app/features/*` (módulos por dominio), `stores`, `plugins`. |
| `docs/` | Documentación del proyecto (este archivo, otros manuales). |

---

## 3. Backend: capas y convenciones

- **API:** controladores delgados que envían comandos/consultas a MediatR.
- **Validación:** FluentValidation + `ValidationBehavior`.
- **Errores:** `GlobalExceptionHandler` y excepciones de dominio (`BadRequestException`, `NotFoundException`, `ConflictException`, etc.).
- **Auditoría:** entidades `IAuditable` generan filas en `audit_logs` al guardar.
- **Base de datos:** PostgreSQL con **nombres en snake_case** (`UseSnakeCaseNamingConvention()`).

**Proyectos .csproj:** `Wms.Api`, `Wms.Application`, `Wms.Domain`, `Wms.Infrastructure`, `Wms.Common`.

**Jobs registrados en `Program.cs` (facturación):** detección de mora, consolidación de cargos diarios, cierre automático de períodos, notificaciones de facturas vencidas.

---

## 4. Frontend: organización

- **Framework:** Nuxt 4 (`ssr: false`).
- **UI:** PrimeVue con preset Material personalizado.
- **Estado:** Pinia (`stores/auth.ts`, `stores/api-errors.ts`, etc.).
- **Datos remotos:** composables que encapsulan llamadas HTTP; muchos usan TanStack Query.
- **API:** plugin `api-client` + `useApi`; base URL en `runtimeConfig.public.apiBase`.
- **Tiempo real:** `@microsoft/signalr` (`plugins/signalr.client.ts`).
- **Features:** cada dominio bajo `app/features/<dominio>/` con `services`, `composables`, `types`, `components` según corresponda.
- **Rutas:** `app/pages` refleja módulos: `operations/entries`, `operations/weighbridge`, `warehouse/receptions`, `foreign-trade/imports|exports|inspections`, `billing/*`, `admin/*`, etc.

---

## 5. Modelo de datos (resumen)

La fuente de verdad del esquema es **EF Core**: `AppDbContext` + configuraciones en el ensamblado de Infrastructure + migraciones en `Wms.Infrastructure/Migrations`. Las tablas siguen convención snake_case en PostgreSQL.

### 5.1 Núcleo operativo y logística

| Concepto EF | Rol |
|-------------|-----|
| `entry_logs` | Ingreso de vehículo/persona a la operación; se vincula a `service_records`. |
| `entry_reasons` | Motivos de ingreso (seed). |
| `vehicles`, `drivers` | Maestros de transporte. |
| `departure_authorizations` | Autorizaciones de salida. |
| `manifests` | Manifiesto asociado al `entry_log` cuando aplica. |

### 5.2 Servicio y báscula

| Concepto EF | Rol |
|-------------|-----|
| `service_records` | Servicio operativo: tipo (`Input`, `OutputCargo`), modalidad, cliente, documento (carta porte en ingresos a depósito), estado, flags de pesaje (`SingleWeightOnly`, `ConfiguredFirstWeightType`). |
| `service_record_documents` | Documentos anexos al servicio. |
| `service_record_stakeholders` | Cliente, importador, agencia, intermediario con rol de negocio. |
| `weighbridge_cycles` | Ciclo de báscula ligado a `service_record`, `entry_log` y factura de báscula cuando corresponde. |
| `operation_modalities` | Modalidades sembradas: **IMP001**, **EXP001**, **OTH001**, **INSP001**. |

### 5.3 Depósito e inventario

| Concepto EF | Rol |
|-------------|-----|
| `warehouse_storages` | **Depósito:** cabecera con estados (`Draft` / `Confirmed` / `Closed` / `Cancelled`), valor de carga, moneda, fechas aduaneras y observaciones. **No contiene stock directamente**; el stock se gestiona por producto en `warehouse_storage_products`. |
| `warehouse_storage_products` | **Producto por depósito (modelo multi-producto):** tabla pivote que asocia múltiples productos a un depósito. Cada fila registra el producto, cantidades declaradas (`declared_quantity`, `net_declared_weight`, `gross_declared_weight`), stock (`received_quantity`, `current_stock`, `reserved_stock`, `available_stock`), embalaje y unidad de medida. La ubicación de bodega (`warehouse_location_id`) se asigna a nivel de producto. |
| `warehouse_storage_entries` | **Una fila por camión** dentro del mismo depósito (mismo `warehouse_storage_id`, distintos `entry_log_id`). Enlaza opcionalmente `weighbridge_cycle_id`. |
| `warehouse_storage_entry_products` | **Desglose por producto de cada entrada de camión:** registra la cantidad declarada y el peso neto/bruto de un producto específico dentro de una entrada. Referencia `warehouse_storage_product_id`. |
| `warehouse_locations` | Ubicaciones físicas (seed). |
| `reception_logs`, `reception_cargo_photos` | Recepción en bodega y evidencias. Estados de recepción: `InProgress` → `Unloaded` → `Completed` / `Cancelled`. |
| `reception_log_products` | **Cantidad descargada por producto en cada recepción:** permite desglosar la descarga por producto cuando un camión transporta múltiples productos. Referencia `warehouse_storage_product_id`. |
| `inventory_movements` | Movimientos de inventario. |
| `forklift_uses` | Uso de montacargas. |
| `loading_orders`, `loading_order_items` | Orden de cargue y líneas por depósito. Estados: `Pending` → `InProgress` → `Loaded` → `Dispatched` → `Complete` / `Cancelled`. |
| `warehouse_reserves` | Reservas de stock contra una orden de cargue. |
| `loading_order_photos` | Fotos asociadas a la orden. |
| `dispatch_guides` | Guías de despacho (comercio exterior). Tipos: `Import`, `Export`, `Inspection`. |

### 5.4 Comercio exterior (importación)

| Concepto EF | Rol |
|-------------|-----|
| `import_warehouse_storages` | Extensión 1:1 de un `warehouse_storage` de modalidad importación: estado de etiquetas (**SinNacionalizar** / **Nacionalizado**), datos de levante, manifiesto DIAN, cantidades/pesos nacionalizados. |
| `import_releases` | Levantes (parciales o que completan nacionalización). |

**Nota:** Para modalidad **EXP** e **INSP** no existe tabla hija análoga en dominio; el depósito se identifica por `warehouse_storages` + `service_records.operation_modality`.

### 5.5 Productos, stakeholders y administración

| Concepto EF | Rol |
|-------------|-----|
| `stakeholders`, `stakeholder_business_roles`, `stakeholder_contact_infos`, `stakeholder_bank_accounts` | Terceros y roles comerciales. |
| `products`, `product_prices`, `taxes`, `product_taxes` | Catálogo e impuestos (p. ej. producto SKU báscula `SRV-BASCULA`). Los productos tienen `ProductType` (enum), `Packaging`, `UnitMeasure` y estado `IsActive`. Actualmente los precios (`ProductPrice`) e impuestos (`ProductTax`) están vinculados a la entidad `Product`; existe un plan de separar productos de servicios (ver requerimiento FAC-4). |
| `agreements`, `agreement_prices` | Convenios por cliente. Cada `Agreement` pertenece a un `Stakeholder`. Los `AgreementPrice` vinculan un `Product` con un `SpecialPrice` (decimal). **Nota:** el modelo actual de precios de acuerdo solo soporta un valor fijo por producto; no soporta fórmulas por porcentaje, tarifas mínimas ni cobro por unidad de medida (ver requerimiento FAC-5.4 para el rediseño planificado). |
| `business_roles` | Roles de negocio (seed). |
| `system_parameters` | Parámetros del sistema. |
| `shipping_document_types` | Tipos de documento de envío (seed). |

### 5.6 Facturación

| Concepto EF | Rol |
|-------------|-----|
| `invoices`, `invoice_items`, `invoice_payments` | Facturación (báscula y módulo de facturación). |
| `stakeholder_billing_configurations` | Ciclo de facturación por cliente. |
| `storage_billing_periods` | Períodos de cobro por depósito. |

### 5.7 Seguridad y auditoría

| Concepto EF | Rol |
|-------------|-----|
| `AspNetUsers`, `AspNetRoles`, etc. | Identity. |
| `refresh_tokens`, `password_reset_tokens` | Sesión y recuperación de clave. |
| `notifications` | Notificaciones in-app (también orquestación por rol). |
| `audit_logs` | Auditoría de cambios en entidades auditable. |

---

## 6. Flujo de la aplicación (macro)

### 6.1 Punto de entrada: ingreso (`entry_logs`)

1. Se registra el ingreso (vehículo, conductor, motivo, etc.).
2. Según el flujo elegido en báscula, el `entry_log` queda libre o se asocia a un `service_record`.

### 6.2 Flujo “solo báscula” (modalidad **OTH001**)

- Se crea un `service_record` de tipo **Input** sin depósito de mercancía en bodega (uso principal: pesaje sin almacenamiento prolongado como depósito WMS).
- No aplica creación de `warehouse_storage` en el flujo de “ingreso a depósito” descrito abajo.

### 6.3 Flujo “ingreso a depósito” (modalidades **IMP001**, **EXP001**, **INSP001**)

**Comando principal:** iniciar pesaje de almacenamiento (`InitiateStorageWeighing`).

1. **Primer camión** con una **carta porte** (`cargo_manifest_number`) que aún no existe en un `service_record` de tipo **Input**:
   - Se crea `ServiceRecord.CreateForStorage` (en tránsito, con modalidad y documento).
   - Se genera el **número de depósito** con `IWeighbridgeService.GenerateWarehouseStorageNumberAsync`:
     - **IMP** → prefijo `DEP-IMP-YYYY-####`
     - **EXP** → `DEP-EXP-YYYY-####`
     - **INSP** → `DEP-INS-YYYY-####`
     - Otros códigos → `DEP-GEN-YYYY-####`
   - Se crea `WarehouseStorage.CreateForStorage` → estado inicial **`Draft`**, stocks en cero.
   - Si la modalidad comienza por **`IMP`**, se crea **`ImportWarehouseStorage`** (`SinNacionalizar`) y puede enviarse notificación al rol de comercio exterior.

2. **Camiones adicionales** con la **misma** carta porte y la **misma** modalidad:
   - Se reutiliza el `service_record` existente (si no está completado).
   - Se reutiliza el **mismo** `warehouse_storage`.
   - Se crea una **nueva** `WarehouseStorageEntry` (camión, manifiesto, cantidades declaradas del ciclo, etc.).

3. **Reglas especiales inspección (`INSP`):** si el código de modalidad empieza por `INSP`, el sistema fuerza **un solo pesaje** (`singleWeightOnly`) y primer peso **bruto**, independientemente de lo que envíe el cliente en otros campos.

4. **Conflicto de modalidad:** no se puede asociar un camión a un documento que ya tuvo otro tipo de modalidad de depósito.

5. El `entry_log` recibe `service_record_id`. Tras `SaveChanges`, se devuelve tarifa de báscula e impuestos para cobro.

**Pago báscula ingreso a depósito** (`ProcessStoragePayment`):

- Valida cliente y estado financiero (`ValidateFinancialStatusAsync`).
- Crea factura de báscula y pago, crea `WeighbridgeCycle`, lo enlaza a la `WarehouseStorageEntry` correspondiente y pasa el servicio a estado de pesaje.

**Ciclo de báscula:** primer peso / segundo peso (o uno solo según configuración), cálculo de neto, actualización de `WarehouseStorageEntry` (neto, ticket), etc. — hasta completar el ciclo según handlers comunes de báscula.

### 6.4 Recepción en bodega

- **`CreateReception`:** asocia recepción al `warehouse_storage_entry` correspondiente. Se registra con `ReceptionLog.Create` (estado `Unloaded`) o `ReceptionLog.RegisterArrival` (estado `InProgress` — camión llegó, descarga pendiente). Las cantidades descargadas se desglosan por producto en `ReceptionLogProduct`, y cada `WarehouseStorageProduct` actualiza su stock con `ReceiveQuantity`.
- **`CompleteReception`:** marca la recepción como `Completed` (`ReceptionLog.Complete`). El estado del depósito (`WarehouseStorage`) **no cambia automáticamente** en `CompleteReception`; el depósito permanece en su estado actual (`Draft` o `Confirmed`).
- Tras recepción (crear/completar), **`StorageBillingService.CreateInitialPeriodAsync`** puede abrir el **primer período de facturación** de almacenamiento según configuración del cliente (producto catalogado, ciclo distinto de `OnDemand`, etc.).

Existen flujos alternativos (p. ej. recepción sin báscula) que también pueden disparar períodos iniciales.

### 6.5 Comercio exterior después del depósito

- **Importaciones:** listados y detalle sobre `import_warehouse_storages` + joins a `warehouse_storages`. Operaciones típicas: actualizar manifiesto DIAN, registrar **levantes** (`ImportRelease`), transición a **Nacionalizado** cuando la cantidad nacionalizada alcanza el tope (stock/recibido según reglas de dominio). Las **órdenes de cargue** para ítems de importación exigen depósito en estado **Nacionalizado**.
- **Exportaciones e inspección:** consultas filtran `warehouse_storages` por `operation_modality` (**EXP001** o código que empiece por **INSP**). Guías de despacho: el tipo de guía (importación / inspección / exportación) se determina en servicios de comercio exterior según la modalidad del depósito.

### 6.6 Órdenes de cargue y salida de mercancía

1. **Crear orden de cargue:** valida que los depósitos sean del **mismo cliente** (`StakeholderId`) *(validación a eliminar con requerimiento CE-12)*, stock disponible a nivel de `WarehouseStorageProduct`, y para importaciones que estén **nacionalizados**; valida estado financiero del cliente; crea reservas (`WarehouseReserve`, `WarehouseStorageProduct.ReserveStock` en dominio) y genera PDF. Ciclo de vida de la orden: `Pending` → `InProgress` → `Loaded` → `Dispatched` → `Complete` / `Cancelled`.
2. **Iniciar salida en báscula** (`InitiateOutputWeighing`): crea `service_record` tipo **`OutputCargo`** con la **misma** `operation_modality_id` que el depósito de la orden, vincula `loading_order_id` y el `entry_log`.
3. Pago y ciclo de báscula de salida en handlers dedicados (`ProcessOutputPayment`, etc.).
4. Al despachar, se libera stock del depósito por producto (`WarehouseStorageProduct.ReleaseStock`) y el depósito puede cerrarse (`WarehouseStorage.Close`) cuando ningún producto tiene stock (`StorageProducts.Any(sp => sp.CurrentStock > 0)` es false).

### 6.7 Facturación y riesgo crediticio

- Períodos de almacenamiento, facturas de servicios, bloqueos por mora: coordinados por servicios de billing y configuración por stakeholder.
- Los puntos de integración con operación incluyen: pago de báscula, validación antes de órdenes de cargue, y creación de períodos al recibir mercancía.

---

## 7. Depósitos: profundización

### 7.1 Qué es un “depósito” en el sistema

El depósito operativo es la entidad **`WarehouseStorage`** (`warehouse_storages`):

- **Identificador de negocio visible:** `warehouse_storage_number` (generado por año y modalidad, ver sección 6.3).
- **Agrupa** toda la mercancía bajo un mismo `service_record` de ingreso (misma carta porte / mismo servicio de entrada).
- **Stock:** `received_quantity`, `current_stock`, `reserved_stock`, `available_stock` (la disponibilidad es coherente con reservas de órdenes de cargue).
- **Estados** (`WarehouseStorageStatus`): 4 valores — `Draft`, `Confirmed`, `Closed`, `Cancelled`.
  - `Draft` (inicial): depósito editable (`UpdateDraftInfo`). Permite recepción de mercancía sin cambiar estado.
  - `Draft` → `Confirmed` (método `Confirm()`): depósito bloqueado para edición; admite recepciones, reservas y despachos.
  - `Confirmed` → `Draft` (método `MarkForCorrection(reason)`): retorno para corrección, solo desde `Confirmed`.
  - `Draft` / `Confirmed` → `Closed` (método `Close()`): requiere que **todos** los productos tengan `CurrentStock = 0`; marca `IsActive = false`.
  - `Draft` / `Confirmed` → `Cancelled` (método `Cancel(reason)`): anulación; marca `IsActive = false`.

### 7.2 Relación “un depósito, varios camiones”

- Cada arribo de camión bajo el mismo servicio genera **`WarehouseStorageEntry`**: une `warehouse_storage_id` + `entry_log_id`, datos de manifiesto/cantidad del ciclo y, tras pago, `weighbridge_cycle_id`.
- El inventario y la recepción consolidan el stock del **depósito**, no un registro duplicado de depósito por camión.

### 7.4 Depósito de importación

- Además de `WarehouseStorage`, existe **`ImportWarehouseStorage`**:
  - Estado de etiquetas: **SinNacionalizar** / **Nacionalizado**.
  - **Levantes:** tabla `import_releases`; el agregado actualiza `nationalized_quantity` / `nationalized_weight` y recalcula el estado. La nacionalización se completa cuando `nationalized_quantity` alcanza `min(current_stock, received_quantity)` del producto (con tolerancia de 0.0001).
  - Levantes vinculados a producto: cada `ImportRelease` referencia un `warehouse_storage_product_id`.
  - Campos de manifiesto DIAN (`manifest_number`, `manifest_date`), validación (`validated_at`), observaciones.
  - Métodos de dominio: `RegisterRelease`, `NationalizePartial`, `RecalculateStatus`, `ApplyNationalizedDeltaFromReleaseEdit`, `UpdateManifest`, `MarkAsValidated`, `AddObservation`.
- Este registro se crea **solo** cuando la modalidad del servicio comienza por **`IMP`**, en el mismo momento en que se crea el depósito (primer camión del documento).

### 7.5 Depósito de exportación

- Solo **`WarehouseStorage`** con `service_records.operation_modality.code = EXP001` (salvo que en el futuro se agreguen más códigos EXP).
- No hay tabla de extensión; las pantallas y reportes filtran por modalidad.

### 7.6 Depósito por inspección

- Misma entidad **`WarehouseStorage`** con modalidad cuyo código **empieza por `INSP`** (seed actual: **INSP001**).
- En báscula: **un solo pesaje** y primer peso **bruto** forzado en `InitiateStorageWeighing`.
- Listados y guías tratan este caso como tipo **Inspection** en servicios de comercio exterior.

### 7.7 Numeración y trazabilidad

- Los números `DEP-*-YYYY-####` son únicos por prefijo y año (búsqueda del último correlativo en BD).
- Notificaciones SignalR y notificaciones persistidas pueden referenciar entidades relacionadas (p. ej. nuevo depósito de importación).

---

## 8. API y módulos útiles para extender

- Controladores bajo `Wms.Api/Controllers/v1/` (rutas en minúsculas): por ejemplo `ForeignTradeController` (importaciones, exportaciones, inspecciones, órdenes de cargue, PDFs, etiquetas), controladores de báscula, warehouse, billing, entries, etc.
- Comandos/consultas: espejo en `Wms.Application` por carpeta de feature.

---

## 9. Mantenimiento del documento

- Tras migraciones relevantes o nuevos flujos, actualizar las secciones **5** (tablas/nuevas entidades) y **6–7** (flujo y depósitos).
- Las reglas exactas de negocio están en los **handlers** y **métodos de dominio**; este archivo no sustituye el código, pero alinea el lenguaje de negocio con las entidades.

---

*Generado como contexto de proyecto para el workspace `code_workspace`. Fecha de referencia del análisis del código: 30 de abril de 2026.*
