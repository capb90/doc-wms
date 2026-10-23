# Plan cerrado — Selector de conductor con alta y edición en modal (Báscula y Bodega)

> **Fecha:** 8 de octubre de 2026. **Estado:** aprobado por el usuario el 2026-10-08. Prompts: Fase 1 `ajustes/prompt-selector-conductor-fase-1.md` (commiteada, BE `3748ec6`); Fase 2 `ajustes/prompt-selector-conductor-fase-2.md` (commiteada, FE `ef5d248` + `7d7516a`); Fase 3 `ajustes/prompt-selector-conductor-fase-3.md` (commiteada, FE `9ecd333` + corrección `4ca4e0a`, BE `044be08`; MINOR 023, 024 y 026 abiertos); Fase 4 `ajustes/prompt-selector-conductor-fase-4.md`.
> **Base:** backend `wms-api` `develop` `b7c656e` · frontend `wms` `develop` `e01d81d` (ambos limpios).
> **Staging (último redespliegue registrado):** BE `84c712f` / FE `8527144`, con datos migrados (4.361 conductores), cuentas `qa.*` y `operario.*`.
> **Ejecutor:** un agente sin historial. Lee este plan completo antes de empezar.

---

## 0. Instrucciones para el agente ejecutor

1. Lee primero `Backend/wms-api/AGENTS.md` y el documento de contexto que cita (`code_workspace/docs/contexto-negocio-wms-para-ia.md`).
2. **Trabaja en `develop` de los dos repositorios.** No crees ramas. No hagas commits: el usuario commitea cada fase.
3. **Ejecuta una fase por sesión y detente en su checkpoint** (§9) con un resumen: archivos tocados, pruebas y conteos, desviaciones.
4. **Este plan no deja decisiones abiertas.** Si algo del código contradice el plan, no improvises. Detente y pregunta, con todas las dudas en un solo mensaje.
5. **Sin migraciones.** Este cambio no toca el esquema. Si `dotnet ef migrations has-pending-model-changes` deja de estar limpio, detente.
6. **Sin secretos en documentos ni en la salida.** En staging no escribes contraseñas en el navegador; el usuario inicia sesión. Ver §8.

---

## 1. Objetivo y alcance

**Hoy**, la card «Camión y conductor» de Báscula y la «Recepción Directa» de Bodega muestran el formulario completo del conductor (`DriverForm.vue`): tipo y número de documento, apellidos, nombres, país y teléfono. El sistema busca al conductor cuando el operario sale del campo del documento.

**Decidido:** en esas dos pantallas, el formulario se reemplaza por **un select con buscador** y **dos botones**:

- **El select** lista los conductores registrados y busca en el servidor, con paginación, por nombre o por número de documento. Cada opción muestra el nombre y el documento.
- **«+»** abre un modal con el formulario actual. El operario registra el conductor, el modal se cierra y el conductor nuevo queda seleccionado.
- **Lápiz** abre el mismo modal precargado para corregir los datos del conductor seleccionado. El documento queda bloqueado.

El objetivo es reducir el tamaño del formulario y agilizar el registro del operario (premisa 1: báscula rápida, ≤ 30 s).

**Fuera de alcance:**

- Vigilancia: su `DriverForm` está comentado en `pages/operations/entries/index.vue`; no se toca.
- La orden de cargue de Comercio Exterior (`LoadingOrderForm.vue` + `CreateDriverDialog.vue`): no se toca.
- Administración → Conductores: no se toca.
- Las reglas de conductor del backend al guardar:
  - en Báscula, `EntryDriverRules` / `EntryLogInfoUpdater` (DEF-F11-008);
  - en Bodega, `GetOrCreateDriverAsync` de `CreateReceptionWithoutWeighbridgeCommandHandler`.

  No cambian, porque el contrato del payload se conserva (§4.1).

---

## 2. Decisiones

