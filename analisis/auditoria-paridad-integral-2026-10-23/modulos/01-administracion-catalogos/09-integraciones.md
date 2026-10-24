# 09 — Integraciones · 01-administracion-catalogos

> **Fecha:** 2026-10-23. Trazas estáticas (interacción → componente → servicio → HTTP → endpoint → lógica → persistencia → respuesta → UI). Rutas relativas a `code_workspace/`; el prefijo `/api/v1` lo pone `Backend/wms-api/Wms.Api/Program.cs:162`.

## I-01 · Crear una ciudad (CF-L006)

1. **UI:** «Nueva ciudad» → diálogo (`Frontend/wms/app/pages/admin/cities/index.vue:247`, formulario `:104-126`). La validación local usa los mismos mensajes del dominio.
2. **Mutación:** `useCreateCity` (`features/administration/composables/useMutationsCities.ts`) → `administration-service.ts:175` → `POST /api/v1/administration/cities` con `{ name, countryCode, district, transitDays, isAbandonmentDestination }` (`types/city.ts:26-32`).
3. **API:** `CitiesController.CreateCity` (`Backend/wms-api/Wms.Api/Controllers/v1/CitiesController.cs:42-58`), `AdminOnly`.
4. **Lógica:** `City.Create` normaliza y valida (`Wms.Domain/Entities/Administration/City.cs:33-119`); `CityDuplicateRules.EnsureUniqueAsync` → 409 (`Cities/Common/CityDuplicateRules.cs:29-41`).
5. **Persistencia:** `cities` + fila `Create` en `audit_logs` (`Wms.Infrastructure/Persistence/AppDbContext.cs:185-243`).
6. **Respuesta:** 201 `ApiResponse<CityDto>`; la UI invalida `["administration","cities"]` y cierra el diálogo. Un 409 se muestra en el campo nombre (`cities/index.vue:100`, `nameConflict`).

## I-02 · Usar la ciudad en la orden de cargue y en la guía (CF-L005 → módulo 05)

`LoadingOrderForm.vue:90-91` pide `GET administration/cities?isActive=true&all=true`; la orden guarda `destinationCityId` (`Backend/wms-api/Wms.Domain/Entities/Warehouse/LoadingOrder.cs:24,459`). La guía calcula el vencimiento con los días de tránsito (`Backend/wms-api/Wms.Application/ForeignTrade/Common/Services/GuideExpirationCalculator.cs:16-44`; `Frontend/wms/app/features/foreign-trade/components/DispatchGuideForm.vue:130-136`). Borrar una ciudad usada → 409 (`DeleteCityHandler.cs:15-24`). El detalle de la orden y la guía lo verifica el módulo 05.

## I-03 · Cuadrilla en recepción, orden y guía (CF-L021 → módulos 03 y 05)

`CrewSelect.vue:25-26` (`isActive=true&all=true`) en `LoadingOrderForm.vue`, `ReceptionStepManualInfo.vue`, `ReceptionStepCompletion.vue` y `LoadingOrderExecutionDialog.vue`. El servidor valida que exista y esté activa (`Crews/Common/CrewDto.cs:31-41`) y la guía toma el nombre de la cuadrilla de la orden (`Backend/wms-api/Wms.Application/ForeignTrade/Commands/CreateDispatchGuide/CreateDispatchGuideCommandHandler.cs:240`; `CreateExportDispatchGuide/CreateExportDispatchGuideCommandHandler.cs:137`).

## I-04 · Alta de tercero (CF-L010, 034, 062)

- **Completa (Admin, FT):** `pages/admin/stakeholders/create.vue:37` → `useStakeholderCreate` → `stakeholder-service.ts:33` → `POST /api/v1/stakeholder` (`StakeholderAccess`) → `CreateStakeholderHandler.cs:18-61` (duplicado tipo + número → 409; al menos un rol; contactos y cuentas en la misma operación) → `stakeholders`, `stakeholder_business_roles`, contactos, cuentas → 201 `StakeholderDto`.
- **Rápida desde báscula (Scale):** `QuickCreateStakeholderDialog.vue:23` → `useQuickCreateStakeholder.ts:27` → `POST /api/v1/weighbridge/stakeholders/quick` (`WeighbridgeController.cs:996-1014`): 201 creado, 200 rol agregado a un existente, 409 rol repetido con el tercero en el cuerpo (el composable lo trata como resultado, `useQuickCreateStakeholder.ts:33-40`).
- **Transportadora rápida (Vigilancia, Báscula, Bodega):** `VehicleForm.vue:274` → `weighbridge-service.ts:564-572` → `POST /api/v1/weighbridge/transport-companies/quick` (`OperationalAccess`).

