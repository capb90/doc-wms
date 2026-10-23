# Contrato de API — paridad con Bodegas legacy (wms-api)

**Fecha:** 2026-09-29. **Documento hermano:** `code_workspace/ajustes/plan-backend-paridad-legacy.md` (plan de backend).

Este contrato enumera **cada endpoint nuevo o modificado** por el plan de paridad, con la forma exacta de su petición, su respuesta y sus errores. Es autosuficiente: el agente de frontend lo usa sin leer el plan ni el análisis. Cada entrada tiene un identificador `C-Fx-yy` y la fase donde se construye.

**Disponibilidad:** todo se construye en `develop`, sin ramas, fase por fase (1 → 6) e ítem por ítem. Un endpoint está disponible cuando el ítem que lo construye tiene su commit en `develop`. La columna «Fase» del índice dice cuándo.

---

## 0. Convenciones comunes

### 0.1 Transporte

- Base: `/api/v1`. Todas las rutas de este documento son relativas a esa base.
- Autenticación: `Authorization: Bearer <JWT>`.
- JSON en *camelCase*. Los enums viajan como **texto**, por ejemplo `"Draft"` o `"Days15"`.
- **Fechas:**
  - Con hora: ISO 8601 con zona, por ejemplo `"2026-09-29T10:00:00-05:00"`.
  - Solo día (`DateOnly`): `"yyyy-MM-dd"`.
  - Los días de negocio se interpretan en hora de Colombia (America/Bogota).
- Los números decimales son números JSON.

### 0.2 Respuesta exitosa

```jsonc
{
  "data": { /* objeto, lista o null */ },
  "pagination": { "pageIndex": 1, "pageSize": 10, "totalCount": 123, "totalPages": 13 } // solo en listados
}
```

Los PDF y ZIP se devuelven como archivo (`application/pdf`, `application/zip`) con nombre de archivo.

### 0.3 Paginación

- `pageIndex` (≥ 1, por defecto 1) y `pageSize` (1 a 50, por defecto 10). **El tope es 50 y no se sube.**
- `all=true` devuelve todas las filas del filtro en una página: úselo para exportar a Excel y para llenar *selects*.

### 0.4 Errores

Cuerpo *ProblemDetails*:

```jsonc
{
  "type": "…", "title": "…", "status": 400,
  "description": "Mensaje para el operario",
  "errors": [ { "code": "NombreDeLaPropiedad", "description": "Mensaje del campo" } ]
}
```

| Status | Cuándo | Dónde viene el mensaje |
|---|---|---|
| 400 | Validación de formato | `errors[].description`, con `code` = propiedad |
| 400 | Regla de negocio | `description` |
| 404 | No existe | `description` |
| 409 | Conflicto de estado o duplicado | `description` |
| 503 | La DIAN no responde (solo donde se indica) | `description` |

**Regla para el frontend:** mostrar `errors[].description` si la lista no está vacía; si no, `description`. Los mensajes de este contrato están en español y se muestran tal cual. Las llaves `{…}` indican valores que el backend reemplaza.

### 0.5 Motivos

Donde se pide `reason`, se valida recortado y entre 10 y 500 caracteres, salvo que se indique otra cosa. El mensaje exacto está en cada endpoint.

### 0.6 Políticas (roles)

| Política | Roles |
|---|---|
| `AdminOnly` | Admin |
| `ScaleAccess` | Admin, Scale |
| `ForeignTradeAccess` | Admin, ForeignTrade |
| `WarehouseAccess` | Admin, Warehouse, Receiving |
| `BillingAccess` | Admin, Billing |
| `ActiveUser` / autenticado | cualquier usuario activo |

---

## 1. Índice

| ID | Verbo y ruta | Tipo | Fase |
|---|---|---|---|
| C-F1-01 | `POST weighbridge/storage/initiate` | modificado | 1 |
| C-F1-02 | `POST weighbridge/storage/register` | modificado | 1 |
| C-F1-03 | `GET weighbridge/service-records/by-document`, `GET weighbridge/warehouse-storage/by-document` | modificado | 1 |
| C-F1-04 | `PUT foreign-trade/warehouse-storages/{id}/stakeholders` | modificado | 1 |
| C-F1-05 | `PATCH foreign-trade/warehouse-storages/{id}/draft` | modificado | 1 |
| C-F1-06 | `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` | nuevo | 1 |
| C-F1-07 | `POST foreign-trade/warehouse-storages/{id}/confirm` | modificado | 1 |
| C-F1-08 | `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` | nuevo | 1 |
| C-F1-09 | `GET product` | modificado | 1 |
| C-F1-10 | `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` | nuevo | 1 |
| C-F1-11 | `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown` | nuevo | 1 |
| C-F1-12 | `POST weighbridge/{storage,weighing-only,output}/process-payment` | modificado | 1 |
| C-F2-01 | `POST foreign-trade/imports/{id}/releases` | modificado | 2 |
| C-F2-02 | `PATCH foreign-trade/imports/{id}/releases/{releaseId}` | modificado | 2 |
| C-F2-03 | `POST foreign-trade/loading-orders` | modificado | 2 |
| C-F2-04 | `GET foreign-trade/loading-orders/deposits` | modificado | 2 |
| C-F2-05 | `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` | nuevo | 2 |
| C-F2-06 | `GET foreign-trade/imports/{id}` (levantes con FOB) | modificado | 2 |
| C-F2-07 | `GET/POST/PUT/DELETE administration/cities…`, `POST administration/cities/import` | nuevo | 2 |
| C-F2-08 | `POST warehouse/loading-orders` | modificado | 2 |
| C-F2-09 | detalle y listados de órdenes de cargue | modificado | 2 |
| C-F2-10 | `POST foreign-trade/dispatch-guides` | modificado | 2 |
| C-F2-11 | `POST foreign-trade/imports/{id}/extension` | nuevo | 2 |
| C-F2-12 | `GET foreign-trade/abandonment` | nuevo | 2 |
| C-F2-13 | `GET foreign-trade/abandonment/summary` | nuevo | 2 |
| C-F2-14 | `GET reports/abandonment-candidates` | nuevo | 2 |
| C-F2-15 | `GET reports/abandonment-exits` | nuevo | 2 |
| C-F3-01 | `POST warehouse/loading-orders/{id}/execute` | modificado | 3 |
| C-F3-02 | `PATCH foreign-trade/loading-orders/{id}/cancel`, `PATCH warehouse/loading-orders/{id}/cancel` | modificado | 3 |
| C-F3-03 | `PUT foreign-trade/loading-orders/{id}/items` | nuevo | 3 |
| C-F3-04 | `POST foreign-trade/dispatch-guides/{id}/cancel` (+ campos en guías) | nuevo | 3 |
| C-F3-05 | `GET billing/configurations/cycles` | nuevo | 3 |
| C-F3-06 | `PUT billing/configurations/{stakeholderId}` (ciclos nuevos) | modificado | 3 |
| C-F3-07 | `GET billing/storage-periods`, `GET billing/storage-periods/{id}` | modificado | 3 |
| C-F3-08 | `POST foreign-trade/loading-orders/{id}/revert` | nuevo | 3 |
| C-F3-09 | `POST foreign-trade/warehouse-storages/{id}/cancel` | modificado | 3 |
| C-F3-10 | `POST weighbridge/cycles/{cycleId}/void` | nuevo | 3 |
| C-F3-11 | `GET weighbridge/history` (anulados) | modificado | 3 |
| C-F3-12 | `PATCH billing/invoices/{id}/cancel` | modificado | 3 |
| C-F3-13 | `POST billing/invoices/{id}/reissue` | nuevo | 3 |
| C-F3-14 | `GET billing/pending-deposits` | modificado | 3 |
| C-F4-01 | `GET warehouse/storage-products/{id}/placements` | nuevo | 4 |
| C-F4-02 | `POST warehouse/storage-products/{id}/placements` | nuevo | 4 |
| C-F4-03 | `POST warehouse/storage-products/{id}/placements/move` | nuevo | 4 |
| C-F4-04 | `POST warehouse/storage-products/{id}/placements/release` | nuevo | 4 |
| C-F4-05 | `GET warehouse/locations/{id}/placements` | nuevo | 4 |
| C-F4-06 | `POST warehouse/receptions`, `…/receptions/{id}/complete`, `…/receptions/without-weighbridge` | modificado | 4 |
| C-F4-07 | `POST warehouse/loading-orders/{id}/execute` (ubicaciones y cuadrilla) | modificado | 4 |
| C-F4-08 | `POST warehouse/novelties` | nuevo | 4 |
| C-F4-09 | `PUT warehouse/novelties/{id}` | nuevo | 4 |
| C-F4-10 | `POST warehouse/novelties/{id}/void` | nuevo | 4 |
| C-F4-11 | `GET warehouse/novelties`, `GET warehouse/novelties/{id}` | nuevo | 4 |
| C-F4-12 | `GET warehouse/novelties/{id}/pdf` | nuevo | 4 |
| C-F4-13 | `GET/POST foreign-trade/packing-list-suppliers` | nuevo | 4 |
| C-F4-14 | `POST foreign-trade/packing-lists/import` | nuevo | 4 |
| C-F4-15 | `GET foreign-trade/packing-lists`, `GET …/{id}`, `DELETE …/{id}` | nuevo | 4 |
| C-F4-16 | `GET foreign-trade/packing-list-items` | nuevo | 4 |
| C-F4-17 | `POST foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items` | nuevo | 4 |
| C-F4-18 | `POST weighbridge/output/cycles/{cycleId}/additional-orders` | nuevo | 4 |
| C-F4-19 | `POST weighbridge/output/from-entry-ticket`, `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` | nuevo | 4 |
| C-F4-20 | `GET foreign-trade/{imports,exports,inspections}/{id}/label?action=` | modificado | 4 |
| C-F4-21 | `GET foreign-trade/warehouse-storages/{id}/label-prints` | nuevo | 4 |
| C-F4-22 | `GET/POST/PUT/DELETE administration/crews…` | nuevo | 4 |
| C-F4-23 | `crewId` en recepción, órdenes y cargue; cuadrilla en la guía | modificado | 4 |
| C-F5-01 | `GET foreign-trade/imports` (saldos y búsquedas) | modificado | 5 |
| C-F5-02 | `GET foreign-trade/releases` | nuevo | 5 |
| C-F5-03 | `GET warehouse/movements-report` (kardex) | modificado | 5 |
| C-F5-04 | `GET reports/general-inventory` | nuevo | 5 |
| C-F5-05 | `GET reports/policies` | nuevo | 5 |
| C-F5-06 | `GET reports/policies/detail` | nuevo | 5 |
| C-F5-07 | `POST stakeholder`, `PATCH stakeholder/{id}`, `GET stakeholder…` (UAP) | modificado | 5 |
| C-F5-08 | `GET reports/incoming-by-product` | nuevo | 5 |
| C-F5-09 | `GET reports/billing-annual` | nuevo | 5 |
| C-F5-10 | `GET reports/deposit-billing` | nuevo | 5 |
| C-F5-11 | `GET weighbridge/history` (filtros y pesos) | modificado | 5 |
| C-F5-12 | `GET reports/customs-agency-entries` | nuevo | 5 |
| C-F5-13 | `GET reports/customs-agency-entries/{warehouseStorageId}` | nuevo | 5 |
| C-F5-14 | Tabla de exportaciones a Excel | referencia | 5 |
| C-F6-01 | `POST administration/legacy-import/{entity}` | nuevo | 6 |
| C-F6-02 | `GET administration/legacy-import/batches`, `GET …/batches/{id}` | nuevo | 6 |
| C-F6-03 | `POST administration/legacy-import/reconciliation` | nuevo | 6 |
| C-F6-04 | `POST administration/legacy-import/open-billing` | nuevo | 6 |
| C-F6-05 | `GET/POST/PUT/DELETE administration/backup-destinations…`, `POST …/{id}/test` | nuevo | 6 |
| C-F6-06 | `POST administration/backups/run` | nuevo | 6 |
| C-F6-07 | `GET administration/backups/runs` | nuevo | 6 |

