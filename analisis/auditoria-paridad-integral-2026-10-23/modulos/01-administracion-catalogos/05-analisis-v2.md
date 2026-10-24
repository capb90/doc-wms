# 05 — Análisis V2 · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Lectura estática de `Backend/wms-api/` y `Frontend/wms/app/` (sin `bin/`, `obj/`, `publish/`, `.output/`, `.nuxt/`, `node_modules/`). Prefijo del API: `/api/v1` (`Backend/wms-api/Wms.Api/Program.cs:162`). Rutas de `[Route("[controller]")]` son insensibles a mayúsculas (`/stakeholder` = `StakeholderController`).

## 1. Frontend

| Página | `requiredRoles` | Menú | Acciones reales | Servicio |
| --- | --- | --- | --- | --- |
| `pages/admin/cities/index.vue` | Admin (`:22-23`) | Administración › Ciudades (`AppMenu.vue:174-176`) | listar, filtrar, crear, editar (con estado), borrar, importar CSV | `features/administration/services/administration-service.ts:170-194` |
| `pages/admin/crews/index.vue` | Admin (`:21-22`) | Administración › Cuadrillas | listar, crear, editar, borrar | `administration-service.ts:200-215` |
| `pages/admin/packaging-types/index.vue` | Admin (`:17-18`) | Administración › Productos › Tipos de embalaje | listar, crear, editar, borrar (sin activar/desactivar) | `administration-service.ts:80-101` |
| `pages/admin/unit-measures/index.vue` | Admin | Productos › Unidades de medida | CRUD | `administration-service.ts:106-130` |
| `pages/admin/cargo-unit-types/index.vue` | Admin | Productos › Tipos de unidad de carga | CRUD | `administration-service.ts:135-159` |
| `pages/admin/products/*` | Admin | Productos | listar, crear (con embalaje rápido), editar, activar/desactivar | `features/products/services/product-service.ts:8-23` |
| `pages/admin/services/*` | Admin | Servicios › Tarifas base | catálogo: listar, crear, editar, activar/desactivar (precios y reglas: módulo 06) | `features/services/services/service-service.ts:21-46` |
| `pages/admin/stakeholders/index.vue`, `[id].vue` | Admin, ForeignTrade, Billing (`index.vue:18-19`, `[id].vue:131-132`) | Administración › Terceros; CE › Terceros (`AppMenu.vue:384-397`); Facturación › Clientes (`:490`) | listar, filtrar por rol, detalle; edición solo Admin/FT (`[id].vue:147`) | `features/stakeholders/services/stakeholder-service.ts` |
| `pages/admin/stakeholders/create.vue`, `edit/[id].vue` | Admin, ForeignTrade | — | crear (con contactos y cuentas), editar, roles | ídem |
| `pages/admin/drivers/index.vue` | Admin (`:17-18`) | Administración › Conductores | listar, filtrar, crear, editar con estado (sin borrar) | `features/entries/services/driver-service.ts:18-33` |
| `pages/admin/vehicles/index.vue` | Admin (`:25-26`) | Administración › Vehículos | listar, crear, editar con estado (sin borrar) | `features/entries/services/vehicle-service.ts:7-37` |
| `pages/admin/entry-reasons/index.vue` | Admin | Motivos de entrada | CRUD | `features/entries/services/entry-reason-service.ts:12-41` |
| `pages/admin/locations/index.vue` | Admin (`:18-19`) | Ubicaciones | listar, filtrar, crear, editar (disponible), borrar | `features/warehouse/services/warehouse-service.ts:532-544` |
| `pages/admin/users/*` | Admin | Usuarios | listar, crear, editar, roles, reset, activar | `features/users/services/user-service.ts:19-69` |
| `pages/admin/audit/index.vue` | Admin (`:17-18`) | Auditoría | consultar con filtros | `features/audit/services/audit-service.ts:7` |
| `pages/admin/parameters/index.vue` | Admin (`:20-21`) | Perfil › Parámetros | listar y editar | `administration-service.ts:54-72` |
| `pages/auth/*` | públicas salvo `change-password` | — | login, recuperación, reset, cambio | `features/auth/services/auth-services.ts:11-23` |
| `pages/index.vue` | Admin, ForeignTrade (`:10-14`) | Dashboards › Trazabilidad | tablero (módulo 03) | — |