| # | Decisión | Fuente |
|---|---|---|
| D1 | Alcance: **Báscula** (`CompleteEntryInfo.vue`) **y Bodega** (`ReceptionStepManualInfo.vue`). | Usuario, 2026-10-08 |
| D2 | La corrección de datos del conductor se conserva con un **botón lápiz** que abre el modal precargado y guarda con `PATCH /drivers/{id}`. El tipo y el número de documento quedan bloqueados. | Usuario, 2026-10-08; regla «sin retrocesos funcionales» |
| D3 | **Búsqueda en el servidor** con un parámetro nuevo `search` en `GET /drivers`. El endpoint ya pagina; se conservan `name`, `idNumber` e `idType` para Administración. | Petición del usuario; `GetAllDriversHandler` |
| D4 | `search` busca, sin distinguir mayúsculas ni tildes (`unaccent` + `ILIKE`), en:<br>• nombres;<br>• apellidos;<br>• «nombres apellidos»;<br>• «apellidos nombres»;<br>• el número de documento, con el término sin espacios.<br>Usa el mismo patrón `%término%` que `GetCrewsQuery`. | Convención del proyecto |
| D5 | Parámetro nuevo `orderByName` (bool). Con `true` ordena por nombres, apellidos e Id. Sin él se mantiene el orden actual (`CreatedAt`, `Id`), así Administración no cambia. | Sin retrocesos |
| D6 | El select pide `isActive=true`, `orderByName=true`, `pageIndex=1` y `pageSize=20`, con *debounce* de 300 ms. Sin texto muestra la primera página. Si `totalCount > 20`, el pie dice «Mostrando 20 de {N}. Escriba nombre o documento para afinar.». Sin *scroll* infinito. | Diseño; `WarehouseDepositSelect.vue` como patrón |
| D7 | Etiqueta de la opción: `{Nombres} {Apellidos} · {TIPO} {número}`. `TIPO` sale del mapa `Cc→CC`, `Nit→NIT`, `Rut→RUT`, `Pasaporte→Pasaporte`, `Ruc→RUC`. Ejemplo: «Mario Demo Benavides · CC 1000000102». | Petición del usuario; `ID_TYPE_LABELS` de `CompleteEntryInfo.vue` |
| D8 | **Sin filtrado local en el select.** PrimeVue filtra las opciones en el cliente por `optionLabel`. Eso ocultaría resultados válidos del servidor, como «demo mario» o un término sin tildes. Se evita con `:filter-fields="['filterText']"`, donde `filterText = \`${label} ${búsquedaCruda}\``: siempre «contiene» lo digitado. PrimeVue 4.5.5 lo soporta (`searchFields` → `filterFields`). | Verificado en `node_modules/primevue/select/index.mjs` |
| D9 | **«+» registra en el acto**: `POST /drivers` desde el modal, antes del «Guardar» de la ficha. Al cerrarse el modal, el conductor nuevo queda seleccionado. | Petición del usuario |
| D10 | En el modal de alta, si el documento ya existe (la búsqueda por documento de `DriverForm` lo encuentra):<br>• avisa «Este conductor ya está registrado.»;<br>• el botón principal pasa a «Usar este conductor»;<br>• al pulsarlo, si cambiaron nombres, apellidos, país o teléfono, hace `PATCH` con esos cuatro campos y luego selecciona;<br>• si no cambiaron, solo selecciona. | Evita el 409 y no pierde lo digitado |
| D11 | Si el `POST` responde 409 (alguien lo creó entre la búsqueda y el guardado):<br>• se consulta `GET weighbridge/drivers/by-document` y se selecciona ese conductor;<br>• aviso informativo: «El conductor ya estaba registrado; quedó seleccionado.».<br>Con 400 el modal sigue abierto y el aviso global muestra el mensaje del backend. | Robustez |
| D12 | El `PATCH` del lápiz envía `firstName`, `lastName`, `country` y `phoneNumber`; nunca el tipo ni el número. Un campo vacío viaja como `null`. Como `Driver.Update` usa `??`, un campo `null` **conserva el valor anterior**: esta función no permite borrar el teléfono ni el país (limitación aceptada; se borra desde Administración). | `Driver.Update` |
| D13 | **Permisos:** `POST /drivers` y `PATCH /drivers/{id}` pasan a una política nueva, `DriverCatalogAccess`, con Admin, Receiving, Scale, ForeignTrade y **Warehouse**. Bodega necesita crear y editar desde la Recepción Directa. Los vehículos siguen en `TransportCatalogAccess`, sin Warehouse. Se afloja por endpoint, no por controlador. | Convención del proyecto; D1 |
| D14 | **Contrato con los padres.** El selector emite lo mismo que emitía `DriverForm` (`update:modelValue` con `Partial<IDriverFormData>` y `edited`). Por eso `getEntryInfo()` (Báscula), `buildManualReceptionRequest()` (Bodega) y el backend al guardar no cambian. | Mínimo cambio |
| D15 | **País del conductor (WMS-6 D06):** si el conductor seleccionado no tiene país, el dato emitido toma:<br>1. el país del vehículo del ingreso;<br>2. si no hay, el recordado en la sesión (`useEntryFormMemory().prefill("driverCountry")`).<br>Debajo del select se muestra «País: {país} (del vehículo)» o «(recordado)». Nunca pisa el país que trae el conductor. | `DriverForm.applyCountryFallback` |
| D16 | **Precarga.** Si los datos iniciales traen tipo y número de documento (camión al que Vigilancia o una edición anterior ya le asignó conductor, u operación retomada), al montar se consulta `GET weighbridge/drivers/by-document`:<br>• **si existe**, queda seleccionado con su Id y el lápiz se habilita;<br>• **si no existe**, se crea una opción local con los datos iniciales, sin Id, y el lápiz queda deshabilitado.<br>La opción seleccionada se conserva aunque una búsqueda posterior no la traiga, como en `WarehouseDepositSelect`. | Patrón existente |
| D17 | En Báscula, los cuatro faltantes del conductor (tipo, número, apellidos y nombres) se unifican en uno:<br>• clave `driverId`;<br>• etiqueta «conductor»;<br>• selector `#driverId [role='combobox']`.<br>El criterio de «completo» no cambia: los cuatro datos presentes. | `CompleteEntryInfo.missingFields` |
| D18 | En Bodega, las cuatro validaciones del conductor se reemplazan por una: «Conductor requerido: selecciónelo o regístrelo con «+».». | `ReceptionStepManualInfo.vue:144-147` |
| D19 | `DriverForm.vue` sigue siendo el formulario del conductor. Gana props opcionales que no cambian su comportamiento por defecto (§5.3). Se reutiliza dentro del modal. | Petición del usuario («muestre el formulario actual») |
| D20 | Los defectos que salgan en QA siguen la serie de regresión: **DEF-F11-023** en adelante, registrados en `INDICE.md`. Los casos nuevos continúan cada bloque:<br>• `F3-CAM-013…`;<br>• `F4-RSB-008…`;<br>• `F9-API-022…`. | `docs/qa/00-plan-maestro.md` §2.5 |

---

## 3. Mapa de archivos

### Backend (`Backend/wms-api`)