---

## 2. Fase 1 — Báscula

### C-F1-01 · `POST weighbridge/storage/initiate` (modificado)

- **Política:** `ScaleAccess`.
- **Qué cambia:** báscula registra el camión con lo que tiene a mano. Comercio Exterior completa el resto y la confirmación lo exige (C-F1-07).

**Petición** (solo campos que cambian; el resto sigue igual):

| Campo | Tipo | Antes | Ahora |
|---|---|---|---|
| `documentDate` | datetime \| null | exigido por el backend | **opcional**; si viene, no futura |
| `importerId`, `importerRoleId` | string (GUID) \| null | obligatorios en IMP | **opcionales**; van juntos |
| `importAgencyId`, `importAgencyRoleId` | string (GUID) \| null | obligatorios en IMP | **opcionales**; van juntos |
| `exporterId`, `exporterRoleId` | string (GUID) \| null | se ignoraban | **nuevos**, opcionales; van juntos |
| `manifestNumber` | string \| null | opcional | opcional, hasta 100 |
| `manifestWeight` | decimal \| null | obligatorio > 0 | **opcional**; si viene, > 0 |
| `currency` | string \| null | sin validar | opcional; `"COP"` o `"USD"`, sin distinguir mayúsculas |
| `cargoValue` | decimal \| null | opcional > 0 | igual |
| `products[].productId` | string (GUID) \| null | obligatorio | **opcional** si viene `productDescription` |
| `products[].productDescription` | string \| null | ignorado sin id | con `productId` nulo: obligatoria, 3 a 200 caracteres. Busca el producto por nombre sin tildes ni mayúsculas; si no existe, lo crea |
| `cargoUnits[].products` | lista \| null | obligatoria | **opcional**: todas las unidades con mercancía o ninguna |
| `cargoUnits[].products[].productId` | string (GUID) \| null | obligatorio | opcional si viene `productDescription` |
| `cargoUnits[].products[].productDescription` | string \| null | — | **nuevo** |

- **Unidades de carga sin mercancía:**
  - Con **una** unidad, el backend le asigna la mercancía del camión.
  - Con **dos o más**, se crean vacías y Comercio Exterior reparte (C-F1-11).
  - No se permiten vacías si el depósito ya está confirmado.
- **Documento sin fecha:** si hay **un** depósito abierto con esa carta porte y ese tipo, el camión se asocia a él. Si hay **varios**, responde 409 pidiendo la fecha. Si la fecha viene y el depósito no la tenía, se le guarda.

**Respuesta 200** (`data`, campos que cambian):

```jsonc
{
  "warehouseStorageNumber": "2026BA00012",  // ahora siempre lleno (primer camión, camión adicional o depósito adicional)
  "createdProducts": [                       // nuevo; vacío si no se creó ninguno
    { "productId": "guid", "name": "CEBOLLA ROJA", "sku": "BAS-1A2B3C4D" }
  ]
  // …resto de campos sin cambios (serviceRecordId, isFirstTruck, weighbridgeCycleId, etc.)
}
```

**Errores nuevos o cambiados:**

| Status | Mensaje |
|---|---|
| 400 | "La fecha del documento no puede ser futura." |
| 400 | "El peso bruto según manifiesto debe ser mayor que cero." |
| 400 | "El número de manifiesto no puede exceder 100 caracteres." |
| 400 | "La moneda debe ser COP o USD." |
| 400 | "La descripción del producto debe tener entre 3 y 200 caracteres." |
| 400 | "Si proporciona el exportador, debe proporcionar su rol." |
| 400 | "El Id del exportador no es válido." / "El rol del exportador no es válido." |
| 400 | "Declare la mercancía en todas las unidades de carga del camión o en ninguna." |
| 400 | "El depósito {número} ya está confirmado: declare la mercancía de cada unidad de carga de este camión." |
| 404 | "El exportador no existe." |
| 404 | "El producto con Id '{id}' no existe." |
| 409 | "Hay {n} depósitos abiertos con el documento {número}: {depósitos separados por coma}. Indique la fecha del documento para elegir el depósito." |
| 409 | "El ingreso de camiones del documento '{número}' fue cerrado por {nombre} el {dd/MM/yyyy HH:mm}. No se pueden asociar más camiones. Si es un documento nuevo, indique su fecha." Si el documento tiene fecha, después del número va " con fecha '{dd/MM/yyyy}'". |
| 409 | "El documento '{número}' ya tiene un depósito con modalidad '{código}'. No se puede asociar un camión con modalidad '{código}'." (sin fecha, el tramo de fecha se omite) |
| 409 | "No se pudo generar un SKU único para el producto; intente de nuevo." |

Se eliminan: "La fecha del documento comercial es requerida…" (ambas variantes) y la exigencia de importador y agencia en IMP.

**Notas para el frontend:**
- El formulario de báscula deja de exigir fecha, importador, agencia, valor, moneda, número y peso de manifiesto; siguen siendo opcionales.
- Muestre `warehouseStorageNumber` después de registrar, para que el operario vea a qué depósito quedó el camión.
- Ante el 409 de ambigüedad, pida la fecha del documento y reintente.

### C-F1-02 · `POST weighbridge/storage/register` (modificado)

- **Política:** `ScaleAccess`.
- **Cambios:** los mismos de C-F1-01 en los campos equivalentes (`documentDate`, importador, agencia, `exporterId`/`exporterRoleId` nuevos, manifiesto, moneda, `products[]`, `cargoUnits[]`). La respuesta y los errores son los de C-F1-01.

### C-F1-03 · Consultas por documento de báscula (modificado)

- **Rutas:** `GET weighbridge/service-records/by-document` y `GET weighbridge/warehouse-storage/by-document`. Parámetros actuales; la fecha del documento es opcional.
- **Respuesta 200:**
  - `data` = el único depósito **abierto** (Borrador o Confirmado, ingreso de camiones sin cerrar, servicio no descartado) que coincide;
  - o `data: null` si no hay ninguno.
  - Nunca devuelve un depósito anulado o cerrado.
- **409:** el mismo mensaje de ambigüedad de C-F1-01, si hay varios.

### C-F1-04 · `PUT foreign-trade/warehouse-storages/{id}/stakeholders` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Petición:** sin cambio de forma, `{ "stakeholders": [ { "roleCode": "EXPORTER", "stakeholderId": "guid" } ] }`. `roleCode` admite ahora `EXPORTER`, además de `IMPORTER`, `CUSTOMS_AGENCY` y `TRANSPORT_COMPANY`.
- **Error cambiado:** 400 "Rol '{rol}' no admitido. Roles válidos: IMPORTER, EXPORTER, CUSTOMS_AGENCY, TRANSPORT_COMPANY."

### C-F1-05 · `PATCH foreign-trade/warehouse-storages/{id}/draft` (modificado)

- **Política:** `ForeignTradeAccess`. Solo en Borrador (regla actual).
- **Petición:**

```jsonc
{
  "customerId": "guid | null",
  "intermediaryId": "guid | null",
  "currency": "COP | USD | null",
  "cargoValue": 12345.67,
  "observations": "string | null",
  "documentDate": "2026-09-20T00:00:00-05:00"   // nuevo, opcional
}
```

- **Errores nuevos:**

| Status | Mensaje |
|---|---|
| 400 | "La fecha del documento no puede ser futura." |
| 409 | "Ya existe un depósito abierto con el documento {número} y fecha {dd/MM/yyyy}: {depósito}." |

### C-F1-06 · `PATCH foreign-trade/warehouse-storages/{id}/entries/{entryId}/manifest` (nuevo)

- **Política:** `ForeignTradeAccess`. Depósito en Borrador o Confirmado.
- **Petición:**

```jsonc
{ "manifestNumber": "MAN-123",   // 1 a 100 caracteres
  "manifestWeight": 12500.5,     // > 0 (kg)
  "reason": "string | null" }    // opcional, hasta 500
```

- **Respuesta 200:**

```jsonc
{ "data": { "warehouseStorageEntryId": "guid", "vehiclePlate": "ABC123",
            "manifestNumber": "MAN-123", "manifestWeight": 12500.5,
            "billingRecalculated": true } }   // true si el depósito está confirmado y cambió el peso
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El número de manifiesto es requerido." |
| 400 | "El número de manifiesto no puede exceder 100 caracteres." |
| 400 | "El peso del manifiesto debe ser mayor que cero." |
| 400 | "El motivo no puede exceder 500 caracteres." |
| 400 | "Solo se puede completar el manifiesto de un depósito en Borrador o Confirmado." |
| 404 | "El camión no pertenece a este depósito." |

- **Nota:** si el depósito está confirmado y cambia el peso, Facturación recibe el aviso de recálculo habitual.

### C-F1-07 · `POST foreign-trade/warehouse-storages/{id}/confirm` (modificado)

- **Política:** `ForeignTradeAccess`. Petición y respuesta sin cambio.
- **Error nuevo:** 400 con la lista completa de lo que falta, separada por "; ", en este orden:

  > "No se puede confirmar el depósito {número}. Falta: cliente; fecha del documento; importador; agencia de aduanas; exportador; moneda; valor de la mercancía; número de manifiesto del camión {placa}; peso del manifiesto del camión {placa}; mercancía de la unidad de carga {placa}; reparto de {producto} en las unidades del camión {placa}."

  Solo aparecen los elementos que faltan.
  - Importador y agencia: solo IMP.
  - Exportador: solo EXP.
  - INSP no exige terceros documentales.
- **Reemplaza** a: "El depósito debe tener un cliente asignado para poder confirmarse."

### C-F1-08 · `GET foreign-trade/warehouse-storages/{id}/confirmation-requirements` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Respuesta 200:**

```jsonc
{ "data": {
  "warehouseStorageId": "guid",
  "warehouseStorageNumber": "2026BA00012",
  "canConfirm": false,
  "missing": [
    { "code": "DOCUMENT_DATE", "message": "fecha del documento" },
    { "code": "MANIFEST_WEIGHT", "message": "peso del manifiesto del camión ABC123" }
  ] } }
```

- **Códigos posibles**, en este orden: `CUSTOMER`, `DOCUMENT_DATE`, `IMPORTER`, `CUSTOMS_AGENCY`, `EXPORTER`, `CURRENCY`, `CARGO_VALUE`, `MANIFEST_NUMBER`, `MANIFEST_WEIGHT`, `CARGO_UNIT_PRODUCTS`, `CARGO_UNIT_BREAKDOWN`.
- **Error:** 404 "El depósito no existe."
- **Nota:** úselo para mostrar la lista antes de confirmar. Es el mismo cálculo del error de C-F1-07. Desde la fase 3 excluye los camiones anulados.

### C-F1-09 · `GET product` (modificado)

- **Política:** actual.
- **Query nueva:** `createdFromWeighbridge` (bool, opcional): filtra los productos creados desde báscula.
- **`ProductDto` agrega** `createdFromWeighbridge: boolean`.

### C-F1-10 · `PUT foreign-trade/deposits/{id}/products/{storageProductId}/catalog-product` (nuevo)

- **Política:** `ForeignTradeAccess`. Depósito en Borrador.
- **Petición:** `{ "productId": "guid", "reason": "string (10 a 500)" }`
- **Respuesta 200:** `{ "data": { "warehouseStorageProductId": "guid", "productId": "guid", "productName": "CEBOLLA", "previousProductName": "CEBOLLA ROJA" } }`
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Solo se pueden editar los productos de un depósito en Borrador." |
| 400 | "La línea ya tiene ese producto." |
| 400 | "No se puede cambiar el producto: la línea {motivo}." |
| 400 | "El motivo del cambio debe tener entre 10 y 500 caracteres." |
| 404 | "El producto no existe en este depósito." |
| 404 | "El producto del catálogo no existe o está inactivo." |
| 409 | "El producto «{nombre}» ya tiene una línea en este depósito; corrija esa línea en lugar de cambiar esta." |

### C-F1-11 · `PUT foreign-trade/warehouse-storages/{id}/entries/{entryId}/cargo-unit-breakdown` (nuevo)

- **Política:** `ForeignTradeAccess`. Depósito en Borrador.
- **Petición** (todas las unidades del camión):

```jsonc
{ "units": [
    { "warehouseStorageCargoUnitId": "guid",
      "products": [ { "warehouseStorageProductId": "guid", "declaredQuantity": 5 } ] }
  ],
  "reason": "string (10 a 500)" }