- **Sin mocks ni datos estáticos de negocio** en estas páginas y sus `features` (búsqueda de «mock», «fake», «dummy», «TODO», «lorem»). Los países son una lista fija `Frontend/wms/app/utils/countries.ts`, como lo era `pais` (sin pantalla en el legacy).
- **Permisos de menú:** `AppMenu.vue:521-527` filtra grupos por rol; `middleware/auth.global.ts:81-88` aplica `requiredRoles` y `utils/role-routes.ts:25-28` evita el «Acceso denegado» del logo (DEF-F0-003, Verificado).
- Las mutaciones invalidan su prefijo (`["administration", "cities", …]`, `["stakeholders"]` en `useQuickCreateStakeholder.ts:45`).

## 2. Backend: endpoints del módulo y su política

| Endpoint | Política | Evidencia |
| --- | --- | --- |
| `GET administration/system-roles`, `business-role`, `taxes`, `operation-modalities`, `packaging-types` | **`[AllowAnonymous]`** | `AdministrationController.cs:40,51,63,111,133` |
| `GET/GET{id}/PATCH administration/system-parameters` · `GET administration/audit-logs` | `AdminOnly` | `AdministrationController.cs:73-107,121-130` |
| `POST administration/packaging-types` | `OperationalAccess` | `:142-151` |
| `PATCH/DELETE administration/packaging-types/{id}` · `POST/PATCH/DELETE unit-measures` y `cargo-unit-types` | `AdminOnly` | `:153-260` |
| `GET administration/unit-measures`, `cargo-unit-types` | `[Authorize]` (clase) | `:36,179-185,222-228` |
| `GET administration/cities` · `POST/PUT/DELETE cities` · `POST cities/import` | `[Authorize]` · `AdminOnly` | `CitiesController.cs:24,34-129` |
| `GET administration/crews` · `POST/PUT/DELETE crews` | `[Authorize]` · `AdminOnly` | `CrewsController.cs:19,23-75` |
| `GET stakeholder…` · escrituras de tercero, contactos y cuentas | `ActiveUser` · `StakeholderAccess` (Admin, FT) | `StakeholderController.cs:44-243` |
| `POST weighbridge/stakeholders/quick` | `ScaleAccess` (clase) | `WeighbridgeController.cs:69,996-1014` |
| `POST weighbridge/transport-companies/quick` | `OperationalAccess` (Admin, Warehouse, Receiving, Scale) | `WeighbridgeSharedController.cs:26,107-115` |
| `GET weighbridge/vehicle-types`, `vehicles/by-plate/{plate}`, `drivers/by-document`, `lookup`, `shipping-document-types` | `ActiveUser` | `WeighbridgeCatalogController.cs:27-97` |
| `GET product…` · `POST/PATCH product` | `[Authorize]` · `AdminOnly` | `ProductController.cs:17-67` |
| `GET service…` · catálogo `POST/PATCH/activate/deactivate` | `[Authorize]` · `BillingAccess` | `ServiceController.cs:33-102` |
| `GET drivers…` · `POST/PATCH drivers` | `ActiveUser` · `DriverCatalogAccess` (+ Bodega) | `DriverController.cs:16-63` |
| `GET vehicles…` · `POST/PATCH vehicles` | `ActiveUser` · `TransportCatalogAccess` | `VehicleController.cs:16-63` |
| `GET entry-reasons…` · escrituras | `ActiveUser` · `AdminOnly` | `EntryReasonController.cs:17-85` |
| `GET warehouse/locations` · `POST/PATCH/DELETE` | `WarehouseAccess` · `AdminOnly` | `WarehouseController.cs:60,900-948` |
| `/user/*` (salvo `me` y notificaciones) | `AdminOnly` | `UserController.cs:31-150` |
| `auth/login`, `refresh-token`, `request-password-reset`, `reset-password` · `logout`, `change-password` | `[AllowAnonymous]` · `[Authorize]` | `AuthController.cs:20-84` |