| Archivo | Cambio |
|---|---|
| `Wms.Application/Logistics/Drivers/Queries/GetAllDrivers/GetAllDriversQuery.cs` | `Search` y `OrderByName` |
| `Wms.Application/Logistics/Drivers/Queries/GetAllDrivers/GetAllDriversHandler.cs` | Filtro D4, orden D5 |
| `Wms.Domain/Security/WmsPolicyRoles.cs` | Constante y roles de `DriverCatalogAccess` |
| `Wms.Api/Controllers/v1/DriverController.cs` | `CreateDriver` y `UpdateDriver` → `DriverCatalogAccess` |
| `Wms.Tests/Security/WmsPolicyRolesTests.cs` | Fila y prueba de la política nueva |
| `Wms.Tests/Security/ControllerAuthorizationTests.cs` | Filas 41-42 → `DriverCatalogAccess` |
| `Wms.IntegrationTests/Logistics/DriverSearchTests.cs` | **Nuevo** |
| `Wms.IntegrationTests/Security/CatalogWriteAuthorizationTests.cs` | Pruebas de Warehouse (§4.3) |

### Frontend (`Frontend/wms`)

| Archivo | Cambio |
|---|---|
| `app/features/entries/services/driver-service.ts` | `IGetDriversQuery`: `search?`, `orderByName?` |
| `app/features/entries/utils/driver-option.ts` | **Nuevo**: utilidades puras (§5.1) |
| `app/features/entries/components/DriverForm.vue` | Props y emit opcionales (§5.3) |
| `app/features/entries/components/DriverFormDialog.vue` | **Nuevo**: modal de alta y edición (§5.4) |
| `app/features/entries/components/DriverPicker.vue` | **Nuevo**: select + «+» + lápiz (§5.5) |
| `app/features/weighbridge/components/CompleteEntryInfo.vue` | Usa `DriverPicker`; faltantes D17; `ID_TYPE_LABELS` desde la utilidad |
| `app/features/warehouse/components/ReceptionStepManualInfo.vue` | Usa `DriverPicker`; validación D18 |
| `test/unit/entries/driver-option.spec.ts` | **Nuevo** |
| `test/components/entries/DriverPicker.spec.ts` | **Nuevo** |
| `test/components/entries/DriverFormDialog.spec.ts` | **Nuevo** |
| `test/components/warehouse/ReceptionStepManualInfo.spec.ts` | Stub `DriverForm` → `DriverPicker`; validación D18 |

### Documentación

| Archivo | Cambio |
|---|---|
| `Frontend/wms/docs/qa/fase-03-bascula.md`, `fase-04-bodega.md`, `fase-09-roles-permisos.md` | Casos (§7.1) |
| `Frontend/wms/docs/qa/resultados/SEL-informe-2026-10-XX.md` | **Nuevo**: informe (§7.3) |
| `Frontend/wms/docs/qa/resultados/defectos/INDICE.md` | Si hay defectos |
| `Backend/wms-api/docs/guiones/guiones-video-tutoriales.md` | Pasos de Báscula y Bodega con el conductor (§7.4) |
| `Backend/wms-api/docs/migracion-staging/resultados/guia-pruebas-operarios.md` | Ídem (§7.4) |

---

## 4. Fase 1 — Backend

### 4.1 Búsqueda (B-1)

En `GetAllDriversQuery` agrega:

```csharp
/// <summary>Selector de conductor: nombre, apellido, «nombre apellido», «apellido nombre» o documento.</summary>
public string? Search { get; set; }
/// <summary>true: ordena por nombres, apellidos e Id (selector). Sin él, orden de creación (Administración).</summary>
public bool? OrderByName { get; set; }
```

En `GetAllDriversHandler`, después de los filtros existentes y antes del `Select`:

```csharp
if (!string.IsNullOrWhiteSpace(request.Search))
{
    var term = request.Search.Trim();
    var pattern = $"%{term}%";
    var idPattern = $"%{EntryDriverRules.NormalizeIdNumber(term)}%";
    query = query.Where(d =>
        EF.Functions.ILike(EF.Functions.Unaccent(d.FirstName), EF.Functions.Unaccent(pattern)) ||
        EF.Functions.ILike(EF.Functions.Unaccent(d.LastName), EF.Functions.Unaccent(pattern)) ||
        EF.Functions.ILike(EF.Functions.Unaccent(d.FirstName + " " + d.LastName), EF.Functions.Unaccent(pattern)) ||
        EF.Functions.ILike(EF.Functions.Unaccent(d.LastName + " " + d.FirstName), EF.Functions.Unaccent(pattern)) ||
        EF.Functions.ILike(d.IdNumber, idPattern));
}
```

**Orden:**

- con `OrderByName == true`: `OrderBy(FirstName).ThenBy(LastName).ThenBy(Id)`;
- sin él: el actual, `OrderBy(CreatedAt).ThenBy(Id)`.

Ordena sobre la entidad **antes** de proyectar al DTO, como `GetCrewsHandler`. No cambies el resto del handler ni el `PaginatedList.CreateAsync`.

`EntryDriverRules` vive en `Wms.Application.Weighbridge.Common.Services`; agrega el `using`.

No agregues índices: son 4.361 filas en staging y el patrón `%x%` no usa índice B-tree.

### 4.2 Política (B-2)

En `WmsPolicyRoles`:

1. agrega la constante `DriverCatalogAccess = "DriverCatalogAccess"`;
2. agrega su entrada en `Roles`, con Admin, Receiving, Scale, ForeignTrade y Warehouse (en ese orden, junto a `TransportCatalogAccess`);
3. agrega el comentario `// Selector de conductor (2026-10-08): Bodega registra y corrige conductores desde la Recepción Directa.`

`WmsAuthentication` registra las políticas recorriendo `Roles`: no lo toques.