```

- **Respuesta 200:** `data` = lista de unidades del camión con su mercancía (misma forma que el `CargoUnitDto` actual: unidad, tipo, placa, estado y `products` con declarado, reservado y despachado).
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Solo se pueden editar los productos de un depósito en Borrador." |
| 400 | "La unidad de carga {placa} no pertenece al camión indicado." |
| 400 | "Envíe el reparto de todas las unidades de carga del camión." |
| 400 | "La unidad de carga {placa} no tiene mercancía." |
| 400 | "La cantidad declarada de la unidad {placa} debe ser mayor a cero." |
| 400 | "El producto está repetido en la unidad {placa}." |
| 400 | "«{producto}» no está declarado en este camión." |
| 400 | "La suma de «{producto}» en las unidades ({x}) no coincide con lo declarado del camión ({y})." |
| 400 | "No se puede cambiar la mercancía de la unidad {placa}: tiene cantidades reservadas o despachadas." |
| 400 | "El motivo debe tener entre 10 y 500 caracteres." |
| 404 | "El camión no pertenece a este depósito." |

### C-F1-12 · `POST weighbridge/{storage|weighing-only|output}/process-payment` (modificado)

- **Política:** `ScaleAccess`.
- **Petición:** agrega `cashReceived` (decimal \| null). Solo con `paymentMethod = "Cash"`.
- **Respuesta 200** (`ProcessPaymentResponseDto`):
  - `changeAmount` ahora se llena: `cashReceived − totalAmount`, redondeado a 2 decimales; 0 si no vino efectivo.
  - Campo nuevo `cashReceived` (decimal \| null).
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El efectivo recibido solo aplica a pagos en efectivo." |
| 400 | "El efectivo recibido no puede ser negativo." |
| 400 | "El efectivo recibido ({x:N0}) es menor que el total a pagar ({y:N0})." |

- **Otros DTO:** los pagos de factura (`GET billing/invoices/{id}`, `GET billing/invoices/{id}/payments`) y el detalle del ciclo de báscula agregan `cashReceived` y `changeGiven` (decimal \| null).

---

## 3. Fase 2 — Control aduanero

### C-F2-01 · `POST foreign-trade/imports/{id}/releases` (modificado)

- **Política:** `ForeignTradeAccess`. `{id}` = `importWarehouseStorageId`.
- **Petición** (campos nuevos al final):

```jsonc
{ "warehouseStorageProductId": "guid",
  "releaseNumber": "string", "releaseDate": "datetime",
  "acceptanceNumber": "string", "acceptanceDate": "datetime",
  "releasedQuantity": 10, "releasedWeight": 1200.5, "observations": "string | null",
  "fobUsd": 1000.00,              // nuevo, opcional, ≥ 0, 2 decimales; 0 o null = sin FOB
  "manualExchangeRate": 3900.25 } // nuevo, opcional, > 0; solo se usa si la DIAN no responde
```

- **Respuesta:** sin cambio de forma. Cada levante del detalle trae los campos de C-F2-06.
- **Reglas visibles:**
  - El tope es por **producto**: recibido − otros levantes del producto. Ya no depende del stock actual.
  - En un depósito con varios productos se registran los levantes de cada uno.
  - La tasa es la TRM de la DIAN del día y queda congelada.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "La cantidad a levantar ({q}) supera lo pendiente por nacionalizar del producto ({p})." |
| 400 | "No se pudo consultar la TRM de la DIAN. Digite la tasa de cambio para registrar el FOB." |
| 409 | "El número de levante {n} ya está registrado en el depósito {m}." |
| 409 | "El número de aceptación {a} ya está registrado en el depósito {m}." |
| 409 | "El levante {n} ya está registrado para este producto." |
| 409 | "El levante {n} ya está registrado en este depósito con la aceptación {a}; use el mismo número de aceptación." |
| 409 | "La aceptación {a} ya está registrada en este depósito con el levante {n}; use el mismo número de levante." |

- **Se elimina:** "El depósito ya está completamente nacionalizado."
- **Permitido:** el mismo número y aceptación para **otro producto** del mismo depósito, porque un levante de la DIAN cubre varios productos.

### C-F2-02 · `PATCH foreign-trade/imports/{id}/releases/{releaseId}` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Petición:** la misma de C-F2-01, con `fobUsd` y `manualExchangeRate`.
  - Si cambia `fobUsd`, el FOB en pesos se recalcula con la **tasa ya guardada**, que no cambia.
  - `fobUsd` 0 o null borra el FOB.
- **Errores:** los de C-F2-01, más 409 "No se puede reducir el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida."

### C-F2-03 · `POST foreign-trade/loading-orders` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Petición:**
  - `destinationCityId` (string GUID) **obligatorio, nuevo**. El texto `destinationCity` se ignora: el backend guarda el nombre de la ciudad.
  - `crewId` (string GUID \| null) **opcional, nuevo**, desde la fase 4 (C-F4-23).
  - El resto sin cambio.
- **Errores nuevos:**

| Status | Mensaje |
|---|---|
| 400 | "Seleccione la ciudad de destino." |
| 404 | "La ciudad de destino no existe o está inactiva." |
| 400 | "La cantidad solicitada de «{producto}» en el depósito {número} ({solicitado}) supera lo nacionalizado disponible ({disponible}). Registre el levante antes de despachar." |

- **Nota:** en importación, la cantidad por producto no puede superar `nationalizedAvailable` de C-F2-04.

### C-F2-04 · `GET foreign-trade/loading-orders/deposits` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Respuesta:** cada producto del depósito agrega:
  - `nationalizedQuantity` (decimal \| null): suma de sus levantes;
  - `nationalizedAvailable` (decimal \| null): lo que aún se puede despachar.
  - Ambos son `null` en exportación e inspección.
- **Nota:** limite la cantidad del producto al menor entre su disponible y `nationalizedAvailable`.

### C-F2-05 · `POST foreign-trade/imports/{id}/releases/{releaseId}/withdraw` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Petición:** `{ "reason": "string (10 a 500)" }`
- **Respuesta 200:** el detalle del depósito de importación (la misma forma de `GET foreign-trade/imports/{id}`).
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "No se pueden retirar levantes de un depósito anulado." |
| 400 | "El motivo del retiro debe tener entre 10 y 500 caracteres." |
| 404 | "El levante no existe o no pertenece a este depósito." |
| 409 | "No se puede retirar el levante: ya se despacharon o reservaron {x} unidades nacionalizadas de «{producto}». Revierta o cancele primero la salida." |

- **Nota:** un levante de varios productos se retira producto por producto. Si el depósito queda sin nacionalizar, Comercio Exterior recibe el aviso de reimprimir la etiqueta.

### C-F2-06 · `GET foreign-trade/imports/{id}` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Cada levante** (`ImportReleaseDto`) agrega:

```jsonc
{ "fobUsd": 1000.00, "exchangeRate": 3900.25, "exchangeRateSource": "Dian", // o "Manual"
  "exchangeRateDate": "2026-09-29", "fobCop": 3900250 }                     // todos null si no hay FOB
```

- **El depósito** agrega la prórroga (C-F2-11): `extensionRegisteredAt` (datetime \| null), `extensionRegisteredByName` (string \| null), `extensionNotes` (string \| null).

### C-F2-07 · Ciudades (nuevo)

- **Política:** lectura para cualquier usuario autenticado; escritura `AdminOnly`.
- **`CityDto`:**

```jsonc
{ "id": "guid", "legacyId": 4956, "name": "IPIALES", "countryCode": "COL", "district": "NARIÑO",
  "transitDays": 3, "isAbandonmentDestination": false, "isActive": true,
  "createdAt": "datetime", "updatedAt": "datetime | null" }