**Reglas y errores** (detalle en 03-reglas-negocio.md): mensajes en español con `BadRequestException`/`ConflictException`/`NotFoundException`. Inconsistencia menor: «en uso» responde 400 en embalajes, unidades de medida, tipos de unidad y motivos (`DeletePackagingTypeHandler.cs:26`, `DeleteUnitMeasureHandler.cs:25`, `DeleteCargoUnitTypeHandler.cs:24`, `DeleteEntryReasonHandler.cs:26`) y 409 en ciudades, cuadrillas y ubicaciones. Un duplicado de código de embalaje al editar responde 400 (`UpdatePackagingTypeHandler.cs:35`). Las violaciones de FK y de unicidad no controladas salen como 409 con texto de negocio (`Backend/wms-api/Wms.Api/Common/Exception/GlobalExceptionHandler.cs:108-128`; `Wms.Common/Http/DatabaseErrorMessages.cs:13-28`).

**Auditoría:** todas las entidades de catálogo del módulo son `IAuditable` (58 en `Wms.Domain`); `AppDbContext.cs:185-243` registra usuario, IP y valores anterior/nuevo. No lo son `OperationModality`, `ShippingDocumentType`, `BusinessRole` ni `StakeholderBusinessRole`: asignar o retirar un rol de negocio a un tercero no deja rastro en `audit_logs` (no hay regla legacy equivalente; se anota, sin brecha).

**Autor:** las escrituras toman el usuario del token. Excepción menor: `CitiesController.cs:124-126` lee el claim con `Guid.Empty` de respaldo en lugar de `GetRequiredUserId()` (convención de `docs/contexto/convenciones-tecnicas.md` §2).

## 3. Integración y contratos

Comparación campo a campo de las operaciones principales (detalle en 09-integraciones.md):

| Contrato | Backend | Frontend | Resultado |
| --- | --- | --- | --- |
| Ciudad | `CityDto` (`Cities/Common/CityDto.cs:6-16`) | `ICity` (`features/administration/types/city.ts:4-17`) | Coincide (10 campos, nulos y fechas como texto) |
| Importación de ciudades | `ImportCitiesResultDto` + `CityCsvError(Row, Message)` | `IImportCitiesResult` (`city.ts:39-45`) | Coincide |
| Cuadrilla | `CrewDto` (`Crews/Common/CrewDto.cs:9`) y `CrewRequest(Name, IsActive = true)` (`Controllers/v1/Requests/CrewRequests.cs:4`) | `ICrew`, `IUpdateCrewRequest` (`types/crew.ts:4-24`) | Coincide |
| Tercero | `StakeholderDto` (`Stakeholders/Common/Dtos/StakeholderDto.cs:8-23`); enums como texto (`Program.cs:63`) | `IStakeholder` (`features/stakeholders/types/stakeholder.ts:16-31`) | Coincide; `idType` limitado a los 5 valores del enum |
| Paginación | `QueryParametersBase` (tope 50, `all=true`) | selects con `{ isActive: true, all: true }` (`CrewSelect.vue:25`, `LoadingOrderForm.vue:82-90`) | Correcto |