En `DriverController`, `CreateDriver` y `UpdateDriver` pasan a `[Authorize(Policy = "DriverCatalogAccess")]`. `VehicleController` no cambia.

### 4.3 Pruebas (B-3)

**`Wms.Tests`:**

- `WmsPolicyRolesTests`: fila de la tabla y prueba `DriverCatalogAccess_IsAdminReceivingScaleForeignTradeWarehouse`;
- `ControllerAuthorizationTests`: filas de `CreateDriver` y `UpdateDriver` con `"DriverCatalogAccess"`.

**`Wms.IntegrationTests/Logistics/DriverSearchTests.cs`** (colección `Api`, `[Trait("Category","Integration")]`):

- **Siembra:** crea por API, como Admin, sus propios conductores con un sufijo único por ejecución, por ejemplo `var tag = Guid.NewGuid().ToString("N")[..6]`. La base es compartida.
- **Casos:**
  1. `Search_ByAccentlessFirstName_FindsAccentedDriver`: «Zúñiga{tag}» se encuentra con «zuniga{tag}».
  2. `Search_ByFullNameInBothOrders`: «Mario{tag} Benavides» se encuentra con «mario{tag} benavides» y con «benavides mario{tag}».
  3. `Search_ByDocumentFragment_IgnoresSpaces`: documento `9{tag-numérico}123`, buscado con un fragmento y con espacios intercalados.
  4. `Search_Paginates`: tres conductores con el mismo `tag`; `pageSize=2` → 2 ítems, `totalCount=3`, `totalPages=2`.
  5. `Search_WithIsActive_ExcludesInactive`: desactiva uno con `PATCH isActive=false`; `isActive=true` no lo trae.
  6. `OrderByName_SortsByFirstThenLastName`: el orden de la respuesta es por nombres y luego apellidos.
  7. `WithoutSearch_KeepsCreationOrder`: sin `search` ni `orderByName`, se mantiene el orden por `CreatedAt`.

**`CatalogWriteAuthorizationTests`:**

- `Warehouse_CreateDriver_IsNotForbidden`;
- `Warehouse_UpdateDriver_IsNotForbidden`;
- `Warehouse_CreateVehicle_Returns403`;
- `Billing_CreateDriver_Returns403`.

### 4.4 Verificación de la fase

```bash
dotnet build
dotnet test Wms.Tests
dotnet test Wms.IntegrationTests
dotnet ef migrations has-pending-model-changes --project Wms.Infrastructure --startup-project Wms.Api
```

- Anota los conteos antes y después. Todo debe quedar verde.
- La última orden (`has-pending-model-changes`) debe quedar limpia.

---

## 5. Fase 2 — Frontend

### 5.1 Utilidades puras: `app/features/entries/utils/driver-option.ts`

```ts
export const ID_TYPE_SHORT_LABELS: Record<string, string> =
  { Cc: "CC", Nit: "NIT", Rut: "RUT", Pasaporte: "Pasaporte", Ruc: "RUC" };

/** D7 — «Nombres Apellidos · CC 123». */
export const driverOptionLabel = (d: Pick<IDriver, "firstName" | "lastName" | "idType" | "idNumber">): string

/** D14 — Datos que el selector emite a los padres. */
export const toDriverFormData = (d: IDriver, country: string): IDriverFormData

/** D15 — País del conductor; si no tiene, el del vehículo y luego el recordado. */
export const resolveDriverCountry = (
  driverCountry: string | null | undefined,
  vehicleCountry: string | null | undefined,
  remembered: string | null | undefined,
): { country: string; source: "driver" | "vehicle" | "memory" | "none" }

/** D10 — ¿El operario cambió algo editable respecto al conductor encontrado? (trim; null ≡ ""). */
export const driverEditableFieldsChanged = (found: IDriver, form: IDriverFormData): boolean

/** Documento sin espacios, igual que EntryDriverRules.NormalizeIdNumber. */
export const normalizeIdNumber = (value: string): string
```

`CompleteEntryInfo.vue` reemplaza su `ID_TYPE_LABELS` local por `ID_TYPE_SHORT_LABELS`.

### 5.2 Servicio

En `IGetDriversQuery` agrega `search?: string` y `orderByName?: boolean`.

`useDrivers`, `useCreateDriver` y `useUpdateDriver` ya existen y ya invalidan `["drivers"]`: úsalos tal cual.

### 5.3 `DriverForm.vue` (props nuevas, comportamiento por defecto intacto)

| Prop / emit | Tipo, por defecto | Efecto |
|---|---|---|
| `hideHeader` | `boolean`, `false` | Oculta el bloque `h4` «Información del Conductor» y su párrafo. Lo usa el modal. |
| `lockDocument` | `boolean`, `false` | El tipo de documento (`Select`) queda `disabled` y el número (`InputText`) `readonly`. **No busca por documento.** |
| `submitLabel` | `string`, `"Guardar Información del Conductor"` | Texto del botón de `showSubmit`. |
| `submitting` | `boolean`, `false` | Botón con `loading` y deshabilitado. |
| `found` (emit) | `(driver: IDriver)` | Se emite cuando `searchDriverByDocument` encuentra un conductor, además de lo que ya hace. |

`getDriverByDocument` devuelve `any`. Tipa su resultado como `IDriver | null` dentro de `DriverForm` al emitir `found`.

### 5.4 `DriverFormDialog.vue` (nuevo)

**Props:**

- `visible: boolean`;
- `mode: "create" | "edit"`;
- `driver?: IDriver | null` (requerido en `edit`);
- `vehicleCountry?: string | null`.

**Emits:**

- `update:visible`;
- `saved(driver: IDriver)`.

**Estructura:**