```

| Verbo y ruta | Petición | Respuesta |
|---|---|---|
| `GET administration/cities` | query: `search`, `countryCode`, `isActive`, `isAbandonmentDestination`, paginado y `all` | lista de `CityDto` |
| `POST administration/cities` | `{ name, countryCode, district?, transitDays?, isAbandonmentDestination }` | 201 `CityDto` |
| `PUT administration/cities/{id}` | `{ name, countryCode, district?, transitDays?, isAbandonmentDestination, isActive }` | 200 `CityDto` |
| `DELETE administration/cities/{id}` | — | 204 |
| `POST administration/cities/import` | multipart: `file` (CSV `id_ciudad;nom_ciudad;id_pais;distrito;dias`, separador `;` o `,`), `headerRows` (≥ 0, por defecto 1), `dryRun` (bool, por defecto true) | `{ dryRun, totalRows, created, updated, errors: [ { row, message } ] }` |

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El nombre de la ciudad es obligatorio y no puede exceder 35 caracteres." |
| 400 | "El país debe ser un código de 3 letras." |
| 400 | "El distrito no puede exceder 20 caracteres." |
| 400 | "Los días de tránsito deben estar entre 0 y 99." |
| 409 | "Ya existe la ciudad {nombre} ({país}, {distrito})." |
| 409 | "La ciudad está en uso en órdenes de cargue; desactívela en lugar de eliminarla." |
| import | errores por fila con el prefijo "Fila {n}: ", por ejemplo "Fila 2: el id de la ciudad no es un número entero." |

- **Nota:** el *select* de destino usa `GET administration/cities?isActive=true&all=true`.

### C-F2-08 · `POST warehouse/loading-orders` (modificado)

- **Política:** `WarehouseAccess`.
- **Cambios y errores:** los mismos de C-F2-03 (`destinationCityId` obligatorio; `crewId` desde la fase 4).

### C-F2-09 · Detalle y listados de órdenes de cargue (modificado)

- **Rutas:** `GET foreign-trade/loading-orders`, `GET foreign-trade/loading-orders/{id}`, `GET warehouse/loading-orders/{id}` y `GET warehouse/loading-orders/pending`.
- **Campo nuevo:** `destinationCityId` (guid \| null). `destinationCity` sigue siendo el nombre.
- Las fases 3 y 4 agregan más campos (C-F3-01, C-F3-08, C-F4-23).

### C-F2-10 · `POST foreign-trade/dispatch-guides` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Petición:** `expirationDate` pasa a ser **opcional** (datetime \| null).
  - Si la ciudad de la orden tiene días de tránsito (> 0), el vencimiento es la salida + esos días, a la misma hora, y el valor enviado se ignora.
  - Si no, es obligatorio y posterior a la salida.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Indique la fecha de vencimiento: la ciudad de destino {nombre} no tiene días de tránsito." |
| 400 | "Indique la fecha de vencimiento: la orden no tiene ciudad de destino." |
| 400 | "La fecha de vencimiento debe ser posterior a la fecha de salida." |

- **Nota:** muestre el vencimiento calculado (salida + días de la ciudad) antes de emitir. La guía de exportación automática vence a `ahora + días de la ciudad`, o a 30 días si la ciudad no los tiene.

### C-F2-11 · `POST foreign-trade/imports/{id}/extension` (nuevo)

- **Política:** `ForeignTradeAccess`. `{id}` = `importWarehouseStorageId`.
- **Petición:** `{ "notes": "string | null" }` (hasta 500).
- **Respuesta 200:**

```jsonc
{ "data": { "importWarehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
            "extensionRegisteredAt": "datetime", "extensionRegisteredByName": "string",
            "extensionNotes": "string | null", "deadlineDays": 60 } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Solo los depósitos de importación en Borrador o Confirmado admiten prórroga." |
| 400 | "El depósito {n} no tiene mercancía sin nacionalizar." |
| 400 | "Las notas de la prórroga no pueden exceder 500 caracteres." |
| 409 | "El depósito {n} ya tiene prórroga registrada el {dd/MM/yyyy} por {usuario}." |

- **Nota:** es irreversible. Pida confirmación en la interfaz.

### C-F2-12 · `GET foreign-trade/abandonment` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `status` (`EnAlerta`, `EnAbandono` o `EnPlazo`), `hasExtension` (bool), `warehouseStorageNumber`, `cargoManifestNumber`, `importerId`, `customsAgencyId`, paginado y `all`.
- **Universo:** depósitos de importación en Borrador o Confirmado, con mercancía sin nacionalizar > 0 y 20 días o más desde el ingreso.
- **Orden:** días faltantes ascendente.
- **Fila:**

```jsonc
{ "importWarehouseStorageId": "guid", "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
  "cargoManifestNumber": "CP-123", "entryDate": "datetime",
  "daysElapsed": 22, "deadlineDays": 30, "daysRemaining": 8,   // negativo si ya venció
  "status": "EnAlerta", "hasExtension": false, "extensionRegisteredAt": "datetime | null",
  "importerName": "string | null", "customsAgencyName": "string | null", "customerName": "string | null",
  "pendingToNationalize": 120, "currentStock": 150 }
```

- **Estados:**
  - `EnAlerta`: 20 a 30 días sin prórroga, o 50 a 60 con prórroga.
  - `EnAbandono`: más del plazo (30 o 60).
  - `EnPlazo`: el resto.
- **Nota:** resalte `daysRemaining ≤ 10`, como el legacy.

### C-F2-13 · `GET foreign-trade/abandonment/summary` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Respuesta 200:** `{ "data": { "inAlert": 3, "abandoned": 1 } }`, para el aviso del tablero.
- **Nota:** además, un job envía cada día a las 07:00 una notificación a Comercio Exterior, título "Depósitos en ventana de abandono", tipo `AbandonmentReport`.

### C-F2-14 · `GET reports/abandonment-candidates` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `importerId`, paginado y `all`.
- **Qué incluye:** productos con existencias > 0 y sin nacionalizar > 0, de depósitos con 30 días o más sin prórroga, o 60 o más con prórroga.
- **Respuesta:**

```jsonc
{ "data": {
    "items": [ { "days": 35, "hasExtension": false, "productName": "CEBOLLA", "packagingName": "BULTO",
                 "unitMeasure": "UNIDAD", "entryDate": "datetime", "warehouseStorageNumber": "2026BA00012",
                 "manifestNumber": "string | null", "manifestDate": "datetime | null",
                 "importerName": "string | null", "customsAgencyName": "string | null",
                 "receivedQuantity": 10, "currentStock": 8, "pendingToNationalize": 6 } ],
    "totals": { "receivedQuantity": 15, "currentStock": 13, "pendingToNationalize": 11 } },
  "pagination": { … } }
```

### C-F2-15 · `GET reports/abandonment-exits` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `fromDate` y `toDate` (`yyyy-MM-dd`; por defecto del 1 de enero del año actual a hoy), paginado y `all`.
- **Qué incluye:** órdenes cargadas cuya ciudad de destino está marcada como «Destino de abandono».
- **Fila:**

```jsonc
{ "loadingDate": "datetime", "loadingOrderNumber": "OC-…", "guideNumber": "string | null",
  "vehiclePlate": "ABC123", "driverName": "string", "transportCompanyName": "string | null",
  "customerName": "string", "customsAgencyName": "string | null",
  "warehouseStorageNumber": "2026BA00012", "cargoManifestNumber": "CP-123", "manifestNumber": "string | null",
  "releaseNumbers": "LEV-1, LEV-2", "productName": "CEBOLLA", "quantity": 10 }
```

- **Nota:** desde la fase 3, `quantity` es la cantidad **cargada**.

---

## 4. Fase 3 — Correcciones y facturación

### C-F3-01 · `POST warehouse/loading-orders/{id}/execute` (modificado)

- **Política:** `WarehouseAccess`.
- **Petición:**
  - `items[].loadedQuantity` admite **0**.
  - Un ítem que no se envía cuenta como 0.
  - Lo no cargado **libera su reserva**.
- **Respuesta:** cada ítem del resultado (`LoadingItemResultDto`) cambia así:

```jsonc
{ "loadingOrderItemId": "guid", "warehouseStorageProductId": "guid", "warehouseStorageId": "guid",
  "warehouseStorageNumber": "2026BA00012",
  "orderedQuantity": 10,          // nuevo
  "loadedQuantity": 6,
  "previousStock": 20, "newStock": 14,
  "reservedStockReleased": 10,    // ahora la reserva completa del ítem (lo pedido)
  "inventoryMovementId": "guid | null" }   // null si no se cargó nada
```

  El resultado incluye **todos** los ítems de la orden, también los no enviados. La fase 4 agrega `releasedPlacements` (C-F4-07).
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "No se cargó mercancía: cancele la orden en lugar de ejecutarla." |
| 400 | "La cantidad a cargar ({q}) excede la cantidad solicitada ({pedida}) para el producto '{p}'." |
| 400 | "La cantidad cargada no puede ser negativa." |

- **Detalle de la orden** (C-F2-09): cada ítem agrega `loadedQuantity` (decimal \| null).
- **Guía** emitida después del cargue: sale con la cantidad cargada.

### C-F3-02 · Cancelar orden de cargue (modificado)

- **Rutas:** `PATCH foreign-trade/loading-orders/{id}/cancel` (`ForeignTradeAccess`) y `PATCH warehouse/loading-orders/{id}/cancel` (`WarehouseAccess`).
- **Petición:** `{ "reason": "string" }`. **Ahora obligatorio**, de 10 a 500 caracteres.
- **Respuesta:** sin cambio.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El motivo de la cancelación debe tener entre 10 y 500 caracteres." |
| 409 | "La orden {n} ya fue cargada: use «Revertir salida»." (orden `Loaded`, `Dispatched` o `Complete`) |
| 409 | "La orden {n} ya está cancelada." |
| 409 | "La orden {n} fue revertida." |

- **Nota:** solo se cancela antes del cargue (`Pending` o `InProgress`). Si estaba en cargue, Bodega recibe un aviso.

### C-F3-03 · `PUT foreign-trade/loading-orders/{id}/items` (nuevo)

- **Política:** `ForeignTradeAccess`. Orden `Pending` o `InProgress`.
- **Petición** (la lista reemplaza a la actual):

```jsonc
{ "items": [
    { "loadingOrderItemId": "guid",               // ítem existente: se ajusta la cantidad
      "warehouseStorageProductId": "guid", "warehouseStorageCargoUnitId": "guid | null", "quantity": 8 },
    { "loadingOrderItemId": null,                 // ítem nuevo
      "warehouseStorageProductId": "guid", "warehouseStorageCargoUnitId": null, "quantity": 3 }
  ],
  "reason": "string (10 a 500)" }
```

  Un ítem existente que no viene se retira y libera su reserva.
- **Respuesta 200:** el detalle de la orden (misma forma de `GET foreign-trade/loading-orders/{id}`).
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "La orden debe conservar al menos un ítem; si ya no sale mercancía, cancélela." |
| 400 | "El ítem {id} no pertenece a la orden." |
| 400 | "La cantidad debe ser mayor a cero." |
| 400 | "El motivo de la modificación debe tener entre 10 y 500 caracteres." |
| 400 | los de C-F2-03: nacionalizado disponible, stock y depósito |
| 409 | "Solo se pueden modificar órdenes pendientes o en cargue; la orden {n} está {estado}." |

### C-F3-04 · `POST foreign-trade/dispatch-guides/{id}/cancel` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Petición:** `{ "reason": "string (10 a 500)" }`
- **Respuesta 200:**

```jsonc
{ "data": {
    "dispatchGuideId": "guid", "guideNumber": "GS-…", "cancelledAt": "datetime",
    "cancelledInvoices": [ { "invoiceId": "guid", "invoiceNumber": "string | null" } ],
    "invoicesToReview": [ { "invoiceId": "guid", "invoiceNumber": "string | null", "status": "Approved", "total": 23000 } ] } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El motivo de la anulación debe tener entre 10 y 500 caracteres." |
| 404 | "La guía no existe." |
| 409 | "La guía {n} ya está anulada." |

- **Guías en listados, detalle y ZIP:** agregan `isCancelled` (bool), `cancelledAt` (datetime \| null) y `cancellationReason` (string \| null). El PDF de una guía anulada lleva la marca "ANULADA".
- **Nota:** tras anular la guía se puede emitir otra para la misma orden, o revertir la salida (C-F3-08). Las facturas aprobadas o pagadas no se tocan: Facturación recibe aviso.

### C-F3-05 · `GET billing/configurations/cycles` (nuevo)

- **Política:** `BillingAccess`.
- **Respuesta 200:**

```jsonc
{ "data": [
  { "value": "Weekly",   "label": "Semanal (7 días)",         "days": 7 },
  { "value": "Biweekly", "label": "Quincenal (14 días)",      "days": 14 },
  { "value": "Days15",   "label": "Quincenal (15 días)",      "days": 15 },
  { "value": "Monthly",  "label": "Mensual (mes calendario)", "days": null },
  { "value": "Days30",   "label": "Mensual (30 días)",        "days": 30 },
  { "value": "Days90",   "label": "Trimestral (90 días)",     "days": 90 },
  { "value": "Days180",  "label": "Semestral (180 días)",     "days": 180 },
  { "value": "Days360",  "label": "Anual (360 días)",         "days": 360 },
  { "value": "OnDemand", "label": "Bajo demanda",             "days": null } ] }
```

### C-F3-06 · `PUT billing/configurations/{stakeholderId}` (modificado)

- **Política:** `BillingAccess`.
- **Petición:** `billingCycle` acepta los nueve valores de C-F3-05. El resto sin cambio: `paymentTermDays`, `invoicingPreference` y `creditLimit`.
- **Nota:** arme el *select* con C-F3-05.

### C-F3-07 · Períodos de almacenamiento (modificado)

- **Rutas:** `GET billing/storage-periods` y `GET billing/storage-periods/{id}` (`BillingAccess`).
- **Campo nuevo:** `limitDate` (`yyyy-MM-dd` \| null): fecha límite = fin + 3 días. Nulo solo en períodos creados antes del cambio.
- **Significado de las fechas** en los períodos nuevos:
  - `periodStart` y `periodEnd` son las 00:00 de Colombia del día de inicio y del día de fin. El fin es inclusivo.
  - Un período de 15 días que empieza el 01/01 termina el 16/01; el siguiente empieza el 17/01.
  - Muestre las fechas como días (`dd/MM/yyyy`).
- **Renovación:** el período se renueva el día siguiente a la fecha límite si el depósito aún tiene mercancía. Si se vacía hasta la fecha límite, no se renueva.

### C-F3-08 · `POST foreign-trade/loading-orders/{id}/revert` (nuevo)

- **Política:** `ForeignTradeAccess`. Orden `Loaded`, `Dispatched` o `Complete`, sin guía vigente.
- **Petición:** `{ "reason": "string (10 a 500)" }`
- **Respuesta 200:**

```jsonc
{ "data": {
    "loadingOrderId": "guid", "orderNumber": "OC-…", "status": "Reverted",
    "returnedItems": [ { "warehouseStorageProductId": "guid", "warehouseStorageNumber": "2026BA00012",
                         "productName": "CEBOLLA", "quantity": 6 } ],
    "reopenedDeposits": [ "2026BA00012" ] } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El motivo de la reversión debe tener entre 10 y 500 caracteres." |
| 409 | "Solo se revierte una orden ya cargada; la orden {n} está {estado}." |
| 409 | "Anule primero la guía {g} de la orden {n}." |
| 400 | "La devolución dejaría más stock que la cantidad del depósito." |

- **Orden:** estado nuevo `Reverted`; el detalle agrega `revertedAt` (datetime \| null) y `reversalReason` (string \| null).
- **Nota:** la mercancía devuelta queda «por ubicar» (fase 4). Bodega recibe el aviso.

### C-F3-09 · `POST foreign-trade/warehouse-storages/{id}/cancel` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Petición:** `{ "reason": "string" }`. **Ahora obligatorio**, de 10 a 500 caracteres.
- **Respuesta 200:**

```jsonc
{ "data": {
    "warehouseStorageId": "guid", "status": "Cancelled",
    "removedOrderItems": 2,
    "cancelledOrders": [ "OC-…" ],
    "closedPeriods": 1,
    "cancelledInvoices": [ { "invoiceId": "guid", "invoiceNumber": "string | null" } ],
    "invoicesToReview": [ { "invoiceId": "guid", "invoiceNumber": "string | null", "status": "Paid", "total": 150000 } ] } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El motivo de la anulación debe tener entre 10 y 500 caracteres." |
| 400 | "No se puede anular un depósito cerrado." |
| 400 | "El depósito ya está anulado." |
| 409 | "El depósito {n} tiene salidas ejecutadas en la orden {o}. Revierta primero la salida." |
| 409 | "El camión {placa} del depósito {n} aún está en báscula. Termine o anule el pesaje antes de anular el depósito." |

- **Depósito:** el detalle agrega `cancelledAt` y `cancellationReason`.
- **Nota:** un camión nuevo con la misma carta porte crea otro depósito.

### C-F3-10 · `POST weighbridge/cycles/{cycleId}/void` (nuevo)

- **Política:** `ScaleAccess`.
- **Petición:** `{ "reason": "string (10 a 500)" }`
- **Respuesta 200:**

```jsonc
{ "data": {
    "weighbridgeCycleId": "guid", "ticketNumber": "string | null",
    "kind": "StorageInput",                                    // StorageInput (ingreso a depósito), Output (salida con orden) o WeighingOnly (solo báscula)
    "voidedEntries": [ { "warehouseStorageNumber": "2026BA00012", "vehiclePlate": "ABC123" } ],
    "cancelledDeposits": [ "2026BA00012" ],                    // depósitos que quedaron sin camiones
    "revertedOrders": [ "OC-…" ],                              // salidas que volvieron a «Cargada»
    "cancelledInvoices": [ { "invoiceId": "guid", "invoiceNumber": "string | null" } ],
    "invoicesToReview": [ { "invoiceId": "guid", "invoiceNumber": "string | null", "status": "Paid", "total": 23000 } ] } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El motivo de la anulación debe tener entre 10 y 500 caracteres." |
| 409 | "El pesaje ya está anulado." |
| 409 | "No se puede anular el pesaje: la mercancía del camión {placa} en el depósito {n} tiene {x} unidades reservadas o despachadas de «{producto}». Revierta o cancele primero la orden {orden}." (sin orden vigente, termina en "de «{producto}».") |
| 409 | "No se puede anular el pesaje: los levantes de «{producto}» ({x}) superarían la cantidad que queda en el depósito {n} ({y}). Retire primero el levante." |
| 409 | "No se puede anular el pesaje: la unidad de carga {placa} tiene mercancía reservada o despachada." |
| 409 | "La orden {n} está completa; revierta la salida antes de anular el pesaje." |
| 409 | "El tiquete {t} se usó para la salida de la orden {o}; revierta o cancele primero esa orden." (desde la fase 4) |

- **Notas:**
  - La misma entrada de portería vuelve a la cola y se puede pesar de nuevo.
  - Anular un pesaje de salida no devuelve la mercancía: para eso está C-F3-08.

### C-F3-11 · `GET weighbridge/history` (modificado)

- **Política:** `ScaleAccess`.
- **Cada fila agrega:** `isVoided` (bool), `voidedAt` (datetime \| null) y `voidReason` (string \| null).
- Las fases 4 y 5 agregan más campos (C-F4-18, C-F4-19, C-F5-11).

### C-F3-12 · `PATCH billing/invoices/{id}/cancel` (modificado)

- **Política:** `BillingAccess`. Petición, respuesta y errores sin cambio.
- **Efecto nuevo:** si la factura tenía períodos de almacenamiento, quedan «por refacturar» y Facturación recibe el aviso. Use C-F3-13.

### C-F3-13 · `POST billing/invoices/{id}/reissue` (nuevo)

- **Política:** `BillingAccess`. Sin cuerpo.
- **Respuesta 201:** el detalle de la **factura nueva**, en Borrador y sin número (misma forma de `GET billing/invoices/{id}`).
- **Errores:**

| Status | Mensaje |
|---|---|
| 409 | "Solo se puede refacturar una factura anulada; la factura {n} está {estado}." |
| 409 | "La factura {n} ya fue refacturada como {m}." |
| 400 | "La factura {n} no tiene períodos de almacenamiento; genere de nuevo el cobro desde su operación." |

- **`InvoiceDetailDto`** agrega `reissuedFromInvoiceId` y `reissuedAsInvoiceId` (guid \| null).
- **Nota:** muestre el botón «Refacturar» solo en facturas anuladas con `reissuedAsInvoiceId` nulo y con líneas de almacenamiento.

### C-F3-14 · `GET billing/pending-deposits` (modificado)

- **Política:** `BillingAccess`.
- **Cada fila agrega** `periodsPendingReissue` (int): períodos cuya factura está anulada y sin refacturar.

---

## 5. Fase 4 — Bodega y mercancía

### Forma común de ubicaciones (`ProductPlacementsDto`)

```jsonc
{ "warehouseStorageProductId": "guid", "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
  "productName": "CEBOLLA", "currentStock": 10, "placedQuantity": 6, "pendingToPlace": 4,
  "mainLocationId": "guid | null",
  "placements": [ { "warehouseLocationId": "guid", "locationCode": "A-01", "locationName": "A-01",
                    "quantity": 6, "lastPlacedAt": "datetime" } ] }
```

### C-F4-01 · `GET warehouse/storage-products/{id}/placements` (nuevo)

- **Política:** `WarehouseAccess`.
- **Respuesta 200:** `ProductPlacementsDto`.
- **Error:** 404 "El producto del depósito no existe."

### C-F4-02 · `POST warehouse/storage-products/{id}/placements` (nuevo) — ubicar

- **Política:** `WarehouseAccess`.
- **Petición:** `{ "warehouseLocationId": "guid", "quantity": 4 }`
- **Respuesta 200:** `ProductPlacementsDto` actualizado.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "La cantidad a ubicar debe ser mayor que cero." |
| 404 | "El producto del depósito no existe." |
| 404 | "La ubicación no existe." |
| 409 | "No se puede ubicar {q}: solo quedan {p} por ubicar." |
| 409 | "La ubicación {código} está deshabilitada." |
| 409 | "El depósito {n} está {estado}; no se puede ubicar mercancía." |

### C-F4-03 · `POST warehouse/storage-products/{id}/placements/move` (nuevo) — mover

- **Política:** `WarehouseAccess`.
- **Petición:** `{ "fromLocationId": "guid", "toLocationId": "guid", "quantity": 2 }`
- **Respuesta 200:** `ProductPlacementsDto` actualizado.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "La ubicación de destino debe ser distinta de la de origen." |
| 400 | "La cantidad a mover debe ser mayor que cero." |
| 404 | "El producto no está ubicado en {código}." |
| 404 | "La ubicación no existe." |
| 409 | "En {código} solo hay {x} unidades ubicadas." |
| 409 | "La ubicación {código} está deshabilitada." |

### C-F4-04 · `POST warehouse/storage-products/{id}/placements/release` (nuevo) — liberar

- **Política:** `WarehouseAccess`.
- **Petición:** `{ "warehouseLocationId": "guid", "quantity": 2 }`
- **Respuesta 200:** `ProductPlacementsDto` actualizado. Lo liberado vuelve a «por ubicar».
- **Errores:** "La cantidad a liberar debe ser mayor que cero." (400), "El producto no está ubicado en {código}." (404) y "En {código} solo hay {x} unidades ubicadas." (409).

### C-F4-05 · `GET warehouse/locations/{id}/placements` (nuevo)

- **Política:** `WarehouseAccess`.
- **Respuesta 200:**

```jsonc
{ "data": { "warehouseLocationId": "guid", "code": "A-01", "name": "A-01", "isAvailable": true,
            "totalQuantity": 16,
            "items": [ { "warehouseStorageProductId": "guid", "warehouseStorageNumber": "2026BA00012",
                         "productName": "CEBOLLA", "quantity": 6, "lastPlacedAt": "datetime" } ] } }
```

- **Error:** 404 "La ubicación no existe."

### C-F4-06 · Recepción (modificado)

- **Rutas:** `POST warehouse/receptions`, `POST warehouse/receptions/{id}/complete` y `POST warehouse/receptions/without-weighbridge` (`WarehouseAccess`).
- **Efecto nuevo:** cuando un producto trae ubicación, además de asignarla se **ubica** la cantidad descargada (hasta lo pendiente por ubicar).
- **Error nuevo:** 409 "La ubicación {código} está deshabilitada."
- **Petición:** agrega `crewId` (string GUID \| null), la cuadrilla que descargó (C-F4-23).

### C-F4-07 · `POST warehouse/loading-orders/{id}/execute` (modificado)

- **Política:** `WarehouseAccess`.
- **Petición:** agrega `crewId` (string GUID \| null). Si viene, reemplaza la cuadrilla de la orden.
- **Respuesta:** cada ítem agrega las posiciones liberadas, de la más reciente a la más antigua:

```jsonc
"releasedPlacements": [ { "warehouseLocationId": "guid", "locationCode": "B-02", "quantity": 3 } ]
```

  Úselas para indicar al operario de dónde retirar.
- **Error nuevo:** 404 "La cuadrilla no existe o está inactiva."

### Forma común de novedades (`WarehouseNoveltyDto`)

```jsonc
{ "id": "guid", "warehouseStorageProductId": "guid", "warehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
  "productName": "CEBOLLA", "warehouseStorageEntryId": "guid | null", "vehiclePlate": "string | null",
  "type": "Routine",                       // Entry, Exit, Transshipment, Routine, Inspection
  "startedAt": "datetime", "endedAt": "datetime", "orderedBy": "string | null",
  "description": "string",
  "totalQuantity": 10, "goodQuantity": 7, "damagedQuantity": 2, "missingQuantity": 1, "surplusQuantity": 0,
  "isUnloaded": true, "unloadedQuantity": 10, // = totalQuantity si isUnloaded; si no, 0
  "tarpCondition": "Good | Holed | Torn | NoTarp | null",
  "trailerCondition": "Clean | Dirty | Rusty | Wet | Broken | null",
  "photoRecord": "string | null",
  "createdByName": "string", "createdAt": "datetime", "updatedAt": "datetime | null",
  "isVoided": false, "voidedAt": "datetime | null", "voidReason": "string | null" }
```

**Rótulos sugeridos (los del legacy):**

| Grupo | Valores |
|---|---|
| Tipo | Entry = Ingreso, Exit = Salida, Transshipment = Trasbordo, Routine = Rutina (por defecto), Inspection = Inspección y muestras |
| Carpa | Good = Buena, Holed = Agujereada, Torn = Rota, NoTarp = Sin carpa |
| Remolque | Clean = Limpio, Dirty = Sucio, Rusty = Oxidado, Wet = Mojado, Broken = Roto |

### C-F4-08 · `POST warehouse/novelties` (nuevo)

- **Política:** `WarehouseAccess`.
- **Petición:** los campos editables de `WarehouseNoveltyDto`:
  - obligatorios: `warehouseStorageProductId`, `type`, `startedAt`, `endedAt`, `description`, `totalQuantity`;
  - con valor por defecto 0: las cuatro cantidades del desglose;
  - booleano: `isUnloaded`;
  - opcionales: `warehouseStorageEntryId`, `orderedBy` (hasta 100), `tarpCondition`, `trailerCondition` y `photoRecord` (hasta 200).
- **Precarga sugerida:** `totalQuantity` = existencias del producto.
- **Respuesta 201:** `WarehouseNoveltyDto`.
- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Seleccione el tipo de novedad." |
| 400 | "La descripción de la novedad es obligatoria." |
| 400 | "La descripción no puede exceder 4000 caracteres." |
| 400 | "La fecha de fin no puede ser anterior a la de inicio." |
| 400 | "Las cantidades no pueden ser negativas." |
| 400 | "El camión no pertenece al depósito del producto." |
| 409 | "El depósito {n} está anulado." |

- **Nota:** con dañada, faltante o sobrante > 0, Comercio Exterior recibe un aviso. No hay regla de suma ni fotos.

### C-F4-09 · `PUT warehouse/novelties/{id}` (nuevo)

- **Política:** `WarehouseAccess`.
- **Petición:** la de C-F4-08 sin `warehouseStorageProductId`.
- **Respuesta 200:** `WarehouseNoveltyDto`.
- **Errores:** los de C-F4-08, más 409 "La novedad está anulada."

### C-F4-10 · `POST warehouse/novelties/{id}/void` (nuevo)

- **Política:** `WarehouseAccess`.
- **Petición:** `{ "reason": "string (10 a 500)" }`
- **Respuesta 200:** `WarehouseNoveltyDto`.
- **Errores:** 400 "El motivo de la anulación debe tener entre 10 y 500 caracteres."; 409 "La novedad ya está anulada."

### C-F4-11 · Consultar novedades (nuevo)

- **Política:** cualquier usuario autenticado.
- **`GET warehouse/novelties`:** query `warehouseStorageId`, `warehouseStorageProductId`, `type`, `from` y `to` (`yyyy-MM-dd`, por fecha de inicio), `includeVoided` (por defecto false), paginado y `all`. Devuelve lista de `WarehouseNoveltyDto`.
- **`GET warehouse/novelties/{id}`:** `WarehouseNoveltyDto`; 404 "La novedad no existe."

### C-F4-12 · `GET warehouse/novelties/{id}/pdf` (nuevo)

- **Política:** cualquier usuario autenticado.
- **Respuesta:** `application/pdf`, archivo `novedad_{depósito}_{yyyyMMdd}.pdf`. Es el «REPORTE DE MERCANCÍAS», con firmas; una novedad anulada lleva la marca "ANULADA".
- **Error:** 404 "La novedad no existe."

### C-F4-13 · Proveedores de listas de empaque (nuevo)

- **Política:** `ForeignTradeAccess`.
- **`GET foreign-trade/packing-list-suppliers`:** `[ { "id": "guid", "name": "string", "isActive": true } ]`.
- **`POST foreign-trade/packing-list-suppliers`:** `{ "name": "string (1 a 200)" }` → 201 con el proveedor.
- **Error:** 409 "Ya existe el proveedor {nombre}."

### C-F4-14 · `POST foreign-trade/packing-lists/import` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Petición** (multipart):
  - `file`: CSV con columnas `codigo;NOMBRE;CANT_BULTOS;UNID_X_BULTOS;PSO_TOTAL_NETO`. Separador `;` (o `,`); con `;` admite coma decimal. UTF-8.
  - `supplierId` y `importerId` (GUID).
  - `headerRows` (≥ 0, por defecto 1) y `dryRun` (por defecto true).
- **Respuesta 200:**

```jsonc
{ "data": {
    "dryRun": true, "packingListFileId": "guid | null",   // null en simulación
    "totalRows": 3, "validRows": 3, "productsToCreate": 2, // en firme: productos creados
    "items": [ { "row": 2, "code": "A-1", "description": "TORNILLO 3/8", "packages": 10, "unitsPerPackage": 12,
                 "quantity": 120, "netWeightKg": 25.5, "productId": "guid | null", "productName": "string",
                 "newProduct": true } ],
    "errors": [ { "row": 4, "message": "Fila 4: los bultos deben ser un número mayor que cero." } ] } }
```

- **Errores de archivo:** 404 "El proveedor no existe o está inactivo.", 404 "El importador no existe.", 400 "El archivo no tiene filas válidas.", 409 "No se pudo generar un SKU único para el código {código}."
- **Errores de fila**, en `errors[]`:
  - "Fila {n}: el código es obligatorio y no puede exceder 40 caracteres."
  - "Fila {n}: el nombre es obligatorio y no puede exceder 250 caracteres."
  - "Fila {n}: los bultos deben ser un número mayor que cero."
  - "Fila {n}: las unidades por bulto deben ser un número mayor que cero."
  - "Fila {n}: el peso neto debe ser un número mayor o igual a cero."
- **Nota:** primero simule y muestre `items` y `errors`; luego importe en firme. Un artículo nuevo crea un producto con SKU = código.

### C-F4-15 · Archivos de listas de empaque (nuevo)

- **Política:** `ForeignTradeAccess`.
- **`GET foreign-trade/packing-lists`:** query `importerId`, `supplierId`, paginado. Fila:

```jsonc
{ "id": "guid", "fileName": "lista.csv", "supplierName": "string", "importerName": "string",
  "itemCount": 3, "activeItems": 2, "associatedItems": 1, "createdByName": "string", "createdAt": "datetime" }
```

- **`GET foreign-trade/packing-lists/{id}`:** la fila anterior más `items` (lista de `PackingListItemDto`, C-F4-16).
- **`DELETE foreign-trade/packing-lists/{id}`:** 204. Error 409 "La lista {archivo} tiene artículos asociados a depósitos; no se puede eliminar."

### C-F4-16 · `GET foreign-trade/packing-list-items` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `importerId` (obligatorio), `status` (`Active` por defecto, o `Associated`), `search` (código o nombre), paginado y `all`.
- **`PackingListItemDto`:**

```jsonc
{ "id": "guid", "packingListFileId": "guid", "fileName": "string", "supplierName": "string",
  "code": "A-1", "description": "TORNILLO 3/8", "packages": 10, "unitsPerPackage": 12, "quantity": 120,
  "netWeightKg": 25.5, "productId": "guid", "productName": "TORNILLO 3/8", "productSku": "A-1",
  "status": "Active", "warehouseStorageEntryId": "guid | null", "warehouseStorageNumber": "string | null",
  "vehiclePlate": "string | null", "associatedAt": "datetime | null" }
```

### C-F4-17 · `POST foreign-trade/deposits/{id}/entries/{entryId}/packing-list-items` (nuevo)

- **Política:** `ForeignTradeAccess`. Depósito en Borrador.
- **Petición:** `{ "itemIds": ["guid"], "warehouseStorageCargoUnitId": "guid | null", "reason": "string (10 a 500)" }` (1 a 200 artículos).
- **Respuesta 200:**

```jsonc
{ "data": { "importerAssigned": false,   // true si el depósito no tenía importador y tomó el de la lista
            "products": [ { "warehouseStorageProductId": "guid", "productName": "string",
                            "declaredQuantity": 120, "entryDeclaredQuantity": 120 } ] } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Solo se pueden editar los productos de un depósito en Borrador." |
| 400 | "El camión indicado no pertenece a este depósito." |
| 400 | "El motivo de la corrección debe tener entre 10 y 500 caracteres." |
| 400 | "Los artículos deben ser de un mismo importador." |
| 400 | "Indique la unidad de carga a la que entra el producto." (depósito con unidades de carga) |
| 400 | "La unidad de carga no pertenece al camión indicado." |
| 404 | "El artículo {id} de la lista de empaque no existe." |
| 409 | "El artículo {código} ya está asociado al depósito {n}." |
| 409 | "Los artículos son de la lista del importador {x}; el depósito es del importador {y}." |

### C-F4-18 · `POST weighbridge/output/cycles/{cycleId}/additional-orders` (nuevo)

- **Política:** `ScaleAccess`.
- **Qué hace:** otras órdenes del mismo camión salen con el pesaje de salida que ya tiene, **sin cobro**.
- **Petición:** `{ "loadingOrderIds": ["guid"] }` (1 a 10).
- **Respuesta 200:**

```jsonc
{ "data": [ { "serviceRecordId": "guid", "loadingOrderId": "guid", "loadingOrderNumber": "OC-…",
              "customerName": "string", "dispatched": false } ] }   // true si ya quedó despachada
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "Se pueden agregar entre 1 y 10 órdenes." |
| 400 | "Solo se agregan órdenes a un pesaje de salida." |
| 400 | "Los depósitos de la orden {n} deben estar confirmados." |
| 404 | "El pesaje no existe." / "La orden de cargue {id} no existe." |
| 409 | "El pesaje está anulado." |
| 409 | "La orden {n} está {estado}; no se puede agregar al pesaje." |
| 409 | "La orden {n} es para el vehículo {placa orden}; el pesaje es del vehículo {placa pesaje}." |
| 409 | "La orden {n} ya tiene un servicio de salida en báscula." |

- **Historial de báscula:** la fila del pesaje agrega `additionalOrders: [ { serviceRecordId, loadingOrderId, loadingOrderNumber, customerName } ]`.

### C-F4-19 · Salida con el tiquete de ingreso (nuevo)

- **Qué hace:** la orden sale con el tiquete de ingreso del camión, **sin pesar de nuevo ni cobrar**.
- **Dos rutas, el mismo comportamiento:**

| Ruta | Política | Petición |
|---|---|---|
| `POST weighbridge/output/from-entry-ticket` | `ScaleAccess` | `{ "entryWeighbridgeCycleId": "guid", "loadingOrderId": "guid" }` |
| `POST foreign-trade/loading-orders/{id}/exit-with-entry-ticket` | `ForeignTradeAccess` | `{ "entryWeighbridgeCycleId": "guid" }`; `{id}` = la orden |

- **«Salida Global» del legacy:** cuando varios camiones de un depósito salen con sus tiquetes de ingreso, se crea una orden por camión y se llama a este endpoint por cada una. Cada camión lleva su guía y se cobra una guía por camión. No hay endpoint de lote.
- **Respuesta 200:**

```jsonc
{ "data": { "serviceRecordId": "guid", "loadingOrderId": "guid", "loadingOrderNumber": "OC-…",
            "ticketNumber": "T-…", "dispatched": false } }
```

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El tiquete {t} no es de un ingreso." |
| 404 | "El pesaje no existe." |
| 409 | "El tiquete {t} no está completo." |
| 409 | "El tiquete {t} está anulado." |
| 409 | "El tiquete {t} ya se usó para la salida de la orden {o}." |
| 409 | "La orden {n} es para el vehículo {placa orden}; el tiquete {t} es del vehículo {placa tiquete}." |
| 409 | "La orden {n} tiene mercancía del depósito {d}, que no llegó en el tiquete {t}." |
| 409 | los de estado y servicio de C-F4-18 |

- **Historial de báscula:** la fila del tiquete agrega `exitOrder: { serviceRecordId, loadingOrderId, loadingOrderNumber } | null`.

### C-F4-20 · Etiquetas (modificado)

- **Rutas:** `GET foreign-trade/imports/{id}/label`, `GET foreign-trade/exports/{id}/label` y `GET foreign-trade/inspections/{id}/label` (`ForeignTradeAccess`).
- **Query nueva:** `action` = `Print` o `Download` (por defecto `Download`). Llame con `Print` cuando el usuario imprime y con `Download` cuando descarga.
- **Error:** 400 "La acción debe ser Print o Download."

### C-F4-21 · `GET foreign-trade/warehouse-storages/{id}/label-prints` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Respuesta 200:**

```jsonc
{ "data": { "warehouseStorageId": "guid", "printCount": 3, "downloadCount": 1,
            "lastPrintedAt": "datetime | null", "lastPrintedByName": "string | null",
            "items": [ { "action": "Print", "printedByName": "string", "createdAt": "datetime" } ] } } // últimas 50
```

### C-F4-22 · Cuadrillas (nuevo)

- **Política:** lectura para cualquier usuario autenticado; escritura `AdminOnly`.
- **`CrewDto`:** `{ "id": "guid", "legacyId": 3, "name": "CUADRILLA 1", "isActive": true, "createdAt": "datetime", "updatedAt": "datetime | null" }`

| Verbo y ruta | Petición | Respuesta |
|---|---|---|
| `GET administration/crews` | query `search`, `isActive`, paginado y `all` | lista de `CrewDto` |
| `POST administration/crews` | `{ name }` | 201 `CrewDto` |
| `PUT administration/crews/{id}` | `{ name, isActive }` | 200 `CrewDto` |
| `DELETE administration/crews/{id}` | — | 204 |

- **Errores:**

| Status | Mensaje |
|---|---|
| 400 | "El nombre de la cuadrilla es obligatorio y no puede exceder 200 caracteres." |
| 409 | "Ya existe la cuadrilla {nombre}." |
| 409 | "La cuadrilla está en uso; desactívela en lugar de eliminarla." |

### C-F4-23 · Cuadrilla en recepción, órdenes, cargue y guía (modificado)

- **`crewId`** (string GUID \| null), opcional, en:
  - `POST foreign-trade/loading-orders` y `POST warehouse/loading-orders` (C-F2-03 y C-F2-08);
  - `POST warehouse/loading-orders/{id}/execute` (C-F4-07);
  - las tres rutas de recepción (C-F4-06).
- **Error:** 404 "La cuadrilla no existe o está inactiva."
- **Lecturas:**
  - el detalle y los listados de órdenes agregan `crewId` y `crewName`;
  - el detalle de los depósitos agrega `crewId` y `crewName` (quién descargó);
  - la guía ya expone `crew`, que ahora se llena con la cuadrilla de la orden al emitirla.

---

## 6. Fase 5 — Reportes y consultas

**Forma de los informes nuevos con totales:** `data: { "items": [...], "totals": {...} }` más `pagination`. Los totales cubren **todo el filtro**, no solo la página. Para el Excel use `all=true`.

**Validaciones comunes de fechas** (`fromDate`/`toDate` en `yyyy-MM-dd`, días de Colombia, inclusivos): 400 "La fecha final no puede ser anterior a la inicial."

### C-F5-01 · `GET foreign-trade/imports` (modificado)

- **Política:** `ForeignTradeAccess`.
- **Query nueva:**
  - `vehiclePlate`: algún camión del depósito con esa placa; búsqueda parcial, sin guiones ni espacios;
  - `releaseNumber`: número de levante o de aceptación; búsqueda parcial.
- **Cada fila agrega** (suma de los productos del depósito):

| Campo | Rótulo |
|---|---|
| `receivedQuantity` | Ingreso |
| `nationalizedQuantity` (existe) | Nacionalizado |
| `pendingToNationalize` | Por nacionalizar |
| `dispatchedQuantity` | Despachado |
| `currentStock` (existe) | Existencias |

- `GET foreign-trade/exports` y `GET foreign-trade/inspections` agregan `receivedQuantity`, `dispatchedQuantity` y `currentStock`.

### C-F5-02 · `GET foreign-trade/releases` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `releaseNumber` (número o aceptación), `warehouseStorageNumber`, `importerId`, `customsAgencyId`, `fromDate`/`toDate` (fecha del levante), paginado y `all`.
- **Orden:** fecha del levante descendente.
- **Fila** (una por levante de producto):

```jsonc
{ "releaseId": "guid", "releaseNumber": "LEV-1", "releaseDate": "datetime",
  "acceptanceNumber": "ACE-1", "acceptanceDate": "datetime",
  "warehouseStorageId": "guid", "importWarehouseStorageId": "guid", "warehouseStorageNumber": "2026BA00012",
  "importerName": "string | null", "customsAgencyName": "string | null", "productName": "CEBOLLA",
  "releasedQuantity": 10, "releasedWeight": 1200.5,
  "fobUsd": 1000.00, "exchangeRate": 3900.25, "fobCop": 3900250, "createdAt": "datetime" }
```

### C-F5-03 · `GET warehouse/movements-report` (modificado; kardex)

- **Política:** `ActiveUser`. Parámetros actuales: `warehouseStorageNumber`, `fromDate` y `toDate`. El PDF (`/pdf`) agrega las mismas secciones.
- **Cada producto agrega:** `receivedQuantity`, `dispatchedQuantity`, y `nationalizedQuantity`, `pendingToNationalize` y `nationalizedAvailable` (estos tres, `null` si el depósito no es de importación).
- **El informe agrega:**

```jsonc
{ "releases": [ { "releaseNumber": "LEV-1", "acceptanceNumber": "ACE-1", "releaseDate": "datetime",
                  "releasedWeight": 1200.5, "fobUsd": 1000.00,
                  "lines": [ { "warehouseStorageProductId": "guid", "quantity": 4 } ] } ],   // solo importación
  "dispatches": [ { "loadingOrderNumber": "OC-…", "departureDate": "datetime", "vehiclePlate": "ABC123",
                    "guideNumber": "string | null", "ticketNumber": "string | null",
                    "lines": [ { "warehouseStorageProductId": "guid", "quantity": 5 } ] } ],
  "totals": { "receivedQuantity": 10, "nationalizedQuantity": 7, "pendingToNationalize": 3,
              "dispatchedQuantity": 5, "currentStock": 5, "nationalizedAvailable": 2 } }
```

  Ingreso − despachado = existencias.

### C-F5-04 · `GET reports/general-inventory` (nuevo)

- **Política:** `ActiveUser`.
- **Query:**
  - `balanceType`: `WithBalance` (por defecto) o `All`;
  - `fromDate`/`toDate` (fecha de ingreso; **obligatorios con `All`**);
  - `importerId`, `customsAgencyId`, `transportCompanyId`, `productId`;
  - `operationModalityCode` (`IMP`, `EXP` o `INSP`);
  - `warehouseLocationId`;
  - `includeReleases` (bool);
  - paginado y `all`.
- **Respuesta:**

```jsonc
{ "data": {
    "items": [ { "warehouseStorageNumber": "2026BA00012", "entryDate": "datetime", "cargoManifestNumber": "CP-123",
                 "manifestNumber": "string | null", "productName": "CEBOLLA", "packagingName": "BULTO",
                 "importerName": "string | null", "customsAgencyName": "string | null", "locations": "A-01, B-02",
                 "receivedQuantity": 10, "nationalizedQuantity": 7, "dispatchedQuantity": 5, "currentStock": 5,
                 "releaseNumbers": "LEV-1, LEV-2" } ],   // solo con includeReleases; nacionalizado null fuera de IMP
    "totals": { "receivedQuantity": 10, "nationalizedQuantity": 7, "dispatchedQuantity": 5, "currentStock": 5 } },
  "pagination": { … } }
```

- **Error:** 400 "Indique el rango de fechas para consultar todo el inventario."
- **Rótulos del legacy:** Depósito, F. Depósito, C.P.I., Manifiesto, Descripción producto, Importador, SIA/Intermediario, Bodega(s), Entran, Nalzdos., Salen, Saldo, Levantes.

### C-F5-05 · `GET reports/policies` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `year` (obligatorio, 2000 a 2100).
- **Respuesta:**

```jsonc
{ "data": { "year": 2026,
    "months": [ { "month": 1, "uapValueUsd": 1000.00, "nonUapValueUsd": 500.00, "totalValueUsd": 1500.00 } /* 12 meses */ ],
    "totals": { "uapValueUsd": 1000.00, "nonUapValueUsd": 500.00, "totalValueUsd": 1500.00 } } }
```

- **Cálculo:** mes de **ingreso del depósito**; suma del FOB en dólares de sus levantes; UAP según el importador.
- **Rótulos:** el legacy rotula las columnas «CIF UAP» y «CIF NUAP» y el informe «INFORME DE PÓLIZA», con firmas «Firma Funcionario», «Jefe del Depósito» y «Recibí conforme». El valor es la suma del FOB.
- **Error:** 400 "El año debe estar entre 2000 y 2100."

### C-F5-06 · `GET reports/policies/detail` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `year` y `month` (obligatorios), `uap` (`true`, `false` o ausente para ambos), paginado y `all`.
- **Respuesta:**

```jsonc
{ "data": {
    "items": [ { "entryDate": "datetime", "warehouseStorageNumber": "2026BA00012", "cargoManifestNumber": "CP-123",
                 "manifestNumber": "string | null", "cargoUnitPlates": "CONT-1, CONT-2",
                 "importerName": "string", "customsAgencyName": "string | null", "productName": "CEBOLLA",
                 "receivedQuantity": 10, "nationalizedQuantity": 7, "dispatchedQuantity": 5, "currentStock": 5,
                 "releaseNumber": "LEV-1", "acceptanceNumber": "ACE-1", "releaseDate": "datetime",
                 "fobUsd": 1000.00, "isUap": true } ],
    "totals": { "fobUsd": 1000.00 } },
  "pagination": { … } }
```

- **Errores:** "El año debe estar entre 2000 y 2100." y "El mes debe estar entre 1 y 12." (400).

### C-F5-07 · Terceros con marca UAP (modificado)

- **Rutas:** `POST stakeholder` y `PATCH stakeholder/{id}` aceptan `isUap` (bool; al crear, por defecto false). `GET stakeholder` y `GET stakeholder/{id}` lo devuelven.
- **Rótulo:** «UAP (usuario aduanero permanente)».

### C-F5-08 · `GET reports/incoming-by-product` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `fromDate` y `toDate` (obligatorios), `importerId` (obligatorio), `productId`, paginado y `all`.
- **Respuesta:** `data: { "items": [ { "productId": "guid", "productName": "CEBOLLA", "packagingName": "BULTO", "quantity": 120 } ], "totals": { "quantity": 120 } }`
- **Errores:** 400 "Indique el rango de fechas." y "Seleccione el importador."

### C-F5-09 · `GET reports/billing-annual` (nuevo)

- **Política:** `BillingAccess`.
- **Query:** `year` (obligatorio) y `serviceCategory` (`Almacenamiento` por defecto; también `Bascula`, `Montacargas` o `GuiaSalida`).
- **Respuesta:**

```jsonc
{ "data": { "year": 2026, "serviceCategory": "Almacenamiento",
    "months": [ { "month": 3, "invoiceCount": 3, "totalAmount": 450000,
                  "days": [ { "day": 5, "invoiceCount": 2, "totalAmount": 300000 } ] } ],
    "totals": { "invoiceCount": 3, "totalAmount": 450000 } } }
```

- **Cálculo:** facturas con número SIIGO, no anuladas, por fecha de emisión en Colombia. El total suma las líneas del servicio elegido.

### C-F5-10 · `GET reports/deposit-billing` (nuevo; informe por CPI)

- **Política:** `BillingAccess`.
- **Query:** `warehouseStorageNumber` (obligatorio).
- **Respuesta:**

```jsonc
{ "data": {
    "warehouseStorageNumber": "2026BA00012", "cargoManifestNumber": "CP-123", "importerName": "string",
    "entryDate": "datetime", "customsAgencyName": "string | null", "manifestNumber": "string | null", "entryTrm": 3900.25,
    "products": [ { "productName": "CEBOLLA", "receivedQuantity": 10, "dispatchedQuantity": 5, "currentStock": 5 } ],
    "dispatches": [ { "vehiclePlate": "ABC123", "ticketNumber": "string | null", "departureDate": "datetime" } ],
    "invoices": [ { "invoiceId": "guid", "invoiceNumber": "string | null", "invoiceDate": "datetime",
                    "periodStart": "datetime", "periodEnd": "datetime", "limitDate": "yyyy-MM-dd | null",
                    "billedTo": "string", "total": 150000, "status": "Approved", "notes": "string | null",
                    "reissuedAsInvoiceNumber": "string | null" } ],
    "invoicesTotal": 150000 } }   // solo facturas no anuladas
```

- **Error:** 404 "No se encontró el depósito '{número}'."

### C-F5-11 · `GET weighbridge/history` (modificado) y `GET weighbridge/history/totals` (nuevo)

- **Política:** `ScaleAccess`.
- **Filtros nuevos en ambos:**
  - `operationModalityId` y `transportCompanyId`;
  - `customerId`;
  - `zeroValue` (bool: sin factura o total 0);
  - `pendingPayment` (bool: factura con saldo pendiente);
  - `notPrinted` (bool: tiquete nunca impreso).
- **Cada fila del historial agrega:**

```jsonc
{ "grossWeightKg": 30000, "tareWeightKg": 12000, "netWeightKg": 18000, "reweighed": false,
  "subtotal": 19328, "taxAmount": 3672, "cashReceived": 50000, "changeGiven": 27000,
  "ticketFirstPrintedAt": "datetime | null" }
```

  Más los campos de C-F3-11, C-F4-18 y C-F4-19.
- **Totales** (`GET weighbridge/history/totals`): `{ "data": { "count": 120, "netWeightKg": 2160000, "subtotal": 2319360, "taxAmount": 440640, "total": 2760000 } }`
- **Nota:** el tiquete queda «impreso» la primera vez que se genera su PDF (`GET weighbridge/{id}/ticket/pdf` o `GET weighbridge/entries/{entryId}/ticket/pdf`).

### C-F5-12 · `GET reports/customs-agency-entries` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `customsAgencyId` (obligatorio), paginado y `all`.
- **Fila:**

```jsonc
{ "warehouseStorageId": "guid", "cargoManifestNumber": "CP-123", "importerName": "string",
  "products": "CEBOLLA (BULTO), PAPA (SACO)", "receivedQuantity": 120, "entryDate": "datetime",
  "process": "Depósito" }   // "Báscula" si está en Borrador
```

- **Visibilidad:** un depósito sin existencias solo aparece si tuvo una salida en las últimas 13 horas. Los que están en Borrador aparecen siempre.
- **Error:** 400 "Seleccione la agencia de aduanas."

### C-F5-13 · `GET reports/customs-agency-entries/{warehouseStorageId}` (nuevo)

- **Política:** `ForeignTradeAccess`.
- **Query:** `customsAgencyId` (obligatorio).
- **Respuesta:**

```jsonc
{ "data": {
    "warehouseStorageNumber": "2026BA00012", "cargoManifestNumber": "CP-123", "importerName": "string",
    "weighings": [ { "ticketNumber": "T-…", "vehiclePlate": "ABC123", "date": "datetime",
                     "grossWeightKg": 30000, "tareWeightKg": 12000, "netWeightKg": 18000 } ],
    "novelties": [ /* WarehouseNoveltyDto (C-F4-08), sin las anuladas */ ],
    "exits": [ { "date": "datetime", "vehiclePlate": "XYZ789", "quantity": 10, "previousBalance": 120,
                 "gateDepartureAt": "datetime | null", "guideNumber": "string | null" } ] } }
```

- **Error:** 404 "El depósito no existe o no es de esta agencia."

### C-F5-14 · Exportaciones a Excel (referencia)

El Excel lo arma el frontend. Siempre con `all=true` y los mismos filtros de la pantalla. Nunca con `pageSize` > 50.

| Exportación | Endpoint |
|---|---|
| Depósitos de importación, exportación e inspección | `GET foreign-trade/imports`, `…/exports`, `…/inspections` |
| Movimientos de inventario (botón de Bodega) | `GET warehouse/inventory/movements` |
| Kardex de un depósito | `GET warehouse/movements-report` (no paginado) |
| Inventario general | `GET reports/general-inventory` |
| Pólizas (resumen y detalle) | `GET reports/policies`, `GET reports/policies/detail` |
| Ingresos por producto | `GET reports/incoming-by-product` |
| Facturación anual y por CPI | `GET reports/billing-annual`, `GET reports/deposit-billing` |
| Báscula | `GET weighbridge/history` y `…/history/totals` |
| Agencias de aduanas | `GET reports/customs-agency-entries` |
| Abandono | `GET foreign-trade/abandonment`, `GET reports/abandonment-candidates`, `GET reports/abandonment-exits` |
| Levantes | `GET foreign-trade/releases` |
| Órdenes, guías y facturas | `GET foreign-trade/loading-orders`, `GET foreign-trade/dispatch-guides`, `GET billing/invoices` |
| Novedades | `GET warehouse/novelties` |

---

## 7. Fase 6 — Migración y respaldos

Todo lo de esta fase es `AdminOnly`.

### C-F6-01 · `POST administration/legacy-import/{entity}` (nuevo)

- **`{entity}`**: `PackagingTypes`, `Crews`, `Locations`, `Customers`, `CustomsAgencies`, `TransportCompanies`, `Vehicles`, `Drivers`, `Products`, `Deposits` o `Releases`. Las ciudades usan C-F2-07.
- **Petición** (multipart): `file` (CSV `;`, `,` o tabulador; UTF-8 o Latin-1), `headerRows` (≥ 0, por defecto 1) y `dryRun` (por defecto true).
- **Columnas por entidad**, en orden:

| Entidad | Columnas |
|---|---|
| `PackagingTypes` | `id_embalaje;nom_embalaje` |
| `Crews` | `id_cuadrilla;nom_cuadrilla` |
| `Locations` | `id_seccion;nombre;fila;columna;nom_bodega` |
| `Customers` | `id_cliente;nom_tipodocumento;nro_documento;digitoverificacion;id_paisdocumento;nom_cliente;dias_facturacion;uap;es_exportador` |
| `CustomsAgencies` | `id_sia;nom_tipodocumento;nro_documento;digitoverificacion;id_paisdocumento;nombre_sia` |
| `TransportCompanies` | `id_empresatransporte;nom_tipodocumento;nro_documento;id_paisdocumento;nom_empresatransporte` |
| `Vehicles` | `id_vehiculo;placa_vehiculo;id_paisplaca;id_empresatransporte` |
| `Drivers` | `id_persona;nom_tipodocumento;documento_persona;id_paisdocumento;nombres_persona;apellidos_persona;telefono_persona` |
| `Products` | `id_producto;aliasproducto;descripcionproducto;id_embalaje` |
| `Deposits` | `nro_deposito;fecha_deposito;modalidad;id_cliente;id_importador;id_exportador;id_sia;nro_doccomercial;fecha_doccomercial;nro_manifiestodian;fecha_manifiestodian;id_producto;id_embalaje;ingresan;nacionalizados;salen;saldo;ultimo_fin_facturado;trm_ingreso` |
| `Releases` | `nro_deposito;id_producto;id_embalaje;nro_levante;fecha_levante;nro_aceptacion;fecha_aceptacion;cantidad_levante;peso_bruto;fob_dolares;tasa_cambio;fob_pesos` |

- **Respuesta 200:**

```jsonc
{ "data": { "batchId": "guid", "entity": "Customers", "dryRun": true,
            "totalRows": 1200, "created": 1180, "updated": 15, "skipped": 3, "errorRows": 2,
            "errors": [ { "row": 45, "message": "Fila 45: el tipo de documento «CE» no tiene equivalente en la v2." } ] } } // hasta 500
```

- **Errores:** 400 "La entidad {x} no se puede importar.", 400 "El archivo no tiene filas." y 400 "El archivo supera 50 000 filas; divídalo."
- **Nota:** la pantalla debe forzar el orden de carga: ciudades, embalajes, cuadrillas, ubicaciones, clientes, agencias, transportadoras, vehículos, conductores, productos, depósitos y levantes. Siempre simulación primero y firme después.

### C-F6-02 · Lotes de importación (nuevo)

- **`GET administration/legacy-import/batches`:** query `entity`, paginado. Fila:

```jsonc
{ "id": "guid", "entity": "Customers", "fileName": "clientes.csv", "dryRun": false,
  "totalRows": 1200, "createdRows": 1180, "updatedRows": 15, "skippedRows": 3, "errorRows": 2,
  "createdByName": "string", "createdAt": "datetime" }
```

- **`GET administration/legacy-import/batches/{id}`:** la fila anterior más `errors: [ { row, message } ]` (hasta 1000).

### C-F6-03 · `POST administration/legacy-import/reconciliation` (nuevo)

- **Petición** (multipart): `file` (el CSV de `Deposits` exportado de nuevo el día del corte) y `headerRows`.
- **Respuesta 200** (no escribe nada):

```jsonc
{ "data": {
    "summary": { "ok": 480, "differences": 3, "notMigrated": 1 },
    "rows": [ { "legacyNumber": "DEP-9123", "v2Number": "2026BA00321", "productName": "CEBOLLA",
                "legacyBalance": 10, "v2Stock": 8, "legacyNationalized": 6, "v2Nationalized": 6,
                "v2MovementsSinceMigration": -2, "status": "Ok" } ] } }   // Ok, Difference o NotMigrated
```

- **Nota:** `Ok` también cuando la diferencia se explica por movimientos hechos en la v2 después de migrar.

### C-F6-04 · `POST administration/legacy-import/open-billing` (nuevo)

- **Petición:** `{ "warehouseStorageIds": ["guid"] }` (opcional; vacío o ausente = todos los migrados sin períodos).
- **Respuesta 200:**

```jsonc
{ "data": [ { "warehouseStorageId": "guid", "number": "2026BA00321", "legacyNumber": "DEP-9123",
              "status": "Opened", "message": "string | null" } ] }   // Opened, Skipped o Failed
```

  - `Skipped`: "El depósito {n} empieza a facturar el {fecha}."
  - `Failed`: el error de resolución de cargos, por ejemplo una tarifa faltante.
- **Nota:** ejecútelo solo después de configurar las tarifas en el motor de acuerdos.

### C-F6-05 · Destinos de respaldo (nuevo)

- **`BackupDestinationDto`** (nunca incluye credenciales):

```jsonc
{ "id": "guid", "name": "local-servidor", "type": "Local",   // o "S3"
  "localPath": "/opt/wms/backups", "bucket": null, "prefix": null, "region": null, "serviceUrl": null,
  "isActive": true, "createdAt": "datetime", "updatedAt": "datetime | null" }
```

| Verbo y ruta | Petición | Respuesta |
|---|---|---|
| `GET administration/backup-destinations` | — | lista |
| `POST administration/backup-destinations` | `{ name, type, localPath?, bucket?, prefix?, region?, serviceUrl?, isActive }` | 201 `BackupDestinationDto` |
| `PUT administration/backup-destinations/{id}` | la misma de `POST` | 200 `BackupDestinationDto` |
| `DELETE administration/backup-destinations/{id}` | — | 204 |
| `POST administration/backup-destinations/{id}/test` | — | `{ "success": true, "message": "string" }` |

- **Errores:** "Indique la carpeta del respaldo." (400), "Indique el bucket del respaldo." (400) y "Ya existe el destino {nombre}." (409).
- **Nota:** las credenciales de S3 se configuran en el servidor (`Backups:S3Credentials:{name}:AccessKeyId`/`SecretAccessKey`) o con el rol de la instancia. La pantalla solo lo informa.

### C-F6-06 · `POST administration/backups/run` (nuevo)

- **Petición:** sin cuerpo.
- **Respuesta 202:** `{ "data": { "backupRunId": "guid", "status": "Running" } }`. La corrida sigue en segundo plano; su resultado se ve en C-F6-07.
- **Error:** 409 "Ya hay un respaldo en curso."

### C-F6-07 · `GET administration/backups/runs` (nuevo)

- **Query:** paginado.
- **Fila:**

```jsonc
{ "id": "guid", "startedAt": "datetime", "finishedAt": "datetime | null",
  "kind": "Daily", "status": "Succeeded",          // kind: Daily, Monthly, Manual; status: Running, Succeeded, PartiallySucceeded, Failed
  "sizeBytes": 123456789, "triggeredByName": "string | null", "error": "string | null",
  "results": [ { "destinationId": "guid", "destinationName": "s3-principal", "status": "Succeeded",
                 "location": "s3://bucket/wms/2026/09/wms_20260929_0200.dump", "error": null } ] }
```

- **Retención:** 30 respaldos diarios y 12 mensuales por destino. Los manuales no se borran. Un fallo notifica al rol Admin.