## I-05 · Alta de vehículo y conductor desde los flujos (CF-L046, CF-L086)

- Comercio Exterior crea vehículo y conductor desde la orden (`LoadingOrderForm.vue:103,381`; `useCreateDriver`) → `POST /api/v1/vehicles` (`TransportCatalogAccess`) y `POST /api/v1/drivers` (`DriverCatalogAccess`).
- Báscula y Bodega eligen o crean el conductor con DriverPicker (DEC-017) → `driver-service.ts:28-33`.
- Báscula busca la placa (`VehicleForm.vue:186` → `GET weighbridge/vehicles/by-plate/{plate}?includeInactive=true`).

## I-06 · Desactivar un tercero, producto, conductor o vehículo (CF-L012, 052, 048, 088)

Interruptor (`StakeholderHeader.vue:22`, `ProductHeader.vue:20`, `drivers/index.vue:281`, `vehicles/index.vue:309-313`) → `PATCH` con `isActive` → el handler llama `Activate/Deactivate` → `UPDATE` + `audit_logs`. No se valida uso (BR-01-006).

## I-07 · Borrar un embalaje (CF-L032)

`packaging-types/index.vue:108` → `administration-service.ts:101` → `DELETE /api/v1/administration/packaging-types/{id}` (`AdminOnly`) → `DeletePackagingTypeHandler.cs:22-28`: 400 si lo usa un producto de depósito; si no, `DELETE` y la base pone en nulo `products.packaging_type_id` (BR-01-001). Respuesta 204.

## I-08 · Carga masiva de ciudades (CF-V012)

`CityImportDialog.vue` → `administration-service.ts:194` (`postForm`) → `POST /api/v1/administration/cities/import` (multipart: `file` ≤ 2 MB, `headerRows`, `dryRun`) (`CitiesController.cs:99-129`) → `ImportCitiesHandler.cs:16-87`: por fila crea o actualiza por `LegacyId`, rechaza ids repetidos en el archivo, simula sin guardar con `dryRun`. Respuesta `ImportCitiesResultDto` (coincide con `IImportCitiesResult`). Se usó en la migración a staging: 1.781 filas, 1.774 creadas, 7 rechazadas (`docs/planes/migracion-staging/resultados/informe-fase-3.md:89,106-107`).

## I-09 · Sesión (CF-V001, CF-V002)

- Login: `login.vue` → `auth-services.ts:11` → `POST auth/login` → tokens en `stores/auth.ts`.
- Renovación: `plugins/api-client.ts:66` reintenta con `auth/refresh-token` ante 401.
- Logout: `stores/auth.ts:108` → `POST auth/logout` con el refresh token.
- Recuperación: `POST auth/request-password-reset` responde 204 siempre y solo envía correo a un administrador activo con correo (`PasswordResetEligibility.cs:9-10`; `RequestPasswordResetHandler.cs:46-78`), con el enlace `Frontend:BaseUrl` + `/auth/reset-password` (`:72-73`).

## Procesos automáticos e integraciones externas

| Proceso | Lado | Qué hace | Equivalente | Evidencia |
| --- | --- | --- | --- | --- |
| Alerta de TRM del menú | Legacy | Consulta cada segundo si hay tasa vigente | Sin equivalente (TRM de la DIAN; DEC-023) | `bodegas-legacy/menus/menuizquierda.php:149-166` |
| Alerta de abandono del menú | Legacy | Resalta «Prorrogas» si hay depósitos en ventana | `AbandonmentAlertBackgroundService` (07:00, notificación a FT) y aviso del tablero de CE | `bodegas-legacy/menus/evaluaabandonos.php:6-14`; `Backend/wms-api/Wms.Application/ForeignTrade/Jobs/AbandonmentAlertService.cs:19,63-69` (detalle: módulo 04) |
| Correo de recuperación | V2 | SMTP vía `IEmailService` | Sin equivalente legacy | `RequestPasswordResetHandler.cs:19,77` |
| Importación de maestros (embalajes, cuadrillas, ubicaciones, terceros, vehículos, conductores, productos) | V2 | `LegacyImportController` por CSV (F6-02) | — | Lo audita el módulo 08 (CF-V081); resultados en `informe-fase-3.md:85-99` |

No hay jobs propios del módulo en `Backend/wms-api/Wms.Api/BackgroundJobs/`.