- `Dialog` modal con `:style="{ width: '640px' }"` y `:breakpoints="{ '640px': '95vw' }"`.
- Encabezado: «Registrar conductor» (create) o «Editar conductor» (edit). No se cierra mientras guarda.
- **El contenido va con `v-if="visible"`**: cada apertura monta un `DriverForm` limpio.
- Dentro, `DriverForm` con:
  - `hideHeader`, `showSubmit` y `:vehicle-country`;
  - `:initial-data`: vacío en create; los datos del `driver` en edit;
  - `:lock-document="mode === 'edit'"`;
  - `:submitting`;
  - `submitLabel`: «Registrar conductor» en create, «Usar este conductor» si hubo `found` (D10) y «Guardar cambios» en edit.
- Debajo del formulario, un botón «Cancelar» (`severity="secondary"`, `outlined`).
- Con `found` en create, un `Message severity="info"`: «Este conductor ya está registrado.».

**Al enviar (`@submit` de `DriverForm`, ya validado por zod):**

| Caso | Acción | Aviso (`useWmsToast`) | Resultado |
|---|---|---|---|
| create, sin `found` | `useCreateDriver().mutateAsync({ firstName: trim, lastName: trim, idType, idNumber: normalizeIdNumber, country: valor o null, phoneNumber: trim o null })` | `showSuccess("Conductor registrado", "{Nombres Apellidos} quedó seleccionado.")` | `saved(driver)`; cerrar |
| create, 409 | D11 | `showInfo` con el texto de D11 | Seleccionar el conductor existente; cerrar |
| create, con `found` | Si `driverEditableFieldsChanged`, `useUpdateDriver` con los cuatro campos (D12) | — | `saved(driverActualizado ?? found)`; cerrar |
| edit | `useUpdateDriver().mutateAsync({ id: driver.id, data: { firstName, lastName, country, phoneNumber } })` (D12) | Ninguno propio: el composable ya muestra «Conductor actualizado exitosamente» | `saved(respuesta)`; cerrar |
| Cualquier otro error | — | El aviso global ya muestra el mensaje | El modal sigue abierto |

**Firmas de las mutaciones:**

- `useUpdateDriver` recibe `{ id, data }` y ya muestra sus propios avisos de éxito y de error (`useMutations.ts:58`). No agregues otro aviso de éxito y no cambies el composable.
- `useCreateDriver` no muestra avisos: el aviso de éxito de create es el de la tabla.
- Para distinguir el 409, usa `normalizeApiError` / `ApiError` de `app/utils/api-error.ts`.
- En el 409, `claimApiError` evita el aviso duplicado; revisa cómo lo usan otros diálogos (`grep claimApiError`).

### 5.5 `DriverPicker.vue` (nuevo)

**Props:**

- `initialData?: Partial<IDriverFormData>`;
- `vehicleCountry?: string | null`;
- `compact?: boolean`, por defecto `false`;
- `invalid?: boolean`;
- `inputId?: string`, por defecto `"driverId"`.

**Emits** (los mismos que `DriverForm`):

- `update:modelValue(Partial<IDriverFormData>)`;
- `edited()`.

**Estado:**

- `search` (crudo, de `@filter`) y `debouncedSearch` (`refDebounced(search, 300)`);
- `selected: IDriver | (IDriverFormData sin Id) | null` (D16).

**Consulta:**

```ts
useDrivers(computed(() => ({ search: debouncedSearch.value.trim() || undefined, isActive: true, orderByName: true, pageIndex: 1, pageSize: 20 })))
```

**Opciones:**

- Los resultados del servidor, con la opción `selected` al inicio si no viene entre ellos.
- Cada opción tiene la forma `{ value: id | "doc:{tipo}:{número}", label: driverOptionLabel(...), filterText: \`${label} ${search.value}\`, driver }`.

**Plantilla.** En una fila: `Select`, botón «+» y botón lápiz.

`Select`:

- `:id="inputId"`, `filter`, `:filter-fields="['filterText']"` (D8);
- `filter-placeholder="Nombre o documento"`, `auto-filter-focus`, `reset-filter-on-hide`, `show-clear`, `fluid`;
- `:loading` e `:invalid`;
- `placeholder="Buscar conductor"`;
- `empty-filter-message="Sin resultados. Use «+» para registrar el conductor."`;
- `empty-message` con el mismo texto;
- slot `#footer` con el texto de D6 cuando `pagination.totalCount > opciones del servidor`.

Botón «+»:

- `icon="pi pi-plus"`, `severity="secondary"`, `outlined`;
- `aria-label="Registrar conductor nuevo"` y `v-tooltip.top="'Registrar conductor nuevo'"`;
- abre `DriverFormDialog` en modo create.

Botón lápiz:

- `icon="pi pi-pencil"`, `severity="secondary"`, `outlined`;
- `aria-label="Editar conductor"` y el mismo tooltip;
- `:disabled` mientras `selected` no tenga `id`;
- abre el modal en modo edit con `selected`.

Etiqueta del campo:

- `compact`: `LabelBase for=inputId required` con el texto «Conductor», dentro de `div.wb-field` (estilo de la ficha de báscula);
- no `compact`: el mismo `LabelBase` dentro de `div.field`.

Ayudas:

- debajo, `small` con el país de D15 (`wb-help` en compact, `text-muted-color` fuera);
- con `invalid` en compact, `small.wb-error` «Requerido».

**Comportamiento:**