- **Endpoints sin consumidor:** `GET entry-reasons/{id}` (el servicio solo usa listado, lista, crear, editar y borrar: `entry-reason-service.ts:12-41`). `POST administration/packaging-types` admite roles operativos, pero solo lo llaman pantallas de Admin (`QuickCreatePackagingTypeDialog.vue:43` desde `ProductForm`): no es defecto. `GET weighbridge/lookup` es del módulo 02.
- **Llamadas del frontend sin endpoint:** ninguna en los servicios del módulo (se cotejaron todas las rutas de `administration-service.ts`, `stakeholder-service.ts`, `product-service.ts`, `service-service.ts` en su parte de catálogo, `user-service.ts`, `auth-services.ts`, `audit-service.ts`, `driver-service.ts`, `vehicle-service.ts`, `entry-reason-service.ts` y las de ubicaciones de `warehouse-service.ts`).

## 4. Permisos: DEC-005 y DEC-031

Para cada escritura de catálogo se listaron las pantallas que la llaman y sus roles:

| Escritura | Política | Pantallas que la llaman (roles) | ¿Algún rol pierde una función? |
| --- | --- | --- | --- |
| Ciudades, cuadrillas, ubicaciones, motivos, productos, unidades, tipos de unidad | `AdminOnly` | Solo `/admin/*` (Admin). Báscula crea productos por su propio flujo (P3) | No |
| Embalaje (alta) | `OperationalAccess` | `ProductForm` (Admin) | No |
| Tercero (alta y edición) | `StakeholderAccess` | `/admin/stakeholders/create`, `edit` (Admin, FT) | No: báscula usa `weighbridge/stakeholders/quick` (Scale) y Vigilancia, Báscula y Bodega usan `transport-companies/quick` desde `VehicleForm.vue:274` |
| Vehículo | `TransportCatalogAccess` | `/admin/vehicles` (Admin), `LoadingOrderForm.vue:381` (FT); Vigilancia, Báscula y Bodega lo crean dentro de su propio registro | No |
| Conductor | `DriverCatalogAccess` | `/admin/drivers` y DriverPicker en báscula y Bodega | No (DEC-017 agregó Bodega) |
| Servicio (catálogo) | `BillingAccess` | `/admin/services` (Admin) | No; la página no se ofrece a Billing (OBS-F9-003), que en el legacy tampoco veía «Configuraciones» |

Las lecturas que usan los flujos operativos son `ActiveUser` o `[Authorize]`, salvo cinco catálogos con `[AllowAnonymous]` (más abiertos que DEC-031: BR-01-002, OBS-F9-001). `GET warehouse/locations` (`WarehouseAccess`) solo lo consumen componentes de Bodega (`ReceptionStepManualInfo.vue:22`, `ReceptionStepCompletion.vue:25`, `ProductPlacementsDialog.vue:19`). **No se encontró ningún retroceso funcional por permisos.**

## 5. Capacidades SOLO_V2

| ID | Estado | Nota |
| --- | --- | --- |
| CF-V001 Autenticación JWT | Confirmada | Reemplaza CF-L001/002 |
| CF-V002 Recuperación y cambio de contraseña | Confirmada | BR-01-008 (cambio sin contraseña actual) |
| CF-V003 Usuarios con 6 roles | Confirmada | Reemplaza CF-L081…084, 098 |
| CF-V004 Consulta de auditoría | Confirmada | La escritura equivale a CF-LX01-02 |
| CF-V005 Parámetros del sistema | Confirmada | Incluye datos de empresa (CHG-84) |
| CF-V006 Unidades de medida | Confirmada | DEC-015 |
| CF-V007 Tipos de unidad de carga | Confirmada | DEC-014 |
| CF-V008 Motivos de ingreso | Confirmada | — |
| CF-V009 Conductores con selector | Confirmada | DEC-017; 3 MINOR «Nuevo» |
| CF-V010 Terceros multirol y alta rápida | Confirmada | — |
| CF-V011 Inicio por rol | Confirmada | Solo frontend |
| CF-V012 Carga masiva de ciudades | **Nueva** | `CitiesController.cs:99-129`; usada en la migración |
| CF-V013 Contactos y cuentas bancarias de terceros | **Nueva** | `StakeholderController.cs:139-243` |