| Situación | Efecto |
|---|---|
| Elegir una opción | `selected = driver`; emitir `toDriverFormData(driver, país D15)` y `edited`. |
| Limpiar (`show-clear`) | `selected = null`; emitir los seis campos en `""` y `edited`. |
| `saved(driver)` del modal | `selected = driver`; emitir como al elegir; `edited`; devolver el foco al combobox (`#inputId [role='combobox']`). |
| Montaje (D16) | Si `initialData` trae tipo y número, consultar `WeighbridgeService().getDriverByDocument`. Si existe, `selected` con Id; si no, la opción local. **No emitir `edited`**: es una precarga. Emitir `update:modelValue` solo si el país cambió por D15. |
| Cambia `vehicleCountry` | Si `selected` no tiene país propio, volver a emitir con el país nuevo, sin `edited`. |

### 5.6 Padres

**`CompleteEntryInfo.vue`:**

- reemplaza `<DriverForm …compact>` por `<DriverPicker :initial-data="driverData" :vehicle-country="vehicleData.vehicleCountry" :invalid="invalidFields.includes('driverId')" compact @update:model-value="onDriverDataChange" @edited="isDirty = true" />`;
- aplica D17 en `missingFields`;
- actualiza el comentario de cabecera: búsqueda y alta del conductor con el selector.

**`ReceptionStepManualInfo.vue`:**

- reemplaza `<DriverForm>` por `<DriverPicker :initial-data="driverData" :vehicle-country="vehicleData.vehicleCountry" @update:model-value="onDriverDataChange" />` dentro de la misma `Card`;
- aplica D18;
- actualiza el comentario de la línea 5.

### 5.7 Pruebas

**`test/unit/entries/driver-option.spec.ts`:**

- etiqueta para los cinco tipos;
- `toDriverFormData`;
- las cuatro fuentes de `resolveDriverCountry`;
- `driverEditableFieldsChanged`: igual, cambia nombre, `null` vs `""`, espacios;
- `normalizeIdNumber`.

**`test/components/entries/DriverPicker.spec.ts`** (`// @vitest-environment nuxt`, `mountSuspended`; mock de `useDrivers` y del servicio de báscula, con el estilo de `AdditionalDepositCollect.spec.ts`):

1. con `initialData` y conductor encontrado, muestra su etiqueta y el lápiz está habilitado;
2. con `initialData` y conductor no encontrado, muestra la opción local y el lápiz está deshabilitado;
3. elegir una opción emite `IDriverFormData` y `edited`;
4. limpiar emite los campos vacíos;
5. `@filter` con «mar» consulta `search: "mar"` después del *debounce* (temporizadores falsos);
6. el pie aparece con `totalCount = 4361`;
7. «+» abre el modal en create; `saved` selecciona y emite;
8. el conductor sin país emite el país del vehículo.

**`test/components/entries/DriverFormDialog.spec.ts`:**

1. create llama a `createDriver` con el documento normalizado y emite `saved`;
2. el 409 consulta por documento y emite `saved` con el existente;
3. con `found` y sin cambios, no llama a `PATCH`;
4. con `found` y nombre cambiado, llama a `PATCH` con cuatro campos;
5. edit llama a `PATCH` sin tipo ni número.

**`ReceptionStepManualInfo.spec.ts`:** stub `DriverPicker` en lugar de `DriverForm`. Ajusta o agrega la aserción del mensaje de D18.

### 5.8 Verificación de la fase

```bash
yarn test
yarn lint -f json -o <scratchpad>/lint.json
```

- `yarn test` debe quedar todo verde.
- Mide los errores de lint en `HEAD` antes de empezar; al terminar deben ser **iguales o menos**.
- Las guardias de `test/unit/guards` deben pasar. En particular, todo botón con `aria-label`.
- `vue-tsc` con un tsconfig temporal limitado a los archivos tocados, que extienda `.nuxt/tsconfig.app.json`, instalado en el scratchpad (ver la memoria del plan de corrección QA).
- **Prueba manual en local** (API en 5281, front en 3000), con las cuentas `bascula` y `bodega`:
  - el selector en la card de báscula;
  - «+», lápiz y guardar la ficha;
  - la Recepción Directa hasta antes de «Guardar».

  Esta prueba no reemplaza la Fase 3.

---

## 6. Rendimiento y teclado (criterios de aceptación de la Fase 2)

- La ficha de báscula **no suma clics** en el caso más común: Tab al select, escribir 3-4 caracteres, Enter para elegir y Tab a lo siguiente.
- Con el conductor ya asignado, no se toca el campo.
- Enter dentro del filtro del select **elige la opción resaltada**; no dispara el «Guardar» de la ficha. Verifícalo: si lo dispara, detente y repórtalo.
- El modal se abre con el foco en «Tipo de Documento». Esc lo cierra si no está guardando.

---

## 7. Fase 3 — Registro y ejecución en QA (local)

### 7.1 Casos nuevos en el plan de QA

**`docs/qa/fase-03-bascula.md`, §6.2 CAM.**

Reescribe en el sitio, con el mismo ID, estos tres casos:

| ID | Pasos | Esperado |
|---|---|---|
| F3-CAM-003 | Guardar sin transportadora, país, tipo o conductor. | No guarda. El faltante del conductor es uno solo, «conductor», y el foco va al select. |
| F3-CAM-004 | Escribir parte del nombre de un conductor de F1. | Aparece «Nombres Apellidos · CC n»; al elegirlo, el resumen de la card lo muestra. País del conductor = el del vehículo si el conductor no tiene. |
| F3-CAM-005 | «+» → documento nuevo, nombres y apellidos → «Registrar conductor». | El modal se cierra, el conductor queda seleccionado y existe en Admin → Conductores **antes** de guardar la ficha. |

Agrega estos casos:

| ID | Caso | Esperado | P | Tipo |
|---|---|---|---|---|
| F3-CAM-013 | Buscar por documento (fragmento) | Lo encuentra | P0 | FUN |
| F3-CAM-014 | Sin tildes / «apellido nombre» | Lo encuentra (D4) | P1 | FUN |
| F3-CAM-015 | Pie de paginación | Sin texto: «Mostrando 20 de N…» | P2 | UI |
| F3-CAM-016 | «+» con documento existente | Aviso «ya está registrado», botón «Usar este conductor»; sin duplicado en Admin | P1 | RN |
| F3-CAM-017 | Lápiz: corregir el teléfono | Documento bloqueado; el cambio se ve en Admin; el select refleja el dato | P1 | FUN |
| F3-CAM-018 | Lápiz sin selección | Deshabilitado | P2 | UI |
| F3-CAM-019 | Reabrir una operación con conductor (`?resume=`) | Conductor preseleccionado (D16), sin «Faltan» por conductor | P1 | PER |
| F3-CAM-020 | Guardar y verificar el ingreso | El ingreso queda con el conductor elegido (historial de Vigilancia o trazabilidad); el conductor anterior no cambia (DEF-F11-008) | P0 | PER |
| F3-CAM-021 | Solo teclado | Tab, texto, Enter y Tab, sin ratón; Enter en el filtro no guarda la ficha | P1 | UX |
| F3-CAM-022 | Conductor inactivo | No aparece en la búsqueda | P2 | RN |

**`docs/qa/fase-04-bodega.md`, §RSB.** Agrega:

| ID | Caso | Esperado | P | Tipo |
|---|---|---|---|---|
| F4-RSB-008 | Recepción directa con el selector | Elegir un conductor existente; el depósito se crea y la recepción muestra ese conductor | P0 | FUN |
| F4-RSB-009 | «+» desde Bodega con `bodega` | Crea el conductor (sin 403) y lo selecciona | P0 | ROL |
| F4-RSB-010 | Lápiz desde Bodega | Guarda (sin 403) | P1 | ROL |
| F4-RSB-011 | Sin conductor | Mensaje D18 | P1 | VAL |

**`docs/qa/fase-09-roles-permisos.md`, §API.** Agrega:

| ID | Caso | Esperado | P | Tipo |
|---|---|---|---|---|
| F9-API-022 | `POST`/`PATCH /drivers` con Warehouse | No 403 | P1 | SEG |
| F9-API-023 | `POST /vehicles` con Warehouse | 403 | P1 | SEG |
| F9-API-024 | `POST /drivers` con Billing | 403 | P1 | SEG |
| F9-API-025 | `GET /drivers?search=` sin sesión | 401 | P2 | SEG |

### 7.2 Ejecución local

- Base local (`wmsdb` o `wms_migracion`, la que esté en uso; anótala) con el build de las Fases 1 y 2 commiteado. Anota los hashes.
- **Ejecuta:**
  - los casos de §7.1;
  - la regresión dirigida F3-REG-001 (registro IMP mínimo), F3-CAM-010 y F3-CAM-011 (persistencia en Solo báscula y Salida) y F4-RSB-002;
  - la medición del API: `GET /drivers?search=…&isActive=true&orderByName=true&pageSize=20` con 5 términos, `curl -w '%{time_total}'`. Criterio: cada respuesta < 1 s.
- **Datos:** usa la marca `QA-SEL` en nombres, observaciones y documentos (`9000000001`…). No edites conductores que no hayas creado tú.
- **Defectos:** fichas DEF-F11-023 y siguientes, con `plantillas/defecto.md` y una fila en `INDICE.md`.

### 7.3 Informe

Crea `docs/qa/resultados/SEL-informe-{fecha}.md` con `plantillas/informe-fase.md`:

- datos, hashes y base;
- criterios de entrada;
- resultado por caso;
- defectos;
- datos creados;
- veredicto local: «Listo para staging» o «No listo», con motivo.

Deja la sección «Staging» vacía para la Fase 4.

### 7.4 Documentación de usuario

En `docs/guiones/guiones-video-tutoriales.md`, reemplaza la captura del conductor campo por campo por «elige el conductor en el selector (búscalo por nombre o documento); si no existe, «+»». Aplica:

- en el paso 2 del guion de registro en Báscula (línea ~654);
- en el paso 1 del de depósito (línea ~671);
- en el paso de la Recepción Directa si lo describe (`grep -n "Recepción Directa"`).

En `guia-pruebas-operarios.md`, ajusta los pasos de Báscula y Bodega que piden digitar el conductor.

No cambies otros pasos.

**Checkpoint de la Fase 3:** informe con veredicto local. El usuario commitea los documentos.

---

## 8. Fase 4 — Despliegue a staging y QA en staging

**Precondiciones:**

- Fases 1-3 commiteadas y veredicto local «Listo para staging».
- El usuario autoriza la fase.
- Respeta las reglas de staging de `docs/migracion-staging/prompt-fase-2.md` y `prompt-fase-4.md`:
  - sin secretos;
  - sin SQL de escritura;
  - no se borran volúmenes ni se recrea la base.

### 8.1 Antes de desplegar

1. **Qué entra.** Lista los commits que entran:

   ```bash
   git log --oneline 84c712f..HEAD
   ```

   ```bash
   git log --oneline 8527144..HEAD
   ```

   Si `docs/migracion-staging/plan-migracion-legacy-staging.md` registra un redespliegue posterior, usa esos hashes. Anótalos en el informe.
2. **Migraciones.** Comprueba que no entra ninguna:

   ```bash
   git diff --stat 84c712f..HEAD -- Wms.Infrastructure/Migrations
   ```

   La salida debe estar vacía (siguen las 11 migraciones). **Si hay migraciones, detente**: aplicarlas en staging exige la aprobación del usuario.
3. **Respaldo manual** (`POST administration/backups/run`) con resultado `Succeeded`. Anota el archivo. Las credenciales del Admin están en `db_legacy/trabajo/.admin-staging.local`: léelas sin imprimirlas.

### 8.2 Despliegue (`Backend/wms-api/scripts/deploy-staging.sh`)

1. `backend`, luego `up`. No hacen falta `config` ni `migrate`: no cambian el compose, el Caddyfile ni el esquema.
2. `frontend` (genera con la URL del API de staging y sincroniza).
3. `smoke`.

**No toques `pgdata` ni `caddy_data`.**

### 8.3 QA en staging

**Cuentas:**

- `qa.bascula`, `qa.bodega`, `qa.vigilancia` y `qa.facturacion` (credenciales en `credenciales-qa-staging.local.md`, columna 5, sin imprimir).
- En el navegador integrado inicia sesión el usuario; tú usas su sesión.

**Datos:**

- marca `QA-SEL`;
- placas nuevas `QSL801` y `QSL802`;
- conductores nuevos `QA-SEL Uno` / `QA-SEL Dos`, documentos CC `9000000801` y `9000000802`.

**Prohibido:**

- editar conductores reales (migrados);
- usar los camiones de práctica P1-P6 (CAH514 es de PRF-002).

**Casos:**

| # | Prueba | Criterio |
|---|---|---|
| S1 | API con `qa.bascula`: `search` con 5 términos sobre los 4.361 migrados (un apellido común, un fragmento de cédula, un término sin tildes) | Resultados pertinentes, `pageSize` 20, `totalCount` coherente, cada respuesta < 1 s |
| S2 | API: F9-API-022 a 024 con `qa.bodega` y `qa.facturacion` | Según §7.1. Para no crear basura, `POST /drivers` con cuerpo inválido `{}` → 400 (no 403); `PATCH` sobre `QA-SEL Uno` |
| S3 | `qa.vigilancia` registra el ingreso `QSL801` (motivo «Solo Báscula», observación «QA-SEL») | En la cola de báscula |
| S4 | `qa.bascula`: tomar `QSL801` y ejecutar F3-CAM-004, 005 (crea `QA-SEL Uno`), 013, 016 (con `9000000801`), 017 (sobre `QA-SEL Uno`) y 021 | Según §7.1 |
| S5 | Guardar el registro de `QSL801` («Solo báscula» con un cliente QA de S6) y verificar F3-CAM-020 | Ingreso con `QA-SEL Uno` |
| S6 | Limpieza de `QSL801`: descartar la operación en «Recuperar operaciones» (sin cobro ni factura) y registrar la salida en Vigilancia | Fuera de la cola y de planta |
| S7 | `qa.bodega`: en «Recepción Directa» elegir `QSL802` (ingreso de `qa.vigilancia`, motivo «Solo bodega», «QA-SEL») y ejecutar F4-RSB-009 (crea `QA-SEL Dos`), 010 y 011. **No guardar la recepción** (crearía un depósito) | Sin 403; selección correcta |
| S8 | Limpieza: salida de `QSL802` en Vigilancia | Fuera de planta |
| S9 | Humo: login de las cuentas `qa.*`; detalle de BA0042; cola de báscula sin camiones `QSL` | Sin cambios inesperados |

**Al terminar:**

1. Respaldo final con resultado `Succeeded`.
2. Evidencia sin secretos en `docs/qa/resultados/evidencias/SEL/`.
3. Completa la sección «Staging» del informe, con el veredicto «Verificado en staging» o «Reabierto», más defectos y hashes desplegados.
4. Agrega una línea al estado del plan de migración (`plan-migracion-legacy-staging.md`) con el redespliegue: hashes, fecha y respaldo.
5. Anota en el informe que **PRF-002** (cronometraje de báscula con un operario) debe medirse con este build, porque cambia la card del conductor.

**Checkpoint de la Fase 4.** Propón al usuario los mensajes de commit:

- `docs(qa): selector de conductor verificado en staging`;
- `docs(migracion): redespliegue de staging con el selector de conductor`.

---

## 9. Orden y checkpoints

| Fase | Repo | Entrega | El agente se detiene y… |
|---|---|---|---|
| 1 | Backend | §4 con pruebas verdes | resume; el usuario commitea, por ejemplo `feat(conductores): búsqueda paginada por nombre o documento y alta desde Bodega` |
| 2 | Frontend | §5 y §6 con pruebas verdes, lint ≤ base | resume; el usuario commitea, por ejemplo `feat(bascula,bodega): selector de conductor con alta y edición en modal` |
| 3 | Docs QA | §7: casos, ejecución local, informe, guiones | entrega el veredicto local; el usuario commitea |
| 4 | Staging | §8 | entrega el informe de staging y los mensajes de commit |

---

## 10. Riesgos conocidos

| Riesgo | Mitigación |
|---|---|
| El filtrado local de PrimeVue oculta resultados del servidor | D8; F3-CAM-014 lo prueba |
| Enter en el filtro dispara el «Guardar» de la ficha | §6; F3-CAM-021. Si ocurre, detenerse y reportar |
| Precarga asíncrona que pisa una selección del operario (patrón de F3-CAM-007) | La consulta de D16 no reemplaza `selected` si el operario ya eligió otro antes de que responda |
| Bodega con 403 al crear | D13; F4-RSB-009 y la prueba de integración |
| Ampliar permisos de más | Política nueva solo para conductores; vehículos sin cambio (F9-API-023) |
| Conductores reales modificados en staging | Prohibición explícita en §8.3 |
